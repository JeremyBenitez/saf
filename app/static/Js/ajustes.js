  
let datosOriginales = []; // Variable global para almacenar los datos originales

// Hacer la función global
async function mostrarFactura(documento) {
    const tienda = document.getElementById('tienda').value;
    const fecha_ini = document.getElementById('startDate').value;
    const fecha_fin = document.getElementById('endDate').value;

    if (!tienda || !fecha_ini || !fecha_fin) {
        Swal.fire("Error", "Faltan datos para obtener la factura", "error");
        return;
    }

    try {
        const response = await fetch(`/ajustes/detalles?documento=${encodeURIComponent(documento)}&tienda=${encodeURIComponent(tienda)}&fecha_ini=${encodeURIComponent(fecha_ini)}&fecha_fin=${encodeURIComponent(fecha_fin)}`);
        const detalles = await response.json();

        if (!response.ok || !detalles.length) {
            Swal.fire("Error", "No se encontraron detalles para esta factura", "error");
            return;
        }

        // Tomamos el primer objeto para llenar la información principal
        const factura = detalles[0];

        // Convertir fecha correctamente en UTC
        //const fecha = factura.f_fecha ? new Date(factura.f_fecha).toLocaleDateString() : "N/P";

        const fecha = factura.f_fecha 
            ? (() => {
                const fechas = new Date(factura.f_fecha);
                return `${fechas.getUTCDate().toString().padStart(2, '0')}/${(fechas.getUTCMonth() + 1).toString().padStart(2, '0')}/${fechas.getUTCFullYear()}`;
            })() 
            : "N/P";

        document.getElementById("fecha").textContent = fecha;
        document.getElementById("origen").textContent = factura.NombreTienda || "N/P";
        document.getElementById("codigo").textContent = documento|| "N/P";

        // Limpiar tabla antes de agregar nuevas filas
        const tabla = document.getElementById("tablaArticulos");
        tabla.innerHTML = "";

        // Llenar la tabla con los artículos
        detalles.forEach(detalle => {
            const fila = document.createElement("tr");
            fila.innerHTML = `
                <td>${detalle.c_CODARTICULO || "N/A"}</td>
                <td>${detalle.n_CANTIDAD || "0"}</td>
                <td>${(detalle.TotalUSD || 0).toFixed(2)}</td>
            `;
            tabla.appendChild(fila);
        });

        // Mostrar modal
        new bootstrap.Modal(document.getElementById("facturaModal")).show();

    } catch (error) {
        console.error("Error al obtener datos de la API:", error);
        Swal.fire("Error", "Hubo un problema al obtener los detalles", "error");
    }
}

// Agregar el evento al cargar el DOM
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("buscar")?.addEventListener("click", async () => {
        const tienda = document.getElementById('tienda').value;
        const fecha_ini = document.getElementById('startDate').value;
        const fecha_fin = document.getElementById('endDate').value;

        if (!tienda || !fecha_ini || !fecha_fin) {
            Swal.fire("Error", "Faltan datos para la búsqueda", "error");
            return;
        }

        try {
            const response = await fetch(`/ajustes/aju?tienda=${encodeURIComponent(tienda)}&fecha_ini=${encodeURIComponent(fecha_ini)}&fecha_fin=${encodeURIComponent(fecha_fin)}`);
            const data = await response.json();

            if (response.ok) {
                // En la función de búsqueda, guarda los datos originales antes de generar tarjetas
                datosOriginales = data; // Guarda los datos completos
                generarTarjetas(data);
            } else {
                Swal.fire("Error", "No hay Datos para esta fecha Seleccionada", "error");
            }
        } catch (error) {
            console.error("Error en la llamada a la API:", error);
            Swal.fire("Error", "Hubo un problema con la solicitud", "error");
        }
    });

    // Función para generar tarjetas dinámicamente
    function generarTarjetas(datos) {
        const cardContainer = document.getElementById("card-container");
        cardContainer.innerHTML = "";
        document.getElementById("cantidad").textContent = datos.length;

        datos.forEach(dato => {
            const card = document.createElement("div");
            // Convertir fecha correctamente en UTC
            //const fecha1 = dato.d_FECHA ? new Date(dato.d_FECHA).toLocaleDateString() : "N/P";

            const fecha1 = dato.d_FECHA 
                ? (() => {
                    const fecha = new Date(dato.d_FECHA);
                    return `${fecha.getUTCDate().toString().padStart(2, '0')}/${(fecha.getUTCMonth() + 1).toString().padStart(2, '0')}/${fecha.getUTCFullYear()}`;
                })() 
                : "N/P";

            card.classList.add("item", "col-12", "col-md-6", "col-lg-3", "py-4", "p-md-4");
            card.innerHTML = `
                <div class="item-inner shadow rounded-4 p-4">
                    <a class="item-link" onclick="mostrarFactura('${dato.c_DOCUMENTO}')">
                        <h4 class="item-heading">Motivo: ${dato.C_MOTIVO}</h4>
                        <h4 class="item-heading">Documento: ${dato.c_DOCUMENTO}</h4>
                    </a>
                    <div class="item-desc text-center">
                        <span class="rate-icon me-2"><i class='bx bx-store'></i></span>${fecha1}
                    </div>
                </div>
            `;
            cardContainer.appendChild(card);
        });
    }

    document.getElementById("escribir").addEventListener("input", function () {
        const filtro = this.value.toLowerCase(); // Obtener el valor en minúsculas
        const datosFiltrados = datosOriginales.filter(dato => 
            dato.C_MOTIVO.toLowerCase().includes(filtro) // Filtrar por motivo
        );
        generarTarjetas(datosFiltrados); // Volver a generar las tarjetas con los datos filtrados
    });
});
