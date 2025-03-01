import easyocr
import os
from PIL import Image

def ocr_image(image_path):
    # 初始化 EasyOCR 读取器，这里使用中文和英文
    reader = easyocr.Reader(['ch_sim', 'en'])
    
    # 检查文件是否存在
    if not os.path.exists(image_path):
        print(f"错误：文件 {image_path} 不存在")
        return
    
    try:
        # 使用 PIL 打开图片以验证格式
        img = Image.open(image_path)
        
        # 打印正在处理的图片信息
        print(f"正在处理图片：{image_path}")
        print(f"图片尺寸：{img.size[0]} x {img.size[1]}")
        print("正在进行 OCR 识别，请稍候...")
        
        # 进行 OCR 识别
        results = reader.readtext(image_path)
        
        # 输出结果
        print("\n识别结果：")
        if not results:
            print("未能识别到任何文本")
        else:
            for i, (bbox, text, prob) in enumerate(results):
                print(f"文本 {i+1}:")
                print(f"  内容: {text}")
                print(f"  置信度: {prob:.2f}")
                print(f"  位置: {bbox}")
                print()
                
    except Exception as e:
        print(f"OCR 处理过程中发生错误: {e}")

if __name__ == "__main__":
    # 指定图片路径
    image_path = "./pic.png"  # 根目录下的 pic.png
    
    # 执行 OCR
    ocr_image(image_path)