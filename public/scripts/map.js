function updateMap(lat, long) {
    if (!google) {
        return;
    }
    var location = new google.maps.LatLng(lat, long)
    oldMarker = droneMarker;
    droneMarker = new google.maps.Marker({
        label: "D",
        position: location,
    })
    droneMarker.setMap(map)
    oldMarker?.setMap(null)

}
function centerMap() {
    if (!droneMarker) {
        setTimeout(centerMap, 1)
        return;
    }
    map.setCenter(droneMarker.getPosition())
}
function setSearchArea(event) {
    var radius = $(".radius").val()
    console.log(radius)

    var lat = event.latLng.lat()
    var long = event.latLng.lng()
    console.log(`lat ${lat} long ${long}`)
    oldsearch = searchMarker;
    searchMarker = new google.maps.Marker({
        label: "Search",
        animation: "DROP",
        map: map,
        position: event.latLng,
    })
    // searchMarker.setMap(map)
    oldsearch?.setMap(null)
}


var map;
var droneMarker;
var searchMarker;

function initMap() {

    // The location of Geeksforgeeks office
    const gfg_office = {
        lat: 28.50231,
        lng: 77.40548
    };

    // Create the map, centered at gfg_office
    map = new google.maps.Map(
        document.getElementById("map"), {
        // Set the zoom of the map
        zoom: 17.56,
        center: gfg_office,
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.SATELLITE
    });
    map.addListener("click", setSearchArea)
}