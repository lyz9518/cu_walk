// https://stackoverflow.com/questions/5865089/simple-javascript-loop-that-repeats-each-second/28107143
let idToken = localStorage.getItem("idToken");
let accessToken = localStorage.getItem("accessToken");
console.log(idToken);
console.log(accessToken);


let from_location = "Fu Foundation School of Engineering and Applied Science" + "New York, NY";
let to_location = "520 West 123rd St" + "New York, NY";

myLatLng = {lat: 40.811547947831826, lng: -73.95883773895977};
let mapOptions = {
    // center: myLatLng,
    zoom: 18, mapTypeId: google.maps.MapTypeId.ROADMAP, center: myLatLng
};

let map = new google.maps.Map(document.getElementById('googleMap'), mapOptions);
let directionsService = new google.maps.DirectionsService();
let directionsDisplay = new google.maps.DirectionsRenderer();
directionsDisplay.setMap(map);

let request = {
    origin: from_location, destination: to_location, travelMode: google.maps.TravelMode.WALKING, //WALKING, BYCYCLING, TRANSIT
    unitSystem: google.maps.UnitSystem.IMPERIAL
}

//pass the request to the route method
let intensePointsArray = [];
directionsService.route(request, function (result, status) {
    directionsDisplay.setDirections(result);
    console.log(result);

});

let image_me = "./assets/picture/marker_me.png";
let marker;
let markerList;
// let response = {
//     "users": [{"abc": [123,123]}, {"abc": [123,123]}, {"abc": [123,123]}, {"abc": [123,123]}]
// }
setInterval(function () {
    $.ajax({
        url: "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/monitor" + "?accessToken=" + accessToken,
        headers: {"Token": idToken},
        type: 'GET',
        cache: false,
        processData: false,
        contentType: 'application/json',
        success: function (r) {
            updateMarker(r);
        }
    })
}, 5000)

function updateMarker(r) {
    if (markerList == null) {
        markerList = [];
        for (let i = 0; i < r["users"].length; i++) {
            let initialLatLng = {lat: r["users"][0], lng: r["users"][1]};
            markerList.push(new google.maps.Marker({
                // position: myLatLng, map, icon: image
                position: initialLatLng, map, icon: image_me,
            }));
        }
    } else {
        // check whether new user join in the list
        if (r["users"].length > markerList.length) {
            for (let i = 0; i < r["users"].length; i++) {
                if (i < markerList.length) {
                    let curLatLng = {lat: r["users"][0], lng: lng1};
                    markerList[i].setPosition()
                }
            }
        } else if (r["users"].length < markerList.length) {

        }
    }
}


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




