import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from tkinter import ttk
import cv2
import mediapipe as mp
from mediapipe import Timestamp
import threading
import time

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("1280x750")
        self.root.resizable(False, False)

        self.BaseOptions = mp.tasks.BaseOptions
        self.GestureRecognizer = mp.tasks.vision.GestureRecognizer
        self.GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        self.GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        self.cap = None  # Initialize the video capture to None
        self.waitval = 0

        # Create a container frame
        self.container = tk.Frame(root)
        self.container.pack(expand=True, fill="both")

        self.image_label = tk.Label(self.container)
        self.image_label.pack(expand=True, fill="both")

        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=root.quit)

        self.image = None  # Store the loaded image
        self.image_path = None
        self.image_index = 0
        self.zoom_factor = 1.0
        self.image_list = []    
        image_folder = "image"  # Specify the folder name where your image files are located
        for filename in os.listdir(image_folder):
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                try:
                    file_path = os.path.join(image_folder, filename)  # Correct the path to the image folder
                    image = Image.open(file_path)  # Open the image using the full file path
                    self.image_list.append(image)
                except Exception as e:
                    print(f"Error loading image '{filename}': {e}")

        self.show_image()
        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        navigation_frame = tk.Frame(self.container)
        navigation_frame.pack()

        style = ttk.Style()
        style.configure("Green.TButton", foreground="black", background="green")
        style.configure("Red.TButton", foreground="black", background="red")
        style.configure("Blue.TButton", foreground="black", background="blue")

        prev_button = ttk.Button(navigation_frame, text="<< Previous", command=self.show_previous_image, style="Green.TButton")
        prev_button.pack(side="left", padx=10)

        next_button = ttk.Button(navigation_frame, text="Next >>", command=self.show_next_image, style="Green.TButton")
        next_button.pack(side="left", padx=10)

        zoom_in_button = ttk.Button(navigation_frame, text="Zoom In", command=self.zoom_in, style="Blue.TButton")
        zoom_in_button.pack(side="left", padx=10)

        zoom_out_button = ttk.Button(navigation_frame, text="Zoom Out", command=self.zoom_out, style="Blue.TButton")
        zoom_out_button.pack(side="left", padx=10)

        reset_button = ttk.Button(navigation_frame, text="Reset", command=self.reset, style="Red.TButton")
        reset_button.pack(side="left", padx=10)

    def show_image(self):
        try:
            image = self.image_list[self.image_index]
            image = image.resize((int(680 * self.zoom_factor), int(480 * self.zoom_factor)))
            self.image = ImageTk.PhotoImage(image)

            # Update the image label within the container
            self.image_label.config(image=self.image)
            self.image_label.image = self.image  # Keep a reference to prevent garbage collection
        except Exception as e:
            print(f"Error showing image: {e}")

    def show_next_image(self):
        self.zoom_factor = 1.0
        if self.image_index < len(self.image_list) - 1:
            self.image_index += 1
            self.show_image()

    def show_previous_image(self):
        self.zoom_factor = 1.0
        if self.image_index > 0:
            self.image_index -= 1
            self.show_image()

    def zoom_in(self):
        if self.zoom_factor < 1.5:
            self.zoom_factor += 0.1
            self.show_image()

    def zoom_out(self):
        if self.zoom_factor > 0.5:
            self.zoom_factor -= 0.1
            self.show_image()

    def reset(self):
        self.zoom_factor = 1.0
        self.show_image()
    
    def start_gesture_recognition(self):
        gesture_thread = threading.Thread(target=self.gesture_recog)
        gesture_thread.start()

    def gesture_recog(self):
        # Create a gesture recognizer instance with the live stream mode:
        def print_result(result: self.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
            if result and result.gestures:
                top_gesture = result.gestures[0][0]
                print('Top gesture category: {}'.format(top_gesture.category_name), result.handedness[0][0].category_name)
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
            self.reset()
        elif gesture == 'move' or gesture == 'move2':
            if hand == 'Left':
                self.show_next_image()
                self.waitval = 15
            elif hand == 'Right':
                self.show_previous_image()
                self.waitval = 15
        elif gesture == 'volumeup':
            self.zoom_in()
            self.waitval = 8
        elif gesture == 'volumedown':
            self.zoom_out()
            self.waitval = 8


if __name__ == "__main__":
    root = tk.Tk()
    media_app = ImageViewer(root)
    media_app.start_gesture_recognition()  # Start the gesture recognition thread
    root.mainloop()
