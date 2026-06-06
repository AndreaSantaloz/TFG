
const dark_mode_save = localStorage.getItem('dark-mode');
const section = document.getElementById('section-dark-mode-button');
const button = document.getElementById('darkmode-button');
if(dark_mode_save == 'enabled'){
    document.body.classList.add('dark-mode');
}

function changeMode(){
    document.body.classList.toggle('dark-mode');
    if(document.body.classList.contains('dark-mode')){
        localStorage.setItem('dark-mode','enabled');
        section.style.justifyContent="flex-end";
        section.style.backgroundColor="#312112";
        section.style.borderColor="#7d6a58"
        button.style.backgroundColor="#e3cebb"
    }else{
        localStorage.setItem('dark-mode','disabled');
        section.style.justifyContent="flex-start";
        section.style.backgroundColor="#fdf5e6";
        section.style.borderColor="#c5ac95"
        button.style.backgroundColor="#7d6a58"
    }

}


