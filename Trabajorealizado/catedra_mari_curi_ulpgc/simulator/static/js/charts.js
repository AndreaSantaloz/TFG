

let time = []
let concentration = [];

document.addEventListener("DOMContentLoaded", function () {

    time = JSON.parse((document.getElementById("time")).textContent);
    console.log(time);
    concentration = JSON.parse(
                                (document.getElementById("concentration")).textContent
                              );
    console.log(concentration);
  
});



function table() {
    const section = document.querySelector('#charts'); 
    section.replaceChildren(); 
    var tableDiv = document.createElement('div');
    tableDiv.id = "table";
    section.appendChild(tableDiv); 
    var values = time;
    var data = [{
        type: 'table',
        header: {
            values: [["<b>Time</b>"]],
            align: 'center',
            line: {width: 1, color: 'black'},
            fill: {color: 'grey'},
            font: {family: 'Arial', size: 12, color: 'white'}
        },
        cells: {
            values: [values],
            align: 'center',
            line: {width: 1, color: 'black'},
            fill: {color: 'white'},
            font: {family: 'Arial', size: 11, color: 'black'}
        }
    }];
   Plotly.newPlot('table',data);
}

function correlation(){
    const section = document.querySelector('#charts');
    section.replaceChildren(); 
    var heatmap= document.createElement('div');
    var scatter = document.createElement('div');
    heatmap.id="heatmap_chart";
    scatter.id="scatter_chart";
    section.appendChild(heatmap)
    section.appendChild(scatter)
     var data = [
                {
                  z:[[1,20,30],[20,1,60],[30,60,1]],
                  type:'heatmap'
                }
                
              ];
    var layout={
                title:{
                   text:'Gráfica heatmap',
                },
               
              };
               Plotly.newPlot('heatmap_chart',data,layout,{staticPlot:true});

    var trace1={
                x:[1,2,3],
                y:[90,40,60],
                type:'scatter'
              };
    var data = [trace1];
    var layout={
                title:{
                   text:'Gráfica de puntos',
                },
                showlegend:false,
              };

                
               Plotly.newPlot('scatter_chart',data,layout,{staticPlot:true});
            
}
function dispersion(){
    const section = document.querySelector('#charts');
    section.replaceChildren(); 
    
    var lineal = document.createElement('div');
    lineal.id = "lineal_chart";
    section.appendChild(lineal);
     
    // Necesitas definir 'data' antes de usarlo en Plotly
    var data = [{
        x: [1, 2, 3, 4],
        y: [10, 15, 13, 17],
        mode: 'lines',
        type: 'scatter'
    }];

    var layout = {
        title: { text: 'Gráfica lineal' },
        showlegend: false,
    };

    Plotly.newPlot('lineal_chart', data, layout);
}
function volume(){
    const section = document.querySelector('#charts');
    section.replaceChildren(); 
    
    var volumeDiv = document.createElement('div');
    volumeDiv.id = "volume-chart";
    section.appendChild(volumeDiv);
    d3.csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv', function(err, rows){
function unpack(rows, key) {
  return rows.map(function(row) { return row[key]; });
}

var z_data=[ ]
for(i=0;i<24;i++)
{
  z_data.push(unpack(rows,i));
}

var data = [{
           z: z_data,
           type: 'surface'
        }];

var layout = {
  title: {
    text: 'Mt Bruno Elevation'
  },
  autosize: false,
  width: 500,
  height: 500,
  margin: {
    l: 65,
    r: 50,
    b: 65,
    t: 90,
  }
};
Plotly.newPlot('volume-chart', data, layout);
});


    // Nota: Aquí falta la lógica de Plotly para dibujar algo en 'volume-chart'
}

