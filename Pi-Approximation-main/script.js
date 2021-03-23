var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

canvas.width = 600;
canvas.height = 600;

var running = false;

function Circle(x, y, vx, vy, r, color, stroke) {
    this.x = x;
    this.y = y;
    this.vx = vx;
    this.vy = vy;
    this.r = r;
    this.color = color;
    this.stroke = stroke;
    this.placed = false;

    this.init = async () => {
        for (let i = 0; i < 10; i++) {
            await delay(10);
            this.r -= 1;
            this.placed = false;
        }
        this.placed = true;
    }

    this.show = () => {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.r, 0, 2 * Math.PI, false);
        ctx.closePath();
        ctx.fill();
        if (this.stroke) {
            ctx.stroke();
            ctx.strokeStyle = "black";
        }
    }
    this.intersect = (other) => {
        var distance = Math.sqrt((other.x - this.x) ** 2 + (other.y - this.y) ** 2);
        if (distance < other.r) {
            return true;
        } else {
            return false;
        }
    }
}
var interval = setInterval(render, 10);
var mainCircle = new Circle(canvas.width / 2, canvas.height / 2, 0, 0, canvas.width / 2, "white", true);
var circles = [];

function calculateRatio(elem) {
    var colorsMap = circles.map((v, i) => {
        return v.color
    });
    var redCount = colorsMap.filter((color) => {
        return color == "red";
    });
    var blueCount = colorsMap.filter((color) => {
        return color == "blue";
    })
    var ratio = (4 * redCount.length / circles.length).toFixed(20);
    $(elem).html(ratio);
    convertTextToSpan(elem);
    return ratio;
}

function convertTextToSpan(elem) {
    var htmlVal = $(elem).html();
    htmlVal = htmlVal.match(/[\d\.]/g).map(char => {
        return `<span class="num${char}">${char}</span>`
    }).join("");
    $(elem).html(htmlVal);
}

async function fillCirclesGroups(number, groups) {
    for (let i = 0; i < number / groups; i++) {
        await delay(1);
        for (let j = 0; j < groups; j++) {
            circles.push(new Circle(Math.random() * canvas.width, Math.random() * canvas.height, 0, 0, 1, "blue", false));
        }
        // circles[i].init();
    }
}
async function fillCircles(number) {
    for (let i = 0; i < number; i++) {
        if (number <= 1000) {
            running = true;
            await delay(1);
            circles.push(new Circle(Math.random() * canvas.width, Math.random() * canvas.height, 0, 0, 12, "blue", false));
            circles[i].init();
        } else {
            circles.push(new Circle(Math.random() * canvas.width, Math.random() * canvas.height, 0, 0, 2, "blue", false));
            circles[i].placed = true;
        }
        $("p#circles").text(circles.length);
    }
    $("input#start").attr("disabled", false);
    $("input#start").removeClass("btn-lg-disabled");
    $("input#start").addClass("btn-success");
    running = false;
}

function calculateDifference(approx, pi, elem) {
    $(elem).text(Math.abs($(approx).text() - $(pi).text()).toFixed(20));
}

async function delay(amount) {
    return new Promise((resolve, reject) => {
        setTimeout(function () {
            resolve();
        }, amount);
    });
}

fillCircles($("input#iterations").val());
convertTextToSpan("p#pi");

function render() {
    ctx.strokeStyle = "black";
    ctx.strokeRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    mainCircle.show();
    for (let i = 0; i < circles.length; i++) {
        var circle = circles[i];
        if (circle.intersect(mainCircle) && circle.color != "red") {
            circle.color = "red";
        }
        circle.show();
    }
    calculateRatio("p#ratio");
    calculateDifference("p#ratio", "p#pi", "p#difference");

    var boolMap = circles.map(circle => circle.placed);
    var testTrue = boolMap.every((bool) => bool);

    if (running) {
        $("input#start").attr("disabled", true);
        $("input#start").removeClass("btn-success");
        $("input#start").addClass("btn-lg-disabled");
    } else {
        if (circles.length == parseInt($("#iterations").val()) && testTrue) {
            clearInterval(interval);
        }
    }
}
$("#largeValueWarning").hide();
$(document).ready(function () {
    $("input#iterations").on('keyup change', function () {
        if ($(this).val() >= 100000) {
            $("#largeValueWarning").show(200);
        } else if ($(this).val() >= 1000000) {
            $(this).val("1000000");
        } else {
            $("#largeValueWarning").hide(200);
        }
    });
    $("form#form").submit(function () {
        interval = setInterval(render, 10);
        // render();
        event.preventDefault();
        circles = [];
        if ($("#iterations").val() != null) {
            var iterations = parseInt($("#iterations").val());
            fillCircles(iterations);
        } else {
            console.error("Please input number");
        }
    })
});