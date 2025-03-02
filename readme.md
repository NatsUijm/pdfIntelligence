# pdfIntelligence

这是一个可以将 PDF 转换为 TXT 文件的脚本组合。

每次运行前需删除全部文件夹，以及根目录下的\*.json和\*.pdf文件。

然后依次运行：

1. pdf2pic
2. paddle_structure(_mt)  // 后者对应多线程优化
3. png_cut
4. text_ocr(_mt)  // 后者对应多线程优化
5. text_concat
6. pdf_content_extract
7. txt_merge

运行环境方面，使用 3.11 版本 Python 安装 requirements.txt 的全部内容即可。