
             
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
