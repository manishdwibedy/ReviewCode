

var getQueryString = function ( field, url ) {
    var href = url ? url : window.location.href;
    var reg = new RegExp( '[#?&]' + field + '=([^&#]*)', 'i' );
    var string = reg.exec(href);
    return string ? string[1] : null;
};

var createCookie = function(name, value, days) {
    var expires;
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toGMTString();
    }
    else {
        expires = "";
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

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

$( document ).ready(function() {
  // Handler for .ready() called.
    $(".bottom").tooltip({
        placement: "bottom"
    });
    // console.log(window.location.href);

    var stack_token = getQueryString('access_token');
    var expires = getQueryString('expires');

    createCookie('stack_token', stack_token, 7);
    createCookie('stack_expires', expires, 7);
});

$(".summary").click(function() {
  //alert('ashutosh mishra');
  var win = window.open('/codes/' + this.id,"_self");
  win.focus();

 });
