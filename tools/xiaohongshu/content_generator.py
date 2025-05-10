#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
小红书内容生成器
---------------
生成小红书内容，包括标题、正文、标签等，并可以调用上传脚本发布到小红书。
"""

import os
import json
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap

# 导入上传脚本
from xhs_uploader import process_and_send_to_xiaohongshu

# 配置
OUTPUT_DIR = "output"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
CONTENT_DIR = os.path.join(OUTPUT_DIR, "content")

# 确保目录存在
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(CONTENT_DIR, exist_ok=True)

# 常用标签库
COMMON_TAGS = {
    "技术": ["AI", "大模型", "技术", "程序员", "算法", "编程", "开发", "Python", "数据", "工具"],
    "效率": ["效率", "干货", "工作", "职场", "生产力", "时间管理", "工具", "自我提升"],
    "产品": ["产品", "设计", "用户体验", "产品经理", "交互", "创新", "用户研究"],
    "创业": ["创业", "商业", "营销", "增长", "策略", "团队", "管理", "领导力"]
}

class ContentGenerator:
    """小红书内容生成器"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    def generate_title(self, topic: str, style: str = "问题型") -> str:
        """生成标题"""
        styles = {
            "问题型": [
                f"{topic}怎么做才能事半功倍？",
                f"{topic}到底有什么用？工作中这样用超高效",
                f"{topic}真的有必要学吗？看完你就懂了",
                f"为什么{topic}这么火？3分钟带你看懂",
                f"{topic}到底难不难？新手也能快速上手"
            ],
            "数字型": [
                f"{topic}入门指南：新手必备{random.randint(3, 7)}个技巧",
                f"{random.randint(3, 10)}个{topic}实用技巧，第{random.randint(3, 5)}个太赞了",
                f"掌握这{random.randint(3, 7)}点，轻松玩转{topic}",
                f"{random.randint(2023, 2025)}年最值得学的{random.randint(3, 7)}个{topic}技能",
                f"{topic}高手都在用的{random.randint(3, 7)}个秘诀"
            ],
            "干货型": [
                f"{topic}完全指南：从入门到精通",
                f"一文掌握{topic}核心技能，建议收藏",
                f"{topic}实战技巧大全，工作效率翻倍",
                f"深度解析：{topic}背后的核心原理",
                f"{topic}最佳实践：来自一线大厂的经验总结"
            ]
        }
        
        return random.choice(styles.get(style, styles["问题型"]))
    
    def generate_content_structure(self, topic: str, sections: int = 4) -> Dict[str, Any]:
        """生成内容结构"""
        intro = f"作为{topic}领域的从业者，我总结了一些实用经验分享给大家。"
        
        section_titles = [
            "核心概念解析", "常见误区", "实用技巧", "进阶方法", 
            "案例分析", "工具推荐", "学习路径", "未来趋势"
        ]
        
        # 随机选择几个章节
        selected_sections = random.sample(section_titles, min(sections, len(section_titles)))
        
        structure = {
            "intro": intro,
            "sections": []
        }
        
        # 为每个章节生成内容
        for section in selected_sections:
            section_content = {
                "title": section,
                "points": []
            }
            
            # 每个章节3-5个要点
            for _ in range(random.randint(3, 5)):
                section_content["points"].append(f"{topic}相关的要点")
            
            structure["sections"].append(section_content)
        
        # 结尾
        structure["conclusion"] = f"以上就是关于{topic}的一些分享，希望对你有所帮助。如果你有其他问题，欢迎在评论区交流！"
        
        return structure
    
    def format_content(self, structure: Dict[str, Any]) -> str:
        """格式化内容为小红书风格"""
        content = structure["intro"] + "\n\n"
        
        # 添加表情符号库
        emojis = ["✨", "🔥", "💡", "📚", "🚀", "⭐", "📌", "🔍", "💪", "👉", "🌟", "📝", "🎯", "🔧", "📊"]
        
        # 添加章节
        for i, section in enumerate(structure["sections"]):
            # 随机选择表情
            emoji = random.choice(emojis)
            content += f"{emoji}【{section['title']}】\n"
            
            # 添加要点
            for j, point in enumerate(section["points"]):
                if random.random() > 0.5:  # 随机使用不同的列表样式
                    content += f"- {point}\n"
                else:
                    content += f"{j+1}. {point}\n"
            
            content += "\n"
        
        # 添加结尾
        content += structure["conclusion"]
        
        return content
    
    def generate_tags(self, topic: str, count: int = 7) -> List[str]:
        """生成标签"""
        # 基于主题选择相关标签类别
        topic_lower = topic.lower()
        
        # 确定主要类别
        if any(keyword in topic_lower for keyword in ["ai", "算法", "编程", "开发", "数据"]):
            primary_category = "技术"
        elif any(keyword in topic_lower for keyword in ["效率", "工作", "时间"]):
            primary_category = "效率"
        elif any(keyword in topic_lower for keyword in ["产品", "设计", "用户"]):
            primary_category = "产品"
        elif any(keyword in topic_lower for keyword in ["创业", "商业", "营销"]):
            primary_category = "创业"
        else:
            primary_category = random.choice(list(COMMON_TAGS.keys()))
        
        # 从主要类别中选择标签
        tags = random.sample(COMMON_TAGS[primary_category], min(4, len(COMMON_TAGS[primary_category])))
        
        # 从其他类别中补充标签
        other_categories = [cat for cat in COMMON_TAGS.keys() if cat != primary_category]
        for category in random.sample(other_categories, min(2, len(other_categories))):
            tags.extend(random.sample(COMMON_TAGS[category], min(2, len(COMMON_TAGS[category]))))
        
        # 确保有主题标签
        if topic not in tags:
            tags.append(topic)
        
        # 去重并限制数量
        tags = list(set(tags))[:count]
        
        return tags
    
    def generate_cover_image(self, title: str, output_path: Optional[str] = None) -> str:
        """生成封面图片"""
        # 设置图片尺寸和背景色
        width, height = 1080, 1440
        background_colors = [
            (255, 240, 245),  # 淡粉色
            (240, 248, 255),  # 爱丽丝蓝
            (245, 255, 250),  # 薄荷色
            (255, 250, 240),  # 花白色
            (240, 255, 240),  # 蜜瓜色
        ]
        bg_color = random.choice(background_colors)
        
        # 创建图片
        image = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(image)
        
        try:
            # 尝试加载字体，如果失败则使用默认字体
            title_font = ImageFont.truetype("Arial.ttf", 80)
            subtitle_font = ImageFont.truetype("Arial.ttf", 40)
        except IOError:
            # 使用默认字体
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # 文本换行
        title_lines = textwrap.wrap(title, width=15)
        
        # 计算文本位置
        y_position = height // 3
        
        # 绘制标题
        for line in title_lines:
            # 获取文本宽度
            text_width = draw.textlength(line, font=title_font)
            position = ((width - text_width) // 2, y_position)
            
            # 绘制文本
            draw.text(position, line, fill=(0, 0, 0), font=title_font)
            y_position += 100
        
        # 绘制副标题
        subtitle = "点击查看详情 👉"
        text_width = draw.textlength(subtitle, font=subtitle_font)
        position = ((width - text_width) // 2, height - 200)
        draw.text(position, subtitle, fill=(100, 100, 100), font=subtitle_font)
        
        # 保存图片
        if output_path is None:
            output_path = os.path.join(IMAGES_DIR, f"cover_{self.timestamp}.png")
        
        image.save(output_path)
        print(f"封面图片已保存至: {output_path}")
        
        return output_path
    
    def generate_post(self, topic: str, title_style: str = "问题型", sections: int = 4) -> Dict[str, Any]:
        """生成完整的小红书帖子"""
        # 生成标题
        title = self.generate_title(topic, title_style)
        
        # 生成内容结构
        structure = self.generate_content_structure(topic, sections)
        
        # 格式化内容
        content = self.format_content(structure)
        
        # 生成标签
        tags = self.generate_tags(topic)
        
        # 生成封面图片
        cover_image_path = self.generate_cover_image(title)
        
        # 组装帖子数据
        post = {
            "title": title,
            "content": content,
            "tags": tags,
            "images": [cover_image_path],
            "timestamp": self.timestamp
        }
        
        # 保存帖子数据
        self.save_post(post)
        
        return post
    
    def save_post(self, post: Dict[str, Any]) -> None:
        """保存帖子数据到文件"""
        # 复制一份数据，避免修改原始数据
        post_data = post.copy()
        
        # 文件路径
        file_path = os.path.join(CONTENT_DIR, f"post_{self.timestamp}.json")
        
        # 保存到文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(post_data, f, ensure_ascii=False, indent=2)
        
        print(f"帖子数据已保存至: {file_path}")
    
    def publish_post(self, post: Dict[str, Any]) -> None:
        """发布帖子到小红书"""
        title = post["title"]
        content = post["content"]
        tags = post["tags"]
        image_paths = post["images"]
        
        # 调用上传脚本
        process_and_send_to_xiaohongshu(title, content, image_paths, tags)
        
        print(f"帖子《{title}》已提交发布")

def main():
    """主函数"""
    # 创建内容生成器
    generator = ContentGenerator()
    
    # 示例：生成一篇关于AI的帖子
    topic = "AI工具"
    post = generator.generate_post(topic, title_style="数字型", sections=4)
    
    # 打印生成的内容
    print("\n" + "="*50)
    print(f"标题: {post['title']}")
    print("-"*50)
    print(f"内容:\n{post['content']}")
    print("-"*50)
    print(f"标签: {', '.join(post['tags'])}")
    print(f"图片: {post['images']}")
    print("="*50)
    
    # 询问是否发布
    answer = input("\n是否发布到小红书? (y/n): ")
    if answer.lower() == 'y':
        generator.publish_post(post)

if __name__ == "__main__":
    main()
