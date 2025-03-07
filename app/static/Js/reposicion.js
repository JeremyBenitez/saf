document.addEventListener("DOMContentLoaded", () => {

    document.getElementById("buscar")?.addEventListener("click", async () => {
        const codigo = document.getElementById('codigo').value;
            codigo.value = codigo.toUpperCase();
        const fecha_ini = document.getElementById('startDate').value;
        const fecha_fin = document.getElementById('endDate').value;

        if (!codigo || !fecha_ini || !fecha_fin) {
            Swal.fire("Error", "Faltan datos para la búsqueda", "error");
            return;
        }

        try {
            const response = await fetch(`/reposicion/repo?codigo=${encodeURIComponent(codigo)}&fecha_ini=${encodeURIComponent(fecha_ini)}&fecha_fin=${encodeURIComponent(fecha_fin)}`);
            const data = await response.json();

            if (response.ok) {
                const tableBody = document.getElementById("table-body");

                const dias_ana = data[0].DiasAnalisis;
                // Referenciamos el span y actualizamos su contenido
                document.getElementById('ana').textContent = dias_ana;

                tableBody.innerHTML = ""; // Limpia la tabla antes de agregar nuevos datos

                data.forEach((item, index) => {
                    /*
                    // Definir el porcentaje de progreso basado en salidas
                    let progreso = 0;
                    if (item.StockActual + item.Entradas > 0) {
                        progreso = Math.round((item.Salidas / (item.StockActual + item.Entradas)) * 100);
                    }
                    console.log(progreso);
                    */
                    // Determinar el color de la barra de progreso
                    let colorClass = "bg-danger"; // Rojo por defecto
                    if (item.Salidas > 3 && item.Salidas <= 6) {
                        colorClass = "bg-primary"; // Azul
                    } else if (item.Salidas > 6) {
                        colorClass = "bg-success"; // Verde
                    }

                    // Crear la fila con los datos
                    const row = `
                        <tr>
                            <td>${item.CodArticulo}</td>
                            <td>${item.DescripcionArticulo}</td>
                            <td>${item.Tienda}</td>
                            <td>${item.StockActual}</td>
                            <td>${item.Entradas}</td>
                            <td>${item.Salidas}</td>
                            <td>${item.SugerirReposicion}</td>
                            <td>${item.MontoSugeridoReposicion}</td>
                            <td>
                                <div class="progress">
                                    <div class="progress-bar ${colorClass}" 
                                                role="progressbar" 
                                                style="width: ${item.Salidas * 1.5}%"
                                                aria-valuenow="${item.Salidas}"
                                                aria-valuemin="0" 
                                                aria-valuemax="10">
                                    </div>
                                </div>
                            </td>
                        </tr>
                    `;
                    tableBody.innerHTML += row;
                });

            } else {
                Swal.fire("Error", data.error || "No se pudo obtener los datos", "error");
            }
        } catch (error) {
            Swal.fire("Error", "No se pudo conectar con la API", "error");
            console.error(error);
        }
    });
})        