import os
import cv2
import glob
import shutil
import pandas as pd
from paddleocr import PPStructure, save_structure_res

def ensure_dir(directory):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def xlsx_to_markdown(xlsx_file, output_file):
    """将单个 xlsx 文件转换为 markdown 文件"""
    try:
        # 读取 Excel 文件中的所有表
        excel_data = pd.read_excel(xlsx_file, sheet_name=None)
        
        with open(output_file, 'w', encoding='utf-8') as md_file:
            # 对每个工作表进行处理
            for sheet_name, df in excel_data.items():
                # 写入工作表名称作为标题
                md_file.write(f"# {sheet_name}\n\n")
                
                # 转换为 markdown 表格
                try:
                    markdown_table = df.to_markdown(index=False)
                    md_file.write(markdown_table)
                except ImportError:
                    # 如果没有安装tabulate，使用简单的表格格式
                    md_file.write(df.to_csv(sep='|', index=False).replace(',', '|'))
                md_file.write("\n\n")
        
        print(f"已将 {xlsx_file} 转换为 {output_file}")
        return True
    except Exception as e:
        print(f"处理 {xlsx_file} 时出错: {e}")
        return False

def process_table_image(img_path, output_dir):
    """处理单个表格图像并保存为markdown"""
    try:
        # 确保输出目录存在
        ensure_dir(output_dir)
        
        # 设置临时保存xlsx的文件夹
        temp_xlsx_dir = os.path.join(output_dir, "temp_xlsx")
        ensure_dir(temp_xlsx_dir)
        
        # 获取文件名（不含扩展名）
        file_name = os.path.splitext(os.path.basename(img_path))[0]
        
        # 初始化表格识别引擎
        table_engine = PPStructure(layout=False, show_log=False)
        
        # 读取图像并进行OCR处理
        img = cv2.imread(img_path)
        result = table_engine(img)
        
        # 保存结构化结果（xlsx文件）
        save_structure_res(result, temp_xlsx_dir, file_name)
        
        # 查找生成的xlsx文件 - 现在正确处理子文件夹路径
        xlsx_folder = os.path.join(temp_xlsx_dir, file_name)
        xlsx_files = glob.glob(os.path.join(xlsx_folder, "*.xlsx"))
        
        if not xlsx_files:
            print(f"未找到生成的xlsx文件在: {xlsx_folder}")
            return
        
        # 获取第一个xlsx文件（通常只有一个）
        xlsx_file = xlsx_files[0]
        
        # 转换为markdown并保存
        txt_file = os.path.join(output_dir, f"{file_name}.txt")
        if xlsx_to_markdown(xlsx_file, txt_file):
            print(f"成功处理表格图像: {img_path}")
        
        # 清理临时文件夹
        shutil.rmtree(temp_xlsx_dir, ignore_errors=True)
    
    except Exception as e:
        print(f"处理表格图像 {img_path} 时出错: {e}")

def main():
    """主函数，处理所有表格图像"""
    # 项目根目录
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 输入和输出目录
    input_dir = os.path.join(root_dir, "cutter_output")
    output_dir = os.path.join(root_dir, "ocr_output")
    
    # 确保输出目录存在
    ensure_dir(output_dir)
    
    # 安装所需库
    try:
        import tabulate
    except ImportError:
        print("需要安装 tabulate 库。正在安装...")
        try:
            import pip
            pip.main(['install', 'tabulate'])
            print("tabulate 安装成功")
        except Exception as e:
            print(f"安装 tabulate 失败: {e}")
            print("请手动安装: pip install tabulate")
    
    # 遍历cutter_output下的所有子文件夹
    for subfolder in glob.glob(os.path.join(input_dir, "*")):
        if os.path.isdir(subfolder):
            folder_name = os.path.basename(subfolder)
            print(f"处理文件夹: {folder_name}")
            
            # 创建对应的输出子文件夹
            output_subfolder = os.path.join(output_dir, folder_name)
            ensure_dir(output_subfolder)
            
            # 查找所有以"_table.png"结尾的PNG文件
            table_images = glob.glob(os.path.join(subfolder, "*_table.png"))
            
            for img_path in table_images:
                print(f"处理表格图像: {img_path}")
                process_table_image(img_path, output_subfolder)

if __name__ == "__main__":
    main()