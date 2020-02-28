/**
 * Defines view responses to user input and dynamically adjusts some components.
 */

// Declaring and Initializing key components of GUI
const mainBody = document.querySelector('.main-body');
const navBar = document.querySelector('.navBar');
const navTab = document.getElementById('navTab');
const loadForm = document.getElementById('loadForm');
const loadInput = document.getElementById('loadInput');
const loadButton = document.getElementById('LoadButton');
const saveForm = document.getElementById('saveForm');
const saveInput = document.getElementById('saveInput');
const saveButton = document.getElementById('SaveButton');
const addClassForm = document.getElementById('AddClassForm');
const classInput = document.getElementById('ClassInput');
const addButton = document.getElementById('AddButton');


mainBody.style.width = screen.availWidth;

navBar.style.height = '100%';

//Creates the Draggable component for the classes

Draggable.create('.draggable', {
    bounds: {
        top: 5,
        left: 5
    },
    onRelease: function () {
        updateCoords(this.target.getAttribute("id"));
    },
});

// Toggles the navBar sliding in and out from left
function navBarAction(){
    navBar.classList.toggle('navActive');
    navTab.classList.toggle('toggle');
    if (loadForm.style.display == "block") {
        closeLoadBoxBeforeSubmit();
    }
    else if (saveForm.style.display == "block") {
        closeSaveBoxBeforeSubmit();
    }
    else if (addClassForm.style.display == "block") {
        closeAddClassBeforeSubmit();
    }
}

function addAttribute(name){
    document.getElementById(name).focus();
    document.getElementById(name).style.boxShadow = 'none';
}

// OnClick function for the edit button
function editClass(name) {
    if(document.getElementById('Relationships-' + name).style.display == 'block') {
        document.getElementById('attInput-' + name).value = "";
        document.getElementById('Relationships-' + name).style.display = 'none';
        document.getElementById('addAttributeForm-' + name).style.display = 'none';
        document.getElementById('attInput-' + name).blur();
    }
    else if (document.getElementById('Relationships-' + name).style.display == 'none') {
        document.getElementById('Relationships-' + name).style.display = 'block';
        document.getElementById('addAttributeForm-' + name).style.display = 'block';
    }
}

// Displays "Add Class" popup, closes all other popups
// TODO: Utilize existing functions, rather than copy-pasting
function addClass() {
    if (loadForm.style.display == "block") {
        closeLoadBoxBeforeSubmit();
    }
    else if (saveForm.style.display == "block") {
        closeSaveBoxBeforeSubmit();
    }
    classInput.value = "";
    addClassForm.style.display = "block";
    addButton.classList.remove("non-active");
    addButton.classList.add("active");
}

// Closes "Add Class" popup
function closeAddClass() {
    addClassForm.style.display = "none";
    addButton.classList.remove("active");
    addButton.classList.add("non-active");
}

// Closes "Add Class" popup, clears field
// TODO: This and "closeAddClass" should probably be one function
function closeAddClassBeforeSubmit() {
    classInput.value = "";
    addClassForm.style.display = "none";
    addButton.classList.remove("active");
    addButton.classList.add("non-active");
}

// Displays "Save File" popup, closes all other popups
// TODO: Utilize existing functions, rather than copy-pasting
function openSaveBox() {
    if (addClassForm.style.display == "block") {
        closeAddClassBeforeSubmit();
    }
    else if (loadForm.style.display == "block") {
        closeLoadBoxBeforeSubmit();
    }
    saveInput.value = "";
    saveForm.style.display = "block";
    saveButton.classList.remove("non-active");
    saveButton.classList.add("active");
}

// Closes "Save File" popup
function closeSaveBox() {
    saveForm.style.display = "none";
    saveButton.classList.remove("active");
    saveButton.classList.add("non-active");
}

// Closes "Save File" popup, clears field
// TODO: This and "closeSaveBox" should probably be one function
function closeSaveBoxBeforeSubmit() {
    saveInput.value = "";
    saveForm.style.display = "none";
    saveButton.classList.remove("active");
    saveButton.classList.add("non-active");
}

// Displays "Load File" popup, closes all other popups
// TODO: Utilize existing functions, rather than copy-pasting
function openLoadBox() {
    if (saveForm.style.display == "block") {
        closeSaveBoxBeforeSubmit();
    }
    else if (addClassForm.style.display == "block") {
        closeAddClassBeforeSubmit();
    }
    loadInput.value = "";
    loadForm.style.display = "block";
    loadButton.classList.remove("non-active");
    loadButton.classList.add("active");
}

// Closes "Load File" popup
function closeLoadBox() {
    loadForm.style.display = "none";
    loadButton.classList.remove("active");
    loadButton.classList.add("non-active");
}

// Closes "Load File" popup, clears field
// TODO: This and "closeLoadBox" should probably be one function
function closeLoadBoxBeforeSubmit() {
    loadInput.value = "";
    loadForm.style.display = "none";
    loadButton.classList.remove("active");
    loadButton.classList.add("non-active");
}

// Upon release of the draggable component this function will be called to update cords in 
// database so that upon reload or other interface calls locations of classes will be saved
function updateCoords(name) {
    let coords = document.getElementById(name).getBoundingClientRect();
    let xReq = new XMLHttpRequest();
    let params = "name=" + name + "&left=" + coords.left + "&top=" + coords.top;
    xReq.open("POST", "/updateCoords/", true);
    xReq.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xReq.setRequestHeader("Content-length", params.length);
    xReq.setRequestHeader("Connection", "close");
    xReq.send(params);
}

function closeFlashMsg(){
    document.getElementById("flashMsg").style.display = "none";
}