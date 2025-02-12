

let btn_consulta = document.getElementById('btn-buscar').addEventListener('click', () =>{
  let deposito = document.getElementById('depositSelect') 
  const selectedOption = deposito.options[deposito.selectedIndex];

  const valor = selectedOption.value
  const extra = selectedOption.dataset.extra

  console.log(extra);
  console.log(valor);

  let departamento = document.getElementById('departamentSelec')
  const departamento_value = departamento.value
  console.log(departamento_value);


  let fecha = document.getElementById('fecha').value
  console.log(fecha);
  if(valor && departamento_value && fecha){
    document.getElementById('div-grupo').style.display  = 'block'
    $.ajax({

      type: 'POST',
      url: '/inventario/grupos',
      contentType: 'application/json',
      data: JSON.stringify({codigo:departamento_value
          }),
          success: function(response) {
  
            
              console.log(response)
              $('#grupoSelect').empty().append('<option value="">Seleccione un grupo</option>');
                  $.each(response, function(index, item) {
                      $('#grupoSelect').append('<option value="' + item.c_CODIGO + '">' + item.C_DESCRIPCIO + '</option>');
                });
              
          },
          error: function(error) {
              console.error('Error:', error);
          }
      });
  }
  $.ajax({

    type: 'POST',
    url: '/inventario/resinventario',
    contentType: 'application/json',
    data: JSON.stringify({  c_CodDeposito:extra,
                            f_FechaInicio:fecha,
                            BaseDatos:valor,
                            c_Departamento:departamento_value
        }),
        success: function(response) {

          
            console.log(response)
            $('#tabla-resultados tbody').empty();

                    // Verificar si hay datos
                    if (response.length > 0) {
                        response.forEach(item => {
                            $('#inventoryTable tbody').append(`
                                <tr class="fila-producto" data-codigo="" data-descripcion="">
                                    <td>${item.c_DescripcionDeposito}</td>
                                    <td>${item.c_CodArticulo}</td>
                                    <td>${item.c_DescripcionArticulo}</td>
                                    <td>${item.n_StockActual}</td>
                                    <td>${item.Ventas30Dias}</td>
                                    <td>${item.Ventas30Mas60Dias}</td>              
                                    <td>${item.Ventas30Mas60Mas90Dias}</td>

                                    
                                </tr>
                            `);
                        });
                    }
            
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
  
})





function filterTable() {
  // Obtener el valor del input y la tabla
  const input = document.getElementById('searchInput');
  const filter = input.value.toLowerCase(); // Convertir a minúsculas para hacer la búsqueda insensible a mayúsculas/minúsculas
  const table = document.getElementById('inventoryTable');
  const rows = table.getElementsByTagName('tr'); // Obtener todas las filas

 
  for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].getElementsByTagName('td'); // Obtener las celdas de la fila
    let match = false;

   
    for (let j = 0; j < cells.length; j++) {
      const cell = cells[j];
      if (cell.textContent.toLowerCase().indexOf(filter) > -1) {
        match = true;
        break;
      }
    }

   
    rows[i].style.display = match ? '' : 'none';
  }
}

function filterTable2() {
  const input = document.getElementById('grupoSelect');
  const filter = input.value.toLowerCase(); // Convertir a minúsculas para hacer la búsqueda insensible a mayúsculas/minúsculas
  const table = document.getElementById('inventoryTable');
  const rows = table.getElementsByTagName('tr'); // Obtener todas las filas

  for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].getElementsByTagName('td'); 
    let match = false;

    for (let j = 0; j < cells.length; j++) {
      const cell = cells[j];
      if (cell.textContent.toLowerCase().indexOf(filter) > -1) {
        match = true;
        break;
      }
    }

   
    rows[i].style.display = match ? '' : 'none';
  }
}



let grupo = document.getElementById('grupoSelect')
grupo.addEventListener('change', () =>{
  const valor_grupo = grupo.value
  console.log(valor_grupo);
})