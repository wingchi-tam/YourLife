from flask import Flask, render_template, request, send_file
from gtts import gTTS
from icrawler.builtin import BingImageCrawler
import ffmpeg
import os
from moviepy.editor import * 

#CONSTANTS 
voice_path = os.path.join('static', 'generated', 'voiceover.mp3')
output_path = os.path.join('static', 'generated', 'final_output.mp4')
video_path = os.path.join('static', 'generated', 'video.mp4')

app = Flask(__name__, static_folder='static')

@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        global biography, required_vars, extra_vars
        biography, required_vars, extra_vars = generate_bio()
        return render_template("index.html", biography=biography, bio_class="user_generated")
    return render_template("index.html", bio_class="hidden")

@app.route('/video')
def video():
    clear_pregenerated()
    create_audio(biography)
    generate_image(required_vars, extra_vars)
    generate_video()
    return render_template('video.html')

@app.route("/download")
def download():
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

def generate_bio():
    #REQUIRED VARS
    required_vars = {}
    required_vars["name"] = request.form.get("name") 
    required_vars["birthday"] =  request.form.get("childhood-birthday")
    required_vars["birthplace"] =  request.form.get("childhood-birthplace")  
    required_vars["childhood_location"] =  request.form.get("childhood-location")  
    required_vars["childhood_description"] =  request.form.get("childhood-description")
    required_vars["curr_living"] =  request.form.get("personal-location")  
    required_vars["hobbies"] =  request.form.get("personal-hobbies")  
    required_vars["goals"] =  request.form.get("personal-goals")  
    required_vars["accomplishment"] =  request.form.get("personal-accomplishment")
    required_vars["pronouns"] = request.form.get("personal-pronouns")

    for key, val in required_vars.items():
        if val == None:
            return "Question" +key+" unanswered, try again"

    user_pronouns = convert_pronouns(required_vars["pronouns"])

    childhood_story = ""+required_vars["name"] +" was born in a place called " + required_vars["birthplace"] + " on " + required_vars["birthday"] + ". \
    "+required_vars["name"]+" spent "+user_pronouns["possessive_adj"]+" childhood growing up in "+ required_vars["childhood_location"] + ". Like many other kids, "+user_pronouns["possessive_adj"]+" \
    childhood could be described as " + required_vars["childhood_description"] + ". "
  
    personal_story = "Now, "+ required_vars["name"] +" currently resides in "+ required_vars["curr_living"] +". In "+user_pronouns["possessive_adj"]+" free time, "+ required_vars["name"]+" enjoys doing the things "+user_pronouns["subject"]+" love such as \
    " +required_vars["hobbies"]+". Although "+ required_vars["name"]+" enjoys "+user_pronouns["possessive_adj"]+" life in "+required_vars["curr_living"]+", "+ required_vars["name"]+" has bigger aspirations. Sometimes, "+required_vars["name"]+" dreams of \
    "+ required_vars["goals"] +". Until then, "+ required_vars["name"]+" relishes on "+user_pronouns["possessive_adj"]+ " biggest accomplishment: "+required_vars["accomplishment"]

    #EXTRA VARS
    extra_vars={}
    extra_vars["highschool"] =  request.form.get("school-highschool")
    extra_vars["college"] =  request.form.get("school-college-name")  
    extra_vars["major"] =  request.form.get("school-major")  
    extra_vars["job"] =  request.form.get("adult-job")  
    extra_vars["job_location"] =  request.form.get("adult-job-location")  
    extra_vars["children_num"] =  int(request.form.get("adult-child-number"))  
    extra_vars["child_name"] =  request.form.get("adult-child-name")  

    school_story = ""
    if extra_vars["highschool"]:
        school_story += "Maturing through the epic highs and lows of elementary and middle school, "+ required_vars["name"] + " later attended "+ extra_vars["highschool"] +". "
          
    if extra_vars["college"]:
        school_story += "Afterwards, "+  required_vars["name"] + " pushed through the hurdles to finally get into "+ extra_vars["college"] +". "

    if extra_vars["major"]:
        school_story += "There, "+ required_vars["name"]+" went on to complete "+user_pronouns["possessive_adj"]+" degree in "+ extra_vars["major"] +". "

    adulthood_story = ""

    if extra_vars["job"] and extra_vars["job_location"]:
        adulthood_story += ""+user_pronouns["subject"]+" is currently working as "+ extra_vars["job"]+" at "+extra_vars["job_location"]+". "
             
    if extra_vars["children_num"] != "0" and extra_vars["children_num"] > 1:
        adulthood_story +=  "Now a parent, "+required_vars["name"]+" has "+extra_vars["children_num"]+" children named "+extra_vars["child_name"]+".  "
    
    if extra_vars["children_num"] == 1:
        adulthood_story +=  "Now a parent, "+required_vars["name"]+" has a child named "+extra_vars["child_name"]+".  "

    icebreaker_story = ""
    

    generated_bio = childhood_story + school_story + adulthood_story + personal_story
    return generated_bio, required_vars, extra_vars

