import heapq
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

rutas_tm = {
    "San Mateo - C.C. Unisur": {"Terreros - Hospital Cardiovascular": {"tiempo": 5, "linea": "NQS"}},
    "Terreros - Hospital Cardiovascular": {"León XIII": {"tiempo": 3, "linea": "NQS"}, "San Mateo - C.C. Unisur": {"tiempo": 5, "linea": "NQS"}},
    "León XIII": {"La Despensa": {"tiempo": 4, "linea": "NQS"}, "Terreros - Hospital Cardiovascular": {"tiempo": 3, "linea": "NQS"}},
    "La Despensa": {"Venecia": {"tiempo": 6, "linea": "NQS"}, "León XIII": {"tiempo": 4, "linea": "NQS"}},
    "Venecia": {"General Santander": {"tiempo": 5, "linea": "NQS"}, "La Despensa": {"tiempo": 6, "linea": "NQS"}},
    "General Santander": {"Ricaurte": {"tiempo": 7, "linea": "NQS"}, "Venecia": {"tiempo": 5, "linea": "NQS"}},
    "Ricaurte": {"Cad": {"tiempo": 8, "linea": "NQS"}, "General Santander": {"tiempo": 7, "linea": "NQS"}},
    "Cad": {"Corferias": {"tiempo": 6, "linea": "NQS"}, "Ricaurte": {"tiempo": 8, "linea": "NQS"}},
    "Corferias": {"Quinta Paredes": {"tiempo": 4, "linea": "NQS"}, "Cad": {"tiempo": 6, "linea": "NQS"}},
    "Quinta Paredes": {"Gobernación": {"tiempo": 3, "linea": "NQS"}, "Corferias": {"tiempo": 4, "linea": "NQS"}},
    "Gobernación": {"Salitre - El Greco": {"tiempo": 5, "linea": "NQS"}, "Quinta Paredes": {"tiempo": 3, "linea": "NQS"}},
    "Salitre - El Greco": {"El Tiempo - Cámara De Comercio De Bogotá": {"tiempo": 4, "linea": "NQS"}, "Gobernación": {"tiempo": 5, "linea": "NQS"}},
    "El Tiempo - Cámara De Comercio De Bogotá": {"Normandía": {"tiempo": 6, "linea": "NQS"}, "Salitre - El Greco": {"tiempo": 4, "linea": "NQS"}},
    "Normandía": {"Modelia": {"tiempo": 5, "linea": "NQS"}, "El Tiempo - Cámara De Comercio De Bogotá": {"tiempo": 6, "linea": "NQS"}},
    "Modelia": {"Portal Eldorado - Centro Comercial Nuestro Bogotá": {"tiempo": 7, "linea": "NQS"}, "Normandía": {"tiempo": 5, "linea": "NQS"}},
    "Portal Eldorado - Centro Comercial Nuestro Bogotá": {"Modelia": {"tiempo": 7, "linea": "NQS"}}
}

reglas_transferencia_tm = {}

def dijkstra_transferencias(rutas, reglas_transferencia, inicio, fin):
    tiempos = {estacion: float('inf') for estacion in rutas}
    tiempos[inicio] = 0
    cola_prioridad = [(0, inicio, [])]
    visitados = set()

    while cola_prioridad:
        tiempo_actual, estacion_actual, ruta_actual = heapq.heappop(cola_prioridad)

        if estacion_actual in visitados:
            continue
        visitados.add(estacion_actual)

        if estacion_actual == fin:
            return tiempo_actual, ruta_actual + [estacion_actual]

        for vecino, info in rutas[estacion_actual].items():
            tiempo_vecino = tiempo_actual + info["tiempo"]
            linea_actual = rutas[ruta_actual[-1]][vecino]["linea"] if ruta_actual and ruta_actual[-1] in rutas and vecino in rutas[ruta_actual[-1]] else None
            linea_vecino = info["linea"]

            if linea_actual and linea_actual != linea_vecino:
                tiempo_vecino += reglas_transferencia.get((linea_actual, linea_vecino), {}).get("tiempo_espera", 0)

            if tiempo_vecino < tiempos[vecino]:
                tiempos[vecino] = tiempo_vecino
                heapq.heappush(cola_prioridad, (tiempo_vecino, vecino, ruta_actual + [estacion_actual]))

    return float('inf'), []

# Tiempos de viaje en vehículo por tramo
tiempo_autopista_sur = 35
tiempo_avenida_68 = 28
tiempo_avenida_eldorado = 22

# Generar datos para el modelo
data = []
estaciones = list(rutas_tm.keys())
num_rutas = 500  # Aumentamos a 500 rutas

for _ in range(num_rutas):
    inicio_tm = random.choice(estaciones)
    fin_tm = random.choice(estaciones)
    tiempo_total_tm, ruta_tm = dijkstra_transferencias(rutas_tm, reglas_transferencia_tm, inicio_tm, fin_tm)

    if tiempo_total_tm != float('inf'):
        # Variación aleatoria en el tiempo de vehículo
        variacion_vehiculo = np.random.normal(0, 10)  # Variación normal con media 0 y desviación estándar 10
        tiempo_vehiculo_minutos = tiempo_autopista_sur + tiempo_avenida_68 + tiempo_avenida_eldorado + variacion_vehiculo

        if tiempo_total_tm < tiempo_vehiculo_minutos:
            medio_rapido = "Transmilenio"
        elif tiempo_total_tm > tiempo_vehiculo_minutos:
            medio_rapido = "Vehiculo"
        else:
            medio_rapido = "Empate"

        data.append({
            "tiempo_tm": tiempo_total_tm,
            "tiempo_vehiculo": tiempo_vehiculo_minutos,
            "medio_rapido": medio_rapido
        })

df = pd.DataFrame(data)

# Preprocesamiento: Escalar los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[["tiempo_tm", "tiempo_vehiculo"]])

# Aplicar K-Means
kmeans = KMeans(n_clusters=3, random_state=42)  # Elegimos 3 clusters arbitrariamente
df["cluster"] = kmeans.fit_predict(X_scaled)

# Visualización de los clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(x="tiempo_tm", y="tiempo_vehiculo", hue="cluster", data=df, palette="viridis")
plt.title("Clusters de tiempos de Transmilenio vs. Vehículo")
plt.xlabel("Tiempo Transmilenio (minutos)")
plt.ylabel("Tiempo Vehículo (minutos)")
plt.show()

# Análisis de los clusters
print(df.groupby("cluster")[["tiempo_tm", "tiempo_vehiculo"]].mean())
print(df["cluster"].value_counts())