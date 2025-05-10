#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生成Self-RAG概念图
"""

import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

# 设置图片尺寸和背景色
width, height = 1080, 1920
bg_color = (255, 255, 255)  # 白色背景

# 创建图片
image = Image.new('RGB', (width, height), bg_color)
draw = ImageDraw.Draw(image)

# 尝试加载字体，如果失败则使用默认字体
try:
    title_font = ImageFont.truetype("Arial.ttf", 60)
    subtitle_font = ImageFont.truetype("Arial.ttf", 40)
    body_font = ImageFont.truetype("Arial.ttf", 30)
except IOError:
    # 使用默认字体
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    body_font = ImageFont.load_default()

# 绘制标题
title = "Self-RAG: 自反思检索增强生成"
title_width = draw.textlength(title, font=title_font)
title_position = ((width - title_width) // 2, 100)
draw.text(title_position, title, fill=(0, 0, 0), font=title_font)

# 绘制传统RAG部分
draw.text((100, 250), "传统RAG模式:", fill=(0, 0, 0), font=subtitle_font)

# 绘制传统RAG框图
box_start_y = 320
box_height = 300
draw.rectangle([(100, box_start_y), (width-100, box_start_y+box_height)], outline=(0, 0, 0), width=2)

# 绘制传统RAG内部组件
components = [
    "用户查询",
    "检索器 (固定次数检索)",
    "生成器 (不评估检索结果质量)",
    "最终回答"
]

component_y = box_start_y + 50
for component in components:
    draw.text((150, component_y), component, fill=(0, 0, 0), font=body_font)
    component_y += 60

# 绘制箭头
arrow_y = box_start_y + 30
for i in range(len(components)-1):
    draw.line([(width//2, arrow_y + i*60), (width//2, arrow_y + (i+1)*60)], fill=(0, 0, 0), width=2)
    draw.polygon([(width//2-10, arrow_y + (i+1)*60), (width//2+10, arrow_y + (i+1)*60), (width//2, arrow_y + (i+1)*60 + 10)], fill=(0, 0, 0))

# 绘制Self-RAG部分
draw.text((100, 700), "Self-RAG模式:", fill=(0, 0, 0), font=subtitle_font)

# 绘制Self-RAG框图
box_start_y = 770
box_height = 600
draw.rectangle([(100, box_start_y), (width-100, box_start_y+box_height)], outline=(0, 0, 0), width=2)

# 绘制Self-RAG内部组件
components = [
    "用户查询",
    "自我反思: 是否需要检索?",
    "检索器 (按需检索)",
    "自我反思: 检索结果是否相关?",
    "生成器",
    "自我反思: 生成内容是否有事实支持?",
    "自我反思: 整体回答质量如何?",
    "最终回答"
]

component_y = box_start_y + 50
for i, component in enumerate(components):
    if "自我反思" in component:
        draw.text((150, component_y), component, fill=(255, 0, 0), font=body_font)
    else:
        draw.text((150, component_y), component, fill=(0, 0, 0), font=body_font)
    component_y += 65

# 绘制箭头
arrow_y = box_start_y + 30
for i in range(len(components)-1):
    draw.line([(width//2, arrow_y + i*65), (width//2, arrow_y + (i+1)*65)], fill=(0, 0, 0), width=2)
    draw.polygon([(width//2-10, arrow_y + (i+1)*65), (width//2+10, arrow_y + (i+1)*65), (width//2, arrow_y + (i+1)*65 + 10)], fill=(0, 0, 0))

# 绘制Self-RAG优势
advantages_title = "Self-RAG核心优势:"
draw.text((100, 1400), advantages_title, fill=(0, 0, 0), font=subtitle_font)

advantages = [
    "1. 按需检索: 智能判断何时需要检索，提高效率",
    "2. 质量评估: 批判性评估检索结果和生成内容",
    "3. 灵活适应: 根据任务特点调整行为",
    "4. 可控性强: 通过反思标记控制生成过程"
]

advantage_y = 1470
for advantage in advantages:
    wrapped_text = textwrap.wrap(advantage, width=40)
    for line in wrapped_text:
        draw.text((120, advantage_y), line, fill=(0, 0, 0), font=body_font)
        advantage_y += 40
    advantage_y += 10

# 保存图片
output_path = "self_rag_concept.png"
image.save(output_path)
print(f"概念图已保存至: {output_path}")
