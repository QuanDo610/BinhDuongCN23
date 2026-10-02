# 🔍 BỘ TIÊU CHÍ RÀ SOÁT VĂN BẢN (AUDIT PARAMETERS)

Đây là bộ khung tham chiếu bắt buộc để hệ thống AI thực hiện nghiệp vụ "Rà soát chéo" (Cross-referencing) và "Kiểm duyệt" văn bản hành chính trước khi xuất xưởng.

Khi có lệnh "Hãy rà soát file...", AI phải quét file dựa trên **4 nhóm tiêu chí** (Parameters) sau:

## 1. Tiêu chí Hình thức & Thể thức (Format Compliance)
Dựa trên tiêu chuẩn Nghị định 30/2020/NĐ-CP:
- **Font & Size:** 100% sử dụng `Times New Roman`. Rà soát gắt gao kích cỡ từng khu vực (Quốc hiệu 12-13 in đậm, Nội dung 13-14, Nơi nhận 11-12). Phát hiện và cảnh báo các font lạ (Arial, Calibri...).
- **Căn lề (Margins & Alignment):** Lùi đầu dòng 1 - 1.27cm. Nội dung chính bắt buộc phải căn đều 2 bên (Justify).
- **Header & Footer:** Đánh số trang nằm ở Header, căn giữa. **Lỗi nghiêm trọng cần báo cáo:** Đánh số trang hiển thị ở trang 1.
- **Bảng biểu (Tables):** Khung Quốc hiệu, Tiêu ngữ, Chữ ký phải dùng bảng ẩn viền (Borderless table), không được gõ space hoặc tab thủ công.

## 2. Tiêu chí Logic Nội dung (Logical Consistency)
- **Xung đột Thông tin Nội bộ (Internal Conflicts):** Rà soát xem các phần trong cùng một văn bản có "đá" nhau không. *(Ví dụ: Phần 1 nêu "Tổng diện tích nhà để xe là 200m2", nhưng Phần 2 lại ghi "Bố trí 250m2 làm nhà để xe")*.
- **Xung đột Liên văn bản (Cross-document Conflicts):** Đối chiếu văn bản phái sinh với Tờ trình/Quyết định gốc. Phát hiện sai lệch về tên người, chức vụ, địa danh, ngày tháng.
- **Tính đầy đủ (Completeness):** Cảnh báo ngay lập tức nếu văn bản còn sót các trường dữ liệu trống dạng `[Nhập số liệu...]`, `...`, hoặc `[Để trống]`.

## 3. Tiêu chí Toán học & Tính toán (Mathematical Accuracy)
- **Tính Tổng (Summation):** AI bắt buộc cộng dồn thủ công tất cả các giá trị thành phần trong bảng biểu và thuyết minh. Báo lỗi ngay nếu kết quả cộng dồn không khớp với ô "Tổng cộng".
- **Tính Thống nhất Đơn vị (Unit Consistency):** Cảnh báo nếu văn bản nhảy loạn đơn vị (ví dụ: đang dùng `m2` tự nhiên nhảy sang `ha`, hoặc nhầm lẫn giữa `đồng` và `nghìn đồng`).
- **Làm tròn số (Rounding):** Kiểm tra dấu phẩy thập phân và dấu chấm hàng nghìn chuẩn Việt Nam (ví dụ: `1.035,30 m2`).

## 4. Tiêu chí Chính tả & Văn phong (Spelling & Tone)
- **Lỗi đánh máy (Typos):** Quét lỗi dính chữ do chuyển đổi PDF sang Word (ví dụ: `Cơquan`, `vănbản`), lỗi thiếu dấu, gõ sai vần tiếng Việt.
- **Khoảng trắng & Dấu câu:** Báo lỗi nếu có dấu cách thừa trước dấu chấm, phẩy (ví dụ: `nhà nước , pháp luật`). Cuối các dòng "Căn cứ..." bắt buộc phải là dấu chấm phẩy `;`.
- **Viết hoa chuẩn (Capitalization NĐ30):** Rà soát quy tắc viết hoa danh từ chung riêng hóa: "Nhà nước", "Nhân dân", viết hoa chữ cái đầu của các từ "Điều", "Khoản", "Điểm" khi viện dẫn, và quy định viết hoa tên Cơ quan ban hành.

## 5. Tiêu chí Pháp lý & Thẩm quyền (Legal & Authority)
- **Kiểm tra Hiệu lực Pháp lý:** Rà soát phần "Căn cứ pháp lý" để phát hiện việc viện dẫn các Luật, Nghị định, Thông tư đã hết hiệu lực (ví dụ: dùng Luật cũ, Nghị định cũ do copy từ form mẫu).
- **Thẩm quyền Chữ ký (Ký thay/Ký thừa lệnh):** Kiểm tra cấu trúc chữ ký. Nếu Cấp phó ký, bắt buộc phải có chữ `KT. TRƯỞNG PHÒNG / GIÁM ĐỐC` ở trên chức danh `PHÓ...`. Nếu cấp dưới ký thừa lệnh thì phải có `TL.`.
- **Thẩm quyền Ban hành:** Cảnh báo nếu loại hình văn bản không phù hợp với cấp Chi nhánh (VD: Chi nhánh ban hành Nghị quyết).

## 6. Tiêu chí Logic Thời gian (Timeline Consistency)
- **Nghịch lý Thời gian:** Rà soát chéo ngày ban hành văn bản so với ngày của các văn bản Căn cứ/Tờ trình đề xuất. (Ngày ban hành Quyết định KHÔNG THỂ nằm trước ngày gửi Tờ trình xin duyệt).
- **Ngày nghỉ/Ngày lễ:** Cảnh báo (Warning) nếu ngày ký ban hành văn bản rơi vào các ngày cuối tuần (Thứ 7, Chủ Nhật) hoặc ngày Lễ chính thức, để người soạn thảo kiểm tra lại xem có hợp lý không.

## 7. Tiêu chí Tính Đồng bộ Phụ lục đính kèm (Attachment Sync)
- **Khớp số lượng & Tên Phụ lục:** Nếu trong nội dung hoặc nơi nhận ghi *"Kèm theo 03 Bảng kê..."* hoặc chỉ đích danh tên Phụ lục, AI phải kiểm tra xem ở phần sau (hoặc file đính kèm) có đúng 03 bảng kê với tên gọi chính xác như vậy không.
- **Tiêu đề Bảng lặp lại (Repeat Header Rows):** Với các Bảng biểu kéo dài qua 2 trang giấy trở lên, AI phải kiểm tra (và tự động cấu hình) việc lặp lại Dòng tiêu đề của bảng ở đầu trang tiếp theo theo đúng chuẩn trình bày.
