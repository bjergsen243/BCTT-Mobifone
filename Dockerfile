# Sử dụng image cơ sở có hỗ trợ Python
FROM python:3.8

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép mã nguồn ứng dụng vào thư mục làm việc
COPY . /app

# Cài đặt các thư viện từ requirements.txt
RUN pip install -r requirements.txt

# Mở cổng cho ứng dụng
EXPOSE 5001

# Chạy ứng dụng
CMD ["python", "app.py"]
