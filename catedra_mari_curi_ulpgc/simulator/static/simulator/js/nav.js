
const login_button=document.getElementById('login-button')
login_button?.addEventListener('click',() =>{
    window.location.href=login_button.dataset.url;
});

const sign_up_button=document.getElementById('sign_up-button')
sign_up_button?.addEventListener('click',() =>{
    window.location.href=sign_up_button.dataset.url;
});


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

const upload_model_button=document.getElementById('charge-models')
upload_model_button?.addEventListener('click',() =>{
    window.location.href=upload_model_button.dataset.url;
});
