function showSchedule(day) {
    // Знайти всі кнопки
    var buttons = document.querySelectorAll('.day-selection button');
    
    // Перебрати кожну кнопку
    buttons.forEach(function(button) {
        // Зняти клас active-button з усіх кнопок і active-text з усіх текстів поруч
        button.classList.remove('active-button');
        var buttonText = button.querySelector('span');
        if (buttonText) {
            buttonText.classList.remove('active-text');
        }
    });

    // Додати клас active-button до натиснутої кнопки і active-text до тексту поруч
    var clickedButton = event.target.closest('button');
    clickedButton.classList.add('active-button');
    var clickedButtonText = clickedButton.querySelector('span');
    if (clickedButtonText) {
        clickedButtonText.classList.add('active-text');
    }

    // Показати або приховати розклад відповідно до вибору дня
    var schedules = document.querySelectorAll('.movie-schedule');
    schedules.forEach(function(schedule) {
        schedule.style.display = 'none';
    });

    // Показати вибраний розклад
    document.getElementById('schedule-' + day).style.display = 'block';
}
