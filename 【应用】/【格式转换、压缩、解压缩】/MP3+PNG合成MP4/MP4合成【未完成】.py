# pip install moviepy
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
# 图片和音频文件的路径
image_path = r'C:\Users\13480\Desktop\.png'
audio_path = r'C:\Users\13480\Desktop\.mp3'
# 设置图片的持续时间和音频文件的长度一致
audio = AudioFileClip(audio_path)
image = ImageClip(image_path).set_duration(audio.duration)
# 设置视频的帧率
fps = 24
image = image.set_fps(fps)
# 将图片和音频合并为一个视频
video = CompositeVideoClip([image]).set_audio(audio)
# 输出视频文件的路径
output_path = 'output_video.mp4'
# 写入文件，指定帧率
video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=fps)