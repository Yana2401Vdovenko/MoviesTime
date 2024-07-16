document.getElementById('ticketForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const cardNumber = document.getElementById('cardNumber').value;
    const password = document.getElementById('password').value;
    const cvv = document.getElementById('cvv').value;
    const fullName = document.getElementById('fullName').value;

    if (cardNumber && password && cvv && fullName) {
        alert('Ваш квиток замовлено успішно!');
    } else {
        alert('Будь ласка, заповніть всі поля.');
    }
});
