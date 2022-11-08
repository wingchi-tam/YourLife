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
    # create_audio(biography)
    # generate_image(required_vars, extra_vars)
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
    required_vars["final_word"] =  request.form.get("personal-description")

    for key, val in required_vars.items():
        if val == None:
            return "Question" +key+" unanswered, try again"

    user_pronouns = convert_pronouns(required_vars["pronouns"])

    #EXTRA VARS
    extra_vars={}
    extra_vars["highschool"] =  request.form.get("school-highschool")
    extra_vars["fav_subject"]=  request.form.get("school-favorite-subject")   
    extra_vars["school_activities"] =  request.form.get("school-activities")  
    extra_vars["college"] =  request.form.get("school-college-name")  
    extra_vars["major"] =  request.form.get("school-major")  
    extra_vars["job"] =  request.form.get("adult-job")  
    extra_vars["job_location"] =  request.form.get("adult-job-location")  
    extra_vars["curr_partner"] =  request.form.get("adult-partner-name")   
    extra_vars["relationship_status"] =  request.form.get("adult-relationship-status")   
    extra_vars["children_num"] =  request.form.get("adult-child-number")  
    extra_vars["child_name"] =  request.form.get("adult-child-name")  

    childhood_story = "Hello, my name is Ken Burns and I will be telling the story of " + required_vars["name"] + "'s life. "+required_vars["name"] +" was born in a place called " + required_vars["birthplace"] + " in \
    on " + required_vars["birthplace"] + ". "+required_vars["name"]+" spent "+user_pronouns["possessive_adj"]+" childhood growing up in "+ required_vars["childhood_location"] + ". Like many other kids, "+user_pronouns["possessive_adj"]+" \
    childhood could be described as " + required_vars["childhood_description"] + ". "
  
    personal_story = "Now, "+ required_vars["name"] +" currently resides in "+ required_vars["curr_living"] +". In "+user_pronouns["possessive_adj"]+" free time, "+ required_vars["name"]+" enjoys doing the things "+user_pronouns["subject"]+" love such as \
    " +required_vars["hobbies"]+". Although "+ required_vars["name"]+" enjoys "+user_pronouns["possessive_adj"]+" life in "+required_vars["curr_living"]+", "+ required_vars["name"]+" has bigger aspirations. Sometimes, late \
    at night,"+required_vars["name"]+" dreams of "+ required_vars["goals"] +". Until then, "+ required_vars["name"]+" relishes on "+user_pronouns["possessive_adj"]+ \
    " biggest accomplishment: "+required_vars["accomplishment"]+". Living such an eventful life, it could be described as "+required_vars["final_word"]+"."

    school_story = ""
    if extra_vars["highschool"]:
        school_story += "Maturing through the epic highs and lows of elementary and middle school, "+  required_vars["name"] + " finally began "+user_pronouns["possessive_adj"]+" epic adventure at "+ extra_vars["highschool"] +". "
    
    if extra_vars["fav_subject"]:
        school_story += "Despite riding the emotionally charged rollercoaster that high school is, nothing brightened "+user_pronouns["possessive_adj"]+" days more than attending "+ extra_vars["fav_subject"] +". "
        
    if extra_vars["school_activities"]:
        school_story += "Moreover, when tests and classes didn't fill "+  required_vars["name"] + "'s schedule, "+user_pronouns["subject"]+" really enjoyed participating in "+ extra_vars["school_activities"] +". "
        
    if extra_vars["college"]:
        school_story += "Yet, as classes, tests and SATs were crunched, "+  required_vars["name"] + " pushed through the hurdles of everything required by college admissions to finally get into "+user_pronouns["possessive_adj"]+" dream school: "+ extra_vars["college"] +". "

    if extra_vars["major"]:
        school_story += "There, the parties, clubs, difficult classes, and stressful environment never stopped "+ required_vars["name"]+" from completing "+user_pronouns["possessive_adj"]+" degree in "+ extra_vars["major"] +". "

    adulthood_story = ""

    if extra_vars["job"] and extra_vars["job_location"]:
        adulthood_story += "The struggles of real life hit when "+user_pronouns["subject"]+" started "+user_pronouns["possessive_adj"]+" first job as a "+ extra_vars["job"]+" at "+extra_vars["job_location"]+". "
        
    if extra_vars["relationship_status"]:
        adulthood_story += "Currently, "+user_pronouns["possessive_adj"]+" relationship status is "+extra_vars["relationship_status"]+". "

    if extra_vars["curr_partner"]:
        adulthood_story += user_pronouns["possessive_adj"].capitalize()+" favorite activity at home is cuddling with "+extra_vars["curr_partner"]+". " 
        
    if extra_vars["children_num"] != "0" and extra_vars["children_num"] > 1:
        adulthood_story +=  required_vars["name"] +" is now also raising "+extra_vars["children_num"]+" children. Thanks to their amazing job at being a parent, they're all growing up to be amazing people and their names are "+extra_vars["child_name"]+".  "
    
    if extra_vars["child_name"]:
        adulthood_story +=  required_vars["name"] + " is now also raising a child. Thanks to their amazing job at being a parent, they're growing up to be an amazing person and their name is "+extra_vars["child_name"]+".  "

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
    bio = biography
    language = 'en'
    voice_path = os.path.join('static', 'generated', 'voiceover.mp3')
    myobj = gTTS(text=biography, lang=language, slow=False)
  
    myobj.save(voice_path)

'''
def create_photo(keywords): 
    google_crawler = GoogleImageCrawler(storage={'root_dir': 'Image_Dir'})
    google_crawler.crawl(keyword= keywords, max_num=4)
'''
def generate_image(required_vars, extra_vars):
    # birthday =  required_vars["birthday"]
    birthplace =  required_vars["birthplace"]  
    childhood_location =  required_vars["childhood_location"]  
    childhood_description =  required_vars["childhood_description"]
    curr_living =  required_vars["curr_living"]  
    hobbies =  required_vars["hobbies"]  
    goals =  required_vars["goals"]  
    accomplishment =  required_vars["accomplishment"]
    # pronouns = required_vars["pronouns"]
    final_word =  required_vars["final_word"]
    photoarray = ['Ken Burns', 
                    birthplace, 
                    childhood_location, 
                    'kid being' + childhood_description, 
                    curr_living, 
                    hobbies, 
                    goals, 
                    accomplishment, 
                    final_word]

    for item in photoarray: 
        bing_crawler = BingImageCrawler(storage={'root_dir': 'img'}, parser_threads=4,
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
    dir = 'static'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, 'generated', f))
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, 'vid', f))
 