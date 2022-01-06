if ($null -eq $args[1]) {
    Write-Output "Usage: ffmpeg720 <input_video> <output.mp4>"
} else {
    ffmpeg `
        -hwaccel cuda `
        -i $args[0] `
        -b:v 2M `
        -vf scale=-1:720 `
        -c:v hevc_nvenc `
        $args[1]
}