// var video = new MediaElementPlayer($("#videoPlayer"));

// $("#videoPlayer").mediaelementplayer({
//     success:function(mediaElement,originalNode,instance) {

//     }
// });
var video = document.getElementById("videoPlayer");
var canvas = document.getElementById("videoCanvas");
canvas.width = video.clientWidth;
canvas.height = video.clientHeight;
var ctx = canvas.getContext("2d");
var interval;

function update() {
    ctx.drawImage(video,0,0,canvas.width,canvas.height);
    drawText();
}

$("#video").change(function(){
    $("#videoPlayer").attr("src",`./video${$(this).val()}.mp4`);
});

function drawText() {
    var outputText = "";
    for (let i = 0;i<canvas.height;i+=5) {
        for (let j = 0;j<canvas.width;j+=2) {
            var data = ctx.getImageData(j,i,1,1).data;
            if (navigator.platform=="Win32") {
                if (0.2126 * data[0] + 0.7152 * data[1] + 0.0722 * data[2]>150) {
                    outputText+="░";
                    // outputText+="⬜";
                    // outputText+="▂";
                } else if (0.2126 * data[0] + 0.7152 * data[1] + 0.0722 * data[2]>80) {
                    outputText+="▒";
                } else {
                    outputText+="▓";
                }
            } else {
                if (i==0||j==0||i>canvas.height-10||j==canvas.width-2) {
                    outputText+="▓";
                } else if (0.2126 * data[0] + 0.7152 * data[1] + 0.0722 * data[2]>150) {
                    outputText+="░";
                    // outputText+="⬜";
                    // outputText+="▂";
                } else if (0.2126 * data[0] + 0.7152 * data[1] + 0.0722 * data[2]>80) {
                    outputText+="▒";
                } else {
                    outputText+="▓";
                } 
            }
            // else if (0.2126 * data[0] + 0.7152 * data[1] + 0.0722 * data[2]>60) {
            //     // outputText+="⬛";
            //     outputText+="▓";
            //     // outputText+="▇";
            // } else {
            //     outputText+="█";
            // }
        }
        outputText+="\n";
    }
    $("#text").val(outputText);
}
drawText();

video.addEventListener('play',function() {interval=setInterval(update)},false);
video.addEventListener('pause',function() {clearInterval(interval);},false);
video.addEventListener('ended',function() {clearInterval(interval);},false);