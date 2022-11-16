from flask import Flask, render_template, request, send_file
from gtts import gTTS
from icrawler import ImageDownloader, Parser
from icrawler.builtin import BingImageCrawler
import ffmpeg
import os
from moviepy.editor import * 
import random 
from mutagen.mp3 import MP3

#CONSTANTS 
voice_path = os.path.join('static', 'generated', 'voiceover.mp3')
output_path = os.path.join('static', 'generated', 'final_output.mp4')
video_path = os.path.join('static', 'generated', 'video.mp4')

#class declaractions
class keywordObj:
    def __init__(self, key):
        self.key = key
        self.text = ""
        self.time = 0
        self.value = None
        self.index = []

class timestampsObj:
    def __init__(self):
        self.keywords = {}
        self.stories = {}
    def add_text(self, key, sentence):
        if self.keywords.get(key) == None:
            self.keywords[key] = keywordObj(key)
        self.keywords[key].text = sentence
    def add_time(self, key, length):
        if self.keywords.get(key) == None:
            self.keywords[key] = keywordObj(key)
        self.keywords[key].length = length
    def add_value(self, key, value):
        if self.keywords.get(key) == None:
            self.keywords[key] = keywordObj(key)
        self.keywords[key].value = value
    def add_index(self, key, index):
        if self.keywords.get(key) == None:
            self.keywords[key] = keywordObj(key)
        self.keywords[key].index = index
    def add_story(self, key, story):
        self.stories[key] = story
    def get_text(self, key):
        if self.keywords.get(key) != None:
            return self.keywords.get(key).text
    def get_time(self, key):
        if self.keywords.get(key) != None:
            return self.keywords.get(key).time
    def get_story(self, key):
        return self.stories.get(key)
    def get_keywords(self):
        return self.keywords.keys()
    def get_value(self, key):
        if self.keywords.get(key) != None:
            return self.keywords.get(key).value
    def get_index(self, key):
        if self.keywords.get(key) != None:
            return self.keywords.get(key).index
    def find_key_from_index(self, index):
        for key in self.get_keywords():
            if index in self.get_index(key):
                print(index)
                return key
    
global timestamp
timestamp = timestampsObj()

#HELPER FUNCTIONS
def add_to_photoarray(keyword, index, photoarray):
    if timestamp.get_value(keyword) != None and timestamp.get_value(keyword) != '' and timestamp.get_value(keyword) != 0: 
        if keyword == "ice_cream":
            val = timestamp.get_value(keyword) + " ice cream" 
        else:
            val = timestamp.get_value(keyword)
        timestamp.add_index(val,[index, index+1])
        index+=2
        photoarray.append(val)
    return index

app = Flask(__name__, static_folder='static')

@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        generate_bio()
        return render_template("index.html", biography=timestamp.get_story("generated_bio"), bio_class="user_generated")
    return render_template("index.html", bio_class="hidden")

@app.route('/video')
def video():
    #clear_pregenerated()
    #create_audio()
    #generate_image()
    generate_video()
    return render_template('video.html')

@app.route("/download")
def download():
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

