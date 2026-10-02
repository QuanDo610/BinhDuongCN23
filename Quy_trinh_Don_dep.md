# Quy Trình Dọn Dẹp và Bảo Trì Dữ Liệu (Weekly Cleanup)

Để đảm bảo hiệu suất xử lý và tránh việc dữ liệu rác làm nhiễu thông tin, chúng ta cần quy trình dọn dẹp định kỳ (có thể hàng tuần) cho toàn bộ thư mục dự án.

## 1. Logic Định Danh File Rác (Trash Identification)

Một file sẽ bị xem là "rác" hoặc "cần dọn dẹp" nếu rơi vào các trường hợp sau:

- **Bị Trùng Lặp (Duplication):** File có cùng nội dung (cùng mã băm MD5) nhưng khác tên, hoặc vô tình bị copy ra nhiều bản ở nhiều thư mục khác nhau.
- **Phiên bản Lỗi Thời (Stale Drafts):** Các file có hậu tố nháp như `_v1`, `_v2`, `_new`, `_old`, `_temp` khi đã có một file mới hơn hoặc file `_FINAL` (Ví dụ: Đã có `phuong_an_v2.docx` thì `phuong_an_v1.docx` nên được dọn dẹp).
- **File Lạc Lõng (Misplaced Files):** 
  - File tài liệu (`.pdf`, `.docx`, `.xlsx`) nằm sai chỗ (ví dụ nằm trong `tools/` hoặc thư mục gốc).
  - File mã nguồn (`.py`, `.js`) nằm trong `documents/` hoặc `OUTPUT/`.
- **Thư Mục Tạm (Temporary/Cache):** Các thư mục tự sinh ra trong quá trình code (VD: `__pycache__`, `.DS_Store`) cần được bỏ qua hoặc xóa sạch định kỳ.

## 2. Quy Trình Dọn Dẹp (Cleanup Process)

Định kỳ vào cuối tuần (hoặc khi người dùng yêu cầu `chạy dọn dẹp hệ thống`), AI hoặc Script tự động (`tools/weekly_cleanup.py` nếu có) sẽ thực hiện:

1. **Kiểm tra thư mục gốc:** Di chuyển toàn bộ file `.py` vào `tools/`. Di chuyển tài liệu vào `documents/`.
2. **Quét Trùng Lặp (Duplicate Scan):** Tính mã MD5 của toàn bộ file trong `documents/` và `OUTPUT/`. Nếu có 2 file giống hệt nhau, giữ lại 1 file có tên hợp lý nhất (ưu tiên file cũ nhất / tên gốc), xóa file copy.
3. **Xử lý Phiên bản (Version Control):** Gom các file nháp (v1, v2, old, new) cũ vào một thư mục `ARCHIVE/` (hoặc `TRASH/`) để dọn trống không gian, chỉ để lại file cuối cùng hoặc file đang làm việc.
4. **Dọn Cache:** Xóa các thư mục `__pycache__` thừa thãi bằng Python script.
5. **Báo cáo (Report):** Tạo một file `Bao_cao_don_dep_[NgayThang].md` trong `OUTPUT/` liệt kê những gì đã được xóa hoặc di chuyển để người dùng nắm được.

## 3. Nguyên tắc Chống Xóa Nhầm

- Tuyệt đối KHÔNG xóa các file cấu hình hệ thống (như các file `.md` tại thư mục gốc, file cấu hình `.gitignore`).
- Khi xử lý trùng lặp, phải đối chiếu MD5 hash, không dựa hoàn toàn vào tên file.
- Thay vì xóa vĩnh viễn (Delete), có thể thiết lập cơ chế chuyển vào thư mục `.TRASH/` để người dùng có thể khôi phục khi cần trong 30 ngày.
