import numpy as np
from maze_problem import MazeProblem
from search import bfs
from utils import cargar_imagen, procesar_imagen, visualizar_laberinto

GRID_SIZE = 6

ruta_imagen = "images/Test.bmp"
imagen = cargar_imagen(ruta_imagen)

matriz_laberinto, filas, columnas = procesar_imagen(imagen, GRID_SIZE)
maze_problem = MazeProblem(matriz_laberinto)

path = bfs(maze_problem)
print("Matriz del laberinto:")
print(np.array(matriz_laberinto))
visualizar_laberinto(matriz_laberinto, path)

