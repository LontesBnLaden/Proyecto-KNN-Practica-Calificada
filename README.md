# Proyecto KNN

Proyecto web educativo que presenta el algoritmo de los K vecinos mas cercanos
(KNN) y dos practicas calificadas interactivas.

## Abrir el proyecto

Abre `index.html` directamente en el navegador o ejecuta desde esta carpeta:

```powershell
python -m http.server 5500
```

Luego visita `http://localhost:5500`.

## Versión Python

Instala las dependencias indicadas por el docente:

```powershell
python -m pip install -r requirements.txt
```

Ejecuta las dos prácticas con el algoritmo KNN de scikit-learn:

```powershell
python knn_practica.py --k 3
```

El parámetro `--k` acepta valores entre 1 y 7. Los resultados de las predicciones
se muestran en consola y las gráficas se guardan en la carpeta `salidas/`.

## Ejecutar la aplicación web conectada a Python

Instala todas las dependencias y inicia el servidor Flask:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Abre `http://localhost:5050`. Las predicciones realizadas desde el navegador usan
Pandas y scikit-learn en el servidor. Matplotlib genera gráficas disponibles en:

- `http://localhost:5050/api/plot/client`
- `http://localhost:5050/api/plot/investment`
