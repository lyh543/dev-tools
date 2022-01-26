:: 从 url 下载 m3u8
@echo off
set /p url=url: 
set /p filename=filename(output.mp4): 
if not defined filename set filename=output.mp4
echo on
ffmpeg -allowed_extensions ALL -i "%url%" -c:v copy "%filename%"