import os
import json
from PIL import Image
import shutil

def ensure_dir(directory):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    # 定义目录路径
    project_root = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(project_root, 'pdf2pic_output')
    structure_dir = os.path.join(project_root, 'structure_info')
    output_dir = os.path.join(project_root, 'cutter_output')
    
    # 确保输出目录存在
    ensure_dir(output_dir)
    
    # 获取所有输入图片
    input_images = [f for f in os.listdir(input_dir) if f.endswith('.png')]
    
    for img_file in input_images:
        # 获取文件名（不含扩展名）
        filename = os.path.splitext(img_file)[0]
        
        # 构建结构信息目录路径
        img_structure_dir = os.path.join(structure_dir, filename)
        res_file_path = os.path.join(img_structure_dir, 'res_0.txt')
        
        # 检查结构信息文件是否存在
        if not os.path.exists(res_file_path):
            print(f"警告: 找不到 {res_file_path}，跳过 {img_file}")
            continue
        
        # 读取图片
        img_path = os.path.join(input_dir, img_file)
        try:
            image = Image.open(img_path)
            img_width, img_height = image.size
        except Exception as e:
            print(f"错误: 无法打开图片 {img_path}: {e}")
            continue
        
        # 创建输出子目录
        img_output_dir = os.path.join(output_dir, filename)
        ensure_dir(img_output_dir)
        
        # 读取边界框信息
        bbox_items = []
        with open(res_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            for i, line in enumerate(lines):
                try:
                    # 解析JSON
                    bbox_info = json.loads(line.strip())
                    
                    # 将索引添加到信息中，用于保留原始顺序（如果需要的话）
                    bbox_info['original_index'] = i
                    
                    bbox_items.append(bbox_info)
                except json.JSONDecodeError:
                    print(f"警告: {res_file_path} 中第 {i+1} 行不是有效的JSON")
        
        # 按照y坐标（bbox的第二个值）排序
        bbox_items.sort(key=lambda x: x.get('bbox', [0, 0, 0, 0])[1])
        
        # 对每个边界框进行切分
        for i, bbox_info in enumerate(bbox_items):
            try:
                # 提取信息
                box_type = bbox_info.get('type', 'unknown')
                bbox = bbox_info.get('bbox', [])
                
                if not bbox or len(bbox) != 4:
                    print(f"警告: 边界框格式不正确")
                    continue
                
                # 扩大边界框（前两个坐标-20，后两个坐标+20）
                left, top, right, bottom = bbox
                left = max(0, left - 20)
                top = max(0, top - 20)
                right = min(img_width, right + 20)
                bottom = min(img_height, bottom + 20)
                
                # 裁剪图片
                cropped_img = image.crop((left, top, right, bottom))
                
                # 保存裁剪后的图片
                output_filename = f"{i+1}_{box_type}.png"
                output_path = os.path.join(img_output_dir, output_filename)
                cropped_img.save(output_path)
                
                print(f"已保存: {output_path}")
                
            except Exception as e:
                print(f"错误: 处理 {img_file} 中的框 {i+1} 时出错: {e}")
    
    print("所有图片处理完成！")

if __name__ == "__main__":
    main()