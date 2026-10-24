# 📋 BẢNG THEO DÕI TIẾN ĐỘ & CẤU TRÚC HỆ THỐNG (TASK TRACKER)
> **Dự án:** Xử lý và Quản trị Văn bản Hành chính - Chi nhánh 23 Bình Dương  
> **Vị trí file:** Nằm ngay tại thư mục gốc dự án: `BINHDUONG/TASK_TRACKER.md`  
> **Cập nhật lần cuối:** 13/10/2026  
> **Giao thức làm việc:** 100% qua Chat Hội thoại tự nhiên (Người dùng không cần gõ Terminal)

---

## 🌳 1. Cấu Trúc Thư Mục Chuẩn Hóa Của Dự Án (Clean Folder Structure)

Toàn bộ hệ thống đã được dọn dẹp sạch sẽ, phân tách rành mạch theo đúng chuẩn 4 thư mục nghiệp vụ + 1 môi trường kỹ thuật:

```text
BINHDUONG/
│
├── documents/                  # 📥 KHO TÀI LIỆU ĐẦU VÀO (CHỈ ĐỌC - READONLY)
│   ├── *.pdf                   # Toàn bộ PDF văn bản & PDF scan đóng dấu đỏ (67 file)
│   ├── *.docx, *.doc           # Các file Word dự thảo, công văn nhận về
│   └── *.xlsx, *.csv           # Bảng tính số liệu kiểm kê, danh mục thiết bị
│
├── OUTPUT/                     # 📤 KHO KẾT QUẢ ĐẦU RA (CHO NGƯỜI DÙNG)
│   ├── *.docx                  # Văn bản hành chính chuẩn 100% Nghị định 30/2020/NĐ-CP
│   ├── *.xlsx                  # Bảng tính số liệu, thống kê tài sản đã xử lý
│   ├── *.html                  # Báo cáo trực quan, Dashboard quản trị, công cụ so sánh
│   ├── evidence_crops/         # Hình ảnh trích xuất minh chứng (bảng biểu, chữ ký...)
│   └── reports_pdf/            # Các báo cáo tiến độ đã xuất bản dạng PDF
│
├── tools/                      # ⚙️ BỘ CÔNG CỤ CỐT LÕI DÙNG CHUNG (CORE ENGINES)
│   ├── nd30_engine.py          # Module sinh Word chuẩn NĐ 30 (Template dùng chung)
│   ├── doc_pipeline.py         # Pipeline tự động quét, trích xuất text & OCR cache
│   ├── ocr_vision              # Công cụ Apple Vision OCR native cực mạnh (Mac)
│   ├── ocr_vision.swift        # Mã nguồn Swift tích hợp Apple PDFKit & Vision
│   └── generate_excel.py       # Tiện ích đọc / ghi file bảng tính
│
├── scratch/                    # 🧠 BỘ NHỚ ĐỆM TẠM THỜI (CACHE & STAGING - Đã chặn Git)
│   ├── cache_texts/            # 67 file .txt đã bóc tách sạch từ documents/
│   ├── documents_index.json    # Bảng chỉ mục MD5 (Cache hit giúp bỏ qua file cũ)
│   ├── legacy_scripts/         # Nơi lưu vết 17 scripts cũ viết riêng cho từng file
│   └── chrome_automation/      # Bộ công cụ crawl web Playwright cũ (đã thu gọn vào đây)
│
├── venv/                       # 🐍 MÔI TRƯỜNG ẢO PYTHON (KỸ THUẬT - Đã chặn Git)
│                               # Chứa python-docx, openpyxl, pypdf, pdfplumber...
│
├── index.html                  # Cổng điều hướng nhanh vào Dashboard OUTPUT/
├── TASK_TRACKER.md             # File này (Bảng theo dõi tiến độ & Cấu trúc dự án)
├── LICH_SU_CONG_VIEC.md        # Nhật ký chi tiết các công việc đã thực hiện
├── QUY_CHUAN_DOCX_ND30.md      # Quy chuẩn kỹ thuật chi tiết theo Nghị định 30/2020/NĐ-CP
├── Cau_truc_Thu_muc.md         # Quy định tổ chức thư mục của dự án
└── Rule.md, Agent.md...        # Bộ khung quy tắc hoạt động của AI
```

---

## 🔍 2. Giải Thích Về Các Thư Mục Đặc Thù

