
function openModal() {
    document.getElementById("myModal").style.display = "flex";
}


function closeModal() {
    document.getElementById("myModal").style.display = "none";
}

function resetForm() {
            document.getElementById('myModal').querySelector('form').reset();
        }

 function confirmDelete() {
    return confirm("Вы уверены, что хотите удалить пациента?");
 }

function openUpdateModal(name) {
  // Отобразить модальное окно для обновления информации о пациенте
  var updateModal = document.getElementById("updateModal");
  updateModal.style.display = "flex";

  // Заполнить поле имени в модальном окне
  var updateNameField = document.getElementById("updateName");
  updateNameField.value = name;

  // Получить значения остальных полей пациента из таблицы
  var patientRow = Array.from(document.querySelectorAll('td')).find(td => td.textContent === name).parentNode;
  var patientPolicyNumber = patientRow.cells[1].textContent; // Номер полиса
  var patientPlotId = patientRow.cells[2].textContent; // Номер участка
  var patientSurname = patientRow.cells[3].textContent;
  var patientAddress = patientRow.cells[6].textContent;
  var patientWork = patientRow.cells[7].textContent;
  var patientComplaints = patientRow.cells[8].textContent;

  // Заполнить остальные поля модального окна данными о пациенте
  var updatePolicyNumberField = document.getElementById("updatePolicyNumber");
  updatePolicyNumberField.value = patientPolicyNumber;

  var updatePlotIdField = document.getElementById("updatePlotId");
  updatePlotIdField.value = patientPlotId;

  var updateSurnameField = document.getElementById("updateSurname");
  updateSurnameField.value = patientSurname;

  var updateAddressField = document.getElementById("updateAddress");
  updateAddressField.value = patientAddress;

  var updateWorkField = document.getElementById("updateWork");
  updateWorkField.value = patientWork;

  var updateComplaintsField = document.getElementById("updateComplaints");
  updateComplaintsField.value = patientComplaints;
}
  function closeUpdateModal() {
    // Скрыть модальное окно для обновления информации о пациенте
    var updateModal = document.getElementById("updateModal");
    updateModal.style.display = "none";
  }

function exportToExcel() {
    // Получаем ссылку на таблицу с данными
    let dataTable = document.querySelector('table');

    // Копируем таблицу без столбца с кнопками "Обновить"
    let dataTableCopy = dataTable.cloneNode(true);
    let buttonsColumn = dataTableCopy.getElementsByTagName('td');
    for (let i = 0; i < buttonsColumn.length; i++) {
        if (buttonsColumn[i].innerHTML.includes("Обновить")) {
            buttonsColumn[i].parentNode.removeChild(buttonsColumn[i]);
        }
    }

    // Создаем новую рабочую книгу
    let workbook = XLSX.utils.book_new();

    // Создаем новый лист в рабочей книге
    let worksheet = XLSX.utils.table_to_sheet(dataTableCopy);

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

function searchBySurname() {
  // Получаем введенное значение из поля ввода поиска
  var searchValue = document.getElementById("searchInput").value.toLowerCase();

  // Получаем все строки таблицы с данными пациентов
  var rows = document.querySelectorAll("table tbody tr");

  // Перебираем строки таблицы и скрываем те, которые не соответствуют введенному значению по фамилии
  rows.forEach(function(row) {
    var surname = row.cells[3].textContent.toLowerCase(); // Фамилия пациента

    if (surname.includes(searchValue)) {
      row.style.display = ""; // Показываем строку, если фамилия соответствует поиску
    } else {
      row.style.display = "none"; // Скрываем строку, если фамилия не соответствует поиску
    }
  });
}

// Добавляем обработчик события ввода текста в поле поиска
document.getElementById("searchInput").addEventListener("input", searchBySurname);

