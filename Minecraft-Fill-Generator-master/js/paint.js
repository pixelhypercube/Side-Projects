var canvasOptions = {
    xGrid:parseInt($("input#sizeX").val()),
    yGrid:parseInt($("input#sizeY").val()),
    zGrid:parseInt($("input#sizeZ").val()),
    gridSize:40,
    canvasMode:"simple", // "simple" - Load blocks with single color, "texture" - Load blocks with minecraft textures
}
var {xGrid,yGrid,zGrid,gridSize,canvasMode} = canvasOptions;
let canvasMouseX = 0, canvasMouseY = 0;
let gridWidth = xGrid*gridSize;
let gridHeight = zGrid*gridSize;
let currentLayer = 1;
let mouseDownCanvas = false,
mouseInCanvas = false;
let selectedColor = "white";
var colorList = [
    "white",
    "orange",
    "magenta",
    "light_blue",
    "yellow",
    "lime",
    "pink",
    "gray",
    "silver",
    "cyan",
    "purple",
    "blue",
    "brown",
    "green",
    "red",
    "black",
    "eraser"
];

//In order - Y, [X,Z]
/*

var arrMap = [
    [
        
        [0,1,0,1],
        [1,0,1,0],
        [0,1,0,1],
        [1,0,1,0]
    ],
    [
        [0,1,0,1],
        [1,0,1,0],
        [0,1,0,1],
        [1,0,1,0]
    ],
];

*/
var arrMap = [];

var canvas = document.getElementById("paintCanvas");
var ctx = canvas.getContext("2d");

function updateSize() {
    gridWidth = xGrid*gridSize;
    gridHeight = zGrid*gridSize;
    canvas.width = gridWidth;
    canvas.height = gridHeight;
    xGrid = parseInt($("input#sizeX").val());
    zGrid = parseInt($("input#sizeZ").val());
    for (let i = 0;i<zGrid;i++) {
        for (let j = 0;j<xGrid;j++) {
            ctx.strokeRect(j*gridSize,i*gridSize,gridSize,gridSize);
        }
    }
}

function updateArrayMap() {
    arrMap = [];
    for (let i = 0;i<yGrid;i++) {
        arrMap.push([]);
        for (let j = 0;j<zGrid;j++) {
            arrMap[i].push([]);
            for (let k = 0;k<xGrid;k++) {
                arrMap[i][j].push(null);
            }
        }
    }
}
updateArrayMap();

function renderArrToCanvas() {
    for (let i in arrMap[currentLayer-1]) {
        for (let j in arrMap[currentLayer-1][i]) {
            // console.log(arrMap[currentLayer-1][i][j])
            switch (arrMap[currentLayer-1][i][j]) {
                case 0:
                    ctx.fillStyle = "white";
                    break;
                case 1:
                    ctx.fillStyle = "orange";
                    break;
                case 2:
                    ctx.fillStyle = "magenta";
                    break;
                case 3:
                    ctx.fillStyle = "skyblue";
                    break;
                case 4:
                    ctx.fillStyle = "yellow";
                    break;
                case 5:
                    ctx.fillStyle = "lime";
                    break;
                case 6:
                    ctx.fillStyle = "pink";
                    break;
                case 7:
                    ctx.fillStyle = "grey";
                    break;
                case 8:
                    ctx.fillStyle = "lightgrey";
                    break;
                case 9:
                    ctx.fillStyle = "cyan";
                    break;
                case 10:
                    ctx.fillStyle = "purple";
                    break;
                case 11:
                    ctx.fillStyle = "blue";
                    break;
                case 12:
                    ctx.fillStyle = "brown";
                    break;
                case 13:
                    ctx.fillStyle = "green";
                    break;
                case 14:
                    ctx.fillStyle = "red";
                    break;
                case 15:
                    ctx.fillStyle = "black";
                    break;
                default:
                    ctx.fillStyle = "rgba(190,212,120,0.5)";
                    break;
            }
            // ctx.fillStyle="black"; - // Used for testing
            ctx.fillRect(j*gridSize,i*gridSize,gridSize,gridSize);
        }
    }
}
function fillCubesFromCanvas() {
    scene.children = [];
    for (let i in arrMap) {
        for (let j in arrMap[i]) {
            for (let k in arrMap[i][j]) {
                var colorIndex = arrMap[i][j][k];
                if (colorIndex!=null && colorList[colorIndex]!="eraser") {
                    var cubeMaterials = [
                        new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/blockTextures/").load(`wool_colored_${colorList[colorIndex]}.png`),side:THREE.DoubleSide}),
                        new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/blockTextures/").load(`wool_colored_${colorList[colorIndex]}.png`),side:THREE.DoubleSide}),
                        new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/blockTextures/").load(`wool_colored_${colorList[colorIndex]}.png`),side:THREE.DoubleSide}),
                        new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/blockTextures/").load(`wool_colored_${colorList[colorIndex]}.png`),side:THREE.DoubleSide}),
                        new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/blockTextures/").load(`wool_colored_${colorList[colorIndex]}.png`),side:THREE.DoubleSide}),
                        new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/blockTextures/").load(`wool_colored_${colorList[colorIndex]}.png`),side:THREE.DoubleSide}),
                    ];
                    var geometry = new THREE.BoxGeometry(1,1,1);
                    var cube = new THREE.Mesh( geometry, cubeMaterials );
                    cube.position.set(k,i,j);
                    scene.add(cube);
                }
            }
        }
    }
}


