import json
import os
import glob
import re

def main():
    # 1. 读取JSON文件
    json_files = glob.glob("*.json")
    if not json_files:
        print("错误：未找到JSON文件")
        return
    
    json_file = json_files[0]  # 获取唯一的JSON文件
    
    with open(json_file, 'r', encoding='utf-8') as f:
        directory = json.load(f)
    
    # 2. 找出最低等级(level最大值)
    max_level = max(item["level"] for item in directory)
    
    # 3. 过滤出最低等级的条目
    filtered_directory = [item for item in directory if item["level"] == max_level]
    
    # 4. 获取所有txt文件并排序
    txt_files = glob.glob("output_pages/*.txt")
    # 使用正则表达式提取页码并按数字排序
    page_pattern = re.compile(r'.*_page_(\d+)\.txt$')
    txt_files_dict = {}
    
    for file in txt_files:
        match = page_pattern.match(file)
        if match:
            page_num = int(match.group(1))
            txt_files_dict[page_num] = file
    
    # 获取最大页码
    max_page = max(txt_files_dict.keys()) if txt_files_dict else 0
    
    # 5. 处理每个目录条目
    for i, item in enumerate(filtered_directory):
        title = item["title"]
        page_start = item["page"]
        
        # 获取下一条目的页码作为结束页码
        if i < len(filtered_directory) - 1:
            page_end = filtered_directory[i + 1]["page"] - 1
        else:
            page_end = max_page
        
        # 安全文件名处理
        safe_title = re.sub(r'[\\/*?:"<>|]', '_', title)
        output_file = f"{safe_title}.txt"
        
        # 合并文件
        merge_files(page_start, page_end, txt_files_dict, output_file)
        print(f"已合并页码 {page_start} 到 {page_end} 的内容到文件: {output_file}")

def merge_files(start_page, end_page, files_dict, output_file):
    """合并指定页码范围内的文件"""
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for page_num in range(start_page, end_page + 1):
            if page_num in files_dict:
                file_path = files_dict[page_num]
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content)
                        # 如果文件内容不以换行符结束，添加一个换行符
                        if content and not content.endswith('\n'):
                            outfile.write('\n')
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")
            else:
                print(f"警告: 未找到页码为 {page_num} 的文件")

if __name__ == "__main__":
    main()