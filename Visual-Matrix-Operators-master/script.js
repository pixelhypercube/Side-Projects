var firstMatrix = [],
    secondMatrix = [],
    resultantArr = [];

function updateMatrix(matrixNo) {
    var matrix, matrixName;
    if (matrixNo == 1) {
        matrix = firstMatrix;
        matrixName = "firstMatrix";
    } else if (matrixNo == 2) {
        matrix = secondMatrix;
        matrixName = "secondMatrix";
    }
    var outHtml = ``;
    $(`table#${matrixName}`).empty();
    for (let i = 0; i < matrix.length; i++) {
        outHtml += "<tr>";
        for (let j = 0; j < matrix[i].length; j++) {
            outHtml +=
                `<td>
            <input value="${matrix[i][j]}" class="inputNum${matrixNo}" type="text" name="">
            </td>`;
        }
        outHtml += "</tr>";
    }
    $(`table#${matrixName}`).append(outHtml);
}

function genFirstArr(w, h) {
    for (let i = 0; i < h; i++) {
        firstMatrix.push([]);
        for (let j = 0; j < w; j++) {
            var rn = Math.floor(Math.random() * 10)
            // firstMatrix[i].push(0);
            firstMatrix[i].push(rn);
        }
    }
}

function genSecondArr(w, h) {
    for (let i = 0; i < h; i++) {
        secondMatrix.push([]);
        for (let j = 0; j < w; j++) {
            var rn = Math.floor(Math.random() * 10)
            // firstMatrix[i].push(0);
            secondMatrix[i].push(rn);
        }
    }
}

function getArr() {
    $(".inputNum1").each(function (i) {
        console.log($(this).val())
        var x = i % firstMatrix[0].length;
        var y = Math.floor(i / firstMatrix[0].length);
        console.log(y, x);
        firstMatrix[y][x] = parseInt($(this).val());
    });
    console.log("FIRST MATRIX: ", firstMatrix);
    $(".inputNum2").each(function (i) {
        var x = i % secondMatrix[0].length;
        var y = Math.floor(i / secondMatrix[0].length);
        // console.log(y,x)
        secondMatrix[y][x] = parseInt($(this).val());
        // console.log(secondMatrix[x][y])
    });
    console.log("SECOND MATRIX: ", secondMatrix);
}

function multiply() {
    try {
        resultantArr = [];
        $("#operator").text("*");
        getArr();
        for (let i = 0; i < firstMatrix.length; i++) {
            resultantArr.push([]);
            for (let j = 0; j < secondMatrix[0].length; j++) {
                var sum = 0;
                for (let k = 0; k < firstMatrix[0].length; k++) {
                    // console.log("K: ",k)
                    sum += firstMatrix[i][k] * secondMatrix[k][j];
                }
                resultantArr[i].push(sum);
            }
        }
        printResultantArr();
        // console.log(resultantArr);
    } catch (e) {
        $("#msg").empty();
        $("#msg").css({
            "display": "block"
        });
        $("#msg").append($.parseHTML(`
        The number of columns of Matrix A need to be equal to the number of rows of Matrix B
        <br>
        A: (${firstMatrix.length}x<span class="multSize">${firstMatrix[0].length}</span>)  B: (<span class="multSize">${secondMatrix.length}</span>x${secondMatrix[0].length})
        <br>
        <span class="multSize">${firstMatrix[0].length} ≠ ${secondMatrix.length}</span>
        `));
    }
}

function add() {
    try {
        resultantArr = [];
        $("#operator").text("+");
        getArr();
        for (let i = 0; i < firstMatrix.length; i++) {
            resultantArr.push([]);
            for (let j = 0; j < firstMatrix[i].length; j++) {
                resultantArr[i].push(firstMatrix[i][j] + secondMatrix[i][j]);
            }
        }
        printResultantArr();
    } catch (e) {
        $("#msg").css({
            "display": "block"
        });
        $("#msg").text(`
        Matrix A & B need to be the same size
        `);
    }
}

function subtract() {
    try {
        resultantArr = [];
        $("#operator").text("-");
        getArr();
        for (let i = 0; i < firstMatrix.length; i++) {
            resultantArr.push([]);
            for (let j = 0; j < firstMatrix[i].length; j++) {
                resultantArr[i].push(firstMatrix[i][j] - secondMatrix[i][j]);
            }
        }
        printResultantArr();
    } catch (e) {
        $("#msg").css({
            "display": "block"
        });
        $("#msg").text(`
        Matrix A & B need to be the same size
        `);
    }
}

function printResultantArr() {
    $("#msg").css({
        "display": "none"
    });
    $("#formula").css({
        "display": "block"
    });
    $("#resultantMatrix").empty();
    var outHtml = ``;
    for (let i = 0; i < resultantArr.length; i++) {
        outHtml += `<tr>`;
        for (let j = 0; j < resultantArr[i].length; j++) {
            outHtml +=
                `<td style="background:hsl(${resultantArr[i][j]},100%,25%)" >
                <input
                style="background:hsl(${resultantArr[i][j]},100%,70%)"
                value="${resultantArr[i][j]}" class="resultNum" type="text">
                </td>`;
            // secondMatrix[i].push(0);
        }
        outHtml += "</tr>";
    }
    $("#resultantMatrix").append(outHtml);
}


function addRow(matrixNo) {
    var matrix;
    if (matrixNo == 1) {
        matrix = firstMatrix;
    } else if (matrixNo == 2) {
        matrix = secondMatrix;
    }
    matrix.push([]);
    for (let i = 0; i < matrix[0].length; i++) {
        matrix[matrix.length - 1].push(Math.floor(Math.random() * 10));
    }
    updateMatrix(matrixNo);
}

function addColumn(matrixNo) {
    var matrix;
    if (matrixNo == 1) {
        matrix = firstMatrix;
    } else if (matrixNo == 2) {
        matrix = secondMatrix;
    }
    for (let i = 0; i < matrix.length; i++) {
        matrix[i].push(Math.floor(Math.random() * 10));
    }
    updateMatrix(matrixNo);
}

function removeRow(matrixNo) {
    var matrix;
    if (matrixNo == 1) {
        matrix = firstMatrix;
    } else if (matrixNo == 2) {
        matrix = secondMatrix;
    }
    matrix.pop();
    updateMatrix(matrixNo);
}

function removeColumn(matrixNo) {
    var matrix;
    if (matrixNo == 1) {
        matrix = firstMatrix;
    } else if (matrixNo == 2) {
        matrix = secondMatrix;
    }
    for (let i = 0; i < matrix.length; i++) {
        matrix[i].pop();
    }
    updateMatrix(matrixNo);
}


$(document).ready(function () {
    genFirstArr(5, 5);
    genSecondArr(5, 5);
    updateMatrix(1);
    updateMatrix(2);
    $("#add").click(function () {
        add();
    });
    $("#subtract").click(function () {
        subtract();
    });
    $("#multiply").click(function () {
        multiply();
    });
    for (let i = 1; i <= 2; i++) {
        $(`#addRow${i}`).click(function () {
            addRow(i);
        });
        $(`#addCol${i}`).click(function () {
            addColumn(i);
        });
        $(`#remRow${i}`).click(function () {
            removeRow(i);
        });
        $(`#remCol${i}`).click(function () {
            removeColumn(i);
        });
    }
})