import os
import numpy as np
from maze_problem import MazeProblem
from search import bfs, dfs, a_star, euclidean_distance, manhattan_distance
from utils import cargar_imagen, procesar_imagen, visualizar_laberinto

GRID_SIZE = 6
IMAGE_PATH = "images"  # Carpeta donde están las imágenes

def listar_imagenes():
    """ Lista todas las imágenes disponibles en la carpeta 'images'. """
    imagenes = [f for f in os.listdir(IMAGE_PATH) if f.endswith(".bmp")]
    return imagenes

def seleccionar_imagen():
    while True:
        imagenes = listar_imagenes()
        if not imagenes:
            print("No se encontraron imágenes en la carpeta 'images'.")
            exit()

        print("\nSeleccione la imagen a analizar:")
        for i, img in enumerate(imagenes, start=1):
            print(f"{i} - {img}")
        print("0 - Salir")

        opcion = input("Opción: ")
        if opcion == "0":
            print("Saliendo del programa...")
            exit()

        try:
            opcion = int(opcion)
            if 1 <= opcion <= len(imagenes):
                return os.path.join(IMAGE_PATH, imagenes[opcion - 1])
            else:
                print("Opción inválida, intente de nuevo.")
        except ValueError:
            print("Ingrese un número válido.")

def seleccionar_algoritmo():
    while True:
        print("\nSeleccione el algoritmo:")
        print("1 - Breadth First Search (BFS)")
        print("2 - Depth First Search (DFS)")
        print("3 - A* con distancia Manhattan")
        print("4 - A* con distancia Euclidiana")
        print("0 - Volver a seleccionar imagen")

        opcion = input("Opción: ")
        if opcion == "0":
            return None  
        elif opcion in ["1", "2", "3", "4"]:
            return opcion
        else:
            print("Opción inválida, intente de nuevo.")

def main():
    """ Bucle principal para ejecutar el programa. """
    while True:

        ruta_imagen = seleccionar_imagen()
        imagen = cargar_imagen(ruta_imagen)


        matriz_laberinto, filas, columnas, start, goals = procesar_imagen(imagen, GRID_SIZE)
        maze_problem = MazeProblem(matriz_laberinto, start, goals)

        while True:

            opcion = seleccionar_algoritmo()
            if opcion is None:
                break  


            if opcion == "1":
                path1, path2 = bfs(maze_problem)
            elif opcion == "2":
                path1, path2 = dfs(maze_problem)
            elif opcion == "3":
                path1, path2 = a_star(maze_problem, manhattan_distance)
            elif opcion == "4":
                path1, path2 = a_star(maze_problem, euclidean_distance)


            visualizar_laberinto(matriz_laberinto, path1, path2)

if __name__ == "__main__":
    main()
