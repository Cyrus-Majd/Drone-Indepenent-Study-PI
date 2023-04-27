var map;
var droneMarker;
var searchMarker;


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
    var radius = parseInt($(".radius").val())
    var alt = parseInt($(".alt").val())

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
    var circle = new google.maps.Circle({
        center: searchMarker.getPosition(),
        radius: radius,
    });
    var circleBounds = circle.getBounds();
    var northEast = circleBounds.getNorthEast();
    var southWest = circleBounds.getSouthWest();
    var northWest = new google.maps.LatLng(northEast.lat(), southWest.lng());
    var southEast = new google.maps.LatLng(southWest.lat(), northEast.lng());

    // Create a square around the circle
    var square = new google.maps.Polygon({
        paths: [northEast, northWest, southWest, southEast],
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: map
    });
    searchMarker.currentSearch = square
    searchMarker.currentSearch.radius = radius;
    searchMarker.currentSearch.alt = alt

    // searchMarker.setMap(map)
    oldsearch?.setMap(null)
    oldsearch?.currentSearch.setMap(null)
    oldsearch?.currentSearch?.path.setMap(null)

}

function mapPath(pathCoordinates, type) {
    var color = '#FF0000';
    if (type == "squaresearch") {
        color = '#FF00FF'
    }
    var path = new google.maps.Polyline({
        path: pathCoordinates,
        geodesic: true,
        strokeColor: color,
        strokeOpacity: 1.0,
        strokeWeight: 2,
        map: map
    });
    searchMarker.currentSearch.path = path

}

async function SquareSearch() {
    if (!searchMarker) {
        alert("Please select a search area!")
        return;
    }

    var radius = searchMarker.currentSearch.radius;
    var alt = searchMarker.currentSearch.alt

    var latLong = searchMarker.getPosition();
    var lat = latLong.lat()
    var long = latLong.lng()
    var data = {
        "radius": radius,
        "lat": lat,
        "long": long,
        "alt": alt
    }
    var response = await fetch('/drone/api/search/square', {
        'method': "post",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    })
    var res = await response.json();
    console.log(res)
    var path = parsePath(res)
    console.log(path)
    mapPath(path, "squaresearch")


}
function clearMarkers() {
    searchMarker?.setMap(null);
    searchMarker?.currentSearch.setMap(null)
    searchMarker?.currentSearch.path.setMap(null)
    searchMarker = null;
}



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
    // mapPath([{ "lat": 40.52201309936123, "lng": -74.46292879108148 },
    // { "lat": 40.52201309936063, "lng": -74.46294060858764 },
    // { "lat": 40.52199513305495, "lng": -74.46294060858764 },
    // { "lat": 40.521995133052535, "lng": -74.46291697358163 },
    // { "lat": 40.522022082511064, "lng": -74.46291697358163 },
    // { "lat": 40.52202208250565, "lng": -74.4629524261049 },
    // { "lat": 40.52198614989429, "lng": -74.4629524261049 },
    // { "lat": 40.521986149884654, "lng": -74.46290515609921 },
    // { "lat": 40.52203106564886, "lng": -74.46290515609921 },
    // { "lat": 40.52203106563382, "lng": -74.46296424364593 },
    // { "lat": 40.52197716671678, "lng": -74.46296424364594 },
    // { "lat": 40.521977166695116, "lng": -74.46289333864692 },
    // { "lat": 40.522040048765, "lng": -74.46289333864692 },
    // { "lat": 40.522040048735505, "lng": -74.4629760612234 },
    // { "lat": 40.521968183512776, "lng": -74.4629760612234 },
    // { "lat": 40.52196818347426, "lng": -74.46288152123736 },
    // { "lat": 40.52204903184983, "lng": -74.46288152123736 },
    // { "lat": 40.522049031801075, "lng": -74.46298787884993 },
    // { "lat": 40.52195920027267, "lng": -74.46298787884993 }])
}


function parsePath(path) {
    var newpath = [];
    for (let i = 0; i < path.length; i++) {
        var waypointArray = path[i];
        newpath.push({ 'lat': waypointArray[0], "lng": waypointArray[1] })
    }
    return newpath
}