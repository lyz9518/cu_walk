// https://stackoverflow.com/questions/5865089/simple-javascript-loop-that-repeats-each-second/28107143
let idToken = localStorage.getItem("idToken");
let accessToken = localStorage.getItem("accessToken");
console.log(idToken);
console.log(accessToken);

myLatLng = {lat: 40.811547947831826, lng: -73.95883773895977};
let mapOptions = {
    zoom: 18, mapTypeId: google.maps.MapTypeId.ROADMAP, center: myLatLng
};
let map = new google.maps.Map(document.getElementById('googleMap'), mapOptions);

$.ajax({
    url: "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/monitor" + "?accessToken=" + accessToken,
    headers: {"Token": idToken},
    type: 'GET',
    cache: false,
    processData: false,
    contentType: 'application/json',
    success: function (r) {
        var routes = r.routes;
        
        for (let i = 0; i<routes.length; i++){
            let from_location = routes[i][1]+"New York, NY";
            let to_location = routes[i][2]+"New York, NY";
            let directionsService = new google.maps.DirectionsService();
            let directionsDisplay = new google.maps.DirectionsRenderer();
            directionsDisplay.setMap(map);
            let request = {
                origin: from_location, destination: to_location, travelMode: google.maps.TravelMode.WALKING, //WALKING, BYCYCLING, TRANSIT
                unitSystem: google.maps.UnitSystem.IMPERIAL
            }
            directionsService.route(request, function (result, status) {
                directionsDisplay.setDirections(result);
                console.log(result);
            });
        }
    }
})




// let from_location1 = "Fu Foundation School of Engineering and Applied Science" + "New York, NY";
// let to_location1 = "520 West 121rd St" + "New York, NY";
// let directionsService1 = new google.maps.DirectionsService();
// let directionsDisplay1 = new google.maps.DirectionsRenderer();
// directionsDisplay1.setMap(map);
// let request1 = {
//     origin: from_location1, destination: to_location1, travelMode: google.maps.TravelMode.WALKING, //WALKING, BYCYCLING, TRANSIT
//     unitSystem: google.maps.UnitSystem.IMPERIAL
// }
// directionsService1.route(request1, function (result, status) {
//     directionsDisplay1.setDirections(result);
//     console.log(result);
// });


//pass the request to the route method
let intensePointsArray = [];




let image_me = "./assets/picture/marker_me.png";
let markerList;
// let response = {
//     "users": [["abc", 123, 123], ["abc", 123, 123]]
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

function createNewMarker(LatLng, name) {
    let contentString ="<div>" + name +"</div>";
    let infoWindow = new google.maps.InfoWindow({
        content: contentString,
    });
    let marker = new google.maps.Marker({
        // position: myLatLng, map, icon: image
        position: LatLng, map, icon: image_me,
    });
    // check if there is problem of event listener

    marker.addListener("click", function(){
        infoWindow.open({
            anchor: marker,
            map,
            shouldFocus: false,
        });
    });
    
    // marker.addEventListener("click", function(){
    //     infoWindow.open({
    //         anchor: marker,
    //         map,
    //         shouldFocus: false,
    //     });
    // });
    return marker;
}

function updateMarker(r) {
    if (r == null || r["users"] == null) {
        alert("Response is null!");
        return;
    } else if (r["users"].length === 0) {
        alert("Response is empty!");
        return;
    }

    if (markerList == null) {
        markerList = [];
        for (let i = 0; i < r["users"].length; i++) {
            let initialLatLng = {lat: r["users"][i][1], lng: r["users"][i][2]};
            let name = r["users"][i][0];
            markerList.push(createNewMarker(initialLatLng, name));
        }
    } else if (r["users"].length > markerList.length) {
        for (let i = 0; i < r["users"].length; i++) {
            let initialLatLng = {lat: r["users"][i][1], lng: r["users"][i][2]};
            let name = r["users"][i][0];
            if (i < markerList.length) {
                markerList[i].setMap(null);
                markerList[i] = createNewMarker(initialLatLng, name);
            } else {
                markerList.push(createNewMarker(initialLatLng, name));
            }
        }
    } else if (r["users"].length >= markerList.length) {
        let i;
        for (i = 0; i < r["users"].length; i++) {
            let initialLatLng = {lat: r["users"][i][1], lng: r["users"][i][2]};
            let name = r["users"][i][0];
            if (i < markerList.length) {
                markerList[i].setMap(null);
                markerList[i] = createNewMarker(initialLatLng, name);
            } else {
                markerList.push(createNewMarker(initialLatLng, name));
            }
        }
        for (; i < markerList.length; i++) {
            markerList[i].setMap(null);
            markerList.splice(i, 1);
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




