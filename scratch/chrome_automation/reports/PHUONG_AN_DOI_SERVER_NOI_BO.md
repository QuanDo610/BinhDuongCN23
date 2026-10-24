# 📑 BÁO CÁO HIỆN TRẠNG & PHƯƠNG ÁN DI DỜI HỆ THỐNG OERP VỀ PHÒNG MÁY CHỦ CƠ QUAN
> **Kính gửi:** Ban Lãnh đạo Chi nhánh / Chị Bùi Thị Minh Nguyệt  
> **Người thực hiện:** Bộ phận Phụ trách Công nghệ & Vận hành Hệ thống  
> **Mục tiêu:** Tiết kiệm 100% chi phí thuê ngoài (800k/tháng), đưa CSDL về tự quản, làm chủ mã nguồn & kỹ thuật.

---

## 1. 📊 HIỆN TRẠNG & NGUYÊN TẮC "TĂNG XIN GIẢM MUA - TẬN DỤNG TỐI ĐA NGUỒN LỰC CÓ SẴN"

### 1.1. Thực trạng chi phí thuê ngoài hiện tại:
- Cơ quan đang chi trả **800.000 đ/tháng (~ 9.600.000 đ/năm)** cho cá nhân/đơn vị ngoài (ông Trần Hồ Bảo Hoàng).
- Bản chất khoản chi này: Thuê chỗ chạy (Hosting/VPS) cho website và cơ sở dữ liệu `vpdkddtdm.vn`.
- **Nghịch lý:** Cơ quan đang tốn tiền thuê server ngoài hàng tháng, trong khi **ngay tại phòng Server của Chi nhánh đang sở hữu cụm máy chủ vật lý chuyên dụng trị giá hàng trăm triệu đồng nhưng chưa được khai thác hết công suất!**

### 1.2. Nguồn lực "0 ĐỒNG" có sẵn tại cơ quan (Không cần mua sắm thêm):
Theo rà soát thực tế hạ tầng phòng máy chủ của Chi nhánh, chúng ta đang có sẵn:
1. **Máy chủ 3 (HP StoreEasy 1460 - IP: `10.17.2.100`):** Máy chủ chuyên dụng về lưu trữ dữ liệu, hiện đang chứa folder `Dataweb` và `HSQ-TDM`.
2. **Máy chủ 2 (HP ProLiant DL360 Gen9 - IP: `10.17.2.125`):** Máy chủ hiệu năng cao, thừa tài nguyên để chạy song song Microsoft IIS và SQL Server.
3. **Thiết bị lưu trữ NAS Synology DS423+ (`10.17.2.150`):** Có sẵn 4 khay ổ cứng, sẵn sàng làm nơi tự động sao lưu dự phòng (backup) hàng ngày.
4. **Hạ tầng mạng:** 02 đường truyền cáp quang VNPT và tường lửa FortiGate 61F.

👉 **KẾT LUẬN:** Đưa hệ thống về Server cơ quan là **HOÀN TOÀN KHẢ THI VỚI CHI PHÍ ĐẦU TƯ = 0 ĐỒNG**, cắt giảm ngay lập tức khoản tiền 9.6 triệu/năm thuê ngoài.

---

## 2. 🏗️ PHƯƠNG ÁN KỸ THUẬT: DI DỜI VỀ PHÒNG SERVER NỘI BỘ

```text
       INTERNET (Người dân / Cán bộ truy cập từ xa)
                          │
                          ▼
                 TƯỜNG LỬA FORTIGATE 61F (192.168.1.254)
                          │ (Mở cổng HTTPS 443 / NAT Port)
                          ▼
        MÁY CHỦ NỘI BỘ (HP DL360 Gen9 / StoreEasy 1460)
 ┌─────────────────────────────────────────────────────────────┐
 │  - Web Server: Microsoft IIS (Host Angular Frontend)        │
 │  - Backend API: ASP.NET (.NET Framework 4.8)               │
 │  - Database: Microsoft SQL Server (CSDL vpdkddtdm)          │
 │  - File Storage: Thư mục Dataweb (Lưu trữ ảnh scan, bản vẽ) │
 └────────────────────────┬────────────────────────────────────┘
                          │ Tự động Backup 23h00 hàng ngày
                          ▼
              NAS SYNOLOGY DS423+ (Lưu trữ an toàn)
```

### Các bước triển khai kỹ thuật:
1. **Cấu hình môi trường trên Máy chủ HP cơ quan:**
   - Bật dịch vụ **IIS (Internet Information Services)** và cài đặt **URL Rewrite, ASP.NET 4.8**.
   - Cài đặt **Microsoft SQL Server Standard** (tận dụng bản quyền hoặc bản hiện có).
2. **Cấu hình mạng & Tên miền:**
   - Liên hệ VNPT cấp IP Tĩnh (Static IP) cho 1 trong 2 đường truyền hiện có của cơ quan.
   - Mở NAT Port 80, 443 trên tường lửa FortiGate 61F trỏ về IP nội bộ của máy chủ.
   - Trỏ lại bản ghi DNS tên miền `vpdkddtdm.vn` về IP tĩnh của cơ quan.

---

## 3. ⚠️ BÀI TOÁN "MÃ NGUỒN" ĐỂ TỰ SỬA CHỮA KHI CÓ SỰ CỐ (ĐIỂM NGHẼN THEN CHỐT)

