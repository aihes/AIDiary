import os
import requests
import json
import uuid
import time
from typing import List
from pydantic import BaseModel, HttpUrl

# 你的 imgBB API 密钥
IMGBB_API_KEY = "676fe62bdaa7db84e5bbec40f05d9ca9"

# 小红书的 API 端点
XHS_API_URL = "https://ngrok.aihe.space/send_xiaohongshu"

def upload_image_to_imgbb(image_path: str) -> str:
    """Upload image to imgBB and return the URL"""
    url = "https://api.imgbb.com/1/upload"
    
    # Open the image file
    with open(image_path, 'rb') as image_file:
        files = {'image': image_file}
        params = {'key': IMGBB_API_KEY}
        
        # Send the POST request to upload the image
        response = requests.post(url, files=files, data=params)
        
        if response.status_code == 200:
            # Parse the response to get the image URL
            response_data = response.json()
            image_url = response_data['data']['url']
            return image_url
        else:
            raise Exception(f"Error uploading image to imgBB: {response.text}")

class XiaoHongShuRequest(BaseModel):
    title: str
    content: str
    is_image_upload: bool = True
    image_urls: List[HttpUrl]
    tags: List[str] = []

def send_to_xiaohongshu(request: XiaoHongShuRequest, max_retries=5, initial_delay=1):
    """Send data to XiaoHongShu API with retry mechanism"""
    # Convert HttpUrl objects to strings for JSON serialization
    payload = request.model_dump()
    payload['image_urls'] = [str(url) for url in payload['image_urls']]
    
    print("Sending payload:", json.dumps(payload, indent=2))
    
    headers = {"Content-Type": "application/json"}
    
    delay = initial_delay
    for attempt in range(max_retries):
        # Send the POST request to the XiaoHongShu API
        response = requests.post(XHS_API_URL, data=json.dumps(payload), headers=headers)
        
        if response.status_code == 200:
            print("Successfully sent to XiaoHongShu.")
            print("Response:", response.json())
            return True
        elif response.status_code == 423:  # Resource is locked
            if attempt < max_retries - 1:
                print(f"Another task is running. Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print("Max retries reached. Failed to send to XiaoHongShu.")
                print("Error:", response.text)
                return False
        else:
            print(f"Failed to send to XiaoHongShu. Status code: {response.status_code}")
            print("Error:", response.text)
            return False

def process_images_and_send_to_xiaohongshu(image_directory: str, title: str, content: str, tags: List[str] = []):
    """Process images in the directory, upload them to imgBB, and send to XiaoHongShu"""
    image_urls = []
    
    # Loop through all the image files in the directory
    for filename in os.listdir(image_directory):
        if filename.lower().endswith(('jpg', 'jpeg', 'png')):
            image_path = os.path.join(image_directory, filename)
            
            # Upload the image to imgBB
            try:
                print(f"Uploading {filename} to imgBB...")
                image_url = upload_image_to_imgbb(image_path)
                image_urls.append(image_url)
                print(f"Uploaded {filename} to imgBB. Image URL: {image_url}")
            except Exception as e:
                print(f"Failed to upload {filename}: {str(e)}")
    
    if image_urls:
        # Create XiaoHongShuRequest object
        request = XiaoHongShuRequest(
            title=title,
            content=content,
            image_urls=image_urls,
            tags=tags
        )
        # Send the data to XiaoHongShu
        send_to_xiaohongshu(request)
    else:
        print("No images to upload to XiaoHongShu.")

def process_and_send_to_xiaohongshu(title: str, content: str, image_urls: List[str], tags: List[str] = []):
    """Process image URLs (mix of local paths and HTTP URLs) and send to XiaoHongShu"""
    processed_urls = []
    
    for url in image_urls:
        # Check if the URL is already an HTTP(S) URL
        if url.lower().startswith(('http://', 'https://')):
            processed_urls.append(url)
        else:
            # Treat as local file path and upload
            try:
                print(f"Uploading {url} to imgBB...")
                image_url = upload_image_to_imgbb(url)
                processed_urls.append(image_url)
                print(f"Uploaded to imgBB. Image URL: {image_url}")
            except Exception as e:
                print(f"Failed to upload {url}: {str(e)}")
    
    if processed_urls:
        # Create XiaoHongShuRequest object
        request = XiaoHongShuRequest(
            title=title,
            content=content,
            image_urls=processed_urls,
            tags=tags
        )
        # Send the data to XiaoHongShu
        send_to_xiaohongshu(request)
    else:
        print("No images to process for XiaoHongShu.")

if __name__ == "__main__":
    # Example usage
#     {
#   "title": "大模型部署的三种姿势，你用对了吗？",
#   "content": "",
#   "tags": ["AI", "大模型", "干货", "DeepSeek", "效率", "技术", "程序员", "算力"]
# }
# {
#   "title": "AI终于连外部工具？这个协议要火！",
#   "content": "🔥最近爆火的Model Context Protocol（MCP），可能是让AI真正实用的革命性技术！作为AI领域从业者，我连夜拆解了这个协议的核心价值👇\n\n💡【MCP是什么】\n- 由Anthropic推出的开放标准\n- 相当于AI界的万能转接头\n- 让AI助手直连你的数据库/代码库/办公软件\n\n🚫【传统AI的致命伤】\n原来自家AI不知道：\n✓ 公司最新销售数据\n✓ 私有代码库内容\n✓ 内部知识文档\n因为每个工具都要单独做插件，维护成本爆炸！\n\n✨【MCP三大突破】\n1️⃣ 统一接口标准：像USB-C一样即插即用\n2️⃣ 实时数据调用：直接读取你的工作场景数据\n3️⃣ 安全边界控制：权限由用户完全掌控\n\n🛠️【技术人看门道】\n▸ 采用客户端-服务器架构\n▸ 底层逻辑类似REST API革命\n▸ 开发一次就能对接所有AI平台\n\n💼【落地案例】\n- Block用MCP连接财务数据库\n- Apollo集成内部知识库\n- Zed/Replit让编程助手读代码\n\n🌟【未来趋势】\n✔️ AI回复不再泛泛而谈\n✔️ 企业级AI应用门槛降低\n✔️ 开发者不用重复造轮子\n\n作为AI产品经理，我认为这协议将掀起新一波生产力革命。建议开发者优先学习MCP文档，普通用户关注支持该协议的工具更新。你的工作场景最需要AI连接什么工具？评论区聊聊～",
#   "is_image_upload": true,
#   "image_urls": [
#     "https://devgo.fun/static/render_1744158792.png",
#   ],
#   "tags": [
#     "AI",
#     "工具",
#     "干货",
#     "效率",
#     "科技",
#     "开发",
#     "数据"
#   ]
# }
    data = {
  "title": "AI总胡说八道？4招根治大模型幻觉",
  "content": "当AI给出看似合理实则虚构的回答时，会引发严重后果。最近整理了破解大模型幻觉问题的核心技术方案，用MECE法则拆解成四大层次：\n\n🔥【源头|输入把关】\n- 数据：喂料就要用真实、多样、去偏见的优质语料\n- 提问：要求「说明数据来源」「不确定时不要脑补」的Prompt句式\n\n🧠【内核|模型调教】\n- RLHF强化学习：用人类反馈教AI分辨回答质量\n- 植入不确定性检测：训练AI主动说「我不知道」（直接减少60%以上幻觉）\n\n🛠️【工具|实时开卷】\n▫️RAG检索增强：像查词典一样调取知识库作答（案例分享：某金融公司用企业文档库减少90%虚构财报信息）\n▫️实时调用工具：遇到计算需求直接调取计算器API\n\n✅【质检|最后防线】\n✔️模型审稿人：用另一AI交叉验证答案一致性\n✔️强制文献引用：输出必须附带信息来源\n✔️亚马逊中国专家：关键业务必须保留人工核查环节\n\n💡实战经验分享：大多数场景需要组合拳！我们先通过RAG构建行业知识库（第一层），再设定输出需附带PMID编号（第四层），双管齐下处理医学咨询场景的谬误问题。对于小红书创作者来说，至少应该设置输出校验规则和必填引用来源。\n\n你现在项目遇到哪些AI幻觉问题？评论区聊聊取经～",
  "is_image_upload": True,
  "image_urls": [
    "https://devgo.fun/static/render_1746798796.png",
    "https://i.ibb.co/ch5K1xXD/image-20250509215132605.png",
    "https://i.ibb.co/PzG2H6Wr/image-20250509214958562.png",
    "https://i.ibb.co/p8NLfDT/image-20250509215029860.png",
    "https://i.ibb.co/Mkm7gHvJ/image-20250509215006449.png",
    "https://i.ibb.co/3yB2g3R1/image-20250509215123674.png",
    "https://i.ibb.co/FL54Z4tn/image-20250509215050146.png",
    "https://i.ibb.co/XZt1wrkn/image-20250509215021633.png",
    "https://i.ibb.co/4w9Cz5rY/image-20250509215037088.png",
    "https://i.ibb.co/WNSdZhc3/image-20250509215113932.png"
  ],
  "tags": [
    "AI",
    "干货",
    "效率",
    "技术",
    "工具",
    "模型",
    "数据"
  ]
}

    title = data["title"]
    content = data["content"]

    image_urls = data["image_urls"]
    tags = data["tags"]
    
    # Process images and send data to XiaoHongShu
    process_and_send_to_xiaohongshu(title, content, image_urls, tags)
