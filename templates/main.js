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