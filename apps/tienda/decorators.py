from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.core.cache import cache
import time


def rate_limit(max_attempts=5, window=300):
    """
    Limitador de tasa para endpoints de autenticación.
    Permite max_attempts intentos en una ventana de `window` segundos.
    Si se excede, redirige con mensaje de error.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method == 'POST':
                ip = request.META.get('REMOTE_ADDR', 'unknown')
                cache_key = f'rate_limit_{ip}'
                now = time.time()
                attempts = cache.get(cache_key, [])
                attempts = [t for t in attempts if now - t < window]
                if len(attempts) >= max_attempts:
                    messages.error(
                        request,
                        'Demasiados intentos. Espera 5 minutos antes de intentar de nuevo.'
                    )
                    return redirect(request.path)
                attempts.append(now)
                cache.set(cache_key, attempts, window)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
