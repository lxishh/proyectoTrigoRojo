document.getElementById("searchInput").addEventListener("keyup", function () {
  const filter = this.value.toLowerCase();
  const rows = document.querySelectorAll("#productosTable tbody tr");

  rows.forEach((row) => {
    const name = row.cells[1].textContent.toLowerCase(); // Toma el texto de la columna "Nombre"
    row.style.display = name.includes(filter) ? "" : "none";
  });
});
