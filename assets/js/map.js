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
                directionsService.route(request, function (result, status) {
                    directionsDisplay.setDirections(result);
                    console.log(result);

                    var points_details = [];
                    var points = result.routes[0].overview_path;
                    for (let i = 0; i<points.length; i++){
                        points_details.push([points[i].lat(), points[i].lng()]);
                    }
                    console.log(points_details)

                    // var polyline = require('google-polyline');
                    
                    // console.log(points);
                    // console.log(points.length);
                    // new google.maps.DirectionsRenderer({
                    //     map: map,
                    //     directions: response,
                    //     suppressMarkers: true
                    // });
                    // var leg = response.routes[0].legs[0];
                    // new google.maps.Marker({position: leg.start_location, icon: icons.start, title: "title", map: map})
                    // new google.maps.Marker({position: leg.end_location, icon: icons.end, title: "title", map: map})
                });

                // var icons = {
                //     start: new google.maps.MarkerImage(
                //         'http://maps.google.com/mapfiles/ms/micons/blue.png',
                //         new google.maps.Size(44, 32),
                //         new google.maps.Point(0, 0),
                //         new google.maps.Point(22, 32)),
                //     end: new google.maps.MarkerImage(
                //         'http://maps.google.com/mapfiles/ms/micons/red.png',
                //         new google.maps.Size(44, 32),
                //         new google.maps.Point(0, 0),
                //         new google.maps.Point(22, 32))
                // };

                var lat1;
                var lng1;

                // const image =
                //     "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";

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

                console.log(idToken);
                console.log(accessToken);
            }
        });
    }
})


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
