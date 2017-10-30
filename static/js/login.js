
// login callback
function loginCallback(response) {
    if (response.status === "PARTIALLY_AUTHENTICATED") {
      var code = response.code;
      var csrf = response.state;
      document.getElementById("code").value = code;
      document.getElementById("csrf").value = csrf;
      document.getElementById("login_success").submit();
    }
    else if (response.status === "NOT_AUTHENTICATED") {
      document.getElementById("message").innerText = "Not Authenticated";
    }
    else if (response.status === "BAD_PARAMS") {
      document.getElementById("message").innerText = "Bad Params";
    }
}
// phone form submission handler
function smsLogin() {
    var countryCode = document.getElementById("country_code").value;
    var phoneNumber = document.getElementById("phone_number").value;
    AccountKit.login(
      'PHONE',
      {countryCode: '+1', phoneNumber: ''}, // will use default values if not specified
      loginCallback
    );
}
// email form submission handler
function emailLogin() {
// var emailAddress = document.getElementById("email").value;
AccountKit.login(
  'EMAIL',
  {emailAddress: ''},
  loginCallback
);
}
