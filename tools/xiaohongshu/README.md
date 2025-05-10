# 小红书内容发布工具

这是一套用于生成和发布小红书内容的工具集，包括内容生成、图片生成和自动发布功能。

## 功能特点

- **内容生成**：自动生成小红书风格的标题、正文和标签
- **图片生成**：创建适合小红书的封面图和内容图
- **自动发布**：支持单篇发布和批量定时发布
- **灵活配置**：可自定义主题、风格和发布计划

## 目录结构

```
tools/xiaohongshu/
├── xhs_uploader.py       # 小红书上传核心脚本
├── content_generator.py  # 内容生成器
├── image_generator.py    # 图片生成器
├── batch_publisher.py    # 批量发布工具
├── output/               # 输出目录
│   ├── images/           # 生成的图片
│   └── content/          # 生成的内容
└── README.md             # 说明文档
```

## 使用方法

### 1. 单篇内容生成与发布

```bash
python content_generator.py
```

这将生成一篇关于AI工具的小红书帖子，并询问是否发布。

### 2. 批量生成发布计划

```bash
python batch_publisher.py schedule --topics "AI工具" "效率提升" "职场技能" --days 7 --posts-per-day 1
```

这将为指定主题生成7天的发布计划，每天1篇。

### 3. 执行发布计划

```bash
python batch_publisher.py run
```

这将按照之前生成的计划，在指定时间自动发布内容。

### 4. 立即发布多篇内容

```bash
python batch_publisher.py publish --topics "AI工具" "效率提升" --count 1
```

这将立即生成并发布指定主题的内容。

## 自定义图片生成

可以使用`image_generator.py`单独生成各种类型的图片：

```bash
python image_generator.py
```

这将生成示例封面图、内容图、列表图和引用图。

## 配置说明

- **IMGBB_API_KEY**：用于图片上传的imgBB API密钥
- **XHS_API_URL**：小红书发布API的端点
- **OUTPUT_DIR**：输出目录，默认为"output"

## 扩展开发

### 添加新的内容模板

在`content_generator.py`中的`generate_title`和`generate_content_structure`方法中添加新的模板。

### 添加新的图片风格

在`image_generator.py`中的各生成方法中添加新的风格选项。

### 自定义发布逻辑

修改`batch_publisher.py`中的调度逻辑，以适应特定的发布需求。

## 注意事项

- 请确保已安装所需的Python包：`pip install requests pillow pydantic schedule`
- 图片生成功能依赖PIL库，确保已正确安装
- 发布频率请遵循小红书平台规则，避免过于频繁的发布
- 建议在正式使用前，先测试内容生成效果
