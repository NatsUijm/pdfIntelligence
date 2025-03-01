import os
import easyocr
from PIL import Image

def process_images(input_dir="cutter_output", output_dir="ocr_output"):
    """
    处理指定目录下的PNG文件，排除以_table.png、_equation.png和_figure.png结尾的文件，
    并将OCR结果保存到对应的TXT文件中
    
    Args:
        input_dir: 输入目录，默认为"cutter_output"
        output_dir: 输出目录，默认为"ocr_output"
    """
    # 初始化 EasyOCR 读取器，这里使用中文和英文
    reader = easyocr.Reader(['ch_sim', 'en'])
    
    # 需要排除的后缀
    excluded_suffixes = ['_table.png', '_equation.png', '_figure.png']
    
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取所有子目录
    subdirs = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]
    
    for subdir in subdirs:
        input_subdir_path = os.path.join(input_dir, subdir)
        output_subdir_path = os.path.join(output_dir, subdir)
        
        # 确保输出子目录存在
        if not os.path.exists(output_subdir_path):
            os.makedirs(output_subdir_path)
        
        # 获取所有PNG文件，排除特定后缀的文件
        png_files = []
        for f in os.listdir(input_subdir_path):
            if f.endswith('.png'):
                # 检查文件是否是需要排除的类型
                should_exclude = False
                for suffix in excluded_suffixes:
                    if f.endswith(suffix):
                        should_exclude = True
                        break
                
                if not should_exclude:
                    png_files.append(f)
        
        for png_file in png_files:
            input_file_path = os.path.join(input_subdir_path, png_file)
            output_file_path = os.path.join(output_subdir_path, png_file.replace('.png', '.txt'))
            
            try:
                # 使用 PIL 打开图片以验证格式
                img = Image.open(input_file_path)
                
                print(f"正在处理图片：{input_file_path}")
                print(f"图片尺寸：{img.size[0]} x {img.size[1]}")
                print("正在进行 OCR 识别，请稍候...")
                
                # 进行 OCR 识别
                results = reader.readtext(input_file_path)
                
                # 将结果连接成一个字符串，不包含换行符
                if results:
                    # 提取所有文本并连接
                    text_content = ' '.join([text for _, text, _ in results])
                    
                    # 写入到输出文件
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        f.write(text_content)
                    
                    print(f"已将OCR结果保存到: {output_file_path}")
                else:
                    print("未能识别到任何文本")
                    # 创建一个空文件
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        f.write("")
                        
            except Exception as e:
                print(f"处理文件 {input_file_path} 时发生错误: {e}")
            
            print("-----------------------------------")

if __name__ == "__main__":
    process_images()
    print("OCR处理完成！")