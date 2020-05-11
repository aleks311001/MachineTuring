let table = document.getElementById('ribbon_machine');
let ribbon = table.rows[0];
let index_ribbon = table.rows[1];

table.style.marginLeft = '-25px';
let numberCellsOnDisplay = document.body.clientWidth / 55;

for (let i = 0; i < numberCellsOnDisplay; ++i) {
    addCell(i, -Math.floor(numberCellsOnDisplay / 2) + i);
}

let widthCell = ribbon.cells[0].offsetWidth;
let middle = Math.floor(numberCellsOnDisplay / 2);
let reallyMarginLeft = parseInt(table.style.marginLeft);

drawBorrow();
table.style.marginTop = '-10px';
let timerMakeNextStepId;
drawAfterLoad();
moveAfterAdd(30);

ribbon.cells[middle].children[0].focus();

document.onkeydown = checkKey;

function addCell(real_index_ceil, write_index_ceil, default_value = null) {
    let newCell = ribbon.insertCell(real_index_ceil);
    newCell.setAttribute('class', 'cell cell-ribbon');

    let input = document.createElement("input");
    input.setAttribute('class', 'input input-ribbon');
    input.setAttribute('type', 'text');
    input.setAttribute('maxlength', '1');
    input.setAttribute('name', 'ribbon~' + write_index_ceil);
    input.setAttribute('autocomplete', 'off');
    if (default_value != null) {
        input.setAttribute('value', default_value);
    } else {
        input.setAttribute('value', '_');
    }

    //inp.setAttribute('autofocus', 'autofocus');
    newCell.append(input);

    let newIndexCell = index_ribbon.insertCell(real_index_ceil);
    newIndexCell.setAttribute('class', 'cell index-cell-ribbon');
    newIndexCell.innerHTML = write_index_ceil;
}

function checkKey(e) {
    let activeParentParent = document.activeElement.parentElement.parentElement;
    if (activeParentParent === ribbon) {
        if (e.keyCode === 37) {
            moveRibbonLeft();
        } else if (e.keyCode === 39) {
            moveRibbonRight();
        }
    } else if (activeParentParent.parentElement.parentElement.parentElement ===
               document.getElementById("program_machine")) {
        if (e.keyCode === 37) {
            activeParentParent.previousElementSibling.children[0].children[0].focus();
        } else if (e.keyCode === 39) {
            activeParentParent.nextElementSibling.children[0].children[0].focus();
        } else if (e.keyCode === 38) {
            let index = activeParentParent.cellIndex
            activeParentParent.parentElement.previousElementSibling.children[index].children[0].children[0].focus();
        } else if (e.keyCode === 40) {
            let index = activeParentParent.cellIndex
            activeParentParent.parentElement.nextElementSibling.children[index].children[0].children[0].focus();
        }
    }
}

function moveAfterAdd(delay) {
    let difference = reallyMarginLeft - parseInt(table.style.marginLeft);
    let moveVal = Math.sign(difference) * Math.ceil(Math.abs(difference) / 8);

    if (widthCell / 10 <= Math.abs(difference) && Math.abs(difference) <= widthCell) {
        moveVal = Math.sign(difference) * widthCell / 10;
    }

    table.style.marginLeft = (parseInt(table.style.marginLeft) + moveVal).toString() + 'px';

    setTimeout(function () {moveAfterAdd(delay);}, delay);
}

function moveRibbonLeft() {
    if (reallyMarginLeft / widthCell > -1) {
        addCell(0, parseInt(index_ribbon.cells[0].innerHTML) - 1);
        table.style.marginLeft = (parseInt(table.style.marginLeft) - widthCell).toString() + 'px';
    } else {
        reallyMarginLeft += widthCell;
        --middle;
    }
    //document.write(JSON.parse(table.dataset.ribbonss));
    //document.write(table.dataset.ribbonss.toString());//table.dataset.ribbonss);

    ribbon.cells[middle].children[0].focus();
}
function moveRibbonRight() {
    if ((document.body.clientWidth - reallyMarginLeft) / widthCell > ribbon.cells.length - 1) {
        addCell(ribbon.cells.length, parseInt(index_ribbon.cells[ribbon.cells.length - 1].innerHTML) + 1);
    }

    reallyMarginLeft -= widthCell;
    ++middle;
    ribbon.cells[middle].children[0].focus();
}

