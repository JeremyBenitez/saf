const formatNumber = (num) => {
  return new Intl.NumberFormat("es-VE", {
    minimumFractionDigits: 2,
    maximationFractionDigits: 2,
  }).format(num);
};
//---------------------------------------------------------------------------------------------------------------------------------------------------------------
// Inicialización de gráficos
let monthlyChart, storesChart, categoryChart, storesMonthlyChart; 

// Función para actualizar los datos del dashboard
const updateDashboard = (data,total_bs,cashea_total,efectivo_total) => {
  // Actualizar métricas principales
  //document.getElementById("dollarBCV").textContent = formatNumber(tasa_dia);
  document.getElementById("totalSalesUSD").textContent =
    "$ " + formatNumber(data);
  document.getElementById("totalSalesBS").textContent =
    "Bs " + formatNumber(total_bs);
 document.getElementById("totalSalesCashea").textContent =
   "$ " + formatNumber(cashea_total);
 document.getElementById("totalSalesCash").textContent =
   "$ " + formatNumber(efectivo_total);
  // Actualizar gráfico de tiendas
  storesChart.data.labels = data.storesSales.map((item) => item.name);
  storesChart.data.datasets[0].data = data.storesSales.map(
    (item) => item.sales
  );
  storesChart.data.datasets[0].backgroundColor = data.storesSales.map(
    (item) => item.color
  );
  storesChart.update();
  
};

