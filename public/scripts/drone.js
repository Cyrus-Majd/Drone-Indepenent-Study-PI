function editDroneInfo(info) {
    $('.drone_name').text(`Name: ${info.drone_name}`)
    $('.drone_gps').text(`Gps: Lat:${info.drone_gps.lat} Long: ${info.drone_gps.long} att: ${info.drone_gps.att}  `)
    $('.drone_battery').text(`Battery: ${info.drone_battery}`)
    $('.drone_heart').text(`Last Heartbeat: ${info.drone_heart}`)
    $('.drone_armable').text(`Armable: ${info.drone_armable}`)
    $('.drone_status').text(`System Status: ${info.drone_status}`)
    $('.drone_mode').text(`Mode: ${info.drone_mode}`)
    editDroneMode(info.drone_mode)
}

function editDroneDirection(info) {
    $('.drone_head').text(`Heading: ${info.drone_head}`)
    $('.drone_att').text(`Attitude: ${info.drone_att}`)
    $('.drone_vel').text(`Velocity: ${info.drone_vel}`)
    $('.drone_air_speed').text(`Air Speed: ${info.drone_air_speed}`)
    $('.drone_ground_speed').text(`Ground Speed: ${info.drone_ground_speed}`)
    $('.drone_arm').text(`Armed: ${info.drone_arm}`)
    if (info.drone_arm) {
        $('.arm').text("Disarm").removeClass("armed").addClass("disarmed")
    } else {
        $('.arm').text("Arm").removeClass("disarmed").addClass("armed")
    }
    $('.drone_home').text(`Home Location: ${info.drone_home}`)

}

async function disarmOrArm() {
    $('.arm').addClass("disabled")
    var response = await fetch('/drone/api/arm', {
        'method': "post",
        headers: {
            "Content-Type": "application/json",
        },
    })
    var res = await response.json();
    $('.arm').removeClass("disabled")
    if (res.armed) {
        $('.arm').text("Disarm").removeClass("armed").addClass("disarmed")
    } else {
        $('.arm').text("Arm").removeClass("disarmed").addClass("armed")
    }
}

function editDroneMode(mode) {

}

async function setMode(mode) {
    if (mode == "NULL") {
        return;
    }
    data = {
        "mode": mode
    }
    var response = await fetch('/drone/api/mode', {
        'method': "post",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    })
    var res = await response.json();
    console.log(res)
    $('#drone_select_mode').val(res.mode)

}
async function takeOff() {
    data = {
        "mode": ""
    }
    var response = await fetch('/drone/api/takeoff', {
        'method': "post",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    })
    var res = await response.json();
    console.log(res)
}
async function land() {
    data = {
        "mode": ""
    }
    var response = await fetch('/drone/api/land', {
        'method': "post",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    })
    var res = await response.json();
    console.log(res)
}
async function homeDrone() {
    data = {
        "mode": ""
    }
    var response = await fetch('/drone/api/home', {
        'method': "post",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    })
    var res = await response.json();
    console.log(res)
}