
// ======================Count Down Timer============================
// Set the date we're counting down to
// TODO:API get time here
var departure_time = "Jan 5, 2022 15:37:25"; 
var countDownDate = new Date(departure_time).getTime();

// Update the count down every 1 second
var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();
    
  // Find the distance between now and the count down date
  var distance = countDownDate - now;
    
  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
  // Output the result in an element with id="timer"
  document.getElementById("timer").innerHTML = days + "d " + hours + "h "
  + minutes + "m " + seconds + "s ";
    
  // If the count down is over, write some text 
  if (distance < 0) {
    clearInterval(x);
    document.getElementById("timer").innerHTML = "Time to Go My Friend!";
  }
}, 1000);
// ==================================================================

function ready(){
    // TODO: API Here
    console.log("User is Ready");
    //Jump to map.html
    window.location.href = "map.html";
}

function cancel(){
    // TODO: API Here
    console.log("User cancelled the trip");
    //Jump to request_trip.html
    window.location.href = "request_trip.html";
}
