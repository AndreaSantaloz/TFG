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

        

            function create_lineal_chart(data=null){
               var tracer1 ={
                  x:[1,2,3,4],
                  y:[10,15,13,17],
                  type:'scatter',
               };

               var tracer2={
                  x:[1,2,3,4],
                  y:[16,5,11,9],
                  type:'scatter',
               };

               var data=[tracer1,tracer2];
                var layout={
                title:{
                   text:'Gráfica lineal',
                },
                showlegend:false,
              };
               Plotly.newPlot('lineal_chart',data);

            }

            
            function create_boxplot_chart(data=null){
              var y0=[];
              var y1=[];
              for(var i =0;i < 50; i++){
                y0[i]=Math.random();
                y1[i]=Math.random()+1;

              }

              var trace1={
                y:y0,
                type:'box',
              };

              var trace2={
                y:y1,
                type:'box',
              };

              var data = [trace1,trace2];
              var layout={
                 title:{
                   text:'Gráfica de boxplot',
                },
                showlegend:false,
              }

              Plotly.newPlot('boxplot_chart',data,layout,{staticPlot:true});

            }
        create_scatter_chart();
        create_lineal_chart();
        create_boxplot_chart();