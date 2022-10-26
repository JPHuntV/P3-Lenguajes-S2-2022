

from pyswip import Prolog
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import *
from copy import deepcopy
from tabulate import tabulate
import time
from datetime import datetime


def getVentana():
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
    return ventana

ventana = getVentana()
prolog = Prolog()
prolog.consult("logica.pro")

rutaArchivoLaberinto = ""
laberinto = []
tablero = []
posX = 0
posY = 0

finX = 0
finY = 0
gano = "inactivo"

fichaAnterior = "i"

colores= {"x":"red","O":"purple", "f":"yellow","i":"green","ad" : "cyan","at" : "cyan","ab": "cyan","ar" : "cyan","inter" : "cyan"}
frames= {}
nickname = "Jugador 1"
numeroMovimientos = 0
numeroSugerencias = 10
tiempoInicio = datetime.now()


def raise_frame(frame):
    frame.tkraise()

def crearPaginaInicio():
    global ventana
    ventanaInicio  = crearFrame()
    frames['ventanaInicio'] = ventanaInicio
    botonJuegoNuevo= tk.Button(ventanaInicio, text ="Juego Nuevo", command = lambda: crearPaginaPreJuego())
    botonJuegoNuevo.grid(column=0,row=0)
    

def crearPaginaTablero():
    global ventana, contadorMov, contadorSug, gano
    ventanaTablero  = crearFrame()
    frames['ventanaTablero'] = ventanaTablero
    tk.Label(ventanaTablero, textvariable=cronometro).grid(column=0, row=0, sticky=NSEW)

    contadorMov = tk.StringVar(frames["ventanaTablero"],value="Numero de movimientos: "+str(numeroMovimientos))
    tk.Label(ventanaTablero,textvariable=contadorMov).grid(column=1,row=0)

    contadorSug = tk.StringVar(frames["ventanaTablero"],value="Sugerencias disponibles: "+str(numeroSugerencias))
    tk.Label(ventanaTablero,textvariable=contadorSug).grid(column=1,row=1)

    
    botonVerificar= tk.Button(ventanaTablero, text ="verificar", command = lambda:verificar())
    botonVerificar.grid(column=2, row=0)

    botonSol= tk.Button(ventanaTablero, text ="Solucion", command = lambda:autoSolucionar())
    botonSol.grid(column=2, row=1)

    botSolicitarSugerencia= tk.Button(ventanaTablero, text ="Sugerencia", command = lambda:solicitarSugerencia())
    botSolicitarSugerencia.grid(column=2, row=2)

    botonAbandonar= tk.Button(ventanaTablero, text ="Abandonar", command = lambda:abandonarPartida())
    botonAbandonar.grid(column=2, row=3)

    tablero = crearTablero(ventanaTablero)
    if not tablero:
        raise_frame(frames["ventanaPreJuego"])

    else:
        tablero.grid(column=0,row=1)
        gano = "activo"



def crearPaginaPreJuego():
    global ventana, laberintoSeleccionado, nickname
    ventanaPreJuego  = crearFrame()
    frames['ventanaPreJuego'] = ventanaPreJuego

    tk.Label(ventanaPreJuego,text="Nickname: ").grid(column=0,row=0)

    nickname = tk.Entry(ventanaPreJuego)
    nickname.grid(column=1,row=0)

    tk.Label(ventanaPreJuego,text="Laberinto: ").grid(column=0,row=1)

    botonArchivo = tk.Button(ventanaPreJuego, text ="Archivo", command = lambda: solicitarArchivo())
    botonArchivo.grid(column=1, row=1)

    laberintoSeleccionado = tk.StringVar(frames["ventanaPreJuego"],value=rutaArchivoLaberinto)
    tk.Label(ventanaPreJuego,textvariable=laberintoSeleccionado).grid(column=0,row=2)

    botonIniciarJuego = tk.Button(ventanaPreJuego, text ="Iniciar", command = lambda: iniciarJuego())
    botonIniciarJuego.grid(column=1, row=3)

    botonVolver = tk.Button(ventanaPreJuego, text ="Volver", command = lambda: raise_frame(frames["ventanaInicio"]))
    botonVolver.grid(column=0, row=3)

