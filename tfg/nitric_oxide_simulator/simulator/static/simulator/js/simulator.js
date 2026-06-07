document.addEventListener("DOMContentLoaded", function() {
    try {
        const el = document.getElementById('datos-django');
        if (!el || !el.textContent.trim()) return;

        const paquete = JSON.parse(el.textContent.trim());
        const t_axis = paquete.resultados_finales.eje_tiempo;
        const c_plano = paquete.resultados_finales.valores_c_plano;

        const rows = paquete.datos_inicio.rowN_ || 1;
        const cols = paquete.datos_inicio.columnN_ || 1;
        const depths = paquete.datos_inicio.depthN_ || 1;
        const pasos_t = t_axis.length;

        const title = document.getElementById('dynamic-title');
        
        // Contenedor secundario para la gráfica lineal (aseguramos que esté limpio)
        const linealChartEl = document.getElementById('lineal_chart');
        if (linealChartEl) linealChartEl.style.display = 'none'; // Por defecto oculto

        // ==========================================
        // CASO 3D
        // ==========================================
    if (depths > 1) {
            if (linealChartEl) linealChartEl.style.display = 'block';
            title.innerText = "Simulation: 3D Space Bubbles & 2D Slices";

            // Asegurar que todos los contenedores HTML estén visibles
            if (document.getElementById('heatmap_chart')) document.getElementById('heatmap_chart').style.display = 'block';
            if (document.getElementById('scatter_chart')) document.getElementById('scatter_chart').style.display = 'block';
            if (document.getElementById('volume_chart')) document.getElementById('volume_chart').style.display = 'block';

            // --- 1. PROCESAR HISTÓRICO LINEAL (Promedio global del cubo) ---
            let concentraciones_promedio = [];
            for (let t = 0; t < pasos_t; t++) {
                let intensidades = obtenerIntensidadesEnT(t);
                let suma = intensidades.reduce((a, b) => a + b, 0);
                concentraciones_promedio.push(suma / intensidades.length);
            }

            Plotly.newPlot('lineal_chart', [{
                x: t_axis,
                y: concentraciones_promedio,
                type: 'scatter',
                mode: 'lines',
                line: { color: 'rgb(219, 64, 82)', width: 3 }
            }], {
                title: 'Evolución Temporal de la Concentración Promedio',
                xaxis: { title: 'Tiempo (s)' },
                yaxis: { title: 'Concentración Promedio' }
            }, { responsive: true });


            // --- 2. FUNCIONES DE EXTRACCIÓN DE DATOS PARA CORTES 2D ---
            let z_central = Math.floor(depths / 2);

            function obtenerPlano2D(t_idx, z_fijo) {
                let x_2d = [], y_2d = [], c_2d = [];
                for (let r = 0; r < rows; r++) {
                    for (let c = 0; c < cols; c++) {
                        // Mapeo correcto del índice plano 3D compuesto: ((r * cols + c) * depths + z_fijo) * pasos_t + t_idx
                        let idx = ((r * cols + c) * depths + z_fijo) * pasos_t + t_idx;
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
                        let idx = ((r * cols + c) * depths + z_fijo) * pasos_t + t_idx;
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
                    intensidades.push(c_plano[i * pasos_t + t_idx] || 0);
                }
                return intensidades;
            }


            // --- 3. COORDENADAS PARA EL CUBO 3D ---
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


            // --- 4. RENDERIZADO DE GRÁFICOS INICIALES (Tiempo t = 0) ---
            let datosPlanoInicial = obtenerPlano2D(0, z_central);

            // Scatter 2D inicial
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

            // Heatmap inicial (Corrección del bug de nombre de función)
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

            // Cubo 3D inicial
            Plotly.newPlot('volume_chart', [{
                x: x_coords, y: y_coords, z: z_coords,
                type: 'scatter3d', mode: 'markers',
                marker: { size: 10, color: obtenerIntensidadesEnT(0), colorscale: 'Jet', showscale: true }
            }], {
                sliders: [{
                    pad: { t: 30 },
                    steps: [] // Se llenará dinámicamente abajo
                }],
                scene: { xaxis: { title: 'X' }, yaxis: { title: 'Y' }, zaxis: { title: 'Z' } }
            }, { responsive: true });


            // --- 5. CREACIÓN DE ANIMACIONES SINCRONIZADAS ---
            const framesCubo = [];
            const framesScatter = [];
            const framesHeatmap = [];
            const sliderSteps = [];

            for (let t = 0; t < pasos_t; t++) {
                let label_t = t_axis[t].toFixed(2) + 's';
                let datosPlanoT = obtenerPlano2D(t, z_central);

                // Frame Cubo 3D
                framesCubo.push({
                    name: label_t,
                    data: [{
                        x: x_coords, y: y_coords, z: z_coords,
                        type: 'scatter3d', mode: 'markers',
                        marker: { size: 8, color: obtenerIntensidadesEnT(t), colorscale: 'Jet' }
                    }]
                });

                // Frame Scatter 2D
                framesScatter.push({
                    name: label_t,
                    data: [{
                        x: datosPlanoT.x, y: datosPlanoT.y,
                        type: 'scatter', mode: 'markers',
                        marker: { size: 12, color: datosPlanoT.c, colorscale: 'Jet' }
                    }]
                });

                // Frame Heatmap
                framesHeatmap.push({
                    name: label_t,
                    data: [{ z: obtenerMatrizHeatmap(t, z_central), type: 'heatmap' }]
                });

                // Control único de Slider asignado al método de animación global
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

            // Inyectar frames a cada gráfica de forma independiente e implementar la sincronización por eventos
            Plotly.addFrames('volume_chart', framesCubo);
            Plotly.addFrames('scatter_chart', framesScatter);
            Plotly.addFrames('heatmap_chart', framesHeatmap);

            // Actualizar el layout del volumen añadiendo los pasos del slider ya calculados
            Plotly.relayout('volume_chart', {
                'sliders[0].steps': sliderSteps
            });

            // ESCUCHADOR DE SLIDER: Sincroniza los cambios de cuadro del Cubo 3D hacia las vistas 2D
            let volEl = document.getElementById('volume_chart');
            volEl.on('plotly_sliderchange', function(e) {
                let pasoActual = e.step.label;
                Plotly.animate('scatter_chart', [pasoActual], { mode: 'immediate', frame: { duration: 0, redraw: true } });
                Plotly.animate('heatmap_chart', [pasoActual], { mode: 'immediate', frame: { duration: 0, redraw: true } });
            });
        } else if (cols > 1) {
            title.innerText = "Simulation: 2D Heatmap & Linear History";
            if (linealChartEl) linealChartEl.style.display = 'block'; // Mostramos el contenedor lineal

            // --- 1. CONFIGURACIÓN DEL MAPA DE CALOR (HEATMAP) ---
            function getGrid2D(t_idx) {
                let grid = [];
                for (let r = 0; r < rows; r++) {
                    let fila = [];
                    for (let c = 0; c < cols; c++) {
                        let idx_plano = (r * cols + c) * pasos_t + t_idx;
                        fila.push(c_plano[idx_plano] || 0);
                    }
                    grid.push(fila);
                }
                return grid;
            }

            let frames2D = [];
            let steps2D = [];

            for (let t = 0; t < pasos_t; t++) {
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

            // Dibuja el Heatmap y espera a que termine de procesar sus fotogramas
            Plotly.newPlot('heatmap_chart', [{
                z: getGrid2D(0),
                type: 'heatmap',
                colorscale: 'Viridis'
            }], {
                sliders: [{ pad: { t: 30 }, steps: steps2D }],
                yaxis: { autorange: 'reverse' }
            }, { responsive: true }).then(function() {
                Plotly.addFrames('heatmap_chart', frames2D);
                
                // --- 2. CONFIGURACIÓN DE LA GRÁFICA LINEAL (Dentro del .then seguro) ---
                let trazas2D = [];
                for (let r = 0; r < rows; r++) {
                    for (let c = 0; c < cols; c++) {
                        let inicio = (r * cols + c) * pasos_t;
                        let datos_celda = c_plano.slice(inicio, inicio + pasos_t);

                        trazas2D.push({
                            x: t_axis,
                            y: datos_celda,
                            mode: 'lines',
                            name: `Fila ${r + 1}, Col ${c + 1}`
                        });
                    }
                }

                const layoutLineal = {
                    xaxis: { title: 'Tiempo (t)' },
                    yaxis: { title: 'Concentración (C)' },
                    hovermode: 'closest'
                };

                let trazasScatter2d = [];
                for (let r = 0; r < rows; r++) {
                    for (let c = 0; c < cols; c++) {
                        let inicio = (r * cols + c) * pasos_t;
                        let datos_celda = c_plano.slice(inicio, inicio + pasos_t);

                        trazasScatter2d.push({
                            x: t_axis,
                            y: datos_celda,
                            mode: 'markers',
                            name: `Fila ${r + 1}, Col ${c + 1}`
                        });
                    }
                Plotly.newPlot('lineal_chart', trazas2D, layoutLineal);
                Plotly.newPlot('scatter_chart', trazasScatter2d);
                }
                 document.getElementById('volume_chart').style.display='none';
            });

        // ==========================================
        // CASO 1D
        // ==========================================
        } else {
            title.innerText = "Simulation: 1D Linear History";
             if (linealChartEl) linealChartEl.style.display = 'block'; 
            let trazas1D = [];
            for (let r = 0; r < rows; r++) {
                let inicio = r * pasos_t;
                trazas1D.push({
                    x: t_axis,
                    y: c_plano.slice(inicio, inicio + pasos_t),
                    mode: 'lines',
                    name: `Comp ${r+1}`
                });
            }

            let trazas1DS = [];
            for (let r = 0; r < rows; r++) {
                let inicio = r * pasos_t;
                trazas1DS.push({
                    x: t_axis,
                    y: c_plano.slice(inicio, inicio + pasos_t),
                    mode: 'markers',
                    name: `Comp ${r+1}`
                });
            }
             const layoutLineal = {
                    xaxis: { title: 'Tiempo (t)' },
                    yaxis: { title: 'Concentración (C)' },
                    hovermode: 'closest'
                };

          Plotly.newPlot('lineal_chart', trazas1D, layoutLineal);
          Plotly.newPlot('scatter_chart', trazas1DS);
          document.getElementById('heatmap_chart').style.display='none';
          document.getElementById('volume_chart').style.display='none';
        }

    } catch (e) {
        console.error("Error en el renderizador global:", e);
    }
});