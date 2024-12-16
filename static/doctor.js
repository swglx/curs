function openModal() {
            document.getElementById('myModal').style.display = 'block';
        }

function closeModal() {
            document.getElementById('myModal').style.display = 'none';
        }

function resetForm() {
            document.getElementById('myModal').querySelector('form').reset();
        }

 function confirmDelete() {
    return confirm("Вы уверены, что хотите удалить пациента?");
 }

// Преобразование таблицы в формат Excel
function exportToExcel() {
    // Получаем ссылку на таблицу с данными
    let dataTable = document.querySelector('table');

    // Создаем новую рабочую книгу
    let workbook = XLSX.utils.book_new();

    // Создаем новый лист в рабочей книге
    let worksheet = XLSX.utils.table_to_sheet(dataTable);

    // Добавляем лист в рабочую книгу
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Данные');

    // Преобразуем рабочую книгу в бинарный формат
    let excelData = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });

    // Создаем объект Blob для сохранения файла Excel
    let blob = new Blob([excelData], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

    // Создаем ссылку для скачивания файла
    let a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'data.xlsx';
    a.click();
}

// Функция для поиска врачей по фамилии
function searchDoctor() {
    let searchValue = document.getElementById('searchInput').value.trim().toLowerCase();

    let rows = Array.from(document.querySelectorAll('tbody tr'));

    rows.forEach(row => {
        let surname = row.querySelector('td:nth-child(2)').textContent.trim().toLowerCase();
        if (surname.includes(searchValue)) {
            row.style.display = 'table-row';
        } else {
            row.style.display = 'none';
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const table = document.querySelector('table');

  // Создаем объект для хранения информации о сортировке
  const sortInfo = {
    sortedColumn: null,
    sortAscending: true,
  };

  // Функция для сортировки таблицы по столбцу
  function sortTable(columnIndex) {
    const rows = Array.from(table.querySelectorAll('tbody tr'));

    // Определяем направление сортировки
    let sortDirection = 1;
    if (sortInfo.sortedColumn === columnIndex) {
      sortDirection = sortInfo.sortAscending ? 1 : -1;
      sortInfo.sortAscending = !sortInfo.sortAscending;
    } else {
      sortInfo.sortedColumn = columnIndex;
      sortInfo.sortAscending = true;
    }

    // Сортируем строки таблицы
    rows.sort((a, b) => {
      const aValue = a.children[columnIndex].textContent.trim().toLowerCase();
      const bValue = b.children[columnIndex].textContent.trim().toLowerCase();
      return aValue.localeCompare(bValue) * sortDirection;
    });

    // Обновляем порядок строк в таблице
    rows.forEach(row => table.querySelector('tbody').appendChild(row));
  }

  // Обработчик события клика на заголовок столбца
  table.addEventListener('click', function (event) {
    if (event.target.matches('th[data-sortable]')) {
      const columnIndex = Array.from(event.target.parentNode.children).indexOf(event.target);
      sortTable(columnIndex);
    }
  });
});