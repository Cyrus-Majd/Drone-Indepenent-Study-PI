function onOpenCvReady() {
    // Retrieve the img element
    var imgElement = document.getElementById('webcam_down');
    imgElement.onload = function me() {
        // Create a new canvas element to display the image
        var canvas = document.createElement('canvas');
        canvas.width = imgElement.width;
        canvas.height = imgElement.height;

        // Get the canvas context and create an OpenCV image
        var context = canvas.getContext('2d');
        var cvImage = cv.imread(imgElement);

        // Display the OpenCV image on the canvas
        cv.imshow(canvas, cvImage);

        // Replace the img element with the canvas element
        imgElement.parentNode.replaceChild(canvas, imgElement);
    }

}
