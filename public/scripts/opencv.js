


function onOpenCvReady() {
    var e = document.getElementById("webcam_down")
    e.addEventListener('change', (e) => {
        e.src = URL.createObjectURL(e.target.files[0]);
        let mat = cv.imread(e)
        cv.imshow("outputCanvas", mat);
    })




}