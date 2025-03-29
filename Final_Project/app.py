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

def apply_laplacian(image, kernel_size):
    """Xử lý ảnh với toán tử Laplacian"""
    # Chuyển sang grayscale và áp dụng Laplacian
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    result = cv.convertScaleAbs(cv.Laplacian(gray, cv.CV_16S, ksize=kernel_size))
    return result

def process_image(image, kernel_size=3, max_width=800, sharpening=False, sharp_strength=1.5):
    """Tiền xử lý và áp dụng bộ lọc làm nét"""
    image = np.array(image)
    if len(image.shape) == 3 and image.shape[2] == 4:
        image = cv.cvtColor(image, cv.COLOR_RGBA2BGR)
    
    image = resize_with_aspect_ratio(image, width=max_width)
    
    # Áp dụng Laplacian
    laplacian = apply_laplacian(image, kernel_size)
    
    # Áp dụng Unsharp Masking nếu được chọn
    if sharpening:
        image = unsharp_mask(image, sharp_strength)
    
    return image, laplacian

def unsharp_mask(image, strength=1.5):
    """Tăng độ sắc nét của ảnh bằng phương pháp Unsharp Masking"""
    blurred = cv.GaussianBlur(image, (5, 5), 0)
    sharpened = cv.addWeighted(image, 1 + strength, blurred, -strength, 0)
    return sharpened

def main():
    st.set_page_config(page_title="Phát Hiện Cạnh Ảnh", layout="wide")

    st.title("Ứng Dụng Phát Hiện Cạnh & Làm Nét Ảnh 📸")

    st.write("""
    🔹 Ứng dụng này cho phép phát hiện cạnh bằng toán tử Laplacian và tùy chỉnh làm nét ảnh.
    \n📥 Tải lên ảnh để trải nghiệm!
    """)

    uploaded_file = st.file_uploader("🖼 Chọn một hình ảnh...", type=['png', 'jpg', 'jpeg', 'bmp', 'webp'])

    st.sidebar.header("⚙ Cài Đặt")

    kernel_size = st.sidebar.slider("🔍 Kích Thước Kernel (chỉ số lẻ)", 1, 7, 3, step=2)

    max_width = st.sidebar.slider("📏 Chiều Rộng Tối Đa Của Ảnh", 300, 1200, 800, step=100)

    sharpening = st.sidebar.checkbox("🖌 Bật Unsharp Masking (Làm Nét)", value=False)
    
    sharp_strength = st.sidebar.slider("🔧 Cường Độ Làm Nét", 0.5, 3.0, 1.5, step=0.1) if sharpening else None

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)

            original, edges = process_image(
                image,
                kernel_size=kernel_size,
                max_width=max_width,
                sharpening=sharpening,
                sharp_strength=sharp_strength
            )

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Ảnh Gốc")
                st.image(original, channels="BGR", use_container_width=True)

            with col2:
                st.subheader("Phát Hiện Cạnh")
                st.image(edges, use_container_width=True)

            st.subheader("💾 Tải Xuống Kết Quả")

            download_col1, download_col2 = st.columns(2)

            with download_col1:
                buf = io.BytesIO()
                Image.fromarray(edges).save(buf, format='PNG')
                st.download_button(
                    label="📥 Tải Ảnh Đã Phát Hiện Cạnh",
                    data=buf.getvalue(),
                    file_name="edge_detection.png",
                    mime="image/png"
                )

            with download_col2:
                original_buf = io.BytesIO()
                original_rgb = cv.cvtColor(original, cv.COLOR_BGR2RGB)
                Image.fromarray(original_rgb).save(original_buf, format='PNG')
                st.download_button(
                    label="📥 Tải Ảnh Gốc",
                    data=original_buf.getvalue(),
                    file_name="original_image.png",
                    mime="image/png"
                )

        except Exception as e:
            st.error(f"⚠ Lỗi xử lý hình ảnh: {str(e)}")

if __name__ == "__main__":
    main()
