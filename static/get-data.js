var clearbtn = document.getElementById('clearbtn');
var searchbtn = document.getElementById('searchbtn');
var table = document.querySelector("table");
var searchinput = document.getElementById('searchfilter');

        
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

function clearTable(table) {
    for (i = table.rows.length - 1; i > -1; i--) {
        table.deleteRow(i);
    }
}

clearbtn.onclick = function(){
    console.log(String(table.rows.length) + ' rows to delete')
    searchfilter.value="";
    clearTable(table)
};

searchbtn.onclick = function(){
    clearTable(table)
    var searchstring = searchinput.value
    var url = 'http://localhost:5000/dev/db';
    if (searchstring != "") {
        url += '/' + searchstring;
    }
    const request = new XMLHttpRequest();
    request.open('GET', url);
    request.send();
    request.onload = (e) => {
        temp = JSON.parse(request.response)['result'];
        let data = Object.keys(temp[0]);
        generateTable(table, temp);
        generateTableHead(table, data);
    }
};