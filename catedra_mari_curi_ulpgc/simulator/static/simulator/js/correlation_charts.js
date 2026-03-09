
             
            function create_heatmap_chart(data){

               var layout={
                title:{
                   text:'Gráfica heatmap',
                },
               
              };
               Plotly.newPlot('heatmap_chart',data,layout,{staticPlot:true});
            }
      

       var data = [
                {
                  z:[[1,20,30],[20,1,60],[30,60,1]],
                  type:'heatmap'
                }
                
              ];

      create_heatmap_chart(data);
    function create_scatter_chart(data=null){
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

    create_scatter_chart();