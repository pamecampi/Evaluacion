# Temperatura Superficial del Mar (SST) en la Costa de Brasil

Este repositorio contiene un script en **Python** que procesa archivos **NetCDF** con datos de temperatura superficial del mar (SST) provenientes del producto **GHRSST – REMSS L4**.  
El objetivo es realiar ejercicios de generación de mapas comparativos de SST en la costa de Brasil para los meses de mayo, junio, julio y agosto del año 2025.

---

## Descripción del ejercicio

El código realiza los siguientes pasos:

1. Abre múltiples archivos `.nc` correspondiente al día 29 de los meses entre mayo a agosto de 2025.  
2. Extrae la variable `analysed_sst` de cada uno de los datasets y convierte la temperatura de **Kelvin a grados Celsius (°C)**.  
3. Selecciona la región de interés que cubre la costa de **Brasil** (longitudes de `-60°` a `-20°`, latitudes de `-40°` a `10°`).  
4. Genera mapas usando: 
   - `pcolormesh` : para representar la distribución espacial de SST.
   - `contourf` : para representar isolíneas de temperatura.
5. Crea mapas comparativos en una cuadrícula 2x2 con barras de color y escala térmica uniforme.

---

Escribir sobre las librerías que usa.
Por qué usar pcolormesh y por qué contourf
Por qué no se saca el promedio y sólo la comparación entre días
Hacer el pequeño análisis de las diferencias de las temperaturas tomando como referencia las noticas que circulaban en Brasil durante esos meses.





