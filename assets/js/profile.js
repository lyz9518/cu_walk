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

function update_profile(){
    console.log("Profile API is working");

    var idToken = "eyJraWQiOiJ4Zk9sZTU2ZG5kTmNNUXY5eVMyeTAxeFFLM251TXFtakJZQlhmbkJVUFFrPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiZlJySmhwQ3RIZ2RlTjhzWmZjeEJ1ZyIsInN1YiI6ImIwMmUzZmQ5LTQzYTYtNDhiNS04YTJmLWE5NzdlNDE0NWQ1NCIsImF1ZCI6InV1ZG9wNWppNGE5MzBoZDJsZDhnaW80cW4iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2Mzg1MDE0NzMsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xXzByTnVvTnVjNCIsImNvZ25pdG86dXNlcm5hbWUiOiJxcSIsImV4cCI6MTYzODUwNTA3MywiaWF0IjoxNjM4NTAxNDczLCJqdGkiOiJiMjUxY2E2Ni01MGJjLTQwMGItODNkMy01MGRlZTkyMzlhMTQiLCJlbWFpbCI6InFxNzI4OTc3ODYyQGdtYWlsLmNvbSJ9.elsImfgVJ33uCtSVvdRcdVIv_IheeSbVX9cC7sJXRWUe_E6ukOrNAKn9Cl9JvqnGbbD6YciqYn4P0HALc4-R2fmkEvjuovcBN9acewz3k9sPesY7EOo3JTbYeFa6CX-OKpPdzy71xZ-aQvvbH1dYqJszCLgl699dOy8rUqvt5sw2ncDcNQkXpf28ISuffXQCHLhM1LCFaNdmjwKTDywZnkOTLoRBuFrVxr1LMZbmaeWJ2sMaSahMvScH1n6ern9zQiBuV6SoZBko0KhLUOrj0prvz9Q3C3ffOKaVbC-mog5Kq_Y_lglj2m3Si6HTHhpDd-HRNsgR_znn3LVPwdY1hg";
    var accessToken = "eyJraWQiOiI4UkY1TDZtdEhGQlBFRkNaSFFPeGxFY2p6azVIVGNaQWZ6a1lLUG9LS3VzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJiMDJlM2ZkOS00M2E2LTQ4YjUtOGEyZi1hOTc3ZTQxNDVkNTQiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIHBob25lIG9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXV0aF90aW1lIjoxNjM4NTAxNDczLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJleHAiOjE2Mzg1MDUwNzMsImlhdCI6MTYzODUwMTQ3MywidmVyc2lvbiI6MiwianRpIjoiZmZhN2ZiNWUtOTVlNC00OGMzLThkNzktYjcxZDU3OGE4NTc0IiwiY2xpZW50X2lkIjoidXVkb3A1amk0YTkzMGhkMmxkOGdpbzRxbiIsInVzZXJuYW1lIjoicXEifQ.j9vpIvohYb0ZCs3JFgajViuT4DB-FB90LwsN_kekmzBKOnyQwBXNDDXeEcRdPLiGJel2deY7vxW-kituYeDBbyI_OspQi8a81umIXguvT1tJUjcLIgeQhivHc1cFj77Vrp-wa6x-uvGiOaCAzF2ZMgTl5d1cT-ngekSMsZq5d6lp19oNaaR-R993Nt89hQ7mFiOLwV4w_8YW0kY8_h3wK225XgmfU6qIw8W9D9p3lqRAi_eD1RhDL7BMuezxmlpmX5vgSLPuIVtKaLkzZc_CSbRkiYjQ3W9kVPheKWt6c9yAYf8_3pDuVyuhwJZImrWtyC_yaqAcGV0HNUt0Fr8wXA";
    var API_addr = "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/profile";
    
    var body = {
        nickname: "TEST",
        gender: "male",
        phone_num: "9491234567",
        emergency_contact: "9499876543"
    } 
    
    $.ajax({
    //   url: API_addr + "?accessToken=" + accessToken,
        url: API_addr,
        // headers: {"Token": idToken},
        //   body: ,
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