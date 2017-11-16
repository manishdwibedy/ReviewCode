
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
});

$(".summary").click(function() {
              //alert('ashutosh mishra');
              var win = window.open('/codes/' + this.id, '_blank');
              win.focus();

         });
