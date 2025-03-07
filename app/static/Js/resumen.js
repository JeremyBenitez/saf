const canvas = document.getElementById("storesChart");
    const ctx = canvas.getContext("2d");

    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    // Calcular las coordenadas del centro del canvas
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    // Configurar estilo de texto
    ctx.font = "30px Arial";
    ctx.fillStyle = "gray";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    // Dibujar texto en el centro del canvas
    ctx.fillText("En espera por selección de tienda", centerX, centerY);

      const tiendaSelect = document.getElementById('tiendaSelect');

        let storesChart = null;
        tiendaSelect.addEventListener('change', () => {
          if (storesChart) {
              storesChart.destroy();
              storesChart = null;
          }

            const opctiones = tiendaSelect.value; // Obtener el valor actual del select
           
            if (opctiones == 'All'){
              const meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]; // Lista de meses
            let resultados = []; // Para almacenar todos los resultados

            // Función para hacer una solicitud al endpoint para un mes específico
            const hacerSolicitud = (mes) => {
                const url = `/2024/totales/${mes}`;
                
                return fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({}) // Puedes agregar datos adicionales si los necesitas
                })
                .then(response => response.json()) // Procesar la respuesta como JSON
                .then(data => {
                    // Extraer el valor de 'sum(V_USD)' y almacenarlo
                    const totalUSD = data[0]['sum(V_USD)'] || 0; // Manejar casos donde no haya datos
                    resultados.push(totalUSD); // Agregar el resultado al array
                    
                    return  totalUSD ; // Devolver los datos procesados
                })
                .catch(error => {
                    console.error(`Error en la solicitud para el mes ${mes}:`, error);
                    resultados.push({ mes, error: error.message });
                });
            };

            // Hacer solicitudes para todos los meses
            const procesarMeses = async () => {
                for (const mes of meses) {
                    await hacerSolicitud(mes); // Esperar cada solicitud
                }

                // Mostrar todos los resultados después de completar las solicitudes
                
                const sumaTotal_general = resultados.reduce((acumulador, valorActual) => acumulador + valorActual, 0);      
              
                const sumaTotalElement = document.getElementById("sumaTotal");
                sumaTotalElement.textContent = ` - Total: $${sumaTotal_general.toLocaleString()}`;
                const storesCtx = document.getElementById("storesChart").getContext("2d");
                                    if (storesChart) {
                                    storesChart.destroy();
                                    storesChart = null; // Asegúrate de reiniciar la variable
                                }
                                    storesChart = new Chart(storesCtx, {
                                    type: "bar",
                                    data: {
                                      labels: ["Enero",
                                              "Febrero",
                                              "Marzo",
                                              "Abril",
                                              "Mayo",
                                              "Junio",
                                              "Julio",
                                              "Agosto",
                                              "Septiembre",
                                              "Octubre",
                                              "Noviembre",
                                              "Diciembre"], // Etiquetas ordenadas por ventas
                                      datasets: [
                                        
                                        {
                                          label: "Ventas Totales ($)",
                                          borderColor: "#006400",
                                          backgroundColor: "#1E3A8A",
                                          data: resultados, // Datos de ventas totales en el orden correcto
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

            };

            procesarMeses(); // Ejecutar el procesamiento

            }
            if (opctiones ==  'tioi') {
              const mesestioi = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]; // Lista de meses
            let resultados = []; // Para almacenar todos los resultados

            // Función para hacer una solicitud al endpoint para un mes específico
            const hacerSolicitudTioI = (mes) => {
                const url = `/2024/tioi/${mes}`;
                
                return fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({}) // Puedes agregar datos adicionales si los necesitas
                })
                .then(response => response.json()) // Procesar la respuesta como JSON
                .then(data => {
                    // Extraer el valor de 'sum(V_USD)' y almacenarlo
                    const totalUSDTioi = data[0]['SUM(V_USD)'] || 0; // Manejar casos donde no haya datos
                    resultados.push(totalUSDTioi); // Agregar el resultado al array
                    
                    
                    return  totalUSDTioi ; // Devolver los datos procesados
                })
                .catch(error => {
                    console.error(`Error en la solicitud para el mes ${mes}:`, error);
                    resultados.push({ mes, error: error.message });
                });
            };

            // Hacer solicitudes para todos los meses
            const procesarMesesTioI = async () => {
                for (const mes of mesestioi) {
                    await hacerSolicitudTioI(mes); // Esperar cada solicitud
                    
                }
                
                // Mostrar todos los resultados después de completar las solicitudes
                
                const sumaTotal_general = resultados.reduce((acumulador, valorActual) => acumulador + valorActual, 0);      
              
                const sumaTotalElement = document.getElementById("sumaTotal");
                sumaTotalElement.textContent = ` - Total: $${sumaTotal_general.toLocaleString()}`;
                const storesCtx = document.getElementById("storesChart").getContext("2d");
                                    if (storesChart) {
                                    storesChart.destroy();
                                    storesChart = null; // Asegúrate de reiniciar la variable
                                }
                                    storesChart = new Chart(storesCtx, {
                                    type: "bar",
                                    data: {
                                      labels: ["Enero",
                                              "Febrero",
                                              "Marzo",
                                              "Abril",
                                              "Mayo",
                                              "Junio",
                                              "Julio",
                                              "Agosto",
                                              "Septiembre",
                                              "Octubre",
                                              "Noviembre",
                                              "Diciembre"], // Etiquetas ordenadas por ventas
                                      datasets: [
                                        
                                        {
                                          label: "Ventas Totales ($)",
                                          borderColor: "#006400",
                                          backgroundColor: "#1E3A8A",
                                          data: resultados, // Datos de ventas totales en el orden correcto
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

            };

            procesarMesesTioI(); // Ejecutar el procesamiento
            }
            
           
            if (opctiones ==  'tioii') {
              const mesestioii = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]; // Lista de meses
            let resultados = []; // Para almacenar todos los resultados

            // Función para hacer una solicitud al endpoint para un mes específico
            const hacerSolicitudTioII = (mes) => {
                const url = `/2024/tioii/${mes}`;
                
                return fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({}) // Puedes agregar datos adicionales si los necesitas
                })
                .then(response => response.json()) // Procesar la respuesta como JSON
                .then(data => {
                    // Extraer el valor de 'sum(V_USD)' y almacenarlo
                    const totalUSDTioii = data[0]['SUM(V_USD)'] || 0; // Manejar casos donde no haya datos
                    resultados.push(totalUSDTioii); // Agregar el resultado al array
                    
                    
                    return  totalUSDTioii ; // Devolver los datos procesados
                })
                .catch(error => {
                    console.error(`Error en la solicitud para el mes ${mes}:`, error);
                    resultados.push({ mes, error: error.message });
                });
            };

            // Hacer solicitudes para todos los meses
            const procesarMesesTioII = async () => {
                for (const mes of mesestioii) {
                    await hacerSolicitudTioII(mes); // Esperar cada solicitud
                    
                }
                
                // Mostrar todos los resultados después de completar las solicitudes
                
                const sumaTotal_general = resultados.reduce((acumulador, valorActual) => acumulador + valorActual, 0);      
              
                const sumaTotalElement = document.getElementById("sumaTotal");
                sumaTotalElement.textContent = ` - Total: $${sumaTotal_general.toLocaleString()}`;
                const storesCtx = document.getElementById("storesChart").getContext("2d");
                                    if (storesChart) {
                                    storesChart.destroy();
                                    storesChart = null; // Asegúrate de reiniciar la variable
                                }
                                    storesChart = new Chart(storesCtx, {
                                    type: "bar",
                                    data: {
                                      labels: ["Enero",
                                              "Febrero",
                                              "Marzo",
                                              "Abril",
                                              "Mayo",
                                              "Junio",
                                              "Julio",
                                              "Agosto",
                                              "Septiembre",
                                              "Octubre",
                                              "Noviembre",
                                              "Diciembre"], // Etiquetas ordenadas por ventas
                                      datasets: [
                                        
                                        {
                                          label: "Ventas Totales ($)",
                                          borderColor: "#006400",
                                          backgroundColor: "#1E3A8A",
                                          data: resultados, // Datos de ventas totales en el orden correcto
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

            };

            procesarMesesTioII(); // Ejecutar el procesamiento
            }
            if (opctiones ==  'tioiv'){
              const mesestioiv = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]; // Lista de meses
            let resultados = []; // Para almacenar todos los resultados

            // Función para hacer una solicitud al endpoint para un mes específico
            const hacerSolicitudTioIV = (mes) => {
                const url = `/2024/tioiv/${mes}`;
                
                return fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({}) // Puedes agregar datos adicionales si los necesitas
                })
                .then(response => response.json()) // Procesar la respuesta como JSON
                .then(data => {
                    // Extraer el valor de 'sum(V_USD)' y almacenarlo
                    const totalUSDTioiv = data[0]['SUM(V_USD)'] || 0; // Manejar casos donde no haya datos
                    resultados.push(totalUSDTioiv); // Agregar el resultado al array
                    
                    
                    return  totalUSDTioiv ; // Devolver los datos procesados
                })
                .catch(error => {
                    console.error(`Error en la solicitud para el mes ${mes}:`, error);
                    resultados.push({ mes, error: error.message });
                });
            };

            // Hacer solicitudes para todos los meses
            const procesarMesesTioIV = async () => {
                for (const mes of mesestioiv) {
                    await hacerSolicitudTioIV(mes); // Esperar cada solicitud
                    
                }
                
                // Mostrar todos los resultados después de completar las solicitudes
                
                const sumaTotal_general = resultados.reduce((acumulador, valorActual) => acumulador + valorActual, 0);      
              
                const sumaTotalElement = document.getElementById("sumaTotal");
                sumaTotalElement.textContent = ` - Total: $${sumaTotal_general.toLocaleString()}`;
                const storesCtx = document.getElementById("storesChart").getContext("2d");
                                    if (storesChart) {
                                    storesChart.destroy();
                                    storesChart = null; // Asegúrate de reiniciar la variable
                                }
                                    storesChart = new Chart(storesCtx, {
                                    type: "bar",
                                    data: {
                                      labels: ["Enero",
                                              "Febrero",
                                              "Marzo",
                                              "Abril",
                                              "Mayo",
                                              "Junio",
                                              "Julio",
                                              "Agosto",
                                              "Septiembre",
                                              "Octubre",
                                              "Noviembre",
                                              "Diciembre"], // Etiquetas ordenadas por ventas
                                      datasets: [
                                        
                                        {
                                          label: "Ventas Totales ($)",
                                          borderColor: "#006400",
                                          backgroundColor: "#1E3A8A",
                                          data: resultados, // Datos de ventas totales en el orden correcto
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

            };

            procesarMesesTioIV(); // Ejecutar el procesamiento
            }
            
    
                    $.ajax({
                            type: 'POST',
                            url: '/2024/tiendas',
                            contentType: 'application/json',
                            data: JSON.stringify({tienda:opctiones}),
                                success: function(response) {

                      
                                    const valoresUSD = response.map(item => item.V_USD);
                                    const sumaTotal = valoresUSD.reduce((acumulador, valorActual) => acumulador + valorActual, 0);

                                    const sumaTotalElement = document.getElementById("sumaTotal");
                                    sumaTotalElement.textContent = ` - Total: $${sumaTotal.toLocaleString()}`;



                                    const storesCtx = document.getElementById("storesChart").getContext("2d");
                                    if (storesChart) {
                                    storesChart.destroy();
                                    storesChart = null; // Asegúrate de reiniciar la variable
                                }
                                    storesChart = new Chart(storesCtx, {
                                    type: "bar",
                                    data: {
                                      labels: ["Enero",
                                              "Febrero",
                                              "Marzo",
                                              "Abril",
                                              "Mayo",
                                              "Junio",
                                              "Julio",
                                              "Agosto",
                                              "Septiembre",
                                              "Octubre",
                                              "Noviembre",
                                              "Diciembre"], // Etiquetas ordenadas por ventas
                                      datasets: [
                                        
                                        {
                                          label: "Ventas Totales ($)",
                                          borderColor: "#006400",
                                          backgroundColor: "#1E3A8A",
                                          data: valoresUSD, // Datos de ventas totales en el orden correcto
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
                                    console.error('Error al insertar el código:', error);
                                    
                                }
                            });
                          });

// Emparejar las ventas y las transacciones en un array de objetos


// Ordenar el array combinado por las ventas de mayor a menor


// Crear el gráfico

        