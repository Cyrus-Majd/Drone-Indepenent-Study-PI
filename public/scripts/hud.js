
$(document).ready(function () {
    var options = {
        size: 300,				// Sets the size in pixels of the indicator (square)
        roll: 0,				// Roll angle in degrees for an attitude indicator
        pitch: 0,				// Pitch angle in degrees for an attitude indicator
        heading: 0,				// Heading angle in degrees for an heading indicator
        vario: 0,				// Variometer in 1000 feets/min for the variometer indicator
        airspeed: 0,			// Air speed in knots for an air speed indicator
        altitude: 0,			// Altitude in feets for an altimeter indicator
        pressure: 1000,			// Pressure in hPa for an altimeter indicator
        showBox: true,			// Sets if the outer squared box is visible or not (true or false)
        img_directory: 'public/img/'	// The directory where the images are saved to
    }
    var indicator = $.flightIndicator('#attitude', 'attitude', options);
    var heading = $.flightIndicator('#heading', 'heading', { size: 300, heading: 150, showBox: true, img_directory: 'public/img/' });
    var variometer = $.flightIndicator('#variometer', 'variometer', { size: 300, vario: -5, showBox: true, img_directory: 'public/img/' });
    var airspeed = $.flightIndicator('#airspeed', 'airspeed', { size: 300, showBox: true, img_directory: 'public/img/' });
    var altimeter = $.flightIndicator('#altimeter', 'altimeter', { size: 300, showBox: true, img_directory: 'public/img/' });
    function updateHUD() {
        var then = new Date()

        $.get("/drone/api/hud", function (data) {
            var now = new Date()
            $('.drone_ping').text(`Ping: ${now - then}ms`)
            indicator.setRoll(data.roll);			// Sets the roll of an attitude indicator
            indicator.setPitch(data.pitch);			// Sets the pitch of an attitude indicator
            indicator.setHeading(data.heading);		// Sets the heading of an heading indicator
            indicator.setVario(data.vario);			// Sets the climb speed of an variometer indicator
            indicator.setAirSpeed(data.speed);		// Sets the speed of an airspeed indicator
            indicator.setAltitude(data.altitude);	// Sets the altitude of an altimeter indicator
            airspeed.setAirSpeed(data.speed);
            heading.setHeading(data.heading);
            variometer.setVario(data.vario);
            altimeter.setAltitude(data.altitude)

            setTimeout(updateHUD, 200)

        })
    }



    updateHUD()

});