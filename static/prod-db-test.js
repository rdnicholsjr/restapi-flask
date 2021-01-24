var clearbtn = document.getElementById('clearbtn');
var dbbtn = document.getElementById('dumpbtn');
var table = document.querySelector("table");
        
function generateTableHead(table, data) {
    let thead = table.createTHead();
    let row = thead.insertRow();
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

clearbtn.onclick = function(){
    console.log(String(table.rows.length) + ' rows to delete')
    for (i = table.rows.length - 1; i > -1; i--) {
        table.deleteRow(i);
    }
};

dumpbtn.onclick = function(){
    const request = new XMLHttpRequest();
    const url = 'http://localhost:5000/dev/db';
    request.open('GET', url);
    request.send();
    request.onload = (e) => {
        temp = JSON.parse(request.response)['result'];
        let data = Object.keys(temp[0]);
        generateTable(table, temp);
        generateTableHead(table, data);
    }
};
