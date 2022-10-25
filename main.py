from distutils.log import error
from flask import Flask, render_template, request
app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       first_name = request.form.get("name")
       return greetings()
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

def greetings():
    #REQUIRED VARS
    name = request.form.get("name") 
    birthday =  request.form.get("childhood-birthday")
    birthplace =  request.form.get("childhood-birthplace")  
    childhood_location =  request.form.get("childhood-location")  
    job =  request.form.get("adult-job")  
    curr_living =  request.form.get("personal-location")  
    hobbies =  request.form.get("personal-hobbies")  
    goals =  request.form.get("personal-goals")  
    accomplishment =  request.form.get("personal-accomplishment")
    pronouns = request.form.get("personal-pronouns")
    required_vars = [name, birthday, birthplace, childhood_location, job, curr_living, hobbies, goals, accomplishment, pronouns]
    #check if required vars were entered
    for var in required_vars:
        if var == None:
            return "Question" +var+" unanswered, try again"

    #EXTRA VARS
    job_location =  request.form.get("adult-job-location") or ""
    childhood_description =  request.form.get("childhood-description") or ""
    highschool =  request.form.get("school-highschool") or ""
    fav_subject =  request.form.get("school-favorite-subject") or ""  
    school_activities =  request.form.get("school-activities") or ""
    college =  request.form.get("school-college-name") or ""
    major =  request.form.get("school-major") or ""
    curr_partner =  request.form.get("adult-partner-name") or "" 
    marriage_status =  request.form.get("adult-marriage-status")  or ""
    children_num =  request.form.get("adult-child-number") or ""
    child_name =  request.form.get("adult-child-name") or ""
    final_word =  request.form.get("personal-description") or ""
    extra_vars = [job_location, childhood_description, highschool, fav_subject, school_activities, college, major, curr_partner,
                    marriage_status, children_num, child_name, final_word]
    # extra_sentences = {}
    # for var in extra_vars:
    #     if var != "":
    #         extra_sentences[var] = 
    
    childhood_story = "Hi, my name is Ken Burns and I will be telling the story of " + name + ". Their story begins on " + birthday + " in a little place called " + birthplace +". \
   Although they were a difficult kid to raise, growing up in "+ childhood_location + ", their childhood was " + adjs + ". <br>"
  
    school_story = "<br> Maturing through the epic highs and lows of elementary and middle school, "+ name + " finally began their epic adventure at "+ hs +". Despite riding the \
  emotionally charged rollercoaster that high school is, nothing brightened their days more than attending "+ subject +". Moreover, when tests and classes didn’t fill "+ name + "’s schedule, \
  they really enjoyed participating in "+ activities +". Yet, as classes, tests and SATs were crunched,\
   "+ name + " pushed through the hurdles of everything required by college admissions to finally get into their dream school: "+ college +". \
   There, the parties, clubs, difficult classes, and stressful environment never stopped "+name+" from completing their degree in "+ major +". <br>"

    adulthood_story = "<br> The struggles of real life hit when they started their first job as a "+ role+" at "+job+". Currently, their relationship status is REL_STATUS - who would have thought!. \
   Their favorite activity at home is cuddling with "+curr_partner+". Despite the temptation to see other people, they’ve been loyally by each other's side since "+meeting_date+". \
   Due to poor planning, they are now stuck raising "+children_num+" child[ren]. However, they’re all growing up to be amazing people and their names are "+child_name+". <br>"

    personal_story = "<br> Now, "+ name +" resides in "+ curr_living +" where they spend their free time doing the things they love such as "+hobbies+". Although "+name+" enjoys their life\
   in "+curr_living+" doing what they love, "+name+" has bigger aspirations. Sometimes, late at night, when everything is quiet and the stars are perfectly aligned,\
    "+name+" dreams to "+ goals +". Until then, "+name+" relishes on his biggest accomplishment – when they "+big_A+". Living such an eventful life, it seems almost\
     impossible to capture it all in one word, but if I had to, I would choose s"+final_word+"."

    return childhood_story + school_story + adulthood_story + personal_story

  
