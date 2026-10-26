import os
import re

with open('OUTPUT/index.html', 'r', encoding='utf-8') as f:
    orig = f.read()

def extract_section_inner(section_id):
    pattern = rf'<section id=\"{section_id}\"[^>]*>(.*?)</section>'
    m = re.search(pattern, orig, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ''

inventory_inner = extract_section_inner('tab-inventory')
network_inner = extract_section_inner('tab-network')
toner_inner = extract_section_inner('tab-toner')
proposal_inner = extract_section_inner('tab-proposal')
risk_inner = extract_section_inner('tab-risk')
markdown_inner = extract_section_inner('tab-markdown')

new_html = '''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bảng Tiến Độ & Quản Trị Hệ Thống IT - Chi Nhánh 23</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Font Awesome CDN -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  
  <!-- KaTeX CSS & JS for LaTeX Math Rendering -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
  
  <!-- Marked.js for Markdown Parsing -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    body {
      font-family: 'Inter', sans-serif;
      background-color: #f8fafc;
      color: #0f172a;
    }
    
    /* Custom Scrollbars */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
    
    /* Markdown body styles */
    .markdown-body {
      color: #334155;
      line-height: 1.75;
      font-size: 0.925rem;
    }
    .markdown-body h1, .markdown-body h2, .markdown-body h3, .markdown-body h4 {
      color: #0f172a;
      font-weight: 700;
      margin-top: 1.5rem;
      margin-bottom: 0.75rem;
    }
    .markdown-body h1 { font-size: 1.6rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; color: #0369a1; }
    .markdown-body h2 { font-size: 1.3rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.4rem; color: #0284c7; }
    .markdown-body h3 { font-size: 1.1rem; color: #0369a1; }
    .markdown-body table {
      width: 100%;
      border-collapse: collapse;
      margin: 1.25rem 0;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .markdown-body th {
      background-color: #f1f5f9;
      color: #0f172a;
      font-weight: 600;
      border: 1px solid #cbd5e1;
      padding: 9px 12px;
      text-align: left;
    }
    .markdown-body td {
      border: 1px solid #e2e8f0;
      padding: 9px 12px;
      text-align: left;
      color: #334155;
    }
    .markdown-body tr:nth-child(even) { background-color: #f8fafc; }
    .markdown-body tr:hover { background-color: #f0f9ff; }
    .markdown-body blockquote {
      border-left: 4px solid #0284c7;
      padding-left: 1rem;
      margin: 1.25rem 0;
      background-color: #f0f9ff;
      border-radius: 0 8px 8px 0;
      padding-top: 0.75rem;
      padding-bottom: 0.75rem;
      color: #0369a1;
    }
    .markdown-body code {
      background-color: #f1f5f9;
      color: #e11d48;
      padding: 0.2rem 0.45rem;
      border-radius: 4px;
      font-size: 0.875em;
      border: 1px solid #e2e8f0;
    }
    .markdown-body pre {
      background-color: #0f172a;
      color: #f8fafc;
      padding: 1rem;
      border-radius: 8px;
      overflow-x: auto;
    }
    .markdown-body pre code {
      background-color: transparent;
      color: inherit;
      border: none;
      padding: 0;
    }

    /* Active Sidebar Link Style */
    .nav-item-active {
      background: linear-gradient(to right, #eff6ff, #f0f9ff);
      color: #0284c7 !important;
      border-left: 4px solid #0284c7;
      font-weight: 700;
    }
  </style>
</head>
<body class="min-h-screen flex antialiased bg-slate-50 text-slate-900">

  <!-- Mobile Sidebar Backdrop Overlay -->
  <div id="sidebar-overlay" onclick="toggleSidebar()" class="fixed inset-0 bg-slate-900/50 backdrop-blur-2xs z-40 hidden lg:hidden transition-opacity"></div>

  <!-- ================= LEFT SIDEBAR NAVIGATION ================= -->
  <aside id="sidebar" class="fixed inset-y-0 left-0 z-50 w-72 bg-white border-r border-slate-200 flex flex-col transition-transform duration-300 transform -translate-x-full lg:translate-x-0 lg:static lg:inset-auto lg:h-screen lg:sticky lg:top-0 shrink-0 shadow-sm">
    
    <!-- Sidebar Brand Header -->
    <div class="p-5 border-b border-slate-100 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-sky-500/25 shrink-0">
          <i class="fa-solid fa-server text-base"></i>
        </div>
        <div class="min-w-0">
          <h1 class="text-sm font-extrabold text-slate-900 tracking-tight leading-tight truncate">CHI NHÁNH SỐ 23</h1>
          <p class="text-[11px] font-semibold text-sky-700 truncate">VP ĐĂNG KÝ ĐẤT ĐAI TP.HCM</p>
        </div>
      </div>
      <!-- Close Button Mobile -->
      <button onclick="toggleSidebar()" class="lg:hidden p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100">
        <i class="fa-solid fa-xmark text-lg"></i>
      </button>
    </div>

    <!-- Quick Status Badge -->
    <div class="px-5 py-3 bg-slate-50/80 border-b border-slate-100 flex items-center justify-between text-xs">
      <span class="inline-flex items-center text-emerald-700 font-semibold">
        <span class="w-2 h-2 mr-2 bg-emerald-500 rounded-full animate-pulse"></span>
        Hệ Thống Trực Tuyến
      </span>
      <span class="text-[11px] text-slate-500 font-medium">Năm 2026</span>
    </div>

    <!-- Sidebar Scrollable Navigation Links -->
    <div class="flex-1 overflow-y-auto p-4 space-y-6">
      
      <!-- Nhóm 1: Quản Trị Thiết Bị & Kiểm Kê -->
      <div>
        <div class="px-3 mb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">
          Điều Hành & Số Liệu Thiết Bị
        </div>
        <div class="space-y-1">
          <button onclick="switchTab('tab-overview')" id="btn-tab-overview" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition nav-item-active">
            <i class="fa-solid fa-chart-pie w-5 text-sky-600 mr-2.5 text-sm"></i>
            <span>Tổng Quan Thiết Bị Đang Dùng</span>
          </button>
          
          <button onclick="switchTab('tab-inventory')" id="btn-tab-inventory" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
            <i class="fa-solid fa-boxes-packing w-5 text-indigo-600 mr-2.5 text-sm"></i>
            <span>Kiểm Kê: Đang Dùng vs Thanh Lý</span>
          </button>
          
          <button onclick="switchTab('tab-network')" id="btn-tab-network" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
            <i class="fa-solid fa-network-wired w-5 text-emerald-600 mr-2.5 text-sm"></i>
            <span>Phòng Server & Mạng IP</span>
          </button>
          
          <button onclick="switchTab('tab-toner')" id="btn-tab-toner" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
            <i class="fa-solid fa-print w-5 text-amber-600 mr-2.5 text-sm"></i>
            <span>Tra Cứu Vật Tư & Mã Mực In</span>
          </button>
        </div>
      </div>

      <!-- Nhóm 2: Văn Bản & Chỉ Đạo Mới (Documents) -->
      <div>
        <div class="px-3 mb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">
          Chỉ Đạo & Quy Định Mới
        </div>
        <div class="space-y-1">
          <button onclick="switchTab('tab-tntt')" id="btn-tab-tntt" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
            <i class="fa-solid fa-award w-5 text-amber-500 mr-2.5 text-sm"></i>
            <span>QĐ 78: Thu Nhập Tăng Thêm</span>
            <span class="ml-auto px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">Mới</span>
          </button>
          
          <button onclick="switchTab('tab-inspection')" id="btn-tab-inspection" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
            <i class="fa-solid fa-scale-balanced w-5 text-rose-600 mr-2.5 text-sm"></i>
            <span>QĐ 9326: Kiểm Tra Công Vụ Sở</span>
            <span class="ml-auto px-1.5 py-0.5 rounded text-[10px] font-bold bg-rose-100 text-rose-800">20/10</span>
          </button>

          <button onclick="switchTab('tab-facility')" id="btn-tab-facility" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
            <i class="fa-solid fa-building-circle-check w-5 text-teal-600 mr-2.5 text-sm"></i>
            <span>Phương Án Trạm Y Tế 3 (NĐ 155)</span>
          </button>
          
          <button onclick="switchTab('tab-proposal')" id="btn-tab-proposal" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
            <i class="fa-solid fa-file-invoice-dollar w-5 text-sky-600 mr-2.5 text-sm"></i>
            <span>Dự Toán Đề Xuất 752 Tr (CV 1342)</span>
          </button>

          <button onclick="switchTab('tab-risk')" id="btn-tab-risk" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
            <i class="fa-solid fa-shield-halved w-5 text-purple-600 mr-2.5 text-sm"></i>
            <span>Quản Trị Rủi Ro & Pháp Lý</span>
          </button>
        </div>
      </div>

      <!-- Nhóm 3: Lịch Sử Sự Kiện -->
      <div>
        <div class="px-3 mb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">
          Lịch Sử & Hồ Sơ Tiến Độ
        </div>
        <div class="space-y-1">
          <button onclick="switchTab('tab-event')" id="btn-tab-event" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
            <i class="fa-solid fa-calendar-check w-5 text-slate-500 mr-2.5 text-sm"></i>
            <span>Sự Kiện & Mốc Thời Gian (Đã qua)</span>
          </button>

          <button onclick="switchTab('tab-markdown')" id="btn-tab-markdown" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
            <i class="fa-solid fa-file-lines w-5 text-slate-500 mr-2.5 text-sm"></i>
            <span>Báo Cáo Markdown Chi Tiết</span>
          </button>
        </div>
      </div>

      <!-- Nhóm 4: Hệ Thống Tiện Ích & Liên Kết -->
      <div>
        <div class="px-3 mb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">
          Tiện Ích & Cổng Dịch Vụ
        </div>
        <div class="space-y-1">
          <a href="../documents/index.html" class="w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-sky-50 hover:text-sky-700 transition">
            <i class="fa-solid fa-folder-open w-5 text-amber-500 mr-2.5 text-sm"></i>
            <span>Kho 58 Tài Liệu Gốc</span>
            <i class="fa-solid fa-arrow-up-right-from-square ml-auto text-[10px] text-slate-400"></i>
          </a>

          <a href="document_viewer.html" class="w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-sky-50 hover:text-sky-700 transition">
            <i class="fa-solid fa-book-open w-5 text-indigo-500 mr-2.5 text-sm"></i>
            <span>Hồ Sơ Gốc Online (Viewer)</span>
          </a>

          <a href="../IT_HELPDESK/index.html" class="w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-sky-50 hover:text-sky-700 transition">
            <i class="fa-solid fa-headset w-5 text-blue-600 mr-2.5 text-sm"></i>
            <span>IT Helpdesk Trực Tuyến</span>
            <i class="fa-solid fa-arrow-up-right-from-square ml-auto text-[10px] text-slate-400"></i>
          </a>

          <a href="../A_THANG/index.html" class="w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-sky-50 hover:text-sky-700 transition">
            <i class="fa-solid fa-calendar-days w-5 text-emerald-600 mr-2.5 text-sm"></i>
            <span>Đăng Ký Lịch Tuần (A_THANG)</span>
          </a>

          <a href="orgchart.html" class="w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-sky-50 hover:text-sky-700 transition">
            <i class="fa-solid fa-sitemap w-5 text-sky-600 mr-2.5 text-sm"></i>
            <span>Sơ Đồ Cơ Cấu Tổ Chức</span>
          </a>

          <a href="print_report.html" target="_blank" class="w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 transition">
            <i class="fa-solid fa-print w-5 text-slate-700 mr-2.5 text-sm"></i>
            <span>Trang In Báo Cáo PDF</span>
          </a>
        </div>
      </div>

    </div>

    <!-- Sidebar Footer -->
    <div class="p-4 border-t border-slate-200 bg-slate-50 text-[11px] text-slate-500 flex items-center justify-between">
      <span>Tổ CNTT - CN23</span>
      <span class="font-mono text-slate-400">v2.5.0</span>
    </div>
  </aside>

  <!-- ================= MAIN CONTENT WRAPPER ================= -->
  <div class="flex-1 flex flex-col min-w-0 min-h-screen">
    
    <!-- Top Bar Header (Breadcrumb, Mobile Toggle, Quick Actions) -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-2xs px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between gap-4">
      <div class="flex items-center space-x-3 min-w-0">
        <!-- Toggle button for mobile -->
        <button onclick="toggleSidebar()" class="lg:hidden p-2 rounded-xl text-slate-600 hover:bg-slate-100 transition">
          <i class="fa-solid fa-bars text-lg"></i>
        </button>
        <div>
          <div class="flex items-center space-x-2 text-xs text-slate-400">
            <span>Chi Nhánh 23</span>
            <span>/</span>
            <span id="breadcrumb-title" class="font-semibold text-sky-700">Tổng Quan Thiết Bị Đang Dùng</span>
          </div>
          <h2 id="topbar-heading" class="text-base sm:text-lg font-bold text-slate-900 tracking-tight leading-tight truncate">
            Bảng Điều Hành & Quản Trị Hệ Thống IT
          </h2>
        </div>
      </div>

      <!-- Quick Action Buttons -->
      <div class="flex items-center space-x-2 shrink-0 text-xs">
        <a href="../documents/index.html" class="hidden sm:inline-flex items-center px-3 py-1.5 rounded-xl font-semibold bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 transition shadow-2xs">
          <i class="fa-solid fa-folder-open mr-1.5 text-amber-600"></i> Kho 58 Văn Bản
        </a>
        <a href="../IT_HELPDESK/index.html" class="hidden md:inline-flex items-center px-3 py-1.5 rounded-xl font-semibold bg-blue-50 hover:bg-blue-100 text-blue-800 border border-blue-200 transition shadow-2xs">
          <i class="fa-solid fa-headset mr-1.5 text-blue-600"></i> IT Helpdesk
        </a>
        <a href="print_report.html" target="_blank" class="inline-flex items-center px-3.5 py-1.5 rounded-xl font-semibold bg-slate-900 hover:bg-slate-800 text-white transition shadow-2xs">
          <i class="fa-solid fa-print mr-1.5"></i> Xuất PDF
        </a>
      </div>
    </header>

    <!-- Main Dynamic Content Area (Full Device Width) -->
    <main class="flex-1 p-4 sm:p-6 lg:p-8 w-full max-w-full overflow-x-hidden">
      
      <!-- ================= 1. TAB OVERVIEW (SỐ LIỆU THIẾT BỊ ĐANG SỬ DỤNG ĐƯỢC) ================= -->
      <section id="tab-overview" class="tab-content block space-y-6">
        
        <!-- Header Section Note -->
        <div class="bg-gradient-to-r from-sky-50 via-indigo-50 to-white border border-sky-200 rounded-2xl p-5 shadow-2xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div class="space-y-1">
            <div class="flex items-center space-x-2">
              <span class="px-2.5 py-0.5 rounded-md text-[11px] font-bold uppercase bg-sky-600 text-white shadow-2xs">Thống Kê Hiện Trạng</span>
              <span class="text-xs font-medium text-slate-500">Cập nhật theo danh mục kiểm kê thực tế năm 2026</span>
            </div>
            <h3 class="text-base sm:text-lg font-extrabold text-slate-900 tracking-tight">
              Tổng Quan Số Lượng Thiết Bị Đang Vận Hành Phục Vụ 85 CBCNV
            </h3>
            <p class="text-xs text-slate-600 leading-relaxed">
              Trích xuất từ <strong>Danh sách máy tính - máy in - máy photo - máy scan đang sử dụng năm 2026</strong> và <strong>Bảng đối chiếu định mức CN23</strong>.
            </p>
          </div>
          
          <div class="flex sm:flex-col items-center sm:items-end justify-between gap-2 shrink-0">
            <span class="text-xs text-slate-500">Tỷ lệ thiết bị hoạt động tốt:</span>
            <span class="text-xl sm:text-2xl font-black text-emerald-600 bg-emerald-50 px-3 py-1 rounded-xl border border-emerald-200">
              61.3% <span class="text-xs font-normal text-slate-500">(130 / 212)</span>
            </span>
          </div>
        </div>

        <!-- 6 Metrics Cards: TẬP TRUNG THIẾT BỊ ĐANG DÙNG ĐƯỢC -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          
          <!-- Card 1: Tổng thiết bị đang dùng -->
          <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between">
            <div class="flex items-center justify-between">
              <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Tổng Thiết Bị Dùng Tốt</span>
              <span class="w-8 h-8 rounded-xl bg-sky-100 text-sky-600 flex items-center justify-center text-sm shadow-2xs"><i class="fa-solid fa-microchip"></i></span>
            </div>
            <div class="mt-3">
              <div class="text-2xl sm:text-3xl font-black text-slate-900">130</div>
              <p class="text-[11px] text-emerald-600 font-semibold mt-1 flex items-center gap-1">
                <i class="fa-solid fa-circle-check"></i> Đang khai thác ổn định
              </p>
            </div>
          </div>

          <!-- Card 2: PC đang dùng -->
          <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between">
            <div class="flex items-center justify-between">
              <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Máy Trạm PC Đang Dùng</span>
              <span class="w-8 h-8 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center text-sm shadow-2xs"><i class="fa-solid fa-desktop"></i></span>
            </div>
            <div class="mt-3">
              <div class="text-2xl sm:text-3xl font-black text-blue-600">75 <span class="text-sm font-normal text-slate-500">PC</span></div>
              <p class="text-[11px] text-slate-500 mt-1">Phục vụ 85 CBCNV (88.2%)</p>
            </div>
          </div>

          <!-- Card 3: Máy chủ Server -->
          <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between">
            <div class="flex items-center justify-between">
              <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Máy Chủ Server</span>
              <span class="w-8 h-8 rounded-xl bg-purple-100 text-purple-600 flex items-center justify-center text-sm shadow-2xs"><i class="fa-solid fa-server"></i></span>
            </div>
            <div class="mt-3">
              <div class="text-2xl sm:text-3xl font-black text-purple-700">03 <span class="text-sm font-normal text-slate-500">Server</span></div>
              <p class="text-[11px] text-purple-600 font-medium mt-1">VBDLIS / OERP / CSDL</p>
            </div>
          </div>

          <!-- Card 4: Máy in đang dùng -->
          <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between">
            <div class="flex items-center justify-between">
              <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Máy In Đang Hoạt Động</span>
              <span class="w-8 h-8 rounded-xl bg-amber-100 text-amber-600 flex items-center justify-center text-sm shadow-2xs"><i class="fa-solid fa-print"></i></span>
            </div>
            <div class="mt-3">
              <div class="text-2xl sm:text-3xl font-black text-amber-700">38 <span class="text-sm font-normal text-slate-500">Máy</span></div>
              <p class="text-[11px] text-slate-500 mt-1">23 A4 + 15 A3 (In GCN/Bản đồ)</p>
            </div>
          </div>

          <!-- Card 5: Máy Scan & Photo -->
          <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between">
            <div class="flex items-center justify-between">
              <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Máy Scan & Photo Dùng Tốt</span>
              <span class="w-8 h-8 rounded-xl bg-teal-100 text-teal-600 flex items-center justify-center text-sm shadow-2xs"><i class="fa-solid fa-copy"></i></span>
            </div>
            <div class="mt-3">
              <div class="text-2xl sm:text-3xl font-black text-teal-700">14 <span class="text-sm font-normal text-slate-500">Máy</span></div>
              <p class="text-[11px] text-slate-500 mt-1">11 Scan (9 A3 + 2 A4) + 3 Photo</p>
            </div>
          </div>

          <!-- Card 6: Chờ thanh lý -->
          <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between">
            <div class="flex items-center justify-between">
              <span class="text-[11px] font-bold uppercase tracking-wider text-rose-500">Thiết Bị Chờ Thanh Lý</span>
              <span class="w-8 h-8 rounded-xl bg-rose-100 text-rose-600 flex items-center justify-center text-sm shadow-2xs"><i class="fa-solid fa-trash-can"></i></span>
            </div>
            <div class="mt-3">
              <div class="text-2xl sm:text-3xl font-black text-rose-600">82 <span class="text-sm font-normal text-slate-500">Máy</span></div>
              <p class="text-[11px] text-rose-500 font-medium mt-1">55 PC, 2 Laptop, 15 In, 7 Photo, 3 Scan</p>
            </div>
          </div>

        </div>

        <!-- Bảng Chi Tiết Thiết Bị Đang Dùng vs Chờ Thanh Lý -->
        <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 class="text-sm sm:text-base font-bold text-slate-900 flex items-center gap-2">
                <i class="fa-solid fa-table-list text-sky-600"></i> Bảng Phân Tích & Đối Chiếu Hiện Trạng Thiết Bị Năm 2026
              </h3>
              <p class="text-xs text-slate-500 mt-0.5">Số liệu đối chiếu giữa danh mục đang hoạt động và danh mục đề nghị thanh lý</p>
            </div>
            <div class="flex items-center gap-2">
              <button onclick="switchTab('tab-inventory')" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-sky-50 hover:bg-sky-100 text-sky-700 transition">
                Xem Sổ Kiểm Kê Chi Tiết <i class="fa-solid fa-arrow-right text-[10px] ml-1"></i>
              </button>
            </div>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-xs text-left border-collapse">
              <thead>
                <tr class="bg-slate-50 text-slate-700 font-bold border-b border-slate-200">
                  <th class="p-3">Loại Thiết Bị</th>
                  <th class="p-3 text-center">Số Lượng Đang Dùng Tốt</th>
                  <th class="p-3 text-center">Số Lượng Chờ Thanh Lý</th>
                  <th class="p-3 text-center">Tổng Cộng Đã Cấp</th>
                  <th class="p-3 text-center">Tỷ Lệ Hoạt Động Tốt</th>
                  <th class="p-3">Tình Trạng & Ghi Chú Đơn Vị</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 font-medium">
                <tr class="hover:bg-slate-50/70 transition">
                  <td class="p-3 flex items-center gap-2 font-bold text-slate-900">
                    <i class="fa-solid fa-desktop text-blue-600 w-4"></i> Máy tính để bàn (PC)
                  </td>
                  <td class="p-3 text-center font-bold text-emerald-700 bg-emerald-50/50">75</td>
                  <td class="p-3 text-center font-bold text-rose-600 bg-rose-50/50">55</td>
                  <td class="p-3 text-center font-bold text-slate-900">130</td>
                  <td class="p-3 text-center">
                    <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-blue-50 text-blue-700">57.7%</span>
                  </td>
                  <td class="p-3 text-slate-600">67 máy đã gán mã H09, nhiều máy cấu hình cũ cần nâng cấp RAM/SSD</td>
                </tr>

                <tr class="hover:bg-slate-50/70 transition">
                  <td class="p-3 flex items-center gap-2 font-bold text-slate-900">
                    <i class="fa-solid fa-laptop text-indigo-600 w-4"></i> Máy tính xách tay (Laptop)
                  </td>
                  <td class="p-3 text-center font-bold text-slate-400">0</td>
                  <td class="p-3 text-center font-bold text-rose-600 bg-rose-50/50">2</td>
                  <td class="p-3 text-center font-bold text-slate-900">2</td>
                  <td class="p-3 text-center">
                    <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-rose-50 text-rose-700">0.0%</span>
                  </td>
                  <td class="p-3 text-slate-600">Đã hư hỏng hoàn toàn, Ban Giám đốc và IT hiện dùng máy bàn</td>
                </tr>

                <tr class="hover:bg-slate-50/70 transition">
                  <td class="p-3 flex items-center gap-2 font-bold text-slate-900">
                    <i class="fa-solid fa-server text-purple-600 w-4"></i> Máy chủ (Server)
                  </td>
                  <td class="p-3 text-center font-bold text-emerald-700 bg-emerald-50/50">3</td>
                  <td class="p-3 text-center font-bold text-slate-400">0</td>
                  <td class="p-3 text-center font-bold text-slate-900">3</td>
                  <td class="p-3 text-center">
                    <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-50 text-emerald-700">100.0%</span>
                  </td>
                  <td class="p-3 text-slate-600">3 máy chủ hoạt động online tại Phòng Server 358 Huỳnh Văn Cù</td>
                </tr>

                <tr class="hover:bg-slate-50/70 transition">
                  <td class="p-3 flex items-center gap-2 font-bold text-slate-900">
                    <i class="fa-solid fa-print text-amber-600 w-4"></i> Máy in văn phòng (Khổ A4)
                  </td>
                  <td class="p-3 text-center font-bold text-emerald-700 bg-emerald-50/50">23</td>
                  <td class="p-3 text-center font-bold text-rose-600 bg-rose-50/50">6</td>
                  <td class="p-3 text-center font-bold text-slate-900">29</td>
                  <td class="p-3 text-center">
                    <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-blue-50 text-blue-700">79.3%</span>
                  </td>
                  <td class="p-3 text-slate-600">Chủ yếu các dòng Canon 2900, HP 1020, Canon 6030 phục vụ văn bản</td>
                </tr>

                <tr class="hover:bg-slate-50/70 transition">
                  <td class="p-3 flex items-center gap-2 font-bold text-slate-900">
                    <i class="fa-solid fa-print text-amber-700 w-4"></i> Máy in chuyên dụng (Khổ A3)
                  </td>
                  <td class="p-3 text-center font-bold text-emerald-700 bg-emerald-50/50">15</td>
                  <td class="p-3 text-center font-bold text-rose-600 bg-rose-50/50">9</td>
                  <td class="p-3 text-center font-bold text-slate-900">24</td>
                  <td class="p-3 text-center">
                    <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-blue-50 text-blue-700">62.5%</span>
                  </td>
                  <td class="p-3 text-slate-600">Chuyên in Giấy chứng nhận quyền sử dụng đất và trích lục bản đồ địa chính</td>
                </tr>

                <tr class="hover:bg-slate-50/70 transition">
                  <td class="p-3 flex items-center gap-2 font-bold text-slate-900">
                    <i class="fa-solid fa-file-invoice text-teal-600 w-4"></i> Máy Scan số hóa (A3 + A4)
                  </td>
                  <td class="p-3 text-center font-bold text-emerald-700 bg-emerald-50/50">11</td>
                  <td class="p-3 text-center font-bold text-rose-600 bg-rose-50/50">3</td>
                  <td class="p-3 text-center font-bold text-slate-900">14</td>
                  <td class="p-3 text-center">
                    <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-50 text-emerald-700">78.6%</span>
                  </td>
                  <td class="p-3 text-slate-600">9 Scan A3 (chuyên quét bản đồ khổ lớn) + 2 Scan A4 (Phòng BĐ có 1 máy scan hư)</td>
                </tr>

                <tr class="hover:bg-slate-50/70 transition">
                  <td class="p-3 flex items-center gap-2 font-bold text-slate-900">
                    <i class="fa-solid fa-copy text-indigo-600 w-4"></i> Máy Photocopy đa năng
                  </td>
                  <td class="p-3 text-center font-bold text-emerald-700 bg-emerald-50/50">3</td>
                  <td class="p-3 text-center font-bold text-rose-600 bg-rose-50/50">7</td>
                  <td class="p-3 text-center font-bold text-slate-900">10</td>
                  <td class="p-3 text-center">
                    <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-rose-50 text-rose-700">30.0%</span>
                  </td>
                  <td class="p-3 text-slate-600">3 máy Ricoh/Toshiba đang chạy, 7 máy cũ hỏng nặng đề nghị thanh lý</td>
                </tr>

                <tr class="bg-slate-100 font-extrabold text-slate-900">
                  <td class="p-3 uppercase">TỔNG CỘNG THIẾT BỊ IT</td>
                  <td class="p-3 text-center text-emerald-700 text-sm">130</td>
                  <td class="p-3 text-center text-rose-600 text-sm">82</td>
                  <td class="p-3 text-center text-sm">212</td>
                  <td class="p-3 text-center text-sky-800 text-sm">61.3%</td>
                  <td class="p-3 text-slate-700">Đơn vị đang tích cực bảo trì và kiến nghị bổ sung máy mới</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Phân Bổ Thiết Bị Theo Phòng Ban & Tổ Chuyên Môn -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
            <h4 class="text-sm font-bold text-slate-900 flex items-center gap-2">
              <i class="fa-solid fa-chart-column text-sky-600"></i> Phân Bổ Máy Tính Theo Khối Chuyên Môn (85 Nhân Sự)
            </h4>
            <div class="space-y-3 text-xs">
              <div>
                <div class="flex justify-between font-semibold mb-1 text-slate-700">
                  <span>Tổ Đăng ký và Cấp GCN (32 nhân sự)</span>
                  <span class="text-sky-700 font-bold">28 PC (87.5%)</span>
                </div>
                <div class="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                  <div class="bg-sky-600 h-2.5 rounded-full" style="width: 87.5%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between font-semibold mb-1 text-slate-700">
                  <span>Tổ Kỹ thuật Địa chính & Lưu trữ (29 nhân sự)</span>
                  <span class="text-indigo-700 font-bold">26 PC (89.6%)</span>
                </div>
                <div class="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                  <div class="bg-indigo-600 h-2.5 rounded-full" style="width: 89.6%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between font-semibold mb-1 text-slate-700">
                  <span>Tổ Hành chính Tổng hợp & Kế toán (18 nhân sự)</span>
                  <span class="text-emerald-700 font-bold">16 PC (88.8%)</span>
                </div>
                <div class="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                  <div class="bg-emerald-600 h-2.5 rounded-full" style="width: 88.8%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between font-semibold mb-1 text-slate-700">
                  <span>Ban Giám Đốc & Phụ trách IT (6 nhân sự)</span>
                  <span class="text-purple-700 font-bold">5 PC + 3 Server (100%)</span>
                </div>
                <div class="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                  <div class="bg-purple-600 h-2.5 rounded-full" style="width: 100%"></div>
                </div>
              </div>
            </div>
            
            <p class="text-[11px] text-slate-500 pt-2 border-t border-slate-100 italic">
              * Ghi chú: Định mức theo NĐ 155/2025/NĐ-CP yêu cầu 100% cán bộ, viên chức làm việc chuyên môn phải được trang bị tối thiểu 01 máy vi tính để bàn cấu hình chuẩn.
            </p>
          </div>

          <!-- Thông Tin Pháp Nhân & Địa Điểm Công Tác -->
          <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
            <h4 class="text-sm font-bold text-slate-900 flex items-center gap-2">
              <i class="fa-solid fa-landmark text-indigo-600"></i> Pháp Nhân & Trụ Sở Đơn Vị (Chi Nhánh Số 23)
            </h4>
            <div class="space-y-2.5 text-xs">
              <div class="flex justify-between py-1.5 border-b border-slate-100">
                <span class="text-slate-500">Cơ quan chủ quản cấp trên:</span>
                <span class="font-bold text-slate-900">Văn phòng Đăng ký đất đai TP.HCM (Sở NN & MT)</span>
              </div>
              <div class="flex justify-between py-1.5 border-b border-slate-100">
                <span class="text-slate-500">Trụ sở cơ sở hiện hữu:</span>
                <span class="font-semibold text-slate-900">Số 358 Huỳnh Văn Cù, P. Thủ Dầu Một</span>
              </div>
              <div class="flex justify-between py-1.5 border-b border-slate-100">
                <span class="text-slate-500">Khuôn viên đất hiện trạng:</span>
                <span class="font-semibold text-slate-800">1.417,70 m² (Sàn xây dựng: 835,30 m²)</span>
              </div>
              <div class="flex justify-between py-1.5 border-b border-slate-100">
                <span class="text-slate-500">Địa điểm đề nghị tiếp nhận:</span>
                <span class="font-bold text-sky-700 bg-sky-50 px-2 py-0.5 rounded">Trạm Y tế số 3 (Liền kề số 358)</span>
              </div>
              <div class="flex justify-between py-1.5 border-b border-slate-100">
                <span class="text-slate-500">Quy mô tiếp nhận đề xuất:</span>
                <span class="font-semibold text-slate-800">1.276,20 m² đất (Sàn xây dựng 548 m²)</span>
              </div>
              <div class="flex justify-between py-1.5">
                <span class="text-slate-500">Mục đích sử dụng chính:</span>
                <span class="font-bold text-emerald-700">Kho lưu trữ chuyên dùng (500m²) & Xử lý số hóa</span>
              </div>
            </div>

            <div class="pt-2 flex items-center justify-between">
              <span class="text-[11px] text-slate-400">Căn cứ NĐ 155/2025 & TT 09/2007</span>
              <button onclick="switchTab('tab-facility')" class="text-xs font-semibold text-sky-700 hover:text-sky-900 hover:underline flex items-center gap-1">
                Xem Phương án cơ sở vật chất <i class="fa-solid fa-chevron-right text-[10px]"></i>
              </button>
            </div>
          </div>

        </div>

      </section>

      <!-- ================= 2. TAB INVENTORY (KIỂM KÊ CHI TIẾT) ================= -->
      <section id="tab-inventory" class="tab-content hidden space-y-6">
''' + inventory_inner + '''
      </section>

      <!-- ================= 3. TAB TNTT (QUY ĐỊNH 78/2026/QĐ-UBND - MỚI TỪ DOCUMENTS) ================= -->
      <section id="tab-tntt" class="tab-content hidden space-y-6">
        <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-5">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 gap-3">
            <div>
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-md text-[11px] font-bold uppercase bg-amber-500 text-white shadow-2xs">Văn Bản Pháp Lý Mới</span>
                <span class="text-xs text-slate-500">Ban hành theo Quyết định số 78/2026/QĐ-UBND của UBND TP.HCM</span>
              </div>
              <h3 class="text-base sm:text-lg font-bold text-slate-900 mt-1 flex items-center gap-2">
                <i class="fa-solid fa-award text-amber-500"></i> Quy Định Xếp Loại Thi Đua & Chi Thu Nhập Tăng Thêm (NQ 98)
              </h3>
            </div>
            <a href="../documents/78_Quydinh_xeploaivachiTNTT__kemQD_signed%20(1).pdf" target="_blank" class="px-3.5 py-2 rounded-xl text-xs font-semibold bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 transition inline-flex items-center gap-1.5 shrink-0 shadow-2xs">
              <i class="fa-solid fa-file-pdf text-amber-600"></i> Tải PDF Gốc (7 Trang)
            </a>
          </div>

          <!-- Policy Summary Grid -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            
            <div class="p-4 rounded-xl bg-amber-50/60 border border-amber-200">
              <div class="text-[11px] font-bold uppercase text-amber-800">Mức 1: Xuất Sắc</div>
              <div class="text-lg font-extrabold text-amber-900 mt-1">Từ 90 - 100 Điểm</div>
              <p class="text-xs text-slate-600 mt-1.5 leading-relaxed">
                Tỷ lệ không quá <strong>20%</strong> số người hoàn thành tốt; tỷ lệ trễ hạn hồ sơ đất đai <strong>&lt; 1%</strong>. Hưởng <strong>100% hệ số chi tối đa</strong>.
              </p>
            </div>

            <div class="p-4 rounded-xl bg-blue-50/60 border border-blue-200">
              <div class="text-[11px] font-bold uppercase text-blue-800">Mức 2: Hoàn Thành Tốt</div>
              <div class="text-lg font-extrabold text-blue-900 mt-1">Từ 75 - Dưới 90 Điểm</div>
              <p class="text-xs text-slate-600 mt-1.5 leading-relaxed">
                Hoàn thành tốt mọi nhiệm vụ được giao; trễ hạn không quá <strong>3%</strong>. Hưởng <strong>80% mức chi xuất sắc</strong>.
              </p>
            </div>

            <div class="p-4 rounded-xl bg-slate-50 border border-slate-200">
              <div class="text-[11px] font-bold uppercase text-slate-700">Mức 3: Hoàn Thành</div>
              <div class="text-lg font-extrabold text-slate-800 mt-1">Từ 50 - Dưới 75 Điểm</div>
              <p class="text-xs text-slate-600 mt-1.5 leading-relaxed">
                Có tiến độ đạt yêu cầu, còn thiếu sót nhưng khắc phục kịp thời. Hưởng <strong>60% mức chi xuất sắc</strong>.
              </p>
            </div>

            <div class="p-4 rounded-xl bg-rose-50/60 border border-rose-200">
              <div class="text-[11px] font-bold uppercase text-rose-800">Mức 4: Không Đạt</div>
              <div class="text-lg font-extrabold text-rose-900 mt-1">Dưới 50 Điểm</div>
              <p class="text-xs text-slate-600 mt-1.5 leading-relaxed">
                Vi phạm kỷ luật hoặc để hồ sơ trễ hạn nghiêm trọng không có lý do chính đáng. <strong>Không được chi TNTT</strong>.
              </p>
            </div>

          </div>

          <!-- Detail Guidelines -->
          <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 space-y-3 leading-relaxed">
            <h4 class="font-bold text-slate-900 text-sm flex items-center gap-2">
              <i class="fa-solid fa-list-check text-sky-600"></i> Quy Trình Đánh Giá Xếp Loại Hằng Tháng & Theo Quý
            </h4>
            <ul class="list-disc pl-5 space-y-1.5">
              <li><strong>Hằng tháng:</strong> Từng cá nhân tự chấm điểm theo biểu mẫu KPI (áp dụng song song với Bảng KPI Công việc 9999). Tổ trưởng họp đánh giá và thống nhất xếp loại từng thành viên.</li>
              <li><strong>Cuối Quý:</strong> Điểm trung bình cộng 3 tháng là căn cứ quy đổi mức xếp loại quý. Trường hợp Quý IV thực hiện đánh giá cuối năm thì lấy kết quả đánh giá cuối năm quy đổi làm căn cứ chi Quý IV.</li>
              <li><strong>Người mới vào làm / Hợp đồng lao động:</strong> Có thời gian công tác từ đủ 01 tháng trở lên trong quý được đánh giá và chi thu nhập tăng thêm theo tỷ lệ thời gian làm việc thực tế.</li>
              <li><strong>Tác động đối với IT Chi nhánh 23:</strong> Đảm bảo hệ thống mạng ổn định, không để xảy ra gián đoạn truyền tải dữ liệu VBDLIS khiến hồ sơ một cửa bị trễ hạn trên cổng Dịch vụ công TP.HCM.</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- ================= 4. TAB INSPECTION (QĐ 9326/QĐ-SNNMT-VP - MỚI TỪ DOCUMENTS) ================= -->
      <section id="tab-inspection" class="tab-content hidden space-y-6">
        <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-5">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 gap-3">
            <div>
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-md text-[11px] font-bold uppercase bg-rose-600 text-white shadow-2xs">Ký Ngày 20/10/2026</span>
                <span class="text-xs text-slate-500">Quyết định của Giám đốc Sở Nông nghiệp và Môi trường TP.HCM</span>
              </div>
              <h3 class="text-base sm:text-lg font-bold text-slate-900 mt-1 flex items-center gap-2">
                <i class="fa-solid fa-scale-balanced text-rose-600"></i> Quyết Định 9326/QĐ-SNNMT-VP Về Thành Lập Đoàn Kiểm Tra Công Vụ
              </h3>
            </div>
            <a href="../documents/9326-Q_signed.pdf" target="_blank" class="px-3.5 py-2 rounded-xl text-xs font-semibold bg-rose-50 hover:bg-rose-100 text-rose-800 border border-rose-200 transition inline-flex items-center gap-1.5 shrink-0 shadow-2xs">
              <i class="fa-solid fa-file-pdf text-rose-600"></i> Xem Quyết Định Gốc (3 Trang)
            </a>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
            
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-3">
              <h4 class="font-bold text-slate-900 text-sm flex items-center gap-2">
                <i class="fa-solid fa-users-gear text-sky-600"></i> Thành Phần Đoàn Kiểm Tra Của Sở
              </h4>
              <ul class="space-y-2 text-slate-700">
                <li class="flex items-start gap-2">
                  <span class="font-bold text-sky-800 min-w-28">Trưởng đoàn:</span>
                  <span><strong>Ông Nguyễn Minh Chánh</strong> - Phó Giám đốc Sở Nông nghiệp và Môi trường</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="font-bold text-sky-800 min-w-28">Phó Trưởng đoàn:</span>
                  <span><strong>Ông Thái Bỉnh Nghĩa</strong> - Trưởng phòng Kiểm tra & Giải quyết khiếu nại, tố cáo</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="font-bold text-sky-800 min-w-28">Phó Trưởng đoàn:</span>
                  <span><strong>Bà Trần Thị Hòa</strong> - Chánh Văn phòng Sở Nông nghiệp và Môi trường</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="font-bold text-sky-800 min-w-28">Phó Trưởng đoàn:</span>
                  <span><strong>Ông Nguyễn Xuân Đức</strong> - Phó Trưởng phòng Kiểm tra & GQ khiếu nại, tố cáo</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="font-bold text-sky-800 min-w-28">Phó Trưởng đoàn:</span>
                  <span><strong>Bà Nguyễn Thị Hồng Tâm</strong> - Phó Chánh Văn phòng Sở</span>
                </li>
              </ul>
            </div>

            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-3">
              <h4 class="font-bold text-slate-900 text-sm flex items-center gap-2">
                <i class="fa-solid fa-magnifying-glass-chart text-amber-600"></i> 6 Nội Dung Kiểm Tra Trọng Điểm Tại Chi Nhánh
              </h4>
              <ol class="list-decimal pl-5 space-y-1.5 text-slate-700 leading-relaxed">
                <li>Việc chấp hành kỷ luật, kỷ cương hành chính và văn hóa công sở của viên chức, người lao động.</li>
                <li>Thực hiện quy chế làm việc, quy chế tiếp công dân, đeo thẻ nhân sự trong giờ làm việc.</li>
                <li>Tình hình tiếp nhận, giải quyết và trả kết quả thủ tục hành chính đất đai đúng hẹn.</li>
                <li>Việc thực hiện các quy định về tiếp dân, giải quyết đơn thư khiếu nại, tố cáo.</li>
                <li>Thực hiện pháp luật về cán bộ, công chức, viên chức và hợp đồng lao động.</li>
                <li>Kiểm tra đột xuất các nội dung khác theo chỉ đạo của Giám đốc Sở.</li>
              </ol>
            </div>

          </div>

          <div class="p-4 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-900 flex items-start gap-3">
            <i class="fa-solid fa-triangle-exclamation text-amber-600 text-base mt-0.5"></i>
            <div>
              <strong>Khuyến nghị hành động đối với Chi nhánh 23:</strong> Đảm bảo 100% cán bộ đeo thẻ công chức/viên chức, duy trì hệ thống máy tính tiếp dân tại bộ phận Một cửa hoạt động thông suốt, sổ nhật ký trực tiếp dân và bảng niêm yết thủ tục hành chính được cập nhật chuẩn xác.
            </div>
          </div>
        </div>
      </section>

      <!-- ================= 5. TAB FACILITY (PHƯƠNG ÁN CƠ SỞ VẬT CHẤT & TRẠM Y TẾ 3) ================= -->
      <section id="tab-facility" class="tab-content hidden space-y-6">
        <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-5">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 gap-3">
            <div>
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-md text-[11px] font-bold uppercase bg-teal-600 text-white shadow-2xs">Nghị định 155/2025/NĐ-CP</span>
                <span class="text-xs text-slate-500">Bảng đối chiếu định mức & Phương án xử lý tài sản công</span>
              </div>
              <h3 class="text-base sm:text-lg font-bold text-slate-900 mt-1 flex items-center gap-2">
                <i class="fa-solid fa-building-circle-check text-teal-600"></i> Phương Án Tiếp Nhận Trạm Y Tế Số 3 (Mở Rộng Trụ Sở 358 Huỳnh Văn Cù)
              </h3>
            </div>
            <a href="../documents/B%E1%BA%A3ng%20%C4%91%E1%BB%91i%20chi%E1%BA%BFu%20%C4%91%E1%BB%8Bnh%20m%E1%BB%A9c%20CN23.docx" download class="px-3.5 py-2 rounded-xl text-xs font-semibold bg-teal-50 hover:bg-teal-100 text-teal-800 border border-teal-200 transition inline-flex items-center gap-1.5 shrink-0 shadow-2xs">
              <i class="fa-solid fa-file-word text-teal-600"></i> Tải Bảng Đối Chiếu DOCX
            </a>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-2">
              <div class="font-bold text-slate-500 uppercase text-[10px]">Cơ Sở Hiện Hữu</div>
              <div class="text-base font-extrabold text-slate-900">358 Huỳnh Văn Cù</div>
              <div class="text-slate-600 pt-2 border-t border-slate-200 space-y-1">
                <div>- Đất hiện trạng: <strong>1.417,70 m²</strong></div>
                <div>- Diện tích sàn xây dựng: <strong>835,30 m²</strong></div>
                <div>- Phục vụ: <strong>85 CBCNV</strong></div>
                <div>- Cấp nhà: Cấp III, kết cấu khung bê tông cốt thép</div>
              </div>
            </div>

            <div class="p-5 rounded-xl bg-teal-50/60 border border-teal-200 text-xs space-y-2">
              <div class="font-bold text-teal-700 uppercase text-[10px]">Đề Nghị Tiếp Nhận</div>
              <div class="text-base font-extrabold text-teal-900">Trạm Y Tế Số 3 (Liền Kề)</div>
              <div class="text-slate-700 pt-2 border-t border-teal-200 space-y-1">
                <div>- Khuôn viên đất: <strong>1.276,20 m²</strong></div>
                <div>- Diện tích sàn: <strong>548,00 m²</strong></div>
                <div>- Vị trí: Giáp ranh trụ sở 358 Huỳnh Văn Cù</div>
                <div>- Đang để trống sau sắp xếp địa giới hành chính</div>
              </div>
            </div>

            <div class="p-5 rounded-xl bg-blue-50/60 border border-blue-200 text-xs space-y-2">
              <div class="font-bold text-blue-700 uppercase text-[10px]">Nhu Cầu Định Mức NĐ 155</div>
              <div class="text-base font-extrabold text-blue-900">Chuẩn 85 Người Làm Việc</div>
              <div class="text-slate-700 pt-2 border-t border-blue-200 space-y-1">
                <div>- Khuôn viên đất cần thiết: <strong>4.127,20 m²</strong></div>
                <div>- Sàn làm việc cần thiết: <strong>2.851,00 m²</strong></div>
                <div>- Kho bảo quản tài liệu (TT 09): <strong>500,00 m²</strong></div>
                <div>- Khu xử lý nghiệp vụ lưu trữ: <strong>250,00 m²</strong></div>
              </div>
            </div>
          </div>

          <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 space-y-3 leading-relaxed">
            <h4 class="font-bold text-slate-900 text-sm flex items-center gap-2">
              <i class="fa-solid fa-circle-info text-sky-600"></i> Ý Nghĩa Cấp Thiết Của Phương Án Điều Chuyển Trạm Y Tế 3
            </h4>
            <p>
              Hiện tại, diện tích sàn kho lưu trữ của Chi nhánh 23 chỉ có <strong>171,2 m²</strong>, trong khi đơn vị đang lưu trữ hơn <strong>2.500 mét giá tài liệu</strong> hồ sơ đăng ký quyền sử dụng đất. Theo Thông tư 09/2007/TT-BNV, kho lưu trữ Loại 4 bảo quản từ 1 - 3 km giá tài liệu phải có diện tích tối thiểu <strong>500 m²</strong>.
            </p>
            <p>
              Việc tiếp nhận Trạm y tế số 3 liền kề sẽ giúp Chi nhánh 23 bổ sung thêm <strong>548 m² sàn xây dựng</strong> để bố trí kho tài liệu chuyên dụng chống cháy, chống ẩm mốc và phòng số hóa hồ sơ địa chính hiện đại.
            </p>
          </div>
        </div>
      </section>

      <!-- ================= 6. TAB NETWORK (MẠNG & SERVER) ================= -->
      <section id="tab-network" class="tab-content hidden space-y-6">
''' + network_inner + '''
      </section>

      <!-- ================= 7. TAB TONER (MÃ MỰC IN) ================= -->
      <section id="tab-toner" class="tab-content hidden space-y-6">
''' + toner_inner + '''
      </section>

      <!-- ================= 8. TAB PROPOSAL (DỰ TOÁN 752 TRIỆU - CV 1342) ================= -->
      <section id="tab-proposal" class="tab-content hidden space-y-6">
''' + proposal_inner + '''
      </section>

      <!-- ================= 9. TAB RISK (QUẢN TRỊ RỦI RO & PHÁP LÝ) ================= -->
      <section id="tab-risk" class="tab-content hidden space-y-6">
''' + risk_inner + '''
      </section>

      <!-- ================= 10. TAB EVENT (SỰ KIỆN & LỊCH SỬ ĐÃ QUA THEO MỐC THỜI GIAN) ================= -->
      <section id="tab-event" class="tab-content hidden space-y-6">
        <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-6">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 gap-3">
            <div>
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-md text-[11px] font-bold uppercase bg-slate-200 text-slate-800 shadow-2xs">Kho Lưu Trữ Lịch Sử</span>
                <span class="text-xs text-slate-500">Các mốc sự kiện quan trọng trong quá trình vận hành đã hoàn thành</span>
              </div>
              <h3 class="text-base sm:text-lg font-bold text-slate-900 mt-1 flex items-center gap-2">
                <i class="fa-solid fa-clock-rotate-left text-slate-600"></i> Tiến Trình Sự Kiện & Biên Bản Bàn Giao (Tháng 09 - 10/2026)
              </h3>
            </div>
            <span class="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-300 self-start sm:self-auto">
              Trạng thái: Đã hoàn tất các mốc
            </span>
          </div>

          <!-- Timeline Steps -->
          <div class="relative border-l-2 border-sky-200 ml-4 pl-6 space-y-8">
            
            <!-- Mốc 1: 03/09/2026 -->
            <div class="relative">
              <span class="absolute -left-[31px] top-1 w-4 h-4 rounded-full bg-sky-600 border-4 border-white shadow-2xs"></span>
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-sky-800 bg-sky-100 px-2.5 py-0.5 rounded-md">03/09/2026</span>
                <span class="text-xs text-emerald-700 font-semibold">[Đã hoàn thành]</span>
              </div>
              <h4 class="text-sm font-bold text-slate-900 mt-1.5">Bắt Đầu Tiếp Nhận Nhiệm Vụ Quản Trị Hệ Thống IT</h4>
              <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                Chi nhánh số 23 tiếp nhận nhân sự kỹ sư phần mềm phụ trách công tác quản trị mạng, máy chủ và hỗ trợ kỹ thuật theo hợp đồng làm việc chuyên môn tại trụ sở 358 Huỳnh Văn Cù.
              </p>
            </div>

            <!-- Mốc 2: 10/09/2026 -->
            <div class="relative">
              <span class="absolute -left-[31px] top-1 w-4 h-4 rounded-full bg-sky-600 border-4 border-white shadow-2xs"></span>
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-sky-800 bg-sky-100 px-2.5 py-0.5 rounded-md">10/09/2026</span>
                <span class="text-xs text-emerald-700 font-semibold">[Đã hoàn thành]</span>
              </div>
              <h4 class="text-sm font-bold text-slate-900 mt-1.5">Nhận Thư Mời Làm Việc Bàn Giao IT Từ Lãnh Đạo Chi Nhánh</h4>
              <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                Phó Giám đốc Nguyễn Thị Lệ Hằng ký Thư mời chuyên gia Phùng Vương Quốc (Văn phòng Đăng ký đất đai TP.HCM Cơ sở 2) xuống phối hợp khảo sát mạng và bàn giao kỹ thuật.
              </p>
            </div>

            <!-- Mốc 3: 16/09/2026 -->
            <div class="relative">
              <span class="absolute -left-[31px] top-1 w-4 h-4 rounded-full bg-emerald-600 border-4 border-white shadow-2xs"></span>
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-emerald-800 bg-emerald-100 px-2.5 py-0.5 rounded-md">16/09/2026</span>
                <span class="text-xs text-emerald-700 font-semibold">[Cột mốc then chốt - Đã hoàn thành]</span>
              </div>
              <h4 class="text-sm font-bold text-slate-900 mt-1.5">Đón Tiếp Chuyên Gia Phùng Vương Quốc & Bàn Giao Trực Tiếp</h4>
              <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                Lúc 08h30 sáng, đơn vị đã đón tiếp chuyên gia khảo sát toàn bộ Phòng Server, hệ thống đường truyền Internet chuyên dùng, máy chủ VBDLIS và hoàn tất lập Biên bản bàn giao công tác IT giữa nhân sự cũ (Lý Minh Tân) và nhân sự mới.
              </p>
            </div>

            <!-- Mốc 4: 01/10/2026 -->
            <div class="relative">
              <span class="absolute -left-[31px] top-1 w-4 h-4 rounded-full bg-indigo-600 border-4 border-white shadow-2xs"></span>
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-indigo-800 bg-indigo-100 px-2.5 py-0.5 rounded-md">01/10/2026</span>
                <span class="text-xs text-emerald-700 font-semibold">[Đã hoàn thành]</span>
              </div>
              <h4 class="text-sm font-bold text-slate-900 mt-1.5">Ban Giám Đốc Phê Duyệt Phương Án Cơ Sở Vật Chất & Định Mức CN23</h4>
              <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                Phó Giám đốc Đặng Huy Cường ký Bảng đối chiếu định mức CN23 theo Nghị định 155/2025/NĐ-CP, chính thức đề xuất tiếp nhận Trạm y tế số 3 làm kho lưu trữ hồ sơ địa chính.
              </p>
            </div>

            <!-- Mốc 5: 13/10/2026 -->
            <div class="relative">
              <span class="absolute -left-[31px] top-1 w-4 h-4 rounded-full bg-purple-600 border-4 border-white shadow-2xs"></span>
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-purple-800 bg-purple-100 px-2.5 py-0.5 rounded-md">13/10/2026</span>
                <span class="text-xs text-emerald-700 font-semibold">[Đã hoàn thành]</span>
              </div>
              <h4 class="text-sm font-bold text-slate-900 mt-1.5">Rà Soát Quy Chế 355 & Báo Cáo PCCC Trụ Sở</h4>
              <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                Hoàn thành rà soát thủ tục chứng từ thanh toán kế toán theo QĐ 355/QĐ-VPĐK và Báo cáo an toàn Phòng cháy chữa cháy năm 2026 cho toàn bộ khuôn viên số 358 Huỳnh Văn Cù.
              </p>
            </div>

            <!-- Mốc 6: 20/10/2026 -->
            <div class="relative">
              <span class="absolute -left-[31px] top-1 w-4 h-4 rounded-full bg-rose-600 border-4 border-white shadow-2xs"></span>
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-rose-800 bg-rose-100 px-2.5 py-0.5 rounded-md">20/10/2026</span>
                <span class="text-xs text-rose-700 font-semibold">[Đang triển khai sẵn sàng]</span>
              </div>
              <h4 class="text-sm font-bold text-slate-900 mt-1.5">Sở Nông Nghiệp & Môi Trường Ban Hành Quyết Định 9326</h4>
              <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                Sở thành lập Đoàn kiểm tra công vụ do PGĐ Sở Nguyễn Minh Chánh làm Trưởng đoàn. Chi nhánh chuẩn bị chu đáo điều kiện cơ sở vật chất, hệ thống một cửa và quy chế công vụ để tiếp đón đoàn kiểm tra.
              </p>
            </div>

          </div>
        </div>
      </section>

      <!-- ================= 11. TAB MARKDOWN (BÁO CÁO TOÀN VĂN) ================= -->
      <section id="tab-markdown" class="tab-content hidden space-y-6">
''' + markdown_inner + '''
      </section>

    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-4 px-6 text-center text-xs text-slate-400 mt-auto">
      Hệ Thống Quản Trị Dữ Liệu IT & Điều Hành Tác Vụ - Chi Nhánh Số 23 (VPĐKĐĐ TP.HCM)
    </footer>

  </div>

  <!-- ================= JAVASCRIPT LOGIC ================= -->
  <script>
    const tabTitles = {
      'tab-overview': { breadcrumb: 'Tổng Quan Thiết Bị Đang Dùng', heading: 'Bảng Điều Hành & Quản Trị Hệ Thống IT' },
      'tab-inventory': { breadcrumb: 'Kiểm Kê Thiết Bị', heading: 'Sổ Kiểm Kê: Thiết Bị Đang Hoạt Động vs Chờ Thanh Lý' },
      'tab-tntt': { breadcrumb: 'Chỉ Đạo Mới / QĐ 78', heading: 'Quy Định Xếp Loại & Chi Thu Nhập Tăng Thêm (NQ 98)' },
      'tab-inspection': { breadcrumb: 'Chỉ Đạo Mới / QĐ 9326', heading: 'Quyết Định Thành Lập Đoàn Kiểm Tra Công Vụ Năm 2026' },
      'tab-facility': { breadcrumb: 'Cơ Sở Vật Chất / NĐ 155', heading: 'Phương Án Tiếp Nhận Trạm Y Tế Số 3 Mở Rộng Trụ Sở' },
      'tab-network': { breadcrumb: 'Hạ Tầng / Mạng & Server', heading: 'Sơ Đồ Phòng Máy Chủ, Switch & Dải IP Chuyên Dùng' },
      'tab-toner': { breadcrumb: 'Vật Tư / Hộp Mực In', heading: 'Bảng Tra Cứu Mã Hộp Mực Cho Toàn Bộ 38 Máy In Đang Dùng' },
      'tab-proposal': { breadcrumb: 'Kinh Phí / Đề Xuất 1342', heading: 'Dự Toán Đề Xuất Bố Trí Kinh Phí IT 752.829.000 VNĐ' },
      'tab-risk': { breadcrumb: 'Pháp Lý / Quản Trị Rủi Ro', heading: 'Báo Cáo Nhận Diện & Kiểm Soát Rủi Ro Kỹ Thuật IT' },
      'tab-event': { breadcrumb: 'Lịch Sử / Sự Kiện Đã Qua', heading: 'Tiến Trình Sự Kiện & Biên Bản Bàn Giao Tháng 09 - 10/2026' },
      'tab-markdown': { breadcrumb: 'Tài Liệu / Toàn Văn Markdown', heading: 'Báo Cáo Kỹ Thuật Hệ Thống & Toàn Văn Đề Xuất' }
    };

    function toggleSidebar() {
      const sidebar = document.getElementById('sidebar');
      const overlay = document.getElementById('sidebar-overlay');
      const isClosed = sidebar.classList.contains('-translate-x-full');
      
      if (isClosed) {
        sidebar.classList.remove('-translate-x-full');
        overlay.classList.remove('hidden');
      } else {
        sidebar.classList.add('-translate-x-full');
        overlay.classList.add('hidden');
      }
    }

    function switchTab(tabId) {
      // 1. Hide all tab contents
      document.querySelectorAll('.tab-content').forEach(el => {
        el.classList.add('hidden');
        el.classList.remove('block');
      });

      // 2. Remove active state from all sidebar nav items
      document.querySelectorAll('.nav-item').forEach(btn => {
        btn.classList.remove('nav-item-active');
      });

      // 3. Show selected tab content
      const targetContent = document.getElementById(tabId);
      if (targetContent) {
        targetContent.classList.remove('hidden');
        targetContent.classList.add('block');
      }

      // 4. Set active state on matching button
      const targetBtn = document.getElementById('btn-' + tabId);
      if (targetBtn) {
        targetBtn.classList.add('nav-item-active');
      }

      // 5. Update Breadcrumb and Topbar Title
      if (tabTitles[tabId]) {
        document.getElementById('breadcrumb-title').textContent = tabTitles[tabId].breadcrumb;
        document.getElementById('topbar-heading').textContent = tabTitles[tabId].heading;
      }

      // 6. Close sidebar on mobile after clicking
      if (window.innerWidth < 1024) {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        sidebar.classList.add('-translate-x-full');
        overlay.classList.add('hidden');
      }

      // 7. Scroll smoothly to top
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Auto-render KaTeX math after load
    document.addEventListener("DOMContentLoaded", function() {
      if (typeof renderMathInElement === 'function') {
        renderMathInElement(document.body, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false},
            {left: '\\(', right: '\\)', display: false},
            {left: '\\[', right: '\\]', display: true}
          ],
          throwOnError : false
        });
      }
    });
  </script>
</body>
</html>
'''

with open('OUTPUT/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("SUCCESS: Generated new responsive sidebar OUTPUT/index.html!")
