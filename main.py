from turtle import pos
from pyswip import Prolog
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from copy import deepcopy
from tabulate import tabulate
import time

ventana = Tk()
prolog = Prolog()
prolog.consult("logica.pro")

rutaArchivoLaberinto = ""
laberinto = []

posX = 0
posY = 0

finX = 0
finY = 0
fichaAnterior = "i"

def solicitarArchivo():
    global archivoLaberinto
    print ("solicitar archivo")
    #rutaArchivoLaberinto = filedialog.askopenfilename()
    #laberintoProlog = prolog.query("getLaberinto('%s',X)." % (rutaArchivoLaberinto))
    laberintoProlog = prolog.query("getLaberinto('laberinto1.txt',X).")################################################
    transformarLaberinto(laberintoProlog)
    obtenerPosicionInicial()
    verLaberinto()

def transformarLaberinto(laberintoProlog):
    global laberinto
    laberinto = []
    for i in laberintoProlog: 
        for j in i["X"]:
            elemento = j.decode("utf-8") #transformar de byte a string
            listaEle = elemento.strip('][').split(',') #transformar de string a lista
            laberinto += [listaEle]

    

def obtenerPosicionInicial():
    global laberinto, posX, posY, finX, finY,fichaAnterior
    x = 0
    y = 0
    for i in laberinto:
        for j in i:
            if j == 'i':
                posX = x
                posY = y
                laberinto[posX][posY]="O"
            if j == "f":
                finX = x
                finY = y
            y+=1
        x+=1
        y=0
    fichaAnterior = "i"
    print("inicial x= ",posX,"inicial y= ",posY)
    print("final x= ",finX,"fin y= ",finY)




botonArchivo= tk.Button(ventana, text ="Archivo", command = lambda: solicitarArchivo())
botonArchivo.pack()

def verificarGane():
    if fichaAnterior =="f":
        print("Ganó")

####################################################################################################################
solucionLaberinto= []

#este algoritmo fue basado en el siguiente articulo https://programmerclick.com/article/67791960095/ 
#tomando en cuenta las diferencias entre los objetivos 
def solucionarLaberinto(laberintoSol, puntoInicio, puntoFinal):
    actual = laberintoSol[puntoInicio[0]][puntoInicio[1]]
    if actual == "O":
        actual = fichaAnterior
    laberintoSol[puntoInicio[0]][puntoInicio[1]] = "v"
    if puntoInicio == puntoFinal:  #si la posición de la p
        solucionLaberinto.append(puntoInicio)
        return True

    puntosMovimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    letrasMovimientos = ['w','s','a','d']
    for i in range(4):
        siguientePunto = (puntoInicio[0] + puntosMovimientos[i][0], puntoInicio[1] + puntosMovimientos[i][1])
        siguiente = laberintoSol[siguientePunto[0]][siguientePunto[1]]
        print("########\nActual: ", actual, "\tsiguiente: ", siguiente, " direccion: ",letrasMovimientos[i])
        movimientosValido = bool(list(prolog.query("permiteMovimiento(%s,'%s',%s)."%(actual, letrasMovimientos[i],siguiente)))) #prolog evalua si el movimiento se puede realizar
        if movimientosValido:
            if solucionarLaberinto(laberintoSol, siguientePunto, puntoFinal):
                solucionLaberinto.append(puntoInicio)
                return True
    return False  # El laberinto no tiene solución

######################################################################################################################################################



def verLaberinto():
    global laberinto
    print("laberinto---------------------")
    print(tabulate(laberinto, tablefmt="grid")) 
    verificarGane()

botonVer= tk.Button(ventana, text ="ver", command = lambda: verLaberinto())
botonVer.pack()

def verSol(laberinto):
    global  posX, posY, finX, finY, solucionLaberinto
    solucionLaberinto = []
    laberintoTemp = deepcopy(laberinto)
    solucionarLaberinto(laberintoTemp,(posX,posY),(finX, finY))
    verLaberinto()##################
    print(solucionLaberinto)

botonSol= tk.Button(ventana, text ="Solucion", command = lambda:verSol(laberinto))
botonSol.pack()

def moverFicha(i):
    global posX, posY,fichaAnterior
    puntosMovimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    letrasMovimientos = ['w','s','a','d']
    siguientePunto = (posX + puntosMovimientos[i][0], posY + puntosMovimientos[i][1])
    movimientoValido = bool(list(prolog.query("permiteMovimiento(%s,%s,%s)."%(fichaAnterior,letrasMovimientos[i],laberinto[siguientePunto[0]][siguientePunto[1]]))))
    print("x: ",siguientePunto[0], " y: ",siguientePunto[1])
    if siguientePunto[0] in range(len(laberinto)) and siguientePunto[1] in range(len(laberinto[siguientePunto[0]])) and movimientoValido:
        fichaTemp = fichaAnterior
        fichaAnterior = laberinto[siguientePunto[0]][siguientePunto[1]]
        laberinto[posX][posY] = fichaTemp
        laberinto[siguientePunto[0]][siguientePunto[1]] = 'O'
        posY+=puntosMovimientos[i][1]
        posX+=puntosMovimientos[i][0]


def moverIzquierda(event):
    moverFicha(2)
    verLaberinto()

def moverDerecha(event):
    moverFicha(3)
    verLaberinto()

def moverArriba(event):
    moverFicha(0)
    verLaberinto()

def moverAbajo(event):
    moverFicha(1)
    verLaberinto()














 
 

ventana.bind("<Left>", moverIzquierda)
ventana.bind("<Right>", moverDerecha)
ventana.bind("<Up>", moverArriba)
ventana.bind("<Down>", moverAbajo)

ventana.mainloop()