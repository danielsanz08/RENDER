document.addEventListener('DOMContentLoaded', function() {
    var searchForm = document.getElementById('search-form');
    var searchSelect = document.getElementById('search-select');
    var searchInput = document.getElementById('search-input');
    var searchWarning = document.getElementById('search-warning');
    var tableBody = document.querySelector('.table tbody');
    var noResultsMessage = document.getElementById('no-results');

    // Cambiar el tipo de input y mostrarlo según la opción seleccionada
    searchSelect.addEventListener('change', function() {
        var selectedOption = this.value;

        if (selectedOption === 'todos') {
            searchInput.style.display = 'none';
            searchInput.value = '';
        } else {
            searchInput.style.display = 'inline-block'; // Asegúrate de que se muestre el input
            searchInput.type = 'text'; // Cambiar el tipo a 'text'
            searchInput.value = ''; // Limpiar el valor del input
        }
    });

    // Manejar el envío del formulario para realizar la búsqueda
    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        performSearch();
    });

    // Función para realizar la búsqueda en la tabla
    function performSearch() {
        var selectedOption = searchSelect.value;
        var searchText = searchInput.value.trim().toLowerCase();
        var rows = tableBody.getElementsByTagName('tr');
        var found = false;

        // Mostrar aviso si el campo está vacío y no es "todos"
        if (searchText === '' && selectedOption !== 'todos') {
            // Seleccionar el elemento de aviso
            const searchWarning = document.getElementById('search-warning');

            function showWarning(message) {
                // Mostrar el aviso de advertencia usando SweetAlert2
                Swal.fire({
                    title: 'ERROR',
                    text: message,
                    icon: 'warning',
                    iconColor: '#ff4f5e', // Color personalizado para el ícono de advertencia
                    background: '#fff', // Fondo con el color principal de la página
                    color: '#000', // Texto en blanco para contraste
                    confirmButtonText: 'OK',
                    confirmButtonColor: '#ff4f5e', // Botón de confirmación en rojo
                    customClass: {
                        popup: 'swal2-border-radius', // Clase personalizada para bordes redondeados
                    }
                });
            }
            
            // Ejemplo de uso
            const searchText = ''; // Ejemplo de valor para la búsqueda
            const selectedOption = 'algun valor'; // Ejemplo de opción seleccionada
            
            if (searchText === '' && selectedOption !== 'todos') {
                showWarning('Por favor, ingresa un valor de búsqueda.');
                return;
            }
        }

        searchWarning.style.display = 'none'; // Ocultar advertencia

        // Iterar a través de cada fila de la tabla
        Array.from(rows).forEach(function(row) {
            var cells = row.getElementsByTagName('td');
            var shouldDisplay = false;

            // Determinar si se debe mostrar la fila según la opción seleccionada
            if (selectedOption === 'todos') {
                shouldDisplay = true; // Mostrar todas las filas
            } else if (selectedOption === 'tipo_cliente') {
                shouldDisplay = cells[0].textContent.toLowerCase().includes(searchText); // Filtrar por tipo cliente
            } else if (selectedOption === 'nombre') {
                shouldDisplay = cells[1].textContent.toLowerCase().includes(searchText); // Filtrar por nombre
            } else if (selectedOption === 'email') {
                shouldDisplay = cells[2].textContent.toLowerCase().includes(searchText); // Filtrar por email
            } else if (selectedOption === 'telefono') {
                shouldDisplay = cells[3].textContent.toLowerCase().includes(searchText); // Filtrar por teléfono
            } else if (selectedOption === 'direccion') {
                shouldDisplay = cells[4].textContent.toLowerCase().includes(searchText); // Filtrar por dirección
            }

            row.style.display = shouldDisplay ? '' : 'none'; // Mostrar u ocultar fila
            found = found || shouldDisplay; // Determinar si se encontraron resultados
        });

        // Mostrar mensaje si no se encontraron resultados
        noResultsMessage.style.display = found ? 'none' : 'block';
    }
});




