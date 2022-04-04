document.getElementById('b').addEventListener('click',function(){
    var tab_url = getCurrentTab();
    tab_url.then(function(result){
        if(!result.startsWith('https://www.amazon.in/')){
            document.getElementsByTagName('p')[0].innerHTML = "Not Amazon";
        }
        else{
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == XMLHttpRequest.DONE) {
                document.getElementsByTagName('p')[0].innerHTML = xhttp.responseText;
                document.getElementById('b').innerHTML = 'Click';
            }
            else {
                document.getElementsByTagName('p')[0].innerHTML = 'Please wait while we proccess the data.';
                document.getElementById('b').innerHTML = '<button class="btn btn-primary" type="button" disabled> <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span><span class="sr-only">Loading...</span> </button>';
            }
        }
        xhttp.open("POST", "http://127.0.0.1:5000/get_url");
        xhttp.send(result);
        }
        
    })
  });