document.querySelectorAll('.message-close-btn').forEach(button => {
    button.addEventListener('click', function() {
        this.parentElement.style.display = 'none';
    });
});