# TÀI LIỆU BÀN GIAO CÔNG VIỆC DỰ ÁN "FAMILY CN23"
> **Hệ thống Cổng Dịch Vụ Nội Bộ - Văn Phòng Đăng Ký Đất Đai Chi Nhánh Số 23**  
> *Ngày cập nhật: 29/10/2026 | Phiên bản hoàn thiện: v3.6-Grid1200 & Scalability Architecture*

---

## 1. THÔNG TIN HỆ THỐNG & ĐỊA CHỈ TRUY CẬP

| Hạng mục | Đường dẫn / Thông số |
| :--- | :--- |
| **Website Cổng Dịch Vụ Hub** | [https://quando610.github.io/vpdk-cn23/index.html](https://quando610.github.io/vpdk-cn23/index.html) |
| **Phân hệ 1: Lịch Công Tác Tuần** | [https://quando610.github.io/vpdk-cn23/lich_tuan.html](https://quando610.github.io/vpdk-cn23/lich_tuan.html) |
| **Phân hệ 2: IT Helpdesk Máy Tính** | [https://quando610.github.io/vpdk-cn23/it_helpdesk.html](https://quando610.github.io/vpdk-cn23/it_helpdesk.html) |
| **Phân hệ 3: Lãnh Đạo Giao Việc** | [https://quando610.github.io/vpdk-cn23/giao_viec.html](https://quando610.github.io/vpdk-cn23/giao_viec.html) |
| **Phân hệ 4: Báo Cáo Số Liệu Tổ & KPI**| [https://quando610.github.io/vpdk-cn23/bao_cao_to.html](https://quando610.github.io/vpdk-cn23/bao_cao_to.html) |
| **Kho mã nguồn GitHub** | [`https://github.com/QuanDo610/vpdk-cn23.git`](https://github.com/QuanDo610/vpdk-cn23.git) *(Branch `main`)* |
| **Google Apps Script API** | `https://script.google.com/macros/s/AKfycbxLjARkYWp2TegCCdMcfVc3W6qQm6PmhFz71-y8zB_xFXxXbRXpsUhk6aPbJtqVqUHE/exec` |
| **Google Spreadsheet Backend** | Trang tính `BINHDUONG23`: `TaiKhoan`, `LichTuan`, `Tickets`, `GiaoViec`, `BaoCaoSoLieu` |

---

## 2. TỔNG HỢP CÁC CÔNG VIỆC HOÀN TẤT TRONG PHIÊN BẢN v3.6

### 2.1. Chuẩn Hóa Toàn Diện Hệ Thống Grid 1200px & Flexbox (Chống Tuyệt Đối Vỡ Layout)
1. **Kiểm tra và sửa toàn bộ CSS / HTML trong hệ thống:**
   - Cập nhật `.main-content` và `.header-container` trong `css/style.css` sang chuẩn `max-width: 1280px; width: 100%; margin: 20px auto; padding: 0 16px; box-sizing: border-box;`.
   - Cập nhật toàn bộ thẻ Header và Main Container trên `it_helpdesk.html`, `giao_viec.html`, `bao_cao_to.html` từ `max-w-[1720px]` về chuẩn đồng nhất `max-w-7xl` (1280px).
   - Thêm lớp khóa toàn cục `html, body { overflow-x: hidden; width: 100%; }` và `img, svg { max-width: 100%; }` ngăn chặn triệt để hiện tượng thanh cuộn ngang xuất hiện vô lý trên màn hình cơ quan.
   - Bổ sung `min-w-0` trên các thẻ Flex child chứa text dài và áp dụng `truncate` kết hợp Modal popup xem toàn văn.
   - Đảm bảo các bảng biểu dữ liệu chuyên môn (Lịch tuần, Tiến độ, Báo cáo) đều có `table-layout: fixed; min-width: 1200px;` đặt trong wrapper `overflow-x: auto;`.

2. **Cập nhật Bộ Quy Chuẩn Kỹ Thuật:**
   - Bổ sung **Mục 5: Kiến Trúc Bố Cục 1200px Grid System & Flexbox Responsive Hiện Đại** vào `docs/SKILL.md`.
   - Bổ sung **Quy Tắc 10: Tiêu Chuẩn Container 1200px & Chống Vỡ Layout (Zero Broken Layout)** vào `docs/RULE.md`.

### 2.2. Hoàn Thành Chuyên Đề Tư Vấn Kiến Trúc Dữ Liệu & Khả Năng Mở Rộng
- Phân tích chi tiết 3 mô hình: **Google Sheets + Apps Script** vs **JSON Flat File** vs **Database Thực Thụ (Supabase/PostgreSQL/Firebase)**.
- Phân tích cặn kẽ tại sao JSON file không thể ghi trực tiếp trên GitHub Pages và dễ gặp lỗi Race Condition.
- Đánh giá dung lượng thực tế với 82 nhân sự CN23 (~5.000 - 12.000 dòng/năm) chứng minh Google Sheets hoàn toàn chạy tốt trong 2-3 năm tới.
- Đề xuất lộ trình công nghệ 2 giai đoạn:
  * **Giai đoạn 1 (Hiện tại):** Hybrid Caching (`localStorage` phản hồi tức thì 0ms + Background Sync lên Google Sheets).
  * **Giai đoạn 2 (Tương lai khi > 30.000 dòng hoặc mở rộng toàn TP):** Chuyển sang Supabase (PostgreSQL) kèm cơ chế sao lưu tự động (Mirror Backup) về Google Drive.
- Cập nhật đầy đủ vào **Mục 6: Kiến Trúc Dữ Liệu & Khả Năng Mở Rộng** trong `docs/SKILL.md`.

### 2.3. Nâng Cấp Hệ Thống Menu Cố Định Bên Trái (Solid Royal Navy & Chế Độ Thu Gọn 3 Gạch)
1. **Màu sắc Solid Royal Navy thuần nhất:**
   - Chuyển màu nền Sidebar sang **Xanh Royal Navy thuần khiết (`#1e3a8a`)**, bỏ hoàn toàn hiệu ứng gradient chuyển màu.
   - Giữ đường viền chỉ vàng kim Chi nhánh 23 (`#f59e0b`) và hiệu ứng hover/active sáng rõ, trang nhã.
2. **Chuẩn hóa tên gọi menu gọn gàng (Không dùng Badge bên cạnh gây `...`):**
   - Đặt lại tên các mục rõ nghĩa, không bị rớt dòng:
     * `Trang chủ`
     * `Đăng ký lịch tuần`
     * `IT Helpdesk`
     * `Giao việc`
     * `Báo cáo số liệu`
     * `Kho cài đặt` (liên kết mở Google Drive)
   - Bỏ hoàn toàn các thẻ badge bên phải (Hub, NĐ 30, Online, 82 CB, Drive) để giải phóng toàn bộ chiều ngang cho chữ, đảm bảo văn bản hiển thị nguyên vẹn 100%, không bao giờ bị cắt thành dấu ba chấm `...`.
3. **Chuẩn hóa thông tin cơ quan tại đỉnh Sidebar:**
   - Đổi tiêu đề đỉnh Sidebar sang: **VP ĐĂNG KÝ ĐẤT ĐAI** &bull; *Chi nhánh số 23 &bull; Portal* (thay vì để Family CN23 vốn chỉ dành cho tên icon Desktop).

### 2.4. Tái Cấu Trúc CSS Phân Tầng (Modular CSS Architecture) & Header Dài Hết Màn Hình
1. **Kiến trúc Design Tokens `:root` & Hệ thống Component Chuẩn Hóa:**
   - Tạo mới `css/variables.css`: Quản lý tập trung toàn bộ biến `:root` (màu sắc cơ quan, kích thước layout 1280px, spacing, typography, radius, shadow).
   - Tạo mới `css/base.css`: Kế thừa `variables.css`, cung cấp các lớp tiện ích dùng chung chuẩn hóa Bootstrap-like (`.btn`, `.btn-primary`, `.card`, `.form-control`, `.badge`, `.app-container`, `.table-responsive`) và khóa toàn cục chống tràn ngang (`overflow-x: hidden`).
   - Tách riêng biệt từng file CSS cho từng trang:
     * `css/hub.css`: Giao diện Hub trung tâm & Form đăng nhập thẻ nổi.
     * `css/lich_tuan.css`: Bảng Lịch Tuần full-width & Hệ thống 2 Tab.
     * `css/it_helpdesk.css`: Lưới 2 cột tiếp nhận & Thẻ sự cố.
     * `css/giao_viec.css`: Thẻ KPI & Bảng theo dõi tiến độ.
     * `css/bao_cao_to.css`: Thẻ chỉ tiêu chuyên môn & Bảng số liệu.
2. **Top Header Chạy Dài Toàn Màn Hình (`app-topbar`) + Sidebar Dưới Header (`app-sidebar`):**
   - Tạo mới module `js/layout.js`: Tự động khởi tạo và chèn **Full-Width Topbar** (cố định `top: 0`, cao `62px`, rộng `100%`) hiển thị đầy đủ tên cơ quan: *VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI THÀNH PHỐ HỒ CHÍ MINH - CHI NHÁNH SỐ 23*, kèm nút 3 gạch `☰`, thông tin cán bộ đăng nhập và nút Đăng xuất.
   - Sidebar được gắn cố định trực tiếp **bên dưới Header** (`top: 62px; height: calc(100vh - 62px)`), giải quyết triệt để lỗi icon và nút 3 gạch chồng chéo lên nhau khi thu gọn.
   - Nút 3 gạch `☰` nằm trên Header: khi bấm, Sidebar thu gọn về chế độ **Mini Icon-Only (`68px`)**, nội dung trang tự động giãn rộng mượt mà, lưu trạng thái vào `localStorage`.
   - Đã đồng bộ liên kết CSS và `layout.js` vào 100% cả 5 trang HTML: `index.html`, `lich_tuan.html`, `it_helpdesk.html`, `giao_viec.html`, `bao_cao_to.html`.
3. **Tư Vấn Chuyên Sâu: Có Nên Dùng Bootstrap CDN Không?:**
   - **Khuyến nghị:** **KHÔNG NÊN** nhúng file Bootstrap CDN (`bootstrap.min.css`).
   - **Lý do:**
     * Bootstrap CDN mang bảng màu mặc định màu xanh dương Twitter (`#0d6efd`), làm mất tính nhận diện Xanh Hoàng Gia Royal Navy (`#1e3a8a`) và Vàng Kim (`#f59e0b`) của cơ quan.
     * Bootstrap CDN sẽ xung đột nghiêm trọng với các lớp Tailwind CDN đang dùng trên `it_helpdesk.html`, `giao_viec.html`, `bao_cao_to.html` (do trùng lặp tên class `.container`, `.card`, `.badge`, `.collapse`, `.modal`, dẫn đến lỗi vỡ giao diện).
     * Bộ `variables.css` + `base.css` vừa xây dựng đã cung cấp đầy đủ các class thông dụng như Bootstrap nhưng nhẹ hơn, không có mã thừa và tương thích 100% với hệ sinh thái cơ quan.

---

## 2. TỔNG HỢP CÁC CÔNG VIỆC ĐÃ HOÀN TẤT (PHIÊN BẢN v3.5)

### 2.1. Hoàn Thành Phân Hệ 3: Lãnh Đạo Giao Việc & Bảng Tiến Độ (`giao_viec.html`)
- **Nghiệp vụ cốt lõi:**
  1. **Form Giao việc & Chỉ đạo:**
     - Tự động nhận diện Lãnh đạo giao việc theo tài khoản đăng nhập (hoặc chọn từ danh sách Ban Giám đốc & Lãnh đạo các tổ).
     - Bộ lọc theo Tổ chuyên môn và danh sách **82 cán bộ viên chức chính thức** thuộc 5 tổ, hiển thị chức vụ và ghi chú nhân sự thời gian thực.
     - Tiêu đề công việc, Độ khẩn (🟢 Bình thường / 🟠 Khẩn / 🔴 Hỏa tốc có hiệu ứng nhấp nháy), Hạn chót hoàn thành (Deadline).
     - Văn bản căn cứ / Mã VBDLIS, tệp hồ sơ đính kèm, ý kiến chỉ đạo chi tiết của Lãnh đạo.
  2. **5 Thẻ KPI Giám Sát Tiến Độ:**
     - Tổng công việc, Đang thực hiện, Quá hạn Deadline (cảnh báo đỏ nhấp nháy), Đã hoàn thành, Tỷ lệ hoàn thành (%).
  3. **Bảng Desktop-First Theo Dõi Tiến Độ:**
     - Thiết kế theo chuẩn `SKILL.md` chống rớt chữ: cố định độ rộng cột, văn bản dài tự động rút gọn `...`, rê chuột xem tooltip hoặc click vào bất kỳ dòng nào để mở **Modal Popup xem toàn văn chi tiết**.
     - Bộ lọc trạng thái (Đang làm, Hoàn thành, Quá hạn), bộ lọc tổ, và ô tìm kiếm tức thì.
     - Nút đánh dấu Hoàn thành ✓ / Mở lại ↩, In phiếu giao việc chuẩn A4 có quốc hiệu và chữ ký, Xuất bảng danh sách ra Excel CSV.
     - Tích hợp lưu trữ kép: `localStorage` offline phản hồi tức thì + tự động đồng bộ ngầm lên Google Sheet qua API (`createTask`, `updateTaskStatus`, `deleteTask`, `getTasks`).

### 2.2. Hoàn Thành Phân Hệ 4: Báo Cáo Số Liệu Thực Hiện Cấp Tổ & KPI (`bao_cao_to.html`)
- **Nghiệp vụ cốt lõi:**
  1. **Biểu mẫu thu thập 8 nhóm chỉ tiêu chuyên môn:**
     - Thông tin chung: Tổ chuyên môn, Loại kỳ (Tuần / Tháng / Quý / Đột xuất), Tên kỳ, Ngày chốt số liệu.
     - Nhóm 1: Tiếp nhận hồ sơ (Trực tiếp, Trực tuyến) -> Tự động tính Tổng tiếp nhận & Tỷ lệ nộp trực tuyến (%).
     - Nhóm 2: Kết quả giải quyết (Trước hạn, Đúng hạn, Quá hạn, Thư xin lỗi) -> Tự động tính Tổng giải quyết & Tỷ lệ đúng hạn (%).
     - Nhóm 3: Hồ sơ đang xử lý (Tồn trong hạn, Tồn quá hạn) -> Tự động tính Tổng tồn đọng.
     - Nhóm 4: Nghĩa vụ tài chính & Thanh toán trực tuyến -> Tự động tính Tỷ lệ thanh toán trực tuyến (%) & Tổng số tiền thu.
     - Nhóm 5: Công tác số hóa hồ sơ (Đầu vào, Đầu ra, Tái sử dụng, Bản sao điện tử).
     - Nhóm 6: Vận hành hệ thống VBDLIS & CSDL dân cư.
     - Nhóm 7 & 8: Khó khăn vướng mắc & Đề xuất kiến nghị với Ban Giám đốc.
  2. **4 Thẻ KPI Giám Sát Chỉ Tiêu Cấp Trên:**
     - Tổng hồ sơ tiếp nhận.
     - Tỷ lệ trực tuyến (Xanh nếu đạt ≥ 50%, Vàng nếu < 50%).
     - Tỷ lệ đúng hạn (Xanh nếu đạt ≥ 98%, Đỏ cảnh báo nếu < 98%).
     - Tỷ lệ thanh toán trực tuyến (Xanh nếu đạt ≥ 40%, Vàng nếu < 40%).
  3. **Bảng Lịch Sử & Thống Kê Kỳ Báo Cáo:**
     - Lọc theo tổ, xem chi tiết modal từng bản ghi, in báo cáo A4 trang trọng có đầy đủ bảng số liệu 5 phần và chữ ký Tổ trưởng / Người lập biểu.
     - Xuất toàn bộ lịch sử ra tệp Excel CSV.
     - Tích hợp lưu trữ kép `localStorage` + API Google Sheet (`createPerformanceReport`, `deletePerformanceRecord`, `getPerformanceReports`).

### 2.3. Nâng Cấp Trang Chủ Hub (`index.html`) Thành Lưới 4 Phân Hệ
- Chuyển đổi lưới 2 card cũ thành **Lưới 4 Card Phân Hệ Nghiệp Vụ Hoàn Chỉnh**:
  1. Đăng ký Lịch công tác tuần (Chuẩn NĐ 30/2020).
  2. IT Helpdesk & Báo sự cố máy tính (Live Monitoring).
  3. Lãnh đạo Giao việc & Bảng tiến độ (Đôn đốc nhiệm vụ).
  4. Báo cáo Số liệu thực hiện cấp Tổ & KPI (8 nhóm chỉ tiêu).
- Thiết kế màu sắc riêng biệt cho từng thẻ nhưng tuân thủ 100% Design System:
  - Thẻ Lịch tuần: Xanh lá Emerald
  - Thẻ IT Helpdesk: Xanh dương Royal
  - Thẻ Giao việc: Vàng hổ phách Amber Gold
  - Thẻ Báo cáo tổ: Xanh mòng két Teal

### 2.4. Đồng Bộ Thanh Header Điều Hướng Toàn Hệ Thống
- Cả 4 trang web ([index.html](file:///Users/admin/Desktop/BINHDUONG/A_THANG/index.html), [lich_tuan.html](file:///Users/admin/Desktop/BINHDUONG/A_THANG/lich_tuan.html), [it_helpdesk.html](file:///Users/admin/Desktop/BINHDUONG/A_THANG/it_helpdesk.html), [giao_viec.html](file:///Users/admin/Desktop/BINHDUONG/A_THANG/giao_viec.html), [bao_cao_to.html](file:///Users/admin/Desktop/BINHDUONG/A_THANG/bao_cao_to.html)) đều được tích hợp thanh điều hướng chéo giúp cán bộ chuyển đổi qua lại giữa bất kỳ phân hệ nào chỉ với 1 cú click mà không cần quay lại trang đăng nhập.

### 2.5. Nâng Cấp Backend Google Apps Script (`backend/google_apps_script.js`)
- Hỗ trợ toàn bộ 5 tab trên Google Sheet:
  - `TaiKhoan`: Xác thực CCCD & Mật khẩu
  - `LichTuan`: Đăng ký lịch tuần
  - `Tickets`: Sự cố tin học & lưu ảnh Drive
  - `GiaoViec`: Quản lý 14 trường thông tin giao việc
  - `BaoCaoSoLieu`: Quản lý 32 trường thông tin 8 nhóm chỉ tiêu
- Cập nhật menu `⭐ BINHDUONG23` với lệnh **1-Click cấu hình chuẩn toàn bộ 5 phân hệ**.

### 2.6. Quy Chuẩn Quy Trình Làm Việc Mới (Bắt Buộc Tuân Thủ)
- **Pipeline 2 Giai Đoạn (Design-First):**
  1. *Giai đoạn 1 (Designer):* Dựng layout HTML/CSS, bố cục giao diện, thẻ, bảng biểu tĩnh. Trình bày người dùng xem và duyệt trước.
  2. *Giai đoạn 2 (Developer/Backend):* Chỉ viết script logic, tương tác JS, API và Google Apps Script sau khi người dùng đã chốt layout. Không làm gộp một mớ cùng lúc.
- **Kỷ Luật Git Push:**
  - Tuyệt đối KHÔNG tự ý push lên GitHub remote khi chưa có lệnh từ người dùng.
  - Toàn bộ việc phát triển và kiểm thử phải được thực hiện ở Local. Chỉ push khi người dùng chỉ đạo trực tiếp.

### 2.7. Nâng Cấp Đăng Nhập Bằng Cột Username (Tên + Họ Tên Lót Viết Tắt: Quân ĐTM)
- **Thuật toán sinh Username chuẩn:**
  - Quy tắc: Tên chính + Chữ cái đầu viết hoa của Họ và các Tên lót (Ví dụ: `Đỗ Trọng Minh Quân` -> `Quân ĐTM`, `Nguyễn Văn An` -> `An NV`).
  - Hỗ trợ công thức trực tiếp trên Google Sheets: `=TAO_USERNAME(C2)`.
  - Hỗ trợ menu 1-click trên Google Sheet: **`⭐ BINHDUONG23` -> `🔤 Tự động tạo & điền Username (Quân ĐTM)`**.
- **Cơ chế so khớp xác thực thông minh:**
  - Tự động nhận diện cột `Username` ở bất kỳ vị trí nào trong tab `TaiKhoan` (ưu tiên cột cuối bảng do người dùng thêm vào).
  - So khớp linh hoạt: không phân biệt hoa thường (`Quân ĐTM`, `quân đtm`), cho phép gõ liền (`quandtm`), và hỗ trợ gõ không dấu (`Quan DTM`).
  - Dự phòng 100%: Nếu ô `Username` trên Google Sheet chưa kịp điền, hệ thống tự động suy luận Username từ cột Họ tên để cán bộ đăng nhập ngay lập tức.
  - Vẫn giữ nguyên khả năng đăng nhập dự phòng bằng số CCCD hoặc Số điện thoại.
- **Đồng bộ giao diện Web Portal (`index.html`):**
  - Ô đăng nhập hỗ trợ nhập Username hoặc CCCD, bỏ ràng buộc `numeric` để cán bộ thoải mái gõ chữ.
  - Nhãn hiển thị và cơ chế lưu trữ phiên làm việc cập nhật đồng bộ.

---

## 3. CẤU TRÚC THƯ MỤC HOÀN CHỈNH HIỆN TẠI

```text
A_THANG/
│
├── index.html                      # Cổng Dịch Vụ Nội Bộ Hub (Lưới 4 phân hệ)
├── lich_tuan.html                  # Phân hệ 1: Đăng ký lịch tuần & Xuất Word NĐ 30
├── it_helpdesk.html                # Phân hệ 2: IT Helpdesk tiếp nhận & chẩn đoán sự cố
├── giao_viec.html                  # Phân hệ 3: Lãnh đạo giao việc & Bảng tiến độ
├── bao_cao_to.html                 # Phân hệ 4: Báo cáo số liệu thực hiện cấp Tổ & KPI
│
├── css/                            # Bảng định kiểu phân tầng (Modular CSS)
│   ├── variables.css               # Design System Tokens (:root biến toàn cục)
│   ├── base.css                    # Khung giao diện App Shell, Reset & Bootstrap-like Utilities
│   ├── hub.css                     # Stylesheet chuyên biệt Cổng Hub trung tâm & Đăng nhập
│   ├── lich_tuan.css               # Stylesheet chuyên biệt Đăng ký Lịch tuần & 2-Tab Switcher
│   ├── it_helpdesk.css             # Stylesheet chuyên biệt IT Helpdesk Máy Tính
│   ├── giao_viec.css               # Stylesheet chuyên biệt Lãnh Đạo Giao Việc & Tiến Độ
│   ├── bao_cao_to.css              # Stylesheet chuyên biệt Báo Cáo Số Liệu Tổ & KPI
│   └── flatpickr.min.css           # Thư viện chọn ngày tháng
│
├── js/                             # JavaScript thuần (Vanilla JS ES6+)
│   ├── layout.js                   # Layout Controller (Full-Width Topbar + Collapsible Sidebar)
│   ├── app.js                      # Logic phân hệ Lịch tuần
│   ├── flatpickr.min.js            # Thư viện Datepicker
│   └── test_suite.js               # Bộ kiểm thử tự động
│
├── backend/                        # Mã nguồn máy chủ Google Apps Script
│   └── google_apps_script.js       # API Gateway xử lý Auth, 5 Sheet Tabs, Drive upload
│
├── assets/                         # Toàn bộ tài nguyên tĩnh
│   ├── icons/                      # Bộ nhận diện Pikachu & VPĐK (.ico)
│   ├── images/                     # Ảnh xem trước (preview png)
│   ├── installer/                  # Bộ cài đặt phím tắt Desktop 1-Click (.bat, .zip)
│   └── templates/                  # Biểu mẫu gốc BM_bao_cao...html & Word mẫu
│
├── docs/                           # TẬP TRUNG TOÀN BỘ FILE TÀI LIỆU (.md)
│   ├── GEMINI.md                   # Kiến trúc hệ thống & nguyên tắc phát triển
│   ├── AGENT.md                    # Vai trò, tác phong & nguyên tắc bảo mật của AI
│   ├── SKILL.md                    # Kỹ năng Vanilla Web, CDN & Bảng mã màu chuẩn
│   ├── RULE.md                     # 7 nguyên tắc vàng cốt lõi (Desktop-first, Zero leak)
│   ├── README.md                   # Thuyết minh chi tiết tính năng toàn hệ thống
│   ├── HANDOFF.md                  # Nhật ký bàn giao kỹ thuật này
│   ├── HD_TRIEN_KHAI.md            # Hướng dẫn nâng cấp 5 tab trên Google Sheet
│   ├── req.md                      # Yêu cầu nghiệp vụ
│   └── task.md                     # Quản lý danh mục nhiệm vụ
│
├── pikachu_badge.ico               # Giữ tại root phục vụ URL tải trực tiếp từ GitHub
├── Family_CN23_Desktop.zip         # Giữ tại root phục vụ URL tải trực tiếp từ GitHub
└── README.md                       # Trang bìa GitHub tổng quan điều hướng vào docs/
```
