function editDroneInfo(info) {
    $('.drone_name').text(`Name: ${info.drone_name}`)
    $('.drone_gps').text(`Gps: ${info.drone_gps}`)
    $('.drone_battery').text(`Battery: ${info.drone_battery}`)
    $('.drone_heart').text(`Last Heartbeat: ${info.drone_heart}`)
    $('.drone_armable').text(`Armable: ${info.drone_armable}`)
    $('.drone_status').text(`System Status: ${info.drone_status}`)
    $('.drone_mode').text(`Mode: ${info.drone_mode}`)
}

function editDroneDirection(info) {
    $('.drone_head').text(`Heading: ${info.drone_head}`)
    $('.drone_att').text(`Attitude: ${info.drone_att}`)
    $('.drone_vel').text(`Velocity: ${info.drone_vel}`)
    $('.drone_air_speed').text(`Air Speed: ${info.drone_air_speed}`)
    $('.drone_ground_speed').text(`Ground Speed: ${info.drone_ground_speed}`)
    $('.drone_arm').text(`Armed: ${info.drone_arm}`)
    $('.drone_home').text(`Home Location: ${info.drone_home}`)

}

async function disarmOrArm() {
    var response = await fetch('/drone/api/arm', {
        'method': "post",
        headers: {
            "Content-Type": "application/json",
        },
    })
    var res = await response.json();
    if (res.armed) {
        $('.arm').text("Disarm").removeClass("armed").addClass("disarmed")
    } else {
        $('.arm').text("Arm").removeClass("disarmed").addClass("armed")
    }
}