def crearPaginaFinal():
    global ventana, tablero
    ventanaFinal = crearFrame()
    frames['ventanaFinal'] = ventanaFinal

    tk.Label(ventanaFinal,text="Juego terminado").grid(column=0,row=0,columnspan=3)

    tablero = crearTablero(ventanaFinal)
    tablero.grid(column=0,row=1,rowspan=5)

    if gano == "auto":
        mostrarSolucion(tablero)

    tk.Label(ventanaFinal,text="Nickname: ").grid(column=1,row=1)
    tk.Label(ventanaFinal,text="Movimientos: ").grid(column=1,row=2)
    tk.Label(ventanaFinal,text="Sugerencias utilizadas: ").grid(column=1,row=3)
    tk.Label(ventanaFinal,text="Tiempo: ").grid(column=1,row=4)
    tk.Label(ventanaFinal,text="Finalizó por:").grid(column=1,row=5)

    tk.Label(ventanaFinal,text=nickname.get()).grid(column=2,row=1)
    tk.Label(ventanaFinal,text=numeroMovimientos).grid(column=2,row=2)
    tk.Label(ventanaFinal,text=10-numeroSugerencias).grid(column=2,row=3)
    tk.Label(ventanaFinal,textvariable=cronometro).grid(column=2,row=4)
    tk.Label(ventanaFinal,text=gano).grid(column=2,row=5)

    botonoEstadisticas = tk.Button(ventanaFinal, text ="Estadísticas", command = lambda: print("estadisticas"))
    botonoEstadisticas.grid(column=1, row=6)

    botonoHome = tk.Button(ventanaFinal, text ="Volver a inicio", command = lambda: raise_frame(frames["ventanaInicio"]))
    botonoHome.grid(column=2, row=6)

def crearFrame():
    global ventana
    frame = ttk.Frame(ventana)
    frame.columnconfigure(0,weight=1)
    frame.grid(column=0, row=0,sticky=NSEW)
    return frame

def solicitarArchivo():
    global rutaArchivoLaberinto, laberintoSeleccionado
    print ("solicitar archivo")
    rutaArchivoLaberinto = filedialog.askopenfilename()
    laberintoSeleccionado.set(rutaArchivoLaberinto)

def iniciarJuego():
    global laberintoSeleccionado,posX,posY, finX, finY, gano

    posX = 0
    posY = 0

    finX = 0
    finY = 0
    gano = "inactivo"
    if nickname.get() != "":
        if laberintoSeleccionado.get() != "":

            laberintoProlog = prolog.query("getLaberinto('%s',X)." % (laberintoSeleccionado.get()))
            #laberintoProlog = prolog.query("getLaberinto('laberinto1.txt',X).")################################################
            transformarLaberinto(laberintoProlog)
            obtenerPosicionInicial()
            crearPaginaTablero()
        else:
            print("seleccione un laberinto")
    else:
        print("ingrese un nombre de usuario")

def transformarLaberinto(laberintoProlog):
    global laberinto
    laberinto = []
    for i in laberintoProlog: 
        for j in i["X"]:
            elemento = j.decode("utf-8") #transformar de byte a string
            listaEle = elemento.strip('][').split(',') #transformar de string a lista
            laberinto += [listaEle]

    

def obtenerPosicionInicial():
    global laberinto, posX, posY, finX, finY,fichaAnterior,numeroMovimientos
    numeroMovimientos = 0
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



def estadoJuego():
    global gano
    print(gano)





def abandonarPartida():
    global gano
    gano = "abandono"
    print (gano)
    crearPaginaFinal()
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

def solicitarSugerencia():
    global solucionLaberinto,tablero,numeroSugerencias
    if numeroSugerencias>0:
        obtenerSolucion()
        if solucionLaberinto !=[]:
            sugerencia = solucionLaberinto[1]
            child = tablero.winfo_children()
            for i in child:
                infoGrid = i.grid_info()
                pos = (infoGrid["row"], infoGrid["column"])
                print("col: ",infoGrid["column"]," row: ", infoGrid["row"], " texto: ",i["text"])
                if sugerencia == pos:
                    i.config(bg="purple")
                    ventana.after(2000,mostrarSugerencia,i)
                    numeroSugerencias -=1
                    contadorSug.set("Sugerencias disponibles: "+str(numeroSugerencias))
                    break
        else:
            print("no hay solución, gg")
    else:
        print("no quedan sugerencias")
        
    print("sssssssssssssssssssssssssssssssss")

def mostrarSugerencia(ficha):
   ficha.config(bg=colores[ficha["text"]])
    


def crearTablero(ventanaTablero):
    global laberinto, colores, tablero
    tablero = ttk.Frame(ventanaTablero)
    tablero.columnconfigure(0,weight=1)
    numFila= 0
    numCol = 0
    for i in laberinto:
        for j in i:
            try:
                ficha = tk.Label(tablero, text=j,background=colores[j],padx=0,pady=0).grid(column=numCol, row=numFila, sticky=NSEW)
            except:
                return False
            numCol +=1
        numFila +=1
        numCol = 0
    return tablero
    


