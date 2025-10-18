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

## 🧰 Requisitos

Antes de ejecutar el script, asegúrate de tener instaladas las siguientes librerías de Python:

```bash
pip install xarray matplotlib cartopy cmocean netCDF4 numpy

# Evaluacion
Código sobre SST en la costa de Brasil
Aquí voy a desarrollar el código para generar los mapas de temperatura superfial del mar en 4 días de los meses de mayo, junio, julio y agosto de 2025.

#importar las librerías necesarias para el ejercicio:

import xarray as xr  
import matplotlib.pyplot as plt  
import cartopy.crs as ccrs  
import cartopy.feature as cfeature  
import cmocean  
import numpy as np  
import calendar  

# Rutas de los archivos descargados guardados en mi computadora (fechas del día 29 de los meses de mayo, junio, julio y agosto del 2025)
archivos = [
    '20250529120000-REMSS-L4_GHRSST-SSTfnd-MW_IR_OI-GLOB-v02.0-fv05.1.nc',
    '20250629120000-REMSS-L4_GHRSST-SSTfnd-MW_IR_OI-GLOB-v02.0-fv05.1.nc',
    '20250729120000-REMSS-L4_GHRSST-SSTfnd-MW_IR_OI-GLOB-v02.0-fv05.1.nc',
    '20250829120000-REMSS-L4_GHRSST-SSTfnd-MW_IR_OI-GLOB-v02.0-fv05.1.nc'
]  

###Para ejecutar usando pcolormesh  
fig, axes = plt.subplots(2, 2, figsize=(12, 8))  
axes = axes.flatten()  


for i, archivo in enumerate(archivos):
    ds = xr.open_dataset(archivo)
    sst = ds['analysed_sst'].isel(time=0) - 273.15
    sst_brasil = sst.sel(lon=slice(-60, -20), lat=slice(-40, 10))
    lon = sst_brasil.lon
    lat = sst_brasil.lat
    fecha = np.datetime_as_string(ds["time"].values[0], unit='D')
    mes_num = int(fecha[5:7])
    mes_nombre = calendar.month_name[mes_num]
    im = axes[i].pcolormesh(lon, lat, sst_brasil, cmap=cmocean.cm.thermal)
    axes[i].set_title(f"SST {archivo[0:8]}", fontsize=10) 
    axes[i].set_xlabel("Longitud")
    axes[i].set_ylabel("Latitud")
    cbar = plt.colorbar(im, ax=axes[i])
    cbar.set_label("SST (°C)")

# Título general
plt.suptitle("Comparação da SST na costa do Brasil entre maio e agosto 2025 ", fontsize=14)
plt.tight_layout()
plt.show()

#Ahora ejecuto usando contourf

# Crear figura con 4 subplots (2x2)
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
axs = axs.flatten()

for i, archivo in enumerate(archivos):
    ds = xr.open_dataset(archivo)
    sst = ds["analysed_sst"].isel(time=0) - 273.15 
    sst_brasil = sst.sel(lon=slice(-60, -20), lat=slice(-40, 10))
    lon = sst_brasil.lon
    lat = sst_brasil.lat
    fecha = np.datetime_as_string(ds["time"].values[0], unit='D')
    mes_num = int(fecha[5:7])
    mes_nombre = calendar.month_name[mes_num]
    
    # Graficar con contourf
    cf = axs[i].contourf(lon, lat, sst_brasil, levels=20, cmap=cmocean.cm.thermal)
    
    axs[i].set_title(f"SST - {mes_nombre}", fontsize=10)
    axs[i].set_xlabel("Longitud")
    axs[i].set_ylabel("Latitud")
    
    # Barra de color individual
    cbar = fig.colorbar(cf, ax=axs[i])
    cbar.set_label("SST (°C)")

plt.tight_layout()
plt.suptitle("Comparação da SST na costa do Brasil entre maio e agosto 2025 ", fontsize=14, y=1.02)
plt.show()

#Ahora generando una sola barra de color para comparar temperaturas
sst_min = np.inf
sst_max = -np.inf

for archivo in archivos:
    ds = xr.open_dataset(archivo)
    sst = ds["analysed_sst"].isel(time=0) - 273.15  # °C
    sst_brasil = sst.sel(lon=slice(-60, -20), lat=slice(-40, 10))
    sst_min = min(sst_min, float(sst_brasil.min()))
    sst_max = max(sst_max, float(sst_brasil.max()))

print(f"Escala común SST: {sst_min:.2f}°C a {sst_max:.2f}°C")

#Crear figura con 4 subplots (2x2)
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
axs = axs.flatten()

for i, archivo in enumerate(archivos):
    ds = xr.open_dataset(archivo)
    sst = ds["analysed_sst"].isel(time=0) - 273.15
    sst_brasil = sst.sel(lon=slice(-60, -20), lat=slice(-40, 10))
    lon = sst_brasil.lon
    lat = sst_brasil.lat
    
    # Obtener el mes desde la variable time
    fecha = np.datetime_as_string(ds["time"].values[0], unit='D')
    mes_num = int(fecha[5:7])
    mes_nombre = calendar.month_name[mes_num]  # inglés
    # Si quieres en español, usa: meses = ["enero","febrero",...]; mes_nombre = meses[mes_num-1]
    
    # Graficar con contourf y escala común
    cf = axs[i].contourf(lon, lat, sst_brasil, levels=20, cmap=cmocean.cm.thermal,
                          vmin=sst_min, vmax=sst_max)
    
    axs[i].set_title(f"SST - {mes_nombre}", fontsize=10)
    axs[i].set_xlabel("Longitud")
    axs[i].set_ylabel("Latitud")
    
    # Barra de color individual (misma escala)
    cbar = fig.colorbar(cf, ax=axs[i])
    cbar.set_label("SST (°C)")

plt.tight_layout()
plt.suptitle("Comparación de SST en la costa de Brasil (4 fechas diferentes)", fontsize=14, y=1.02)
plt.show()



