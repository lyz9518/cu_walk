// https://stackoverflow.com/questions/5865089/simple-javascript-loop-that-repeats-each-second/28107143
var mainLoopId = setInterval(function () {
    // Do your update stuff...
}, 40);
var myLatLng = {lat: 40.8114424, lng: -73.9587781};

var from_location = {lat: 40.8114424, lng: -73.9587781};
var to_location = {lat: 40.8105964, lng: -73.95830099999999};


var mapOptions = {
    // center: myLatLng,
    zoom: 18, mapTypeId: google.maps.MapTypeId.ROADMAP, center: myLatLng
};

var map = new google.maps.Map(document.getElementById('googleMap'), mapOptions);
var directionsService = new google.maps.DirectionsService();
var directionsDisplay = new google.maps.DirectionsRenderer();
directionsDisplay.setMap(map);


new google.maps.Marker({
    position: myLatLng, map, title: "Hello World!",
});

// function calcRoute() {
// create request

var request = {
    origin: from_location, destination: to_location, travelMode: google.maps.TravelMode.WALKING, //WALKING, BYCYCLING, TRANSIT
    unitSystem: google.maps.UnitSystem.IMPERIAL
}

//pass the request to the route method
directionsService.route(request, function (result, status) {
    //display route
    directionsDisplay.setDirections(result);
});


// // function calcRoute() {
//     //create request
//     var request = {
//         origin: from_location,
//         destination: to_location,
//         travelMode: google.maps.TravelMode.WALKING, //WALKING, BYCYCLING, TRANSIT
//         unitSystem: google.maps.UnitSystem.IMPERIAL
//     }
//
//     //pass the request to the route method
//     directionsService.route(request, function (result, status) {
//         // if (status == google.maps.DirectionsStatus.OK) {
//
//         //     //Get distance and time
//         //     const output = document.querySelector('#output');
//         //     output.innerHTML = "<div class='alert-info'>From: " + document.getElementById("from").value + ".<br />To: " + document.getElementById("to").value + ".<br /> Driving distance <i class='fas fa-road'></i> : " + result.routes[0].legs[0].distance.text + ".<br />Duration <i class='fas fa-hourglass-start'></i> : " + result.routes[0].legs[0].duration.text + ".</div>";
//
//             //display route
//         directionsDisplay.setDirections(result);
//         // } else {
//         //     //delete route from map
//         //     directionsDisplay.setDirections({ routes: [] });
//         //     //center map in London
//         //     map.setCenter(myLatLng);
//
//         //     //show error message
//         //     output.innerHTML = "<div class='alert-danger'><i class='fas fa-exclamation-triangle'></i> Could not retrieve driving distance.</div>";
//         // }
//     });
//
// // }


//create autocomplete objects for all inputs
// var options = {
//     types: ['(cities)']
// }

// var input1 = document.getElementById("from");
// var autocomplete1 = new google.maps.places.Autocomplete(input1, options);

// var input2 = document.getElementById("to");
// var autocomplete2 = new google.maps.places.Autocomplete(input2, options);


function emergency() {
    console.log("call emergency contact");
}

function arrived() {
    console.log("arrived home");
}