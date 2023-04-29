async function onOpenCvReady() {
    // Retrieve the img element

}
function RunImage() {
    var imgElement = document.getElementById('webcam_down');

    // Create a new canvas element to display the image
    var canvas = document.getElementById('outputCanvas');
    canvas.width = imgElement.width;
    canvas.height = imgElement.height;

    // Get the canvas context and create an OpenCV image
    //  var context = canvas.getContext('2d');
    var cvImage = cv.imread(imgElement);

    // Display the OpenCV image on the canvas
    cv.imshow(canvas, cvImage);
    window.requestAnimationFrame(RunImage);

}