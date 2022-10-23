
from glob import glob
from turtle import pos
from pyswip import Prolog
import tkinter as tk
from tkinter import filedialog
from tkinter import *

from tabulate import tabulate


ventana = Tk()
prolog = Prolog()
prolog.consult("logica.pro")

rutaArchivoLaberinto = ""
laberinto = []

posX = 0
posY = 0
fichaAnterior = "i"

def solicitarArchivo():
    global archivoLaberinto
    print ("solicitar archivo")
    #rutaArchivoLaberinto = filedialog.askopenfilename()
    #laberintoProlog = prolog.query("getLaberinto('%s',X)." % (rutaArchivoLaberinto))
    laberintoProlog = prolog.query("getLaberinto('laberinto1.txt',X).")
    transformarLaberinto(laberintoProlog)
    obtenerPosicionInicial()
    verLaberinto()

def transformarLaberinto(laberintoProlog):
    global laberinto
    for i in laberintoProlog: 
        for j in i["X"]:
            elemento = j.decode("utf-8") #transformar de byte a string
            listaEle = elemento.strip('][').split(',') #transformar de string a lista
            laberinto += [listaEle]

def obtenerPosicionInicial():
    global laberinto, posX, posY
    x = 0
    y = 0
    for i in laberinto:
        for j in i:
            if j == 'i':
                posX = x
                posY = y
                laberinto[posX][posY]="O"
            y+=1
        x+=1
        y=0
    print("x= ",posX," y= ",posY)



botonArchivo= tk.Button(ventana, text ="Archivo", command = solicitarArchivo)
botonArchivo.pack()

def verificarGane():
    if fichaAnterior =="f":
        print("Ganó")

def verLaberinto():
    global laberinto
    print("laberinto---------------------")
    print(tabulate(laberinto, tablefmt="grid"))
    verificarGane()

botonVer= tk.Button(ventana, text ="ver", command = verLaberinto)
botonVer.pack()

verLaberinto()
def moverIzquierda(event):
    global posX, posY,fichaAnterior
    print("Movimiento: Izquirda\n")
    print("actual: ",fichaAnterior,"\tsiguiente: ",laberinto[posX][posY-1])
    movimientoValido = bool(list(prolog.query("permiteMovimiento(%s,a,%s)."%(fichaAnterior, laberinto[posX][posY-1]))))
    print(movimientoValido)
    if posY-1 >= 0 and movimientoValido:
        fichaTemp = fichaAnterior
        fichaAnterior = laberinto[posX][posY-1]
        laberinto[posX][posY] = fichaTemp
        laberinto[posX][posY-1] = 'O'
        posY-=1
    verLaberinto()

def moverDerecha(event):
    global posX, posY,fichaAnterior
    print("Movimiento: Derecha\n")
    print("actual: ",fichaAnterior,"\tsiguiente: ",laberinto[posX][posY+1])
    movimientoValido = bool(list(prolog.query("permiteMovimiento(%s,d,%s)."%(fichaAnterior, laberinto[posX][posY+1]))))
    print(movimientoValido)
    if posY+1 < len(laberinto[posX]) and movimientoValido:
        fichaTemp = fichaAnterior
        fichaAnterior = laberinto[posX][posY+1]
        laberinto[posX][posY] = fichaTemp
        laberinto[posX][posY+1] = 'O'
        posY+=1
    verLaberinto()

def moverArriba(event):
    global posX, posY,fichaAnterior
    print("Movimiento: Arriba\n")
    print("actual: ",fichaAnterior,"\tsiguiente: ",laberinto[posX-1][posY])
    movimientoValido = bool(list(prolog.query("permiteMovimiento(%s,w,%s)."%(fichaAnterior, laberinto[posX-1][posY]))))
    print(movimientoValido)
    if posX-1 >= 0 and movimientoValido:
        fichaTemp = fichaAnterior
        fichaAnterior = laberinto[posX-1][posY]
        laberinto[posX][posY] = fichaTemp
        laberinto[posX-1][posY] = 'O'
        posX-=1
    verLaberinto()

def moverAbajo(event):
    global posX, posY,fichaAnterior
    print("Movimiento: abajo\n")
    print("actual: ",fichaAnterior,"\tsiguiente: ",laberinto[posX+1][posY])
    movimientoValido = bool(list(prolog.query("permiteMovimiento(%s,s,%s)."%(fichaAnterior, laberinto[posX+1][posY]))))
    print(movimientoValido)
    if posX+1 < len(laberinto) and movimientoValido:
        fichaTemp = fichaAnterior
        fichaAnterior = laberinto[posX+1][posY]
        laberinto[posX][posY] = fichaTemp
        laberinto[posX+1][posY] = 'O'
        posX+=1
    verLaberinto()

 
 

ventana.bind("<Left>", moverIzquierda)
ventana.bind("<Right>", moverDerecha)
ventana.bind("<Up>", moverArriba)
ventana.bind("<Down>", moverAbajo)

ventana.mainloop()