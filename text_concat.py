import os
import glob
import re

def natural_sort_key(s):
    """用于自然排序的键函数，处理数字编号的文件名"""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]

def concatenate_txt_files():
    # 创建输出目录
    output_dir = "output_pages"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录: {output_dir}")
    
    # 获取所有子文件夹
    ocr_dir = "ocr_output"
    subdirs = [d for d in os.listdir(ocr_dir) if os.path.isdir(os.path.join(ocr_dir, d))]
    
    for subdir in subdirs:
        subdir_path = os.path.join(ocr_dir, subdir)
        output_filename = f"{subdir}.txt"
        output_path = os.path.join(output_dir, output_filename)
        
        # 获取所有txt文件并按自然顺序排序
        txt_files = glob.glob(os.path.join(subdir_path, "*.txt"))
        txt_files.sort(key=natural_sort_key)
        
        # 合并文件内容
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for txt_file in txt_files:
                try:
                    with open(txt_file, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content)
                        # 如果文件末尾没有换行符，则添加一个
                        if content and not content.endswith('\n'):
                            outfile.write('\n')
                except Exception as e:
                    print(f"处理文件 {txt_file} 时出错: {str(e)}")
        
        print(f"已合并 {len(txt_files)} 个文件到 {output_path}")

if __name__ == "__main__":
    concatenate_txt_files()
    print("所有文件处理完成！")