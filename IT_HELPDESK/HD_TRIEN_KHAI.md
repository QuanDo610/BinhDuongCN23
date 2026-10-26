# HƯỚNG DẪN TRIỂN KHAI HỆ THỐNG IT HELPDESK & KẾT NỐI GOOGLE SHEET (BẢN NÂNG CẤP)

Hệ thống được thiết kế theo cấu trúc **Workspace 2 cột cạnh nhau (Side-by-side)** giống hệ thống `A_THANG`, kết nối 2 chiều thời gian thực với Google Sheets và lưu trữ hình ảnh trên Google Drive.

---

## 🌟 CÁC TÍNH NĂNG NỔI BẬT VỪA ĐƯỢC TỐI ƯU HÓA:

1. **Bố cục 1 trang (Kế nhau giống `A_THANG`):**
   - **Cột Trái:** Form gửi yêu cầu ngắn gọn, trực quan (Tên, SĐT, Phòng ban, Tên máy, Lỗi, Upload ảnh).
   - **Cột Phải:** Bảng Monitoring / Hàng đợi xử lý theo thời gian thực (Hiển thị ngay cạnh form, có 4 thẻ thống kê, bộ lọc tìm kiếm, xem ảnh chụp lỗi và ghi chú IT).

2. **Tự động nhận diện Tên máy & Thông số thiết bị (Auto-Detect):**
   - Người dùng không cần phải biết tên máy là gì! Hệ thống sẽ **tự động sinh và gán một Mã định danh máy cố định (VD: `Win 10/11 (PC-48A2)`)** và lưu vĩnh viễn trên máy tính đó.
   - Tự động quét: **Hệ điều hành (Windows 10/11, macOS)**, **RAM**, **Số nhân CPU**, **Độ phân giải màn hình** và **Địa chỉ IP Public**.
   - Người dùng chỉ việc điền Tên + SĐT (được tự động nhớ cho những lần sau).

3. **Hỗ trợ Upload Ảnh lỗi & Dán trực tiếp từ Clipboard (`Ctrl + V`):**
   - Đồng nghiệp có thể bấm nút chọn ảnh hoặc chụp từ điện thoại.
   - **Đặc biệt:** Khi gặp lỗi, họ chỉ cần nhấn nút chụp màn hình (PrintScreen / Snipping Tool / Zalo) rồi bấm **`Ctrl + V`** vào trang web là ảnh tự động được dán vào!
   - Ảnh được **nén tự động ngay trên trình duyệt** xuống ~150KB để upload siêu nhanh lên Google Drive.

4. **Ô nhập Thông báo lỗi tiếng Anh (Error Message):**
   - Thiết kế riêng 1 ô để người dùng gõ/copy nguyên văn câu chữ tiếng Anh trên màn hình (VD: `Paper Jam`, `Printer Offline`, `Access Denied`, `Not Responding`...).
   - Giúp bạn (IT) đọc là biết ngay nguyên nhân mà không cần họ phải giải thích dài dòng.

---

## 🚀 CÁCH CÀI ĐẶT GOOGLE SHEET & GOOGLE APPS SCRIPT (3 PHÚT)

### Bước 1: Tạo Google Sheet mới
1. Mở trình duyệt, truy cập [Google Sheets](https://sheets.new) để tạo một bảng tính mới.
2. Đổi tên bảng tính thành: **`Sổ Tiếp Nhận Sự Cố IT - Chi Nhánh 23`**.

### Bước 2: Dán mã Google Apps Script
1. Trên thanh menu của Google Sheet, bấm vào **Tiện ích mở rộng (Extensions)** ➔ Chọn **Apps Script**.
2. Xoá sạch code cũ trong file `Code.gs`.
3. Mở file [google_apps_script.js](file:///Users/admin/Desktop/BINHDUONG/IT_HELPDESK/google_apps_script.js), sao chép toàn bộ nội dung và dán vào.
4. Bấm biểu tượng **Đĩa mềm (Lưu)** hoặc bấm `Ctrl + S`.

### Bước 3: Triển khai Ứng dụng Web (Deploy Web App)
1. Ở góc trên bên phải màn hình Apps Script, bấm nút **Triển khai (Deploy)** ➔ **Tùy chọn triển khai mới (New deployment)**.
2. Bấm vào biểu tượng bánh răng **Chọn loại** ➔ Chọn **Ứng dụng web (Web App)**.
3. Cấu hình:
   - **Mô tả:** `IT Helpdesk API v2`
   - **Thực thi dưới dạng (Execute as):** `Tôi (Me)`
   - **Ai có quyền truy cập (Who has access):** **`Bất kỳ ai (Anyone)`** *(Bắt buộc chọn Anyone để đồng nghiệp gửi được form và ảnh).*
4. Bấm **Triển khai (Deploy)**.
5. Cấp quyền truy cập Google Sheet & Google Drive:
   - Bấm **Ủy quyền truy cập (Authorize access)** ➔ Chọn tài khoản Google của bạn.
   - Nếu hiện thông báo *"Google chưa xác minh ứng dụng này"*, bấm vào dòng chữ nhỏ **Nâng cao (Advanced)** ở góc dưới bên trái ➔ Bấm **Đi tới... (không an toàn)** ➔ Bấm **Cho phép (Allow)**.
6. Sao chép (Copy) đường link **URL ứng dụng web (Web App URL)** (dạng `https://script.google.com/macros/s/AKfycb.../exec`).

---

## 🔗 KẾT NỐI VÀO WEBSITE

- **Cách nhanh nhất:** Mở trang web [IT_HELPDESK/index.html](file:///Users/admin/Desktop/BINHDUONG/IT_HELPDESK/index.html) trên trình duyệt ➔ Bấm nút **Cài Đặt Server** ở góc trên bên phải ➔ Dán link URL vừa sao chép vào ➔ Bấm **Lưu Kết Nối**.
- **Cách gán cố định cho toàn bộ cơ quan:** Mở file `IT_HELPDESK/index.html`, dán link của bạn vào dòng khoảng số 370:
  ```javascript
  const DEFAULT_SCRIPT_URL = "https://script.google.com/macros/s/AKfycb.../exec";
  ```
  Sau đó đẩy code lên GitHub repository, bật **GitHub Pages** (Settings -> Pages -> Deploy from branch `main`).

---

## 🛠️ QUY TRÌNH VẬN HÀNH DÀNH CHO IT:

1. **Khi có máy hỏng:** Đồng nghiệp mở web, nhập tên, chọn lỗi, bấm Ctrl+V dán ảnh chụp màn hình (nếu có) và bấm gửi.
2. **Dữ liệu hiển thị đồng thời:**
   - Đổ về Google Sheet của bạn (tự động lưu ảnh vào thư mục `IT_Helpdesk_Uploads` trên Drive của bạn).
   - Xuất hiện ngay trên cột **Monitoring** bên phải màn hình web.
3. **Khi bạn xử lý xong:**
   - Bạn chỉ cần mở Google Sheet, đổi cột **Trạng thái** thành **`Đã hoàn thành`** (và gõ vài chữ vào cột **Ghi chú IT**).
   - Ngay lập tức trên web của cơ quan, Ticket đó đổi sang màu xanh lá cây với huy hiệu *Đã hoàn thành*!