// Inicialización de gráficos al cargar la página
// Inicialización de gráficos al cargar la página
document.addEventListener("DOMContentLoaded", () => {
  // Configuración del gráfico mensual (estático)
  const monthlyCtx = document.getElementById("monthlyChart").getContext("2d");
  monthlyChart = new Chart(monthlyCtx, {
    type: "line",
    data: {
      labels: [
        "Ene",
        "Feb",
        "Mar",
        "Abr",
        "May",
        "Jun",
        "Jul",
        "Ago",
        "Sep",
        "Oct",
        "Nov",
        "Dic",
      ],
      datasets: [
        {
          label: "Ventas Totales ($)",
          borderColor: "#6366F1",
          backgroundColor: "rgba(99, 102, 241, 0.1)",
          data: grafico_mensuales,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales:{
        x:{
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
      },
      plugins: {
        legend: {
          position: "top",
        },
      },
    },
  });
//---------------------------------------------------------------------------------------------------------------------------------------------------------------

      // Configuración del gráfico de tiendas y transacciones
      const storesCtx = document.getElementById("storesChart").getContext("2d");

      // Emparejar las ventas y las transacciones en un array de objetos
      const combinedData = grafico_tiendas.map((value, index) => ({
        label: [
          'BABILON','BARALT','CABUDARE','CAGUA','CABIMAS','CATIA','CRUZ VERDE','GUACARA',
              'GUANARE','KAPITANA','MATURIN','PROPATRIA','UPATA','VALENCIA','VALERA'
        ][index],
        sales: value,
        transactions: grafico_trans[index]
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
              label: "Ventas Totales $",
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
  
  
  //---------------------------------------------------------------------------------------------------------------------------------------------------------------
  // Actualizar con datos iniciales
  updateDashboard(total_ventas,total_bs,cashea_total,efectivo_total);
  //---------------------------------------------------------------------------------------------------------------------------------------------------------------
  // Actualización periódica cada 5 segundos
  setInterval(() => {
    fetch("/api/data")
      .then((response) => response.json())
      .then((data) => updateDashboard(data));
  }, 1000);
});

// GRAFICO QUE FUNCIONA sin nombres ¡NOO BORRAR!
/*
    // Configuración del gráfico de tiendas y transacciones
    const storesCtx = document.getElementById("storesChart").getContext("2d");

    // Emparejar las ventas y las transacciones en un array de objetos
    const combinedData = grafico_tiendas.map((value, index) => ({
      label: [
        "Kapitana", "Valencia", "Guacara", "Cagua", "Cruz Verde", "Cabimas", 
        "Babilon", "Guanare", "Cabudare", "Valera", "Catia", "Propatria", 
        "Baralt", "Maturin", "Upata"
      ][index],
      sales: value,
      transactions: grafico_trans[index]
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
        labels: sortedLabels,
        datasets: [
          {
            label: "Unidades Vendidas",
            backgroundColor: "rgba(99, 102, 241, 0.6)",  // Color de fondo de las barras
            data: sortedTrans,  // Datos de transacciones
            borderRadius: 4,
            fill: true,  // Llenar el área debajo de las barras
            barThickness: 28,  // Grosor de las barras
          },
          {
            label: "Ventas Totales ($)",
            borderColor: "#006400",
            backgroundColor: "#1E3A8A",
            data: sortedSales,  // Datos de ventas totales
            borderRadius: 4,
            fill: true,  // Llenar el área debajo de las barras
            barThickness: 28,  // Grosor de las barras
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            stacked: true,  // Apilar las barras en el eje X
            ticks: {
              display: false,  // No mostrar etiquetas en el eje X
            },
          },
          y: {
            beginAtZero: true,
            stacked: true,  // Apilar las barras en el eje Y
          },
        },
        plugins: {
          tooltip: {
            enabled: true,
            callbacks: {
              label: function (tooltipItem) {
                return tooltipItem.dataset.label + ': ' + tooltipItem.raw.toLocaleString();  // Mostrar ventas en formato de moneda
              },
            },
          },
          // Mostrar solo los nombres de las tiendas dentro de las barras
          datalabels: {
            anchor: 'center',  // Anclaje del texto en el centro de la barra
            align: 'center',   // Alineación del texto en el centro
            color: 'black',    // Color del texto
            font: {
              weight: 'bold',  // Fuente en negrita
              size: 12,        // Tamaño de la fuente
            },
            formatter: function (value, context) {
              // Mostrar solo el nombre de la tienda (sin los valores)
              return sortedLabels[context.dataIndex];  // Mostrar solo el nombre de la tienda
            },
          },
        },
      },
    });

*/

/** GRAFICO QUE SI FUNCIONA CON NOMBRES ¡NO BORRAR!
  // Configuración del gráfico de tiendas y transacciones
      const storesCtx = document.getElementById("storesChart").getContext("2d");

      // Emparejar las ventas y las transacciones en un array de objetos
      const combinedData = grafico_tiendas.map((value, index) => ({
        label: [
          "Kapitana", "Valencia", "Guacara", "Cagua", "Cruz Verde", "Cabimas", 
          "Babilon", "Guanare", "Cabudare", "Valera", "Catia", "Propatria", 
          "Baralt", "Maturin", "Upata"
        ][index],
        sales: value,
        transactions: grafico_trans[index]
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
          labels: sortedLabels,  // Etiquetas ordenadas por ventas
          datasets: [
            {
              label: "Unidades Vendidas",
              backgroundColor: "rgba(99, 102, 241, 0.6)",  // Color de fondo de las barras
              data: sortedTrans,  // Datos de transacciones en el orden correcto
              borderRadius: 4,
              fill: true,  // Llenar el área debajo de las barras
            },
            {
              label: "Ventas Totales ($)",
              borderColor: "#006400",
              backgroundColor: "#1E3A8A",
              data: sortedSales,  // Datos de ventas totales en el orden correcto
              borderRadius: 4,
              fill: true,  // Llenar el área debajo de las barras
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              stacked: true,  // Apilar las barras en el eje X
            },
            y: {
              beginAtZero: true,
              stacked: true,  // Apilar las barras en el eje Y
            },
          },
          plugins: {
            tooltip: {
              enabled: true,
              callbacks: {
                label: function (tooltipItem) {
                  return tooltipItem.dataset.label + ': ' + tooltipItem.raw.toLocaleString();  // Mostrar ventas en formato de moneda
                },
              },
            },
            // Plugin de etiquetas para mostrar dentro o encima de las barras
            datalabels: {
              anchor: 'end',  // Posicionar la etiqueta al final de la barra
              align: 'start', // Alineación a la parte superior de la barra
              color: 'white', // Color de las etiquetas
              font: {
                weight: 'bold',  // Fuente en negrita
              },
              formatter: function (value) {
                return value.toLocaleString();  // Formatear el valor de las ventas como número
              },
            },
          },
        },
      });
*/