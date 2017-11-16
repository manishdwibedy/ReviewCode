
var editor = CodeMirror.fromTextArea(document.getElementById("code1"), {
    lineNumbers: true,
    matchBrackets: true,
    mode: $("#lang").val()
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
    e.preventDefault();
    // addData();
});


function switchLanguage() {
    this.editor.setOption("mode", $("#lang").val());
}

$( document ).ready(function() {
  // Handler for .ready() called.


});


