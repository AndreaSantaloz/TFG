


//Botones de simulador
const simulator_model_button=document.getElementById('simulate-button')
simulator_model_button?.addEventListener('click',() =>{
    window.location.href=simulator_model_button.dataset.url;
});




// Botones de settings 
const exit_button=document.getElementById('exit-button')
exit_button?.addEventListener('click',() =>{
    window.location.href=exit_button.dataset.url;
});
const edit_button=document.getElementById('edit-profile-button')
edit_button?.addEventListener('click',() =>{
    window.location.href=edit_button.dataset.url;
});

const delete_account_button=document.getElementById('delete-account-button')
delete_account_button?.addEventListener('click',() =>{
    window.location.href=delete_account_button.dataset.url;
});

const recover_password_button=document.getElementById('recover-password')
recover_password_button?.addEventListener('click',() =>{
    window.location.href=recover_password_button.dataset.url;
});
const change_password_button=document.getElementById('change-password')
change_password_button?.addEventListener('click',() =>{
    window.location.href=change_password_button.dataset.url;
});



