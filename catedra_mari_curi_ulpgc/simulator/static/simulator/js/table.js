


            function create_table(data=null){
              var values=[
                ['sí','no'],
                ['no','sí'],
                
              ];

              var data=[{
                type:'table',
                header:{
                  values:[["<b>Fumar</b>"],["<b>No Fumar</b>"]],
                  align:'center',
                  line:{width:1,color:'black'},
                  fill:{color:'grey'},
                  font:{familiy:'Arial',size:12,color:'white'}
                },
                cells:{
                  values:values,
                  align:'center',
                  line:{width:1,color:'black'},
                  fill:{color:'white'},
                  font:{familiy:'Arial',size:11,color:'black'}
                },
              }]

              Plotly.newPlot(table,data)

            }

        create_table();