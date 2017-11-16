
submitted = false;
$('.alert').hide();

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
        $('.alert').addClass('alert-warning');
        $('#alert-body').text('Your question has already been posted.. ');
        $('.alert').show();
        $(".alert").alert();
    }
    // addData();
});

function success(data) {
    if (data.acknowledged){
        submitted = true;
        $('#alert-header').text('Well done');
        $('#alert-body').text('Your question has been posted.. \nLet\'s wait for the community to help you here.....');
        $('.alert').addClass('alert-success');
        $('.alert').removeClass('alert-warning');
        $('.alert').show();
        $(".alert").alert();
    }
    else{

    }
    console.log(data);
}
function switchLanguage() {
    this.editor.setOption("mode", $("#lang").val());
}

$( document ).ready(function() {

});

$('.alert .close').click(function(){
   $(this).parent().hide();
});
