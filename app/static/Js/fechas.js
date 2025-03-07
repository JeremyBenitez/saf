const hoy = new Date();
    const anio = hoy.getFullYear();
    const mes = String(hoy.getMonth() + 1).padStart(2, '0');
    const dia = String(hoy.getDate()).padStart(2, '0');
    const fechaHoy = `${anio}-${mes}-${dia}`;
    
    // Asignar la fecha de hoy como el valor máximo
    document.getElementById("startDate").max = fechaHoy;
    document.getElementById("endDate").max = fechaHoy;
    // Función para formatear la fecha en formato DD-MM-YYYY
    function formatDate(date) {
      const [year, month, day] = date.split('-');
      return `${day}-${month}-${year}`;
    }

    // Función que actualiza el rango de fechas en el span
    function updateSelectedDates() {
      const startDate = document.getElementById('startDate').value;
      const endDate = document.getElementById('endDate').value;
      
      // Si ambas fechas están seleccionadas, las mostramos en el span
      if (startDate && endDate) {
        const selectedRange = document.getElementById('selectedRange');
        selectedRange.textContent = `${formatDate(startDate)} - ${formatDate(endDate)}`;
      }
    }

    // Aseguramos que el contenido del span se actualice cuando el usuario cambie las fechas
    document.getElementById('startDate').addEventListener('change', updateSelectedDates);
    document.getElementById('endDate').addEventListener('change', updateSelectedDates);

    // Si ya hay valores, actualizamos el span al cargar la página
    window.addEventListener('load', function() {
      updateSelectedDates();
    });


    function showLoadingModal() {
      const modal = document.getElementById("loadingModal");
      modal.classList.add("active");
    }
    
    // Función para ocultar el modal
    function hideLoadingModal() {
      const modal = document.getElementById("loadingModal");
      modal.classList.remove("active");

      
    }
    
    // Escucha el evento de envío de formularios
    document.addEventListener("submit", function (event) {
      const form = event.target;
      if (form.tagName === "FORM") {
        showLoadingModal(); // Mostrar el modal al enviar el formulario
      }
    });
    
    // Escucha el evento de carga completa de la página
    window.addEventListener("load", function () {
      
      hideLoadingModal(); // Ocultar el modal cuando se cargue la página
    });

  
    // URL del endpoint

  let storesChart; // Variable global para almacenar la instancia del gráfico

