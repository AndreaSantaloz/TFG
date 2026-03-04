
             
            function create_heatmap_chart(data=null){
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
                showlegend:false,
              };
               Plotly.newPlot('heatmap_chart',data,layout,{staticPlot:true});
            }


      create_heatmap_chart();
