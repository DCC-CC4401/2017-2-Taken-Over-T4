
$( document ).ready(function() {
getLocation();
});
var x = document.getElementById("demo");

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);

    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    var latdata = (Math.round(100000000*position.coords.latitude))/100000000;
    var lngdata = (Math.round(100000000*position.coords.longitude))/100000000;

    document.getElementById("id_complaint-lat").value = latdata;
    document.getElementById("id_complaint-lng").value = lngdata;

    var geocoder = new google.maps.Geocoder;

    var LatLng = {lat: latdata,lng: lngdata};

    geocoder.geocode({'location': LatLng}, function(results, status) {
    if (status === 'OK') {
      if (results[1]) {
        document.getElementById("id_complaint-directions").value = results[1].formatted_address;
      } else {
        window.alert('No results found');
      }
    } else {
      window.alert('Geocoder failed due to: ' + status);
    }
  });

}


