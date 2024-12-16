async function fetchMedicalNews() {
    const apiKey = '21473258f2464d6ab2647a656c898351';
    const url = `https://newsapi.org/v2/everything?q=medicine&language=ru&apiKey=${apiKey}`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const newsContainer = document.getElementById('news-container');

        newsContainer.innerHTML = '';

        data.articles.forEach(article => {
            const item = document.createElement('div');
            item.className = 'news-item';
            item.innerHTML = `
                <h5>${article.title}</h5>
                <p>${article.description || 'Описание отсутствует'}</p>
                <a href="${article.url}" class="btn" target="_blank">Читать далее</a>
            `;
            newsContainer.appendChild(item);
        });
    } catch (error) {
        console.error('Ошибка при получении новостей:', error);
    }
}

fetchMedicalNews();