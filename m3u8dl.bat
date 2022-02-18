:: 从 url 下载 m3u8
@echo off
"C:\Program Files\Google\Chrome\Application\chrome.exe" https://github.com/HeiSir2014/M3U8-Downloader
set /p url=url: 
set /p filename=filename(output.mp4): 
if not defined filename set filename=output.mp4
echo on
ffmpeg -allowed_extensions ALL -i "%url%" -c:v copy "%filename%"