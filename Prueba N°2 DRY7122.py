import requests
import urllib.parse

def obtener_coordenadas(ciudad, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": ciudad, "limit": "1", "key": key})
    replydata = requests.get(url)
    if replydata.status_code == 200:
        json_data = replydata.json()
        if json_data['hits']:
            coordenadas = json_data['hits'][0]['point']
            return (coordenadas['lat'], coordenadas['lng'])
        else:
            print(f"No se encontraron coordenadas para {ciudad}")
            return None
    else:
        print(f"Error al obtener coordenadas: {replydata.status_code}")
        return None

def obtener_datos_viaje(origen_coords, destino_coords, key):
    route_url = "https://graphhopper.com/api/1/route?"
    url = route_url + urllib.parse.urlencode({
        "point": [f"{origen_coords[0]},{origen_coords[1]}", f"{destino_coords[0]},{destino_coords[1]}"],
        "vehicle": "car",
        "locale": "es",
        "key": key
    }, doseq=True)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al obtener datos de Graphhopper:", response.text)
        return None

def calcular_combustible(distancia_km, rendimiento_km_l):
    return distancia_km / rendimiento_km_l

def imprimir_narrativa_viaje(origen, destino, distancia, duracion_horas, combustible):
    print(f"Viaje desde {origen} hasta {destino}:")
    print(f"Distancia total: {distancia:.2f} km")
    print(f"Duración estimada: {duracion_horas:.2f} horas")
    print(f"Combustible requerido: {combustible:.2f} litros")

def main():
    key = "f03c3d0d-3202-4bc3-b434-48ab3c31f438"
    while True:
        origen = input("Ciudad de Origen (o 'q' para salir): ")
        if origen.lower() == 'q':
            break
        destino = input("Ciudad de Destino: ")
        if destino.lower() == 'q':
            break

        origen_coords = obtener_coordenadas(origen, key)
        destino_coords = obtener_coordenadas(destino, key)

        if origen_coords and destino_coords:
            datos_viaje = obtener_datos_viaje(origen_coords, destino_coords, key)
            if datos_viaje:
                try:
                    distancia_km = datos_viaje['paths'][0]['distance'] / 1000  # Convertir a kilómetros
                    duracion_ms = datos_viaje['paths'][0]['time']  # Duración en milisegundos
                    duracion_horas = duracion_ms / (1000 * 60 * 60)  # Convertir a horas

                    rendimiento_km_l = float(input("Rendimiento del vehículo (km/l): "))
                    combustible = calcular_combustible(distancia_km, rendimiento_km_l)

                    imprimir_narrativa_viaje(origen, destino, distancia_km, duracion_horas, combustible)
                except KeyError as e:
                    print(f"Error en los datos recibidos: {e}")
            else:
                print("No se pudieron obtener los datos del viaje. Intente nuevamente.")
        else:
            print("No se pudieron obtener las coordenadas de una o ambas ciudades. Intente nuevamente.")

if __name__ == "__main__":
    main()
