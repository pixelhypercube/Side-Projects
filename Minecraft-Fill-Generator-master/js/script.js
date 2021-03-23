let mouseIsOver = false, mouseIsDown = false,mouseX = 0,mouseY = 0
cursorX = 0, cursorY = 0;
$(document).ready(function(){
    $("div#renderer").mousemove(function(e){
        mouseX = e.pageX
        mouseY = e.pageY;
    });
    $(window).mousedown(function(){
        mouseIsDown = true;
    });
    $(window).mouseup(function(){
        mouseIsDown = false;
    });
    $("div#renderer").mouseover(function(){
        mouseIsOver = true;
    });
    $("div#renderer").mouseleave(function(){
        mouseIsOver = false;
    });
    $("form#fillBlocks").submit(function(){
        event.preventDefault();
        var sizeX = parseInt($("input#sizeX").val());
        var sizeY = parseInt($("input#sizeY").val());
        var sizeZ = parseInt($("input#sizeZ").val());
        // fillCubesTest(sizeX,sizeY,sizeZ);
        fillCubesFromCanvas();
        $("#command").val(generateCommand());
    });
    $("div#layerHelp").hide();
    $("button#layerHelpBtn").click(function(){
        console.log("Clicked!")
        if ($("div#layerHelp").is(":hidden")) {
            $("div#layerHelp").show(500);
        } else {
            $("div#layerHelp").hide(500);
        }
    });
})