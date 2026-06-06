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
       
        if (depths > 1) {
            title.innerText = "Simulation: 3D Space Bubbles";
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

            function obtenerIntensidadesEnT(t_idx) {
                let intensidades = [];
                let total_celdas = rows * cols * depths;
                for (let i = 0; i < total_celdas; i++) {
                    intensidades.push(c_plano[i * pasos_t + t_idx] || 0);
                }
                return intensidades;
            }

            const frames = [];
            const sliderSteps = [];

            for (let t = 0; t < pasos_t; t++) {
                let label_t = t_axis[t].toFixed(2) + 's';

                frames.push({
                    name: label_t,
                    data: [{
                        x: x_coords,
                        y: y_coords,
                        z: z_coords,
                        type: 'scatter3d',
                        mode: 'markers',
                        marker: {
                            size: 8,
                            color: obtenerIntensidadesEnT(t),
                            colorscale: 'Jet',
                            showscale: true
                        }
                    }]
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

            Plotly.newPlot('nitricOxidePlotGlobal', [{
                x: x_coords,
                y: y_coords,
                z: z_coords,
                type: 'scatter3d',
                mode: 'markers',
                marker: {
                    size: 10,
                    color: obtenerIntensidadesEnT(0),
                    colorscale: 'Jet',
                    showscale: true
                }
            }], {
                sliders: [{ pad: { t: 30 }, steps: sliderSteps }],
                scene: { xaxis: { title: 'X' }, yaxis: { title: 'Y' }, zaxis: { title: 'Z' } }
            }, { responsive: true }).then(function() {
                Plotly.addFrames('nitricOxidePlotGlobal', frames);
            });

        // ------------------------------------------
        // CASO 2D
        // ------------------------------------------
        } else if (cols > 1) {
            title.innerText = "Simulation: 2D Heatmap Grid";

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
                    label: lbl,
                    method: 'animate',
                    args: [[lbl], {
                        mode: 'immediate',
                        frame: { duration: 50, redraw: true }
                    }]
                });
            }

            Plotly.newPlot('nitricOxidePlotGlobal', [{
                z: getGrid2D(0),
                type: 'heatmap',
                colorscale: 'Viridis'
            }], {
                sliders: [{ pad: { t: 30 }, steps: steps2D }],
                yaxis: { autorange: 'reverse' }
            }, { responsive: true }).then(function() {
                Plotly.addFrames('nitricOxidePlotGlobal', frames2D);
            });
        } else {
            title.innerText = "Simulation: 1D Linear History";
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

            Plotly.newPlot('nitricOxidePlotGlobal', trazas1D, {
                xaxis: { title: 'Tiempo (t)' },
                yaxis: { title: 'Concentración (C)' }
            }, { responsive: true });
        }

    } catch (e) {
        console.error("Error en el renderizador global:", e);
    }
});
