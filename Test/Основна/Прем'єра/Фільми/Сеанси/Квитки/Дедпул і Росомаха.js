document.addEventListener('DOMContentLoaded', () => {
    const seatsContainer = document.querySelector('.seats');
    const bookButton = document.getElementById('book-ticket');
    const layout = [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1],
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
        [0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0],
        [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
        [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0],
    ];

    layout.forEach((row, rowIndex) => {
        row.forEach((seatType, colIndex) => {
            const seat = document.createElement('div');
            seat.classList.add('seat');

            switch (seatType) {
                case 2:
                    seat.classList.add('wheelchair');
                    break;
                case 1:
                    seat.classList.add('occupied');
                    break;
                case 0:
                    seat.classList.add('empty');
                    seat.addEventListener('click', () => {
                        if (!seat.classList.contains('occupied')) {
                            seat.classList.toggle('selected');
                        }
                    });
                    break;
                default:
                    break;
            }

            // Додаємо обведення червоним кольором для нижнього рядка
            if (rowIndex === layout.length - 1) {
                seat.style.borderColor = 'red';
            }

            seatsContainer.appendChild(seat);
        });
    });

    bookButton.addEventListener('click', () => {
        const selectedSeats = document.querySelectorAll('.seat.selected');
        if (selectedSeats.length > 0) {
            alert(`Ви забронювали ${selectedSeats.length} місце(ць).`);
        } else {
            alert('Будь ласка, виберіть місце перед бронюванням.');
        }
    });
});
