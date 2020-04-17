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
const exportForm = document.getElementById('exportForm');
const exportInput = document.getElementById('exportInput');
const exportButton = document.getElementById('ExportButton');

mainBody.style.width = screen.availWidth;

navBar.style.height = '100%';

// Initialize important components on document ready
jsPlumb.ready(function() {

    // Add click event listeners to flash messages to allow closing
    let elements = document.getElementsByClassName("flash");
    for(const el of elements) {
        el.addEventListener('click', closeFlashMsg, true);
    }

    // Initialize jsPlumb to allow relationship lines and draggable classes
    jsPlumb.Defaults.Container = mainBody;

    renderLines();

    jsPlumb.draggable(document.querySelectorAll(".Class"), {
        stop: function(params) {
            ensureValidCoords(params.el.getAttribute("id"));
            ensureNoOverlap(params.el.getAttribute("id"), "none");
            jsPlumb.repaintEverything();
            updateCoords(params.el.getAttribute("id"));
        }
    });

    // Ensure lines remain useful when window resized or zoomed
    window.onresize = function (){
        jsPlumb.repaintEverything();
    };
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
    }else if(exportForm.style.display == "block"){
        closeExportBoxBeforeSubmit();
    }
}

// A way that brings the class being moved or used forward to the front for editing or anything 
// user wants to do with it.
let val = 250;
function bringForward(name) {
    val += 5;
    document.getElementById(name).style.zIndex = val;
}

//Focuses the input field of the class you are in when you want to add attributes
function addAttribute(name){
    document.getElementById(name).focus();
    document.getElementById(name).style.boxShadow = 'none';
}

// OnClick function for the edit button
function editClass(name) {
    let attrNames = document.getElementsByClassName('attrname-' + name);
    let attrTexts = document.getElementsByClassName('attrtext-' + name);
    let attrChecks = document.getElementsByClassName('container-' + name);
    

    if(document.getElementById('Relationships-' + name).style.display == 'block') {
        document.getElementById(name).classList.remove('activeEdit');
        document.getElementById(name).classList.add('non-activeEdit');
        document.getElementById('Relationships-' + name).style.display = 'none';
        document.getElementById('addAttributeForm-' + name).style.display = 'none';
        document.getElementById('class-' + name).style.display = "block";
        document.getElementById('classtext-' + name).type = "hidden";
        document.getElementById('attrsave-' + name).style.display = "none";

        for (let i = 0; i < attrNames.length; ++i)
        {
            attrNames[i].style.display = "block";
            attrTexts[i].type = "hidden";
        }
        for (let i = 0; i < attrChecks.length; ++i){
            attrChecks[i].style.display = "none";
        }

    }
    else if (document.getElementById('Relationships-' + name).style.display == 'none') {
        document.getElementById(name).classList.remove('non-activeEdit');
        document.getElementById(name).classList.add('activeEdit');
        document.getElementById('Relationships-' + name).style.display = 'block';
        document.getElementById('addAttributeForm-' + name).style.display = 'block';
        document.getElementById('class-' + name).style.display = "none";
        document.getElementById('classtext-' + name).type = "text";
        document.getElementById('attrsave-' + name).style.display = "inline-block";

        for (let i = 0; i < attrNames.length; ++i)
        {
            attrNames[i].style.display = "none";
            attrTexts[i].type = "text";
        }
        for (let i = 0; i < attrChecks.length; ++i){
            attrChecks[i].style.display = "inline";
        }
    }
    jsPlumb.repaintEverything();
}

