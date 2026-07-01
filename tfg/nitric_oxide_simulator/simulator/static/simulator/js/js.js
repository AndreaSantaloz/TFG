const layoutLineal = {
    xaxis:{title:'Time(t)'},
    xaxis:{title:'Time(t)'},
    hovermode:'closest'
}

function create_chart(name,data,layout){
    Plotly.newPlot(name,data,layout);
}


try {
        const data = document.getElementById('datos-django');
        
        if (!data || !data.textContent.trim()) return;
        
    

        const paquete = JSON.parse(data.textContent.trim());
        const t_axis = paquete.final_results.time;
        const c_plano = paquete.final_results.concentration;
        const rows = paquete.initial_data.rowN_ || 1;
        document.getElementById('rows').textContent = "Rows: "+rows;
        const cols = paquete.initial_data.columnN_ || 1;
        document.getElementById('cols').textContent ="Columns: "+cols;
        const depths = paquete.initial_data.depthN_ || 1;
        document.getElementById('depths').textContent ="Depth: "+ depths;

        if(paquete.initial_data.rowN_ > 1){
            document.getElementById("compartimentals").textContent=paquete.initial_data.rowN_;
        }else{
            document.getElementById("compartimentals").textContent=paquete.initial_data.N_ ;
        }
        
        document.getElementById("start_t").textContent= paquete.initial_data.start_t +" s";
        document.getElementById("end_t").textContent=paquete.initial_data.end_t +" s";
        document.getElementById("delta_t").textContent=paquete.initial_data.delta_t +" s" ;


      
        const timestap = t_axis.length;
        

        const title = document.getElementById('dynamic-title');
        
        const linealChartEl = document.getElementById('lineal_chart');
        if (linealChartEl) linealChartEl.style.display = 'none';

    if (depths > 1) {
            if (linealChartEl) linealChartEl.style.display = 'block';
            title.innerText = "Simulation: 3D model";

            if (document.getElementById('heatmap_chart')) document.getElementById('heatmap_chart').style.display = 'block';
            if (document.getElementById('scatter_chart')) document.getElementById('scatter_chart').style.display = 'block';
            if (document.getElementById('volume_chart')) document.getElementById('volume_chart').style.display = 'block';

        
        let serie_data = [];
        let frames = [];
        let concentrations_por_tiempo = [];

        
        for (let t = 0; t < timestap; t++) {
            let intensity = obtenerIntensidadesEnT(t);
            let data_en_t = [];
            for (let i = 0; i < intensity.length; i++) {
                    data_en_t.push(intensity[i]);
            }
            concentrations_por_tiempo.push(data_en_t);
        }
        for (let t = 0; t < timestap; t++) {
            let frame_data = [];
            for (let i = 0; i < concentrations_por_tiempo[0].length; i++) {
                let y_values = [];
                for (let k = 0; k <= t; k++) {
                    y_values.push(concentrations_por_tiempo[k][i]);
                }
                frame_data.push({
                y: y_values,
                name: `Serie ${i+1}`,
                type: 'scatter',
                mode: 'lines'
                });
            }
            frames.push({
            name: `frame_${t}`,
            data: frame_data
            });
        }
        let layout = {
            title: 'Temporal Evolution of the box of the NO',
            xaxis: { 
        title: 'Time (s)',
        range: [0, timestap - 1]
    },
    yaxis: { title: 'Concentration' },
    sliders: [{
        pad: { t: 30 },
        len: 0.9,
        x: 0.1,
        currentvalue: {
            visible: true,
            prefix: 'Time: ',
            font: { size: 16 }
        },
        steps: frames.map((frame, idx) => ({
            label: idx,
            method: 'animate',
            args: [[frame.name], {
                mode: 'immediate',
                frame: { duration: 0, redraw: true },
                transition: { duration: 0 }
            }]
        }))
    }]
};

Plotly.newPlot('lineal_chart', frames[0].data, layout);
Plotly.addFrames('lineal_chart', frames);

            let z_central = Math.floor(depths / 2);

            function obtenerPlano2D(t_idx, z_fijo) {
                let x_2d = [], y_2d = [], c_2d = [];
                for (let r = 0; r < rows; r++) {
                    for (let c = 0; c < cols; c++) {
                        let idx = ((r * cols + c) * depths + z_fijo) * timestap + t_idx;
                        x_2d.push(c);
                        y_2d.push(r);
                        c_2d.push(c_plano[idx] || 0);
                    }
                }
                return { x: x_2d, y: y_2d, c: c_2d };
            }

            function obtenerMatrizHeatmap(t_idx, z_fijo) {
                let matriz = [];
                for (let r = 0; r < rows; r++) {
                    let fila = [];
                    for (let c = 0; c < cols; c++) {
                        let idx = ((r * cols + c) * depths + z_fijo) * timestap + t_idx;
                        fila.push(c_plano[idx] || 0);
                    }
                    matriz.push(fila);
                }
                return matriz;
            }

            function obtenerIntensidadesEnT(t_idx) {
                let intensidades = [];
                let total_celdas = rows * cols * depths;
                for (let i = 0; i < total_celdas; i++) {
                    intensidades.push(c_plano[i * timestap + t_idx] || 0);
                }
                return intensidades;
            }

            let x_coords = [], y_coords = [], z_coords = [];
            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    for (let d = 0; d < depths; d++) {
                        x_coords.push(c);
                        y_coords.push(r);
                        z_coords.push(d);
                    }
                }
            }

            let datosPlanoInicial = obtenerPlano2D(0, z_central);

            Plotly.newPlot('scatter_chart', [{
                x: datosPlanoInicial.x,
                y: datosPlanoInicial.y,
                mode: 'markers',
                type: 'scatter',
                marker: { size: 12, color: datosPlanoInicial.c, colorscale: 'Jet', showscale: true }
            }], {
                title: `Corte 2D del Cubo (Scatter - Z: ${z_central})`,
                xaxis: { title: 'Eje X' },
                yaxis: { title: 'Eje Y' }
            }, { responsive: true });

            Plotly.newPlot('heatmap_chart', [{
                z: obtenerMatrizHeatmap(0, z_central),
                type: 'heatmap',
                colorscale: 'Jet',
                showscale: true
            }], {
                title: `Mapa de Calor de Concentración (Z: ${z_central})`,
                xaxis: { title: 'Columnas (X)' },
                yaxis: { title: 'Filas (Y)' },
                yaxis: { autorange: 'reverse' }
            }, { responsive: true });

            Plotly.newPlot('volume_chart', [{
                x: x_coords, y: y_coords, z: z_coords,
                type: 'scatter3d', mode: 'markers',
                marker: { size: 10, color: obtenerIntensidadesEnT(0), colorscale: 'Jet', showscale: true }
            }], {
                sliders: [{
                    pad: { t: 30 },
                    steps: []
                }],
                scene: { xaxis: { title: 'X' }, yaxis: { title: 'Y' }, zaxis: { title: 'Z' } }
            }, { responsive: true });

            const framesCubo = [];
            const framesScatter = [];
            const framesHeatmap = [];
            const sliderSteps = [];

            for (let t = 0; t < timestap; t++) {
                let label_t = t_axis[t].toFixed(2) + 's';
                let datosPlanoT = obtenerPlano2D(t, z_central);

                framesCubo.push({
                    name: label_t,
                    data: [{
                        x: x_coords, y: y_coords, z: z_coords,
                        type: 'scatter3d', mode: 'markers',
                        marker: { size: 8, color: obtenerIntensidadesEnT(t), colorscale: 'Jet' }
                    }]
                });

                framesScatter.push({
                    name: label_t,
                    data: [{
                        x: datosPlanoT.x, y: datosPlanoT.y,
                        type: 'scatter', mode: 'markers',
                        marker: { size: 12, color: datosPlanoT.c, colorscale: 'Jet' }
                    }]
                });

                framesHeatmap.push({
                    name: label_t,
                    data: [{ z: obtenerMatrizHeatmap(t, z_central), type: 'heatmap' }]
                });

                sliderSteps.push({
                    label: label_t,
                    method: 'animate',
                    args: [[label_t], { 
                        mode: 'immediate', 
                        transition: { duration: 0 }, 
                        frame: { duration: 50, redraw: true } 
                    }]
                });
            }

            Plotly.addFrames('volume_chart', framesCubo);
            Plotly.addFrames('scatter_chart', framesScatter);
            Plotly.addFrames('heatmap_chart', framesHeatmap);

            Plotly.relayout('volume_chart', {
                'sliders[0].steps': sliderSteps
            });

            let volEl = document.getElementById('volume_chart');
            volEl.on('plotly_sliderchange', function(e) {
                let pasoActual = e.step.label;
                Plotly.animate('scatter_chart', [pasoActual], { mode: 'immediate', frame: { duration: 0, redraw: true } });
                Plotly.animate('heatmap_chart', [pasoActual], { mode: 'immediate', frame: { duration: 0, redraw: true } });
            });
        } else if (cols > 1) {
            title.innerText =  "Simulation: 2D model";
            if (linealChartEl) linealChartEl.style.display = 'block';

            function getGrid2D(t_idx) {
                let grid = [];
                for (let r = 0; r < rows; r++) {
                    let fila = [];
                    for (let c = 0; c < cols; c++) {
                        let idx_plano = (r * cols + c) * timestap + t_idx;
                        fila.push(c_plano[idx_plano] || 0);
                    }
                    grid.push(fila);
                }
                return grid;
            }

            let frames2D = [];
            let steps2D = [];

            for (let t = 0; t < timestap; t++) {
                let lbl = t_axis[t].toFixed(2) + 's';
                frames2D.push({
                    name: lbl,
                    data: [{ z: getGrid2D(t), type: 'heatmap' }]
                });
                steps2D.push({
                    label: lbl, method: 'animate',
                    args: [[lbl], { mode: 'immediate', frame: { duration: 50, redraw: true } }]
                });
            }

            Plotly.newPlot('heatmap_chart', [{
                z: getGrid2D(0),
                type: 'heatmap',
                colorscale: 'Viridis'
            }], {
                sliders: [{ pad: { t: 30 }, steps: steps2D }],
                yaxis: { autorange: 'reverse' }
            }, { responsive: true }).then(function() {
                Plotly.addFrames('heatmap_chart', frames2D);
                
                let trazas2D = [];
                let trazasScatter2d = [];
                for (let r = 0; r < rows; r++) {
                    for (let c = 0; c < cols; c++) {
                        let inicio = (r * cols + c) * timestap;
                        let datos_celda = c_plano.slice(inicio, inicio + timestap);
                        trazas2D.push({
                            x: t_axis,
                            y: datos_celda,
                            mode: 'lines',
                            name: `Fila ${r + 1}, Col ${c + 1}`
                        });
                        trazasScatter2d.push({
                            x: t_axis,
                            y: datos_celda,
                            mode: 'markers',
                            name: `Fila ${r + 1}, Col ${c + 1}`
                        });
                    }
                }
                create_chart('lineal_chart',trazas2D,layoutLineal)
                create_chart('scatter_chart',trazasScatter2d,layoutLineal)
                
                 document.getElementById('volume_chart').style.display='none';
            });
        } else {
           
            title.innerText =  "Simulation: 1D model";
            if (linealChartEl) linealChartEl.style.display = 'block'; 
            const layoutLineal = {
                    xaxis: { title: 'Time (t)' },
                    yaxis: { title: 'Concentration (C)' },
                    hovermode: 'closest'
                };

            let trazas1D = [];
            let trazas1DS = [];
            for (let r = 0; r < rows; r++) {
                let inicio = r * timestap;
                trazas1D.push({
                    x: t_axis,
                    y: c_plano.slice(inicio, inicio + timestap),
                    mode: 'lines',
                    name: `Comp ${r+1}`
                });
                trazas1DS.push({
                    x: t_axis,
                    y: c_plano.slice(inicio, inicio + timestap),
                    mode: 'markers',
                    name: `Comp ${r+1}`
                });
                
            }
            create_chart('lineal_chart',trazas1D,layoutLineal)
            create_chart('scatter_chart',trazas1DS,layoutLineal)
           
          
          document.getElementById('heatmap_chart').style.display='none';
          document.getElementById('volume_chart').style.display='none';
        }

    } catch (e) {
        console.error("Error en el renderizador global:", e);
    }