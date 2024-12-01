import vlc
import tkinter as tk
import os
import time
import threading
import cv2
import mediapipe as mp
from mediapipe import Timestamp

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player")
        self.root.geometry("1280x740")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.BaseOptions = mp.tasks.BaseOptions
        self.GestureRecognizer = mp.tasks.vision.GestureRecognizer
        self.GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        self.GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        self.cap = None

        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.current_file = None
        self.playing_video = False
        self.video_paused = False
        self.playlist = []
        self.current_index = 0
        self.video_directory = "video"
        self.create_widgets()
        self.load_video_files()
        self.current_index = 0
        self.volume = 75
        self.waitval = 0

    def create_widgets(self):
        self.media_canvas = tk.Canvas(self.root, bg="black", width=800, height=400)
        self.media_canvas.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Create a frame to hold buttons horizontally
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=5)

        self.play_button = tk.Button(
            button_frame,
            text="Play",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.play_video,
        )
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(
            button_frame,
            text="Pause",
            font=("Arial", 12, "bold"),
            bg="#FF9800",
            fg="white",
            command=self.pause_video,
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(
            button_frame,
            text="Stop",
            font=("Arial", 12, "bold"),
            bg="#F44336",
            fg="white",
            command=self.stop,
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(
            button_frame,
            text="Next Video",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            command=self.play_next,
        )
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.previous_button = tk.Button(
            button_frame,
            text="Previous Video",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            command=self.play_previous,
        )
        self.previous_button.pack(side=tk.LEFT, padx=5)

        self.fast_forward_button = tk.Button(
            button_frame,
            text="Fast Forward 5s",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            command=self.fast_forward,
        )
        self.fast_forward_button.pack(side=tk.LEFT, padx=5)

        self.rewind_button = tk.Button(
            button_frame,
            text="Rewind 5s",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            command=self.rewind,
        )
        self.rewind_button.pack(side=tk.LEFT, padx=5)
        self.volume_scale = tk.Scale(
            button_frame,
            label="Volume",
            font=("Arial", 12, "bold"),
            orient=tk.HORIZONTAL,
            from_=0,
            to=100,
            command=self.set_volume,
        )
        self.volume_scale.set(75)
        self.volume_scale.pack(side=tk.LEFT, padx=5)
        

    def load_video_files(self):
        self.playlist = []
        if self.video_directory:
            for file_name in os.listdir(self.video_directory):
                if file_name.lower().endswith((".mp4", ".avi", ".mkv")):
                    file_path = os.path.join(self.video_directory, file_name)
                    self.playlist.append(file_path)

    def play_video(self):
        if not self.playing_video and self.playlist:
            if self.current_index >= 0 and self.current_index < len(self.playlist):
                media = self.instance.media_new(self.playlist[self.current_index])
                self.media_player.set_media(media)
                self.media_player.set_hwnd(self.media_canvas.winfo_id())
                self.media_player.play()
                self.playing_video = True

    def pause_video(self):
        if self.playing_video:
            if self.video_paused:
                self.media_player.play()
                self.video_paused = False
                self.pause_button.config(text="Pause")
            else:
                self.media_player.pause()
                self.video_paused = True
                self.pause_button.config(text="Resume")

    def stop(self):
        if self.playing_video:
            self.media_player.stop()
            self.playing_video = False

    def play_next(self):
        if self.current_index < len(self.playlist) - 1:
            self.current_index += 1
            self.stop()
            self.play_video()

    def play_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.stop()
            self.play_video()

    def fast_forward(self):
        if self.playing_video:
            current_time = self.media_player.get_time() + 5000
            self.media_player.set_time(current_time)

    def rewind(self):
        if self.playing_video:
            current_time = self.media_player.get_time() - 5000
            if current_time < 0:
                current_time = 0
            self.media_player.set_time(current_time)

    def set_volume(self, value):
        volume_level = int(value)
        self.media_player.audio_set_volume(volume_level)

    def on_closing(self):
        if self.playing_video:
            self.media_player.stop()
        self.root.destroy()
    
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
        if gesture == 'reset':
            self.stop()
        elif  gesture == 'pause':
            self.pause_video()
            self.waitval = 15
        elif gesture == 'play':
            self.play_video()
        elif gesture == 'move':
            if hand == 'Left':
                self.play_next()
                self.waitval = 15
            elif hand == 'Right':
                self.play_previous()
                self.waitval = 15
        elif  gesture == 'move2':
            if hand == 'Left':
                self.fast_forward()
                self.waitval = 8
            elif hand == 'Right':
                self.rewind()
                self.waitval = 8
        elif gesture == 'volumeup':
            if self.volume <= 100:
                self.volume += 5
            self.set_volume(self.volume)
            self.volume_scale.set(self.volume)
            self.waitval = 3
        elif gesture == 'volumedown':
            if self.volume > 0:
                self.volume -= 5
            self.set_volume(self.volume)
            self.volume_scale.set(self.volume)
            self.waitval = 3

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    app.start_gesture_recognition()
    root.mainloop()