def generate_bio():
    #REQUIRED VARS
    timestamp.add_value("name", request.form.get("name"))
    timestamp.add_value("birthday", request.form.get("childhood-birthday"))
    timestamp.add_value("birthplace", request.form.get("childhood-birthplace")) 
    timestamp.add_value("childhood_location", request.form.get("childhood-location"))  
    timestamp.add_value("childhood_description", request.form.get("childhood-description"))
    timestamp.add_value("curr_living", request.form.get("personal-location"))
    timestamp.add_value("hobbies", request.form.get("personal-hobbies"))
    timestamp.add_value("goals", request.form.get("personal-goals"))
    timestamp.add_value("accomplishment", request.form.get("personal-accomplishment"))
    timestamp.add_value("pronouns", request.form.get("personal-pronouns"))

    user_pronouns = convert_pronouns(request.form.get("personal-pronouns"))

    timestamp.add_text("birthplace", timestamp.get_value("name") +" was born in a place called " + timestamp.get_value("birthplace") + " on " + timestamp.get_value("birthday") + ". ")
    timestamp.add_text("childhood_location", timestamp.get_value("name")+" spent "+user_pronouns["possessive_adj"]+" childhood growing up in "+ timestamp.get_value("childhood_location") + ". ")
    timestamp.add_text("childhood_description", "Like many other kids, "+user_pronouns["possessive_adj"]+" childhood could be described as " + timestamp.get_value("childhood_description") + ". ")
    childhood_story = timestamp.get_text("birthplace") + timestamp.get_text("childhood_location") + timestamp.get_text("childhood_description") 
    timestamp.add_story("childhood_story", childhood_story)

    timestamp.add_text("curr_living", "Now, "+ timestamp.get_value("name") +" currently resides in "+ timestamp.get_value("curr_living") +". ")
    timestamp.add_text("hobbies", "In "+user_pronouns["possessive_adj"]+" free time, "+ timestamp.get_value("name")+" enjoys doing the things "+user_pronouns["subject"]+" love such as " +timestamp.get_value("hobbies")+". ")
    timestamp.add_text("goals", "Although "+ timestamp.get_value("name")+" enjoys "+user_pronouns["possessive_adj"]+" life in "+timestamp.get_value("curr_living")+", "+ timestamp.get_value("name")+" has bigger aspirations. Sometimes, "+timestamp.get_value("name")+" dreams of "+ timestamp.get_value("goals") +". ")
    timestamp.add_text("accomplishment", "Until then, "+ timestamp.get_value("name")+" relishes on "+user_pronouns["possessive_adj"]+ " biggest accomplishment: "+timestamp.get_value("accomplishment")+". ")
    personal_story = timestamp.get_text("curr_living") + timestamp.get_text("hobbies") + timestamp.get_text("goals") + timestamp.get_text("accomplishment")
    timestamp.add_story("personal_story", personal_story)

    #EXTRA VARS
    timestamp.add_value("highschool", request.form.get("school-highschool"))
    timestamp.add_value("college", request.form.get("school-college-name"))
    timestamp.add_value("major", request.form.get("school-major"))
    timestamp.add_value("children_num", int(request.form.get("adult-child-number")))  
    timestamp.add_value("child_name", request.form.get("adult-child-name"))
    timestamp.add_value("ice_cream", request.form.get("ib-ice-cream"))
    timestamp.add_value("money_concern", request.form.get("ib-dream"))
    timestamp.add_value("island_music", request.form.get("ib-island-music"))
    timestamp.add_value("mt_rushmore", request.form.get("ib-rushmore"))
    timestamp.add_value("fictional_world", request.form.get("ib-fictional-place"))
    timestamp.add_value("one_movie", request.form.get("ib-first-movie"))
    timestamp.add_value("unlimited_supply", request.form.get("ib-unlimited-supply"))
    timestamp.add_value("tv_character", request.form.get("ib-character"))
    timestamp.add_value("superpower", request.form.get("ib-superpower"))
    timestamp.add_value("history_friend", request.form.get("ib-history-friend"))

    school_story = ""
    if timestamp.get_value("highschool"):
        timestamp.add_text("highschool", "Maturing through the epic highs and lows of elementary and middle school, "+ timestamp.get_value("name") + " later attended "+ timestamp.get_value("highschool") +". ")
        school_story += timestamp.get_text("highschool")

    if timestamp.get_value("college"):
        timestamp.add_text("college", "Afterwards, "+  timestamp.get_value("name") + " pushed through the hurdles to finally get into "+ timestamp.get_value("college") +". ")
        school_story += timestamp.get_text("college")

    if timestamp.get_value("major"):
        timestamp.add_text("major", "There, "+ timestamp.get_value("name")+" went on to complete "+user_pronouns["possessive_adj"]+" degree in "+ timestamp.get_value("major") +". ")
        school_story += timestamp.get_text("major")

    timestamp.add_story("school_story", school_story)
    adulthood_story = ""         
    if timestamp.get_value("children_num") != "0" and timestamp.get_value("children_num") > 1:
        timestamp.add_text("children_num","Now a parent, "+timestamp.get_value("name")+" has "+timestamp.get_value("children_num")+" children named "+timestamp.get_value("child_name")+". ")
        adulthood_story += timestamp.get_text("children_num")

    if timestamp.get_value("children_num") == 1:
        timestamp.add_text("children_num", "Now a parent, "+timestamp.get_value("name")+" has a child named "+timestamp.get_value("child_name")+". ")
        adulthood_story += timestamp.get_text("children_num")

    timestamp.add_story("adulthood_story", adulthood_story)
    icebreaker_story = ""
    if timestamp.get_value("ice_cream"):
        timestamp.add_text("ice_cream", timestamp.get_value("name") + "'s favorite ice cream flavor is "+timestamp.get_value("ice_cream")+". ")
        icebreaker_story += timestamp.get_text("ice_cream")
    if timestamp.get_value("money_concern"):
        timestamp.add_text("money_concern", "If money wasn't a concern for " +timestamp.get_value("name") + ", the first thing " + user_pronouns["subject"]+ " would buy is " +timestamp.get_value("money_concern")+". ")
        icebreaker_story += timestamp.get_text("money_concern")
    if timestamp.get_value("island_music"):
        timestamp.add_text("island_music", "If "+timestamp.get_value("name")+" was stranded on a deserted island with only one thing to listen to, it would be "+timestamp.get_value("island_music")+". ")
        icebreaker_story += timestamp.get_text("island_music")
    if timestamp.get_value("mt_rushmore"):
        timestamp.add_text("mt_rushmore", "If " +timestamp.get_value("name") + " could add any person from history to Mr. Rushmore, " + user_pronouns["subject"] + " would choose " + timestamp.get_value("mt_rushmore")+ ". ")
        icebreaker_story += timestamp.get_text("mt_rushmore")
    if timestamp.get_value("fictional_world"):
        timestamp.add_text("fictional_world", "If "+user_pronouns["subject"]+" had the opportunity to travel to a fictional place, it would be "+timestamp.get_value("fictional_world")+ ". ")
        icebreaker_story += timestamp.get_text("fictional_world")
    if timestamp.get_value("unlimited_supply"):
        timestamp.add_text("unlimited_supply", "If "+timestamp.get_value("name") +" had an unlimited supply of one thing for the rest of " + user_pronouns["possessive_adj"] + "life, " + user_pronouns["subject"] + "would choose " + timestamp.get_value("unlimited_supply")+ ". ")
        icebreaker_story += timestamp.get_text("unlimited_supply")
    if timestamp.get_value("one_movie"):
        timestamp.add_text("one_movie", "If " + timestamp.get_value("name") + " could only see one movie for the rest of " + user_pronouns["possessive_adj"] + " life, " + user_pronouns["subject"] + " would choose " + timestamp.get_value("one_movie")+ ". ")
        icebreaker_story += timestamp.get_text("one_movie")
    if timestamp.get_value("tv_character"): 
        timestamp.add_text("tv_character", "If " + timestamp.get_value("name") + " could be a character in any TV show, " + user_pronouns["subject"] + " would be " + timestamp.get_value("tv_character")+ ". ")
        icebreaker_story += timestamp.get_text("tv_character")
    if timestamp.get_value("superpower"): 
        timestamp.add_text("superpower", timestamp.get_value("name")+"'s ideal superpower would be " + timestamp.get_value("superpower") + ". ")
        icebreaker_story += timestamp.get_text("superpower")
    if timestamp.get_value("history_friend"): 
        timestamp.add_text("history_friend", "If " + timestamp.get_value("name") + " could choose any person from history to be " + user_pronouns["possessive_adj"] + " imaginary friend, it would be " + timestamp.get_value("history_friend") + ". ")
        icebreaker_story += timestamp.get_text("history_friend")
    timestamp.add_story("icebreaker_story", icebreaker_story)

    generated_bio = childhood_story + school_story + adulthood_story + personal_story + icebreaker_story
    timestamp.add_story("generated_bio", generated_bio)

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