def convert_pronouns(pronouns):
    user_pronouns = {}
    if pronouns == "she-her":
        user_pronouns["possessive_adj"] = "her"
        user_pronouns["subject"] = "she"
        user_pronouns["possessive_pro"] = "hers"
        user_pronouns["relative"] = "herself"
        user_pronouns["relative"] = "herself"
        user_pronouns["verb"] = "was"
    elif pronouns == "he-him":
        user_pronouns["possessive_adj"] = "his"
        user_pronouns["subject"] = "he"
        user_pronouns["possessive_pro"] = "his"
        user_pronouns["relative"] = "himself"
        user_pronouns["verb"] = "was"
    else:
        user_pronouns["possessive_adj"] = "their"
        user_pronouns["subject"] = "they"
        user_pronouns["possessive_pro"] = "theirs"
        user_pronouns["relative"] = "themself"
        user_pronouns["verb"] = "were"
    return user_pronouns

def create_audio(biography):
    language = 'en'
    voice_path = os.path.join('static', 'generated', 'voiceover.mp3')
    myobj = gTTS(text=biography, lang=language, slow=False)
  
    myobj.save(voice_path)

def generate_image(required_vars, extra_vars):
    # birthday =  required_vars["birthday"]
    birthplace =  required_vars["birthplace"]  
    childhood_location =  required_vars["childhood_location"]  
    childhood_description =  required_vars["childhood_description"]
    curr_living =  required_vars["curr_living"]  
    hobbies =  required_vars["hobbies"]  
    goals =  required_vars["goals"]  
    accomplishment =  required_vars["accomplishment"]
    
    photoarray = [birthplace, 
                    childhood_location, 
                    'kid being' + childhood_description, 
                    curr_living, 
                    hobbies, 
                    goals, 
                    accomplishment]

    for item in photoarray: 
        bing_crawler = BingImageCrawler(storage={'root_dir': 'img'}, parser_threads=2,
            downloader_threads=4)
        filters = dict(
            size= 'large',
            layout= 'square',
            type= 'photo'
        )
        bing_crawler.crawl(keyword= item, max_num=2, filters=filters, file_idx_offset='auto')

def generate_video():
    generate_transitions()
    video = ffmpeg.input(video_path)
    audio = ffmpeg.input(voice_path)
    vid_aud_cat = ffmpeg.concat(video, audio, v=1, a=1)
    output = ffmpeg.output(vid_aud_cat, output_path, r=30, pix_fmt='yuv420p').run()

def generate_transitions():
    ListImg = sorted(os.listdir('img'))

    for img in ListImg: 
        output_path = os.path.join('static', 'vid', str(img)+'.mp4')
        imgFile = os.path.join('img', img)
        video = ffmpeg.input(imgFile)
        effect_video = ffmpeg.zoompan(video, d = 65, z = 'zoom+0.001', s='800x800')
        output = ffmpeg.output(effect_video, output_path).run()
    #concatinate all vid 

    ListVid = sorted(os.listdir('static/vid'))

    filenames = []
    clips = []
    for filename in ListVid:
        if filename.endswith('.mp4'):
            filenames.append(filename)

    sorted(filenames)

    for filename in filenames: 
        clip = VideoFileClip(os.path.join('static', 'vid', filename))
        clips.append(clip)

    video = concatenate_videoclips(clips, method='compose')
    video.write_videofile('static/generated/video.mp4', fps=30)
        
def clear_pregenerated():
    dir = 'img'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    dir = 'static/generated'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    dir = 'static/vid'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
 