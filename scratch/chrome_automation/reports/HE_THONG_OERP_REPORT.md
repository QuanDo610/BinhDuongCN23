# 📑 BÁO CÁO NGHIÊN CỨU TOÀN DIỆN HỆ THỐNG OERP (vpdkddtdm.vn)
> **Đơn vị quản lý**: Chi nhánh Văn phòng Đăng ký đất đai TP. Thủ Dầu Một (Bình Dương)  
> **Tài khoản kiểm tra**: `tdm_nguyetbtm` (Cán bộ BÙI THỊ MINH NGUYỆT - Đơn vị ID: `20227`)  
> **Thời gian khảo sát**: Tháng 09/2026

---

## 1. 🗺️ SITEMAP & BẢN ĐỒ CHỨC NĂNG HỆ THỐNG

Hệ thống được thiết kế theo mô hình **Một Cửa Liên Thông** và **Điều Hành Tác Nghiệp Đất Đai (OERP)** khép kín từ khâu nhận hồ sơ đến trả kết quả:

- `/vptdm/trangchu`: Trang chủ, xem danh sách hồ sơ cán bộ cần xử lý trong ngày.
- `/vptdm/tiepnhanhoso`: **Tiếp nhận hồ sơ mới** (Tổ chức/Cá nhân, Số tờ, Số thửa, Số nhà, In biên nhận, In phiếu theo dõi, Gửi SMS, Cấu hình lịch đo đạc, Tra cứu ngăn chặn).
- `/vptdm/xulyhoso`: **Xử lý hồ sơ** (Lịch đo đạc, Chức năng thuế, Quy trình thực hiện, Thành phần hồ sơ, Chuyển nội bộ, Giao hồ sơ, Giao phiếu nhanh, Xuất Excel).
- `/vptdm/suahoso`: **Sửa hồ sơ** (Cập nhật thông tin sai sót, danh sách tài liệu yêu cầu bổ sung).
- `/vptdm/trahoso`: **Trả hồ sơ** (Trả hồ sơ khách hàng, In ký nhận, Xuất/Import dữ liệu Excel).
- `/vptdm/tracuuhoso`: **Tra cứu** (Tra cứu mã biên nhận một cửa, tên khách hàng/công ty, xem hình ảnh trích lục/sản phẩm đo đạc).
- `/vptdm/quanlytrangthaihoso`: **Quản lý trạng thái** (Hoàn thành hồ sơ, Hủy hồ sơ lỗi, Khôi phục hồ sơ).
- `/vptdm/dashboard-trichdo`: **Dashboard trích đo** (Biểu đồ luồng xử lý hồ sơ theo điểm quy trình đo đạc).
- `/vptdm/thongketonghop`: **Thống kê tổng hợp** (Báo cáo tham số, chi tiết luồng giao, xuất file Excel).

---

## 2. 🎯 MỤC TIÊU CỦA WEBSITE LÀ PHỤC VỤ VẤN ĐỀ GÌ? LÀM GÌ?

Hệ thống này được xây dựng chuyên biệt để:
1. **Số hóa toàn bộ quy trình dịch vụ công đất đai**:
   - Quản lý từ lúc người dân nộp hồ sơ xin cấp sổ, tách thửa, đo đạc trích lục địa chính đến khi trao trả kết quả.
2. **Kiểm soát thời hạn & Chống trễ hẹn hồ sơ**:
   - Ghi nhận chính xác mốc thời gian chuyển giao giữa: Bộ phận một cửa ➔ Bộ phận đo đạc ➔ Bộ phận thẩm tra ➔ Bộ phận thuế ➔ Lãnh đạo ký duyệt.
   - Phục vụ chỉ số cải cách hành chính (CCHC).
3. **Tra cứu ngăn chặn giao dịch**:
   - Kiểm tra tức thì xem thửa đất có đang bị tranh chấp, kê biên thi hành án hay cấm chuyển nhượng hay không.
4. **Tương tác với người dân**:
   - Tích hợp cổng SMS tự động nhắn tin tiến độ và thông báo nhận kết quả đến số điện thoại của người dân.

---

## 3. ⚙️ CÔNG NGHỆ ĐỨNG SAU HỆ THỐNG NÀY

- **Frontend**: Single Page Application (SPA) phát triển bằng **Angular**. Mã nguồn biên dịch thành các tệp chunk tĩnh (`main-es2015.*.js`, `vendor-es2015.*.js`). Có kèm Bootstrap 4.5.2, jQuery 3.5.1, CKEditor, Google Analytics.
- **Gateway & CDN**: **Cloudflare** (IP: `172.67.215.43`, `104.21.53.164`) - bảo vệ chống DDoS và cấp phát SSL.
- **Backend API**: Máy chủ Windows Server chạy **Microsoft IIS** với nền tảng **ASP.NET (v4.0.30319)** tại máy chủ API: `https://apisql.vpdkddtdm.vn/api/ChucNang/`.
- **Cơ sở dữ liệu (Database)**: **Microsoft SQL Server (MSSQL)**. Kiến trúc API gọi trực tiếp các Stored Procedure nghiệp vụ (như `postA1011SELEDN`, `PostHT2000ThuTucTongHop`, `postA1012DangNhapA`).

---

## 4. 🚚 ĐÁNH GIÁ TÍNH KHẢ THI KHI CLONE HOẶC DI CHUYỂN SERVER

> ⚠️ **Hiện trạng**: Hệ thống đang "xài ké" server lưu trữ của một công ty khác.

### 4.1. Có tiện không?
**KHÔNG THỂ tự ý copy từ xa nếu không có sự hợp tác bàn giao chính thức từ công ty đang giữ server.**
- **Giao diện (Frontend)**: Tự lấy được (100%) vì chạy phía client trình duyệt.
- **Mã nguồn Backend & Database**: **0% Không thể lấy từ xa**. Toàn bộ logic nghiệp vụ, thủ tục SQL Server và dữ liệu đất đai hàng chục ngàn hồ sơ nằm trên máy chủ nội bộ của công ty đó. Cần có file backup `.bak` của SQL Server và thư mục IIS publish.
- **Kho tệp tin đính kèm (File Storage)**: Ảnh scan sổ đỏ, bản vẽ trích lục nằm trên ổ đĩa server đối tác, cần bàn giao nguyên khối.

### 4.2. Khuyến nghị cho người mới phụ trách:
1. **Làm việc chính thức với đối tác**: Yêu cầu bàn giao file `.bak` (Database), source/publish của Backend API (`apisql.vpdkddtdm.vn`), và thư mục file đính kèm.
2. **Chuẩn bị server độc lập**: Cần 1 máy chủ Windows Server (khuyên dùng RAM tối thiểu 32GB vì SQL Server xử lý dữ liệu địa chính rất nặng, ổ SSD NVMe 500GB+).
3. **Tránh rủi ro pháp lý & bảo mật**: Dữ liệu đất đai là dữ liệu nhà nước nhạy cảm, việc lưu trữ ké trên server tư nhân tiềm ẩn rủi ro rất lớn về gián đoạn vận hành và an toàn thông tin theo quy định.
