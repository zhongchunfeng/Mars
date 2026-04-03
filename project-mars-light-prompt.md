【角色设定】
你现在是一名资深的高级 Python 后端工程师。请帮我从零开发一个名为 "Project Mars (Lightweight)" 的自动化脚本工具。你的目标是编写极其轻量、极速且高容错的 Python 代码。

【项目背景与架构目标】
Project Mars 是一个纯文本处理引擎。它的核心业务流是：接收一个 YouTube 视频链接，不下载任何视频或音频，而是直接通过 API 抓取该视频的 YouTube 官方生成字幕，将其拼接为纯文本文件，最后自动上传至我的 Google Drive 并清理本地痕迹。

【技术栈与依赖要求】
请严格基于以下 Python 库进行开发，禁止引入重量级的处理库（如 whisper 或 ffmpeg）：

字幕抓取: youtube-transcript-api (核心引擎)

视频元数据获取: yt-dlp (⚠️ 强制约束：仅允许使用其抓取视频 Title 等元数据，绝对禁止下载任何媒体文件)

Google Drive 交互: google-api-python-client, google-auth-httplib2, google-auth-oauthlib

【核心功能模块与执行流程】
请将代码拆分为职责单一的函数，并按以下流程串联：

模块 1：Google OAuth 2.0 鉴权 (authenticate_google_drive)

权限范围（Scope）需严格限制为 https://www.googleapis.com/auth/drive.file（仅限应用自身创建的文件）。

读取 credentials.json，初次运行走本地服务器浏览器授权。

授权成功后保存为 token.json，包含 Token 过期自动刷新逻辑。

模块 2：获取视频元数据 (get_video_metadata)

接收 YouTube URL。

使用 yt-dlp 提取视频信息。必须设置 download=False 以确保零 I/O 下载。

返回干净的视频标题（需过滤掉可能导致本地文件系统报错的特殊字符，如 |, /, \, : 等）。

模块 3：急速字幕提取与格式化 (fetch_and_format_transcript)

提取 YouTube URL 中的 video_id。

调用 YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'zh-Hans', 'zh-Hant'])（优先尝试获取英文或中文字幕）。

将返回的 JSON 字典列表（包含 text, start, duration）提取纯 text 字段，并拼接成易于阅读的段落（如每句用空格或换行隔开）。

将最终的纯文本写入本地临时文件 "{清洗后的视频标题}_字幕.txt"。

模块 4：Google Drive 上传 (upload_to_drive)

使用 Drive API v3，将 .txt 文本文件作为 text/plain MIME 类型上传到 Drive 根目录。

打印上传成功后的云端文件链接或 ID。

模块 5：主程序与容错处理 (main)

终端交互式等待用户输入 URL。

核心错误捕获：必须捕获并优雅处理 TranscriptsDisabled（视频未开启字幕）或 NoTranscriptFound（找不到指定语言字幕）的异常，并向用户输出友好的中文提示。

强制清理：使用 finally 块确保任务结束后，本地生成的 .txt 临时文件被彻底删除。

【代码规范与输出要求】

直接输出完整的、可运行的 Python 源码（如 main.py），无需提供环境安装教程。

代码必须包含详细的中文注释，并在控制台通过 print 输出关键节点的运行日志（如：“🚀 正在免下载抓取字幕...”、“✅ 抓取成功，耗时 x 秒”）。