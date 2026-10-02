# Kỹ năng Nghiệp Vụ Văn Phòng (Office Workflow Skills)

Để hoàn thành tốt công tác văn thư, hành chính, Agent được trang bị và phải thành thạo các nhóm kỹ năng (Skill) sau đây.
**Yêu cầu hệ thống (Thư viện bắt buộc):** Quá trình setup ban đầu AI phải tự động cài đặt các thư viện: `python-docx`, `openpyxl`, `pandas`, `PyPDF2`, `pdfplumber`.

## 1. Nhóm Kỹ năng Đọc và Trích xuất Dữ liệu (Data Extraction)
- **Đọc PDF chữ (Text-based):** Sử dụng các thư viện như `PyPDF2`, `pdfplumber` để trích xuất văn bản từ PDF.
- **Đọc PDF ảnh (Scanned PDF - OCR):** Khi gặp file PDF scan hoặc hình ảnh không có text, Agent ƯU TIÊN sử dụng công cụ `view_file` (built-in) để đọc trực tiếp bằng thị giác máy tính (AI Vision). Nếu phải viết script tự động hóa hàng loạt, Agent sẽ tự động cài thêm `pytesseract`, `pdf2image` và `Pillow` (Yêu cầu hệ thống phải có Tesseract OCR).
- **Đọc DOCX/XLSX:** Sử dụng `python-docx`, `openpyxl`, `pandas` để rút trích dữ liệu từ các báo cáo, bảng biểu, phụ lục mà không làm mất cấu trúc.
- **Rà soát chéo (Cross-referencing):** Có khả năng đọc nhiều file cùng lúc để đối chiếu sự khớp nhau của số liệu (Ví dụ: Diện tích đất ở Tờ trình có khớp với Bản vẽ và Báo cáo hay không). Không được tự chế biến dữ liệu.

## 2. Nhóm Kỹ năng Sinh Văn Bản Chuẩn (Document Generation)
- **Sinh DOCX chuẩn Nghị định 30/2020/NĐ-CP:** Kỹ năng sinh văn bản tự động tuân thủ TUYỆT ĐỐI hướng dẫn kỹ thuật trong `QUY_CHUAN_DOCX_ND30.md` (Margin, Header/Footer ẩn trang đầu, Quốc hiệu, Tiêu ngữ, Căn cứ pháp lý, Bảng không viền). 
- **Sinh Báo cáo/Phụ lục XLSX:** Khả năng tự động hóa việc xuất dữ liệu ra file Excel với định dạng chuẩn, căn chỉnh phù hợp cho việc in ấn hoặc báo cáo.
- **Mail Merge / Template Generation:** Sử dụng một file mẫu, tự động điền các thông số từ file Excel/PDF để xuất ra hàng loạt các văn bản hành chính (Quyết định, Thông báo,...).

## 3. Nhóm Kỹ năng Phân tích và Tổng hợp (Analysis & Reporting)
- **Báo cáo Trực quan (HTML/MD):** Khả năng tổng hợp sai sót, chênh lệch số liệu và xuất ra một báo cáo phân tích dưới định dạng HTML thuần (chứa HTML, CSS, JS trong 1 file duy nhất) để người dùng dễ dàng mở trên trình duyệt, hoặc file Markdown gọn gàng.
- **Tóm tắt Văn bản dài (Summarization):** Rút gọn các Nghị định, Thông tư dài hàng chục trang thành các gạch đầu dòng trọng tâm.
- **Phát hiện Dữ liệu Thiếu/Sai (Missing & Invalid Data Detection):** Kỹ năng phân tích bảng biểu để chỉ ra chính xác ô nào, dòng nào bị thiếu dữ liệu, sai thuật toán tính toán và cảnh báo (la lên) rõ ràng cho người dùng.

## 4. Nhóm Kỹ năng Quản lý Hệ thống & Dọn Dẹp (System & Cleanup)
- **Quản lý Thư mục:** Tuân thủ chặt chẽ `Cau_truc_Thu_muc.md` (Code ở `tools/`, Dữ liệu ở `documents/`, Kết quả ở `OUTPUT/`).
- **Tự động Dọn dẹp (Cleanup Scripting):** Áp dụng logic trong `Quy_trinh_Don_dep.md` để quét MD5 phát hiện file trùng lặp, xử lý các phiên bản nháp (`_v1`, `_v2`), và di chuyển rác để giữ không gian làm việc sạch sẽ.
