
function switchTheme(event){
    if(event.target.click){
        document.documentElement.setAttribute('data-theme','dark');
    }else{
         document.documentElement.setAttribute('data-theme','light');
    }
}

const toggleSwitch= document.getElementById('change-mode-button');
toggleSwitch.addEventListener('click',switchTheme,false);
