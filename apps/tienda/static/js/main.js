document.addEventListener('DOMContentLoaded', function () {
    var messagesContainer = document.getElementById('messages-container');
    if (messagesContainer) {
        var messages = messagesContainer.querySelectorAll('.message');
        messages.forEach(function (msg) {
            if (msg.textContent.trim().indexOf('ACCION_VACIADO_EXITOSA') !== -1) {
                msg.textContent = 'Carrito vaciado exitosamente.';
                msg.style.borderColor = '#1A1A1A';
                msg.style.color = '#1A1A1A';
            }
            setTimeout(function () {
                msg.style.opacity = '0';
                msg.style.transition = 'opacity 0.5s ease';
                setTimeout(function () {
                    msg.remove();
                }, 500);
            }, 4000);
        });
    }
});
