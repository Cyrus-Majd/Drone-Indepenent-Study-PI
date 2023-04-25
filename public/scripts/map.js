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
var map;
var droneMarker;
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

}