document.getElementById('consultarBtn').addEventListener('click', function() {
    const fechaIni = document.getElementById('startDate').value;
    const fechaFin = document.getElementById('endDate').value;

    if (!fechaIni || !fechaFin) {
        alert('Por favor, ingrese ambas fechas.');
        return;
    }

    // Lista de tiendas para consultar
    const tiendas = ['BABILON','BARALT','CABUDARE','CAGUA','CABIMAS','CATIA','CRUZ_VERDE','GUACARA',
    'GUANARE','KAPITANA','MATURIN','PROPATRIA','UPATA','VALENCIA','VALERA'] // Aquí agregas las tiendas que necesitas consultar

    // Resultados donde se almacenarán todas las respuestas
    let resultados = [];

    // Función para hacer la solicitud a la API
    const hacerSolicitud = (tienda) => {
        const url = `/fechas/usdxtiendas/${tienda}`;
        const requestData = { fecha_init: fechaIni, fecha_end: fechaFin };

      return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
      resultados.push({ tienda, data: data[0] }); // Guardar los datos de la tienda
      
      
      return data;
    })
    .catch(error => {
      console.error('Error:', error);
      resultados.push({ tienda, error: error.message });
    });
  };
  
  
    
  const showGrafico = document.getElementById("grafico");

  showGrafico.style.display = "block";
  showLoadingModal(); // Mostrar el modal al hacer clic

  // Hacer las peticiones para todas las tiendas
  Promise.all(tiendas.map(tienda => hacerSolicitud(tienda)))
    .then(() => {
      const validResults = resultados.filter(
        (item) => item.data && !item.error
      );

      if (validResults.length === 0) {
        console.error('No hay datos válidos para graficar');
        hideLoadingModal();
        return;
      }
      // Preparar los datos para el gráfico
      
      const combinedData = validResults.map((item) => ({
        label: item.tienda,
        totalUSD: item.data.total_usd || 0,
        total_transacciones:item.data.n_trasacciones || 0
      }));

      const sortedData = combinedData.sort((a, b) => b.totalUSD - a.totalUSD);


      const sortedLabels = sortedData.map((item) => item.label);
      const sortedTotalUSD = sortedData.map((item) => item.totalUSD)      
      const sortedTransaciones = sortedData.map((item) =>item.total_transacciones)

    const storesCanvas = document.getElementById("storesChart");
    const storesCtx = storesCanvas.getContext("2d");

    if (storesChart) {
        storesChart.destroy();
      }

    // Crear el gráfico
    storesChart = new Chart(storesCtx, {
      type: "bar",
      data: {
        labels: sortedLabels,
        datasets: [
        {
              label: 'Unidades Vendidas',
              backgroundColor: "rgba(99, 102, 241, 0.6)",
              data: sortedTransaciones,
              borderRadius: 4,
            },
       
          {
            label: "Ventas Totales $",
            borderColor: "#006400",
            backgroundColor: "#1E3A8A",
            data: sortedTotalUSD,
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

    hideLoadingModal(); // Ocultar el modal cuando se haya completado la solicitud
  })
  .catch(error => {
    console.error("Error en alguna de las peticiones", error);
    hideLoadingModal(); // Asegúrate de ocultar el modal en caso de error

});

});


document.getElementById('btn-formulario').addEventListener('click', (event) => {
    const fechaIni = document.getElementById('startDate').value;
    const fechaFin = document.getElementById('endDate').value;

    // Definir la fecha límite (por ejemplo, 2024-01-01)
    const fechaLimite = new Date('2025-01-01');
    const fechaInicioSeleccionada = new Date(fechaIni);

    if (fechaInicioSeleccionada < fechaLimite) {
      showLoadingModal()
      $.ajax({
            type: 'POST',
            url: '/fechas/consultassp',
            contentType: 'application/json',
            data: JSON.stringify({fecha_ini:fechaIni,
                                  fecha_fin:fechaFin,
                }),
                success: function(response) {
                  const formatted_usd = new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(response[0]['total_usd']);
                  const formatted_bs = new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(response[0]['total_bs']);
                  const formatted_csh = new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(response[0]['total_csh']);
                  const formatted_efe = new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(response[0]['total_efec']);

                  console.log(response);
                  document.getElementById('totalSalesUSD').innerText = `$ ${formatted_usd}`
                  document.getElementById('totalSalesBS').innerText = `Bs ${formatted_bs}`
                  document.getElementById('totalSalesCashea').innerText = `$ ${formatted_csh}`
                  document.getElementById('totalSalesCash').innerText = `$ ${formatted_efe}`
                  hideLoadingModal();
                  
                }
              })
        event.preventDefault(); // Evita el envío del formulario si está dentro de un <form>
        return;
    }

    // Si pasa la validación, puedes continuar con el envío del formulario
    console.log("Formulario enviado con éxito.");
});


document.getElementById("startDate").addEventListener("change", actualizarBotones);
document.getElementById("endDate").addEventListener("change", actualizarBotones);

function actualizarBotones() {
    const fechaInicio = new Date(document.getElementById("startDate").value);
    const fechaFin = new Date(document.getElementById("endDate").value);
    
    const boton1 = document.getElementById("consultarBtn");
    const boton2 = document.getElementById("consultarBtn2");

    // Verifica si alguna fecha es válida y si es menor a 2025
    if ((fechaInicio && fechaInicio.getFullYear() < 2025) || (fechaFin && fechaFin.getFullYear() < 2025)) {
        boton1.style.display = "none";
        boton2.style.display = "block";
    } else {
        boton1.style.display = "block";
        boton2.style.display = "none";
    }
}



document.getElementById('consultarBtn2').addEventListener('click', function() {
    const fechaIni = document.getElementById('startDate').value;
    const fechaFin = document.getElementById('endDate').value;

    if (!fechaIni || !fechaFin) {
        alert('Por favor, ingrese ambas fechas.');
        return;
    }

    // Lista de tiendas para consultar
    const tiendas = ['BABILON','BARALT','CABIMAS','CABUDARE','CAGUA','CATIA','CRUZVERDE','GUACARA',
    'GUANARE','KAPITANA','MATURIN','PROPATRIA','UPATA','VALENCIA','VALERA'] // Aquí agregas las tiendas que necesitas consultar

    // Resultados donde se almacenarán todas las respuestas
    let resultados = [];

    // Función para hacer la solicitud a la API
    const hacerSolicitud = (tienda) => {
        const url = `/fechas/usdxtiendas2024/${tienda}`;
        const requestData = { fecha_init: fechaIni, fecha_end: fechaFin };

      return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
      resultados.push({ tienda, data: data[0] }); // Guardar los datos de la tienda
      
      
      return data;
    })
    .catch(error => {
      console.error('Error:', error);
      resultados.push({ tienda, error: error.message });
    });
  };
  
  
    
  const showGrafico = document.getElementById("grafico");

  showGrafico.style.display = "block";
  showLoadingModal(); // Mostrar el modal al hacer clic

  // Hacer las peticiones para todas las tiendas
  Promise.all(tiendas.map(tienda => hacerSolicitud(tienda)))
    .then(() => {
      const validResults = resultados.filter(
        (item) => item.data && !item.error
      );

      if (validResults.length === 0) {
        console.error('No hay datos válidos para graficar');
        hideLoadingModal();
        return;
      }
      // Preparar los datos para el gráfico
      
      const combinedData = validResults.map((item) => ({
        label: item.tienda,
        totalUSD: item.data.total_usd || 0,
        total_transacciones:item.data.n_trasacciones || 0
      }));

      const sortedData = combinedData.sort((a, b) => b.totalUSD - a.totalUSD);


      const sortedLabels = sortedData.map((item) => item.label);
      const sortedTotalUSD = sortedData.map((item) => item.totalUSD)      
      const sortedTransaciones = sortedData.map((item) =>item.total_transacciones)

    const storesCanvas = document.getElementById("storesChart");
    const storesCtx = storesCanvas.getContext("2d");

    if (storesChart) {
        storesChart.destroy();
      }

    // Crear el gráfico
    storesChart = new Chart(storesCtx, {
      type: "bar",
      data: {
        labels: sortedLabels,
        datasets: [

       
          {
            label: "Ventas Totales $",
            borderColor: "#006400",
            backgroundColor: "#1E3A8A",
            data: sortedTotalUSD,
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

    hideLoadingModal(); // Ocultar el modal cuando se haya completado la solicitud
  })
  .catch(error => {
    console.error("Error en alguna de las peticiones", error);
    hideLoadingModal(); // Asegúrate de ocultar el modal en caso de error

});

});


//respaldo

//const hoy = new Date();
//     const anio = hoy.getFullYear();
//     const mes = String(hoy.getMonth() + 1).padStart(2, '0');
//     const dia = String(hoy.getDate()).padStart(2, '0');
//     const fechaHoy = `${anio}-${mes}-${dia}`;
    
//     // Asignar la fecha de hoy como el valor máximo
//     document.getElementById("startDate").max = fechaHoy;
//     document.getElementById("endDate").max = fechaHoy;

// function formatDate(date) {
//         const [year, month, day] = date.split('-');
//         return `${day}-${month}-${year}`;
//       }
  
//       // Función que actualiza el rango de fechas en el span
//       function updateSelectedDates() {
//         const startDate = document.getElementById('startDate').value;
//         const endDate = document.getElementById('endDate').value;
        
//         // Si ambas fechas están seleccionadas, las mostramos en el span
//         if (startDate && endDate) {
//           const selectedRange = document.getElementById('selectedRange');
//           selectedRange.textContent = `${formatDate(startDate)} - ${formatDate(endDate)}`;
//         }
//       }
  
//       // Aseguramos que el contenido del span se actualice cuando el usuario cambie las fechas
//       document.getElementById('startDate').addEventListener('change', updateSelectedDates);
//       document.getElementById('endDate').addEventListener('change', updateSelectedDates);
  
//       // Si ya hay valores, actualizamos el span al cargar la página
//       window.addEventListener('load', function() {
//         updateSelectedDates();
//       });



    
// const storesCtx = document.getElementById("storesChart").getContext("2d");

//       // Emparejar las ventas y las transacciones en un array de objetos
//   const combinedData = grafica_tiendas.map((value, index) => ({
//         label: [
//           "Kapitana", "Valencia", "Guacara", "Cagua", "Cruz Verde", "Cabimas", 
//           "Babilon", "Guanare", "Cabudare", "Valera", "Catia", "Propatria", 
//           "Baralt", "Maturin", "Upata"
//         ][index],
//         sales: value,
//         transactions: grafica_transiccion[index]
//       }));
  
//       // Ordenar el array combinado por las ventas de mayor a menor
//       const sortedCombinedData = combinedData.sort((a, b) => b.sales - a.sales);
  
//       // Extraer los datos ordenados
//       const sortedLabels = sortedCombinedData.map(item => item.label);
//       const sortedSales = sortedCombinedData.map(item => item.sales);
//       const sortedTrans = sortedCombinedData.map(item => item.transactions);
  
//       // Crear el gráfico
//       storesChart = new Chart(storesCtx, {
//         type: "bar",
//         data: {
//           labels: sortedLabels, // Etiquetas ordenadas por ventas
//           datasets: [
//             {
//               label: "Unidades Vendidas",
//               backgroundColor: "rgba(99, 102, 241, 0.6)", // Color de fondo de las barras
//               data: sortedTrans, // Datos de transacciones en el orden correcto
//               borderRadius: 4,
//               fill: true, // Llenar el área debajo de las barras
//             },
//             {
//               label: "Ventas Totales ($)",
//               borderColor: "#006400",
//               backgroundColor: "#1E3A8A",
//               data: sortedSales, // Datos de ventas totales en el orden correcto
//               borderRadius: 4,
//               fill: true, // Llenar el área debajo de las barras
//             },
//           ],
//         },
//         options: {
//           responsive: true,
//           maintainAspectRatio: false,
//           scales: {
//             x: {
//               stacked: true,
//               ticks: {
//                 maxRotation: 45,
//                 minRotation: 20,
//                 font: {
//                   size: function () {
//                     // Obtener el ancho de la pantalla
//                     const chartWidth = window.innerWidth; 
//                     return chartWidth > 450 ? 12 : 7; // Ajustar a 10px si es mayor a 360px, sino 7px
//                   },
//                 },
//               },
//             },
//             y: {
//               beginAtZero: true,
//               stacked: true, // Apilar las barras en el eje Y
//             },
//           },
//           plugins: {
//             tooltip: {
//               enabled: true,
//               callbacks: {
//                 label: function (tooltipItem) {
//                   return tooltipItem.dataset.label + ': ' + tooltipItem.raw.toLocaleString(); // Mostrar ventas en formato de moneda
//                 },
//               },
//             },
//             datalabels: {
//               anchor: "end", // Posicionar la etiqueta al final de la barra
//               align: "start", // Alineación a la parte superior de la barra
//               color: "white", // Color de las etiquetas
//               font: {
//                 size: function () {
//                   const chartWidth = window.innerWidth;
//                   return chartWidth > 450 ? 10 : 7; // Ajustar tamaño de datalabels dinámicamente
//                 },
//                 weight: "bold", // Fuente en negrita
//               },
//               formatter: function (value) {
//                 return value.toLocaleString(); // Formatear el valor de las ventas como número
//               },
//             },
//           },
//         },
//       });




// // Función para mostrar el modal
// /*function showLoadingModal() {
//   const modal = document.getElementById("loadingModal");
//   modal.classList.add("active");
// }

// // Función para ocultar el modal
// function hideLoadingModal() {
//   const modal = document.getElementById("loadingModal");
//   modal.classList.remove("active");
// }

// // Escucha el evento de envío de formularios
// document.addEventListener("submit", function (event) {
//   const form = event.target;
//   if (form.tagName === "FORM") {
//     showLoadingModal(); // Mostrar el modal al enviar el formulario
//   }
// });

// // Escucha el evento de carga completa de la página
// window.addEventListener("load", function () {
//   hideLoadingModal(); // Ocultar el modal cuando se cargue la página
// });*/



// // Función para mostrar el modal de carga
// // Función para mostrar el modal de carga
// // Función para mostrar el modal de carga
// function showLoadingModal() {
//   const modal = document.getElementById("loadingModal");
//   modal.classList.add("active");
// }

// // Función para ocultar el modal de carga
// function hideLoadingModal() {
//   const modal = document.getElementById("loadingModal");
//   modal.classList.remove("active");
// }

// // Escucha el evento de envío de formularios
// document.addEventListener("submit", function (event) {
//   const form = event.target;
//   if (form.tagName === "FORM") {
//     // Guardar en localStorage que el formulario fue enviado
//     localStorage.setItem("formSubmitted", "true");
//     showLoadingModal(); // Mostrar el modal de carga
//   }
// });

// // Escucha el evento de carga completa de la página
// window.addEventListener("load", function () {
//   hideLoadingModal(); // Ocultar el modal cuando la página haya cargado

//   // Verificar si el formulario fue enviado
//   if (localStorage.getItem("formSubmitted") === "true") {
//     const botonVerDetalles = document.getElementById("verDetalles");
//     botonVerDetalles.style.display = "inline-block"; // Mostrar el botón
//     localStorage.removeItem("formSubmitted"); // Limpiar el estado después de mostrar el botón
//   }
// });

// // Mostrar el contenedor del gráfico al pulsar el botón
// document.getElementById("verDetalles").addEventListener("click", function () {
//   const graficoContenedor = document.getElementById("grafico-contenedor");
//   const botonVerDetalles = this;

//   // Cambiar el estado del contenedor del gráfico
//   if (graficoContenedor.style.display === "none") {
//     graficoContenedor.style.display = "block"; // Mostrar el contenedor
//     botonVerDetalles.textContent = "Ocultar detalles"; // Cambiar el texto del botón
//   } else {
//     graficoContenedor.style.display = "none"; // Ocultar el contenedor
//     botonVerDetalles.textContent = "Ver detalles"; // Cambiar el texto del botón
//   }
// });

