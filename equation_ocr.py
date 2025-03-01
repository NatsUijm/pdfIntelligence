import os
import glob
from PIL import Image
from pix2tex.cli import LatexOCR
import shutil

def process_equation_images():
    # 初始化OCR模型
    model = LatexOCR()
    
    # 创建输出根目录
    output_root = "ocr_output"
    os.makedirs(output_root, exist_ok=True)
    
    # 获取cutter_output下的所有子文件夹
    input_root = "cutter_output"
    subfolders = [f.path for f in os.scandir(input_root) if f.is_dir()]
    
    for subfolder in subfolders:
        # 获取子文件夹名
        subfolder_name = os.path.basename(subfolder)
        
        # 创建对应的输出子文件夹
        output_subfolder = os.path.join(output_root, subfolder_name)
        os.makedirs(output_subfolder, exist_ok=True)
        
        # 查找所有包含"equation"的PNG文件
        equation_images = glob.glob(os.path.join(subfolder, "*equation*.png"))
        
        for image_path in equation_images:
            try:
                # 获取图像文件名（不含扩展名）
                image_name = os.path.basename(image_path)
                image_name_without_ext = os.path.splitext(image_name)[0]
                
                # 转换图像为LaTeX
                img = Image.open(image_path)
                latex_result = model(img)
                
                # 创建与输入图像对应的输出文本文件路径
                output_file_path = os.path.join(output_subfolder, f"{image_name_without_ext}.txt")
                
                # 将LaTeX结果写入文本文件
                with open(output_file_path, "w", encoding="utf-8") as f:
                    f.write(latex_result)
                
                print(f"Processed: {image_path} -> {output_file_path}")
                
            except Exception as e:
                print(f"Error processing {image_path}: {str(e)}")
    
    print("Processing completed!")

if __name__ == "__main__":
    process_equation_images()