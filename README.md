# Xử lý ảnh số - Nhóm 2

Đây là repository GitHub chính thức cho môn **Xử lý ảnh số**.

![image](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExOWw1Z2dhMjVtNXJrdmc1ZjZpMnpncDFqbXZmdjNmYmhkM3JwcDU5cSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xUOxfg0ESyhKOv4Vva/giphy.gif)

## Cài đặt môi trường

### 1. Tạo môi trường ảo (Virtual Environment)

```bash
# Tạo môi trường ảo mới
python -m venv venv

# Kích hoạt môi trường ảo
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Cài đặt thư viện

```bash
# Cài đặt các thư viện cần thiết từ requirements.txt
pip install -r requirements.txt
```

## GitHub Commands

```bash
# Clone repository có sẵn về máy local
git clone <repository_url>

# Stage các thay đổi để chuẩn bị commit
git add <file_name>  # Hoặc dùng . để stage tất cả thay đổi

# Lưu các thay đổi đã stage kèm message
git commit -m "Your commit message"

# Tải các thay đổi lên GitHub repository
git push

# Tải các thay đổi từ GitHub repository về
git pull
```

## Chạy ứng dụng

```bash
# Chạy ứng dụng Streamlit
streamlit run app.py

# Chạy ứng dụng Python
python app.py
```

## Cấu trúc thư mục

```
├── README.md
├── requirements.txt
├── app.py
└── venv/
```

## Thư viện sử dụng

- streamlit==1.32.0
- opencv-python==4.9.0.80
- Pillow==10.2.0
- numpy==1.26.4