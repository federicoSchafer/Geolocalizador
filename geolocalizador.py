# -*- coding: utf-8 -*-

from geopy.geocoders import Nominatim
import csv
import string
import sys
import os
import time

def escribirCSV(archivo, datos):
	salida = csv.writer(archivo, delimiter=';', lineterminator='\n')
	salida.writerow(datos)

provincias = {'jujuy': [-24.1945700, -65.2971200],
'salta': [-24.7859001, -65.4116592],
'formosa': [-26.1775303	-58.1781387],
'chaco': [-22.8666700, -62.9333300],
'catamarca': [-28.4695700, -65.7852400],
'tucuman': [-26.8241400, -65.2226000],
'santiago del estero': [-27.7656200, -64.3101200],
'corrientes': [-27.4667, -58.8333],
'misiones': [-23.8000000, -63.1166700],
'la rioja': [-29.4110500, -66.8506700],
'santa fe': [-31.6333300, -60.7000000],
'san juan': [-31.5375000, -68.5363900],
'cordoba': [-31.4135000, -64.1810500],
'entre rios': [-30.1146, -68.6919],
'mendoza': [-32.8908400, -68.8271700],
'san luis': [-33.2950096, -66.3356323],
'la pampa': [-36.616700, -64.2833300],
'buenos aires': [-34.6131516, -58.3772316],
'neuquen': [-38.9516100, -68.0591000],
'rio negro': [-40.8134500, -62.9966800],
'chubut': [-42.6643, -66.1881],
'santa cruz': [-51.6226082, -69.218132],
'tierra del fuego': [-54.7999992, -68.3000031]}

arch = open('proceso.csv', 'a')
archErr = open('errores.csv', 'a')
archRev = open('revision.csv', 'a')
archDatos = open('direcciones.txt', 'r')

info = input("Ingrese la provincia a procesar: ")
info = info.lower()
parametros = provincias.get(info)
if parametros is None:
	print("La provincia ingresada no se encuentra para ser procesada.")
	time.sleep(5)
	arch.close()
	archErr.close()
	archRev.close()
	archDatos.close()
	exit()
else:
	MAX_LATITUD = parametros[0]
	MAX_LONGITUD = parametros[1]
	geolocalizador = Nominatim(user_agent="my-application")
	contador = 0
	for linea in archDatos.readlines():
		linea = linea.rstrip('\n')
		linea = linea + ', ' + info
		linea = linea.upper()
		contador += 1
		print("procesando a " + linea)
		direccion = geolocalizador.geocode([linea], timeout=15)
		if direccion is None:
			datos = (contador, linea)
			escribirCSV(archErr, datos)
		else:
			latitud = direccion.latitude
			longitud = direccion.longitude
			datos = (contador, linea,latitud, longitud)
			if latitud > MAX_LATITUD or longitud > MAX_LONGITUD:
				escribirCSV(archRev, datos)
			else:
				escribirCSV(arch, datos)
	arch.close()
	archErr.close()
	archRev.close()
	archDatos.close()