function printTable() {
    const element = document.getElementById('search-results'); // Elemento a imprimir
    const options = {
        margin: 1,
        filename: 'Clientes_Registrados.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    };

    // Estilo adicional para el PDF
    const customStyle = `
        <style>
            body {
                font-family: 'Arial', sans-serif;
                text-align: center;
                margin: 0;
                padding: 20px;
            }
            .header-content {
                display: flex;
                flex-direction: column;
                align-items: center;
                margin-bottom: 20px;
            }
            .header-content img {
                width: 80px; /* Ajusta el tamaño del logo */
                height: auto;
                margin-bottom: 10px; /* Espacio debajo del logo */
            }
            h1 {
                font-size: 24px; /* Tamaño del título */
                color: #01AB7B; /* Color del título */
                margin: 10px 0; /* Margen arriba y abajo */
            }
            .table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0; /* Margen arriba y abajo */
            }
            .table th, .table td {
                border: 1px solid #ddd;
                padding: 12px; /* Espaciado interno */
                text-align: left;
                background-color: #fff; /* Color de fondo */
            }
            .table th {
                background-color: #01AB7B; /* Color del encabezado */
                color: #fff; /* Color del texto en el encabezado */
            }
            /* Ocultar la última columna */
            .table td:last-child, .table th:last-child {
                display: none;
            }
        </style>
    `;

    // Crear un nuevo documento con el estilo
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
            <head>
                <title>Imprimir Tabla</title>
                ${customStyle} <!-- Aplicar estilos personalizados -->
            </head>
            <body>
                <div class="header-content">
                    <img src="{% static 'imagen/logo.png' %}" alt="Logo"> <!-- Ruta de tu logo -->
                    <h1>Lácteos Hedybed</h1>
                </div>
                <h1>CLIENTES REGISTRADOS</h1>
                <table class="table">
                    <thead>
                <tr>
                    <th title="Tipo de cliente">Tipo Cliente</th>
                    <th>Tipo de documento</th>
                    <th>Número de documento</th>
                    <th title="Nombre">Nombre</th>
                    <th title="Email">Email</th>
                    <th title="Teléfono">Teléfono</th>
                    <th title="Dirección">Dirección</th>
                    <th title="Registrado por">Registrado por</th>
                    <th title="Acciones">Acciones</th>
                </tr>
            </thead>
                    <tbody>
                        {% for cliente in clientes %}
                            <tr>
                                <td>{{ cliente.tipo_cliente|capfirst }}</td>
                                <td>{{ cliente.nombre }}</td>
                                <td>{{ cliente.email }}</td>
                                <td>{{ cliente.telefono }}</td>
                                <td>{{ cliente.direccion }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </body>
        </html>
    `);
    printWindow.document.close(); // Cierra el documento
    printWindow.print(); // Abre el diálogo de impresión
    printWindow.close(); // Cierra la ventana de impresión
}


function exportToPDF() {
    const element = document.body;
    // Crear e inyectar estilos específicos para el PDF
    const styleSheet = document.createElement('style');
    styleSheet.type = 'text/css';
    styleSheet.innerText = `
        /* Estilos generales del header */
        header {
            display: flex !important;
            justify-content: center;
            align-items: center; /* Centrar horizontalmente */
            padding: 15px 0;
            margin: 0;
            border-bottom: 2px solid #01AB7B; /* Color principal */
            background-color: #e4f1f2 !important;
            width: 100%;
            position: relative;
        }

        .header-content {
            display: flex;
            align-items: center;
            padding: 5px 20px;
            border-radius: 8px;
            background-color: #ffffff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin: 0 auto;
        }

        .header-content img {
            width: 80px;
            height: auto;
            margin-right: 12px;
        }

        .header-content b {
            font-size: 26px;
            color: #000000;
            font-weight: 700;
            margin: 0;
            font-family: 'Georgia', serif;
        }

        /* Estilos de la tabla */
        .table {
            width: 100%; /* Asegura que la tabla ocupe el 100% del ancho */
            border-collapse: collapse;
            margin: 20px 0; /* Margen superior e inferior */
            background-color: #f8f8f8; /* Fondo de la tabla */
        }

        .table th, .table td {
            border: 1px solid #ddd;
            padding: 12px 18px;
            text-align: left;
            color: #333;
            font-size: 16px;
            font-family: 'Arial', sans-serif;
            background-color: #fff;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 6px;
        }

        .table th {
            background-color: #01AB7B; /* Color principal */
            color: #ffffff;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 14px;
        }

        .table tr:nth-child(even) {
            background-color: #f2f2f2;
        }

        .table tr:nth-child(odd) {
            background-color: #ffffff;
        }

        /* Eliminar la última columna de la tabla */
        .table td:last-child, .table th:last-child {
            display: none; /* Ocultar última columna */
        }

        /* Evitar que las celdas se dividan entre páginas */
        tr, td, th {
            page-break-inside: avoid;
            break-inside: avoid;
        }

        /* Ocultar elementos no deseados */
        .navbar__menu, .btn, #search-form, #no-results, #search-warning, 
        #toggle-accessibility-menu, .opciones, .toolbar, .header-icons, .user, footer {
            display: none !important;
        }
    `;
    document.head.appendChild(styleSheet);

    // Crear marca de agua como una imagen
    const watermark = document.createElement('img');
    watermark.src = watermarkUrl; // Usa la variable definida en el HTML
    watermark.className = 'watermark';
    document.body.appendChild(watermark);

    watermark.onload = () => {
        // Ocultar otros elementos no deseados
        const elementsToHide = document.querySelectorAll('.navbar-menu, .btn, #search-form, #search-warning, #toggle-accessibility-menu, .opciones, .toolbar');
        elementsToHide.forEach(el => el.style.display = 'none');

        // Seleccionar el elemento "no se encontraron resultados"
        const noResults = document.querySelector('#no-results');

        // Guardar el estado original del elemento
        const noResultsParent = noResults?.parentNode;
        const noResultsSibling = noResults?.nextSibling;

        // Eliminar el aviso de "no se encontraron resultados"
        if (noResults) {
            noResultsParent?.removeChild(noResults);
        }

        // Crear PDF usando html2pdf
        html2pdf().from(element).set({
            margin: [0.5, 0.5, 0.5, 0.5], // Márgenes ajustados para evitar saltos innecesarios
            filename: 'pagina_completa.pdf',
            html2canvas: { scale: 2, logging: true },
            jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' },
            pagebreak: { mode: ['css', 'legacy'] } // Configuración para gestionar mejor los saltos
        }).toPdf().get('pdf').then(function (pdf) {
            // Restaurar el contenido original
            elementsToHide.forEach(el => el.style.display = '');
            document.body.removeChild(watermark);
            document.head.removeChild(styleSheet);
            if (noResults) {
                noResultsParent?.insertBefore(noResults, noResultsSibling);
            }
            pdf.save('Tabla_Clientes.pdf');
        }).catch(error => {
            console.error('Error al generar el PDF:', error);
            // Restaurar el contenido original en caso de error
            elementsToHide.forEach(el => el.style.display = '');
            document.body.removeChild(watermark);
            document.head.removeChild(styleSheet);
            if (noResults) {
                noResultsParent?.insertBefore(noResults, noResultsSibling);
            }
        });
    };
}

async function exportToExcel() {
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Sheet1');

    // Datos de la empresa
    const companyName = 'LACTEOS HEDYBED'; // Cambia esto por el nombre de tu empresa
    const imageUrl = '/static/imagen/logo_hedybed.png'; // Ruta de tu imagen

    try {
        // Leer la imagen como buffer
        const response = await fetch(imageUrl);
        if (!response.ok) throw new Error('Network response was not ok.');
        const imageBlob = await response.blob();
        const imageArrayBuffer = await imageBlob.arrayBuffer();

        // Agregar la imagen al archivo Excel
        const imageId = workbook.addImage({
            buffer: imageArrayBuffer,
            extension: 'png',
        });

        // Añadir la imagen al archivo Excel y centrarla en las celdas combinadas
        worksheet.addImage(imageId, {
            tl: { col: 0, row: 0 }, // Posición de la imagen
            ext: { width: 150, height: 97 }, // Tamaño de la imagen
        });

        // Combinar celdas para el logo y el nombre de la empresa
        worksheet.mergeCells('A1:E1'); // Combina cuatro columnas (A, B, C, D)

        // Añadir el nombre de la empresa a la celda combinada
        worksheet.getCell('A1').value = companyName;
        worksheet.getCell('A1').font = {
            bold: true,
            size: 18,
            name: 'Arial' // Tipo de letra
        };
        worksheet.getCell('A1').alignment = { vertical: 'middle', horizontal: 'center' };
        worksheet.getCell('A1').fill = {
            type: 'pattern',
            pattern: 'solid',
            fgColor: { argb: 'FFFFFF' } // Fondo blanco para la celda de texto
        };

        // Añadir borde a la celda combinada
        worksheet.getCell('A1').border = {
            top: { style: 'medium', color: { argb: '000000' } },
            left: { style: 'medium', color: { argb: '000000' } },
            bottom: { style: 'medium', color: { argb: '000000' } },
            right: { style: 'medium', color: { argb: '000000' } }
        };

        // Ajustar la altura de la fila para que el texto y la imagen queden bien alineados
        worksheet.getRow(1).height = 75; // Mantener la altura de la fila

    } catch (error) {
        console.error('Error al obtener o agregar la imagen:', error);
    }

    // Agregar los datos de la tabla HTML al archivo Excel
    const table = document.querySelector(".table");
    const rows = table.querySelectorAll("tr");

    let rowIndex = 2; // Ajustar el índice de fila para después del encabezado y del logo/nombre
    rows.forEach((row, index) => {
        const cells = row.querySelectorAll("th, td");
        cells.forEach((cell, cellIndex) => {
            if (cellIndex < cells.length - 1) { // Excluir la última columna
                const cellAddress = worksheet.getCell(rowIndex, cellIndex + 1);
                cellAddress.value = cell.innerText;

                // Aplicar estilos a las celdas
                if (index === 0) { // Fila de encabezado
                    cellAddress.font = { bold: true, color: { argb: '000000' } };
                    cellAddress.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: '01AB7B' } };
                    cellAddress.alignment = { vertical: 'middle', horizontal: 'center' };
                } else {
                    cellAddress.border = {
                        top: { style: 'thin' },
                        left: { style: 'thin' },
                        bottom: { style: 'thin' },
                        right: { style: 'thin' }
                    };
                    cellAddress.alignment = { vertical: 'middle', horizontal: 'center' };
                }
            }
        });
        rowIndex++;
    });

    // Ajustar el ancho de las columnas
    worksheet.columns.forEach(column => {
        column.width = 25;
    });

    // Generar el archivo y descargarlo
    workbook.xlsx.writeBuffer().then(buffer => {
        saveAs(new Blob([buffer]), 'Tabla_Clientes.xlsx');
    }).catch(error => {
        console.error('Error al generar el archivo Excel con diseño:', error);
    });
}