// Displays "Add Class" popup, closes all other popups
function addClass() {
    if (loadForm.style.display == "block") {
        closeLoadBoxBeforeSubmit();
    }
    else if (saveForm.style.display == "block") {
        closeSaveBoxBeforeSubmit();
    }else if(exportForm.style.display == "block"){
        closeExportBoxBeforeSubmit();
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
function closeAddClassBeforeSubmit() {
    classInput.value = "";
    addClassForm.style.display = "none";
    addButton.classList.remove("active");
    addButton.classList.add("non-active");
}

// Displays "Save File" popup, closes all other popups
function openSaveBox() {
    if (addClassForm.style.display == "block") {
        closeAddClassBeforeSubmit();
    }
    else if (loadForm.style.display == "block") {
        closeLoadBoxBeforeSubmit();
    }else if(exportForm.style.display == "block"){
        closeExportBoxBeforeSubmit();
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
function closeSaveBoxBeforeSubmit() {
    saveInput.value = "";
    saveForm.style.display = "none";
    saveButton.classList.remove("active");
    saveButton.classList.add("non-active");
}

// Displays "Load File" popup, closes all other popups
function openLoadBox() {
    if (saveForm.style.display == "block") {
        closeSaveBoxBeforeSubmit();
    }
    else if (addClassForm.style.display == "block") {
        closeAddClassBeforeSubmit();
    }else if(exportForm.style.display == "block"){
        closeExportBoxBeforeSubmit();
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
function closeLoadBoxBeforeSubmit() {
    loadInput.value = "";
    loadForm.style.display = "none";
    loadButton.classList.remove("active");
    loadButton.classList.add("non-active");
}

// Displays "Export File" popup, closes all other popups
function openExportBox(){
    if (saveForm.style.display == "block") {
        closeSaveBoxBeforeSubmit();
    }else if (addClassForm.style.display == "block") {
        closeAddClassBeforeSubmit();
    }else if(loadForm.style.display == "block"){
        closeLoadBoxBeforeSubmit();
    }
    exportInput.value = "";
    exportForm.style.display = "block";
    exportButton.classList.remove("non-active");
    exportButton.classList.add("active");
}

// Closes "Export File" popup
function closeExportBox(){
    exportForm.style.display = "none";
    exportButton.classList.remove("active");
    exportButton.classList.add("non-active");
}

// Closes "Export File" popup, clears field
function closeExportBoxBeforeSubmit(){
    exportInput.value = "";
    exportForm.style.display = "none";
    exportButton.classList.remove("active");
    exportButton.classList.add("non-active");
}

// Upon release of the draggable component this function will be called to update cords in 
// database so that upon reload or other interface calls locations of classes will be saved
function updateCoords(name) {
    let coords = document.getElementById(name).getBoundingClientRect();
    let left = coords.left + window.scrollX;
    let top = coords.top + window.scrollY;
    let xReq = new XMLHttpRequest();
    let params = "name=" + name + "&left=" + left + "&top=" + top;
    xReq.open("POST", "/updateCoords/", true);
    xReq.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xReq.setRequestHeader("Content-length", params.length);
    xReq.setRequestHeader("Connection", "close");
    xReq.send(params);
}

// On click function for flash messages to close
function closeFlashMsg(){
    this.style.display = "none";
}

//agg-> Open Diamond 
//comp-> filled diamond
//gen-> empty arrow 
//none-> plain arrow

//Get overlay returns the an array for the overlay for relationship types
function getOverlay(relType){
    switch(relType){
        case "agg": 
            return ["Label", {location:1, width:15, length:15, "label":"◇", cssClass:"labelStyle"}];
        case "comp":
            return ["Diamond", {location:1, width:18, length:18}];
        case "gen":
            return ["PlainArrow", {location:1, width:15, length:15}];
        default: 
            return ["Arrow", {location:1, width:15, length:15, foldback:.25}];
    }
}

//getConnector is used to get the connector becuase for the agg relationship I needed
// to give the non-filled diamond a gap from the class
function getConnector(relType, from, to){
    if(relType == "agg"){
        return [(from != to ? "Flowchart" : "Bezier"),{gap:[0,11]}];
    }else{
        return (from != to ? "Flowchart" : "Bezier");
    }
}
  
// Get relationship data from database and use jsPlumb to draw lines
function renderLines(){
    let xReq = new XMLHttpRequest();
    xReq.onreadystatechange = function() {
        if (xReq.readyState == 4 && xReq.status == 200) {
            if (this.responseText != "Error: Unable to get relationship data"){
                let data = JSON.parse(this.responseText);
                for(var i = 0; i < data.length; ++i) {
                    let from = data[i].from_name;
                    let relType = data[i].rel_type;
                    let to = data[i].to_name;
                    jsPlumb.connect({
                        source:from, 
                        target:to,
                        anchor:"Continuous",
                        endpoint:"Blank",
                        connector:getConnector(relType, from, to),
                        paintStyle:{ stroke: '#6B6E70', strokeWidth:2 },
                        overlays:[getOverlay(relType)]
                    });
                }
            }
        }
    }
    xReq.open("POST", "/getRelationships/", true);
    xReq.send();
}

// Put the element back onto the screen if it gets dragged off
function ensureValidCoords(name){
    let el = document.getElementById(name);
    if (parseInt(el.style.top) < 0){
        el.style.top = 0;
    }
    if (parseInt(el.style.left) < 0){
        el.style.left = 0;
    }
}

// Prevent overlap of dragged elements when dropped
function ensureNoOverlap(name, lastMove){
    let el = document.getElementById(name);
    let rect1 = el.getBoundingClientRect();
    let classes = document.getElementsByClassName("Class");
    for (let i = 0; i < classes.length; ++i){
        if (classes[i] !== el){
            let rect2 = classes[i].getBoundingClientRect();
            var localMove = "none";

            if (!(rect1.right < rect2.left || rect1.left > rect2.right || rect1.bottom < rect2.top || rect1.top > rect2.bottom)){
                let distanceRight = rect2.right - rect1.right;
                let distanceLeft = rect1.left - rect2.left;
                let distanceTop = rect1.top - rect2.top;
                let distanceBottom = rect2.bottom - rect1.bottom;
                
                if (distanceRight < 0){
                    if (lastMove != "left"){
                        el.style.left = (rect2.right + 1) + "px";
                        localMove = "right";
                    }
                    else{
                        el.style.top = (rect2.bottom + 1) + "px";
                        localMove = "down";
                    }
                }
                else if (distanceBottom < 0){
                    if (lastMove != "up"){
                        el.style.top = (rect2.bottom + 1) + "px";
                        localMove = "down";
                    }
                    else{
                        el.style.left = (rect2.right + 1) + "px";
                        localMove = "right";
                    }
                }
                else{
                    if (distanceTop < 0 && (rect2.top - rect1.height - 1) > 0 ){
                        if (lastMove != "down"){
                            el.style.top = (rect2.top - rect1.height - 1) + "px";
                            localMove = "up";
                        }
                        else{
                            el.style.left = (rect2.right + 1) + "px";
                            localMove = "right";
                        }
                    }
                    else if (distanceLeft < 0 && (rect2.left - rect1.width - 1) > 0){
                        if (lastMove != "right"){
                            el.style.left = (rect2.left - rect1.width - 1) + "px";
                            localMove = "left";
                        }
                        else{
                            el.style.top = (rect2.bottom + 1) + "px";
                            localMove = "down";
                        }
                    }
                    else{
                        if (lastMove != "left"){
                            el.style.left = (rect2.right + 1) + "px";
                            localMove = "right";
                        }
                        else{
                            el.style.top = (rect2.bottom + 1) + "px";
                            localMove = "down";
                        }
                    }
                }

                ensureNoOverlap(name, localMove);
            }
        }
    }
}

// Two possible states for the entrance of this function:
//   If the process is in the first stage (no class has been selected):
//     Save the clicked name, open the help prompt
//     Allows the next part to occur
//   If the process is halfway (one class has already been selected):
//     Prompt for type until given a valid type or cancelled.
//     If given type, call to add the relationship
let class_clicked = "";
function readyRelationship(name){
    if (class_clicked == ""){
        class_clicked = name;
        let addRelHelp = document.getElementById("addRelHelp");
        addRelHelp.style.display = "block";
    }
    else{
        let type = "";
        while (true){
            let attempt = prompt("What type of relationship?\n\nagg, comp, gen, or none");
            if (attempt == "agg" || attempt == "comp" || attempt == "gen" || attempt == "none"){
                type = attempt;
                break;
            }
            if (attempt == null){
                cancelAddRel();
                return;
            }
        }

        addRelationship(class_clicked, name, type);
        class_clicked = "";
    }
    
}

// Given a 'from' name, 'to' name, and relationship type,
//   send a request to add a relationship and render the line.
function addRelationship(from, to, type){
    let xReq = new XMLHttpRequest();
    xReq.onreadystatechange = function() {
        if (xReq.readyState == 4 && xReq.status == 200) {
           window.location.replace("/");
        }
    }
    let params = "class_name=" + from + "&to=" + to + "&rel_type=" + type;
    xReq.open("POST", "/addRelationship/", true);
    xReq.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xReq.setRequestHeader("Content-length", params.length);
    xReq.setRequestHeader("Connection", "close");
    xReq.send(params);
}

// Upon cancelling adding a relationship, clear progress of that process
function cancelAddRel(){
    class_clicked = "";
    let addRelHelp = document.getElementById("addRelHelp");
    addRelHelp.style.display = "none";
}