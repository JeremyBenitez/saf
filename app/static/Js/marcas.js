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
                    url: '/marcas/consulta_general',
                    contentType: 'application/json',
                    data: JSON.stringify({FechaInicio:fecha_inicio,
                                          FechaFin:fecha_fin,
                                          filtro:dpto
                        }),
                        success: function(response) {
                          console.log(response);
                                
                          const formatted_bs = new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(response.bsTienda.total_bs);
                          const formatted_usd = new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(response.usd.total_usd);
                          const formatted_transa = new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(response.usd.total_cantidad);



                          document.getElementById('totalSalesUSD').innerText = `$ ${formatted_usd}`
                          document.getElementById('transacciones').innerText = formatted_transa
                          document.getElementById('totalSalesBS').innerText = `Bs ${formatted_bs}`

                          hideLoadingModal();
                          
                          labels = Object.keys(response.usd.valores_tiendas)
                          console.log(labels);
                          const btn_detalles = document.getElementById('btn-detalles').addEventListener('click', () =>{
                            if (storesChart) {
                              storesChart.destroy();
                          }
                          const storesCanvas = document.getElementById("storesChart");
                          const storesCtx = storesCanvas.getContext("2d");
                          const combinedData = Object.keys(response.usd.valores_tiendas).map((tienda) => ({
                            label: tienda,
                            sales: response.usd.valores_tiendas[tienda].total_USD,
                            transactions: response.usd.valores_tiendas[tienda].cantidad
                          }));
                              

                            const sortedCombinedData = combinedData.sort((a, b) => b.sales - a.sales);
  
                            // Extraer los datos ordenados
                            const sortedLabels = sortedCombinedData.map(item => item.label);
                            const sortedSales = sortedCombinedData.map(item => item.sales);
                            const sortedTrans = sortedCombinedData.map(item => item.transactions);

                            storesChart = new Chart(storesCtx, {
                                type: "bar",
                                data: {
                                  labels: sortedLabels, // Etiquetas ordenadas por ventas
                                  datasets: [
                                    {
                                      label: "Unidades Vendidas",
                                      backgroundColor: "rgba(99, 102, 241, 0.6)", // Color de fondo de las barras
                                      data: sortedTrans, // Datos de transacciones en el orden correcto
                                      borderRadius: 4,
                                      fill: true, // Llenar el área debajo de las barras
                                    },
                                    {
                                      label: "Ventas Totales ($)",
                                      borderColor: "#006400",
                                      backgroundColor: "#1E3A8A",
                                      data: sortedSales, // Datos de ventas totales en el orden correcto
                                      borderRadius: 4,
                                      fill: true, // Llenar el área debajo de las barras
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
                                    datalabels: {
                                      anchor: "end", // Posicionar la etiqueta al final de la barra
                                      align: "start", // Alineación a la parte superior de la barra
                                      color: "white", // Color de las etiquetas
                                      font: {
                                        size: function () {
                                          const chartWidth = window.innerWidth;
                                          return chartWidth > 450 ? 10 : 7; // Ajustar tamaño de datalabels dinámicamente
                                        },
                                        weight: "bold", // Fuente en negrita
                                      },
                                      formatter: function (value) {
                                        return value.toLocaleString(); // Formatear el valor de las ventas como número
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
                    url: '/marcas/marcasdetalles',
                    contentType: 'application/json',
                    data: JSON.stringify({FechaInicio:fecha_inicio,
                                          FechaFin:fecha_fin,
                                          marca:marca
                        }),
                        success: function(response) {
            
                          
                            console.log(response)
                            // Mostrar en consola la descripción de cada item recibido
                            const usd_marca =response.Total_USD
                            const trasaciones = response.cantidades
                            
                            const formatted_usd = new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(usd_marca);
                            const formatted_transa = new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(trasaciones);
                            
                            document.getElementById('totalSalesUSD').innerText = `$ ${formatted_usd}`
                            document.getElementById('transacciones').innerText = formatted_transa
                            
                        },
                        error: function(error) {
                            console.error('Error:', error);
                            hideLoadingModal();
                        }
                    });
                    $.ajax({
            
                        type: 'POST',
                        url: '/marcas/marcasdetallesbs',
                        contentType: 'application/json',
                        data: JSON.stringify({FechaInicio:fecha_inicio,
                                              FechaFin:fecha_fin,
                                              marca:marca
                            }),
                            success: function(response) {
                
                              
                                console.log(response)
                                // Mostrar en consola la descripción de cada item recibido
                                const bs_marca =response.Total_BS
                                
                                const formatted_bs = new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(bs_marca);
                                
                                document.getElementById('totalSalesBS').innerText = `$ ${formatted_bs}`
                                hideLoadingModal();

                            },
                            error: function(error) {
                                console.error('Error:', error);
                                hideLoadingModal();
                            }
                        });


            })
            
            
            
            

            const btn_detalles = document.getElementById('btn-detalles').addEventListener('click', () =>{
                if (storesChart) {
                    storesChart.destroy();
                }
                const fecha_inicio = document.getElementById('startDate').value
                const fecha_fin = document.getElementById('endDate').value
                const marca = document.getElementById('marca').value
                showLoadingModal();
                $.ajax({
                    
                        type: 'POST',
                        url: '/marcas/marcasdetallesxtiendas',
                        contentType: 'application/json',
                        data: JSON.stringify({FechaInicio:fecha_inicio,
                                            FechaFin:fecha_fin,
                                            marca:marca
                            }),
                            success: function(response) {
                                
                                let ventasUsd  = []
                                let label = []
                            const tiendas = Object.keys(response)
                            console.log(tiendas);

                            const cantidades = [];
                            const totalesUSD = [];
                            
                            // Iterar sobre las tiendas para llenar los arrays
                            for (const tienda in response) {
                              if (response.hasOwnProperty(tienda)) {
                                cantidades.push(response[tienda].cantidad);
                                totalesUSD.push(response[tienda].total_USD);
                              }
                            }
                            console.log("Cantidades:", cantidades);
                            console.log("Totales en USD:", totalesUSD);
                                

                            hideLoadingModal();

                            const storesCanvas = document.getElementById("storesChart");
                            const storesCtx = storesCanvas.getContext("2d");

                            const combinedData = Object.keys(response).map((tienda) => ({
                                label: tienda,
                                sales: response[tienda].total_USD,
                                transactions: response[tienda].cantidad
                              }));
                              

                            const sortedCombinedData = combinedData.sort((a, b) => b.sales - a.sales);
  
                            // Extraer los datos ordenados
                            const sortedLabels = sortedCombinedData.map(item => item.label);
                            const sortedSales = sortedCombinedData.map(item => item.sales);
                            const sortedTrans = sortedCombinedData.map(item => item.transactions);

                            storesChart = new Chart(storesCtx, {
                                type: "bar",
                                data: {
                                  labels: sortedLabels, // Etiquetas ordenadas por ventas
                                  datasets: [
                                    {
                                      label: "Unidades Vendidas",
                                      backgroundColor: "rgba(99, 102, 241, 0.6)", // Color de fondo de las barras
                                      data: sortedTrans, // Datos de transacciones en el orden correcto
                                      borderRadius: 4,
                                      fill: true, // Llenar el área debajo de las barras
                                    },
                                    {
                                      label: "Ventas Totales ($)",
                                      borderColor: "#006400",
                                      backgroundColor: "#1E3A8A",
                                      data: sortedSales, // Datos de ventas totales en el orden correcto
                                      borderRadius: 4,
                                      fill: true, // Llenar el área debajo de las barras
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
                                    datalabels: {
                                      anchor: "end", // Posicionar la etiqueta al final de la barra
                                      align: "start", // Alineación a la parte superior de la barra
                                      color: "white", // Color de las etiquetas
                                      font: {
                                        size: function () {
                                          const chartWidth = window.innerWidth;
                                          return chartWidth > 450 ? 10 : 7; // Ajustar tamaño de datalabels dinámicamente
                                        },
                                        weight: "bold", // Fuente en negrita
                                      },
                                      formatter: function (value) {
                                        return value.toLocaleString(); // Formatear el valor de las ventas como número
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




