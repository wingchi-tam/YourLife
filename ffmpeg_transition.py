import ffmpeg
import os
from moviepy.editor import * 


ListImg = sorted(os.listdir('img'))

# vidList = []
for img in ListImg: 
    output_path = os.path.join('vid', str(img)+'.mp4')
    imgFile = os.path.join('img', img)
    video = ffmpeg.input(imgFile)
    effect_video = ffmpeg.zoompan(video, d = 100, z = 'zoom+0.001')
    output = ffmpeg.output(effect_video, output_path).run()
#concatinate all vid 

clips = []
for filename in os.listdir('vid'):
    # print(filename)
    if filename.endswith('.mp4'):
        # order = int(filename[:6])
        clip = VideoFileClip(os.path.join('vid', filename))
        clips.append(clip)

video = concatenate_videoclips(clips, method='compose')
video.write_videofile('transition_test.mp4', fps=30)

