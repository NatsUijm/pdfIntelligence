请写一个python脚本，要求将一组图片分别以指定的范围分割成一堆小图片，具体要求如下：

1. 原始图片保存在项目根目录下的`pdf2pic_output`文件夹中，该文件夹下是一些`PNG`图片，例如：
   ```
   电力系统继电保护_page_47.png
   电力系统继电保护_page_48.png
   电力系统继电保护_page_49.png
   ```

2. 每个`PNG`图片都有不同的切分框，保存在根目录下的`structure_info`文件夹中，这个文件夹下面有一些子文件夹，例如：
   ```
   电力系统继电保护_page_47
   电力系统继电保护_page_48
   电力系统继电保护_page_49
   ```

   每一个子文件夹都有一个`res_0.txt`文件，其中储存了不同种类的文本框数据，比如：
   ```
   {"type": "text", "bbox": [168, 876, 1925, 2827], "res": "", "img_idx": 0, "score": 0.9934877157211304}
   {"type": "text", "bbox": [174, 289, 1931, 525], "res": "", "img_idx": 0, "score": 0.9757193922996521}
   {"type": "title", "bbox": [632, 612, 1395, 660], "res": "", "img_idx": 0, "score": 0.5757401585578918}
   {"type": "header", "bbox": [865, 190, 1236, 225], "res": "", "img_idx": 0, "score": 0.955810546875}
   {"type": "header", "bbox": [1850, 187, 1891, 219], "res": "", "img_idx": 0, "score": 0.9079431891441345}
   ```

3. 需要将每个`bbox`的内容切成一个`PNG`文件，保存在`cutter_output`文件夹中，这个文件夹同样包含一些子文件夹，例如：
   ```
   电力系统继电保护_page_47
   电力系统继电保护_page_48
   电力系统继电保护_page_49
   ```

   每个子文件夹保存着对应页面的每个文本框，并且按照`res_0.txt`的顺序排序，包含`type`信息，例如对于上面的那个`res_0.txt`文件，应该生成如下的`PNG`文件：
   ```
   1_text.png  // 对应[168, 876, 1925, 2827]的文本框
   2_text.png  // 对应[174, 289, 1931, 525]的文本框
   3_title.png // 以此类推...
   4_header.png
   5_header.png
   ```







请你写一个python脚本，要求对特定的PNG文件进行LaTeX转换，具体逻辑如下：

1. 项目根目录下有一个文件夹`cutter_output`，存储着一些子文件夹，例如：
   ```
   电力系统继电保护_page_47
   电力系统继电保护_page_48
   电力系统继电保护_page_49
   ```

   每个子文件夹下都有一些`png`文件，例如：
   ```
   3_text.png
   4_equation.png
   ...
   ```

2. 需要使用`pix2tex`库对每一个`equation`类型的`png`文件进行OCR处理，示例代码如下：
   ```python
   from PIL import Image
   from pix2tex.cli import LatexOCR
   
   img = Image.open('./equaltion.png')
   model = LatexOCR()
   print(model(img))
   ```

3. 输出到项目根目录下的`ocr_output`文件夹中，具体路径与输入相同。例如对于上面的情况，应该在`ocr_output`中也建立子文件夹：
   ```
   电力系统继电保护_page_47
   电力系统继电保护_page_48
   电力系统继电保护_page_49
   ```

   要将`PNG`对应的`txt`文件输出到同名的文件中，例如：
   ```
   4_equation.txt
   ...
   ```

   

请你写一个python脚本，要求对特定的PNG文件进行OCR转换，具体逻辑如下：

1. 项目根目录下有一个文件夹`cutter_output`，存储着一些子文件夹，例如：

   ```
   电力系统继电保护_page_47
   电力系统继电保护_page_48
   电力系统继电保护_page_49
   ```

   每个子文件夹下都有一些`png`文件，例如：

   ```
   3_text.png
   4_figure.png
   5_equation.png
   19_table.png
   ...
   ```

2. 需要使用`paddleocr`库对每一个`table`类型的`png`文件进行OCR处理，示例代码如下：

   ```python
   import os
   import cv2
   from paddleocr import PPStructure,save_structure_res
   
   table_engine = PPStructure(layout=False, show_log=True)
   
   save_folder = './output'
   img_path = './table.png'
   img = cv2.imread(img_path)
   result = table_engine(img)
   save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])
   
   for line in result:
       line.pop('img')
       print(line)
   ```

