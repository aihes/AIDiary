#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
小红书批量发布工具
----------------
批量生成和发布小红书内容，支持定时发布和主题批量生成。
"""

import os
import json
import time
import random
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Any
import schedule

# 导入内容生成器和上传脚本
from content_generator import ContentGenerator
from xhs_uploader import process_and_send_to_xiaohongshu

class BatchPublisher:
    """小红书批量发布工具"""
    
    def __init__(self):
        self.generator = ContentGenerator()
        self.scheduled_posts = []
    
    def generate_batch(self, topics: List[str], count_per_topic: int = 1) -> List[Dict[str, Any]]:
        """批量生成内容"""
        posts = []
        
        for topic in topics:
            for _ in range(count_per_topic):
                # 随机选择标题风格
                title_style = random.choice(["问题型", "数字型", "干货型"])
                
                # 随机选择章节数
                sections = random.randint(3, 5)
                
                # 生成帖子
                post = self.generator.generate_post(topic, title_style, sections)
                posts.append(post)
                
                # 随机暂停，避免生成过快
                time.sleep(random.uniform(0.5, 2.0))
        
        return posts
    
    def schedule_post(self, post: Dict[str, Any], publish_time: datetime) -> None:
        """安排帖子在指定时间发布"""
        scheduled_info = {
            "post": post,
            "publish_time": publish_time,
            "status": "scheduled"
        }
        
        self.scheduled_posts.append(scheduled_info)
        
        # 格式化时间
        time_str = publish_time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"帖子《{post['title']}》已安排在 {time_str} 发布")
    
    def publish_scheduled_post(self, scheduled_info: Dict[str, Any]) -> None:
        """发布已安排的帖子"""
        post = scheduled_info["post"]
        
        try:
            # 发布帖子
            self.generator.publish_post(post)
            
            # 更新状态
            scheduled_info["status"] = "published"
            scheduled_info["published_time"] = datetime.now()
            
            print(f"帖子《{post['title']}》已成功发布")
        except Exception as e:
            # 更新状态
            scheduled_info["status"] = "failed"
            scheduled_info["error"] = str(e)
            
            print(f"帖子《{post['title']}》发布失败: {str(e)}")
    
    def check_scheduled_posts(self) -> None:
        """检查并发布已安排的帖子"""
        now = datetime.now()
        
        for scheduled_info in self.scheduled_posts:
            # 只处理状态为scheduled的帖子
            if scheduled_info["status"] != "scheduled":
                continue
            
            # 检查是否到达发布时间
            if now >= scheduled_info["publish_time"]:
                self.publish_scheduled_post(scheduled_info)
    
    def generate_schedule(self, topics: List[str], days: int = 7, posts_per_day: int = 1, 
                         start_hour: int = 9, end_hour: int = 21) -> None:
        """生成发布计划"""
        # 计算总帖子数
        total_posts = days * posts_per_day
        
        # 确保有足够的主题
        if len(topics) * 3 < total_posts:  # 假设每个主题最多生成3篇不同的帖子
            # 复制主题列表以满足需求
            topics = topics * (total_posts // len(topics) + 1)
        
        # 随机打乱主题顺序
        random.shuffle(topics)
        
        # 生成帖子
        posts = self.generate_batch(topics[:total_posts], 1)
        
        # 生成发布时间
        now = datetime.now()
        start_date = now.date()
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            for post_index in range(posts_per_day):
                if day * posts_per_day + post_index >= len(posts):
                    break
                
                # 随机选择发布时间
                hour = random.randint(start_hour, end_hour)
                minute = random.randint(0, 59)
                
                publish_time = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=hour, minutes=minute)
                
                # 如果发布时间已经过去，则安排在明天同一时间
                if publish_time < now:
                    publish_time += timedelta(days=1)
                
                # 安排发布
                self.schedule_post(posts[day * posts_per_day + post_index], publish_time)
        
        # 保存发布计划
        self.save_schedule()
    
    def save_schedule(self) -> None:
        """保存发布计划到文件"""
        # 准备数据
        schedule_data = []
        for scheduled_info in self.scheduled_posts:
            # 复制数据，避免修改原始数据
            info = scheduled_info.copy()
            
            # 转换datetime对象为字符串
            info["publish_time"] = info["publish_time"].strftime("%Y-%m-%d %H:%M:%S")
            if "published_time" in info:
                info["published_time"] = info["published_time"].strftime("%Y-%m-%d %H:%M:%S")
            
            schedule_data.append(info)
        
        # 文件路径
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schedule.json")
        
        # 保存到文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(schedule_data, f, ensure_ascii=False, indent=2)
        
        print(f"发布计划已保存至: {file_path}")
    
    def load_schedule(self) -> None:
        """从文件加载发布计划"""
        # 文件路径
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schedule.json")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"发布计划文件不存在: {file_path}")
            return
        
        try:
            # 从文件加载数据
            with open(file_path, 'r', encoding='utf-8') as f:
                schedule_data = json.load(f)
            
            # 转换数据
            self.scheduled_posts = []
            for info in schedule_data:
                # 转换字符串为datetime对象
                info["publish_time"] = datetime.strptime(info["publish_time"], "%Y-%m-%d %H:%M:%S")
                if "published_time" in info:
                    info["published_time"] = datetime.strptime(info["published_time"], "%Y-%m-%d %H:%M:%S")
                
                self.scheduled_posts.append(info)
            
            print(f"已加载 {len(self.scheduled_posts)} 个发布计划")
        except Exception as e:
            print(f"加载发布计划失败: {str(e)}")
    
    def run_scheduler(self) -> None:
        """运行定时任务"""
        # 每分钟检查一次
        schedule.every(1).minutes.do(self.check_scheduled_posts)
        
        print("定时任务已启动，按 Ctrl+C 停止")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("定时任务已停止")

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="小红书批量发布工具")
    
    # 添加子命令
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 生成计划子命令
    schedule_parser = subparsers.add_parser("schedule", help="生成发布计划")
    schedule_parser.add_argument("--topics", nargs="+", required=True, help="主题列表")
    schedule_parser.add_argument("--days", type=int, default=7, help="计划天数")
    schedule_parser.add_argument("--posts-per-day", type=int, default=1, help="每天发布数量")
    schedule_parser.add_argument("--start-hour", type=int, default=9, help="发布开始时间（小时）")
    schedule_parser.add_argument("--end-hour", type=int, default=21, help="发布结束时间（小时）")
    
    # 运行计划子命令
    run_parser = subparsers.add_parser("run", help="运行发布计划")
    
    # 立即发布子命令
    publish_parser = subparsers.add_parser("publish", help="立即发布")
    publish_parser.add_argument("--topics", nargs="+", required=True, help="主题列表")
    publish_parser.add_argument("--count", type=int, default=1, help="每个主题的发布数量")
    
    # 解析参数
    args = parser.parse_args()
    
    # 创建发布器
    publisher = BatchPublisher()
    
    # 处理命令
    if args.command == "schedule":
        publisher.generate_schedule(args.topics, args.days, args.posts_per_day, args.start_hour, args.end_hour)
    elif args.command == "run":
        publisher.load_schedule()
        publisher.run_scheduler()
    elif args.command == "publish":
        posts = publisher.generate_batch(args.topics, args.count)
        for post in posts:
            publisher.generator.publish_post(post)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
