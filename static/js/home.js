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