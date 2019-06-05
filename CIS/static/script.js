$(document).ready(function() {
  $(".carousel").attr("max-width", maxwidth());
  $('#segment').submit(function(e) {
    e.preventDefault();
    var form_data = new FormData($('#segment')[0]);
    $.ajax({
      type: 'POST',
      url: '/process',
      data: form_data,
      contentType: false,
      processData: false,
      dataType: 'json'
    }).done(function(data){
      if(data["output_image"] != undefined){
        var images = data["output_image"].toString().split(",");
        for (var i = 0; i < images.length; i++) {
          var url = '/static/output_images/'+images[i];
          $.ajax({
            url: url,
            cache: true,
            processData: false,
          });
          $("#outputImages .carousel-inner").append("<div class=\"carousel-item\">\
            <img class=\"d-block\" src=\""+url+"\" alt=\"output image "+(i+1)+"\" style=\"max-width: 250px; max-height: 250px;\">\
          </div>");
        }
        if (images.length == 1) {
          $("#outputImage small").text("Output Image");
          $(".carousel-control-prev").hide();
          $(".carousel-control-next").hide();
        }else {
          $("#outputImage small").text("Output Images");
        }
        $("#outputImage").css("display", "block");
        $(".carousel-item:first-child").addClass("active");
        $("#results").css("display", "block");
        $("#buttons").css("display", "block");
        $("#outputImage button").click(function () {
          clearResults()
        });
        $("#notif").text(data['message']).css("display", "block").addClass("alert-success");
        if(data['compactness'] != null && data['separation'] != null){
          $("#table").css("display", "block");
          $("#wss").text(data['compactness']);
          $("#bss").text(data['separation']);
        }
      }else{
        if (data["image_errors"].length > 0){
          $(".custom-file-input").addClass('is-invalid');
          for (var i = 0; i < data["image_errors"].length; i++) {
            $("#image_errors").append(data["image_errors"][i]);
            if (i < data["image_errors"].length - 1) {
              $("#image_errors").append("<br>");
            }
          }
          $("#image_errors").css("display", "block");
          $('#inputImage').attr('src', '/static/input_images/default.jpg');
        }
        if (data["algorithm_errors"].length > 0){
          $("#algorithm").addClass('is-invalid');
          $("#algorithm_errors").css("display", "block");
          for (var i = 0; i < data["algorithm_errors"].length; i++) {
            $("#algorithm_errors span").append(data["algorithm_errors"][i]);
            if (i < data["algorithm_errors"].length - 1) {
              $("#algorithm_errors span").append("<br>");
            }
          }
        }
        if (data["colors_errors"].length > 0){
          $("#colors").addClass('is-invalid');
          $("#colors_errors").css("display", "block");
          for (var i = 0; i < data["colors_errors"].length; i++) {
            $("#colors_errors span").append(data["colors_errors"][i]);
            if (i < data["colors_errors"].length - 1) {
              $("#colors_errors span").append("<br>");
            }
          }
        }
        if (data["clusters_errors"].length > 0){
          $("#clusters").addClass('is-invalid');
          $("#clusters_errors").css("display", "block");
          for (var i = 0; i < data["clusters_errors"].length; i++) {
            $("#clusters_errors span").append(data["clusters_errors"][i]);
            if (i < data["clusters_errors"].length - 1) {
              $("#clusters_errors span").append("<br>");
            }
          }
        }
      }
    }).fail(function(data){
      $("#notif").text('Something went wrong ! Please try again').css("display", "block").addClass("alert-danger");
    });
  });
  $(document).ajaxStart(function(){
    $("#loadingDiv").css("display","block");
    $("#notif").css("display","none").removeClass("alert-danger alert-success");
    $("#algorithm_errors").css("display", "none");
    $("#algorithm_errors span").text("");
    $("#algorithm_errors").removeClass("is-invalid");
    $("#color_errors").css("display", "none");
    $("#colors_errors span").text("");
    $("#color_errors").removeClass("is-invalid");
    $("#image_errors").text('').css("display", "none");
    $("#clusters_errors").css("display", "none");
    $("#clusters_errors span").text("");
    $("#clusters_errors").removeClass("is-invalid");
    $("#outputImage ").css("display", "none");
    $("#outputImages .carousel-inner").text("");
    $("#table").css("display", "none");
    $(".carousel-control-prev").show();
    $(".carousel-control-next").show();
  });
  $(document).ajaxComplete(function(){
    $("#loadingDiv").css("display","none");
  });

  $(":file").change(function () {
    if (this.files && this.files[0]) {
      clearResults();
      $("#image_errors").text('').css("display", "none");
      var reader = new FileReader();
      reader.onload = imageIsLoaded;
      reader.readAsDataURL(this.files[0]);
      this.labels[0].innerText = this.files[0].name;
    }else {
      $('#inputImage').attr('src', '/static/input_images/default.jpg');
      this.labels[0].innerText = "Choose an Input Image";
    }
  });

  $("#algorithm").change(function () {
    disable();
    $("#algorithm_errors").css("display", "none");
    $("#algorithm_errors span").text("");
    $("#algorithm").removeClass("is-invalid");
  });

  $("#colors").change(function () {
    $("#color_errors").css("display", "none");
    $("#colors_errors span").text("");
    $("#colors").removeClass("is-invalid");
  });

  $("#clusters").keypress(function () {
    $("#clusters_errors").css("display", "none");
    $("#clusters_errors span").text("");
    $("#clusters").removeClass("is-invalid");
  });

  $('#outimg_table').carousel({
    interval: 2000
  });

  $("#buttons a").click(function (){
    url = $("#outputImages .active img").attr("src");
    $("#buttons a").attr("href", url);
  });
});

function imageIsLoaded(e) {
  $('#inputImage').attr('src', e.target.result);
}

function clearResults(){
  $("#outputImage").css("display", "none");
  $("#buttons").css("display", "none");
  $("#notif").css("display", "none");
  $("#table").css("display", "none");
  $("#results").css("display", "none");
}

function delete_run(run_id) {
	$("#delete_form").attr("action", "/run/"+run_id+"/delete");
}

function disable(){
 if ($("#algorithm").val() == "VIBGYOR") {
   $("#clusters").prop("disabled", true);
   $("#choices").prop("disabled", true);
   $("#colors").prop("disabled", false);
 }else{
   $("#clusters").prop("disabled", false);
   $("#choices").prop("disabled", false);
   $("#colors").prop("disabled", true);
 }
}

function maxwidth(){
  var max = 0;
  var images = $(".carousel-item img");
  for (var i = 0; i < images.length; i++) {
    if (max < images[i].attr("width")) {
      max = images[i].attr("width");
    }
  }
  return max;
}
