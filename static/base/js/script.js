// Check if the django message exists
const messageElement = document.getElementById('django-message');

if (messageElement) {
    // Set a timeout to hide the message after 30 seconds (30000ms)
    setTimeout(() => {
        messageElement.style.display = 'none'; // Hide the message
    }, 10000); // 10 seconds
}