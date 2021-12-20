//=========Tokens=========
var idToken = localStorage.getItem("idToken");
var accessToken = localStorage.getItem("accessToken");

// Glabal Var
var time = null;
var departure = null;
var destination = null;
var lat = null;
var lng = null;


function request_trip() {
    time = document.getElementById("time").value;
    departure = document.getElementById("departure").value;
    destination = document.getElementById("destination").value;
    if (time == null || time === "") {
        alert("Please select a time")
    } else if (departure == null || departure === "") {
        alert("Please select a departure building")
    } else if (destination == null || destination === "") {
        alert("Please type in a destination")
    } else {
        var address = destination.replaceAll(" ", "+");
        var url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address + ",+New+York,+NY&key=AIzaSyAOhQqll5NI0TUOrYbbvQbF-TdU9qYWJHM";
        console.log(url)
        $.ajax({
            url: url,
            success: function (data) {
                var result = data.results[0];
                lat = result.geometry.location.lat;
                lng = result.geometry.location.lng;
                console.log(lat);
                console.log(lng);
                console.log(time);
                console.log(departure);
                console.log(destination);
                console.log("Google API finished");
                var body = JSON.stringify({
                    "time": time,
                    "departure": departure,
                    "destination": {
                        "address": destination,
                        "latitude": lat,
                        "longitude": lng
                    }
                })

                // TODO: Add real data to body here
                var body = JSON.stringify({
                    "time": time,
                    "departure": departure,
                    "destination": {
                        "address": destination,
                        "latitude": lat,
                        "longitude": lng
                    }
                })

                var API_addr = "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/trip";

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
                        alert("Trip Requested!");
                    }
                })

                // TODO: uncomment the jump page code when others are ready
                window.location.assign("select_trip.html");
            }
        });
    }
}


// function edit_profile() {
//     // window.location.href = "profile.html";
//     window.location.assign("profile.html");
// }

function monitor() {
    // window.location.href = "profile.html";
    window.location.assign("select_monitor.html");
}