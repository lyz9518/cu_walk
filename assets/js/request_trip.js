//=========Tokens=========
var idToken = localStorage.getItem("idToken");
var accessToken = localStorage.getItem("accessToken");

// Glabal Var
var time = null;
var departure = null;
var destination = null;
// TODO: Implement API call
function request_trip(){
    time = document.getElementById("time").value;
    departure = document.getElementById("departure").value;
    destination = document.getElementById("destination").value;
    if (time == null || time == "" ){
        alert("Please select a time")
    } else if(departure == null || departure == "" ){
        alert("Please select a departure building")
    } else if(destination == null || destination == "" ){
        alert("Please type in a destination")
    } else {
        var address = destination.replaceAll(" ", "+");
        var url = "https://maps.googleapis.com/maps/api/geocode/json?address="+address+",+New+York,+NY&key=AIzaSyAOhQqll5NI0TUOrYbbvQbF-TdU9qYWJHM";
        console.log(url)
        $.ajax({
            url: url,
            success: function(data) {
                var result = data.results[0];
                var lat = result.geometry.location.lat;
                var lng = result.geometry.location.lng;
                console.log(lat);
                console.log(lng);
                console.log(time);
                console.log(departure);
                console.log(destination);


                window.location.href = "select_trip.html"
            }
        });
    }
}



function edit_profile(){
    window.location.href = "profile.html";
}