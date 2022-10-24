
from glob import glob
from turtle import color, width
from pyswip import Prolog
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import *
from copy import deepcopy
from tabulate import tabulate
import time


ventana = Tk()

anchoVentana = 1280 
altoVentana = 720

# get the screen dimension
anchoPantalla = ventana.winfo_screenwidth()
altoPantalla = ventana.winfo_screenheight()

# find the center point
centroX = int(anchoPantalla/2 - anchoVentana / 2)
centroY = int(altoPantalla/2 - altoVentana / 2)

# set the position of the window to the center of the screen
ventana.geometry(f'{anchoVentana}x{altoVentana}+{centroX}+{centroY}')
ventana.columnconfigure(0,weight=1)

prolog = Prolog()
prolog.consult("logica.pro")

rutaArchivoLaberinto = ""
laberinto = []
tablero = []
posX = 0
posY = 0

finX = 0
finY = 0


fichaAnterior = "i"

colores= {"x":"red","O":"purple", "f":"yellow","i":"green","ad" : "cyan","at" : "cyan","ab": "cyan","ar" : "cyan","inter" : "cyan"}

def solicitarArchivo():
    global archivoLaberinto
    print ("solicitar archivo")
    #rutaArchivoLaberinto = filedialog.askopenfilename()
    #laberintoProlog = prolog.query("getLaberinto('%s',X)." % (rutaArchivoLaberinto))
    laberintoProlog = prolog.query("getLaberinto('laberinto1.txt',X).")################################################
    transformarLaberinto(laberintoProlog)
    obtenerPosicionInicial()
    crearTablero()
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
botonArchivo.grid(column=1, row=0)

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
    global laberinto, ventana, colores
    print("laberinto---------------------")

    
    print(tabulate(laberinto, tablefmt="grid")) 
    verificarGane()
    

def crearTablero():
    global laberinto, ventana, colores, tablero
    tablero = ttk.Frame(ventana)
    tablero.columnconfigure(0,weight=1)
    numFila= 0
    numCol = 0
    for i in laberinto:
        for j in i:
            ficha = tk.Label(tablero, text=j,background=colores[j],padx=0,pady=0).grid(column=numCol, row=numFila, sticky=NSEW)
            numCol +=1
        numFila +=1
        numCol = 0
    tablero.grid(column=0,row=0)



botonVer= tk.Button(ventana, text ="ver", command = lambda: verLaberinto())
botonVer.grid(column=1, row=1)

def verSol(laberinto):
    global  posX, posY, finX, finY, solucionLaberinto
    solucionLaberinto = []
    laberintoTemp = deepcopy(laberinto)
    solucionarLaberinto(laberintoTemp,(posX,posY),(finX, finY))
    verLaberinto()##################
    print(solucionLaberinto)

botonSol= tk.Button(ventana, text ="Solucion", command = lambda:verSol(laberinto))
botonSol.grid(column=1, row=2)


#mover ficha en interfaz
def moverFichaAux(fichaActual, fichaSiguiente):
    global tablero, fichaAnterior
    child = tablero.winfo_children()
    for i in child:
        infoGrid = i.grid_info()
        pos = (infoGrid["row"], infoGrid["column"])
        print("col: ",infoGrid["column"]," row: ", infoGrid["row"], " texto: ",i["text"])
        if fichaActual == pos:
            print("encontré la ficha actual")
            i["bg"] = colores[fichaAnterior]
        elif fichaSiguiente == pos:
            print("encontré la siguiente")
            i["bg"] = colores["O"]

def moverFicha(i):
    global posX, posY,fichaAnterior
    puntosMovimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    letrasMovimientos = ['w','s','a','d']
    siguientePunto = (posX + puntosMovimientos[i][0], posY + puntosMovimientos[i][1])
    movimientoValido = bool(list(prolog.query("permiteMovimiento(%s,%s,%s)."%(fichaAnterior,letrasMovimientos[i],laberinto[siguientePunto[0]][siguientePunto[1]]))))
    print("x: ",siguientePunto[0], " y: ",siguientePunto[1])
    if siguientePunto[0] in range(len(laberinto)) and siguientePunto[1] in range(len(laberinto[siguientePunto[0]])) and movimientoValido:
        moverFichaAux((posX,posY),siguientePunto) #mueve la ficha graficamente
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