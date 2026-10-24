# -*- coding: utf-8 -*-
with open('/Users/admin/Desktop/BINHDUONG/OUTPUT/document_viewer.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update <style> block to include robust Light Mode rules for documents and tables
old_style_marker = """    body {
      font-family: 'Inter', sans-serif;
      background-color: #f8fafc;
      color: #0f172a;
    }"""

new_style_block = """    body {
      font-family: 'Inter', sans-serif;
      background-color: #f8fafc;
      color: #0f172a;
    }
    
    /* Ensure all paragraphs in document body are high contrast and sharp */
    .document-render-body p {
      color: #1e293b !important;
      font-weight: 400;
    }
    
    /* Document headings */
    .document-render-body h4 {
      color: #0369a1 !important;
      border-color: #e2e8f0 !important;
    }
    
    /* Document transcript blocks */
    .document-render-body pre {
      color: #0f172a !important;
      background-color: #f8fafc !important;
    }

    /* All tables in document viewer */
    table {
      background-color: #ffffff !important;
    }
    th {
      color: #0f172a !important;
    }
    td {
      color: #1e293b !important;
    }"""

if old_style_marker in content:
    content = content.replace(old_style_marker, new_style_block)

# 2. Fix doc (.docx) paragraph text colors
content = content.replace("class='text-slate-300 mb-2 leading-relaxed text-sm'", "class='text-slate-800 mb-2 leading-relaxed text-sm font-normal'")
content = content.replace('class="text-slate-300 mb-2 leading-relaxed text-sm"', 'class="text-slate-800 mb-2 leading-relaxed text-sm font-normal"')
content = content.replace("text-slate-300", "text-slate-800")

# 3. Fix headings border
content = content.replace("border-slate-700/60 pb-1", "border-slate-200 pb-1")
content = content.replace("border-slate-700/60", "border-slate-200")
content = content.replace("border-slate-800", "border-slate-200")

# 4. Fix Excel (.xlsx) table header rows
content = content.replace(
    "<tr class='bg-slate-800 text-sky-800 font-semibold sticky top-0 z-10 border-b border-slate-700/60 hover:bg-sky-950/30 transition'>",
    "<tr class='bg-slate-100 text-slate-900 font-bold sticky top-0 z-10 border-b-2 border-slate-300 hover:bg-slate-200/70 transition shadow-2xs'>"
)
content = content.replace(
    "<tr class='bg-slate-800 text-sky-800 font-semibold sticky top-0 z-10 border-b border-slate-200 hover:bg-sky-950/30 transition'>",
    "<tr class='bg-slate-100 text-slate-900 font-bold sticky top-0 z-10 border-b-2 border-slate-300 hover:bg-slate-200/70 transition shadow-2xs'>"
)

# 5. Fix Excel table data rows (even & odd)
content = content.replace(
    "<tr class='bg-slate-900/30 border-b border-slate-700/60 hover:bg-sky-950/30 transition'>",
    "<tr class='bg-white border-b border-slate-200 text-slate-800 hover:bg-sky-50/60 transition'>"
)
content = content.replace(
    "<tr class='bg-slate-900/70 border-b border-slate-700/60 hover:bg-sky-950/30 transition'>",
    "<tr class='bg-slate-50/70 border-b border-slate-200 text-slate-800 hover:bg-sky-50/60 transition'>"
)
content = content.replace(
    "<tr class='bg-slate-900/30 border-b border-slate-200 hover:bg-sky-950/30 transition'>",
    "<tr class='bg-white border-b border-slate-200 text-slate-800 hover:bg-sky-50/60 transition'>"
)
content = content.replace(
    "<tr class='bg-slate-900/70 border-b border-slate-200 hover:bg-sky-950/30 transition'>",
    "<tr class='bg-slate-50/70 border-b border-slate-200 text-slate-800 hover:bg-sky-50/60 transition'>"
)

# 6. Any remaining dark backgrounds or dark hovers
content = content.replace("hover:bg-sky-950/30", "hover:bg-sky-50/60")
content = content.replace("bg-slate-900/80", "bg-slate-50")
content = content.replace("bg-slate-900/60", "bg-slate-50")
content = content.replace("bg-slate-900/30", "bg-white")
content = content.replace("bg-slate-900/70", "bg-slate-50")
content = content.replace("bg-slate-800", "bg-slate-100")

# 7. Ensure table container is bg-white
content = content.replace(
    "overflow-x-auto rounded-lg border border-slate-200 max-h-[600px] shadow-2xs rounded-lg",
    "overflow-x-auto rounded-lg border border-slate-200 bg-white max-h-[650px] shadow-xs"
)
content = content.replace(
    "<table class='w-full text-xs text-left border-collapse'>",
    "<table class='w-full text-xs text-left border-collapse bg-white'>"
)

with open('/Users/admin/Desktop/BINHDUONG/OUTPUT/document_viewer.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated OUTPUT/document_viewer.html colors successfully!")
