// function update_profile(){
//     var nickname = document.getElementById(nickname).value;
//     var gender = document.getElementById(gender).value;
//     var phone_num = document.getElementById(phone_num).value;
//     var emergency_contact = document.getElementById(emergency_contact).value;

//     //TODO: API Here
//     console.log(nickname);
//     console.log(gender);
//     console.log(phone_num);
//     console.log(emergency_contact);
// }

function load_existing_profile(){
    var existing_user = false;
    var nickname = "abc";
    var gender = "Male";
    var phone_num = "0123456789";
    var emergency_contact = "9876543210";
    // TODO: Profile Get API Here
    // Assign the vars above.


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
    var API_addr = "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/login";
    
    var body = {
        nickname: "TEST",
        gender: "male",
        phone_num: "9491234567",
        emergency_contact: "9499876543"
    } 
    
    $.ajax({
        url: API_addr + "?accessToken=" + accessToken,
        headers: {"Token": idToken},
        type: 'GET',
        // cache: false,
        // processData: false,
        contentType: 'application/json',
        success: function (r) {
            console.log(r);
        }
    })


    // $.ajax({
    //     // url: "https://szi6xpfx7g.execute-api.us-east-1.amazonaws.com/put_v2_test/upload?" +
    //     //     "custom_label=" + custom_label + "&file_name=" + file_name + "&ContentEncoding=base64",
    //     url: "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/profile?name=“ABC”&gender="abc"&phone="abc"&contact="abc",
    //     type: 'POST',
    //     headers: {'Content-Type': "application/json"},
    //     // data: fileBody,
    //     // cache: false,
    //     // dataType: 'html',
    //     // processData: false,
    //     contentType: "application/json",
    //     success: function (r) {
    //         console.log(r)
    //     }
    // })
}