
submitted = false;
stack_logged = false
$('.alert').hide();

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) {
                c_end = document.cookie.length;
            }
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

var editor = CodeMirror.fromTextArea(document.getElementById("code1"), {
    lineNumbers: true,
    matchBrackets: true,
    mode: 'javascript'//$("#lang").val()
});

$("#stackLogin").click(function(e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: "https://stackexchange.com/oauth/dialog?client_id=11120&redirect_uri=http://localhost:5000/stack_login&scope=private_info",
        success: function(result) {
            alert('ok');
        },
        error: function(result) {
            alert('error');
        }
    });
});

$("#submit-code").click(function(e) {
    if (stack_logged){
        var code = $('#code1')[0].value;
        var title = $('#question-title-input')[0].value;
        if (!submitted){
            $.ajax({
                type: "POST",
                url: '/ask',
                data: {
                    'code': code,
                    'title': title
                },
                success: success,
            });
        }
        else{
            $('#alert-header').text('Ohhhh, Patience is key!!');
            $('.alert').removeClass('alert-success');
            $('.alert').removeClass('alert-danger');
            $('.alert').addClass('alert-warning');
            $('#alert-body').text('Your question has already been posted.. ');
            $('.alert').show();
            $(".alert").alert();
        }
    }
    else {
        $('#alert-header').text('Need Stack Overflow login');
        $('.alert').removeClass('alert-success');
        $('.alert').removeClass('alert-warning');
        $('.alert').addClass('alert-danger');

        $('#alert-body').text('We would need stackover flow login for posting this question.');
        $('.alert').show();
        $(".alert").alert();
    }
});

function success(data) {
    if (data.acknowledged){
        submitted = true;
        $('#alert-header').text('Well done');
        $('#alert-body').text('Your question has been posted.. \nLet\'s wait for the community to help you here.....');
        $('.alert').addClass('alert-success');
        $('.alert').removeClass('alert-warning');
        $('.alert').removeClass('alert-danger');

        $('.alert').show();
        $(".alert").alert();
    }

}
function switchLanguage() {
    this.editor.setOption("mode", $("#lang").val());
}

$( document ).ready(function() {
    var stack_token = getCookie('stack_token');
    if (stack_token == null || stack_token == "null" || stack_token.length == 0){
        $('#alert-header').text('Need Stack Overflow login');
        $('.alert').removeClass('alert-success');
        $('.alert').removeClass('alert-danger');
        $('.alert').addClass('alert-warning');
        $('#alert-body').text('We would need stackover flow login for posting this question.');
        $('.alert').show();
        $(".alert").alert();
    }
    else{
        stack_logged = true
    }
});

$('.alert .close').click(function(){
   $(this).parent().hide();
});
