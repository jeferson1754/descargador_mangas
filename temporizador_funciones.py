import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"La función {func.__name__} tardó {
              end_time - start_time:.4f} segundos en ejecutarse.")
        return result
    return wrapper

# Ejemplo de uso:


@timer
def ejemplo_funcion():
    # Simulamos una tarea que toma tiempo
    time.sleep(2)
    print("Tarea completada")


# Ejecutar la función
ejemplo_funcion()
