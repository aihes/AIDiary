#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
小红书图片生成器
--------------
生成适合小红书的图片，包括封面图、内容图等。
"""

import os
import random
import textwrap
from typing import List, Tuple, Optional, Dict, Any
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# 配置
OUTPUT_DIR = "output"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")

# 确保目录存在
os.makedirs(IMAGES_DIR, exist_ok=True)

class ImageGenerator:
    """小红书图片生成器"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # 尝试加载字体
        try:
            self.title_font = ImageFont.truetype("Arial.ttf", 80)
            self.subtitle_font = ImageFont.truetype("Arial.ttf", 40)
            self.body_font = ImageFont.truetype("Arial.ttf", 30)
        except IOError:
            # 使用默认字体
            self.title_font = ImageFont.load_default()
            self.subtitle_font = ImageFont.load_default()
            self.body_font = ImageFont.load_default()
    
    def generate_cover(self, title: str, subtitle: Optional[str] = None, 
                      style: str = "simple", output_path: Optional[str] = None) -> str:
        """生成封面图片"""
        # 设置图片尺寸和背景色
        width, height = 1080, 1440
        
        # 根据风格选择背景色
        if style == "simple":
            background_colors = [
                (255, 240, 245),  # 淡粉色
                (240, 248, 255),  # 爱丽丝蓝
                (245, 255, 250),  # 薄荷色
                (255, 250, 240),  # 花白色
                (240, 255, 240),  # 蜜瓜色
            ]
            bg_color = random.choice(background_colors)
        elif style == "gradient":
            # 渐变风格暂时使用纯色代替
            bg_color = (240, 240, 255)  # 淡蓝色
        else:
            bg_color = (255, 255, 255)  # 白色
        
        # 创建图片
        image = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(image)
        
        # 文本换行
        title_lines = textwrap.wrap(title, width=15)
        
        # 计算文本位置
        y_position = height // 3
        
        # 绘制标题
        for line in title_lines:
            # 获取文本宽度
            text_width = draw.textlength(line, font=self.title_font)
            position = ((width - text_width) // 2, y_position)
            
            # 绘制文本
            draw.text(position, line, fill=(0, 0, 0), font=self.title_font)
            y_position += 100
        
        # 绘制副标题
        if subtitle:
            subtitle_text = subtitle
        else:
            subtitle_text = "点击查看详情 👉"
        
        text_width = draw.textlength(subtitle_text, font=self.subtitle_font)
        position = ((width - text_width) // 2, height - 200)
        draw.text(position, subtitle_text, fill=(100, 100, 100), font=self.subtitle_font)
        
        # 保存图片
        if output_path is None:
            output_path = os.path.join(IMAGES_DIR, f"cover_{self.timestamp}.png")
        
        image.save(output_path)
        print(f"封面图片已保存至: {output_path}")
        
        return output_path
    
    def generate_content_image(self, title: str, content: List[str], 
                              style: str = "simple", output_path: Optional[str] = None) -> str:
        """生成内容图片"""
        # 设置图片尺寸和背景色
        width, height = 1080, 1920
        
        # 根据风格选择背景色
        if style == "simple":
            bg_color = (255, 255, 255)  # 白色
        elif style == "dark":
            bg_color = (30, 30, 30)  # 深色
        else:
            bg_color = (255, 255, 255)  # 默认白色
        
        # 根据风格选择文本颜色
        if style == "dark":
            text_color = (240, 240, 240)  # 浅色文本
            title_color = (255, 255, 255)  # 白色标题
        else:
            text_color = (50, 50, 50)  # 深色文本
            title_color = (0, 0, 0)  # 黑色标题
        
        # 创建图片
        image = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(image)
        
        # 绘制标题
        title_lines = textwrap.wrap(title, width=20)
        y_position = 100
        
        for line in title_lines:
            text_width = draw.textlength(line, font=self.title_font)
            position = ((width - text_width) // 2, y_position)
            draw.text(position, line, fill=title_color, font=self.title_font)
            y_position += 100
        
        y_position += 50  # 标题和内容之间的间距
        
        # 绘制内容
        for paragraph in content:
            lines = textwrap.wrap(paragraph, width=30)
            
            for line in lines:
                text_width = draw.textlength(line, font=self.body_font)
                position = ((width - text_width) // 2, y_position)
                draw.text(position, line, fill=text_color, font=self.body_font)
                y_position += 40
            
            y_position += 30  # 段落间距
        
        # 保存图片
        if output_path is None:
            output_path = os.path.join(IMAGES_DIR, f"content_{self.timestamp}.png")
        
        image.save(output_path)
        print(f"内容图片已保存至: {output_path}")
        
        return output_path
    
    def generate_list_image(self, title: str, items: List[str], 
                           style: str = "simple", output_path: Optional[str] = None) -> str:
        """生成列表图片"""
        # 设置图片尺寸和背景色
        width, height = 1080, 1920
        
        # 根据风格选择背景色和文本颜色
        if style == "simple":
            bg_color = (255, 255, 255)  # 白色
            text_color = (50, 50, 50)  # 深色文本
            title_color = (0, 0, 0)  # 黑色标题
            bullet_color = (255, 100, 100)  # 红色项目符号
        elif style == "dark":
            bg_color = (30, 30, 30)  # 深色
            text_color = (240, 240, 240)  # 浅色文本
            title_color = (255, 255, 255)  # 白色标题
            bullet_color = (100, 200, 255)  # 蓝色项目符号
        else:
            bg_color = (255, 255, 255)  # 默认白色
            text_color = (50, 50, 50)  # 深色文本
            title_color = (0, 0, 0)  # 黑色标题
            bullet_color = (255, 100, 100)  # 红色项目符号
        
        # 创建图片
        image = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(image)
        
        # 绘制标题
        title_lines = textwrap.wrap(title, width=20)
        y_position = 100
        
        for line in title_lines:
            text_width = draw.textlength(line, font=self.title_font)
            position = ((width - text_width) // 2, y_position)
            draw.text(position, line, fill=title_color, font=self.title_font)
            y_position += 100
        
        y_position += 50  # 标题和列表之间的间距
        
        # 绘制列表项
        for i, item in enumerate(items):
            # 绘制项目符号
            bullet = f"{i+1}."
            bullet_width = draw.textlength(bullet, font=self.body_font)
            bullet_position = (width // 6, y_position)
            draw.text(bullet_position, bullet, fill=bullet_color, font=self.body_font)
            
            # 绘制项目内容
            item_lines = textwrap.wrap(item, width=25)
            for j, line in enumerate(item_lines):
                # 第一行与项目符号对齐，后续行缩进
                if j == 0:
                    text_position = (width // 6 + bullet_width + 20, y_position)
                else:
                    text_position = (width // 6 + bullet_width + 20, y_position)
                
                draw.text(text_position, line, fill=text_color, font=self.body_font)
                y_position += 40
            
            y_position += 30  # 项目间距
        
        # 保存图片
        if output_path is None:
            output_path = os.path.join(IMAGES_DIR, f"list_{self.timestamp}.png")
        
        image.save(output_path)
        print(f"列表图片已保存至: {output_path}")
        
        return output_path
    
    def generate_quote_image(self, quote: str, author: Optional[str] = None, 
                            style: str = "simple", output_path: Optional[str] = None) -> str:
        """生成引用图片"""
        # 设置图片尺寸和背景色
        width, height = 1080, 1080
        
        # 根据风格选择背景色和文本颜色
        if style == "simple":
            bg_color = (255, 255, 255)  # 白色
            text_color = (50, 50, 50)  # 深色文本
            quote_color = (0, 0, 0)  # 黑色引用
        elif style == "elegant":
            bg_color = (245, 245, 245)  # 浅灰色
            text_color = (100, 100, 100)  # 灰色文本
            quote_color = (50, 50, 50)  # 深灰色引用
        else:
            bg_color = (255, 255, 255)  # 默认白色
            text_color = (50, 50, 50)  # 深色文本
            quote_color = (0, 0, 0)  # 黑色引用
        
        # 创建图片
        image = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(image)
        
        # 绘制引号
        quote_mark = "\""
        quote_mark_width = draw.textlength(quote_mark, font=self.title_font)
        quote_mark_position = (width // 6, height // 3 - 100)
        draw.text(quote_mark_position, quote_mark, fill=quote_color, font=self.title_font)
        
        # 绘制引用内容
        quote_lines = textwrap.wrap(quote, width=20)
        y_position = height // 3
        
        for line in quote_lines:
            text_width = draw.textlength(line, font=self.subtitle_font)
            position = ((width - text_width) // 2, y_position)
            draw.text(position, line, fill=quote_color, font=self.subtitle_font)
            y_position += 60
        
        # 绘制作者
        if author:
            author_text = f"— {author}"
            text_width = draw.textlength(author_text, font=self.body_font)
            position = ((width + text_width) // 2 - text_width, y_position + 50)
            draw.text(position, author_text, fill=text_color, font=self.body_font)
        
        # 保存图片
        if output_path is None:
            output_path = os.path.join(IMAGES_DIR, f"quote_{self.timestamp}.png")
        
        image.save(output_path)
        print(f"引用图片已保存至: {output_path}")
        
        return output_path
    
    def generate_image_set(self, post_data: Dict[str, Any]) -> List[str]:
        title = post_data["title"]
        content = post_data["content"]
        
        # 解析内容，提取段落和列表
        paragraphs = content.split("\n\n")
        
        # 生成图片列表
        image_paths = []
        
        # 生成封面
        cover_path = self.generate_cover(title)
        image_paths.append(cover_path)
        
        # 提取内容中的列表和段落
        lists = []
        quotes = []
        regular_paragraphs = []
        
        for paragraph in paragraphs:
            if paragraph.strip() == "":
                continue
            
            # 检查是否为列表（包含多个短行，每行以-或数字开头）
            lines = paragraph.split("\n")
            if len(lines) > 2 and all(line.strip().startswith(("-", "1", "2", "3", "4", "5", "6", "7", "8", "9")) for line in lines if line.strip()):
                lists.append(lines)
            # 检查是否为引用（较短且包含引号）
            elif len(paragraph) < 200 and ('"' in paragraph or '"' in paragraph or '"' in paragraph):
                quotes.append(paragraph)
            else:
                regular_paragraphs.append(paragraph)
        
        # 生成列表图片
        for list_items in lists[:2]:  # 最多生成2张列表图
            list_title = title
            list_path = self.generate_list_image(list_title, list_items)
            image_paths.append(list_path)
        
        # 生成引用图片
        for quote in quotes[:1]:  # 最多生成1张引用图
            quote_path = self.generate_quote_image(quote)
            image_paths.append(quote_path)
        
        # 生成内容图片
        if regular_paragraphs:
            content_chunks = []
            current_chunk = []
            current_length = 0
            
            for paragraph in regular_paragraphs:
                # 如果当前块加上新段落超过一定长度，创建新块
                if current_length + len(paragraph) > 500:
                    if current_chunk:
                        content_chunks.append(current_chunk)
                    current_chunk = [paragraph]
                    current_length = len(paragraph)
                else:
                    current_chunk.append(paragraph)
                    current_length += len(paragraph)
            
            # 添加最后一个块
            if current_chunk:
                content_chunks.append(current_chunk)
            
            # 为每个内容块生成图片
            for i, chunk in enumerate(content_chunks[:2]):  # 最多生成2张内容图
                content_title = title if i == 0 else f"{title} (续)"
                content_path = self.generate_content_image(content_title, chunk)
                image_paths.append(content_path)
        
        return image_paths

def main():
    # 创建图片生成器
    generator = ImageGenerator()
    
    # 示例：生成封面图片
    cover_path = generator.generate_cover("AI时代的10个必备技能，你掌握了几个？")
    
    # 示例：生成内容图片
    content_path = generator.generate_content_image(
        "AI时代的必备技能",
        [
            "随着人工智能技术的快速发展，未来的职场将发生巨大变化。",
            "掌握与AI协作的能力将成为核心竞争力。",
            "数据分析、批判性思维和创造性思维将比以往任何时候都更加重要。"
        ]
    )
    
    # 示例：生成列表图片
    list_path = generator.generate_list_image(
        "AI时代的10个必备技能",
        [
            "提示工程（Prompt Engineering）",
            "数据分析与可视化",
            "批判性思维",
            "创造性思维",
            "跨学科知识整合"
        ]
    )
    
    # 示例：生成引用图片
    quote_path = generator.generate_quote_image(
        "未来不属于担心AI会取代自己的人，而属于懂得如何与AI协作的人。",
        "艾贺"
    )
    
    print("\n生成的图片路径:")
    print(f"封面图片: {cover_path}")
    print(f"内容图片: {content_path}")
    print(f"列表图片: {list_path}")
    print(f"引用图片: {quote_path}")

if __name__ == "__main__":
    main()
