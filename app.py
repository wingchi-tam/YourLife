from distutils.log import error
from lib2to3.pytree import convert
from flask import Flask, render_template, request
from gtts import gTTS
from icrawler.builtin import GoogleImageCrawler
app = Flask(__name__)


@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        global biography, required_vars, extra_vars
        biography, required_vars, extra_vars = generate_bio()
        # create_audio(biography)
        # generate_image()
        return render_template("index.html", biography=biography, bio_class="user_generated")
    return render_template("index.html", bio_class="hidden")

@app.route('/video')
def video():
    create_audio(biography)
    generate_image(required_vars, extra_vars)
    return render_template('video.html')

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

    #check if required vars were entered
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

    childhood_story = "Hi, my name is Ken Burns and I will be telling the story of " + required_vars["name"] + ". "+user_pronouns["possessive_adj"].capitalize()+" story begins on " + required_vars["birthday"] + " in a place \
    called " + required_vars["birthplace"] + ". Growing up in "+ required_vars["childhood_location"] + ", "+user_pronouns["possessive_adj"]+" childhood was " + required_vars["childhood_description"] + ".  "
  
    personal_story = "  Now, "+ required_vars["name"] +" resides in "+ required_vars["curr_living"] +", spending "+user_pronouns["possessive_adj"]+" free time doing the things "+user_pronouns["subject"]+" love such as \
    " +required_vars["hobbies"]+". Although "+ required_vars["name"]+" enjoys "+user_pronouns["possessive_adj"]+" life in "+required_vars["curr_living"]+", "+ required_vars["name"]+" has bigger aspirations. Sometimes, late \
    at night, when everything is quiet and the stars are perfectly aligned,"+required_vars["name"]+" dreams of "+ required_vars["goals"] +". Until then, "+ required_vars["name"]+" relishes on "+user_pronouns["possessive_adj"]+ \
    " biggest accomplishment: "+required_vars["accomplishment"]+". Living such an eventful life, it seems almost impossible to capture it all in one word, but if I had to, I would choose "+required_vars["final_word"]+"."

    school_story = ""
    if extra_vars["highschool"]:
        school_story += "  Maturing through the epic highs and lows of elementary and middle school, "+  required_vars["name"] + " finally began "+user_pronouns["possessive_adj"]+" epic adventure at "+ extra_vars["highschool"] +". "
    
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
        adulthood_story += "  The struggles of real life hit when "+user_pronouns["subject"]+" started "+user_pronouns["possessive_adj"]+" first job as a "+ extra_vars["job"]+" at "+extra_vars["job_location"]+". "
        
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
    name = "soundtrack.mp3"
    myobj = gTTS(text=biography, lang=language, slow=False)
  
    myobj.save("soundtrack.mp3")

'''
def create_photo(keywords): 
    google_crawler = GoogleImageCrawler(storage={'root_dir': 'Image_Dir'})
    google_crawler.crawl(keyword= keywords, max_num=4)
'''
def generate_image(required_vars, extra_vars):
    birthday =  required_vars["birthday"]
    birthplace =  required_vars["birthplace"]  
    childhood_location =  required_vars["childhood_location"]  
    childhood_description =  required_vars["childhood_description"]
    curr_living =  required_vars["curr_living"]  
    hobbies =  required_vars["hobbies"]  
    goals =  required_vars["goals"]  
    accomplishment =  required_vars["accomplishment"]
    pronouns = required_vars["pronouns"]
    final_word =  required_vars["final_word"]
    photoarray = ['Ken Burns', birthday + 'newspaper', birthplace, childhood_location, 'kid being' + childhood_description, curr_living, hobbies, goals, accomplishment, final_word]

    for item in photoarray: 
        google_crawler = GoogleImageCrawler(storage={'root_dir': 'img'}, parser_threads=4,
    downloader_threads=4)
        google_crawler.crawl(keyword= item, max_num=3, file_idx_offset='auto')
        