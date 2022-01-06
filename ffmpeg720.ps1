if ($args[1].Equals('')) {
	Write-Output "Usage: ffmpeg720 <input_video> <output.mp4>"
} else {
	ffmpeg -hwaccel cuda `	# cuda 加速
		-i $args[0] `		# 输入文件
		-b:v 2M `			# 码率
		-vf scale=-1:720 `	# 高度为 720p，宽度按比例调整
		-c:v hevc_nvenc `	# h. 265 编码
		$args[1]			# 输出文件
}