def autoSolucionar():
    global solucionLaberinto, gano
    obtenerSolucion()
    if solucionLaberinto !=[]:
        gano = "auto"
        crearPaginaFinal()
    else:
        print("no hay solución, gg")

def mostrarSolucion(tab):
    child = tab.winfo_children()
    for i in child:
        infoGrid = i.grid_info()
        pos = (infoGrid["row"], infoGrid["column"])
        print("col: ",infoGrid["column"]," row: ", infoGrid["row"], " texto: ",i["text"])
        i.config(bg=colores[i["text"]])
        if pos in solucionLaberinto:
            print ("Si")
            i.config(bg="purple")
            #ventana.after(2000,mostrarSugerencia,i)
            #numeroSugerencias -=1
            #contadorSug.set("Sugerencias disponibles: "+str(numeroSugerencias))
            #break
    

def obtenerSolucion():
    global  posX, posY, finX, finY, solucionLaberinto
    solucionLaberinto = []
    laberintoTemp = deepcopy(laberinto)
    solucionarLaberinto(laberintoTemp,(posX,posY),(finX, finY))
    #verLaberinto()##################
    #########raise_frame(frames["ventanaInicio"])
    solucionLaberinto.reverse()
    print(solucionLaberinto)
    


def verificar():
    global solucionLaberinto, gano
    obtenerSolucion()
    if solucionLaberinto !=[]:
        print("si forma parte del camino")
    else:
            print("no forma parte del camino")

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
    global posX, posY,fichaAnterior, numeroMovimientos, tiempoInicio, laberinto,gano
    if gano != "activo":
        print("el juego no está activo")
        return
    puntosMovimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    letrasMovimientos = ['w','s','a','d']
    siguientePunto = (posX + puntosMovimientos[i][0], posY + puntosMovimientos[i][1])
    if siguientePunto[0] in range(len(laberinto)) and siguientePunto[1] in range(len(laberinto[siguientePunto[0]])):
        movimientoValido = bool(list(prolog.query("permiteMovimiento(%s,%s,%s)."%(fichaAnterior,letrasMovimientos[i],laberinto[siguientePunto[0]][siguientePunto[1]]))))
        if movimientoValido and gano == "activo":
            print("x: ",siguientePunto[0], " y: ",siguientePunto[1])
            moverFichaAux((posX,posY),siguientePunto) #mueve la ficha graficamente
            fichaTemp = fichaAnterior
            fichaAnterior = laberinto[siguientePunto[0]][siguientePunto[1]]
            laberinto[posX][posY] = fichaTemp
            laberinto[siguientePunto[0]][siguientePunto[1]] = 'O'
            posY+=puntosMovimientos[i][1]
            posX+=puntosMovimientos[i][0]
            numeroMovimientos+=1
            contadorMov.set("Numero de movimientos: "+str(numeroMovimientos)) 

        ###########################################################################
            print(tabulate(laberinto, tablefmt="grid")) 
            if fichaAnterior =="f":
                print("Ganó")
                gano = "exitosa"
                crearPaginaFinal()
    
    if numeroMovimientos == 1:
        tiempoInicio = datetime.now()
        refrescarTiempo()
    print(numeroMovimientos)


def moverIzquierda(event):
    moverFicha(2)
    

def moverDerecha(event):
    moverFicha(3)
    

def moverArriba(event):
    moverFicha(0)
    

def moverAbajo(event):
    moverFicha(1)
    







def formatearTiempo(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas*60*60
    minutos = int(segundos/60)
    segundos -= minutos*60
    print(f"{horas:02d}:{minutos:02d}:{segundos:02d}")
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def getTiempo():
    segundos_transcurridos= (datetime.now() - tiempoInicio).total_seconds()
    return formatearTiempo(int(segundos_transcurridos))


def refrescarTiempo():
    global ventana
    if numeroMovimientos >=1 and gano == "activo":
        cronometro.set(getTiempo())
        ventana.after(500, refrescarTiempo)


cronometro = tk.StringVar(ventana, value=getTiempo())



 
 
crearPaginaInicio()
ventana.bind("<Left>", moverIzquierda)
ventana.bind("<Right>", moverDerecha)
ventana.bind("<Up>", moverArriba)
ventana.bind("<Down>", moverAbajo)

ventana.mainloop()