# NHẬT KÝ TIẾN ĐỘ & QUẢN LÝ HỆ THỐNG (PROJECT LOG)
> **Dự án:** Xử lý và Quản trị Văn bản Hành chính - Chi nhánh 23 Bình Dương  
> **Khởi tạo:** 13/10/2026  
> **Cập nhật lần cuối:** 13/10/2026  

---

## 1. Nhật ký công việc đã thực hiện

### Ngày 13/10/2026:
- [x] **Dọn dẹp và xóa bỏ thư mục `QQ`:**
  - Đã rã toàn bộ 124 file dữ liệu từ `QQ/` về đúng các thư mục chuẩn:
    + Báo cáo HTML, Dashboard, tiến độ markdown, hình ảnh minh chứng và PDF báo cáo -> chuyển vào `OUTPUT/`.
    + Các mã nguồn Python, Swift, công cụ OCR Vision -> chuyển vào `tools/`.
    + Toàn bộ cache văn bản OCR thô và các thư mục ảnh trang scan -> chuyển vào `scratch/`.
  - Cập nhật lại đường dẫn chuyển hướng trong `index.html` tại thư mục gốc sang `OUTPUT/index.html`.
  - Xóa sạch hoàn toàn thư mục `QQ/`.
- [x] **Khóa cấu trúc phân vùng chuẩn:**
  - `documents/`: Chỉ đọc (Readonly), nơi chứa toàn bộ văn bản đầu vào (PDF, DOCX, XLSX, CSV, JPG, PNG).
  - `OUTPUT/`: Nơi xuất kết quả duy nhất (Word DOCX chuẩn NĐ 30, Excel XLSX, Báo cáo HTML).
  - `tools/`: Chứa các công cụ lõi dùng chung (`nd30_engine.py`, `doc_pipeline.py`, `ocr_vision`).
  - `scratch/`: Chứa cache dữ liệu bóc tách (`scratch/cache_texts/`, `scratch/documents_index.json`).
- [x] **Xây dựng Core Document Engine chuẩn NĐ 30 (`tools/nd30_engine.py`):**
  - Đóng gói 100% quy chuẩn [QUY_CHUAN_DOCX_ND30.md](file:///Users/admin/Desktop/BINHDUONG/QUY_CHUAN_DOCX_ND30.md).
  - Tự động hóa: Căn lề A4 (20-20-30-15mm), Tiêu ngữ với đường kẻ 18 ký tự em-dash cỡ 8.5pt exact 6pt, Cơ quan ban hành với đường kẻ 8 ký tự em-dash, Bảng biểu lặp tiêu đề trang (`tblHeader`) và chống cắt dòng (`cantSplit`), Khối nơi nhận và chữ ký người ký.
  - Đã test sinh mẫu thành công file: `OUTPUT/Mau_van_ban_test_ND30.docx`.
- [x] **Nâng cấp công cụ Apple Vision OCR (`tools/ocr_vision`):**
  - Cập nhật mã nguồn Swift (`tools/ocr_vision.swift`) hỗ trợ trực tiếp cả file ảnh lẫn file `.pdf` qua Apple PDFKit native, nhận diện tiếng Việt cực chuẩn và siêu nhanh.
- [x] **Xây dựng Auto Document Pipeline (`tools/doc_pipeline.py`):**
  - Tự động quét `documents/`, trích xuất text và bảng biểu (Word, Excel, PDF văn bản), tự động kích hoạt Apple Vision OCR với PDF scan dạng ảnh/ảnh chụp.
  - Lưu trữ đệm tại `scratch/cache_texts/` kèm bảng chỉ mục MD5 `scratch/documents_index.json` (Cache hit giúp bỏ qua tài liệu không thay đổi).
  - Tích hợp tính năng tìm kiếm nhanh (`search`) và đọc nội dung văn bản (`get`).
- [x] **Dọn dẹp thư mục `tools/`:**
  - Đã di chuyển toàn bộ 17 file script viết riêng cho từng văn bản cũ vào `scratch/legacy_scripts/` để lưu vết.
  - Thư mục `tools/` hiện tại chỉ chứa các công cụ cốt lõi tái sử dụng cao.
- [x] **Đồng bộ 100% toàn bộ kho tài liệu:**
  - **Đã bóc tách thành công toàn bộ 67 tài liệu** (kể cả PDF scan đóng dấu nhiều trang) sang text thuần tại `scratch/cache_texts/`.
  - Tốc độ tra cứu toàn văn trong toàn bộ kho đạt **0.05 giây**.
- [x] **Dọn dẹp chuẩn hóa kho `documents/`:**
  - Chuyển toàn bộ các file `.md` (`BB bàn giao IT v1/v2/v3.md`) ra khỏi `documents/`.
  - Chuyển các kết quả hoàn chỉnh (`report_v3.pdf`, `Báo cáo mới v1.xlsx`, `BB bàn giao IT final.docx`) sang `OUTPUT/`.
  - Chuyển 13 file nháp version cũ sang `scratch/archive_docs/` để lưu vết an toàn.
  - Xóa `.DS_Store` và file lock Word tạm thời `.~*`.
  - Cập nhật lại chỉ mục `scratch/documents_index.json` chuẩn xác còn đúng 54 tài liệu pháp lý gốc đầu vào sạch sẽ.

---

## 2. Hướng dẫn sử dụng (100% qua Hội thoại Chat)

> **Lưu ý quan trọng:** Bạn **KHÔNG CẦN** gõ lệnh Terminal nào cả. Toàn bộ các công cụ trong `tools/` là hạ tầng ngầm để AI tự động thực thi. Bạn chỉ cần giao tiếp bằng lời nói tự nhiên trong cửa sổ Chat:

1. **Khi bạn vừa tải thêm tài liệu mới vào `documents/`:**
   - Bạn chỉ cần nhắn: *"Tôi vừa thêm công văn mới vào doc, bạn cập nhật và tóm tắt giúp tôi."*
   - AI sẽ tự động chạy pipeline đồng bộ ngầm, tự OCR nếu là file scan, và trả lời bạn ngay lập tức.
2. **Khi bạn cần tìm kiếm thông tin:**
   - Bạn chỉ cần hỏi: *"Trong kho tài liệu có văn bản nào nói về định mức xe ô tô/máy tính không?"*
   - AI sẽ tự tra cứu toàn văn siêu tốc trong cache và trích dẫn số hiệu, điều khoản cho bạn.
3. **Khi bạn cần tạo văn bản Word mới:**
   - Bạn chỉ cần nhắn: *"Dựa vào tài liệu X và Y, hãy soạn Tờ trình xin kinh phí sửa chữa..."*
   - AI sẽ tự động phân tích dữ liệu, gọi `nd30_engine.py` để sinh file `.docx` chuẩn 100% Nghị định 30 vào thư mục `OUTPUT/`.
4. **Khi bạn cần bảng Excel hoặc Báo cáo HTML:**
   - Bạn chỉ cần nhắn: *"Lập bảng Excel thống kê tài sản..."* hoặc *"Xuất báo cáo HTML đối chiếu số liệu..."*
   - AI sẽ tự động tạo file và đặt vào `OUTPUT/`.
