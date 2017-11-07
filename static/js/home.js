
// Initialize Firebase
var config = {
apiKey: "AIzaSyAoskz4tPPIuZXRXkZxvzsQ59xbHssTHv0",
authDomain: "review-code-38d2b.firebaseapp.com",
databaseURL: "https://review-code-38d2b.firebaseio.com",
projectId: "review-code-38d2b",
storageBucket: "",
messagingSenderId: "585561892876"
};
firebase.initializeApp(config);

// Initialize Cloud Firestore through Firebase
var db = firebase.firestore();


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

getCode();

function getCode() {
    db.collection("code").get().then((querySnapshot) => {
        querySnapshot.forEach((doc) => {
            console.log(`${doc.id} =>`);
            console.log(doc.data());
            const data = doc.data();
            var html = '';
            html += "<div id='code'>";

            const title = data.title.length > 0 ? data.title : "No title provided";
            html += "<p>" + title + "</p>";
            html += "</div>"
            $( "div#codeHolder" ).append( html );

        });
    });
}

function addData(){
    db.collection("code").add({
        "user-id": "",
        "language": $("#lang").val(),
        "content": this.editor.getValue(),
        "timestamp": ""
    })
    // db.collection("code").add({
    //     "user-id": "a",
    //     "language": "bb",
    //     "content": "c",
    //     "timestamp": "d"
    // })
    .then(function(docRef) {
        console.log("Document written with ID: ", docRef.id);
    })
    .catch(function(error) {
        console.error("Error adding document: ", error);
    });
}


