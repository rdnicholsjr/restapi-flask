const clearbtn = document.getElementById("clearbtn");
const dbbtn = document.getElementById("dumpbtn");
const databaseServer = "localhost:5000"
const database = "dev/db"
var table = document.querySelector("table");

function generateTableHead(table, data) {
    let tableHead = table.createTHead();
    let row = tableHead.insertRow();
    for (let key of data) {
        let th = document.createElement("th");
        let text = document.createTextNode(key);
        th.appendChild(text);
        row.appendChild(th);
    }
}

function generateTable(table, data) {
    for (let element of data) {
        let row = table.insertRow();
        for (key in element) {
            let cell = row.insertCell();
            let text = document.createTextNode(element[key]);
            cell.appendChild(text);
        }
    }
}

clearbtn.onclick = function () {
    console.log(String(table.rows.length) + " rows to delete")
    for (i = table.rows.length - 1; i > -1; i--) {
        table.deleteRow(i);
    }
};

dumpbtn.onclick = function () {
    const request = new XMLHttpRequest();
    const url = "http://" + databaseServer + "/" + database;
    request.open("GET", url);
    request.send();
    request.onload = (e) => {
        temp = JSON.parse(request.response)["result"];
        let data = Object.keys(temp[0]);
        generateTable(table, temp);
        generateTableHead(table, data);
    }
};