function makeNextStep(moves, change_symbols, executed, statuses, index) {
    if (index >= moves.length) {
        return;
    }

    ribbon.cells[middle].children[0].setAttribute('value', change_symbols[index]);
    executed.setAttribute('value', statuses[index]);

    let pos_input = document.getElementById('pos');
    makeMiddleCommonIndex();
    if (moves[index] === '<') {
        moveRibbonLeft();
        //pos_input.setAttribute('value', (parseInt(pos_input.getAttribute('value')) - 1).toString());
    } else if (moves[index] === '>') {
        moveRibbonRight();
        //pos_input.setAttribute('value', (parseInt(pos_input.getAttribute('value')) + 1).toString());
    }
    pos_input.setAttribute('value', (middle + parseInt(index_ribbon.cells[0].innerHTML)).toString());
    makeMiddleMainIndex();

    timerMakeNextStepId = setTimeout(function () {makeNextStep(moves, change_symbols, executed, statuses, index + 1);}, 250);
}

function drawAfterLoad() {
    let ribbon_data = JSON.parse(table.dataset.ribbon);
    let ribbon_extremum = JSON.parse(table.dataset.ribbon_extremum);

    drawRibbon(ribbon_data, ribbon_extremum);

    let executed = document.getElementById("status");
    let moves = JSON.parse(executed.dataset.moves);
    let statuses = JSON.parse(executed.dataset.statuses);
    let pos = parseInt(executed.dataset.pos);
    let change_symbols = JSON.parse(executed.dataset.change_symbols);
    document.getElementById('pos').setAttribute('value', pos.toString());

    middle += pos;
    reallyMarginLeft -= pos * widthCell;
    table.style.marginLeft = reallyMarginLeft.toString() + 'px';

    makeNextStep(moves, change_symbols, executed, statuses, 0);
}

function drawRibbon(ribbon_data, ribbon_extremum) {
    for (let i = 0; i <= ribbon_extremum['max_index']; ++i) {
        let real_index = i - parseInt(index_ribbon.cells[0].innerHTML);
        if (i <= parseInt(index_ribbon.cells[ribbon.cells.length - 1].innerHTML)) {
            ribbon.cells[real_index].children[0].setAttribute('value', ribbon_data[i]);
        } else {
            addCell(real_index, i, ribbon_data[i]);
        }
    }

    for (let i = -1; i >= ribbon_extremum['min_index']; --i) {
        if (i >= parseInt(index_ribbon.cells[0].innerHTML)) {
            let real_index = i - parseInt(index_ribbon.cells[0].innerHTML);
            ribbon.cells[real_index].children[0].setAttribute('value', ribbon_data[i]);
        } else {
            addCell(0, i, ribbon_data[i]);
            ++middle;
            reallyMarginLeft -= widthCell;
            table.style.marginLeft = reallyMarginLeft.toString() + 'px';
        }
    }
}
function drawBorrow() {
    document.getElementById("borrow").style.marginLeft = (middle * widthCell - widthCell * 0.4).toString() + 'px';
    document.getElementById("borrow").style.marginTop = '-70px';
    document.getElementById("borrow").style.color = 'red';
}

function makeMiddleCommonIndex() {
    index_ribbon.cells[middle].style.fontWeight = "500";
    index_ribbon.cells[middle].style.fontSize = "15px";
}
function makeMiddleMainIndex() {
    index_ribbon.cells[middle].style.fontWeight = "700";
    index_ribbon.cells[middle].style.fontSize = "20px";
}

function stopMakeNextStep() {
    clearTimeout(timerMakeNextStepId);
}