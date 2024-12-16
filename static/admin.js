function confirmDelete() {
    return confirm("Вы уверены, что хотите удалить пользователя?");
}

function searchUsers() {
    let searchValue = document.getElementById('searchInput').value.trim().toLowerCase();

    let rows = Array.from(document.querySelectorAll('#userTableBody tr'));

    rows.forEach(row => {
        let login = row.querySelector('td:nth-child(2)').textContent.trim().toLowerCase();
        if (login.includes(searchValue)) {
            row.style.display = 'table-row';
        } else {
            row.style.display = 'none';
        }
    });
}