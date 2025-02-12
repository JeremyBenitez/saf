

function filterTable() {
  const searchInput = document.getElementById('searchInput').value.toLowerCase();
  const checkboxes = document.querySelectorAll('.groupContainer');
  const table = document.getElementById('inventoryTable');
  const rows = table.getElementsByTagName('tr');

  // Obtener los valores de los checkboxes seleccionados
  const filters = Array.from(checkboxes)
    .filter(checkbox => checkbox.checked)
    .map(checkbox => checkbox.value.toLowerCase());

  for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].getElementsByTagName('td');
    const articleCode = cells[1].textContent.toLowerCase(); // Código en la columna 1
    const articleName = cells[2].textContent.toLowerCase(); // Nombre en la columna 2

    // Condiciones para mostrar la fila
    const matchesSearch = articleCode.includes(searchInput) || articleName.includes(searchInput);
    const matchesCheckbox = filters.length === 0 || filters.some(filter => articleCode.includes(filter));

    // Mostrar la fila si cumple con ambas condiciones
    if (matchesSearch && matchesCheckbox) {
      rows[i].style.display = '';
    } else {
      rows[i].style.display = 'none';
    }
  }
}

// Agregar evento 'change' a los checkboxes para que también activen el filtrado
const checkboxes = document.querySelectorAll('.filter-checkbox');
checkboxes.forEach(checkbox => {
  checkbox.addEventListener('change', filterTable);
});

