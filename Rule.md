# Quy tắc cốt lõi (Rules)

## 1. Nguồn dữ liệu (Source of Truth)
- Tất cả dữ liệu phải được lấy trực tiếp từ các tài liệu trong thư mục `documents/`.
- **TUYỆT ĐỐI KHÔNG chế biến, không tự bịa (hallucinate) dữ liệu, hoặc suy diễn ngoài văn bản.**

## 2. Xử lý dữ liệu thiếu
- Nếu thông tin yêu cầu không có trong tài liệu nguồn:
  - Để trống trường thông tin đó trong file kết quả (ví dụ: để khoảng trắng hoặc ghi chú `[Trống]`).
  - **BẮT BUỘC** phải thông báo (la lên) rõ ràng cho người dùng biết dữ liệu nào đang bị thiếu trong khung chat.

## 3. Định dạng Output
- Định dạng xuất văn bản mặc định theo yêu cầu: `.docx`, `.xlsx`, `.pdf`.
- **QUY ĐỊNH BẮT BUỘC ĐỐI VỚI FILE `.DOCX`:** Mọi file output có đuôi `.docx` khi tạo mới hoặc cập nhật **MẶC ĐỊNH BẮT BUỘC 100% PHẢI ĐƯỢC FORMAT THEO QUY CHUẨN NGHỊ ĐỊNH 30/2020/NĐ-CP** (tham chiếu chi tiết tại [QUY_CHUAN_DOCX_ND30.md](file:///Users/admin/Desktop/BINHDUONG/QUY_CHUAN_DOCX_ND30.md)). **Quy tắc này áp dụng tự động trong mọi tác vụ mà không cần người dùng phải nhắc lại trong mỗi yêu cầu.**
- Đối với yêu cầu tạo file để mở trên trình duyệt (HTML):
  - Chỉ sử dụng HTML, CSS và Javascript thuần túy (Vanilla).
  - Tích hợp các CDN nếu cần thiết để biểu diễn dữ liệu trực quan (ví dụ: dùng CDN MermaidJS để vẽ flowchart, KaTeX/MathJax để hiển thị công thức toán học).
  - Trừ khi người dùng có yêu cầu chia file cụ thể, **tất cả mã HTML, CSS và JS (kể cả CDN script) phải được gộp chung vào 1 file `.html` duy nhất** để dễ dàng xem.

## 4. Quản lý File
- Luôn lưu các file kết quả vào thư mục `OUTPUT/`.
- Tuyệt đối không ghi đè hay chỉnh sửa trực tiếp vào file gốc trong thư mục `documents/`.

## 5. Báo cáo Rà soát & Yêu cầu File Đối chiếu (Audit Reporting)
- **Báo cáo những gì đã sửa:** Sau khi thực hiện rà soát (Audit), AI BẮT BUỘC phải tạo một file báo cáo (hoặc tóm tắt trực tiếp trong chat) liệt kê chi tiết các lỗi đã phát hiện và những thông tin cụ thể đã được điều chỉnh.
- **Hỏi lại nếu thiếu File gốc:** Nếu người dùng yêu cầu rà soát chéo hoặc đối chiếu số liệu nhưng lại cung cấp thiếu file nguồn (file đối chiếu), AI **TẠM DỪNG XỬ LÝ VÀ PHẢI HỎI LẠI NGƯỜI DÙNG** để xin thêm file. Tuyệt đối không được im lặng bỏ qua, tự biên dịch hay làm bừa dẫn đến sai lệch dữ liệu.

## 6. Giữ nguyên định dạng tài liệu gốc (Format Preserving)
- Khi xuất kết quả ra các định dạng văn bản (đặc biệt là `.docx`), AI phải tái tạo lại tối đa format của bản PDF gốc kết hợp với quy chuẩn thể thức Nghị định 30.
- Bao gồm: Chiều trang (Landscape/Portrait), phông chữ tiêu chuẩn (Times New Roman), các dòng tiêu đề in đậm, các dòng căn cứ pháp lý in nghiêng, và giữ nguyên cấu trúc/câu từ trong bảng biểu.

## 7. Kiểm tra chéo Toán học & Logic (Mathematical Cross-check)
- AI bắt buộc phải tự động tính toán, cộng dồn lại tất cả các cột tổng, hàng tổng trong các bảng biểu và thuyết minh khi đọc dữ liệu.
- Nếu phát hiện sai sót số học hoặc mâu thuẫn từ bản gốc, tự động điều chỉnh số liệu đúng vào file kết quả cuối cùng (OUTPUT) và thông báo trong khung chat.

## 8. Quy chuẩn trình bày văn bản .docx (Mặc định tuân thủ toàn diện Nghị định 30/2020/NĐ-CP)
> **NGUYÊN TẮC BẤT DI BẤT DỊCH:** Bất cứ khi nào tạo mới hoặc chỉnh sửa file văn bản hành chính (`.docx`), AI **tự động áp dụng toàn bộ quy chuẩn sau đây mà người dùng không cần phải nhắc lại**:
Toàn bộ chi tiết kỹ thuật được quy định tại [QUY_CHUAN_DOCX_ND30.md](file:///Users/admin/Desktop/BINHDUONG/QUY_CHUAN_DOCX_ND30.md):

1. **Khổ giấy & Căn lề chuẩn (Phụ lục I - Mục I):**
   - Khổ giấy A4 ($210\text{ mm} \times 297\text{ mm}$), hướng Portrait (chỉ chuyển sang Landscape khi có bảng biểu rộng).
   - Lề trên và lề dưới: $20 - 25\text{ mm}$ ($2.0 - 2.5\text{ cm}$).
   - Lề trái: $30 - 35\text{ mm}$ ($3.0 - 3.5\text{ cm}$) để đóng tập.
   - Lề phải: $15 - 20\text{ mm}$ ($1.5 - 2.0\text{ cm}$).
2. **Quy chuẩn Font & Đánh số trang:**
   - Phông chữ chuẩn tiếng Việt: **Times New Roman**, bộ mã Unicode TCVN 6909:2001, màu đen.
   - Số trang: Đánh từ số 1 bằng số Ả Rập, cỡ $13 - 14$, đứng, **đặt tại lề trên (Header), canh giữa theo chiều ngang**, và **tuyệt đối không hiển thị ở trang thứ nhất**.
3. **Bố cục 14 ô thành phần thể thức bắt buộc (Phụ lục I - Mục IV & V):**
   - **Quốc hiệu:** In hoa, cỡ $12 - 13$, đứng, đậm. **Tiêu ngữ:** In thường, cỡ $13 - 14$, đứng, đậm. Đường kẻ ngang dưới Tiêu ngữ có độ dài bằng chính xác độ dài dòng chữ.
   - **Tên cơ quan ban hành:** In hoa, cỡ $12 - 13$, đứng, đậm. Kẻ ngang dưới dài $1/3$ đến $1/2$ độ dài dòng chữ.
   - **Số, ký hiệu:** Cỡ $13$, đứng. Số < 10 có số 0 phía trước (ví dụ `Số: 05/...`).
   - **Địa danh & ngày tháng:** Cỡ $13 - 14$, *nghiêng*. Ngày < 10, tháng 1, 2 có số 0 ở trước.
   - **Tên loại & Trích yếu:** In hoa, cỡ $13 - 14$, đứng, đậm (với văn bản có tên loại); với công văn thì trích yếu ghi `V/v ...` cỡ $12 - 13$, đứng.
   - **Nội dung văn bản:** Cỡ $13 - 14$, in thường, đứng, **canh đều 2 lề (Justify)**. Lùi đầu dòng đoạn văn $1 - 1.27\text{ cm}$. Khoảng cách đoạn tối thiểu $6\text{pt}$, giãn dòng từ Single đến $1.5\text{ lines}$.
   - **Căn cứ ban hành:** Cỡ $13 - 14$, *nghiêng*, cuối mỗi căn cứ có chấm phẩy (`;`), dòng cuối chấm (`.`).
   - **Điều, Khoản, Điểm:** "Điều" in thường lùi $1 - 1.27\text{ cm}$, số Ả Rập, đậm. Khoản số Ả Rập kèm dấu chấm. Điểm dùng a), b), c) kèm ngoặc đơn.
   - **Chức vụ, quyền hạn & Họ tên:** Quyền hạn (`TM.`, `KT.`, `TL.`) và Chức vụ in hoa, $13 - 14$, đứng, đậm. Họ tên người ký in thường, $13 - 14$, đứng, đậm, **không ghi học hàm/học vị**.
   - **Nơi nhận:** "Nơi nhận:" cỡ $12$, *nghiêng*, đậm. Danh sách nhận cỡ $11$, đứng, gạch đầu dòng, cuối dòng chấm phẩy (`;`), dòng lưu cuối cùng kết thúc bằng dấu chấm (`.`).
4. **Quy tắc viết hoa chuẩn xác (Phụ lục II):**
   - Tuân thủ quy định viết hoa tên người, tên địa lý (Thủ đô Hà Nội, Thành phố Hồ Chí Minh, đơn vị hành chính), tên cơ quan, tổ chức, danh từ chung riêng hóa (Nhân dân, Nhà nước), và các trường hợp viện dẫn (Khoản, Điều...).
5. **Ký hiệu viết tắt tên loại văn bản (Phụ lục III):**
   - Áp dụng đúng chuẩn viết tắt 27 loại văn bản hành chính (NQ, QĐ, CT, KH, BC, BB, TTr, HĐ...) và bản sao (SY, TrS, SL).

