document.getElementById('b').addEventListener('click',function(){
    var tab_url = getCurrentTab();
    tab_url.then(function(result){
        if(!result.startsWith('https://www.amazon.in/')){
            document.getElementsByTagName('p')[0].innerHTML = "Not Amazon";
        }
        else{
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "http://127.0.0.1:5000/get_url");
        xhttp.send(result);
        }
        
    })
  });