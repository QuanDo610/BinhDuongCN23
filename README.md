# HỆ THỐNG XỬ LÝ VÀ TỰ ĐỘNG HÓA VĂN BẢN VĂN PHÒNG
**Văn phòng Đăng ký Đất đai - Chi nhánh số 23**

Dự án này là bộ công cụ (Framework) tự động hóa các nghiệp vụ văn phòng, giúp tiết kiệm thời gian trong việc xử lý, đối chiếu dữ liệu, báo cáo, và đặc biệt là khởi tạo các văn bản tự động tuân thủ tuyệt đối **Nghị định 30/2020/NĐ-CP**.

---

## 📁 1. Cấu trúc và Nguyên tắc Hoạt động

Hệ thống hoạt động dựa trên các tài liệu cấu trúc xương sống để hướng dẫn AI (Gemini/Antigravity) hoạt động một cách nhất quán:

*   **`Gemini.md` & `Agent.md`**: Quy định về tổng quan luồng làm việc và hành vi của AI.
*   **`Rule.md`**: Các nguyên tắc bất di bất dịch (Không chế biến dữ liệu, Không bỏ sót data).
*   **`Skill.md`**: Tập hợp các kỹ năng nghiệp vụ văn phòng (đọc PDF/DOC/EXCEL, rà soát chéo, sinh báo cáo).
*   **`QUY_CHUAN_DOCX_ND30.md`**: Bộ quy chuẩn kỹ thuật ép buộc mọi file `.docx` được sinh ra phải đạt chuẩn Nghị định 30 (căn lề, cỡ chữ, bảng không viền).
*   **`Cau_truc_Thu_muc.md`**: Quy tắc bắt buộc về cách sắp xếp thư mục.
*   **`Quy_trinh_Don_dep.md`**: Logic dọn dẹp hệ thống, tránh rác và trùng lặp dữ liệu.

### Thư mục làm việc:
*   `documents/`: Nơi **BẠN** tải vào các tài liệu nguồn (văn bản đến, phụ lục, bảng biểu).
*   `OUTPUT/`: Nơi **AI** xuất ra kết quả (văn bản mới, báo cáo HTML/Excel).
*   `tools/`: Chứa các script Python mã nguồn.

---

## 🚀 2. Hướng Dẫn Sử Dụng cho Nhân Viên Văn Phòng

1. **Chuẩn bị dữ liệu:** Copy các file văn bản, nghị định, quyết định, hoặc bảng tính cần xử lý vào thư mục `documents/`.
2. **Ra lệnh cho AI:** Mở khung chat với AI và yêu cầu. Ví dụ:
   * *"Trích xuất dữ liệu từ các file PDF trong documents và lập bảng đối chiếu diện tích ra file HTML."*
   * *"Từ file Bảng đối chiếu, hãy sinh ra một Quyết định phân công chuẩn Nghị định 30."*
   * *"Quét và dọn dẹp hệ thống, xóa các file trùng lặp."*
3. **Nhận kết quả:** Vào thư mục `OUTPUT/` để lấy báo cáo hoặc file văn bản đã hoàn thiện.

---

## 🛠 3. Cài đặt (Dành cho IT / Lần đầu chạy)

1. Mở Terminal (MacOS) / Command Prompt (Windows).
2. Di chuyển vào thư mục dự án: `cd BINHDUONG`
3. Kích hoạt môi trường ảo (nếu có): `source venv/bin/activate` (Mac) hoặc `venv\Scripts\activate` (Win).
4. Cài đặt các thư viện cần thiết: `pip install python-docx openpyxl pandas PyPDF2 pdfplumber`
