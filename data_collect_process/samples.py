import os
import random
import cv2

# Function to select a given number of image samples from a dataset
def select_image_samples(dataset_directory, output_directory, num_samples):
    # Get a list of all image files in the dataset directory
    image_files = [f for f in os.listdir(dataset_directory) if f.endswith('.jpg') or f.endswith('.png')]

    # Ensure that the number of samples requested is not greater than the dataset size
    num_samples = min(num_samples, len(image_files))
    
    # Use random.sample to select random image samples without replacement
    selected_samples = random.sample(image_files, num_samples)
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Copy the selected images to the output directory
    for image_file in selected_samples:
        input_path = os.path.join(dataset_directory, image_file)
        output_path = os.path.join(output_directory, image_file)
        # Copy the image file to the output directory (you can also move it if needed)
        # You can use shutil.copy() for this purpose
        cv2.imwrite(output_path, cv2.imread(input_path))

    return selected_samples

# Example usage
# Suppose you have an image dataset in a directory called 'image_dataset'
dataset_directory = 'two_pointing_cropped'  # Replace with the path to your dataset directory

# Output directory where selected samples will be stored
output_directory = 'two_pointing_cropped/100'  # Replace with your desired output directory

# Number of image samples you want to select
num_samples_to_select = 100

# Call the function to select the desired number of image samples
selected_samples = select_image_samples(dataset_directory, output_directory, num_samples_to_select)

# Print the selected image samples
print("Selected Image Samples:", selected_samples)
