import os
import cv2
from paddleocr import PPStructure, save_structure_res
import glob
import concurrent.futures

# 初始化PPStructure引擎
table_engine = PPStructure(table=False, ocr=False, show_log=True)

# 设置输入和输出文件夹
input_folder = './pdf2pic_output'
output_folder = './structure_info'

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取所有PNG文件
png_files = glob.glob(os.path.join(input_folder, '*.png'))

# 处理单个文件的函数
def process_image(img_path):
    print(f"处理文件: {img_path}")
    
    # 读取图像
    img = cv2.imread(img_path)
    if img is None:
        print(f"无法读取图像: {img_path}")
        return
    
    # 获取结果
    result = table_engine(img)
    
    # 获取不带路径和扩展名的文件名
    base_name = os.path.basename(img_path).split('.')[0]
    
    # 保存结构化结果
    save_structure_res(result, output_folder, base_name)
    
    # 打印结果信息(去除图像数据)
    print(f"文件 {base_name} 的结构信息:")
    for line in result:
        line_copy = line.copy()
        if 'img' in line_copy:
            line_copy.pop('img')
        print(line_copy)
    print("="*50)
    
    return f"{base_name} 处理完成"

# 使用线程池执行
print(f"开始处理 {len(png_files)} 个文件，使用8线程...")
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(process_image, img_path) for img_path in png_files]
    
    # 获取结果（可选）
    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()
            if result:
                print(result)
        except Exception as e:
            print(f"处理过程中出现错误: {e}")

print("所有文件处理完成！")