| Thư mục | Bản chất kỹ thuật | Xử lý & Khuyến nghị |
| :--- | :--- | :--- |
| **`__pycache__/`** | Thư mục tự sinh của Python chứa mã bytecode biên dịch (`.pyc`). Không có giá trị lưu trữ. | **Đã xóa sạch hoàn toàn.** Đã cấu hình `.gitignore` chặn vĩnh viễn. |
| **`chrome_automation/`** | Bộ script tự động hóa trình duyệt (Playwright) nghiên cứu website `vpdkddtdm.vn` từ cuối tháng 9. | **Đã di chuyển vào `scratch/chrome_automation/`** để dọn sạch thư mục gốc mà vẫn bảo toàn 100% dữ liệu. |
| **`venv/`** | Thư mục Môi trường ảo Python (Virtual Environment). Chứa các thư viện phụ thuộc (`python-docx`, `openpyxl`, `pypdf`, `pdfplumber`...) để chạy các công cụ. | **BẮT BUỘC GIỮ LẠI.** Đây là nền tảng kỹ thuật để AI chạy các công cụ. Thư mục này đã nằm trong `.gitignore`, không ảnh hưởng tới Git hay người dùng. |
| **`scratch/`** | Phân vùng tạm (Staging/Cache) phục vụ AI xử lý dữ liệu. | Chứa kho text bóc tách siêu tốc (0.05s). Đã nằm trong `.gitignore`. |

---

## 📌 3. Bảng Theo Dõi Tiến Độ Công Việc

| STT | Nhiệm vụ | Trạng thái | Kết quả cụ thể |
| :---: | :--- | :---: | :--- |
| **01** | **Giải thể & Xóa bỏ folder `QQ/`** | ✅ Hoàn thành | Rã 124 file về đúng `OUTPUT/`, `tools/`, `scratch/`. Xóa hoàn toàn thư mục `QQ/`. |
| **02** | **Cập nhật Portal điều hướng (`index.html`)** | ✅ Hoàn thành | Chuyển hướng sang `OUTPUT/index.html`. Xác minh 100% link và ảnh hoạt động. |
| **03** | **Xây dựng NĐ 30 Core Document Engine** | ✅ Hoàn thành | `tools/nd30_engine.py` đóng gói 100% thể thức NĐ 30. Đã test sinh mẫu thành công file `OUTPUT/Mau_van_ban_test_ND30.docx`. |
| **04** | **Nâng cấp Apple Vision OCR Engine** | ✅ Hoàn thành | `tools/ocr_vision` hỗ trợ cả ảnh scan lẫn PDF nhiều trang qua Apple PDFKit. |
| **05** | **Xây dựng Auto Document Pipeline** | ✅ Hoàn thành | `tools/doc_pipeline.py` tự động quét, bóc tách text & ghi nhận MD5. |
| **06** | **Dọn dẹp `tools/`** | ✅ Hoàn thành | Chuyển 17 scripts cũ vào `scratch/legacy_scripts/`. Giữ `tools/` tinh gọn chuẩn mực. |
| **07** | **Đồng bộ 100% kho tài liệu gốc** | ✅ Hoàn thành | Bóc tách toàn bộ **67/67 tài liệu** trong `documents/` sang text thuần tại `scratch/cache_texts/`. |
| **08** | **Dọn sạch gốc dự án (`__pycache__`, `chrome_automation`)** | ✅ Hoàn thành | Xóa `__pycache__`, gom `chrome_automation` vào `scratch/`, đưa `BEST_PRACTICE.html` vào `OUTPUT/`. |
| **09** | **Xuất Task Tracker trực tiếp ra gốc dự án** | ✅ Hoàn thành | Tạo file [TASK_TRACKER.md](file:///Users/admin/Desktop/BINHDUONG/TASK_TRACKER.md) ngay tại thư mục làm việc để người dùng mở trực tiếp. |
| **10** | **Dọn dẹp chuẩn hóa kho `documents/`** | ✅ Hoàn thành | - Xóa sạch 100% file `.md` khỏi `documents/`.<br/>- Chuyển các kết quả hoàn chỉnh (`report_v3.pdf`, `Báo cáo mới v1.xlsx`, `BB bàn giao IT final.docx`) sang `OUTPUT/`.<br/>- Chuyển 13 file nháp version cũ sang `scratch/archive_docs/`.<br/>- Thư mục `documents/` hiện tại chỉ còn đúng 54 tài liệu pháp lý gốc đầu vào sạch sẽ. |

---

## 💬 4. Cách Tương Tác: 100% Qua Chat Tự Nhiên

Người dùng **không cần gõ lệnh Terminal hay quan tâm đến code**. Mọi thao tác đều thực hiện qua lời nói trong Chat:

1. **Khi thêm văn bản mới:** Kéo file vào `documents/` rồi nhắn trong chat: *"Tôi vừa thêm file mới vào doc, bạn cập nhật giúp tôi."*
2. **Khi tìm kiếm số liệu:** Nhắn: *"Tìm giúp tôi trong các văn bản quy định về định mức máy tính."*
3. **Khi soạn văn bản mới:** Nhắn: *"Dựa vào tài liệu X và Y, soạn Tờ trình xin chủ trương đầu tư..."* -> AI tự động xuất file `.docx` chuẩn NĐ 30 vào `OUTPUT/`.
