
from pyswip import Prolog
import tkinter as tk
from tkinter import filedialog
from tkinter import *


ventana = Tk()
prolog = Prolog()
prolog.consult("logica.pro")
rutaArchivoLaberinto = ""
laberinto = []

def solicitarArchivo():
    global archivoLaberinto
    print ("solicitar archivo")
    rutaArchivoLaberinto = filedialog.askopenfilename()
    laberintoProlog = prolog.query("getLaberinto('%s',X)." % (rutaArchivoLaberinto))
    transformarLaberinto(laberintoProlog)

def transformarLaberinto(laberintoProlog):
    global laberinto
    for i in laberintoProlog: 
        for j in i["X"]:
            elemento = j.decode("utf-8") #transformar de byte a string
            listaEle = elemento.strip('][').split(',') #transformar de string a lista
            laberinto += [listaEle]





botonArchivo= tk.Button(ventana, text ="Archivo", command = solicitarArchivo)
botonArchivo.pack()


def verLaberinto():
    global laberinto
    print("laberinto---------------------")
    for fila in laberinto:
        print(fila)

botonVer= tk.Button(ventana, text ="ver", command = verLaberinto)
botonVer.pack()

verLaberinto()
def moverIzquierda(event):
    print("Izquierda")
def moverDerecha(event):
    print("Derecha")
def moverArriba(event):
    print("Arriba")
def moverAbajo(event):
    print("Abajo")

 
 

ventana.bind("<Left>", moverIzquierda)
ventana.bind("<Right>", moverDerecha)
ventana.bind("<Up>", moverArriba)
ventana.bind("<Down>", moverAbajo)

ventana.mainloop()