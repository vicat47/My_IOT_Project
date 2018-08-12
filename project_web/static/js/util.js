var ajax = function(request_message, success_function) {
    msg = request_message;
    success_function == success_function || function(){
        return 0;
    }
    var a = new XMLHttpRequest();
    a.onreadystatechange = function() {
        if(a.readyStat == 4 && a.status == 200) {
            success_function();
            var message = a.responseText;
            console.log(message);
        }
    }
    a.open('post', '/open');
    a.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    a.send(msg);
}