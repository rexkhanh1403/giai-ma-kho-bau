
# 🏴‍☠️ Giải Mã Kho Báu

Đây là dự án **"Giải Mã Kho Báu"**, một trò chơi web tương tác được xây dựng bằng Python và Flask. Người chơi sẽ giải các câu đố được mã hóa bằng Caesar, Vigenère, RSA, AES để dần dần mở khóa các màn chơi và tìm ra kho báu cuối cùng.

---

## 📁 Cấu trúc dự án

```
giai-ma-kho-bau/
├── app.py               # Logic chính của Flask app
├── crypto_utils.py      # Các thuật toán mã hóa: Caesar, Vigenere, RSA, AES
├── requirements.txt     # Các thư viện cần thiết
├── static/              # Tài nguyên tĩnh (CSS, JS, hình ảnh, âm thanh)
│   ├── audio/
│   ├── images/
│   ├── js/
│   └── style.css
├── templates/           # Giao diện HTML (Flask Jinja2 templates)
│   ├── game_intro.html
│   ├── select_level.html
│   ├── level_01.html → level_04.html
│   └── game_complete.html
```

---

## ✨ Tính năng nổi bật

- 🧠 **Câu đố mã hóa nhiều cấp độ**: Caesar → Vigenère → RSA → AES
- 🎮 **Giao diện người dùng hiện đại** với hiệu ứng âm thanh và cài đặt
- 🔐 **Tích hợp thuật toán bảo mật** thực tế vào gameplay
- 🕐 **Giới hạn thời gian**, kiểm tra đáp án, lưu tiến độ
- 🌐 Xây dựng bằng **Python Flask**, dễ mở rộng và bảo trì

---

## ⚙️ Hướng dẫn cài đặt

### ✅ Bước 1: Clone dự án về máy

```bash
git clone https://github.com/rexkhanh1403/giai-ma-kho-bau.git
cd giai-ma-kho-bau
```

### ✅ Bước 2: Tạo và kích hoạt môi trường ảo (khuyên dùng)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### ✅ Bước 3: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

---

## 🚀 Cách chạy trò chơi

```bash
python app.py
```

Sau đó mở trình duyệt và truy cập:

```
http://127.0.0.1:5000
```

---

## 🤝 Đóng góp

Mọi đóng góp cho dự án đều được chào đón!

- Gửi **Issue** để báo lỗi hoặc góp ý
- Tạo **Pull Request** nếu bạn muốn sửa đổi
- Fork dự án và tùy biến theo ý tưởng của bạn

---

## 📚 Tài liệu tham khảo

1. Nguyễn Hồng Sơn (2007), *Giáo trình hệ thống Mạng máy tính CCNA*, NXB Lao động xã hội.
2. Phạm Quốc Hùng (2017), *Đề cương bài giảng Mạng máy tính*, Đại học SPKT Hưng Yên.
3. James F. Kurose & Keith W. Ross (2013), *Computer Networking: A Top-Down Approach*, Pearson.

---

## 🧑‍💻 Thực hiện bởi

| Họ tên              | MSSV         | Lớp         |
|---------------------|--------------|-------------|
| Nguyễn Mạnh Đức     | 1671020088   | CNTT 16-06  |
| Vương Quốc Khánh    | 1671020164   | CNTT 16-06  |

---

📅 *Đại học Đại Nam – Môn: An toàn bảo mật thông tin*  
🧑‍🏫 GVHD: TS. Trần Đăng Công
