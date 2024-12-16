function openModal() {
    document.getElementById('myModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('myModal').style.display = 'none';
}

function openUpdateModal(clinicId) {
    document.getElementById("updateClinicId").value = clinicId;
    document.getElementById("updateModal").style.display = "block";
}

function closeUpdateModal() {

    document.getElementById('updateModal').style.display = 'none';
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

function confirmDelete() {
    return confirm("Вы уверены, что хотите удалить приём?");
}

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
        let dateText = row.cells[4].innerText; // Значение столбца "Дата приёма"
        let date = new Date(dateText);

        if (date >= startDate && date <= endDate) {
            let dateStr = date.toDateString();
            dataCount[dateStr] = (dataCount[dateStr] || 0) + 1;
        }
    });

    let dates = Object.keys(dataCount);
    let uniqueData = dates.map(date => dataCount[date]);


    console.log("Selected Dates:", dates);
    console.log("Data Counts:", uniqueData);

    if (dates.length === 0) {
        alert("Нет данных для отображения графика.");
        return;
    }

    openChartModal();

    let ctx = document.getElementById('myChart').getContext('2d');
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height); // Очищаем canvas перед построением нового графика

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dates,
            datasets: [{
                label: 'Количество приёмов',
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
                        stepSize: 1
                    }
                }
            }
        }
    });

    closeDateModal(); // Закрываем модальное окно выбора дат
}

function createChartForAllData() {
    let dataTable = document.querySelector('table');
    let rows = dataTable.querySelectorAll('tbody tr');

    let dataCount = {};

    rows.forEach(function(row) {
        let dateText = row.cells[4].innerText; // Значение столбца "Дата приёма"
        let date = new Date(dateText);
        let dateStr = date.toDateString();
        dataCount[dateStr] = (dataCount[dateStr] || 0) + 1;
    });

    let dates = Object.keys(dataCount);
    let uniqueData = dates.map(date => dataCount[date]);

    // Отладочная информация
    console.log("All Dates:", dates);
    console.log("All Data Counts:", uniqueData);

    if (dates.length === 0) {
        alert("Нет данных для отображения графика.");
        return;
    }

    openChartModal();

    let ctx = document.getElementById('myChart').getContext('2d');
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height); // Очищаем canvas перед построением нового графика

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dates,
            datasets: [{
                label: 'Количество приёмов',
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
                        stepSize: 1
                    }
                }
            }
        }
    });

    closeDateModal();
}


