import cv2
import numpy as np
import matplotlib.pyplot as plt

def cargar_imagen(ruta):
    imagen = cv2.imread(ruta)
    if imagen is None:
        print(f"Error: No se pudo cargar la imagen en {ruta}")
        exit()
    return imagen

def procesar_imagen(imagen, grid_size=5):
    h, w, _ = imagen.shape
    new_h, new_w = (h // grid_size) * grid_size, (w // grid_size) * grid_size

    imagen_resized = cv2.resize(imagen, (new_w, new_h), interpolation=cv2.INTER_NEAREST)

    filas, columnas = new_h // grid_size, new_w // grid_size
    laberinto = np.zeros((filas, columnas), dtype=int)

    for i in range(filas):
        for j in range(columnas):
            bloque = imagen_resized[i * grid_size:(i + 1) * grid_size, j * grid_size:(j + 1) * grid_size]

            rojo = np.sum((bloque[:, :, 2] > 150) & (bloque[:, :, 1] < 100) & (bloque[:, :, 0] < 100))
            verde = np.sum((bloque[:, :, 1] > 150) & (bloque[:, :, 2] < 100) & (bloque[:, :, 0] < 100))
            blanco = np.sum(bloque == 255)
            negro = np.sum(bloque == 0)

            if rojo > 20:  
                laberinto[i, j] = 2  # Punto de inicio
            elif verde > 20:
                laberinto[i, j] = 3  # Meta
            elif blanco > negro:
                laberinto[i, j] = 1  # Camino libre
            else:
                laberinto[i, j] = 0  # Pared

    return laberinto, filas, columnas

def visualizar_laberinto(matriz):
    filas, columnas = matriz.shape
    img = np.zeros((filas, columnas, 3), dtype=np.uint8)
    
    for i in range(filas):
        for j in range(columnas):
            if matriz[i, j] == 0:
                img[i, j] = [0, 0, 0]  # Negro
            elif matriz[i, j] == 1:
                img[i, j] = [255, 255, 255]  # Blanco
            elif matriz[i, j] == 2:
                img[i, j] = [255, 0, 0]  # Rojo (Punto de inicio)
            elif matriz[i, j] == 3:
                img[i, j] = [0, 255, 0]  # Verde (Meta)

    plt.figure(figsize=(10, 10))
    plt.imshow(img, interpolation='nearest')

    ax = plt.gca()
    ax.set_xticks(np.arange(-0.5, columnas, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, filas, 1), minor=True)
    ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.5)

    plt.xticks(np.arange(0, columnas, 1))  
    plt.yticks(np.arange(0, filas, 1))
    
    plt.show()

ruta_imagen = "Test2.bmp"
imagen = cargar_imagen(ruta_imagen)

grid_size = 6 
matriz_laberinto, filas, columnas = procesar_imagen(imagen, grid_size)
visualizar_laberinto(matriz_laberinto)
