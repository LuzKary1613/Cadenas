import random
import pandas as pd

# INICIALIZACIÓN DE LA MATRIZ (VALORES ALEATORIOS)
def inicializar_matriz(num_grupos):
    matriz = []
    etiquetas = list(range(1, num_grupos + 1))

    # ELABORACIÓN DE LA MATRIZ
    for _ in range(num_grupos):
        fila = [round(random.uniform(0, 1), 2) for _ in range(num_grupos)]
        suma_fila = sum(fila)
        fila = [valor / suma_fila if suma_fila != 0 else 0 for valor in fila]
        matriz.append(fila)

    # ASIGNACIÓN DEL 0
    for i in range(num_grupos):
        matriz[i][i] = 0

    return matriz, etiquetas

# SIMULACIÓN DE LA BATALLA
def ataque(matriz, guerreros, etiquetas, archivo):
    grupos_vivos = len(guerreros)

    while grupos_vivos > 1:
        grupo_atacante = random.choice(etiquetas)
        grupo_atacado = random.choice(etiquetas)

        # VERIFICACIÓN DE QUE EL GRUPO ATACANTE ES DIFERENTE AL GRUPO ATACADO
        while grupo_atacado == grupo_atacante:
            grupo_atacado = random.choice(etiquetas)

        archivo.write(f"Grupo {grupo_atacante} ataca al Grupo {grupo_atacado}\n")

        # ELIMINACIÓN DE LOS GUERREROS
        guerreros[etiquetas.index(grupo_atacado)] -= 1

        if guerreros[etiquetas.index(grupo_atacado)] == 0:
            archivo.write(f"Grupo {grupo_atacado} ha sido eliminado\n")
            index_eliminado = etiquetas.index(grupo_atacado)
            guerreros.pop(index_eliminado)
            etiquetas.pop(index_eliminado)

            matriz, etiquetas = reconfigurar_matriz(matriz, index_eliminado, etiquetas, archivo)
            grupos_vivos -= 1

        archivo.write(f"Cantidad de guerreros actualizada {guerreros}\n\n")

    return guerreros, matriz

# RECONFIGURACIÓN DE LA MATRIZ DESPUÉS DE LA ELIMINACIÓN DEL GRUPO PERDEDOR
def reconfigurar_matriz(matriz, index_eliminado, etiquetas, archivo):
    for i in range(len(matriz)):
        matriz[i].pop(index_eliminado)
    matriz.pop(index_eliminado)

    for i in range(len(matriz)):
        suma_fila = sum(matriz[i])
        matriz[i] = [valor / suma_fila if suma_fila != 0 else 0 for valor in matriz[i]]
        matriz[i][i] = 0

    archivo.write("\nNueva matriz:\n")
    mostrar_matriz_en_tabla(matriz, etiquetas, archivo)
    archivo.write("\n")

    return matriz, etiquetas

# TABLA DE LA MATRIZ
def mostrar_matriz_en_tabla(matriz, etiquetas, archivo):
    df = pd.DataFrame(matriz, index=etiquetas, columns=etiquetas)
    archivo.write(df.to_string() + "\n")

# REESCRIPCIÓN DE LA INFORMACIÓN DEL ARCHIVO "output-1.txt" 
def escribir_archivo(matriz, guerreros, etiquetas):
    with open("C:/Users/Luz Karen/Desktop/output-1.txt", "w") as archivo:
        archivo.write("Matriz inicial:\n")
        mostrar_matriz_en_tabla(matriz, etiquetas, archivo)
        archivo.write("\nCantidad de guerreros por grupo: ")
        archivo.write(f"{guerreros}\n")
        archivo.write("\nResultados de la batalla:\n")

# OBTENCIÓN DE LA CANTIDAD DE GRUPOS Y GUERREROS
num_grupos = int(input("Ingrese la cantidad de grupos: "))
guerreros = [int(input(f"Ingrese la cantidad de guerreros para el Grupo {i + 1}: ")) for i in range(num_grupos)]

# INICIALIZO DE LA MATRIZ Y REESCRIPCIÓN DE LA INFORMACIÓN INICIAL
matriz, etiquetas = inicializar_matriz(num_grupos)
escribir_archivo(matriz, guerreros, etiquetas)

# SIMULACIÓN Y RESULTADOS
with open("C:/Users/Luz Karen/Desktop/output-1.txt", "a") as archivo:
    guerreros_finales, matriz_final = ataque(matriz, guerreros, etiquetas, archivo)
    ganador = etiquetas[0]  # Último grupo sobreviviente
    archivo.write(f"El grupo ganador es el Grupo {ganador}")

print("\nSimulación lista, los resultados estan en output-1.txt")
