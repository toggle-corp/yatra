var allmarkers = new Array();
var infowindow = new Array();
var geocoder;
var myRoute;
var info = null;
// var directionsDisplay;
// var directionsService;
var plan;
// var plan = {
//     title : 'Pokhara',
//     description : 'Pokhara is a beautiful place. My friend Safar lives there. His friend died of hiccups.',
//     budget : 'Rs.5000',
//     visibility : 'Public',
//     creator : 'Barbie Doll',
//     waypoints : []
// }

function initMap() {
    // var directionsDisplay;
    // directionsService = new google.maps.DirectionsService();
    // directionsDisplay = new google.maps.DirectionsRenderer();
    var mapDiv = document.getElementById('map');
    var map = new google.maps.Map(mapDiv, {
        center: {lat: 28.3949, lng: 84.1240},
        zoom: 8,
        scrollwheel: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });
    myRoute = new google.maps.Polyline({
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    geocoder = new google.maps.Geocoder();

    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function() {
        searchBox.setBounds(map.getBounds());
    });


    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function() {
        var places = searchBox.getPlaces();
        if (places.length == 0) {
            return;
        }

        // For each place, get the icon, name and location.
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function(place) {
            var icon = {
                url: place.icon,
                size: new google.maps.Size(71, 71),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(17, 34),
                scaledSize: new google.maps.Size(25, 25)
            };

            if (place.geometry.viewport) {
                // Only geocodes have viewport.
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);
    });


    // document.getElementById('address').addEventListener("keyup",
    //  function(event) {
    //      if (event.keyCode == 13) {
    //     document.getElementById('submit').click();
    //     }
    // });
    // document.getElementById('submit').addEventListener('click', function(){
    //     var address = document.getElementById('address').value;
    //     geocodeAddress(geocoder, address, function(location){
    //         var loc = location;
    //         map.setCenter(loc);
    //         map.setZoom(map.getZoom()+2);
    //     });
    // });
    if (editMode){
        google.maps.event.addListener(map, 'click', function(event){
            //console.log(event.latLng.lat());
            var mark = addMarker(event.latLng, map);
            updatePath(map, myRoute);
            // console.log(allmarkers);

            if (info) {
                info.close();
                info = null;
            }
        });
    }

    refresh(map);
    updatePath(map, myRoute);

    $("#post-plan").on('click', function(){
        data = {"points": JSON.stringify(points),
            "title": $("#title").html(),
            "description": $("#description").html(),
        };
        $.redirectPost(
            postUrl,
            data
        );
    });
}

function updatePoints() {
    $("#trip-points").children().remove();
    for (var i=0; i<points.length; ++i) {
        var element = $("<div class='trip-point'>Day " + points[i][2] + ": " + points[i][4] + "<div class='description'>" + points[i][3]+"</div></div>");
        $("#trip-points").append(element);
        day = points[i][2];
    }
}

function updatePath(myMap, route){
    updatePoints();
    myPath = [];
    wp = [];
    for (var i=0; i<allmarkers.length; i++){
        myPath.push(allmarkers[i].position);
        allmarkers[i].setMap(myMap);
    }
    route.setPath(myPath);
    route.setMap(myMap);
    console.log(points);
}

function addMarker(location, onMap, dday=null, ddescription=null){
    var marker = new google.maps.Marker({
        position : location,
        map : onMap
    });
    marker.setMap(onMap);
    allmarkers.push(marker);

    points.push([
        location.lat(),
        location.lng(),
        dday?dday:day, ddescription?ddescription:""
    ]);

    var currentIndex = points.length-1;
    points[currentIndex][4] = "";

    reverseGeocode(geocoder, marker.getPosition(), function(location){
        points[currentIndex][4] = location;
        updatePoints();
    });

    google.maps.event.addListener(marker, 'click', function() {
        if (info) {
            info.close();
            info = null;
        }
        var index = currentIndex;
        var point = points[index];
        var loc = point[4];
        // var loc = "";
        info = new google.maps.InfoWindow({
            content: '<div style="padding-left: 24px; padding-top: 10px; padding-bottom: 10px; min-width: 300px;"><div  style="margin-bottom: 10px"><strong>' +loc + '</strong></div><div class="popup"><div style="margin-bottom: 5px">Day:</div>'
            + ' </input><input id="day" type="number" class="form-control" onchange="changeDay($(this).val(), '+index+')" value="'+point[2]+'">'
            + ' <div style="margin-bottom: 5px; margin-top: 16px;">Description</div>'
            + ' </input><input id="desc" type="textbox" class="form-control" onchange="changeDescription($(this).val(), '+index+')" value="'+point[3]+'"></div></div>'
        });
        info.open(map, marker);
    });

    if (editMode) {
        google.maps.event.addListener(marker, 'rightclick',
          function() {
            marker.setMap(null);
            var index = allmarkers.indexOf(marker);
            allmarkers.splice(index, 1);
            points.splice(index, 1);
            updatePath(map, myRoute);
        });
    }
}


function geocodeAddress(geocoder, address, callback) {
    geocoder.geocode({'address': address}, function(results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            callback(results[0].geometry.location);
        } else {
            window.alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

function reverseGeocode(geocoder, input, callback) {
    //var latlngStr = input.split(',', 2);
    //var latlng = {lat: parseFloat(latlngStr[0]), lng: parseFloat(latlngStr[1])};
    var latlng = {lat: parseFloat(input.lat()), lng: parseFloat(input.lng())};
    geocoder.geocode({'location': latlng}, function(results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            if (results[1]) {
                callback(results[1].formatted_address);
            } else {
            // window.alert('No results found');
                console.log("No results found");
            }
        }
        else if (status === google.maps.GeocoderStatus.OVER_QUERY_LIMIT) {
            setTimeout(function() {
                reverseGeocode(geocder, input, callback);
            }, 50);
        }
        else {
            // window.alert('Geocoder failed due to: ' + status);
            console.log('Geocoder failed due to: ' + status);
        }
    });
}

function changeDay(value, index) {
    points[index][2] = value << 0;
    updatePoints();
}

function changeDescription(value, index) {
    points[index][3] = value;
    updatePoints();
}
