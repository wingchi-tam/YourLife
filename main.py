from distutils.log import error
from lib2to3.pytree import convert
from flask import Flask, render_template, request
app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       biography = greetings()
       return render_template("index.html", biography=biography)
    return render_template("index.html")

@app.route('/video')
def video():
    return render_template('video.html')

if __name__ == '__main__':
    app.run(debug=True)

def greetings():
    #REQUIRED VARS
    name = request.form.get("name") 
    birthday =  request.form.get("childhood-birthday")
    birthplace =  request.form.get("childhood-birthplace")  
    childhood_location =  request.form.get("childhood-location")  
    childhood_description =  request.form.get("childhood-description")
    curr_living =  request.form.get("personal-location")  
    hobbies =  request.form.get("personal-hobbies")  
    goals =  request.form.get("personal-goals")  
    accomplishment =  request.form.get("personal-accomplishment")
    pronouns = request.form.get("personal-pronouns")
    final_word =  request.form.get("personal-description")

    required_vars = [name, birthday, birthplace, childhood_location, childhood_description, curr_living, hobbies, 
                        goals, accomplishment, pronouns, final_word]

    #check if required vars were entered
    for var in required_vars:
        if var == None:
            print(var)
            return "Question" +var+" unanswered, try again"

    user_pronouns = convert_pronouns(pronouns)

    #EXTRA VARS
    highschool =  request.form.get("school-highschool")
    fav_subject =  request.form.get("school-favorite-subject")   
    school_activities =  request.form.get("school-activities")  
    college =  request.form.get("school-college-name")  
    major =  request.form.get("school-major")  
    job =  request.form.get("adult-job")  
    job_location =  request.form.get("adult-job-location")  
    curr_partner =  request.form.get("adult-partner-name")   
    relationship_status =  request.form.get("adult-relationship-status")   
    children_num =  request.form.get("adult-child-number")  
    child_name =  request.form.get("adult-child-name")  
    extra_vars = [highschool, fav_subject, school_activities, college, major, job, job_location, curr_partner,
                    relationship_status, children_num, child_name, final_word]

    
    childhood_story = "Hi, my name is Ken Burns and I will be telling the story of " + name + ". "+user_pronouns["possessive_adj"].capitalize()+" story begins on " + birthday + " in a little place called " + birthplace +". \
   Although "+user_pronouns["subject"]+" "+user_pronouns["verb"]+" a difficult kid to raise, growing up in "+ childhood_location + ", "+user_pronouns["possessive_adj"]+" childhood was " + childhood_description + ". <br>"
  
    personal_story = "<br> Now, "+ name +" resides in "+ curr_living +", spending "+user_pronouns["possessive_adj"]+" free time doing the things "+user_pronouns["subject"]+" love such as "+hobbies+". \
    Although "+name+" enjoys "+user_pronouns["possessive_adj"]+" life in "+curr_living+", "+name+" has bigger aspirations. Sometimes, late at night, when everything is quiet and the stars are perfectly aligned,\
    "+name+" dreams of "+ goals +". Until then, "+name+" relishes on "+user_pronouns["possessive_adj"]+" biggest accomplishment: "+accomplishment+". Living such an eventful life, it seems almost\
     impossible to capture it all in one word, but if I had to, I would choose "+final_word+"."

    school_story = ""
    if highschool:
        school_story += "<br> Maturing through the epic highs and lows of elementary and middle school, "+ name + " finally began "+user_pronouns["possessive_adj"]+" epic adventure at "+ highschool +". "
    
    if fav_subject:
        school_story += "Despite riding the emotionally charged rollercoaster that high school is, nothing brightened "+user_pronouns["possessive_adj"]+" days more than attending "+ fav_subject +". "
        
    if school_activities:
        school_story += "Moreover, when tests and classes didn't fill "+ name + "'s schedule, "+user_pronouns["subject"]+" really enjoyed participating in "+ school_activities +". "
        
    if college:
        school_story += "Yet, as classes, tests and SATs were crunched, "+ name + " pushed through the hurdles of everything required by college admissions to finally get into "+user_pronouns["possessive_adj"]+" dream school: "+ college +". "

    if major:
        school_story += "There, the parties, clubs, difficult classes, and stressful environment never stopped "+name+" from completing "+user_pronouns["possessive_adj"]+" degree in "+ major +". "

    adulthood_story = ""

    if job and job_location:
        adulthood_story += "<br> The struggles of real life hit when "+user_pronouns["subject"]+" started "+user_pronouns["possessive_adj"]+" first job as a "+ job+" at "+job_location+". "
        
    if relationship_status:
        adulthood_story += "Currently, "+user_pronouns["possessive_adj"]+" relationship status is "+relationship_status+" - who would have thought! "

    if curr_partner:
        adulthood_story += user_pronouns["possessive_adj"].capitalize()+" favorite activity at home is cuddling with "+curr_partner+". " 
        
    if children_num != "0":
        adulthood_story += user_pronouns["subject"].capitalize()+" are now raising "+children_num+" child[ren]. However, they're all growing up to be amazing people and their names are "+child_name+". <br>"


    return childhood_story + school_story + adulthood_story + personal_story

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

