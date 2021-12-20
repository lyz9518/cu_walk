// https://stackoverflow.com/questions/5865089/simple-javascript-loop-that-repeats-each-second/28107143
var idToken = localStorage.getItem("idToken");
var accessToken = localStorage.getItem("accessToken");
console.log(idToken);
console.log(accessToken);


var from_location = "Fu Foundation School of Engineering and Applied Science" + "New York, NY";
var to_location = "520 West 123rd St" + "New York, NY";

myLatLng = {lat:40.811547947831826, lng:-73.95883773895977};
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

});

// let response = {
//     "users": [{"abc": [123,123]}, {"abc": [123,123]}, {"abc": [123,123]}, {"abc": [123,123]}]
// }

// $.ajax({
//     url: "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/monitor" + "?accessToken=" + accessToken,
//     headers: {"Token": idToken},
//     type: 'GET',
//     cache: false,
//     processData: false,
//     contentType: 'application/json',
//     success: function (r) {
//         let response = r;
//         // if (response["users"] == null || response["users"].length == 0) {
//         //
//         // }
//     }
// })

var lat1;
var lng1;

myLatLng = {lat: lat1, lng: lng1};
var image_me = "./assets/picture/marker_me.png";
var marker = new google.maps.Marker({
    // position: myLatLng, map, icon: image
    position: myLatLng, map, icon: image_me,
});

// if (navigator.geolocation) {
//     navigator.geolocation.watchPosition(showPosition);
// } else {
//     alert("Geolocation is not supported by this browser.");
// }

// function showPosition(position) {
//     // x.innerHTML="Latitude: " + position.coords.latitude +
//     // "<br>Longitude: " + position.coords.longitude;
//     lat1 = position.coords.latitude;
//     lng1 = position.coords.longitude;
//     myLatLng = {lat: lat1, lng: lng1};
//     marker.setPosition(myLatLng);
// }




