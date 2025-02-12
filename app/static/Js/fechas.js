const hoy = new Date();
    const anio = hoy.getFullYear();
    const mes = String(hoy.getMonth() + 1).padStart(2, '0');
    const dia = String(hoy.getDate()).padStart(2, '0');
    const fechaHoy = `${anio}-${mes}-${dia}`;
    
    // Asignar la fecha de hoy como el valor máximo
    document.getElementById("startDate").max = fechaHoy;
    document.getElementById("endDate").max = fechaHoy;

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



    
const storesCtx = document.getElementById("storesChart").getContext("2d");

      // Emparejar las ventas y las transacciones en un array de objetos
  const combinedData = grafica_tiendas.map((value, index) => ({
        label: [
          "Kapitana", "Valencia", "Guacara", "Cagua", "Cruz Verde", "Cabimas", 
          "Babilon", "Guanare", "Cabudare", "Valera", "Catia", "Propatria", 
          "Baralt", "Maturin", "Upata"
        ][index],
        sales: value,
        transactions: grafica_transiccion[index]
      }));
  
      // Ordenar el array combinado por las ventas de mayor a menor
      const sortedCombinedData = combinedData.sort((a, b) => b.sales - a.sales);
  
      // Extraer los datos ordenados
      const sortedLabels = sortedCombinedData.map(item => item.label);
      const sortedSales = sortedCombinedData.map(item => item.sales);
      const sortedTrans = sortedCombinedData.map(item => item.transactions);
  
      // Crear el gráfico
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




// Función para mostrar el modal
/*function showLoadingModal() {
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
});*/



// Función para mostrar el modal de carga
// Función para mostrar el modal de carga
// Función para mostrar el modal de carga
function showLoadingModal() {
  const modal = document.getElementById("loadingModal");
  modal.classList.add("active");
}

// Función para ocultar el modal de carga
function hideLoadingModal() {
  const modal = document.getElementById("loadingModal");
  modal.classList.remove("active");
}

// Escucha el evento de envío de formularios
document.addEventListener("submit", function (event) {
  const form = event.target;
  if (form.tagName === "FORM") {
    // Guardar en localStorage que el formulario fue enviado
    localStorage.setItem("formSubmitted", "true");
    showLoadingModal(); // Mostrar el modal de carga
  }
});

// Escucha el evento de carga completa de la página
window.addEventListener("load", function () {
  hideLoadingModal(); // Ocultar el modal cuando la página haya cargado

  // Verificar si el formulario fue enviado
  if (localStorage.getItem("formSubmitted") === "true") {
    const botonVerDetalles = document.getElementById("verDetalles");
    botonVerDetalles.style.display = "inline-block"; // Mostrar el botón
    localStorage.removeItem("formSubmitted"); // Limpiar el estado después de mostrar el botón
  }
});

// Mostrar el contenedor del gráfico al pulsar el botón
document.getElementById("verDetalles").addEventListener("click", function () {
  const graficoContenedor = document.getElementById("grafico-contenedor");
  const botonVerDetalles = this;

  // Cambiar el estado del contenedor del gráfico
  if (graficoContenedor.style.display === "none") {
    graficoContenedor.style.display = "block"; // Mostrar el contenedor
    botonVerDetalles.textContent = "Ocultar detalles"; // Cambiar el texto del botón
  } else {
    graficoContenedor.style.display = "none"; // Ocultar el contenedor
    botonVerDetalles.textContent = "Ver detalles"; // Cambiar el texto del botón
  }
});





// Escuchar el evento de envío del formulario


