# Smart Document Management System

## Giới thiệu

Ứng dụng quản lý tài liệu thông minh này được xây dựng bằng Flask. Dự án hỗ trợ phân quyền người dùng, quy trình xử lý tài liệu, quản lý thông báo và tích hợp các dịch vụ AI/OCR để trích xuất và tóm tắt nội dung.

## Tính năng chính

- Quản lý người dùng với phân quyền `admin`, `staff`, `employee`
- Đăng nhập/đăng ký và quản lý phiên làm việc
- Quản lý tài liệu: tải lên, duyệt, phê duyệt, xử lý và xem chi tiết
- Hệ thống thông báo cho người dùng
- Kiểm tra sức khỏe hệ thống qua API `/health`
- Hỗ trợ tài liệu PDF, DOC, DOCX, XLS, XLSX, hình ảnh
- Các dịch vụ AI/OCR trong thư mục `app/ai` để trích xuất và xử lý nội dung tài liệu

## Cấu trúc dự án

- `app/` - mã nguồn Flask chính
  - `controllers/` - định nghĩa blueprint và xử lý route
  - `models/` - quản lý database và mô hình dữ liệu
  - `services/` - logic nghiệp vụ
  - `ai/` - dịch vụ AI, OCR, trích xuất, tóm tắt
  - `static/` - CSS, JavaScript, uploads
  - `templates/` - giao diện HTML
  - `utils/` - helper, validator và middleware
- `config/` - cấu hình môi trường
- `database/` - nơi lưu trữ file database SQLite
- `tests/` - bộ test tự động
- `run.py` - chạy ứng dụng Flask

## Yêu cầu

- Python 3.10 trở lên
- Thư viện trong `requirements.txt`
- Phần mềm hỗ trợ OCR khi cần sử dụng `pytesseract`

## Cài đặt và chạy

1. Tạo môi trường ảo

```bash
python -m venv venv
```

2. Kích hoạt môi trường

```bash
venv\Scripts\activate
```

3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

4. Cài thêm các thư viện OCR và hỗ trợ hình ảnh

```bash
pip install paddleocr
pip install paddlepaddle
pip install pytesseract pillow pdf2image
```

5. Chạy ứng dụng

```bash
python run.py
```

6. Mở trình duyệt và truy cập

```text
http://127.0.0.1:5000
```

## Chạy test

```bash
pytest
```

## Cấu hình

Mặc định ứng dụng dùng `config/development_config.py` cho môi trường phát triển. Bạn có thể mở rộng thêm `production_config.py` hoặc `testing_config.py` nếu cần.

## Ghi chú

- Dữ liệu database mặc định nằm trong `database/development.db`
- Thư mục upload file là `app/static/uploads`
- Nếu cần triển khai lên production, hãy chỉnh `DEBUG = False`, cấu hình `SECRET_KEY` và `SESSION_COOKIE_SECURE = True`