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