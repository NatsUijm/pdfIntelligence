import os
import json
import fitz  # PyMuPDF
from pathlib import Path

def extract_toc_from_pdf():
    # 查找项目根目录下的唯一PDF文件
    pdf_files = list(Path('.').glob('*.pdf'))
    
    if len(pdf_files) == 0:
        print("错误：在当前目录下未找到PDF文件")
        return
    
    if len(pdf_files) > 1:
        print("错误：在当前目录下找到多个PDF文件")
        return
    
    pdf_file = pdf_files[0]
    print(f"找到PDF文件：{pdf_file}")
    
    # 打开PDF文件
    try:
        doc = fitz.open(str(pdf_file))
        toc = doc.get_toc()
        
        # 如果没有目录
        if not toc:
            print("该PDF文件没有目录")
            return
        
        # 转换目录结构为所需格式
        toc_data = []
        for item in toc:
            level, title, page = item
            toc_data.append({
                "title": title,
                "level": level,
                "page": page
            })
        
        # 将目录数据保存为JSON文件
        output_file = pdf_file.stem + "_toc.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(toc_data, f, ensure_ascii=False, indent=2)
        
        print(f"目录已保存到：{output_file}")
        doc.close()
        
    except Exception as e:
        print(f"处理PDF时出错：{e}")

if __name__ == "__main__":
    extract_toc_from_pdf()