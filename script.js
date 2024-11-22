// Change the background color of the page when the button is clicked
document.getElementById('colorButton').addEventListener('click', function() {
    const colors = ['#FFB6C1', '#ADD8E6', '#98FB98', '#FFFFE0', '#F0E68C'];
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    document.body.style.backgroundColor = randomColor;
});
