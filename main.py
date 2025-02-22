import numpy as np
from maze_problem import MazeProblem
from search import bfs, dfs, a_star, euclidean_distance, manhattan_distance
from utils import cargar_imagen, procesar_imagen, visualizar_laberinto


GRID_SIZE = 6

ruta_imagen = "images/Prueba Lab1.bmp"
imagen = cargar_imagen(ruta_imagen)

matriz_laberinto, filas, columnas, start, goals = procesar_imagen(imagen, GRID_SIZE)

maze_problem = MazeProblem(matriz_laberinto, start, goals)

print("Seleccione el algoritmo:")
print("1 - Breadth First Search (BFS)")
print("2 - Depth First Search (DFS)")
print("3 - A* con distancia Manhattan")
print("4 - A* con distancia Euclidiana")

opcion = input("Opción: ")


if opcion == "1":
    path1, path2 = bfs(maze_problem)
elif opcion == "2":
    path1, path2 = dfs(maze_problem)
elif opcion == "3":
    path1, path2 = a_star(maze_problem, manhattan_distance)
elif opcion == "4":
    path1, path2 = a_star(maze_problem, euclidean_distance)
else:
    print("Opción inválida")
    exit()


visualizar_laberinto(matriz_laberinto, path1, path2)
