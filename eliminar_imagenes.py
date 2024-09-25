import os

def eliminar_imagenes_png():
    """Elimina todas las imágenes en formato PNG en la carpeta actual tras confirmación."""
    archivos_png = [archivo for archivo in os.listdir('.') if archivo.endswith('.png')]
    
    if not archivos_png:
        print("No se encontraron imágenes PNG en la carpeta actual.")
        return
    
    print("Se encontraron las siguientes imágenes PNG:")
    for archivo in archivos_png:
        print(archivo)

    confirmar = input("¿Estás seguro de que deseas eliminar estas imágenes? (Presiona Enter para confirmar): ")
    
    if confirmar == '':
        for archivo in archivos_png:
            try:
                os.remove(archivo)
                print(f"Eliminado: {archivo}")
            except Exception as e:
                print(f"No se pudo eliminar {archivo}: {e}")
    else:
        print("Eliminación cancelada.")

# Llamar a la función
eliminar_imagenes_png()
