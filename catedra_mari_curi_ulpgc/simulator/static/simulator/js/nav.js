

//Botones de autenticación 

const login_button=document.getElementById('login-button')
login_button?.addEventListener('click',() =>{
    window.location.href=login_button.dataset.url;
});

const sign_up_button=document.getElementById('sign_up-button')
sign_up_button?.addEventListener('click',() =>{
    window.location.href=sign_up_button.dataset.url;
});

// Botones de menú

const simulator_button=document.getElementById('dashboard-button')
simulator_button?.addEventListener('click',() =>{
    window.location.href=simulator_button.dataset.url;
});

const profile_button=document.getElementById('profile-button')
profile_button?.addEventListener('click',() =>{
    window.location.href=profile_button.dataset.url;
});

const store_button=document.getElementById('store-button')
store_button?.addEventListener('click',() =>{
    window.location.href=store_button.dataset.url;
});

const setting_button=document.getElementById('setting-button')
setting_button?.addEventListener('click',() =>{
    window.location.href=setting_button.dataset.url;
});

const tutorial_button=document.getElementById('tutorial-button')
tutorial_button?.addEventListener('click',() =>{
    window.location.href=tutorial_button.dataset.url;
});

const upload_model_button=document.getElementById('charge-models')
upload_model_button?.addEventListener('click',() =>{
    window.location.href=upload_model_button.dataset.url;
});

//Botones de simulador

const tabular_button=document.getElementById('tabular_chart')
tabular_button?.addEventListener('click',() =>{
    window.location.href=tabular_button.dataset.url;
});

const dispersion_button=document.getElementById('dispersion_chart')
dispersion_button?.addEventListener('click',() =>{
    window.location.href=dispersion_button.dataset.url;
});

const correlation_button=document.getElementById('correlation_chart')
correlation_button?.addEventListener('click',() =>{
    window.location.href=correlation_button.dataset.url;
});

const volume_button=document.getElementById('volumen_chart')
volume_button?.addEventListener('click',() =>{
    window.location.href=volume_button.dataset.url;
});

const error_button =document.getElementById('error_chart')
error_button?.addEventListener('click',() =>{
    window.location.href=error_button.dataset.url;
});

// Botones de settings 
const exit_button=document.getElementById('exit-button')
exit_button?.addEventListener('click',() =>{
    window.location.href=exit_button.dataset.url;
});
