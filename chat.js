function search() {
  $("#img-container").empty();
  var client = apigClientFactory.newClient();
  var query_string = $('#query_string').val();
  var params = {query_text : query_string, "bucket" : "photosbucket112"};
  var additionalParams = {}
  var body = {}
  client.bucketGet(params, body, additionalParams).then(function(res){
    data = res.data
    data_length = data.length;
    if(data_length == 0){
      console.log('no images found');
    } else {
      data.forEach(function(val) {
        var img = new Image(300,);
        img.src = 'data:image/png;base64,' + val;
        console.log(img.src);
        $("#img-container").append(img);
        $('#img-container').append('&nbsp;');
      });
    }
  }).catch( function(res){
    console.log(res);
  });
}

function upload(){
  var file = $("#file_path").prop("files")[0];
  var labels = $("#file_labels").val();
  const reader = new FileReader();

  $.ajax({
    url: "https://2f2oruw7m3.execute-api.us-east-1.amazonaws.com/3/photosbucket112/" + file.name,
    type: 'PUT',
    data: file,
    dataType: 'html',
    headers: {"x-amz-meta-customLabels":labels},
    processData: false,
    contentType: file.type,
    success: function (response) {
      $('#message').html(file.name + ' was successfully uploaded');
      $('#file_path').val('');
      $("#file_labels").val('');
    },
    error: function(xhr, status, error){
     er = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
     $('#message').html(file.name + ' was not uploaded');
    }
 });
}
