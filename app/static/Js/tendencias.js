// Variable global para almacenar los datos de los departamentos
let departamentosData = null;

            // Función para hacer la solicitud a la API y actualizar los contadores (una sola vez)
            async function fetchSalesData() {
                try {
                    // Hacer la solicitud a la API
                    const response = await fetch('http://10.21.5.23:5000/tendencias/api/cantidad');
                                        
                    // Verificar si la respuesta es exitosa
                    if (!response.ok) {
                        throw new Error('Error al obtener los datos de la API');
                    }

                    // Convertir la respuesta a JSON
                    const data = await response.json();

                    // Depuración: Verificar los datos obtenidos
                    console.log('Datos obtenidos de la API:', data);

                    // Verificar si la respuesta es una lista con un solo objeto
                    if (Array.isArray(data) && data.length > 0) {
                        const salesData = data[0]; // Obtener el primer (y único) objeto de la lista
                        
                        // Guardar los datos en la variable global
                        departamentosData = salesData;

                        // Iterar sobre las claves del objeto
                        Object.keys(salesData).forEach(key => {
                            // Buscar el span con el id correspondiente a la clave
                            const salesCountSpan = document.getElementById(key);
                            if (salesCountSpan) {
                                // Actualizar el contenido del span con el total de ventas
                                salesCountSpan.textContent = `${salesData[key].toLocaleString()} Unidades vendidas`;
                            } else {
                                console.warn(`No se encontró un span con el id: ${key}`);
                            }
                        });
                    } else {
                        console.error('La respuesta de la API no tiene el formato esperado');
                    }
                } catch (error) {
                    console.error('Error al obtener los datos:', error);
                    // Si hay un error, mostrar un mensaje de error en los spans
                    document.querySelectorAll('.sales-count').forEach(span => {
                        span.textContent = 'Error al cargar';
                    });
                }
            }

            // Función para ajustar el tamaño del span según el contenido
            function adjustSpanSize() {
                // Seleccionar todos los spans con la clase .sales-count
                document.querySelectorAll('.sales-count').forEach(span => {
                    // Calcular el ancho necesario en función del contenido
                    const textWidth = span.scrollWidth; // Ancho del contenido
                    const maxWidth = 350; // Ancho máximo permitido
                    const minWidth = 200; // Ancho mínimo permitido

                    // Ajustar el ancho del span
                    if (textWidth > maxWidth) {
                        span.style.width = `${maxWidth}px`; // Limitar al ancho máximo
                    } else if (textWidth < minWidth) {
                        span.style.width = `${minWidth}px`; // Limitar al ancho mínimo
                    } else {
                        span.style.width = `${textWidth}px`; // Ajustar al ancho del contenido
                    }
                });
            }

            // Función para cargar detalles del departamento (una sola petición por departamento)
            function loadDepartmentData(departmentCode) {
                // Verificar si ya tenemos datos en caché
                if (window[`departmentDetails_${departmentCode}`]) {
                    displayDepartmentDetails(departmentCode, window[`departmentDetails_${departmentCode}`]);
                    return;
                }
                
                // Si no hay datos en caché, hacer la petición
                $.ajax({
                    url: `http://10.21.5.23:5000/tendencias/detalles/${departmentCode}`,
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({}),
                    success: function(response) {
                        console.log('Datos recibidos:', response);
                        
                        // Guardar los datos en caché
                        window[`departmentDetails_${departmentCode}`] = response;
                        
                        // Mostrar los datos
                        displayDepartmentDetails(departmentCode, response);
                    },
                    error: function(xhr, status, error) {
                        console.error('Error al cargar los datos:', error);
                        $('#modal-stores-container').html(`<div class="alert alert-danger">Error al cargar los datos: ${error}</div>`);
                    }
                });
            }

            function displayDepartmentDetails(departmentCode, response) {
                // Limpiar el contenedor de tiendas
                $('#modal-stores-container').empty();
                
                // Verificar si hay datos de tiendas
                if (response && response.valores_tiendas) {
                    // Convertir el objeto de tiendas en un array
                    const tiendas = Object.keys(response.valores_tiendas);

                    // Ordenar las tiendas de mayor a menor según el total general vendido
                    tiendas.sort((a, b) => {
                        const cantidadA = response.valores_tiendas[a].cantidad || 0;
                        const cantidadB = response.valores_tiendas[b].cantidad || 0;
                        return cantidadB - cantidadA; // Orden descendente
                    });

                    // Iterar sobre cada tienda y crear una tarjeta para cada una
                    tiendas.forEach((tienda, index) => {
                        const datosTienda = response.valores_tiendas[tienda];
                        const productoMasVendido = datosTienda.producto_mas_vendido || {};
                        
                        // Crear una tarjeta para la tienda con los datos formateados
                        const tiendaCard = `
                            <div class="col-md-3">
                                <div class="card mb-4 shadow-sm" style="margin: 10px;">
                                    <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                                        <h5 class="mb-0">${formatTiendaName(tienda)}</h5>
                                        <i class="fas fa-store"></i> <!-- Icono de tienda -->
                                    </div>
                                    <div class="card-body p-4">
                                        <div class="d-flex flex-column gap-3">
                                            <!-- Total vendido (de todo el departamento) -->
                                            <div class="d-flex align-items-center gap-2">
                                                <i class="fas fa-chart-bar text-primary"></i>
                                                <div>
                                                    <p class="mb-0 text-muted">Total vendido (departamento)</p>
                                                    <p class="mb-0 fw-bold">${numberWithCommas(datosTienda.cantidad || 0)} unidades</p>
                                                </div>
                                            </div>

                                            <!-- Artículo más vendido -->
                                            <div class="d-flex align-items-center gap-2">
                                                <i class="fas fa-star text-warning"></i>
                                                <div>
                                                    <p class="mb-0 text-muted">Artículo más vendido</p>
                                                    <p class="mb-0 fw-bold">${productoMasVendido.nombre || 'No disponible'}</p>
                                                </div>
                                            </div>

                                            <!-- Código del producto -->
                                            <div class="d-flex align-items-center gap-2">
                                                <i class="fas fa-barcode text-success"></i>
                                                <div>
                                                    <p class="mb-0 text-muted">Código del producto</p>
                                                    <p class="mb-0 fw-bold">${productoMasVendido.codigo || 'No disponible'}</p>
                                                </div>
                                            </div>

                                            <!-- Cantidad vendida (del producto más vendido) -->
                                            <div class="d-flex align-items-center gap-2">
                                                <i class="fas fa-boxes text-info"></i>
                                                <div>
                                                    <p class="mb-0 text-muted">Cantidad vendida (artículo)</p>
                                                    <p class="mb-0 fw-bold">${numberWithCommas(productoMasVendido.cantidad || 0)} unidades</p>
                                                </div>
                                            </div>

                                            <!-- Sección "Top de los 20 artículos más vendidos" -->
                                            <div class="d-flex align-items-center gap-2 top-section" onclick="openTop20('${departmentCode}')">
                                                <i class="fas fa-fire-alt text-danger"></i> <!-- Icono de fuego mejorado -->
                                                <div>
                                                    <p class="mb-0 text-muted">Top 20 artículos más vendidos</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `;
                        
                        // Agregar la tarjeta al contenedor del modal
                        $('#modal-stores-container').append(tiendaCard);
                    });
                } else {
                    // Si no hay datos, mostrar un mensaje
                    $('#modal-stores-container').html('<div class="alert alert-warning">No hay datos disponibles para este departamento.</div>');
                }
            }

            // Función para manejar el clic en la sección "Top de los 20 artículos más vendidos"
            function openTop20(departmentCode) {
                alert(`Abriendo el Top 20 del departamento: ${departmentCode}`);
                // Aquí puedes agregar la lógica para abrir un modal o redirigir a otra vista
            }

            // Función para formatear el nombre de la tienda (primera letra en mayúscula)
            function formatTiendaName(name) {
                return name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();
            }

            // Función para formatear números con comas como separadores de miles
            function numberWithCommas(x) {
                return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            }

            // Cuando el DOM esté listo
            document.addEventListener('DOMContentLoaded', function() {
                // Cargar los datos iniciales
                fetchSalesData();
                
                // Ajustar el tamaño de los spans
                adjustSpanSize();
                
                // Configurar el observador para ajustar los spans cuando cambie su contenido
                const observer = new MutationObserver(adjustSpanSize);
                document.querySelectorAll('.sales-count').forEach(span => {
                    observer.observe(span, { childList: true, characterData: true });
                });
                
                // Configurar el evento del modal
                $('#departmentModal').on('show.bs.modal', function (event) {
                    let button = $(event.relatedTarget); // Botón que activó el modal
                    let department = button.data('department'); // Extraer el nombre del departamento
                    let departmentId = button.attr('id'); // Obtener el ID del botón
                    
                    // Actualizar el título del modal
                    let modal = $(this);
                    modal.find('.modal-title').text('Departamento: ' + department);
                    
                    // Determinar el código del departamento
                    let departmentCode;
                    if (departmentId) {
                        departmentCode = departmentId.toUpperCase();
                    } else {
                        // Si no hay un ID, usar la primera o las dos primeras letras del nombre del departamento
                        const deptName = department || '';
                        if (deptName.includes(' ')) {
                            // Si hay un espacio, usar la primera letra de cada palabra
                            departmentCode = deptName.split(' ').map(word => word.charAt(0)).join('').toUpperCase();
                        } else {
                            // Si no hay espacio, usar las dos primeras letras
                            departmentCode = deptName.substring(0, 2).toUpperCase();
                        }
                    }
                    
                    // Cargar los datos del departamento (solo una vez por departamento)
                    loadDepartmentData(departmentCode);
                });
                
                // Asignar eventos de clic a todos los botones de departamento
                document.querySelectorAll('.btn-primary').forEach(button => {
                    button.addEventListener('click', function() {
                        // No es necesario hacer nada aquí, ya que el modal se encargará de todo
                        // cuando se muestre
                    });
                });
            });