# Hệ Thống IT Helpdesk & Tiếp Nhận Sự Cố Máy Tính - Chi Nhánh 23

Hệ thống tiếp nhận, theo dõi và xử lý sự cố thiết bị tin học (máy tính, máy in, mạng nội bộ, phần mềm, chữ ký số) dành cho **Văn Phòng Đăng Ký Đất Đai TP.HCM - Chi Nhánh 23**.

Trang web hoạt động theo mô hình **Serverless** (không cần máy chủ, miễn phí 100% trên GitHub Pages), giao diện 1 trang duy nhất (Workspace Grid 2 cột cạnh nhau), đồng bộ thời gian thực 2 chiều với **Google Sheets** và tự động lưu trữ hình ảnh trên **Google Drive**.

---

## 🌟 Tính Năng Nổi Bật

1. **Bố cục 1 trang trực quan (Side-by-side Workspace):**
   - **Cột Trái (Gửi yêu cầu):** Form gửi ticket tối giản (Họ tên, SĐT, Phòng ban, Loại sự cố, Thông báo lỗi tiếng Anh, Mô tả và Upload ảnh).
   - **Cột Phải (Bảng Monitoring):** Theo dõi hàng đợi xử lý trực tiếp với 4 thẻ thống kê (Tổng, Chờ xử lý, Đang xử lý, Đã hoàn thành), bộ lọc tìm kiếm và xem ảnh lỗi phóng to.

2. **Tự động nhận diện thiết bị & IP (Auto-Detection):**
   - Tự động sinh và lưu **Mã định danh máy (Machine ID)** cố định (VD: `Win 10/11 (PC-48A2)`). Người dùng không cần biết hay gõ tên máy tính của mình.
   - Tự động thu thập: Địa chỉ IP Public, Hệ điều hành (Windows 10/11, macOS), RAM, CPU Cores, độ phân giải màn hình để hỗ trợ IT chẩn đoán từ xa.
   - Tự động nhớ Họ tên & SĐT của người dùng trên máy đó qua `localStorage`.

3. **Hỗ trợ Upload ảnh lỗi & Dán trực tiếp từ Clipboard (`Ctrl + V`):**
   - Hỗ trợ chọn file ảnh hoặc chụp ảnh từ điện thoại.
   - **Đặc biệt:** Người dùng chỉ cần chụp màn hình lỗi (`PrintScreen` / `Snipping Tool` / Zalo) rồi bấm **`Ctrl + V`** vào trang web là ảnh tự dán vào form.
   - Ảnh được nén tự động (HTML5 Canvas Compression) xuống ~150KB trước khi gửi lên Google Drive (`IT_Helpdesk_Uploads`).

4. **Ô nhập "Thông báo lỗi tiếng Anh" (Error Message):**
   - Dành riêng cho các thông báo hệ thống như: `Paper Jam`, `Printer Offline`, `Access Denied`, `Not Responding`, `No Internet`... giúp IT chẩn đoán nhanh mà người dùng không cần phải giỏi tiếng Anh.

5. **Bảo mật & Kết nối ngầm:**
   - URL Google Apps Script được tích hợp ngầm và mã hóa trong mã nguồn, không để lộ trên giao diện người dùng.

---

## 🚀 Cấu Trúc Thư Mục

```text
├── index.html              # Toàn bộ ứng dụng giao diện web (HTML + Tailwind CSS + JS)
├── google_apps_script.js   # Mã nguồn Google Apps Script triển khai trên Google Sheet
└── README.md               # Tài liệu hướng dẫn hệ thống
```

---

## 🛠️ Quy Trình Vận Hành Của IT

1. **Người dùng gửi ticket:** Dữ liệu lập tức đổ về Google Sheet và hiển thị ngay trên bảng Monitoring ở cột bên phải web.
2. **IT kiểm tra & xử lý:** Mở bảng Monitoring hoặc mở Google Sheet trên điện thoại/máy tính để đi fix máy theo thứ tự ưu tiên.
3. **Cập nhật hoàn thành:** Sửa ô **Trạng thái** trong Google Sheet thành `Đã hoàn thành` (và gõ vài chữ vào cột `Ghi chú IT` nếu muốn) ➔ Trên web của mọi người tự động đổi sang màu xanh hoàn tất!
