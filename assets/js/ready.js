//=========Tokens=========
var idToken = localStorage.getItem("idToken");
var accessToken = localStorage.getItem("accessToken");


// ======================Count Down Timer============================
// Set the date we're counting down to
// TODO:API get time here

var idToken = localStorage.getItem("idToken");
    var accessToken = localStorage.getItem("accessToken");

    var API_addr = "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/getdeparturetime";

    $.ajax({
      url: API_addr + "?accessToken=" + accessToken,
      headers: {"Token": idToken},
      type: "GET",
      cache: false,
      processData: false,
      contentType: 'application/json',
      success: function (r) {
        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0');
        if(mm=="01"){mm="Jan"}else if(mm=="02"){mm="Feb"}else if(mm=="03"){mm="Mar"}else if(mm=="04"){mm="Apr"}else if(mm=="05"){mm="May"}else if(mm=="06"){mm="Jun"}
        else if(mm=="07"){mm="Jul"}else if(mm=="08"){mm="Aug"}else if(mm=="09"){mm="Sep"}else if(mm=="10"){mm="Oct"}else if(mm=="11"){mm="Nov"}else if(mm=="12"){mm="Dec"}
        var yyyy = today.getFullYear();
        today = mm + ' ' + dd + ', ' + yyyy;
        tomorrow = mm + ' ' + String(parseInt(dd)+1) + ', ' + yyyy;

        const convertTime12to24 = (time12h) => {
          const [time, modifier] = time12h.split(' ');
        
          let [hours, minutes] = time.split(':');
        
          if (hours === '12') {
            hours = '00';
          }
        
          if (modifier === 'PM') {
            hours = parseInt(hours, 10) + 12;
          }
        
          return `${hours}:${minutes}:00`;
        }

        var departure_time = r.time; //"Dec 4, 2021 23:00:00";  11:00 PM
        var signal = r.code;
        document.getElementById("signal").innerHTML = signal; 
        departure_time = convertTime12to24(departure_time);
        var departure_today = today + " "+departure_time;
        var departure_tomorrow = tomorrow + " "+departure_time;
        console.log(departure_today);
        
        var countDownDate = new Date(departure_today).getTime();
        console.log(countDownDate);
        var now = new Date().getTime();
        if (countDownDate <now){
          // countDownDate  = new Date().setDate(countDownDate +1);
          countDownDate = new Date(departure_tomorrow).getTime();
          console.log(departure_tomorrow);
          console.log(countDownDate);
        }
        console.log(countDownDate );
        // Update the count down every 1 second
        var x = setInterval(function() {
        
          // Get today's date and time
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
            window.location.assign("map.html");
          }
        }, 1000);
      }
    })







// ==================================================================



function user_ready(){
    // TODO: API Here
    console.log("User is Ready");
    //Jump to map.html
    window.location.href = "map.html";


    var idToken = "eyJraWQiOiJ4Zk9sZTU2ZG5kTmNNUXY5eVMyeTAxeFFLM251TXFtakJZQlhmbkJVUFFrPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiZlJySmhwQ3RIZ2RlTjhzWmZjeEJ1ZyIsInN1YiI6ImIwMmUzZmQ5LTQzYTYtNDhiNS04YTJmLWE5NzdlNDE0NWQ1NCIsImF1ZCI6InV1ZG9wNWppNGE5MzBoZDJsZDhnaW80cW4iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2Mzg1MDE0NzMsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xXzByTnVvTnVjNCIsImNvZ25pdG86dXNlcm5hbWUiOiJxcSIsImV4cCI6MTYzODUwNTA3MywiaWF0IjoxNjM4NTAxNDczLCJqdGkiOiJiMjUxY2E2Ni01MGJjLTQwMGItODNkMy01MGRlZTkyMzlhMTQiLCJlbWFpbCI6InFxNzI4OTc3ODYyQGdtYWlsLmNvbSJ9.elsImfgVJ33uCtSVvdRcdVIv_IheeSbVX9cC7sJXRWUe_E6ukOrNAKn9Cl9JvqnGbbD6YciqYn4P0HALc4-R2fmkEvjuovcBN9acewz3k9sPesY7EOo3JTbYeFa6CX-OKpPdzy71xZ-aQvvbH1dYqJszCLgl699dOy8rUqvt5sw2ncDcNQkXpf28ISuffXQCHLhM1LCFaNdmjwKTDywZnkOTLoRBuFrVxr1LMZbmaeWJ2sMaSahMvScH1n6ern9zQiBuV6SoZBko0KhLUOrj0prvz9Q3C3ffOKaVbC-mog5Kq_Y_lglj2m3Si6HTHhpDd-HRNsgR_znn3LVPwdY1hg";
    var accessToken = "eyJraWQiOiI4UkY1TDZtdEhGQlBFRkNaSFFPeGxFY2p6azVIVGNaQWZ6a1lLUG9LS3VzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJiMDJlM2ZkOS00M2E2LTQ4YjUtOGEyZi1hOTc3ZTQxNDVkNTQiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIHBob25lIG9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXV0aF90aW1lIjoxNjM4NTAxNDczLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJleHAiOjE2Mzg1MDUwNzMsImlhdCI6MTYzODUwMTQ3MywidmVyc2lvbiI6MiwianRpIjoiZmZhN2ZiNWUtOTVlNC00OGMzLThkNzktYjcxZDU3OGE4NTc0IiwiY2xpZW50X2lkIjoidXVkb3A1amk0YTkzMGhkMmxkOGdpbzRxbiIsInVzZXJuYW1lIjoicXEifQ.j9vpIvohYb0ZCs3JFgajViuT4DB-FB90LwsN_kekmzBKOnyQwBXNDDXeEcRdPLiGJel2deY7vxW-kituYeDBbyI_OspQi8a81umIXguvT1tJUjcLIgeQhivHc1cFj77Vrp-wa6x-uvGiOaCAzF2ZMgTl5d1cT-ngekSMsZq5d6lp19oNaaR-R993Nt89hQ7mFiOLwV4w_8YW0kY8_h3wK225XgmfU6qIw8W9D9p3lqRAi_eD1RhDL7BMuezxmlpmX5vgSLPuIVtKaLkzZc_CSbRkiYjQ3W9kVPheKWt6c9yAYf8_3pDuVyuhwJZImrWtyC_yaqAcGV0HNUt0Fr8wXA";

    $.ajax({
      url: "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/login" + "?accessToken=" + accessToken,
      headers: {"Token": idToken},
      type: 'GET',
      cache: false,
      processData: false,
      contentType: 'application/json',
      success: function (r) {
          console.log(r);
      }
    })
}

function user_cancel(){
    // TODO: API Here
    console.log("User cancelled the trip");
    //Jump to request_trip.html
    // window.location.href = "request_trip.html";
}
