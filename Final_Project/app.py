import streamlit as st
import cv2 as cv
import numpy as np
from PIL import Image
import io

def resize_with_aspect_ratio(image, width=None, height=None, inter=cv.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    
    if width is None and height is None:
        return image
    
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    
    return cv.resize(image, dim, interpolation=inter)

def process_image(image, kernel_size=3, max_width=800):
    # Convert PIL Image to OpenCV format
    image = np.array(image)
    if len(image.shape) == 3 and image.shape[2] == 4:  # If RGBA
        image = cv.cvtColor(image, cv.COLOR_RGBA2BGR)
    elif len(image.shape) == 2:  # If grayscale
        image = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
    
    # Resize image
    image = resize_with_aspect_ratio(image, width=max_width)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv.GaussianBlur(image, (3, 3), 0)
    
    # Convert to grayscale
    gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
    
    # Apply Laplacian edge detection
    laplacian = cv.Laplacian(gray, cv.CV_16S, ksize=kernel_size)
    
    # Convert back to uint8
    abs_laplacian = cv.convertScaleAbs(laplacian)
    
    return image, abs_laplacian

def main():
    st.title("Image Edge Detection App")
    
    # Add description
    st.write("""
    This app performs edge detection on uploaded images using the Laplacian operator.
    Upload an image to see the edge detection result!
    """)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image...", 
        type=['png', 'jpg', 'jpeg', 'bmp', 'webp']
    )
    
    # Sidebar controls
    st.sidebar.header("Settings")
    kernel_size = st.sidebar.slider(
        "Kernel Size (odd numbers only)",
        min_value=1,
        max_value=7,
        value=3,
        step=2
    )
    
    max_width = st.sidebar.slider(
        "Maximum Image Width",
        min_value=300,
        max_value=1200,
        value=800,
        step=100
    )
    
    if uploaded_file is not None:
        try:
            # Read the image
            image = Image.open(uploaded_file)
            
            # Process the image
            original, edges = process_image(
                image,
                kernel_size=kernel_size,
                max_width=max_width
            )
            
            # Display images side by side
            col1, col2 = st.columns(2)
            
            with col1:
                st.header("Original Image")
                st.image(original, channels="BGR")
                
            with col2:
                st.header("Edge Detection")
                st.image(edges)
                
            # Add download button for the processed image
            buf = io.BytesIO()
            Image.fromarray(edges).save(buf, format='PNG')
            st.download_button(
                label="Download Edge Detection Result",
                data=buf.getvalue(),
                file_name="edge_detection.png",
                mime="image/png"
            )
            
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            
if __name__ == "__main__":
    main()