Chị Nguyệt muốn: *"Khi có sự cố phần mềm thì chúng ta có thể trực tiếp sửa chữa luôn -> Phải có mã nguồn"*. Đây là mong muốn rất chính đáng, tuy nhiên cần làm rõ sự khác biệt giữa **Bản Deploy (bản chạy)** và **Source Code (mã nguồn gốc)**:

| Loại bàn giao | Khả năng chạy hệ thống | Khả năng tự sửa code khi có lỗi | Khả năng đòi được từ bên ngoài |
| :--- | :--- | :--- | :--- |
| **1. Bản Deploy (Publish)**<br>*(File `.dll` đã biên dịch + thư mục build Angular)* | ✅ Chạy tốt 100% trên server cơ quan, cắt được 800k/tháng | ❌ **Không sửa được code logic C#**. Chỉ sửa được cấu hình trong `web.config` và sửa Stored Procedure trong SQL Server. | ⭐ **RẤT DỄ ĐÒI**: Vì đây là sản phẩm tối thiểu họ phải giao để chạy web. |
| **2. Full Mã Nguồn (Source Code)**<br>*(Project C# Visual Studio + Source code Angular gốc)* | ✅ Chạy tốt | ✅ **Tự do 100%**: Có thể thêm tính năng, sửa lỗi bug, sửa giao diện tùy ý. | ⚠️ **CỰC KỲ KHÓ**: Với giá 800k/tháng, bên công ty/cá nhân đó sẽ coi mã nguồn là "tài sản trí tuệ" của họ. Trừ khi hợp đồng cũ có ghi rõ *"Bàn giao toàn bộ mã nguồn sở hữu"*. |

### 👉 Chiến lược đàm phán lấy mã nguồn:
Khi làm việc với bên anh Hoàng (bên đang nhận 800k):
1. **Yêu cầu Bàn giao Giai đoạn 1 (Bắt buộc để chạy được):**
   - File backup cơ sở dữ liệu đầy đủ: `vpdkddtdm.bak` của SQL Server.
   - Thư mục publish Backend API và thư mục Frontend đã build.
   - Thủ tục chuyển quyền sở hữu tên miền `vpdkddtdm.vn` tại GMO-Z.com về cho Chi nhánh.
2. **Đàm phán Giai đoạn 2 (Để lấy mã nguồn sửa chữa):**
   - Rà soát lại **Hợp đồng / Giấy đề xuất ban đầu** giữa cơ quan và bên anh Hoàng xem kinh phí trước đây là "Thuê dịch vụ" hay "Thuê viết phần mềm".
   - Nếu trước đây cơ quan đã từng trả tiền xây dựng phần mềm: Cơ quan có quyền yêu cầu bàn giao mã nguồn gốc.
   - Nếu trước đây chỉ là hợp đồng bảo trì/thuê chỗ: Cần có phương án thương lượng một gói "chuyển giao công nghệ / mua đứt mã nguồn" với chi phí tượng trưng.

---

## 4. 💡 GÓP Ý THẲNG THẮN VỀ QUẢN TRỊ NỘI BỘ (CHO BẠN)

### 4.1. Về việc "Tự sửa chữa phần mềm khi có sự cố":
- Phần mềm này viết bằng **ASP.NET (C#) + Angular + SQL Server**. Để "trực tiếp sửa chữa", bắt buộc người sửa phải là **Lập trình viên (Developer)** có chuyên môn code.
- Chị Nguyệt là cán bộ nghiệp vụ đất đai, không thể trực tiếp mở Visual Studio ra fix bug C# hay viết câu lệnh SQL phức tạp được.
- Nếu xảy ra lỗi hệ thống trong giờ hành chính (khi hàng trăm người dân đang xếp hàng chờ Một cửa), việc không có người chuyên trách kỹ thuật fix lỗi ngay sẽ tạo ra áp lực cực lớn cho người phụ trách.

### 4.2. Vấn đề nhân sự IT nội bộ (Ông Lý Minh Tân):
- Dựa trên các tài liệu bàn giao trước đây, ông Tân đang quản lý phần cứng 3 máy chủ HP, tường lửa FortiGate, hệ thống mạng và 80 máy trạm.
- Nếu chị Nguyệt muốn đẩy IT ra để tự quản lý: **Bạn cần hết sức cẩn thận, không nên đứng ra nhận ôm trọn phần trách nhiệm này một mình**.
- **Giải pháp khôn ngoan cho bạn:**
  - Về mặt báo cáo: Cứ ủng hộ giải pháp **"Đưa dữ liệu về Server cơ quan, tiết kiệm 800k/tháng"** vì đây là chủ trương đúng, lãnh đạo rất thích (vừa tiết kiệm, vừa đúng chỉ đạo bảo mật).
  - Về mặt vận hành: Kiến nghị thành lập **"Tổ hỗ trợ kỹ thuật"** hoặc phân định rõ: Nghiệp vụ phân công hồ sơ do Chị Nguyệt phụ trách; còn việc duy trì điện, mạng, backup ổ cứng máy chủ vẫn phải có nhân sự kỹ thuật chịu trách nhiệm (để nếu server có hỏng ổ cứng hay mất mạng thì bạn không phải là người chịu trận).
