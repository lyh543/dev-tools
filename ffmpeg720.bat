@if '%2'=='' (
	echo Usage: ffmpeg720 ^<input_video^> ^<output.mp4^>
) else (
	ffmpeg -hwaccel cuda ^
		-i %1 ^
		-b:v 2M ^
		-vf scale=-1:720 ^
		-c:v hevc_nvenc ^
		%2
)