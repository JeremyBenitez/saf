// Gráfico para el departamento que más vendió
const ctxBest = document.getElementById('bestSalesChart').getContext('2d');
const bestSalesChart = new Chart(ctxBest, {
    type: 'line', // Tipo de gráfico: línea
    data: {
    labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'], // Cambiado a meses
    datasets: [{
        label: `Ventas del Departamento ${salesData.bestDepartment}`,
        data: salesData.bestSales, // Asegúrate de que este arreglo contenga datos
        backgroundColor: 'rgba(75, 192, 192, 0.4)', // Color de fondo
        borderColor: 'rgba(75, 192, 192, 1)', // Color de la línea
        fill: true, // Rellena el área bajo la línea
        tension: 0.4 // Curvatura de la línea
    }]
    },
    options: {
    scales: {
        y: {
        beginAtZero: true
        }
    }
    }
});

// Gráfico para el departamento que menos vendió
const ctxWorst = document.getElementById('worstSalesChart').getContext('2d');
const worstSalesChart = new Chart(ctxWorst, {
    type: 'line', // Tipo de gráfico: línea
    data: {
    labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'], // Cambiado a meses
    datasets: [{
        label: `Ventas del Departamento ${salesData.worstDepartment}`,
        data: salesData.worstSales, // Asegúrate de que este arreglo contenga datos
        backgroundColor: 'rgba(255, 99, 132, 0.4)', // Color de fondo
        borderColor: 'rgba(255, 99, 132, 1)', // Color de la línea
        fill: true, // Rellena el área bajo la línea
        tension: 0.4 // Curvatura de la línea
    }]
    },
    options: {
    scales: {
        y: {
        beginAtZero: true
        }
    }
    }
});