3. 上述代码输出的是xlsx文件，我们需要将其转化为markdown格式，示例代码如下：
   ```python
   import os
   import pandas as pd
   import glob
   
   def xlsx_to_markdown(xlsx_file):
       """将单个 xlsx 文件转换为 markdown 文件"""
       # 获取文件名（不含扩展名）
       file_name = os.path.splitext(os.path.basename(xlsx_file))[0]
       
       # 创建输出文件的路径
       output_file = f"{file_name}.md"
       
       # 读取 Excel 文件中的所有表
       excel_data = pd.read_excel(xlsx_file, sheet_name=None)
       
       with open(output_file, 'w', encoding='utf-8') as md_file:
           # 对每个工作表进行处理
           for sheet_name, df in excel_data.items():
               # 写入工作表名称作为标题
               md_file.write(f"# {sheet_name}\n\n")
               
               # 转换为 markdown 表格
               markdown_table = df.to_markdown(index=False)
               md_file.write(markdown_table)
               md_file.write("\n\n")
       
       print(f"已将 {xlsx_file} 转换为 {output_file}")
   
   def main():
       """处理当前目录下的所有 xlsx 文件"""
       # 查找当前目录下的所有 xlsx 文件
       xlsx_files = glob.glob("*.xlsx")
       
       if not xlsx_files:
           print("当前目录下未找到 xlsx 文件")
           return
       
       # 确保已安装必要的库
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
               return
       
       # 处理每个文件
       for xlsx_file in xlsx_files:
           try:
               xlsx_to_markdown(xlsx_file)
           except Exception as e:
               print(f"处理 {xlsx_file} 时出错: {e}")
   
   if __name__ == "__main__":
       main()
   ```

4. 输出到项目根目录下的`ocr_output`文件夹中，具体路径与输入相同。例如对于上面的情况，应该在`ocr_output`中也建立子文件夹：

   ```
   电力系统继电保护_page_47
   电力系统继电保护_page_48
   电力系统继电保护_page_49
   ```

   要将`PNG`对应的`txt`文件输出到同名的文件中，例如：

   ```
   19_table.txt
   ...
   ```







请你写一个python脚本，要求对特定的PNG文件进行OCR转换，具体逻辑如下：

1. 项目根目录下有一个文件夹`cutter_output`，存储着一些子文件夹，例如：

   ```
   电力系统继电保护_page_47
   电力系统继电保护_page_48
   电力系统继电保护_page_49
   ```

   每个子文件夹下都有一些`png`文件，例如：

   ```
   3_text.png
   4_equation.png
   ...
   ```

2. 需要使用`easyocr`库对每一个`text`类型的`png`文件进行OCR处理，示例代码如下：

   ```python
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
   ```

3. 输出到项目根目录下的`ocr_output`文件夹中，具体路径与输入相同。例如对于上面的情况，应该在`ocr_output`中也建立子文件夹：

   ```
   电力系统继电保护_page_47
   电力系统继电保护_page_48
   电力系统继电保护_page_49
   ```

   要将`PNG`对应的`txt`文件输出到同名的文件中，例如：

   ```
   3_text.txt
   ...
   ```

   注意：对于每一个`png`文件，OCR引擎的处理结果一定是一块一块的，请把它们连在一起，不要在输出结果中包含任何换行符。





请写一个python脚本，用于拼接文件，具体要求如下：

1. 项目根目录下有文件夹`ocr_output`，其中是一些子文件夹，例如：
   ```
   电力系统继电保护_page_47
   电力系统继电保护_page_48
   电力系统继电保护_page_49
   ```

   每个子文件夹里面都有一些`*.txt`文件，例如：
   ```
   1_header.txt
   2_header.txt
   3_text.txt
   4_equation.txt
   5_text.txt
   6_text.txt
   7_equation.txt
   8_text.txt
   ```
   

2. 我需要对于每个子文件夹里面的全部`*.txt`文件，按照顺序连接成一个完整的`*.txt`文件，输出到项目根目录下的`output_pages`文件夹中，例如：
   ```
   电力系统继电保护_page_47.txt
   电力系统继电保护_page_48.txt
   电力系统继电保护_page_49.txt
   ```

   