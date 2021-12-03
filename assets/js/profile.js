function update_profile(){
    var nickname = document.getElementById(nickname).value;
    var gender = document.getElementById(gender).value;
    var phone_num = document.getElementById(phone_num).value;
    var emergency_contact = document.getElementById(emergency_contact).value;

    //TODO: API Here
    console.log(nickname);
    console.log(gender);
    console.log(phone_num);
    console.log(emergency_contact);
}

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