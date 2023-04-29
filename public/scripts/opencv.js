function onOpenCvReady() {
    // Retrieve the img element
    imgElement.addEventListener('change', function me() {


        // Replace the img element with the canvas element
        imgElement.parentNode.replaceChild(canvas, imgElement);
    })

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
}