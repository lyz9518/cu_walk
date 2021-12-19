// https://stackoverflow.com/questions/5865089/simple-javascript-loop-that-repeats-each-second/28107143
var idToken = localStorage.getItem("idToken");
var accessToken = localStorage.getItem("accessToken");
console.log(idToken);
console.log(accessToken);
$.ajax({
    url: "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/group" + "?accessToken=" + accessToken,
    headers: {"Token": idToken},
    type: 'GET',
    cache: false,
    processData: false,
    contentType: 'application/json',
    success: function (r) {
        //TODO: debug the logic here and need to optimze the structure here.
        alert("Starting Trip!");
        let res = JSON.parse(JSON.stringify(r));
        console.log(res)
        // from_location_str is the location name of departure.
        let from_location_str = res[0]['departure'];
        console.log(from_location_str)
        // to_location_str is a dict
        let to_location_str = JSON.parse(res[0]['first_user_coordinate']);
        console.log(to_location_str);
        let address = from_location_str.replaceAll(" ", "+");
        let url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address + ",+New+York,+NY&key=AIzaSyAOhQqll5NI0TUOrYbbvQbF-TdU9qYWJHM";
        $.ajax({
            url: url,
            success: function (data) {
                console.log(data)
                let result = data.results[0];
                let latCord = result.geometry.location.lat;
                let lngCord = result.geometry.location.lng;
                console.log(latCord);
                console.log(lngCord);
                // in order to get marker, from_location is in coordicnate format.
                let from_location = {"lat": latCord, "lng": lngCord};
                // to_location should be in location name, not coordinate
                let to_location = {"lat": to_location_str["latitude"], "lng": to_location_str["longitude"]};
                let myLatLng = from_location;
                console.log(from_location);
                console.log(to_location);
                // test location
                // var from_location = {lat: 40.8114424, lng: -73.9587781};
                // var to_location = {lat: 40.8105964, lng: -73.95830099999999};

                var mapOptions = {
                    // center: myLatLng,
                    zoom: 18, mapTypeId: google.maps.MapTypeId.ROADMAP, center: myLatLng
                };

                var map = new google.maps.Map(document.getElementById('googleMap'), mapOptions);
                var directionsService = new google.maps.DirectionsService();
                var directionsDisplay = new google.maps.DirectionsRenderer();
                directionsDisplay.setMap(map);

                var request = {
                    origin: from_location, destination: to_location, travelMode: google.maps.TravelMode.WALKING, //WALKING, BYCYCLING, TRANSIT
                    unitSystem: google.maps.UnitSystem.IMPERIAL
                }

                //pass the request to the route method
                let intensePointsArray = [];
                directionsService.route(request, function (result, status) {
                    directionsDisplay.setDirections(result);
                    console.log(result);

                    var points_details = [];
                    var points = result.routes[0].overview_path;
                    for (let i = 0; i < points.length; i += 5) {
                        points_details.push([points[i].lat(), points[i].lng()]);
                    }
                    for (let i = 0; i < points.length; i++) {
                        intensePointsArray.push([points[i].lat(), points[i].lng()]);
                    }
                    console.log(points_details);
                    sendPointsArrayForRiskDetection(points_details);

                });

                var lat1;
                var lng1;

                var marker = new google.maps.Marker({
                    // position: myLatLng, map, icon: image
                    position: myLatLng, map
                });

                if (navigator.geolocation) {
                    navigator.geolocation.watchPosition(showPosition);
                } else {
                    alert("Geolocation is not supported by this browser.");
                }

                function showPosition(position) {
                    // x.innerHTML="Latitude: " + position.coords.latitude +
                    // "<br>Longitude: " + position.coords.longitude;
                    lat1 = position.coords.latitude;
                    lng1 = position.coords.longitude;
                    myLatLng = {lat: lat1, lng: lng1};
                    marker.setPosition(myLatLng);
                }

                setInterval(function () {
                    sendPointsForHazardDetection(myLatLng, intensePointsArray);
                }, 10000)

                console.log(idToken);
                console.log(accessToken);
            }
        });
    }
})


function sendPointsArrayForRiskDetection(points_details) {
    $.ajax({
        url: "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/detect_rist_zone",
        headers: {"Token": idToken},
        type: 'POST',
        cache: false,
        data: JSON.stringify(points_details),
        processData: false,
        contentType: 'application/json',
        success: function (r) {
            let response = JSON.parse(r);
            let pc = "";
            let crimeRatio = "";
            for (let i = 0; i < response.length; i++) {
                pc += "Precinct" + response[i]["pc_id"] + " ";
                crimeRatio += response[i]["crime_ratio"] + " ";
            }
            let alertString = "You are about to enter following areas: " + pc + ", with crime ratio of " + crimeRatio
            alert(alertString);
        }
    })
}

function sendPointsForHazardDetection(myLatLng, intensePointsArray) {
    $.ajax({
        url: "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/hazard_detection",
        headers: {"Token": idToken},
        type: 'POST',
        cache: false,
        data: JSON.stringify(
            {
                "pointsArray": intensePointsArray,
                "curLocation": myLatLng
            }
        ),
        processData: false,
        contentType: 'application/json',
        success: function (r) {
            let response = JSON.parse(r);
            console.log(response["condition"]);
            if (response["condition"] == "safe") {
                alert("current situation safe");
            } else {
                alert("Hazard detected, message sent to your emergency contact!");
                emergency();
            }
        }
    })
}


function emergency() {
    console.log("call emergency contact");
    $.ajax({
        url: "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/emergency" + "?accessToken=" + accessToken,
        headers: {"Token": idToken},
        type: 'GET',
        cache: false,
        processData: false,
        contentType: 'application/json',
        success: function (r) {
            alert("We have sent messages to your contact! Stay safe!")
        }
    })
}

function arrived() {
    console.log("arrived home");
    $.ajax({
        url: "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/arrive" + "?accessToken=" + accessToken,
        headers: {"Token": idToken},
        type: 'GET',
        cache: false,
        processData: false,
        contentType: 'application/json',
        success: function (r) {
            alert("We have sent messages to your contact that you have arrived.")
            window.location.assign("request_trip.html")
        }
    })
}
