document.addEventListener('DOMContentLoaded', function () {
    var messagesContainer = document.getElementById('messages-container');
    if (messagesContainer) {
        var alerts = messagesContainer.querySelectorAll('.alert');
        alerts.forEach(function (alert) {
            var textEl = alert.querySelector('i') ? alert.nextSibling : alert;
            var text = alert.textContent || alert.innerText;
            if (text.indexOf('ACCION_VACIADO_EXITOSA') !== -1) {
                alert.classList.remove('alert-success');
                alert.classList.add('alert-success');
                var icon = alert.querySelector('i');
                if (icon) icon.className = 'bi bi-check-circle-fill me-2';
                alert.innerHTML = '<i class="bi bi-check-circle-fill me-2"></i>Carrito vaciado exitosamente.<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
            }
            setTimeout(function () {
                var bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        });
    }
});
