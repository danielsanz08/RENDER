// Asegúrate de que las bibliotecas html2pdf.js y xlsx.js estén incluidas en tu HTML antes de este script

function exportToPDF() {
    const element = document.getElementById('search-results'); // Elemento a imprimir

    const options = {
        margin: 0.5,
        filename: 'Clientes_Registrados.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' },
        pagebreak: { mode: ['css', 'legacy'] } // Usar modo de CSS para mejor manejo de saltos de página
    };

    // Ocultar elementos no deseados
    document.querySelectorAll('.navbar__menu, .btn, #search-form, #search-warning, #toggle-accessibility-menu, .opciones, .toolbar').forEach(el => el.style.display = 'none');

    // Crear el PDF
    html2pdf()
        .from(element)
        .set(options)
        .save()
        .then(() => {
            // Restaurar elementos ocultos después de la exportación
            document.querySelectorAll('.navbar__menu, .btn, #search-form, #search-warning, #toggle-accessibility-menu, .opciones, .toolbar').forEach(el => el.style.display = '');
        });
}

function exportToExcel() {
    // Obtener la tabla
    var table = document.getElementById('search-results');
    
    // Crea un nuevo libro de trabajo
    var wb = XLSX.utils.table_to_book(table, { sheet: "Clientes" });
    
    // Exportar el libro de trabajo a un archivo .xlsx
    XLSX.writeFile(wb, 'Clientes_Registrados.xlsx');
}

// Asegúrate de que estas funciones se llamen desde los botones en tu HTML
