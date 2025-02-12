 // Gráfico de Ventas Diarias
 const ctxDaily = document.getElementById('dailySalesChart').getContext('2d');
 new Chart(ctxDaily, {
   type: 'line',
   data: {
     labels: ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
     datasets: [{
       label: 'Ventas Diarias $',
       data: salesData.dailySales,
       backgroundColor: 'rgba(75, 192, 192, 0.4)',
       borderColor: 'rgba(75, 192, 192, 1)',
       fill: true,
       tension: 0.4
     }]
   },
   options: { scales: { y: { beginAtZero: true } } }
 });

 // Gráfico de Ventas Semanales
 const ctxWeekly = document.getElementById('weeklySalesChart').getContext('2d');
 new Chart(ctxWeekly, {
   type: 'bar',
   data: {
     labels: ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4', 'Semana 5'],
     datasets: [{
       label: 'Ventas Semanales $',
       data: salesData.weeklySales,
       backgroundColor: 'rgba(255, 159, 64, 0.4)',
       borderColor: 'rgba(255, 159, 64, 1)',
       fill: true
     }]
   },
   options: { scales: { y: { beginAtZero: true } } }
 });

 // Gráfico de Ventas Mensuales
 const ctxMonthly = document.getElementById('monthlySalesChart').getContext('2d');
 new Chart(ctxMonthly, {
   type: 'line',
   data: {
     labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
     datasets: [{
       label: 'Ventas Mensuales $',
       data: salesData.monthlySales,
       backgroundColor: 'rgba(153, 102, 255, 0.4)',
       borderColor: 'rgba(153, 102, 255, 1)',
       fill: true,
       tension: 0.4
     }]
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
      y:{ 
        beginAtZero: true 
      } 
    } 
  }
 });


