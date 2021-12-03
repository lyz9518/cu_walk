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
        // TODO: API Call here
        console.log(time);
        console.log(departure);
        console.log(destination);
        
        // Jump to ready page
        window.location.href = "select_trip.html";
    }
}