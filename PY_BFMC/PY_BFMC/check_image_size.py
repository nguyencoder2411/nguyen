from PIL import Image

def measure_image_size(image_path):
    try:
        # Mở tệp ảnh
        with Image.open(image_path) as img:
            # Lấy kích thước (width, height)
            width, height = img.size
            print(f"Kích thước của ảnh '{image_path}':")
            print(f"Chiều rộng: {width} pixels")
            print(f"Chiều cao: {height} pixels")
            return width, height
    except FileNotFoundError:
        print(f"Tệp '{image_path}' không tồn tại.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

# Ví dụ sử dụng
if __name__ == "__main__":
    # Thay đường dẫn dưới đây bằng ảnh bạn muốn đo kích thước
    image_path = "Track2025_2.png"  # Đường dẫn tới ảnh
    measure_image_size(image_path)
