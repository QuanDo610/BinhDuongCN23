# Gemini Instructions (Project BINHDUONG)

## Tổng quan dự án
Dự án này tập trung vào việc xử lý các văn bản pháp lý, hành chính (công văn, nghị định, nghị quyết, quyết định, v.v.).

## Cấu trúc thư mục
- `documents/`: Chứa các tài liệu gốc (input). **Tuyệt đối không sửa đổi các file trong thư mục này.** Người dùng sẽ tải các tài liệu pháp lý vào đây.
- `OUTPUT/`: Chứa các file kết quả sau khi xử lý (output).
- Các file tài liệu hướng dẫn (`Gemini.md`, `Agent.md`, `Rule.md`, `Skill.md`, `QUY_CHUAN_DOCX_ND30.md`, `Cau_truc_Thu_muc.md`, `Quy_trinh_Don_dep.md`, `TIEU_CHI_RA_SOAT.md`) đóng vai trò là bộ khung (framework) để AI hoạt động nhất quán và giữ hệ thống sạch sẽ.

## Quy trình làm việc tiêu chuẩn
1. Nhận yêu cầu từ người dùng.
2. Đọc và phân tích tài liệu nguồn trong thư mục `documents/`.
3. Xử lý dữ liệu tuân thủ tuyệt đối các quy tắc trong `Rule.md`.
4. Xuất kết quả ra thư mục `OUTPUT/` theo định dạng được yêu cầu (docx, xlsx, pdf, html). **ĐẶC BIỆT: Mọi file `.docx` mặc định 100% tuân thủ toàn diện thể thức Nghị định 30/2020/NĐ-CP theo [QUY_CHUAN_DOCX_ND30.md](file:///Users/admin/Desktop/BINHDUONG/QUY_CHUAN_DOCX_ND30.md) mà không cần người dùng phải nhắc lại trong từng yêu cầu.**
5. Báo cáo lại cho người dùng về kết quả và đặc biệt là các dữ liệu bị thiếu (nếu có).
