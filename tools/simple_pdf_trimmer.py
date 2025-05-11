#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单PDF裁剪工具 - 保留指定页数
"""

import os
import sys
from PyPDF2 import PdfReader, PdfWriter

def trim_pdf(input_path, output_path, max_pages):
    """裁剪PDF文件，保留指定页数"""
    print(f"处理文件: {input_path}")
    print(f"将保留前 {max_pages} 页")
    
    # 读取输入PDF
    reader = PdfReader(input_path)
    
    # 获取页数
    total_pages = len(reader.pages)
    pages_to_keep = min(max_pages, total_pages)
    
    print(f"总页数: {total_pages}")
    print(f"将保留: {pages_to_keep} 页")
    
    # 创建一个新的PDF写入器
    writer = PdfWriter()
    
    # 添加要保留的页
    for page_num in range(pages_to_keep):
        writer.add_page(reader.pages[page_num])
    
    # 写入新的PDF
    with open(output_path, "wb") as output_file:
        writer.write(output_file)
    
    # 获取文件大小
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"输出文件: {output_path}")
    print(f"文件大小: {size_mb:.2f} MB")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python simple_pdf_trimmer.py <输入PDF路径> [输出PDF路径] [最大页数]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    # 设置输出路径
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        file_name, file_ext = os.path.splitext(input_path)
        output_path = f"{file_name}_trimmed{file_ext}"
    
    # 设置最大页数
    max_pages = 33
    if len(sys.argv) > 3:
        max_pages = int(sys.argv[3])
    
    # 裁剪PDF
    trim_pdf(input_path, output_path, max_pages)
