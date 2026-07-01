const layoutLineal = {
    xaxis:{title:'Time(t)'},
    xaxis:{title:'Time(t)'},
    hovermode:'closest'
}

function create_chart(name,data,layout){
    Plotly.newPlot(name,data,layout);
}

document.addEventListener("DOMContentLoaded",function(){
    //Zona de gestión de datos
    const data = document.getElementById('json');
    console.log(data);
    if(!data || !data.textContent.trim()){
        alert("Los datos no son validos");
    }
    const datas = JSON.parse(data.textContent.trim());
    const t_axis = datas?.final_results?.time;
    const c_plano = datas?.final_results?.concentration;
    const rows = datas.initial_data.rowN_ || datas.initial_data.N_ || 1;
    const cols = datas.initial_data.columnN_ || 1;
    const depths = datas.initial_data.depthN_ || 1;
    const timestap = t_axis.length;
    if (document.getElementById('rows')) document.getElementById('rows').textContent = "Rows: " + rows;
    if (document.getElementById('cols')) document.getElementById('cols').textContent = "Columns: " + cols;
    if (document.getElementById('depths')) document.getElementById('depths').textContent = "Depth: " + depths;
    if (document.getElementById('compartimentals')) {
            document.getElementById("compartimentals").textContent = datas.initial_data.rowN_ || datas.initial_data.N_ || rows;
        }
    if (document.getElementById('start_t')) document.getElementById('start_t').textContent = datas.initial_data.start_t + " s";
    if (document.getElementById('end_t')) document.getElementById('end_t').textContent = datas.initial_data.end_t + " s";
    if (document.getElementById('delta_t')) document.getElementById('delta_t').textContent = datas.initial_data.delta_t + " s";
    const title = document.getElementById('dynamic-title');
    title.innerText = "Charge the input datas!";

      
})