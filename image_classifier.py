import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification
import os
from tqdm import tqdm # Import tqdm for the progress bar

def classify_image_directly(image_path, model, processor):
    """
    Classifies a single image using a pre-trained Document AI model.
    """
    try:
        # Open the image and ensure it's in RGB format
        image = Image.open(image_path).convert("RGB")
        
        # Process the image to prepare it for the model
        inputs = processor(images=image, return_tensors="pt")

        # Get the model's prediction
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits

        # Find the class with the highest probability
        predicted_label_id = logits.argmax(-1).item()
        
        # Get the name of the predicted class
        predicted_label = model.config.id2label[predicted_label_id]
        
        return predicted_label

    except Exception as e:
        # Silently handle errors by returning a specific category
        return "error_processing"

# --- SETUP ---

# Use a pre-trained Document Image Transformer
model_name = "microsoft/dit-base-finetuned-rvlcdip"

# Load the model and its processor from Hugging Face
print(f"Loading model '{model_name}'...")
image_processor = AutoImageProcessor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)
print("Model loaded successfully.")

# --- CLASSIFICATION ---

# Folder containing the images you want to classify
input_folder = r"classified_output\images" 
# Folder where the classified images will be moved
output_folder = "classified_output_silent" 

if not os.path.exists(input_folder):
    print(f"Error: Input folder '{input_folder}' not found. Please create it and add images.")
else:
    print(f"\nSilently classifying images from '{input_folder}'...")
    
    # Get a list of all image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # Use tqdm to create a progress bar
    for filename in tqdm(image_files, desc="Classifying"):
        image_path = os.path.join(input_folder, filename)
        
        # Get the prediction for the current image
        predicted_category = classify_image_directly(image_path, model, image_processor)
        
        # Create a directory for the predicted category if it doesn't exist
        destination_dir = os.path.join(output_folder, predicted_category)
        os.makedirs(destination_dir, exist_ok=True)
        
        # Move the file to its new home
        destination_path = os.path.join(destination_dir, filename)
        try:
            os.rename(image_path, destination_path)
        except OSError as e:
            # This can happen if the destination file already exists or other permission issues
            print(f"Could not move {filename}: {e}")
            
    print(f"\nClassification complete! Files moved to '{output_folder}'.")