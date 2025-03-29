import heapq

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

inicio_tm = "San Mateo - C.C. Unisur"
fin_tm = "Portal Eldorado - Centro Comercial Nuestro Bogotá"

tiempo_total_tm, ruta_tm = dijkstra_transferencias(rutas_tm, reglas_transferencia_tm, inicio_tm, fin_tm)

# Tiempos de viaje en vehículo por tramo
tiempo_autopista_sur = 35
tiempo_avenida_68 = 28
tiempo_avenida_eldorado = 22

tiempo_vehiculo_minutos = tiempo_autopista_sur + tiempo_avenida_68 + tiempo_avenida_eldorado

if tiempo_total_tm == float('inf'):
    print("No se encontró una ruta en Transmilenio.")
else:
    print(f"Tiempo en Transmilenio: {tiempo_total_tm} minutos")
    print(f"Ruta en Transmilenio: {' -> '.join(ruta_tm)}")
    print(f"Tiempo en vehículo: {tiempo_vehiculo_minutos} minutos")
    print(f"Ruta en vehículo:")
    print(f"  - Autopista Sur: {tiempo_autopista_sur} minutos")
    print(f"  - Avenida 68: {tiempo_avenida_68} minutos")
    print(f"  - Avenida El Dorado: {tiempo_avenida_eldorado} minutos")

    if tiempo_total_tm < tiempo_vehiculo_minutos:
        print("Transmilenio es más rápido.")
        print("La mejor opción para llegar a tu destino es Transmilenio.")
    elif tiempo_total_tm > tiempo_vehiculo_minutos:
        print("El vehículo es más rápido.")
        print("La mejor opción para llegar a tu destino es el vehículo.")
    else:
        print("Ambos medios de transporte tardan aproximadamente lo mismo.")