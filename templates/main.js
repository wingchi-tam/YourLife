function countWord() {
    var words = document.getElementById("bio_text").value;

    var count = 0;

    var split = words.split(' ');

    for (var i = 0; i < split.length; i++) {
        if (split[i] != "") {
            count += 1;
        }
    }

    document.getElementById("wordCount")
        .innerHTML = count;
}

function greetings() {
  var name = document.getElementById("name_text").value;
  var date = document.getElementById("childhood-birthday").value;
  var place = document.getElementById("childhood-birthplace").value;
  var place2 = document.getElementById("childhood-location").value;
  var adjs = document.getElementById("childhood-description").value;
  var hs = document.getElementById("school-highschool").value;
  var subject = document.getElementById("school-favorite-subject").value;
  var activities = document.getElementById("school-activities").value;
  var college = document.getElementById("school-college-name").value;
  var major = document.getElementById("school-major").value;
  var role = document.getElementById("adult-job").value;
  var job = document.getElementById("adult-job-location").value;
  var curr_partner = document.getElementById("adult-partner-name").value;
  var meeting_date = document.getElementById("adult-marriage-status").value;
  var children_num = document.getElementById("adult-child-number").value;
  var child_name = document.getElementById("adult-child-name").value;
  var curr_living = document.getElementById("personal-location").value;
  var hobbies = document.getElementById("personal-hobbies").value;
  var goals = document.getElementById("personal-goals").value;
  var big_A = document.getElementById("personal-accomplishment").value;
  var final_word = document.getElementById("personal-description").value;

  document.write("Hi, my name is Ken Burns and I will be telling the story of " + name + ". Their story begins on " + date + " in a little place called " + place +". \
   Although they were a difficult kid to raise, growing up in "+ place2 + ", their childhood was " + adjs + ". <br>");
  
  document.write("<br> Maturing through the epic highs and lows of elementary and middle school, "+ name + " finally began their epic adventure at "+ hs +". Despite riding the \
  emotionally charged rollercoaster that high school is, nothing brightened their days more than attending "+ subject +". Moreover, when tests and classes didn’t fill "+ name + "’s schedule, \
  they really enjoyed participating in "+ activities +". Yet, as classes, tests and SATs were crunched,\
   "+ name + " pushed through the hurdles of everything required by college admissions to finally get into their dream school: "+ college +". \
   There, the parties, clubs, difficult classes, and stressful environment never stopped "+name+" from completing their degree in "+ major +". <br>"); 

  document.write("<br> The struggles of real life hit when they started their first job as a "+ role+" at "+job+". Currently, their relationship status is REL_STATUS - who would have thought!. \
   Their favorite activity at home is cuddling with "+curr_partner+". Despite the temptation to see other people, they’ve been loyally by each other's side since "+meeting_date+". \
   Due to poor planning, they are now stuck raising "+children_num+" child[ren]. However, they’re all growing up to be amazing people and their names are "+child_name+". <br>");

  document.write("<br> Now, "+ name +" resides in "+ curr_living +" where they spend their free time doing the things they love such as "+hobbies+". Although "+name+" enjoys their life\
   in "+curr_living+" doing what they love, "+name+" has bigger aspirations. Sometimes, late at night, when everything is quiet and the stars are perfectly aligned,\
    "+name+" dreams to "+ goals +". Until then, "+name+" relishes on his biggest accomplishment – when they "+big_A+". Living such an eventful life, it seems almost\
     impossible to capture it all in one word, but if I had to, I would choose s"+final_word+".");

  }

document.getElementById("bio_text").addEventListener("keypress", function(evt){

    var words = this.value.split(/\s+/);
    var numWords = words.length;    
    var maxWords = 500;
    
    if(numWords > maxWords){
      evt.preventDefault(); 
    }
  });

  const form  = document.getElementById('inputs');

  form.addEventListener('submit', (event) => {
    console.log("Hello");
});