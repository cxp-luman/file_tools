import os
import re
from PyPDF2 import PdfMerger, PdfReader

def merge_pdfs(directory):
    merger = PdfMerger()
    digit_pdf_files = []
    not_digit_pdf_files = []
    # 遍历目录
    for root, dirs, files in os.walk(directory):
        if len(files) == 0:
            continue
        # 分类文件
        for file in files:
            if file.endswith('.pdf'):
                if not str(file.split('|')[0]).isdigit() and not str(file.split('丨')[0]).isdigit():
                    not_digit_pdf_files.append(root+'/'+file)
                else:
                    digit_pdf_files.append(root+'/'+file)
    # 按文件名前数字升序合并pdf文件
    digit_pdf_files.sort(key=lambda x: int(re.match(r'(\d+)', x.split('/')[-1]).group(1)))
    digit_pdf_files.extend(not_digit_pdf_files)
    page_num = 0
    for pdf_file in digit_pdf_files:
        print(pdf_file)
        pdf = PdfReader(pdf_file)
        merger.append(pdf)
        merger.add_outline_item(pdf_file.split('/')[-1][:-4], page_num)  # 去除.pdf后缀作为书签
        page_num += len(pdf.pages)
        merge_pdf_name = directory.split('/')[-1]
    merged_pdf_path = os.path.join(directory, f'{merge_pdf_name}.pdf')
    # merger.add_metadata({'/Title': merged_pdf_path})  # 设置合并后的pdf文件标题
    merger.write(merged_pdf_path)
    merger.close()

# 测试
directory = '/home/luman/文档/01-数据结构与算法之美'
merge_pdfs(directory)
