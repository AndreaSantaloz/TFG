
function no_edit_profile(){
    document.getElementById("description").readOnly =true;
    document.getElementById("researchs").readOnly =true;
}

function edit_profile(){
    document.getElementById("description").readonly=false;
    document.getElementById("researchs").readonly=false;
}

