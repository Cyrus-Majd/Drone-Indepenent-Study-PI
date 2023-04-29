function startComputerVision() {
    $(document).ready(function () {
        var video = document.getElementById('cv_webcam_front')
        video.onload = function () {
            console.log("LOADING")
            var canvas = document.getElementById('cv_outputCanvas')
            var context = canvas.getContext('2d');
            var tracker = new tracking.ColorTracker("cyan");

            tracking.track('#webcam_front', tracker);
            tracker.setMinDimension(5);

            tracker.on('track', function (event) {
                context.clearRect(0, 0, canvas.width, canvas.height);

                event.data.forEach(function (rect) {
                    if (rect.color === 'custom') {
                        rect.color = tracker.customColor;
                    }

                    context.strokeStyle = rect.color;
                    context.strokeRect(rect.x, rect.y, rect.width, rect.height);
                    context.font = '11px Helvetica';
                    context.fillStyle = "#fff";
                    context.fillText('x: ' + rect.x + 'px', rect.x + rect.width + 5, rect.y + 11);
                    context.fillText('y: ' + rect.y + 'px', rect.x + rect.width + 5, rect.y + 22);
                });
            });
        }

    })
}