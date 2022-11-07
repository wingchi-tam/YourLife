import ffmpeg
import os
from moviepy.editor import * 


def generate_transitions():
    ListImg = sorted(os.listdir('img'))

    # vidList = []
    for img in ListImg: 
        output_path = os.path.join('vid', str(img)+'.mp4')
        imgFile = os.path.join('img', img)
        video = ffmpeg.input(imgFile)
        effect_video = ffmpeg.zoompan(video, d = 65, z = 'zoom+0.001', s='800x800')
        output = ffmpeg.output(effect_video, output_path).run()
    #concatinate all vid 

    ListVid = sorted(os.listdir('vid'))

    filenames = []
    clips = []
    for filename in ListVid:
        if filename.endswith('.mp4'):
            filenames.append(filename)

    sorted(filenames)

    for filename in filenames: 
        clip = VideoFileClip(os.path.join('vid', filename))
        clips.append(clip)

    video = concatenate_videoclips(clips, method='compose')
    video.write_videofile('video.mp4', fps=30)


