var clearbtn = document.getElementById('clearbtn');
var searchbtn = document.getElementById('searchbtn');
var table = document.querySelector("table");
var searchinput = document.getElementById('searchfilter');
var usertoaddbox = document.getElementById('newusernamebox');
var emailtoaddbox = document.getElementById('newuseremailbox');
var useraddbtn = document.getElementById('useraddbtn');
var statusmsg = document.getElementById('statusmsg');


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
    var rowcount = 1;
    for (let element of data) {
        let row = table.insertRow();
        for (key in element) {
            let cell = row.insertCell();
            let text = document.createTextNode(element[key]);
            cell.appendChild(text);
        }
        //Delete button
        var delbtn = document.createElement("button");
        delbtn.value=rowcount;
        delbtn.innerHTML="DEL";
        delbtn.addEventListener("click", delbtnfnc);
        let delcell = row.insertCell();
        delcell.appendChild(delbtn);
        
        //Edit button
        var edbtn = document.createElement('button');
        edbtn.value=rowcount;
        edbtn.innerHTML='EDIT';
        edbtn.addEventListener('click', editfieldfnc);
        let edcell = row.insertCell();
        edcell.appendChild(edbtn);

        rowcount += 1;        
    }
}

function delbtnfnc() {
    var url = 'http://localhost:5000/dev/db/' + String(table.rows[this.value].cells[0].innerHTML);
    const request = new XMLHttpRequest();
    request.open('DELETE', url);
    request.send();
    request.onload = (e) => {
        if (JSON.parse(request.response)['result']) {
            for (scell = 0; scell < 2; scell++) {
                table.rows[this.value].cells[scell].innerHTML = "<s>" + String(table.rows[this.value].cells[scell].innerHTML) + "</s>";
            }
        }
    }
}

function clearTable(table) {
    for (i = table.rows.length - 1; i > -1; i--) {
        table.deleteRow(i);
    }
}

clearbtn.onclick = function(){
    //Leave this Ben...  I need to extract this into sampe (re-usable) code.
    //console.log(String(table.rows.length) + ' rows to delete')
    searchinput.value="";
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
    searchinput.value="";
};

useraddbtn.onclick = function(){
    var usertoadd = {'name': usertoaddbox.value, 'email': emailtoaddbox.value};
    if ((usertoadd['name'] != "") && (usertoadd['email'] != "")) {
        var url = 'http://localhost:5000/dev/db'
        const request = new XMLHttpRequest();
        request.open('POST', url);
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.send(JSON.stringify(usertoadd));
        request.onload = (e) => {
            if (JSON.parse(request.response)['result']) {
                statusmsg.innerHTML = "user " + usertoadd['name'] + " added";
                usertoaddbox.value = "";
                emailtoaddbox.value = "";
            } else {
                addfailed();
            }
        }
    } else {
        addfailed();
    }
};


function addfailed() {
    statusmsg.innerHTML = "User add failed";
};


function editfieldfnc() {
    //So much easier to handle...
    var oldmail=String(table.rows[this.value].cells[1].innerHTML);

    //remove HTML marking for italication if they exist from previous edit without refreshing table info.
    if (oldmail.slice(0,3) == "<i>") {
        oldmail = oldmail.slice(3, (oldmail.length - 4))
    }

    var newemail = prompt("User's new email:", oldmail);

    //push change to DB and italicize new email if successful.
    if ((newemail != null ) && (newemail != "") && (newemail != oldmail)) {
        var url = 'http://localhost:5000/dev/db/' + String(table.rows[this.value].cells[0].innerHTML);
        const request = new XMLHttpRequest();
        request.open('PATCH', url);
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.send(JSON.stringify(newemail));
        request.onload = (e) => {
            if (JSON.parse(request.response)['result']) {
                table.rows[this.value].cells[1].innerHTML = "<i>" + newemail + "</i>";
            } else {
                statusmsg.innerHTML = "Edit failed";
            }
        }
    }
};
