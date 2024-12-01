import tkinter as tk
import mediapipe as mp
from mediapipe import Timestamp
import cv2
from tkinter import ttk
from PIL import Image, ImageTk
from image_viewer import ImageViewer
from video_player import VideoPlayer
from audio_player import AudioPlayer

class Media:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Apps")
        self.root.resizable(False, False)
        self.current_gesture = None

        self.create_icons()

        style = ttk.Style()
        style.configure("Green.TButton", foreground="black", background="green")
        style.configure("Red.TButton", foreground="black", background="red")
        style.configure("Blue.TButton", foreground="black", background="blue")

        # Create a frame to hold the buttons in the center
        center_frame = tk.Frame(self.root)
        center_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Use grid to center horizontally

        # Create buttons with icons and text
        self.image_icon = ImageTk.PhotoImage(self.image_icon)
        self.image = ttk.Button(center_frame, text="Image Viewer", image=self.image_icon, compound=tk.TOP, command=self.open_img_viewer, style="Green.TButton")
        self.image.grid(row=0, column=0, padx=10)  # Use grid to center horizontally

        self.music_icon = ImageTk.PhotoImage(self.music_icon)
        self.music = ttk.Button(center_frame, text="Audio Player", image=self.music_icon, compound=tk.TOP, command=self.open_mus_player, style="Blue.TButton")
        self.music.grid(row=0, column=1, padx=10)  # Use grid to center horizontally

        self.video_icon = ImageTk.PhotoImage(self.video_icon)
        self.video = ttk.Button(center_frame, text="Video Player", image=self.video_icon, compound=tk.TOP, command=self.open_vid_player, style="Red.TButton")
        self.video.grid(row=0, column=2, padx=10)  # Use grid to center horizontally

        # Make the center frame expand to fill any available space
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_icons(self):
        self.image_icon = Image.open("icon/image_icon.png")
        self.image_icon = self.image_icon.resize((64, 64), Image.ADAPTIVE)

        self.music_icon = Image.open("icon/music_icon.png")
        self.music_icon = self.music_icon.resize((64, 64), Image.ADAPTIVE)

        self.video_icon = Image.open("icon/video_icon.png")
        self.video_icon = self.video_icon.resize((64, 64), Image.ADAPTIVE)

    def open_img_viewer(self):
        # live = Live(self.handle_gestures)
        self.image_app = tk.Toplevel(self.root)
        self.instance = ImageViewer(self.image_app)
        self.instance.start_gesture_recognition()
        self.image_app.mainloop()

    def open_mus_player(self):
        self.music_app = tk.Toplevel(self.root)
        self.instance = AudioPlayer(self.music_app)
        self.instance.start_gesture_recognition()
        self.music_app.mainloop()

    def open_vid_player(self):
        self.video_app = tk.Toplevel(self.root)  # Pass the main window reference
        self.instance = VideoPlayer(self.video_app)
        self.instance.start_gesture_recognition()
        self.video_app.mainloop()
    
if __name__ == "__main__":
    root = tk.Tk()
    media_app = Media(root)
    root.mainloop()
