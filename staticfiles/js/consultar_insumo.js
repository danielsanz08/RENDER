function printTable() {
    window.print();
}

function exportToExcel() {
    let table = document.querySelector(".table");
    let wb = XLSX.utils.table_to_book(table, { sheet: "Sheet1" });
    XLSX.writeFile(wb, "tabla_insumos.xlsx");
}

function exportToPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    doc.autoTable({ html: '.table' });
    doc.save('tabla_insumos.pdf');
}

let deleteUrl = ""; // Variable para almacenar la URL de eliminación

function showConfirmModal(event, element) {
    event.preventDefault(); // Prevenir la acción de redirección por defecto
    deleteUrl = element.href; // Guardar la URL de eliminación en una variable
    document.getElementById("confirmModal").style.display = "flex"; // Mostrar el modal
}

function closeModal() {
    document.getElementById("confirmModal").style.display = "none"; // Ocultar el modal
}

function confirmDelete() {
    window.location.href = deleteUrl; // Redirigir a la URL de eliminación si el usuario confirma
}
