import os
import tkinter as tk
from tkinter import ttk
import pygame
import threading
import time
import cv2
import mediapipe as mp
from mediapipe import Timestamp


class AudioPlayer:
    def __init__(self, window):
        self.window = window
        self.window.title("Audio Player")
        self.window.geometry("350x400")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.resizable(False, False)

        self.BaseOptions = mp.tasks.BaseOptions
        self.GestureRecognizer = mp.tasks.vision.GestureRecognizer
        self.GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        self.GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        self.cap = None  # Initialize the video capture to None
        self.volume = 0.5
        self.waitval = 0

        pygame.init()
        pygame.mixer.init()
        self.load_music_files()

        self.track = tk.StringVar()
        self.status = tk.StringVar()
        self.duration = tk.StringVar()
        self.duration.set("Duration: 0:00")

        trackframe = ttk.Frame(window)
        trackframe.pack(pady=10)

        self.tracklabel = ttk.Label(trackframe, textvariable=self.track)
        self.tracklabel.pack()

        statusframe = ttk.Frame(window)
        statusframe.pack(pady=10)

        self.statuslabel = ttk.Label(statusframe, textvariable=self.status)
        self.statuslabel.pack()

        durationframe = ttk.Frame(window)
        durationframe.pack(pady=10)

        self.durationlabel = ttk.Label(durationframe, textvariable=self.duration)
        self.durationlabel.pack()

        buttonframe = ttk.Frame(window)
        buttonframe.pack(pady=10)

        self.style = ttk.Style()
        self.style.configure('Green.TButton', foreground='black', background='green', padding=(4, 4))
        self.style.configure('Red.TButton', foreground='black', background='red', padding=(4, 4))
        self.style.configure('Blue.TButton', foreground='black', background='blue', padding=(4, 4))

        self.playbutton = ttk.Button(buttonframe, text="Play", command=self.play_song, style='Green.TButton')
        self.playbutton.grid(row=0, column=0, padx=2, pady=2)

        self.stopbutton = ttk.Button(buttonframe, text="Stop", command=self.stop_song, style='Red.TButton')
        self.stopbutton.grid(row=0, column=1, padx=2, pady=2)

        self.prevbutton = ttk.Button(buttonframe, text="<< Prev", command=self.prev_song, style='Blue.TButton')
        self.prevbutton.grid(row=1, column=0, padx=2, pady=2)

        self.nextbutton = ttk.Button(buttonframe, text="Next >>", command=self.next_song, style='Blue.TButton')
        self.nextbutton.grid(row=1, column=1, padx=2, pady=2)

        scaleframe = ttk.Frame(window)
        scaleframe.pack(pady=10)

        self.volumelabel = ttk.Label(scaleframe, text="Volume:")
        self.volumelabel.grid(row=0, column=0)

        self.volumescale = ttk.Scale(scaleframe, from_=0, to=1.0, orient=tk.HORIZONTAL,
                                     command=self.set_volume)
        self.volumescale.set(0.5)
        pygame.mixer.music.set_volume(0.5)
        self.volumescale.grid(row=0, column=1)

        self.progressbar = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=300, mode="determinate")

        self.update_duration_thread = threading.Thread(target=self.update_duration)
        self.update_duration_thread.daemon = True  # Allow the thread to exit when the main program exits
        self.update_duration_thread.start()

    def load_music_files(self):
        self.music = []
        music_folder = "music"  # Specify the folder name where your music files are located
        for filename in os.listdir(music_folder):
            if filename.endswith((".mp3", ".wav", ".m4a")):
                file_path = os.path.join(music_folder, filename)  # Correct the path to the music folder
                self.music.append(file_path)  # Append the full file path
        self.current_music = 0
        pygame.mixer.music.load(self.music[self.current_music])

    def update_duration(self):
        while True:
            if pygame.mixer.music.get_busy():
                total_length = pygame.mixer.Sound(self.music[self.current_music]).get_length()
                current_time = pygame.mixer.music.get_pos() / 1000.0
                self.progressbar["value"] = (current_time / total_length) * 100
                minutes = int(current_time // 60)
                seconds = int(current_time % 60)
                self.duration.set(f"Duration: {minutes}:{seconds:02}")
                self.progressbar.update()
            pygame.time.delay(1000)

    def play_song(self):
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
                self.status.set(f"Playing - {self.music[self.current_music]}")

        except Exception as e:
            print(e)
            self.status.set("Error playing song")

    def stop_song(self):
        pygame.mixer.music.stop()
        self.status.set("Stopped")
        self.progressbar["value"] = 0

    def prev_song(self):
        if self.current_music != 0:
            self.current_music -= 1
            pygame.mixer.music.load(self.music[self.current_music])
            self.play_song()

    def next_song(self):
        if self.current_music < len(self.music) - 1:
            self.current_music += 1
            pygame.mixer.music.load(self.music[self.current_music])
            self.play_song()

    def set_volume(self, val):
        pygame.mixer.music.set_volume(float(val))

    def on_closing(self):
        pygame.mixer.music.stop()  # Stop the music when the window is closed
        self.window.destroy()

    def start_gesture_recognition(self):
        gesture_thread = threading.Thread(target=self.gesture_recog)
        gesture_thread.start()

    def gesture_recog(self):
        # Create a gesture recognizer instance with the live stream mode:
        def print_result(result: self.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
            if result and result.gestures:
                top_gesture = result.gestures[0][0]
                print('Top gesture category: {}'.format(top_gesture.category_name))
                if self.waitval == 0:
                    ges = self.gesture_control(top_gesture.category_name, result.handedness[0][0].category_name)
                else:
                    self.waitval -= 1

        options = self.GestureRecognizerOptions(
            base_options=self.BaseOptions(model_asset_path='model.task'),min_hand_detection_confidence=0.5, 
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            result_callback=print_result)
        with self.GestureRecognizer.create_from_options(options) as recognizer:
            self.cap = cv2.VideoCapture(0)  # Open the video capture here

            if not self.cap.isOpened():
                print('Error: Could not open video capture device')
                exit()

            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                frame_timestamp = Timestamp(int(self.cap.get(cv2.CAP_PROP_POS_MSEC)))
                result = recognizer.recognize_async(mp_image, int(frame_timestamp.microseconds()))
                cv2.imshow('Hand Gesture Recognition', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            self.cap.release()
            cv2.destroyAllWindows()

    def gesture_control(self, gesture, hand):
        if gesture == 'reset' or gesture == 'pause':
            self.stop_song()
        elif gesture == 'play':
            self.play_song()
            self.waitval = 5
        elif gesture == 'move' or gesture == 'move2':
            if hand == 'Left':
                self.next_song()
                self.waitval = 15
            elif hand == 'Right':
                self.prev_song()
                self.waitval = 15
        elif gesture == 'volumeup':
            if self.volume <= 1.0:
                self.volume += 0.05
            self.set_volume(self.volume)
            self.volumescale.set(self.volume)
            self.waitval = 2
        elif gesture == 'volumedown':
            if self.volume > 0.0:
                self.volume -= 0.05
            self.set_volume(self.volume)
            self.volumescale.set(self.volume)
            self.waitval = 2

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioPlayer(root)
    app.start_gesture_recognition()
    root.mainloop()
