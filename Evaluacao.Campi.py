#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 14:59:40 2025

@author: pamelita
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean
import calendar

# Lista de archivos en formato NetCDF correspondientes al día 29 de los meses mayo, junio, julio  y agosto.
archivos = [
    "20250501120000-REMSS-L4_GHRSST-SSTfnd-MW_IR_OI-GLOB-v02.0-fv05.1.nc",
    "20250601120000-REMSS-L4_GHRSST-SSTfnd-MW_IR_OI-GLOB-v02.0-fv05.1.nc",
    "20250701120000-REMSS-L4_GHRSST-SSTfnd-MW_IR_OI-GLOB-v02.0-fv05.1.nc",
    "20250801120000-REMSS-L4_GHRSST-SSTfnd-MW_IR_OI-GLOB-v02.0-fv05.1.nc"
]

# Como quiero crear 4 gráficos con diferentes valores de temperatura, necesito que todos los gráficos estén dentro de la misma escala.
#Por esa razón voy a extraer los valores mínimos y máximos de temperatura para poder hacer una sola escala en °C. 
#Es necesario hacer un filtrado de los datos para trabajar sólo con la zona de interés que corresponde a la costa de Brasil. 
sst_min, sst_max = np.inf, -np.inf
for archivo in archivos:
    ds = xr.open_dataset(archivo)
    sst = ds["analysed_sst"].isel(time=0) - 273
    sst_brasil = sst.sel(lon=slice(-60, -20), lat=slice(-40, 10))
    sst_min = min(sst_min, float(sst_brasil.min()))
    sst_max = max(sst_max, float(sst_brasil.max()))

# Ahora se crea la figura que es un subplot de 2x2 y se ajusta el tamñana de la figura a conveniencia. 
#Como las coordenadas del dataset son geográficas, quiero que las muestre de esa manera, por eso usaré la proyección PlateCarree.
fig, axs = plt.subplots(2, 2, figsize=(6, 8),
                        subplot_kw={'projection': ccrs.PlateCarree()})
axs = axs.flatten() #esto es solo para que se pueda recorrer los gráficos por medio del bucle.

# Graficar cada mapa
for i, archivo in enumerate(archivos):
    ds = xr.open_dataset(archivo)
    sst = ds["analysed_sst"].isel(time=0) - 273
    sst_brasil = sst.sel(lon=slice(-60, -20), lat=slice(-40, 10))
    lon = sst_brasil.lon
    lat = sst_brasil.lat

    fecha = np.datetime_as_string(ds["time"].values[0], unit='D')
    mes_nombre = calendar.month_name[int(fecha[5:7])]

    # Aplicando las funciones de las librerías importadas para agrefar características de contorno de tierra y las líneas de costa.
    axs[i].add_feature(cfeature.LAND, color='lightgrey')
    axs[i].coastlines(color='black', linewidth=1)
    axs[i].add_feature(cfeature.LAKES, facecolor='white', edgecolor='gray')
    axs[i].add_feature(cfeature.RIVERS, linewidth=0.3, edgecolor='blue')
    gl = axs[i].gridlines(draw_labels=True, linewidth=0.5, color='grey', linestyle='-.')
    gl.top_labels = False 
    gl.right_labels = False

    # Para el mapa de temperatura donde se marcan las isolíneas.
    cf = axs[i].contourf(lon, lat, sst_brasil, levels=20,
                         cmap=cmocean.cm.thermal, vmin=sst_min, vmax=sst_max)

    axs[i].set_title(f"SST - {mes_nombre}", fontsize=10)
    axs[i].set_extent([-60, -20, -40, 10])
    axs[i].set_xlabel("Longitud")
    axs[i].set_ylabel("Latitud")

# Ajustar espaciado
plt.subplots_adjust(bottom=0.15, top=0.9, wspace=0.25, hspace=0.25)

# Esto es solo para generar una sola barra de color para todo el gráfico en orientación horizontal.
cbar_ax = fig.add_axes([0.25, 0.08, 0.5, 0.02])  # [x, y, ancho, alto]
cbar = fig.colorbar(cf, cax=cbar_ax, orientation='horizontal')
cbar.set_label("SST (°C)")

# Título del gráfico generado
fig.suptitle("Comparação da SST na costa do Brasil (Maio–Agosto 2025)", fontsize=14)

plt.show()

































