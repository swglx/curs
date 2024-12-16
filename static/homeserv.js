function openModal() {
    document.getElementById('myModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('myModal').style.display = 'none';
    resetForm(); // Reset the form after closing
}

function openDateModal() {
    document.getElementById('dateModal').style.display = 'block';
}

function closeDateModal() {
    document.getElementById('dateModal').style.display = 'none';
}

function openChartModal() {
    document.getElementById('chartModal').style.display = 'block';
}

function closeChartModal() {
    document.getElementById('chartModal').style.display = 'none';
}

function resetForm() {
    document.getElementById('myModal').querySelector('form').reset();
}

function confirmDelete() {
    return confirm("Вы уверены, что хотите удалить приём?");
}

// Преобразование таблицы в формат Excel
function exportToExcel() {
    let dataTable = document.querySelector('table');

    let workbook = XLSX.utils.book_new();
    let worksheet = XLSX.utils.table_to_sheet(dataTable);
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Данные');

    let excelData = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
    let blob = new Blob([excelData], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    let a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'data.xlsx';
    a.click();
}

function createChartWithDate() {
    let startDate = new Date(document.getElementById('startDate').value);
    let endDate = new Date(document.getElementById('endDate').value);

    let dataTable = document.querySelector('table');
    let rows = dataTable.querySelectorAll('tbody tr');

    let dataCount = {};

    rows.forEach(function(row) {
        let date = new Date(row.cells[3].innerText); // Значение столбца "Дата приёма"

        if (date >= startDate && date <= endDate) {
            if (dataCount[date.toDateString()]) {
                dataCount[date.toDateString()]++;
            } else {
                dataCount[date.toDateString()] = 1;
            }
        }
    });

    let dates = [];
    let uniqueData = [];
    for (let date in dataCount) {
        dates.push(date);
        uniqueData.push(dataCount[date]);
    }

    // Открываем модальное окно для графика
    openChartModal();

    let canvas = document.getElementById('myChart');
    if (canvas) {
        let ctx = canvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Количество приёмов на дому',
                    data: uniqueData,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1 // Устанавливаем шаг на оси Y равным 1
                        }
                    }
                }
            }
        });
    }

    closeDateModal(); // Закрываем модальное окно выбора дат
}

function createChartForAllData() {
    let dataTable = document.querySelector('table');
    let rows = dataTable.querySelectorAll('tbody tr');

    let dataCount = {};

    rows.forEach(function(row) {
        let date = new Date(row.cells[3].innerText); // Значение столбца "Дата приёма"
        if (dataCount[date.toDateString()]) {
            dataCount[date.toDateString()]++;
        } else {
            dataCount[date.toDateString()] = 1;
        }
    });

    let dates = [];
    let uniqueData = [];
    for (let date in dataCount) {
        dates.push(date);
        uniqueData.push(dataCount[date]);
    }

    // Открываем модальное окно для графика
    openChartModal();

    let canvas = document.getElementById('myChart');
    if (canvas) {
        let ctx = canvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Количество приёмов на дому',
                    data: uniqueData,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1 // Устанавливаем шаг на оси Y равным 1
                        }
                    }
                }
            }
        });
    }

    closeDateModal(); // Закрываем модальное окно выбора дат
}