// function getBlockIndex(mouseX,mouseY) {
    // let xPos = Math.floor(mouseX/gridSize);
    // let yPos = Math.floor(mouseY/gridSize);
    
// }

$(document).ready(function(){
    $("canvas#paintCanvas").mousemove(function(e){
        canvasMouseX = e.offsetX;
        canvasMouseY = e.offsetY;
    });
    $("canvas#paintCanvas").mouseenter(function(){
        mouseInCanvas = true;
    });
    $("canvas#paintCanvas").mouseleave(function(){
        mouseInCanvas = false;
    });
    $("canvas#paintCanvas").mousemove(function(e){
        if (mouseIsDown && mouseInCanvas) {
            let xPos = Math.floor(canvasMouseX/gridSize);
            let zPos = Math.floor(canvasMouseY/gridSize);
            arrMap[currentLayer-1][zPos][xPos] = colorList.indexOf(selectedColor);
        }
    });
    $("canvas#paintCanvas").click(function(){
        let xPos = Math.floor(canvasMouseX/gridSize);
        let zPos = Math.floor(canvasMouseY/gridSize);
        arrMap[currentLayer-1][zPos][xPos] = colorList.indexOf(selectedColor);
    })
    $("input#sizeX,input#sizeY,input#sizeZ").change(function() {
        updateArrayMap(arrMap);
        $("input#layer").attr("max",parseInt($("input#sizeY").val()));
    });
    $("input#layer").attr("max",parseInt($("input#sizeY").val()));
    $("input#layer").change(function(){
        currentLayer = parseInt($(this).val());
    });
});

function renderSelectedColor() {
    // $("button.colorBtn").each(function(i,elem){
    //     // $(elem).empty();
    //     // $(elem).append("<p> </p>");
    // });
    $("button.colorBtn").each(function(i,elem){
        $(elem).empty();
        $(elem).append("<p> </p>");
        if ($(elem).data("color")=="eraser") {
            $(elem).append(`<p>Eraser</p>`)
        }
        if ($(elem).data("color")==selectedColor) {
            $(elem).addClass("selectedColorBtn");
            // var tickInsertHTML = `
            // <p>✔</p>
            // `;
            // $(elem).append(tickInsertHTML);
        } else {
            $(elem).removeClass("selectedColorBtn");
        }
    });
}

function fillColorBtnList() {
    for (let color of colorList) {
        if (color!="eraser") {
            var insertHTML = 
            `
            <button data-color="${color}" style="background:${color.replace(/_/g,"").replace(/cyan/g,"teal")}"
            class="colorBtn">
                <p> </p>
            </button>
            `
            ;
            $("div#colorBtnList").append(insertHTML);
        }
    }
    renderSelectedColor();
    $("button.colorBtn").click(function(){
        selectedColor = $(this).data("color");
        renderSelectedColor();
    });
}
fillColorBtnList();


function update() {
    updateSize();
    renderArrToCanvas();
    ctx.fillStyle = "rgba(0,0,0,0.5)";
    ctx.fillRect(Math.floor(canvasMouseX/gridSize)*gridSize,
    Math.floor(canvasMouseY/gridSize)*gridSize,gridSize,gridSize);
    ctx.strokeStyle = "rgba(255,0,0,1)";
    ctx.strokeRect(Math.floor(canvasMouseX/gridSize)*gridSize,
    Math.floor(canvasMouseY/gridSize)*gridSize,gridSize,gridSize);
}

function generateCommand() {
    var outputString = "";
    for (let i = 0;i<arrMap.length;i++) {
        for (let j = 0;j<arrMap[i].length;j++) {
            for (let k = 0;k<arrMap[i][j].length;k++) {
                if (arrMap[i][j][k]!=null) {
                    outputString+=`/setblock ~${j} ~${i} ~${k} minecraft:wool ${arrMap[i][j][k]}\n`;
                }
            }
        }
    }
    //console.log(outputString);
    return outputString;
}

// update();
setInterval(update,10);