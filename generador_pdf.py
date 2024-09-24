from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = None

def divide_image_and_convert_to_pdf(image_path, num_parts):
    # Abrir la imagen
    img = Image.open(image_path)
    width, height = img.size
    
    # Calcular la altura de cada parte
    part_height = height // num_parts
    parts = []

    # Dividir la imagen en partes
    for i in range(num_parts):
        # Definir la caja de recorte para cada parte
        top = i * part_height
        bottom = (i + 1) * part_height if i < num_parts - 1 else height
        part = img.crop((0, top, width, bottom))
        
        # Guardar la parte como una imagen temporal
        part_path = f"part_{i + 1}.png"
        part.save(part_path)
        parts.append(part_path)

    # Crear un PDF a partir de las partes
    pdf_path = "salida.pdf"
    images = [Image.open(part) for part in parts]
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    
    # Limpiar archivos temporales
    for part in parts:
        os.remove(part)

    # Eliminar la imagen original si lo deseas
    #os.remove(image_path)

    print(f"PDF guardado como: {pdf_path}")

# Usar la función
image_path = "screenshot.png"  # Cambia esto a la ruta de tu imagen
num_parts = 10  # Cambia esto al número de partes que deseas
divide_image_and_convert_to_pdf(image_path, num_parts)
