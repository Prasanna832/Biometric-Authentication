import streamlit as st
import numpy as np
import cv2
from PIL import Image
import os
from skimage.metrics import structural_similarity as ssim
from skimage.transform import resize

# Function to preprocess uploaded image
def preprocess_image(image):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    # Resize to a fixed size
    resized_image = resize(gray_image, (256, 256), anti_aliasing=True)
    return resized_image

# Function to calculate SSIM similarity score
def calculate_ssim(image1, image2):
    score, _ = ssim(image1, image2, full=True, data_range=image1.max() - image1.min())
    return score

def main():
    st.title("Biometric Authentication App")
    st.markdown(
        """
        Welcome to the Biometric Authentication App! This app allows you to upload an image 
        and check if it matches any of the reference images in the specified directory.
        """
    )

    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    # Set the path to your images directory
    images_dir = "C:\\Users\\Deepika Hegde\\OneDrive\\Desktop\\123p\\images"

    if uploaded_file:
        try:
            # Preprocess uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            np_uploaded_image = preprocess_image(image)

            # List files in the reference directory
            reference_images = []
            for filename in os.listdir(images_dir):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    reference_path = os.path.join(images_dir, filename)
                    reference_image = cv2.imread(reference_path, cv2.IMREAD_GRAYSCALE)
                    
                    if reference_image is None:
                        st.warning(f"Could not read reference image: {reference_path}")
                        continue

                    np_reference_image = resize(reference_image, (256, 256), anti_aliasing=True)  # Resize reference image
                    reference_images.append((reference_path, np_reference_image))

            # Calculate similarity scores
            found_match = False
            for ref_path, ref_image in reference_images:
                similarity_ssim = calculate_ssim(np_uploaded_image, ref_image)
                
                # Display similarity score
                st.write(f"SSIM Similarity Score with {ref_path}: {similarity_ssim:.4f}")

                # Check if a match is found (threshold can be adjusted)
                if similarity_ssim > 0.95:
                    st.success(f"Match found with {ref_path}. Access Granted!")
                    st.balloons()
                    found_match = True
                    break
            
            if not found_match:
                st.warning("No match found with any reference image. Access Denied.")

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
