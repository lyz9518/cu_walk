// https://stackoverflow.com/questions/5865089/simple-javascript-loop-that-repeats-each-second/28107143
var idToken = localStorage.getItem("idToken");
var accessToken = localStorage.getItem("accessToken");
console.log(idToken);
console.log(accessToken);





// let response = {
//     "users": [{"abc": [123,123]}, {"abc": [123,123]}, {"abc": [123,123]}, {"abc": [123,123]}]
// }

$.ajax({
    url: "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/monitor" + "?accessToken=" + accessToken,
    headers: {"Token": idToken},
    type: 'GET',
    cache: false,
    processData: false,
    contentType: 'application/json',
    success: function (r) {
        let response = r;
        // if (response["users"] == null || response["users"].length == 0) {
        //
        // }
    }
})






