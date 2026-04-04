"""
Module Header: Project Mars (Lightweight)
Author: Antigravity Assistant
Description: 极轻量化抓取 YouTube 字幕并上传至 Google Drive 的自动化工具。
License: MIT
"""

import os
import re
import sys
import time
from typing import List, Dict, Optional

# 第三方依赖
try:
    import yt_dlp
    from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
except ImportError as e:
    print(f"❌ 运行环境诊断: 找不到模块 '{e.name}'")
    print(f"🚀 当前解析器路径: {sys.executable}")
    print(f"💡 建议: 请运行 ./run_mars.sh 或在虚拟环境中执行 'pip install -r requirements.txt'")
    sys.exit(1)

# 配置常量
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

def authenticate_google_drive() -> any:
    """
    模块 1: Google Drive OAuth 2.0 自动鉴权与令牌管理
    实现 Token 自动保存与过期重刷逻辑。
    """
    creds = None
    # 尝试加载已有的持久化 Token
    # 为什么：遵循最小化交互原则，优先使用已授权的凭证避免频繁触发 OAuth 流程。
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # 如果没有有效的凭据，则进行授权流程
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🚀 正在刷新过期授权令牌...")
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"❌ 错误: 未在根目录找到 {CREDENTIALS_FILE}。请先配置 Google Cloud 项目凭据。")
                sys.exit(1)
            
            print("🔑 正在开启本地授权服务器，请在浏览器中完成验证...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # 保存持久化令牌
        # 为什么：减少用户重复手动授权的成本，确保脚本在自动化环境下的半持续运行能力。
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    print("✅ Google Drive 授权成功")
    return build('drive', 'v3', credentials=creds)

def get_video_metadata(url: str) -> str:
    """
    模块 2: 获取视频元数据
    使用 yt-dlp 抓取 Title，download=False 确保零 I/O 损耗。
    """
    print("🚀 正在获取视频元数据...")
    ydl_opts = {
        'quiet': True,
        'skip_download': True,        # 为什么：仅需元数据，禁止二进制下载以节省带宽与 I/O 损耗。
        'no_warnings': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as yt_dl_instance:
            info = yt_dl_instance.extract_info(url, download=False)
            title = info.get('title', '未知视频')
            # 过滤 OS 不允许的文件名特殊字符
            # 为什么：确保生成的本地 .txt 文件在所有主流桌面操作系统下均能成功创建。
            cleaned_title = re.sub(r'[\\/:*?"<>|]', '_', title)
            return cleaned_title
    except Exception as e:
        print(f"⚠️ 获取元数据失败，将使用默认名称。原因: {e}")
        return "YouTube_Transcript"

def fetch_and_format_transcript(video_id: str, title: str) -> Optional[str]:
    """
    模块 3: 提取并格式化字幕
    支持中英官方字幕抓取，合并为纯文本文件。
    """
    print(f"🚀 正在提取字幕 (ID: {video_id})...")
    start_time = time.time()
    
    try:
        # 为什么：使用 YouTubeTranscriptApi().fetch() 以确保与各版本库的兼容性。
        transcript_list = YouTubeTranscriptApi().fetch(
            video_id, 
            languages=['en', 'zh-Hans', 'zh-Hant', 'zh']
        )
        
        # 将列表形式的字幕字典串联为纯文本，每段间以空格隔开
        full_text = " ".join([item['text'] for item in transcript_list])
        
        # 本地文件名
        filename = f"{title}_字幕.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        elapsed = time.time() - start_time
        print(f"✅ 字幕分析成功，耗时 {elapsed:.2f} 秒")
        return filename

    except TranscriptsDisabled:
        print("❌ 错误: 该视频已禁用官方字幕，无法提取。")
    except NoTranscriptFound:
        print("❌ 错误: 找不到支持的中文字幕或英文字幕。")
    except Exception as e:
        if "Could not retrieve a transcript" in str(e):
            print("❌ 错误: 您的 IP 似乎已被 YouTube 封禁。")
            print("💡 建议：1. 开启全局代理；2. 在同目录下放置 'cookies.txt' 文件。")
        else:
            print(f"❌ 发生未知异常: {e}")
    
    return None

def upload_to_drive(service, file_path: str, file_name: str):
    """
    模块 4: Google Drive 文件上传
    上传到 Drive 根目录并返回云端 ID。
    """
    print(f"🚀 正在上传至 Google Drive: {file_name}...")
    
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, mimetype='text/plain')
    
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        
        print(f"✅ 上传成功！")
        print(f"🔗 云端链接: {file.get('webViewLink')}")
        print(f"📦 文件 ID: {file.get('id')}")
        
    except Exception as e:
        print(f"❌ 上传过程发生错误: {e}")

def main():
    """
    模块 5: 主程序与流程调度
    处理用户交互、整体异常流及强制性环境清理。
    """
    print("="*40)
    print("      Project Mars (Lightweight) v1.0")
    print("="*40)
    
    url = input("请输入 YouTube 视频链接 (或输入 'q' 退出): ").strip()
    if url.lower() == 'q' or not url:
        return

    # 提取 Video ID (兼容 URL/Shorts/Live 格式)
    # 为什么：使用更广泛的正则识别模式，确保针对不同来源的 YouTube 链接都能精准定位视频唯一标识。
    video_id_match = re.search(r'(?:v=|\/|vi\/|e\/|u\/|shorts\/|live\/)([0-9A-Za-z_-]{11})', url)
    if not video_id_match:
        print("❌ 无法从链接中解析出 Video ID，请检查链接格式。")
        return
    
    video_id = video_id_match.group(1)
    service = authenticate_google_drive()
    
    temp_file = None
    try:
        # 1. 抓元数据
        title = get_video_metadata(url)
        
        # 2. 抓字幕并存为本地临时文件
        temp_file = fetch_and_format_transcript(video_id, title)
        
        # 3. 如果成功生成临时文件，则上传
        if temp_file and os.path.exists(temp_file):
            upload_to_drive(service, temp_file, os.path.basename(temp_file))
        
    except KeyboardInterrupt:
        print("\n操作已由用户取消。")
    finally:
        # 模块 5: 强制清理逻辑
        # 为什么：符合 CISA 数据残留控制要求，确保临时字幕文件在处理完成后立即销毁，防止本地存储污染与潜在信息泄露。
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"🧹 本地缓存已安全清理。")

if __name__ == '__main__':
    main()
