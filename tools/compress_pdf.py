#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF压缩工具 - 使用PyPDF2和压缩图像
"""

import os
import sys
import io
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image

def compress_pdf(input_path, output_path, max_pages=None, image_quality=30, max_size_mb=2.0):
    """
    压缩PDF文件，可选择保留指定页数
    
    Args:
        input_path: 输入PDF路径
        output_path: 输出PDF路径
        max_pages: 最大页数，None表示保留所有页
        image_quality: 图像压缩质量 (1-100)
        max_size_mb: 目标文件大小上限 (MB)
    """
    print(f"处理文件: {input_path}")
    
    # 读取输入PDF
    reader = PdfReader(input_path)
    
    # 获取页数
    total_pages = len(reader.pages)
    pages_to_keep = total_pages
    
    if max_pages is not None:
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
    print(f"裁剪后文件大小: {size_mb:.2f} MB")
    
    # 如果文件大小已经小于限制，直接返回
    if size_mb <= max_size_mb:
        print(f"文件大小已经小于 {max_size_mb} MB，无需进一步压缩")
        return True
    
    # 尝试使用更强的压缩
    print(f"文件大小超过 {max_size_mb} MB，尝试更强的压缩...")
    
    # 使用ghostscript进行压缩
    try:
        import subprocess
        
        # 构建ghostscript命令
        gs_command = [
            'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/screen',  # 最高压缩
            '-dNOPAUSE', '-dQUIET', '-dBATCH',
            f'-sOutputFile={output_path}.compressed',
            output_path
        ]
        
        # 执行命令
        subprocess.run(gs_command, check=True)
        
        # 如果压缩成功，替换原文件
        if os.path.exists(f"{output_path}.compressed"):
            os.remove(output_path)
            os.rename(f"{output_path}.compressed", output_path)
            
            # 获取压缩后的文件大小
            compressed_size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"压缩后文件大小: {compressed_size_mb:.2f} MB")
            
            if compressed_size_mb <= max_size_mb:
                print(f"文件已成功压缩到 {max_size_mb} MB 以下")
                return True
            else:
                print(f"警告: 即使使用最高压缩，文件大小仍然超过 {max_size_mb} MB")
                return True
    except Exception as e:
        print(f"使用ghostscript压缩时出错: {e}")
        print("尝试使用替代方法...")
    
    # 如果ghostscript失败，尝试减少页数
    if max_pages is not None:
        reduced_pages = int(pages_to_keep * 0.8)  # 减少20%的页数
        if reduced_pages < pages_to_keep:
            print(f"尝试减少页数到 {reduced_pages} 页...")
            return compress_pdf(input_path, output_path, reduced_pages, image_quality, max_size_mb)
    
    print(f"警告: 无法将文件压缩到 {max_size_mb} MB 以下")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python compress_pdf.py <输入PDF路径> [输出PDF路径] [最大页数] [最大大小MB]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    # 设置输出路径
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        file_name, file_ext = os.path.splitext(input_path)
        output_path = f"{file_name}_compressed{file_ext}"
    
    # 设置最大页数
    max_pages = 33
    if len(sys.argv) > 3:
        max_pages = int(sys.argv[3])
    
    # 设置最大大小
    max_size_mb = 2.0
    if len(sys.argv) > 4:
        max_size_mb = float(sys.argv[4])
    
    # 压缩PDF
    compress_pdf(input_path, output_path, max_pages, 30, max_size_mb)
