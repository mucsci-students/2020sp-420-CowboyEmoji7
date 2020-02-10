document.querySelector('.main-body').style.width = screen.availWidth;
const container = document.querySelector('.main-body');

document.querySelector('.navBar').style.height = '96%';

Draggable.create('.draggable', {
    bounds: container
});

focusMethod = function getFocus(){
    document.getElementById('saveInput').focus();
}

function addClass(){
    if(document.getElementById('loadForm').style.display == "block")
    {
        document.getElementById('loadInput').value = "";
        document.getElementById('loadForm').style.display = "none";
        document.getElementById('LoadButton').classList.remove("active");
        document.getElementById('LoadButton').classList.add("non-active");
    }
    else if(document.getElementById('saveForm').style.display == "block")
    {
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

function closeAddClass(){
    document.getElementById('AddClassForm').style.display = "none";
    document.getElementById('AddButton').classList.remove("active");
    document.getElementById('AddButton').classList.add("non-active");
}

function closeAddClassBeforeSubmit(){
    document.getElementById('ClassInput').value = "";
    document.getElementById('AddClassForm').style.display = "none";
    document.getElementById('AddButton').classList.remove("active");
    document.getElementById('AddButton').classList.add("non-active");
}


function openSaveBox() {
    if(document.getElementById('AddClassForm').style.display == "block")
    {
        document.getElementById('ClassInput').value = "";
        document.getElementById('AddClassForm').style.display = "none";
        document.getElementById('AddButton').classList.remove("active");
        document.getElementById('AddButton').classList.add("non-active");
    }
    else if(document.getElementById('loadForm').style.display == "block")
    {
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

function closeSaveBox() {
    document.getElementById('saveForm').style.display = "none";
    document.getElementById('SaveButton').classList.remove("active");
    document.getElementById('SaveButton').classList.add("non-active");
}

function closeSaveBoxBeforeSubmit() {
    document.getElementById('saveInput').value = "";
    document.getElementById('saveForm').style.display = "none";
    document.getElementById('SaveButton').classList.remove("active");
    document.getElementById('SaveButton').classList.add("non-active");
}

function openLoadBox(){
    if(document.getElementById('saveForm').style.display == "block")
    {
        document.getElementById('saveInput').value = "";
        document.getElementById('saveForm').style.display = "none";
        document.getElementById('SaveButton').classList.remove("active");
        document.getElementById('SaveButton').classList.add("non-active");
    }
    else if(document.getElementById('AddClassForm').style.display == "block")
    {
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

function closeLoadBox(){
    document.getElementById('loadForm').style.display = "none";
    document.getElementById('LoadButton').classList.remove("active");
    document.getElementById('LoadButton').classList.add("non-active");
}

function closeLoadBoxBeforeSubmit(){
    document.getElementById('loadInput').value = "";
    document.getElementById('loadForm').style.display = "none";
    document.getElementById('LoadButton').classList.remove("active");
    document.getElementById('LoadButton').classList.add("non-active");
}