import cv2
import mediapipe as mp
import os
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Function to detect and crop hands from an image
def detect_and_crop_hands(input_image_path, output_directory):
    # Read the input image
    image = cv2.imread(input_image_path)

    # Convert the image to RGB format (required by Mediapipe)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect hands in the image
    results = hands.process(image_rgb)

    # Check if hands are detected
    if results.multi_hand_landmarks:
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Loop through detected hands and crop them
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Get the bounding box coordinates of the hand
            x_min, y_min = image.shape[1], image.shape[0]
            x_max, y_max = 0, 0
            for landmark in hand_landmarks.landmark:
                x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x)
                y_max = max(y_max, y)

            # Increase the padding
            padding = 80
            x_min = max(0, x_min - padding)
            y_min = max(0, y_min - padding)
            x_max = min(image.shape[1], x_max + padding)
            y_max = min(image.shape[0], y_max + padding)

            # Crop the hand region
            hand_crop = image[y_min:y_max, x_min:x_max]

            # Generate a unique filename using a timestamp
            timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
            output_filename = f'hand_{timestamp}_{i}.jpg'

            # Save the cropped hand image to the output directory
            output_path = os.path.join(output_directory, output_filename)
            cv2.imwrite(output_path, hand_crop)

            print(f"Hand {i+1} from {input_image_path} cropped and saved to {output_path}")

# Directory containing input images
input_images_directory = 'two_pointing'  # Replace with the path to your directory containing images

# Output directory for cropped hands
output_directory = 'two_pointing_cropped'     # Replace with your desired output directory

# List all filenames in the input directory
input_files = os.listdir(input_images_directory)

# Loop through each input image file and call the function
for input_file in input_files:
    input_image_path = os.path.join(input_images_directory, input_file)
    detect_and_crop_hands(input_image_path, output_directory)
