let storesChart;
function showLoadingModal() {
    const modal = document.getElementById("loadingModal");
    modal.classList.add("active");
    }
    
    // Función para ocultar el modal
    function hideLoadingModal() {
    const modal = document.getElementById("loadingModal");
    modal.classList.remove("active");
    
    
    }

function toggleLists() {
    const showDepartments = document.getElementById('showDepartments').checked;
    const showBrands = document.getElementById('showBrands').checked;

    const departmentsList = document.getElementById('departmentsList');
    const brandsList = document.getElementById('brandsList');
    const btn_brand = document.getElementById('btn-buscar-brand');
    const btn_deptos = document.getElementById('btn-buscar');

    // Mostrar u ocultar las listas según los checkboxes
    // SECCION DE DEPARTMENTOS
    if (showDepartments) {
        if (storesChart) {
            storesChart.destroy();
        }

        departmentsList.classList.remove('hidden');
        brandsList.classList.add('hidden');
        btn_deptos.classList.remove('hidden');
        document.getElementById('showBrands').checked = false;
       
        const btn = document.getElementById('btn-buscar').addEventListener('click', () =>{
            const fecha_inicio = document.getElementById('startDate').value
            const fecha_fin = document.getElementById('endDate').value
            const dpto = document.getElementById('departamento').value
           
            showLoadingModal();
            $.ajax({
            
                    type: 'POST',
                    url: '/marcas/ventasdepartamentos',
                    contentType: 'application/json',
                    data: JSON.stringify({FechaInicio:fecha_inicio,
                                          FechaFin:fecha_fin,
                                          c_departamento:dpto
                        }),
                        success: function(response) {
            
                         
                            let usds = []
                            let bs = []
                            let cantidad = []
                            let label = ['BABILON','BARALT','CABIMAS','CABUDARE','CAGUA','CATIA','CRUZ_VERDE','GUACARA',
                                'GUANARE','KAPITANA','MATURIN','PROPATRIA','UPATA','VALENCIA','VALERA']
                            response.forEach(item =>{
                                usds.push(item['TOTALUSD'])
                                bs.push(item['Total'])
                                cantidad.push(item['Cantidad'])
                              
                                
                            })

                            
                            
                            const sumaUSD = usds.map(Number).reduce((acumulador, valorActual) => acumulador + valorActual, 0);                        
                            const formatted_usd = new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(sumaUSD);

                            const sumaBS = bs.map(Number).reduce((acumulador, valorActual) => acumulador + valorActual, 0);
                            const formatted_bs = new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(sumaBS);

                            const cantidad_transa = cantidad.map(Number).reduce((acumulador, valorActual) => acumulador + valorActual, 0);
                            const formatted_transa = new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(cantidad_transa);



                            document.getElementById('totalSalesUSD').innerText = `$ ${formatted_usd}`

                            
                            document.getElementById('totalSalesBS').innerText = `Bs ${formatted_bs}`

                            document.getElementById('transacciones').innerText = formatted_transa

                            hideLoadingModal();

                            
                            const btn_detalles = document.getElementById('btn-detalles').addEventListener('click', () =>{
                            const combined = usds.map((venta, index) => ({
                                    venta,
                                    label: label[index]
                                }));
                            combined.sort((a, b) => b.venta - a.venta);
                            usds = combined.map(item => item.venta);
                            label = combined.map(item => item.label);

                            const storesCanvas = document.getElementById("storesChart");
                            const storesCtx = storesCanvas.getContext("2d");

                       

                            // Crear el gráfico
                            storesChart = new Chart(storesCtx, {
                            type: "bar",
                            data: {
                                labels: label,
                                datasets: [

                                {
                                    label: "Ventas Totales $",
                                    borderColor: "#006400",
                                    backgroundColor: "#1E3A8A",
                                    data: usds,
                                    borderRadius: 4,
                                    fill: true,
                                },
                                ],
                            },
                            options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                scales: {
                                    x: {
                                    stacked: true,
                                    ticks: {
                                        maxRotation: 45,
                                        minRotation: 20,
                                        font: {
                                        size: function () {
                                            // Obtener el ancho de la pantalla
                                            const chartWidth = window.innerWidth; 
                                            return chartWidth > 450 ? 12 : 7; // Ajustar a 10px si es mayor a 360px, sino 7px
                                        },
                                        },
                                    },
                                    },
                                    y: {
                                    beginAtZero: true,
                                    stacked: true, // Apilar las barras en el eje Y
                                    },
                                },
                                plugins: {
                                    tooltip: {
                                    enabled: true,
                                    callbacks: {
                                        label: function (tooltipItem) {
                                        return tooltipItem.dataset.label + ': ' + tooltipItem.raw.toLocaleString(); // Mostrar ventas en formato de moneda
                                        },
                                    },
                                    },
                                },
                            },
                            });

                        })
                         
                        },
                        error: function(error) {
                            console.error('Error:', error);
                            hideLoadingModal();
                        }
                    });
            })
                
            
    // SECCION DE MARCAS 
    } else if (showBrands) {
        if (storesChart) {
            storesChart.destroy();
        }

        brandsList.classList.remove('hidden');
        departmentsList.classList.add('hidden');
        btn_brand.classList.remove('hidden')
        document.getElementById('showDepartments').checked = false;
        const btn = document.getElementById('btn-buscar-brand').addEventListener('click', () =>{
            const fecha_inicio = document.getElementById('startDate').value
            const fecha_fin = document.getElementById('endDate').value
            const marca = document.getElementById('marca').value
            showLoadingModal();
            $.ajax({
            
                    type: 'POST',
                    url: '/marcas/apigeneral',
                    contentType: 'application/json',
                    data: JSON.stringify({FechaInicio:fecha_inicio,
                                          FechaFin:fecha_fin,
                                          marca:marca
                        }),
                        success: function(response) {
            
                          
                            console.log(response)
                            // Mostrar en consola la descripción de cada item recibido
                            const usd_marca =response.MarcaUSD[0].Total_Ventas_USD
                            const bs_marca = response.MarcaBs[0].Total_Ventas
                            const trasaciones = response.MarcaUSD[0].Total_Transacciones
                            
                            const formatted_bs = new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(bs_marca);
                            const formatted_usd = new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(usd_marca);
                            
                            document.getElementById('totalSalesUSD').innerText = `$ ${formatted_usd}`
                            document.getElementById('totalSalesBS').innerText = `Bs ${formatted_bs}`
                            document.getElementById('transacciones').innerText = trasaciones
                            hideLoadingModal();
                        },
                        error: function(error) {
                            console.error('Error:', error);
                            hideLoadingModal();
                        }
                    });
            })
            
            

            const btn_detalles = document.getElementById('btn-detalles').addEventListener('click', () =>{
            
                const fecha_inicio = document.getElementById('startDate').value
                const fecha_fin = document.getElementById('endDate').value
                const marca = document.getElementById('marca').value
                showLoadingModal();
                $.ajax({
                    
                        type: 'POST',
                        url: '/marcas/tiendas',
                        contentType: 'application/json',
                        data: JSON.stringify({FechaInicio:fecha_inicio,
                                            FechaFin:fecha_fin,
                                            marca:marca
                            }),
                            success: function(response) {
                                
                                let ventasUsd  = []
                                let label = []
                                response.forEach(item => {
                            
                                console.log(`${item.Total_Ventas_USD}`, `${item.tienda}`);
                                ventasUsd.push(item.Total_Ventas_USD)
                                label.push(item.tienda)
                                
                            });
                            const combined = ventasUsd.map((venta, index) => ({
                                venta,
                                label: label[index]
                            }));
                            combined.sort((a, b) => b.venta - a.venta);
                            ventasUsd = combined.map(item => item.venta);
                            label = combined.map(item => item.label);
            
                                
                            hideLoadingModal();
                                const storesCanvas = document.getElementById("storesChart");
                                const storesCtx = storesCanvas.getContext("2d");
            
                                if (storesChart) {
                                storesChart.destroy();
                            }
            
                                // Crear el gráfico
                                storesChart = new Chart(storesCtx, {
                                type: "bar",
                                data: {
                                    labels: label,
                                    datasets: [
                                
                                
                                    {
                                        label: "Ventas Totales $",
                                        borderColor: "#006400",
                                        backgroundColor: "#1E3A8A",
                                        data: ventasUsd,
                                        borderRadius: 4,
                                        fill: true,
                                    },
                                    ],
                                },
                                options: {
                                    responsive: true,
                                    maintainAspectRatio: false,
                                    scales: {
                                        x: {
                                        stacked: true,
                                        ticks: {
                                            maxRotation: 45,
                                            minRotation: 20,
                                            font: {
                                            size: function () {
                                                // Obtener el ancho de la pantalla
                                                const chartWidth = window.innerWidth; 
                                                return chartWidth > 450 ? 12 : 7; // Ajustar a 10px si es mayor a 360px, sino 7px
                                            },
                                            },
                                        },
                                        },
                                        y: {
                                        beginAtZero: true,
                                        stacked: true, // Apilar las barras en el eje Y
                                        },
                                    },
                                    plugins: {
                                        tooltip: {
                                        enabled: true,
                                        callbacks: {
                                            label: function (tooltipItem) {
                                            return tooltipItem.dataset.label + ': ' + tooltipItem.raw.toLocaleString(); // Mostrar ventas en formato de moneda
                                            },
                                        },
                                        },
                                    },
                                },
                                });
                            },
                            
                            error: function(error) {
                                console.error('Error:', error);
                                hideLoadingModal();
                            }
                        });
            
            })
        
    } else {
        btn_brand.classList.add('hidden')
        departmentsList.classList.add('hidden');
        brandsList.classList.add('hidden');
        btn_deptos.classList.add('hidden');
    }
}














//////////////// SECCION DEPARTAMENTO //////////////




