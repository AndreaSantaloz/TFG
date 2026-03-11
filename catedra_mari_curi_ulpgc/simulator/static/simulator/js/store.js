
const add_model_button=document.getElementById('add-button')
add_model_button?.addEventListener('click',() =>{
    window.location.href=add_model_button.dataset.url;
})

const delete_model_button=document.getElementById('delete-button')
delete_model_button?.addEventListener('click',() =>{
    window.location.href=delete_model_button.dataset.url;
})

const update_model_button = document.getElementById('update-button')
update_model_button?.addEventListener('click',()=>{
    window.location.href=update_model_button.dataset.url;
})


const simulate_model_button=document.getElementById('simulate-button')
simulate_model_button?.addEventListener('click',() =>{
    window.location.href=simulate_model_button.dataset.url;
})