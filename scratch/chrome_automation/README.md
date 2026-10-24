# 🌐 Chrome Automation & Web Research Hub

Hệ thống công cụ chuyên biệt để nghiên cứu cấu trúc website và tự động hóa các tác vụ lặp đi lặp lại trên Google Chrome bằng **Playwright** và **Antigravity AI**.

---

## 📁 Cấu Trúc Thư Mục

```text
chrome_automation/
├── README.md               # Hướng dẫn chi tiết & tài liệu sử dụng
├── requirements.txt        # Các thư viện phụ thuộc (Playwright, bs4, httpx,...)
├── analyzer.py             # Script tự động phân tích sâu website (Tech Stack, API, DOM, Forms)
├── sample_workflow.py      # Mẫu kịch bản tự động hóa (Click, Form, Lưu Session/Cookies)
└── reports/                # Thư mục lưu kết quả phân tích (Screenshots, Markdown & JSON)
```

---

## 🎯 1. Khả Năng Của Antigravity Với Chrome & Automation

Antigravity **hoàn toàn có thể** thực hiện các tác vụ bạn yêu cầu:

1. **Nghiên cứu website theo đường link**:
   - Khi bạn gửi một URL, Antigravity có thể điều khiển Chrome vào trang, bóc tách cấu trúc DOM, chụp ảnh màn hình, bắt toàn bộ các lời gọi API Backend ngầm (XHR/Fetch), xác định công nghệ Frontend (React, Vue, Next.js, v.v.).
   - Trả về báo cáo phân tích kiến trúc chi tiết ngay trong khung chat hoặc xuất file markdown.

2. **Tự động hóa các tác vụ lặp đi lặp lại**:
   - Tự động điền biểu mẫu (Form submission), click nút, cuộn trang.
   - Đăng nhập và lưu trạng thái phiên làm việc (`storage_state.json`) để không phải đăng nhập lại.
   - Thu thập dữ liệu theo chu kỳ, tải file PDF/Excel định kỳ.
   - Bạn chỉ cần mô tả: *"Vào trang X, tìm danh sách sản phẩm/đơn hàng, click vào từng trang lấy dữ liệu và lưu vào file Excel"*, Antigravity sẽ tự viết code và chạy trực tiếp cho bạn.

---

## 🤖 2. Model Nào Thích Hợp Nhất Để Làm Việc Này?

| Nhu Cầu | Model Đề Xuất | Lý Do |
| :--- | :--- | :--- |
| **Nghiên Cứu Hệ Thống Phức Tạp, Reverse Engineering** | **Gemini 3 Pro** / Model Reasoning cao | Có khả năng suy luận sâu về kiến trúc hệ thống, phân tích các file JavaScript phức tạp/bị nén (minified), đoán biết cấu trúc Database/API Backend từ các payload mạng. |
| **Chạy Tự Động Hóa Hằng Ngày, Crawling Lặp Lại** | **Gemini 3 Flash / 3.8 Flash** | Tốc độ cực nhanh, phản hồi tức thì, tối ưu tài nguyên, rất chuẩn xác khi viết script định tuyến, bóc tách selector CSS/XPath. |

> 💡 **Khuyên dùng**: 
> - Dùng **Gemini Flash** làm mặc định để thao tác nhanh gọn.
> - Khi gặp một trang web có kiến trúc bảo mật cao, mã hóa luồng API hoặc trang Single Page Application (SPA) phức tạp, hãy chuyển sang **Gemini Pro** để Antigravity phân tích sâu.

---

## 🚀 3. Hướng Dẫn Sử Dụng Nhanh

### Bước 1: Kích hoạt môi trường ảo
```bash
source ../venv/bin/activate
```

### Bước 2: Phân tích và nghiên cứu một website bất kỳ
Chạy lệnh sau (thay URL bằng link bạn muốn):
```bash
python analyzer.py https://example.com
```
*Tùy chọn:* Thêm `--headed` nếu bạn muốn mở cửa sổ Chrome thật để xem trực tiếp quá trình quét:
```bash
python analyzer.py https://example.com --headed
```
Kết quả sẽ được tự động xuất ra thư mục `reports/<tên_miền>_<thời_gian>/`:
- `RESEARCH_REPORT.md`: Báo cáo tóm tắt tech stack, API endpoints, forms.
- `analysis_data.json`: Dữ liệu thô để phân tích sâu.
- `screenshots/fullpage.png`: Ảnh chụp toàn bộ trang web.

### Bước 3: Chạy kịch bản tự động hóa tác vụ
Chạy kịch bản mẫu:
```bash
python sample_workflow.py
```

---

## 💬 4. Các Lệnh / Slash Commands Hữu Ích Trong Antigravity

- **`/browser`**: Sử dụng khi muốn tương tác hoặc duyệt web trực tiếp qua Antigravity.
- **`/schedule`**: Đặt lịch chạy kịch bản tự động lặp lại (ví dụ: mỗi 30 phút vào cào dữ liệu 1 lần).
- **`/goal`**: Giao các tác vụ nghiên cứu chuyên sâu, yêu cầu Antigravity đào sâu cho đến khi tìm ra toàn bộ luồng hoạt động của hệ thống.
