//=========Tokens=========
var idToken = localStorage.getItem("idToken");
var accessToken = localStorage.getItem("accessToken");

function load_existed_profile(){

    // Google API
    console.log("loading profile");
    $.ajax({
        url: "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/profile" + "?accessToken=" + accessToken,
        headers: {"Token": idToken},
        type: 'GET',
        cache: false,
        processData: false,
        contentType: 'application/json',
        success: function (r) {
            console.log(r);
            console.log(typeof r);
            var res = JSON.stringify(r);
            console.log(res);
            // TODO: check the flag condition
            // check if existing user and update inner value
            // if (res.isOldUser == true){
            //     var nickname = res.name;
            //     var gender = res.gender;
            //     var phone_num = res.cellphone;
            //     var emergency_contact = res.emergency_contact;
            // } else {
            //     var nickname = "Lion";
            //     var gender = "e.g Male";
            //     var phone_num = "e.g 0103334567";
            //     var emergency_contact = "e.g 9493334567";
            // }
            var nickname = "e.g Lion";
            var gender = "e.g Male";
            var phone_num = "e.g 0103334567";
            var emergency_contact = "e.g 9493334567";
            document.getElementById("nickname").placeholder = nickname;
            document.getElementById("gender").placeholder = gender;
            document.getElementById("phone_num").placeholder = phone_num;
            document.getElementById("emergency_contact").placeholder = emergency_contact;

            alert("Old user profile loaded");
        }
    })
}

function update_profile(){

    var nickname = document.getElementById("nickname").value;
    var gender = document.getElementById("gender").value;
    var phone_num = document.getElementById("phone_num").value;
    var emergency_contact = document.getElementById("emergency_contact").value;


    console.log("Profile API is working");

    var idToken = localStorage.getItem("idToken");
    var accessToken = localStorage.getItem("accessToken");
    
    
    var body = JSON.stringify({
        "name": nickname,
        "gender": gender,
        "cellphone": phone_num,
        "emergency_contact": emergency_contact
    })


    var API_addr = "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/profile";

    $.ajax({
        url: API_addr + "?accessToken=" + accessToken,
        headers: {"Token": idToken},
        type: 'POST',
        data: body,
        cache: false,
        processData: false,
        contentType: 'application/json',
        success: function (r) {
            console.log(r);
            alert("User profile saved");
        }
    })

    // TODO: uncomment the jump page code when others are ready 
    // window.location.href = "request_trip.html";
}