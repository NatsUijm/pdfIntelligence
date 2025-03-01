import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# 定义不同类型的边界框颜色
colors = {
    "text": (255, 0, 0),         # 蓝色
    "figure": (0, 255, 0),       # 绿色
    "figure_caption": (0, 255, 255),  # 黄色
    "table": (255, 0, 255),      # 紫色
    "table_caption": (0, 0, 255),  # 红色
    "reference": (255, 165, 0),  # 橙色
    "equation": (128, 0, 128)    # 深紫色
}

def draw_boxes_on_image(txt_file, image_file, output_file=None):
    # 读取文本文件
    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 读取图像
    img = cv2.imread(image_file)
    if img is None:
        raise FileNotFoundError(f"图像文件 {image_file} 没有找到")
    
    # 获取图像尺寸
    height, width = img.shape[:2]
    
    # 解析边界框并绘制在图像上
    for line in lines:
        try:
            data = json.loads(line.strip())
            bbox = data.get("bbox")
            box_type = data.get("type")
            
            if bbox and box_type:
                x1, y1, x2, y2 = [int(i) for i in bbox]
                color = colors.get(box_type, (0, 0, 0))  # 默认黑色
                
                # 绘制矩形框
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                
                # 添加类型标签
                cv2.putText(img, box_type, (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        except json.JSONDecodeError:
            print(f"无效的JSON行: {line}")
        except Exception as e:
            print(f"处理行时出错: {e}")
    
    # 保存或显示结果图像
    if output_file:
        cv2.imwrite(output_file, img)
        print(f"标注图像已保存到 {output_file}")
    else:
        output_file = "annotated_pic.png"
        cv2.imwrite(output_file, img)
        print(f"标注图像已保存到 {output_file}")
    
    return img

# 执行函数
if __name__ == "__main__":
    txt_file = "res_0.txt"
    image_file = "pic.png"
    output_file = "annotated_pic.png"
    
    # 检查文件是否存在
    if not os.path.exists(txt_file):
        print(f"错误: 文件 {txt_file} 不存在")
    elif not os.path.exists(image_file):
        print(f"错误: 图像 {image_file} 不存在")
    else:
        img = draw_boxes_on_image(txt_file, image_file, output_file)