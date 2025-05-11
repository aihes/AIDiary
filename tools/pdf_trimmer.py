#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF裁剪工具 - 保留指定页数并控制文件大小
"""

import os
import sys
import argparse
from PyPDF2 import PdfReader, PdfWriter
import subprocess

def get_pdf_size_mb(file_path):
    """获取PDF文件大小（MB）"""
    return os.path.getsize(file_path) / (1024 * 1024)

def compress_pdf(input_path, output_path, compression_level=2):
    """使用Ghostscript压缩PDF文件
    
    压缩级别:
    0 - 默认
    1 - 预压缩
    2 - 高压缩
    3 - 最高压缩
    """
    # 检查是否安装了Ghostscript
    try:
        subprocess.run(['gs', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("警告: Ghostscript未安装，无法进行压缩。请安装Ghostscript后重试。")
        return False
    
    quality = {
        0: '/default',
        1: '/prepress',
        2: '/ebook',
        3: '/screen'
    }
    
    # 构建Ghostscript命令
    gs_command = [
        'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS={quality[compression_level]}',
        '-dNOPAUSE', '-dQUIET', '-dBATCH',
        f'-sOutputFile={output_path}',
        input_path
    ]
    
    try:
        subprocess.run(gs_command, check=True)
        return True
    except subprocess.SubprocessError as e:
        print(f"压缩PDF时出错: {e}")
        return False

def trim_pdf(input_path, output_path, max_pages, max_size_mb=2, compression_attempts=3):
    """裁剪PDF文件，保留指定页数并控制文件大小"""
    # 读取输入PDF
    try:
        reader = PdfReader(input_path)
    except Exception as e:
        print(f"读取PDF文件时出错: {e}")
        return False
    
    # 获取页数
    total_pages = len(reader.pages)
    pages_to_keep = min(max_pages, total_pages)
    
    print(f"原始PDF: {input_path}")
    print(f"总页数: {total_pages}")
    print(f"将保留前 {pages_to_keep} 页")
    
    # 创建一个新的PDF写入器
    writer = PdfWriter()
    
    # 添加要保留的页
    for page_num in range(pages_to_keep):
        writer.add_page(reader.pages[page_num])
    
    # 创建临时文件
    temp_output = f"{output_path}.temp.pdf"
    
    # 写入新的PDF
    try:
        with open(temp_output, "wb") as output_file:
            writer.write(output_file)
    except Exception as e:
        print(f"写入PDF文件时出错: {e}")
        if os.path.exists(temp_output):
            os.remove(temp_output)
        return False
    
    # 检查文件大小
    current_size = get_pdf_size_mb(temp_output)
    print(f"裁剪后大小: {current_size:.2f} MB")
    
    # 如果文件大小已经小于限制，直接重命名
    if current_size <= max_size_mb:
        os.rename(temp_output, output_path)
        print(f"文件已裁剪并保存为: {output_path}")
        return True
    
    # 尝试压缩
    print(f"文件大小超过 {max_size_mb} MB，尝试压缩...")
    
    # 尝试不同级别的压缩
    for level in range(compression_attempts):
        print(f"尝试压缩级别 {level+1}/{compression_attempts}...")
        
        if compress_pdf(temp_output, output_path, level+1):
            compressed_size = get_pdf_size_mb(output_path)
            print(f"压缩后大小: {compressed_size:.2f} MB")
            
            if compressed_size <= max_size_mb:
                print(f"文件已裁剪、压缩并保存为: {output_path}")
                os.remove(temp_output)
                return True
    
    # 如果所有压缩尝试都失败，使用最后一次压缩的结果
    if os.path.exists(output_path):
        final_size = get_pdf_size_mb(output_path)
        print(f"警告: 无法将文件压缩到 {max_size_mb} MB 以下。")
        print(f"最终文件大小: {final_size:.2f} MB")
        os.remove(temp_output)
        return True
    else:
        # 如果压缩完全失败，使用未压缩的版本
        os.rename(temp_output, output_path)
        print(f"警告: 压缩失败，使用未压缩的裁剪版本。")
        print(f"最终文件大小: {current_size:.2f} MB")
        return True

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="PDF裁剪工具 - 保留指定页数并控制文件大小")
    parser.add_argument("input_pdf", help="输入PDF文件路径")
    parser.add_argument("--output", "-o", help="输出PDF文件路径 (默认为添加_trimmed后缀)")
    parser.add_argument("--pages", "-p", type=int, default=33, help="要保留的最大页数 (默认: 33)")
    parser.add_argument("--size", "-s", type=float, default=2.0, help="目标文件大小上限，单位MB (默认: 2.0)")
    
    args = parser.parse_args()
    
    # 检查输入文件是否存在
    if not os.path.exists(args.input_pdf):
        print(f"错误: 输入文件 '{args.input_pdf}' 不存在")
        return 1
    
    # 设置输出文件路径
    if args.output:
        output_path = args.output
    else:
        # 在文件名中添加_trimmed后缀
        file_name, file_ext = os.path.splitext(args.input_pdf)
        output_path = f"{file_name}_trimmed{file_ext}"
    
    # 裁剪PDF
    success = trim_pdf(args.input_pdf, output_path, args.pages, args.size)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
