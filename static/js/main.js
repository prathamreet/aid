// Main JavaScript file for the application

// Auto-dismiss flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.bg-red-100, .bg-green-100, .bg-blue-100');
    
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'opacity 1s ease';
            message.style.opacity = '0';
            
            setTimeout(() => {
                message.remove();
            }, 1000);
        }, 5000);
    });
});