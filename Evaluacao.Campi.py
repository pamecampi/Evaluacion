#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 14:59:40 2025

@author: pamelita
"""

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean
import numpy as np
import calendar


# Rutas de archivos NetCDF de los meses de mayo, junio, julio y agosto.
archivos = [
    '20250529120000-REMSS-L4_GHRSST-SSTfnd-MW_IR_OI-GLOB-v02.0-fv05.1.nc',
    '20250629120000-REMSS-L4_GHRSST-SSTfnd-MW_IR_OI-GLOB-v02.0-fv05.1.nc',
    '20250729120000-REMSS-L4_GHRSST-SSTfnd-MW_IR_OI-GLOB-v02.0-fv05.1.nc',
    '20250829120000-REMSS-L4_GHRSST-SSTfnd-MW_IR_OI-GLOB-v02.0-fv05.1.nc'
]

#Para ejecutar usando pcolormesh

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes = axes.flatten()

#Abro el dataset y por medio de un bucle recorro la información buscando la variable de temperatura para seleccionarla.
#Se le resta 273 a la temperatura para pasar de °K a °C
#Del dataset, voy a seleccionar solo la región de interés, que es la costa de Brasil: lon(-60,-20), lat(-40,10)
#Se importó la librería "calendar" para poder extraer las fechas de los datasets.
#Se crea la figura con 4 subplots de 2x2 con las características especificadas y usando la escala de colores "thermal"

for i, archivo in enumerate(archivos):
    
    ds = xr.open_dataset(archivo)
    sst = ds['analysed_sst'].isel(time=0) - 273
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

# Título del gráfico en general
plt.suptitle("Comparação da SST na costa do Brasil entre maio e agosto 2025 ", fontsize=14)
plt.tight_layout()
plt.show()


#Ahora se realiza el mismo proceso pero usando contourf para generar los mapas.


# Crear figura con 4 subplots (2x2)
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
axs = axs.flatten()

for i, archivo in enumerate(archivos):
    ds = xr.open_dataset(archivo)
    sst = ds["analysed_sst"].isel(time=0) - 273
    sst_brasil = sst.sel(lon=slice(-60, -20), lat=slice(-40, 10))
    lon = sst_brasil.lon
    lat = sst_brasil.lat
    
    fecha = np.datetime_as_string(ds["time"].values[0], unit='D')
    mes_num = int(fecha[5:7])
    mes_nombre = calendar.month_name[mes_num]
 
    cf = axs[i].contourf(lon, lat, sst_brasil, levels=20, cmap=cmocean.cm.thermal)
    
    axs[i].set_title(f"SST - {mes_nombre}", fontsize=10)
    axs[i].set_xlabel("Longitud")
    axs[i].set_ylabel("Latitud")
    
    cbar = fig.colorbar(cf, ax=axs[i])
    cbar.set_label("SST (°C)")

#Título del gráfico en general
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
    
    fecha = np.datetime_as_string(ds["time"].values[0], unit='D')
    mes_num = int(fecha[5:7])
    mes_nombre = calendar.month_name[mes_num]
    
    # Graficar con contourf y escala común para todos los gráficos
    cf = axs[i].contourf(lon, lat, sst_brasil, levels=20, cmap=cmocean.cm.thermal,
                          vmin=sst_min, vmax=sst_max)
    
    axs[i].set_title(f"SST - {mes_nombre}", fontsize=10)
    axs[i].set_xlabel("Longitud")
    axs[i].set_ylabel("Latitud")
    
    # Barra de color individual (misma escala)
    cbar = fig.colorbar(cf, ax=axs[i])
    cbar.set_label("SST (°C)")
    


plt.tight_layout()
plt.suptitle("Comparação da SST na costa do Brasil entre maio e agosto 2025 ", fontsize=14, y=1.02)
plt.show()
