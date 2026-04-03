# Story: YouTube 视频转文字并存入 Google Drive (Project Mars)

## 项目背景
将 YouTube 视频内容自动转换为文字并存储在 Google Drive 中，以便进行后续的资料整理与 AI 分析。

## 核心流程 (Core Flow)
1. **输入**: 获取用户提供的 YouTube 视频 URL。
2. **下载**: 使用 `yt-dlp` 提取视频的音频部分（MP3 格式）。
3. **转录**: 调用本地 `OpenAI Whisper` 模型（`base` 级别）进行语音识别。
4. **存盘**: 将转录出的文本（`.txt`）通过 Google Drive API 上传至用户的云盘。
5. **清理**: 任务结束后自动删除本地的临时音频和文本文件。

## 验收标准 (Acceptance Criteria)
- [ ] 脚本能够成功获取 Google Drive 的 OAuth2 授权。
- [ ] 能够成功下载 YouTube 音频并存储为临时文件。
- [ ] Whisper 模型能够输出可读的转录内容（支持中文/英文）。
- [ ] 最终生成的 `.txt` 文件成功出现在 Google Drive 根目录。
- [ ] 脚本运行结束后，本地目录保持清洁。

## 核心依赖
- `yt-dlp`: 视频抓取。
- `openai-whisper`: AI 转录。
- `google-api-python-client`: Drive 同步。
- `ffmpeg`: 系统级音频处理器。