// https://stackoverflow.com/questions/5865089/simple-javascript-loop-that-repeats-each-second/28107143

var from_location = {lat: 40.8114424, lng: -73.9587781};
var to_location = {lat: 40.8105964, lng: -73.95830099999999};
var myLatLng = from_location;

var mapOptions = {
    // center: myLatLng,
    zoom: 18, mapTypeId: google.maps.MapTypeId.ROADMAP, center: myLatLng
};

var map = new google.maps.Map(document.getElementById('googleMap'), mapOptions);
var directionsService = new google.maps.DirectionsService();
var directionsDisplay = new google.maps.DirectionsRenderer();
directionsDisplay.setMap(map);

// function calcRoute() {
// create request

var request = {
    origin: from_location, destination: to_location, travelMode: google.maps.TravelMode.WALKING, //WALKING, BYCYCLING, TRANSIT
    unitSystem: google.maps.UnitSystem.IMPERIAL
}

//pass the request to the route method
directionsService.route(request, function (response, status) {
    // directionsDisplay.setDirections(result);

    new google.maps.DirectionsRenderer({
        map: map,
        directions: response,
        suppressMarkers: true
    });
    var leg = response.routes[0].legs[0];
    new google.maps.Marker({position: leg.start_location, icon: icons.start, title: "title", map: map})
    new google.maps.Marker({position: leg.end_location, icon: icons.end, title: "title", map: map})
});

var icons = {
    start: new google.maps.MarkerImage(
        'http://maps.google.com/mapfiles/ms/micons/blue.png',
        new google.maps.Size(44, 32),
        new google.maps.Point(0, 0),
        new google.maps.Point(22, 32)),
    end: new google.maps.MarkerImage(
        'http://maps.google.com/mapfiles/ms/micons/red.png',
        new google.maps.Size(44, 32),
        new google.maps.Point(0, 0),
        new google.maps.Point(22, 32))
};

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

function emergency() {
    console.log("call emergency contact");
    var idToken = localStorage.getItem("idToken");
    var accessToken = localStorage.getItem("accessToken");
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
    var idToken = localStorage.getItem("idToken");
    var accessToken = localStorage.getItem("accessToken");
    $.ajax({
        url: "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/arrive" + "?accessToken=" + accessToken,
        headers: {"Token": idToken},
        type: 'GET',
        cache: false,
        processData: false,
        contentType: 'application/json',
        success: function (r) {
            alert("We have sent messages to your contact that you have arrive.")
        }
    })
}