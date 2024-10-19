document.addEventListener('DOMContentLoaded', function() {
    var searchForm = document.getElementById('search-form');
    var searchSelect = document.getElementById('search-select');
    var searchInput = document.getElementById('search-input');
    var searchWarning = document.getElementById('search-warning');
    var transactionsTableBody = document.getElementById('transactions-table-body');
    var noResultsMessage = document.getElementById('no-results');

    searchSelect.addEventListener('change', function() {
        var selectedOption = this.value;
        if (selectedOption === 'descripcion' || selectedOption === 'fecha') {
            searchInput.style.display = 'inline-block';
            searchInput.value = '';
            searchInput.type = (selectedOption === 'fecha') ? 'date' : 'text';
            searchWarning.style.display = 'none';
        } else {
            searchInput.style.display = 'none';
            searchWarning.style.display = 'none';
            performSearch();
        }
    });

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        performSearch();
    });

    function performSearch() {
        var selectedOption = searchSelect.value;
        var searchText = searchInput.value.trim();

        if ((selectedOption === 'descripcion' || selectedOption === 'fecha') && searchText === '') {
            searchWarning.textContent = 'Ingresa una ' + (selectedOption === 'descripcion' ? 'descripción' : 'fecha');
            searchWarning.style.display = 'block';
            return;
        }

        searchWarning.style.display = 'none';
        var rows = transactionsTableBody.getElementsByTagName('tr');
        var found = false;

        Array.from(rows).forEach(function(row) {
            var shouldDisplay = false;
            var cells = row.getElementsByTagName('td');

            if (selectedOption === 'todos') {
                shouldDisplay = true;
            } else if (['compra', 'venta', 'gasto', 'ingreso'].includes(selectedOption)) {
                shouldDisplay = cells[0].textContent.toLowerCase() === selectedOption;
            } else if (selectedOption === 'fecha') {
                // Obtener la fecha seleccionada del calendario
                var searchDate = new Date(searchText);
                // Formatear la fecha como "YYYY-MM-DD"
                var formattedSearchDate = searchDate.toISOString().split('T')[0];
                
                // Obtener la fecha en la tabla y formatearla como "YYYY-MM-DD"
                var tableDateText = cells[3].textContent.trim();
                var [year, month, day] = tableDateText.split('/').map(Number);
                var tableDate = new Date(year, month - 1, day).toISOString().split('T')[0];
                
                // Comparar fechas
                shouldDisplay = tableDate === formattedSearchDate;
            } else if (selectedOption === 'descripcion') {
                shouldDisplay = cells[1].textContent.toLowerCase().includes(searchText.toLowerCase());
            }

            row.style.display = shouldDisplay ? '' : 'none';
            found = found || shouldDisplay;
        });

        noResultsMessage.style.display = found ? 'none' : 'block';
    }
});