def create_audio():
    for key in timestamp.get_keywords():
        file_name = key + ".mp3"
        voice_path = os.path.join('static', 'audio', file_name)
        text = timestamp.get_text(key)
        if text != "":
            audio_obj = gTTS(text=text, lang='en', slow=False)
            audio_obj.save(voice_path)
            audio = MP3(voice_path)
            timestamp.add_time(key, audio.info.length)
    voice_path = os.path.join('static', 'generated', 'voiceover.mp3')
    text = timestamp.get_story("generated_bio")
    audio_obj = gTTS(text=text, lang='en', slow=False)
    audio_obj.save(voice_path)
    
def generate_image():
    birthplace =  timestamp.get_value("birthplace")
    childhood_location =  timestamp.get_value("childhood_location")
    childhood_description =  timestamp.get_value("childhood_description")
    curr_living =  timestamp.get_value("curr_living")
    hobbies =  timestamp.get_value("hobbies")
    goals =  timestamp.get_value("goals")
    accomplishment =  timestamp.get_value("accomplishment")
    photoarray = [birthplace, 
                    childhood_location, 
                    'kid being ' + childhood_description, 
                    curr_living, 
                    hobbies, 
                    goals, 
                    accomplishment]

    timestamp.add_index("birthplace", [1, 2])
    timestamp.add_index("childhood_location", [3, 4])
    timestamp.add_index("childhood_description", [5, 6])
    timestamp.add_index("curr_living",[7, 8])
    timestamp.add_index("hobbies",[9, 10])
    timestamp.add_index("goals", [11, 12])
    timestamp.add_index("accomplishment",[13, 14])
    index = 15
    index = add_to_photoarray("ice_cream", index, photoarray)
    index = add_to_photoarray("money_concern", index, photoarray)
    index = add_to_photoarray("island_music", index, photoarray)
    index = add_to_photoarray("mt_rushmore", index, photoarray)
    index = add_to_photoarray("fictional_world", index, photoarray)
    index = add_to_photoarray("unlimited_supply", index, photoarray)
    index = add_to_photoarray("one_movie", index, photoarray)
    index = add_to_photoarray("tv_character", index, photoarray)
    index = add_to_photoarray("superpower", index, photoarray)
    index = add_to_photoarray("history_friend", index, photoarray)
    print(photoarray)

    for item in photoarray: 
        bing_crawler = BingImageCrawler(storage={'root_dir': 'img'}, 
            parser_threads=2,
            downloader_threads=4)
        filters = dict(
            size= 'large',
            layout= 'square',
            type= 'photo'
        )
        bing_crawler.crawl(keyword=item, max_num=2, filters=filters, file_idx_offset='auto')

