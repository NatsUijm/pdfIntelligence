import os
import sys
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from PIL import Image
import numpy as np

def convert_pdf_pages_to_png(pdf_path, output_folder, start_page=None, end_page=None):
    """
    将PDF文件的指定页面范围转换为PNG图片，并进行二值化处理
    
    参数:
        pdf_path: PDF文件路径
        output_folder: 输出文件夹路径
        start_page: 起始页码（从1开始），默认为None表示从第一页开始
        end_page: 结束页码，默认为None表示到最后一页
    """
    # 固定阈值为240
    threshold = 240
    
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 获取PDF文件名（不含扩展名）
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # 读取PDF文件获取总页数
    pdf = PdfReader(pdf_path)
    total_pages = len(pdf.pages)
    
    # 设置起始页和结束页
    if start_page is None:
        start_page = 1
    else:
        start_page = max(1, start_page)
    
    if end_page is None:
        end_page = total_pages
    else:
        end_page = min(total_pages, end_page)
    
    # 将页码从1开始调整为从0开始（pdf2image库使用从0开始的索引）
    start_idx = start_page - 1
    end_idx = end_page - 1
    
    print(f"正在处理 {pdf_path}")
    print(f"转换页面范围: {start_page} 到 {end_page} (总页数: {total_pages})")
    print(f"使用二值化阈值: {threshold}")
    
    # 转换PDF页面为图片
    images = convert_from_path(
        pdf_path,
        first_page=start_page,
        last_page=end_page,
        dpi=300
    )
    
    # 保存图片并进行二值化处理
    for i, image in enumerate(images):
        page_num = start_idx + i + 1
        
        # 转为灰度图像
        gray_image = image.convert('L')
        
        # 使用NumPy进行二值化处理
        gray_array = np.array(gray_image)
        binary_array = np.where(gray_array < threshold, 0, 255).astype(np.uint8)
        binary_image = Image.fromarray(binary_array)
        
        # 保存二值化图像
        output_path = os.path.join(output_folder, f"{pdf_name}_page_{page_num}.png")
        binary_image.save(output_path, 'PNG')
        print(f"已保存二值化图像: {output_path}")
    
    print(f"转换完成: {len(images)} 页已转换为二值化PNG图片")

def main():
    # 获取当前工作目录（根目录）
    root_dir = os.getcwd()
    output_folder = os.path.join(root_dir, "pdf2pic_output")
    
    # 获取根目录下的所有PDF文件
    pdf_files = [f for f in os.listdir(root_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("根目录下没有找到PDF文件。")
        return
    
    print(f"在根目录中找到 {len(pdf_files)} 个PDF文件")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(root_dir, pdf_file)
        
        # 用户输入要转换的页面范围
        print(f"\n处理文件: {pdf_file}")
        start_input = input("输入起始页码 (直接回车表示从第一页开始): ")
        end_input = input("输入结束页码 (直接回车表示到最后一页): ")
        
        start_page = int(start_input) if start_input.strip() else None
        end_page = int(end_input) if end_input.strip() else None
        
        convert_pdf_pages_to_png(pdf_path, output_folder, start_page, end_page)
    
    print("\n所有PDF文件处理完成！")

if __name__ == "__main__":
    main()