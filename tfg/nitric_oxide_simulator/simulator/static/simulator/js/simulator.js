document.addEventListener("DOMContentLoaded", function() {
    try {
        const el = document.getElementById("datos-django");
        if (!el || !el.textContent.trim()) return;

        const paquete = JSON.parse(el.textContent.trim());
        const t_axis = paquete.final_results.time || [];
        const concentration = paquete.final_results.concentration || [];
        const initialData = paquete.initial_data || {};
        const dataShape = getArrayShape(concentration);
        const rows = Number(initialData.rowN_ || initialData.N_ || dataShape[0] || 1);
        const cols = Number(initialData.columnN_ || (dataShape.length >= 3 ? dataShape[1] : 1) || 1);
        const depths = Number(initialData.depthN_ || (dataShape.length >= 4 ? dataShape[2] : 1) || 1);
        const pasos_t = t_axis.length;

        const title = document.getElementById("dynamic-title");
        const linealChartEl = document.getElementById("lineal_chart");
        const scatterChartEl = document.getElementById("scatter_chart");
        const heatmapChartEl = document.getElementById("heatmap_chart");
        const volumeChartEl = document.getElementById("volume_chart");

        if (document.getElementById("rows")) document.getElementById("rows").textContent = rows;
        if (document.getElementById("cols")) document.getElementById("cols").textContent = cols;
        if (document.getElementById("depths")) document.getElementById("depths").textContent = depths;
        if (document.getElementById("compartimentals")) document.getElementById("compartimentals").textContent = rows * cols * depths;
        if (document.getElementById("start_t")) document.getElementById("start_t").textContent = `${initialData.start_t ?? ""} s`;
        if (document.getElementById("end_t")) document.getElementById("end_t").textContent = `${initialData.end_t ?? ""} s`;
        if (document.getElementById("delta_t")) document.getElementById("delta_t").textContent = `${initialData.delta_t ?? ""} s`;

        if (title) title.innerText = "Simulation";

        setDisplay(linealChartEl, false);
        setDisplay(scatterChartEl, true);
        setDisplay(heatmapChartEl, true);
        setDisplay(volumeChartEl, true);

        function setDisplay(element, visible) {
            if (element) element.style.display = visible ? "block" : "none";
        }

        function getArrayShape(value) {
            const shape = [];
            let current = value;
            while (Array.isArray(current)) {
                shape.push(current.length);
                current = current[0];
            }
            return shape;
        }

        function numericValue(value) {
            const numberValue = Number(value);
            return Number.isFinite(numberValue) ? numberValue : 0;
        }

        function flatIndex(r, c, d, t) {
            return (((r * cols + c) * depths + d) * pasos_t) + t;
        }

        function getConcentration(r, c, d, t) {
            if (Array.isArray(concentration?.[r]?.[c]?.[d])) {
                return numericValue(concentration[r][c][d][t]);
            }

            if (depths === 1 && Array.isArray(concentration?.[r]?.[c])) {
                return numericValue(concentration[r][c][t]);
            }

            if (cols === 1 && depths === 1 && Array.isArray(concentration?.[r])) {
                return numericValue(concentration[r][t]);
            }

            return numericValue(concentration[flatIndex(r, c, d, t)]);
        }

        function getSeries(r, c = 0, d = 0) {
            const values = [];
            for (let t = 0; t < pasos_t; t++) {
                values.push(getConcentration(r, c, d, t));
            }
            return values;
        }

        function getGlobalRange() {
            let min = Infinity;
            let max = -Infinity;

            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    for (let d = 0; d < depths; d++) {
                        for (let t = 0; t < pasos_t; t++) {
                            const value = getConcentration(r, c, d, t);
                            min = Math.min(min, value);
                            max = Math.max(max, value);
                        }
                    }
                }
            }

            if (!Number.isFinite(min) || !Number.isFinite(max)) return { min: 0, max: 1 };
            if (min === max) return { min: min - 1, max: max + 1 };
            return { min, max };
        }

        function labelTime(t) {
            const value = Number(t_axis[t]);
            return Number.isFinite(value) ? `${value.toFixed(2)}s` : `${t}`;
        }

        function animationOptions(duration = 0) {
            return {
                mode: "immediate",
                transition: { duration: 0 },
                frame: { duration, redraw: true }
            };
        }

        const colorRange = getGlobalRange();
        const colorScale = "Jet";
        const plotConfig = { responsive: true };

        if (depths > 1) {
            setDisplay(linealChartEl, true);

            function obtenerIntensidadesEnT(t_idx) {
                const intensidades = [];
                for (let r = 0; r < rows; r++) {
                    for (let c = 0; c < cols; c++) {
                        for (let d = 0; d < depths; d++) {
                            intensidades.push(getConcentration(r, c, d, t_idx));
                        }
                    }
                }
                return intensidades;
            }

            function obtenerPlano2D(t_idx, z_fijo) {
                const x_2d = [];
                const y_2d = [];
                const c_2d = [];

                for (let r = 0; r < rows; r++) {
                    for (let c = 0; c < cols; c++) {
                        x_2d.push(c);
                        y_2d.push(r);
                        c_2d.push(getConcentration(r, c, z_fijo, t_idx));
                    }
                }

                return { x: x_2d, y: y_2d, c: c_2d };
            }

            function obtenerMatrizHeatmap(t_idx, z_fijo) {
                const matriz = [];
                for (let r = 0; r < rows; r++) {
                    const fila = [];
                    for (let c = 0; c < cols; c++) {
                        fila.push(getConcentration(r, c, z_fijo, t_idx));
                    }
                    matriz.push(fila);
                }
                return matriz;
            }

            const trazas3D = [];
            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    for (let d = 0; d < depths; d++) {
                        trazas3D.push({
                            x: t_axis,
                            y: getSeries(r, c, d),
                            type: "scatter",
                            mode: "lines",
                            name: `Fila ${r + 1}, Col ${c + 1}, Prof ${d + 1}`
                        });
                    }
                }
            }

            Plotly.newPlot("lineal_chart", trazas3D, {
                title: "Evolucion temporal de C de los compartimentos",
                xaxis: { title: "Tiempo (s)" },
                yaxis: { title: "Concentracion (C)" },
                hovermode: "closest"
            }, plotConfig);

            const z_central = Math.floor(depths / 2);
            const datosPlanoInicial = obtenerPlano2D(0, z_central);
            const x_coords = [];
            const y_coords = [];
            const z_coords = [];

            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    for (let d = 0; d < depths; d++) {
                        x_coords.push(c);
                        y_coords.push(r);
                        z_coords.push(d);
                    }
                }
            }

            const scatterLayout = {
                title: `Corte 2D del cubo (puntos - Z: ${z_central})`,
                xaxis: { title: "Eje X" },
                yaxis: { title: "Eje Y", autorange: "reversed" }
            };

            const heatmapLayout = {
                title: `Mapa de calor de concentracion (Z: ${z_central})`,
                xaxis: { title: "Columnas (X)" },
                yaxis: { title: "Filas (Y)", autorange: "reversed" }
            };

            const volumeLayout = {
                title: "Cubo 3D de concentracion",
                sliders: [{ active: 0, currentvalue: { prefix: "Tiempo: " }, pad: { t: 30 }, steps: [] }],
                updatemenus: [{
                    type: "buttons",
                    showactive: false,
                    x: 0,
                    y: 1.12,
                    buttons: [{
                        label: "Play",
                        method: "animate",
                        args: [null, animationOptions(80)]
                    }, {
                        label: "Pause",
                        method: "animate",
                        args: [[null], animationOptions(0)]
                    }]
                }],
                scene: {
                    xaxis: { title: "X" },
                    yaxis: { title: "Y" },
                    zaxis: { title: "Z" }
                }
            };

            const framesCubo = [];
            const framesScatter = [];
            const framesHeatmap = [];
            const sliderSteps = [];

            for (let t = 0; t < pasos_t; t++) {
                const label_t = labelTime(t);
                const datosPlanoT = obtenerPlano2D(t, z_central);

                framesCubo.push({
                    name: label_t,
                    data: [{
                        x: x_coords,
                        y: y_coords,
                        z: z_coords,
                        type: "scatter3d",
                        mode: "markers",
                        marker: {
                            size: 8,
                            color: obtenerIntensidadesEnT(t),
                            colorscale: colorScale,
                            cmin: colorRange.min,
                            cmax: colorRange.max,
                            showscale: true
                        }
                    }]
                });

                framesScatter.push({
                    name: label_t,
                    data: [{
                        x: datosPlanoT.x,
                        y: datosPlanoT.y,
                        type: "scatter",
                        mode: "markers",
                        marker: {
                            size: 12,
                            color: datosPlanoT.c,
                            colorscale: colorScale,
                            cmin: colorRange.min,
                            cmax: colorRange.max,
                            showscale: true
                        }
                    }]
                });

                framesHeatmap.push({
                    name: label_t,
                    data: [{
                        z: obtenerMatrizHeatmap(t, z_central),
                        type: "heatmap",
                        colorscale: colorScale,
                        zmin: colorRange.min,
                        zmax: colorRange.max,
                        showscale: true
                    }]
                });

                sliderSteps.push({
                    label: label_t,
                    method: "animate",
                    args: [[label_t], animationOptions(50)]
                });
            }

            volumeLayout.sliders[0].steps = sliderSteps;

            Promise.all([
                Plotly.newPlot("scatter_chart", [{
                    x: datosPlanoInicial.x,
                    y: datosPlanoInicial.y,
                    mode: "markers",
                    type: "scatter",
                    marker: {
                        size: 12,
                        color: datosPlanoInicial.c,
                        colorscale: colorScale,
                        cmin: colorRange.min,
                        cmax: colorRange.max,
                        showscale: true
                    }
                }], scatterLayout, plotConfig),
                Plotly.newPlot("heatmap_chart", [{
                    z: obtenerMatrizHeatmap(0, z_central),
                    type: "heatmap",
                    colorscale: colorScale,
                    zmin: colorRange.min,
                    zmax: colorRange.max,
                    showscale: true
                }], heatmapLayout, plotConfig),
                Plotly.newPlot("volume_chart", [{
                    x: x_coords,
                    y: y_coords,
                    z: z_coords,
                    type: "scatter3d",
                    mode: "markers",
                    marker: {
                        size: 8,
                        color: obtenerIntensidadesEnT(0),
                        colorscale: colorScale,
                        cmin: colorRange.min,
                        cmax: colorRange.max,
                        showscale: true
                    }
                }], volumeLayout, plotConfig)
            ]).then(function() {
                Plotly.addFrames("volume_chart", framesCubo);
                Plotly.addFrames("scatter_chart", framesScatter);
                Plotly.addFrames("heatmap_chart", framesHeatmap);

                volumeChartEl.on("plotly_sliderchange", function(e) {
                    const pasoActual = e.step.label;
                    Plotly.animate("scatter_chart", [pasoActual], animationOptions(0));
                    Plotly.animate("heatmap_chart", [pasoActual], animationOptions(0));
                });

                volumeChartEl.on("plotly_animated", function(e) {
                    const frameName = e?.frame?.name;
                    if (!frameName) return;
                    Plotly.animate("scatter_chart", [frameName], animationOptions(0));
                    Plotly.animate("heatmap_chart", [frameName], animationOptions(0));
                });
            });
        } else if (cols > 1) {
            setDisplay(linealChartEl, true);
            setDisplay(volumeChartEl, false);

            function getGrid2D(t_idx) {
                const grid = [];
                for (let r = 0; r < rows; r++) {
                    const fila = [];
                    for (let c = 0; c < cols; c++) {
                        fila.push(getConcentration(r, c, 0, t_idx));
                    }
                    grid.push(fila);
                }
                return grid;
            }

            const frames2D = [];
            const steps2D = [];

            for (let t = 0; t < pasos_t; t++) {
                const lbl = labelTime(t);
                frames2D.push({
                    name: lbl,
                    data: [{
                        z: getGrid2D(t),
                        type: "heatmap",
                        colorscale: "Viridis",
                        zmin: colorRange.min,
                        zmax: colorRange.max
                    }]
                });
                steps2D.push({
                    label: lbl,
                    method: "animate",
                    args: [[lbl], animationOptions(50)]
                });
            }

            Plotly.newPlot("heatmap_chart", [{
                z: getGrid2D(0),
                type: "heatmap",
                colorscale: "Viridis",
                zmin: colorRange.min,
                zmax: colorRange.max
            }], {
                title: "Mapa de calor de concentracion",
                sliders: [{ active: 0, currentvalue: { prefix: "Tiempo: " }, pad: { t: 30 }, steps: steps2D }],
                yaxis: { autorange: "reversed" }
            }, plotConfig).then(function() {
                Plotly.addFrames("heatmap_chart", frames2D);
            });

            const trazas2D = [];
            const trazasScatter2d = [];

            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    const datosCelda = getSeries(r, c, 0);
                    const name = `Fila ${r + 1}, Col ${c + 1}`;

                    trazas2D.push({ x: t_axis, y: datosCelda, mode: "lines", name });
                    trazasScatter2d.push({ x: t_axis, y: datosCelda, mode: "markers", name });
                }
            }

            const layoutLineal = {
                xaxis: { title: "Tiempo (t)" },
                yaxis: { title: "Concentracion (C)" },
                hovermode: "closest"
            };

            Plotly.newPlot("lineal_chart", trazas2D, layoutLineal, plotConfig);
            Plotly.newPlot("scatter_chart", trazasScatter2d, layoutLineal, plotConfig);
        } else {
            setDisplay(linealChartEl, true);
            setDisplay(heatmapChartEl, false);
            setDisplay(volumeChartEl, false);

            const trazas1D = [];
            const trazas1DS = [];

            for (let r = 0; r < rows; r++) {
                const datosCelda = getSeries(r, 0, 0);
                const name = `Comp ${r + 1}`;
                trazas1D.push({ x: t_axis, y: datosCelda, mode: "lines", name });
                trazas1DS.push({ x: t_axis, y: datosCelda, mode: "markers", name });
            }

            const layoutLineal = {
                xaxis: { title: "Tiempo (t)" },
                yaxis: { title: "Concentracion (C)" },
                hovermode: "closest"
            };

            Plotly.newPlot("lineal_chart", trazas1D, layoutLineal, plotConfig);
            Plotly.newPlot("scatter_chart", trazas1DS, layoutLineal, plotConfig);
        }
    } catch (e) {
        console.error("Error en el renderizador global:", e);
    }
});
