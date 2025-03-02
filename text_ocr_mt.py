import os
import easyocr
from PIL import Image
import concurrent.futures
import threading

# 创建线程锁用于打印输出，避免输出混乱
print_lock = threading.Lock()

def safe_print(*args, **kwargs):
    """线程安全的打印函数"""
    with print_lock:
        print(*args, **kwargs)

def process_image_file(input_file_path, output_file_path, reader):
    """处理单个图像文件的函数，用于多线程调用"""
    try:
        # 使用 PIL 打开图片以验证格式
        img = Image.open(input_file_path)
        
        safe_print(f"正在处理图片：{input_file_path}")
        safe_print(f"图片尺寸：{img.size[0]} x {img.size[1]}")
        safe_print("正在进行 OCR 识别，请稍候...")
        
        # 进行 OCR 识别
        results = reader.readtext(input_file_path)
        
        # 将结果连接成一个字符串，不包含换行符
        if results:
            # 过滤掉符合特定条件的文本：
            # 以左括号开头，右括号结尾，且总长度小于10
            filtered_texts = []
            for _, text, _ in results:
                # 检查文本是否以左括号开头，右括号结尾
                starts_with_left_paren = text.startswith("(") or text.startswith("（")
                ends_with_right_paren = text.endswith(")") or text.endswith("）")
                
                # 如果同时满足开头、结尾条件且长度小于10，则排除
                if starts_with_left_paren and ends_with_right_paren and len(text) < 10:
                    continue
                
                filtered_texts.append(text)
            
            # 提取所有文本并连接
            text_content = ''.join(filtered_texts)
            
            # 写入到输出文件
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(text_content)
            
            safe_print(f"已将OCR结果保存到: {output_file_path}")
        else:
            safe_print("未能识别到任何文本")
            # 创建一个空文件
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write("")
                
    except Exception as e:
        safe_print(f"处理文件 {input_file_path} 时发生错误: {e}")
    
    safe_print("-----------------------------------")
    return input_file_path

def process_images(input_dir="cutter_output", output_dir="ocr_output", num_threads=8):
    """
    使用多线程处理指定目录下的PNG文件，排除以特定后缀结尾的文件，
    并将OCR结果保存到对应的TXT文件中
    
    Args:
        input_dir: 输入目录，默认为"cutter_output"
        output_dir: 输出目录，默认为"ocr_output"
        num_threads: 线程数，默认为8
    """
    # 初始化 EasyOCR 读取器，这里使用中文和英文
    reader = easyocr.Reader(['ch_sim', 'en'])
    
    # 需要排除的后缀
    excluded_suffixes = ['_table.png', '_equation.png', '_figure.png', '_header.png', '_equation.png', '_figure_caption.png', '_table_caption.png']
    
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取所有子目录
    subdirs = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]
    
    # 创建任务列表
    tasks = []
    
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
            
            # 添加到任务列表
            tasks.append((input_file_path, output_file_path))
    
    # 使用线程池执行任务
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # 提交所有任务
        future_to_file = {
            executor.submit(process_image_file, input_file, output_file, reader): input_file
            for input_file, output_file in tasks
        }
        
        # 等待所有任务完成并获取结果
        completed_count = 0
        total_count = len(tasks)
        
        for future in concurrent.futures.as_completed(future_to_file):
            completed_count += 1
            filename = future_to_file[future]
            try:
                future.result()
                safe_print(f"进度: {completed_count}/{total_count} ({(completed_count/total_count)*100:.1f}%)")
            except Exception as e:
                safe_print(f"处理文件 {filename} 时发生异常: {e}")

if __name__ == "__main__":
    process_images(num_threads=8)
    print("OCR处理完成！")