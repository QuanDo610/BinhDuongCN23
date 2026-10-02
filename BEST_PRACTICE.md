# 📘 CẨM NANG VẬN HÀNH DỰ ÁN (BEST PRACTICES & WORKFLOW)
*Tài liệu hướng dẫn chuẩn hóa quy trình làm việc với dữ liệu và AI dành cho nhân viên văn phòng.*

---

## 1. ⚙️ Cài đặt & Khởi tạo (Dành cho người không chuyên)

Bạn không cần biết code để sử dụng hệ thống này. Hãy làm theo 3 bước sau:

1. **Cài đặt Antigravity:** Truy cập `https://antigravity.google` để tải và cài đặt ứng dụng **Google Antigravity**. Chọn model **Gemini 3.1 Pro** để có sức mạnh tốt nhất.
2. **Cấp quyền Tự động (Full Turbo):**
   - Tải thư mục dự án `BINHDUONG` về máy và mở bằng Antigravity.
   - Vào phần **Cài đặt (Settings)** của Antigravity, bật tùy chọn cho phép AI chạy lệnh Terminal tự động mà không cần hỏi (Auto-approve tool calls).
3. **Cài đặt bằng "Câu Thần Chú":**
   - Copy nguyên văn câu lệnh dưới đây dán vào khung chat của Antigravity và bấm Enter:
   > *"Tôi là nhân viên văn phòng mới. Hãy đọc kỹ thư mục dự án này (đặc biệt là Skill.md) và tự động setup toàn bộ môi trường làm việc cho tôi. Khởi tạo venv, cài đặt toàn bộ thư viện python cần thiết. Cứ tự động chạy, làm xong thì báo cáo cho tôi."*

Hệ thống sẽ tự động cài đặt mọi thứ (Python, thư viện xử lý Word/Excel/PDF...) trong vòng 1-2 phút!

---

## 2. 🔄 Luồng Công Việc Tổng Quan (Workflow)

Quá trình xử lý văn bản trong dự án tuân theo luồng công việc 1 chiều, đảm bảo tính an toàn cho dữ liệu gốc và tính chuẩn xác của đầu ra.

```mermaid
flowchart TD
    A[Nhận tài liệu từ cấp trên\n(Zalo, Email, iDesk)] -->|Tải về máy| B(Thư mục: /documents)
    B -->|Ra lệnh cho AI| C{AI Xử lý Dữ liệu\n(Chạy Python/Phân tích)}
    
    C -->|Sinh Văn Bản NĐ30| D[Thư mục: /OUTPUT\n(File .docx)]
    C -->|Lọc Báo Cáo| E[Thư mục: /OUTPUT\n(File .xlsx, .html)]
    C -->|Báo Lỗi Dữ Liệu| F[Cảnh báo thiếu Data]
    
    D --> G((In Ấn / Trình Ký))
    E --> G
```

> [!IMPORTANT]
> **Nguyên tắc "Chỉ Đọc" (Read-only):** Tuyệt đối không mở các file trong `/documents` ra sửa trực tiếp bằng tay. Nếu file sai, hãy để AI tạo ra một bản sửa lỗi lưu tại `/OUTPUT`. Điều này giúp giữ nguyên bằng chứng gốc.

---

## 2. 📁 Quy Chuẩn Tổ Chức Dữ Liệu

Khi bạn clone/tải dự án này về máy, hãy luôn ghi nhớ 3 không gian làm việc chính:

| Thư mục | Chức năng | Phân quyền của bạn |
| :--- | :--- | :--- |
| 📂 **`documents/`** | Nơi chứa dữ liệu thô (Công văn đến, Phụ lục, PDF). | Bỏ file vào đây. Không sửa, không xóa. |
| 📂 **`OUTPUT/`** | Nơi AI trả kết quả (Quyết định, Báo cáo, Bảng biểu). | Lấy file từ đây đem đi in ấn, báo cáo. |
| 📂 **`tools/`** | Nơi chứa bộ não mã nguồn của dự án (Code). | **KHÔNG đụng vào** (Trừ khi bạn là IT). |

---

## 3. 🏷️ Quy Chuẩn Đặt Tên File (Naming Convention)

Để hệ thống (và AI) dễ dàng nhận diện và dọn dẹp, toàn bộ file khi đưa vào hệ thống phải tuân thủ quy tắc sau:

*   ❌ **Không dùng khoảng trắng và tiếng Việt có dấu:** (Máy tính rất ghét điều này).
    *   Sai: `Báo cáo tháng 9 bản mới.docx`
    *   Đúng: `Bao_cao_thang_9_ban_moi.docx`
*   ✅ **Sử dụng Dấu gạch dưới (`_`) để phân cách chữ.**
*   ✅ **Quản lý Phiên bản (Versioning):**
    *   Khi đang nháp, thêm hậu tố: `_v1`, `_v2`. Ví dụ: `Phuong_an_CN23_v1.docx`
    *   Khi đã chốt, thêm hậu tố: `_FINAL`. Ví dụ: `Phuong_an_CN23_FINAL.docx`
*   ✅ **Gắn Ngày tháng (Nếu cần):** Dùng định dạng `YYYYMMDD`. Ví dụ: `Bao_cao_20261002.xlsx`

> [!TIP]
> Việc đặt tên chuẩn giúp bộ máy dọn dẹp hàng tuần của AI biết đâu là file nháp để dọn vào thùng rác, và đâu là file `_FINAL` để giữ lại mãi mãi.

---

## 4. 🤖 Kỹ Năng "Ra Lệnh" Cho AI (Prompting)

Dự án này được gắn một bộ "Não" (Agent) đã được lập trình sẵn các quy tắc về văn thư (Nghị định 30). Để khai thác tối đa, hãy ra lệnh rõ ràng theo công thức: **[Hành động] + [File nguồn] + [Định dạng đích]**

**Các câu lệnh mẫu hiệu quả:**
1. *"Hãy đọc file `Bang_doi_chieu.xlsx` trong documents và sinh ra một Quyết định phân công nhân sự ra thư mục OUTPUT."* (AI sẽ tự động ốp chuẩn Nghị định 30 vào file Word).
2. *"Hãy rà soát chéo file `Bao_cao.pdf` dựa trên Bộ Tiêu Chí Rà Soát, tìm cho tôi các lỗi sai logic và tính toán lại bảng biểu."* (Hệ thống sẽ dùng `TIEU_CHI_RA_SOAT.md` để check font chữ, xung đột nội dung, lỗi toán học và chính tả).
3. *"Hãy tổng hợp file PDF Nghị định này thành 5 gạch đầu dòng ngắn gọn."*

---

## 5. 🧹 Quy Trình Bảo Trì Hệ Thống (Mỗi Chiều Thứ Sáu)

Vào mỗi cuối tuần, để giữ máy tính không bị đầy bộ nhớ bởi các file tạm, hãy nhắn cho AI:

💬 **"Hãy chạy quy trình dọn dẹp hệ thống."**

Hệ thống sẽ tự động:
1. Quét tìm các file copy trùng lặp nội dung 100%.
2. Gom các bản nháp (`_v1`, `_v2`) vào thư mục lưu trữ (Archive/Trash) khi đã có bản `_FINAL`.
3. Sắp xếp lại các file bị lưu lạc sai thư mục.
4. Xuất ra một báo cáo tổng kết những gì đã dọn dẹp.

---
*Lưu ý: Tài liệu này là kim chỉ nam cho toàn bộ cán bộ nhân viên. Tuân thủ đúng sẽ giúp tự động hóa 80% công việc thủ công hàng ngày.*
