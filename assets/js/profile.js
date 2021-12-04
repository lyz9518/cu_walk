//=========Tokens=========
var idToken = localStorage.getItem("idToken");
var accessToken = localStorage.getItem("accessToken");

function load_existed_profile(){
    var existing_user = false;
    var nickname = "abc";
    var gender = "Male";
    var phone_num = "0123456789";
    var emergency_contact = "9876543210";
    // TODO: Profile Get API Here
    $.ajax({
        url: "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/profile" + "?accessToken=" + accessToken,
        headers: {"Token": idToken},
        type: 'GET',
        cache: false,
        processData: false,
        contentType: 'application/json',
        success: function (r) {
            console.log(r);
            console.log("Finally Get API is working");
        }
    })

    alert("onload test");
    if (existing_user == false){
        document.getElementById("nickname").placeholder = "";
        document.getElementById("gender").placeholder = "";
        document.getElementById("phone_num").placeholder = "";
        document.getElementById("emergency_contact").placeholder = "";
    } else {
        document.getElementById("nickname").placeholder = nickname;
        document.getElementById("gender").placeholder = gender;
        document.getElementById("phone_num").placeholder = phone_num;
        document.getElementById("emergency_contact").placeholder = emergency_contact;
    }
}

function update_profile(){

    var nickname = document.getElementById("nickname").value;
    var gender = document.getElementById("gender").value;
    var phone_num = document.getElementById("phone_num").value;
    var emergency_contact = document.getElementById("emergency_contact").value;


    console.log("Profile API is working");

    var idToken = localStorage.getItem("idToken");
    var accessToken = localStorage.getItem("accessToken");
    var API_addr = "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/profile";
    
    var body = JSON.stringify({
        "name": nickname,
        "gender": gender,
        "cellphone": phone_num,
        "emergency_contact": emergency_contact
       })

    // $.ajax({
    //     url: API_addr + "?accessToken=" + accessToken,
    //     // url: API_addr,
    //     headers: {"Token": idToken},
    //     type: 'POST',
    //     data: body,
    //     // cache: false,
    //     // processData: false,
    //     contentType: 'application/json',
    //     success: function (r) {
    //         console.log(r);
    //         console.log("YESSS");
    //         // alert("Personal profile has been recorded.");
    //     }
    // })



    $.ajax({
        url: "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/profile" + "?accessToken=" + accessToken,
        headers: {"Token": idToken},
        type: 'GET',
        cache: false,
        processData: false,
        contentType: 'application/json',
        success: function (r) {
            console.log(r);
            console.log("Finally Get API is working");
        }
    })





    // window.location.href = "request_trip.html";
}
