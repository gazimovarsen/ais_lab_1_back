function returnToHome() {
    // Скрываем секцию тестов и очищаем вопросы
    const testContainer = document.getElementById('test-container');
    testContainer.style.display = 'none';
    document.getElementById('questions').innerHTML = '';

    // Скрываем секцию результатов
    document.getElementById('results').style.display = 'none';

    // Показываем секцию выбора уровня
    const levelSelection = document.getElementById('level-selection');
    levelSelection.style.display = 'flex';
}


const buttons = document.querySelectorAll('#level-selection button');
buttons.forEach(button => {
    button.style.margin = '0 auto'; // Центрируем кнопки
    button.style.display = 'block'; // Убеждаемся, что кнопки ведут себя как блочные элементы
});


document.getElementById('return-home-btn').addEventListener('click', returnToHome);


