var ajax = function(request_message, success_function, request_url) {
    var msg = request_message;
    var req_url = request_url || '/open'
    success_function = success_function || function(){
        console.log("success")
    }
    var a = new XMLHttpRequest();
    a.open('post', req_url);
    a.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    a.send(msg);
    a.onreadystatechange = function() {
        if(a.readyState == 4 && a.status == 200) {
            success_function();
            var message = a.responseText;
            console.log(message);
            window.location.reload()
        }
    }
}