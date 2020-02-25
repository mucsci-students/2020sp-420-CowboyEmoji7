/**
 * Defines view responses to user input and dynamically adjusts some components.
 */

document.querySelector('.main-body').style.width = screen.availWidth;
const container = document.querySelector('.main-body');

document.querySelector('.navBar').style.height = '96%';

Draggable.create('.draggable', {
    bounds: container,
    onDragEnd: function () {
        updateCoords(this.target.getAttribute("id"));
    }
});

// Displays "Add Class" popup, closes all other popups
// TODO: Utilize existing functions, rather than copy-pasting
function addClass() {
    if (document.getElementById('loadForm').style.display == "block") {
        document.getElementById('loadInput').value = "";
        document.getElementById('loadForm').style.display = "none";
        document.getElementById('LoadButton').classList.remove("active");
        document.getElementById('LoadButton').classList.add("non-active");
    }
    else if (document.getElementById('saveForm').style.display == "block") {
        document.getElementById('saveInput').value = "";
        document.getElementById('saveForm').style.display = "none";
        document.getElementById('SaveButton').classList.remove("active");
        document.getElementById('SaveButton').classList.add("non-active");
    }
    document.getElementById('ClassInput').value = "";
    document.getElementById('AddClassForm').style.display = "block";
    document.getElementById('AddButton').classList.remove("non-active");
    document.getElementById('AddButton').classList.add("active");
}

// Closes "Add Class" popup
function closeAddClass() {
    document.getElementById('AddClassForm').style.display = "none";
    document.getElementById('AddButton').classList.remove("active");
    document.getElementById('AddButton').classList.add("non-active");
}

// Closes "Add Class" popup, clears field
// TODO: This and "closeAddClass" should probably be one function
function closeAddClassBeforeSubmit() {
    document.getElementById('ClassInput').value = "";
    document.getElementById('AddClassForm').style.display = "none";
    document.getElementById('AddButton').classList.remove("active");
    document.getElementById('AddButton').classList.add("non-active");
}

// Displays "Save File" popup, closes all other popups
// TODO: Utilize existing functions, rather than copy-pasting
function openSaveBox() {
    if (document.getElementById('AddClassForm').style.display == "block") {
        document.getElementById('ClassInput').value = "";
        document.getElementById('AddClassForm').style.display = "none";
        document.getElementById('AddButton').classList.remove("active");
        document.getElementById('AddButton').classList.add("non-active");
    }
    else if (document.getElementById('loadForm').style.display == "block") {
        document.getElementById('loadInput').value = "";
        document.getElementById('loadForm').style.display = "none";
        document.getElementById('LoadButton').classList.remove("active");
        document.getElementById('LoadButton').classList.add("non-active");
    }
    document.getElementById('saveInput').value = "";
    document.getElementById('saveForm').style.display = "block";
    document.getElementById('SaveButton').classList.remove("non-active");
    document.getElementById('SaveButton').classList.add("active");
}

// Closes "Save File" popup
function closeSaveBox() {
    document.getElementById('saveForm').style.display = "none";
    document.getElementById('SaveButton').classList.remove("active");
    document.getElementById('SaveButton').classList.add("non-active");
}

// Closes "Save File" popup, clears field
// TODO: This and "closeSaveBox" should probably be one function
function closeSaveBoxBeforeSubmit() {
    document.getElementById('saveInput').value = "";
    document.getElementById('saveForm').style.display = "none";
    document.getElementById('SaveButton').classList.remove("active");
    document.getElementById('SaveButton').classList.add("non-active");
}

// Displays "Load File" popup, closes all other popups
// TODO: Utilize existing functions, rather than copy-pasting
function openLoadBox() {
    if (document.getElementById('saveForm').style.display == "block") {
        document.getElementById('saveInput').value = "";
        document.getElementById('saveForm').style.display = "none";
        document.getElementById('SaveButton').classList.remove("active");
        document.getElementById('SaveButton').classList.add("non-active");
    }
    else if (document.getElementById('AddClassForm').style.display == "block") {
        document.getElementById('ClassInput').value = "";
        document.getElementById('AddClassForm').style.display = "none";
        document.getElementById('AddButton').classList.remove("active");
        document.getElementById('AddButton').classList.add("non-active");
    }
    document.getElementById('loadInput').value = "";
    document.getElementById('loadForm').style.display = "block";
    document.getElementById('LoadButton').classList.remove("non-active");
    document.getElementById('LoadButton').classList.add("active");
}

// Closes "Load File" popup
function closeLoadBox() {
    document.getElementById('loadForm').style.display = "none";
    document.getElementById('LoadButton').classList.remove("active");
    document.getElementById('LoadButton').classList.add("non-active");
}

// Closes "Load File" popup, clears field
// TODO: This and "closeLoadBox" should probably be one function
function closeLoadBoxBeforeSubmit() {
    document.getElementById('loadInput').value = "";
    document.getElementById('loadForm').style.display = "none";
    document.getElementById('LoadButton').classList.remove("active");
    document.getElementById('LoadButton').classList.add("non-active");
}

function updateCoords(name) {
    var coords = document.getElementById(name).getBoundingClientRect();
    var xReq = new XMLHttpRequest();
    var params = "name=" + name + "&left=" + coords.left + "&top=" + coords.top;
    xReq.open("POST", "/updateCoords/", true);
    xReq.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xReq.setRequestHeader("Content-length", params.length);
    xReq.setRequestHeader("Connection", "close");
    xReq.send(params);
}