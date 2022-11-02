import ffmpeg
import os

# voiceover = ffm.input('soundtrack.mp3')
# out = ffm.output('test_video.mp4')

# video = ffmpeg.input('/ken_burns.png', framerate=1)
# output = ffmpeg.output('ffmpeg_test.mp4', )
# audio = ffmpeg.input('/soundtrack.mp3')
# av = ffmpeg.concat(video, audio)

def save():
    os.system("ffmpeg -framerate 1 -i img\%06d.jpg -c:v libx264 -r 30 test_output.mp4")

save()
