let video = null; 

let width = 320;
let height = 0;

let src = null;
let dst = null;

let streaming = false;
let stream = null;
let vc = null;

let socket = null;

function processVideo() {

    vc.read(src);
    cv.imshow("canvasOutput", src);

    var type = "image/png"
    var data = document.getElementById("canvasOutput").toDataURL(type);
    data = data.replace('data:' + type + ';base64,', ''); 

    socket.emit('image', data);

    requestAnimationFrame(processVideo);
}

function stopVideoProcessing() {
    if (src != null && !src.isDeleted()) src.delete();
}

function stopCamera() {
    if (!streaming) return;
    stopVideoProcessing();
    document.getElementById("canvasOutput").getContext("2d").clearRect(0, 0, width, height);
    video.pause();
    video.srcObject=null;
    stream.getVideoTracks()[0].stop();
    streaming = false;
}

function startVideoProcessing() {
    if (!streaming) { console.warn("Please startup your webcam"); return; }
    stopVideoProcessing();
    src = new cv.Mat(height, width, cv.CV_8UC4);
    requestAnimationFrame(processVideo);
}

function startCamera() {
    if (streaming) return;
    navigator.mediaDevices.getUserMedia({video: true, audio: false})
        .then(function(s) {
            stream = s;
            video.srcObject = s;
            video.play();
        })
        .catch(function(err) {
            console.log("An error occured! " + err);
        });

    video.addEventListener("canplay", function(ev){
        if (!streaming) {
            height = video.videoHeight / (video.videoWidth/width);
            video.setAttribute("width", width);
            video.setAttribute("height", height);
            streaming = true;
            vc = new cv.VideoCapture(video);
        }
        startVideoProcessing();
    }, false);
}

function onOpenCvReady() {
   console.log('OpenCV.js is readyyyyy.');
}

$( document ).ready(function() {
    console.log('document ready');

    video = document.getElementById("videoInput"); 
    video.width = 640;
    video.height = 480;
    startCamera();

    socket = io('http://localhost:8080');
    socket.on('connect', function(){
        console.log("Connected...!", socket.connected)
    });
    socket.on('response_back', function(image){
        console.log('got response back!');
        const image_id = document.getElementById('imagebox');
        image_id.src = image;
    });
});