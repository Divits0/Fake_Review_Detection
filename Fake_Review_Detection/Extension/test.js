document.getElementById('submit-button').addEventListener('click',function(){
    var tab_url = getCurrentTab();
    tab_url.then(function(result){
        if(!result.startsWith('https://www.amazon.in/')){
            document.getElementsByTagName('p')[0].innerHTML = "Not Amazon";
        }
        else{
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == XMLHttpRequest.DONE) {
                if(xhttp.responseText == "Something went wrong."){
                    document.getElementsByTagName('p')[0].innerHTML = xhttp.responseText;
                    document.getElementById('submit-button').innerHTML = 'Click';
                }
                else{
                    if(xhttp.responseText == "Less Likely to have Fake reviews"){
                        document.getElementById('result').style.color = "#14C38E"; 
                    }
                    else if(xhttp.responseText == "Highly Likely to have Fake reviews"){
                        document.getElementById('result').style.color = "#F32424";
                    }
                    document.getElementById('result').innerHTML = xhttp.responseText;
                    document.querySelector('.feedback-container').style.display = 'block';
                    document.getElementById('submit-button').innerHTML = 'Click';
                    document.querySelector('.parent-container').style.display = 'none';
                }
            }
            else {
                document.getElementsByTagName('p')[0].innerHTML = 'Please wait while we proccess the data.';
                document.getElementById('submit-button').innerHTML = '<button class="btn btn-primary" type="button" disabled> <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span><span class="sr-only">Loading...</span> </button>';
            }
        }
        xhttp.open("POST", "http://127.0.0.1:5000/get_url");
        xhttp.send(result);
        }
    
    })


  });
document.getElementById('thumbs-up').addEventListener('click',function(){
    document.querySelector('.chrome-extension').style.display = 'none';
    document.querySelector('.feedback-message').style.display = 'block';
    send_feedback(1);

});

document.getElementById('thumbs-down').addEventListener('click',function(){
    document.querySelector('.chrome-extension').style.display = 'none';
    document.querySelector('.feedback-message').style.display = 'block';
    send_feedback(0);
});

document.getElementById('home-button').addEventListener('click',function(){
    document.getElementsByTagName('p')[0].innerHTML = 'Click to check the likelihood of fake reviews';
    document.querySelector('.feedback-message').style.display = 'none';
    document.querySelector('.chrome-extension').style.display = 'block';
    document.querySelector('.parent-container').style.display = 'block';
    document.querySelector('.feedback-container').style.display = 'none';

});

function send_feedback(user_feedback){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "http://127.0.0.1:5000/get_feedback");
    xhttp.send(user_feedback);
}