def generate_video():
    generate_transitions()
    video = ffmpeg.input(video_path)
    audio = ffmpeg.input(voice_path)
    vid_aud_cat = ffmpeg.concat(video, audio, v=1, a=1)
    output = ffmpeg.output(vid_aud_cat, output_path, r=30, pix_fmt='yuv420p').run()

def generate_transitions():
    ListImg = sorted(os.listdir('img'))

    #9 effects 
    #top left(0, 0), top (iw/2-(iw/zoom/2), 0), top right (ow, 0), right (ow, ih/2-(ih/zoom/2)), bottom right(ow, oh), 
    #bottom (iw/2-(iw/zoom/2), oh), bottom left (ow, 0), left (0, ih/2-(ih/zoom/2)), middle (iw/2-(iw/zoom/2), ih/2-(ih/zoom/2))
    possible_transtiion = [("0", "0"), ("iw/2-(iw/zoom/2)", "0"), ("ow", "0"), 
                           ("ow", "ih/2-(ih/zoom/2)"), ("ow", "oh"), ("iw/2-(iw/zoom/2)", "oh"), 
                           ("ow", "0"), ("0", "ih/2-(ih/zoom/2)"), ("iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)")]

    for img in ListImg: 
        output_path = os.path.join('static', 'vid', str(img)+'.mp4')
        imgFile = os.path.join('img', img)
        video = ffmpeg.input(imgFile)
        scaled_video = ffmpeg.filter(video, "scale", height = 8000, width = -1)
        transition = random.choice(possible_transtiion)
        img_name = int(img.split(".")[0])
        print(img_name)
        curr_key = timestamp.find_key_from_index(img_name)
        curr_length = (timestamp.get_time(curr_key)/2)*30 #two images so need to divide the length of time by two, times 30 fps to get the
        effect_video = ffmpeg.zoompan(scaled_video, x = transition[0], y = transition[1], d = curr_length, z = 'zoom+0.001', s='800x800')
        output = ffmpeg.output(effect_video, output_path).run()

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
    dir = 'static/vid'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    dir = 'static/generated'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    dir = 'static/audio'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
 