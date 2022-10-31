#python3 -m pip install pillow

import os
from turtle import left
from pyswip import Prolog
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image  
from copy import deepcopy
from tabulate import tabulate
import time
from datetime import datetime
import uuid
from scroll import ScrollableFrame



def getVentana():
    global ventana
    ventana = Tk()
    x = 1280
    y = 720

    anchoPantalla = ventana.winfo_screenwidth()
    altoPantalla = ventana.winfo_screenheight()

    # find the center point
    centroX = int(anchoPantalla/2 - x / 2)
    centroY = int(altoPantalla/2 - y / 2)

    # set the position of the window to the center of the screen
    ventana.geometry(f'{x}x{y}+{centroX}+{centroY}')
    ventana.columnconfigure(0,weight=1, uniform="vent")
    ventana.rowconfigure(0,weight=1)
    ventana.resizable(width=False, height=False)
    return ventana

def cambiarTama(x, y):
    global ventana

    anchoPantalla = ventana.winfo_screenwidth()
    altoPantalla = ventana.winfo_screenheight()
    centroX = int(anchoPantalla/2 - x / 2)
    centroY = int(altoPantalla/2 - y / 2)

    # set the position of the window to the center of the screen
    ventana.geometry(f'{x}x{y}+{centroX}+{centroY}')
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
flechas={"at":"←","ad":"→","ar":"↑","ab":"↓","inter":"+","i":"⌂","f":"▧","x":"x","O":"O"}
colores = {"x":"#211438",
            "auto": "#9734FA",
            "sugerencia" : "#9734FA",
            "O":"#71A85E",
            "i":"#D7FA0F",
            "inicio": "#D7FA0F",
            "f":"#FA5041",
            "ar" : "#C9429E",
            "ab": "#0A56AD",
            "ad" : "#E28B48",
            "at" : "#F4D03F",
            "inter" : "#873600",
            "normal" : "#16A085",
            }
frames= {}
movRepeticion = []
nickname = "Jugador 1"
numeroMovimientos = 0
numeroSugerencias = 10
tiempoInicio = datetime.now()

laberintoPrueba = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'], ['x', 'ar', 'x', 'x', 'ad', 'ad', 'ad', 'inter', 'ad', 'inter', 'x'], ['i', 'inter', 'ad', 'ad', 'inter', 'x', 'x', 'ab', 'x', 'ab', 'x'], ['x', 'ab', 'x', 'x', 'x', 'inter', 'at', 'inter', 'x', 'ab', 'x'], ['x', 'ab', 'x', 'x', 'x', 'ab', 'x', 'ab', 'x', 'x', 'x'], ['x', 'ab', 'x', 'x', 'inter', 'inter', 'x', 'ab', 'x', 'inter', 'f'], ['x', 'ab', 'x', 'x', 'ab', 'x', 'x', 'inter', 'inter', 'inter', 'x'], ['x', 'ab', 'x', 'x', 'ab', 'x', 'x', 'x', 'ar', 'x', 'x'], ['x', 'ab', 'x', 'at', 'inter', 'inter', 'ad', 'ad', 'inter', 'at', 'x'], ['x', 'ab', 'x', 'ar', 'x', 'ab', 'x', 'x', 'ab', 'ar', 'x'], ['x', 'inter', 'ad', 'inter', 'x', 'inter', 'ad', 'x', 'ab', 'inter', 'x'], ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
def raise_frame(frame,x,y):
    cambiarTama(x,y)
    frame.tkraise()

def crearPaginaInicio():
    global ventana,img
    cambiarTama(270,400)
    ventanaInicio  = crearFrame()
    ventanaInicio.tk_setPalette(background = "white")
    ventanaInicio
    frames['ventanaInicio'] = ventanaInicio
    ventanaInicio.grid_columnconfigure(0, weight=1)
    ventanaInicio.grid_rowconfigure(1, weight=1)
    img =ImageTk.PhotoImage(Image.open("img/inicio.jpg").resize((300,200), Image.ANTIALIAS))


    
    imagenInicio  = tk.Label(ventanaInicio, image=img)
    imagenInicio.grid(row=0,column=0)

    frameBotones = Frame(ventanaInicio)
    frameBotones.grid(column=0, row=1, sticky=NSEW)
    frameBotones.columnconfigure(0, weight=1)
    frameBotones.rowconfigure((0,1,2),weight=1, uniform="frameBotones")
    botonJuegoNuevo= tk.Button(frameBotones, text ="Juego Nuevo", font="MS-Sans-Serif 12" ,command = lambda: crearPaginaPreJuego(), width=230, height=25, background="#4F67E0", foreground="white")
    botonJuegoNuevo.grid(column=0,row=0, padx = 20,sticky=EW, pady=13)


    botonEstadisticas= tk.Button(frameBotones, text ="Estadisticas", font="MS-Sans-Serif 12" ,command = lambda: crearPaginaEstadisticas("ventanaInicio"), width=230, height=25, background="#4F67E0", foreground="white")
    botonEstadisticas.grid(column=0,row=1, padx=20, sticky=EW, pady=13)

    botonRepeticiones= tk.Button(frameBotones, text ="Repeticiones", font="MS-Sans-Serif 12" ,command = lambda: crearPaginaEstadisticas("ventanaInicio"), width=230, height=25, background="#4F67E0", foreground="white")
    botonRepeticiones.grid(column=0,row=2, padx=20, sticky=EW, pady=13)
   
    

def crearPaginaTablero():
    global ventana, contadorMov, contadorSug, gano, laberinto, tablero
    cambiarTama(1280,720)
    ventanaTablero  = crearFrame()
    frames['ventanaTablero'] = ventanaTablero
    ventanaTablero["bg"] = "white"
    ventanaTablero.grid(sticky=NSEW)
    ventanaTablero.columnconfigure((0,1,2),weight=1, uniform="elemTab")

    
    contadorSug = tk.StringVar(frames["ventanaTablero"],value="Sugerencias disponibles: "+str(numeroSugerencias))
    tk.Label(ventanaTablero,textvariable=contadorSug, relief='sunken', borderwidth=2).grid(row=0, column=0, sticky="we")

    tk.Label(ventanaTablero, textvariable=cronometro, relief='sunken', borderwidth=2).grid(row=0, column=1, sticky=NSEW)

    contadorMov = tk.StringVar(frames["ventanaTablero"],value="Numero de movimientos: "+str(numeroMovimientos))
    tk.Label(ventanaTablero,textvariable=contadorMov, relief='sunken', borderwidth=2).grid(row=0, column=2, sticky=NSEW)


    botSolicitarSugerencia= tk.Button(ventanaTablero, text ="Sugerencia", command = lambda:solicitarSugerencia())
    botSolicitarSugerencia.grid(row=2, column=0, sticky=NSEW)
    
    botonVerificar= tk.Button(ventanaTablero, text ="verificar", command = lambda:verificar())
    botonVerificar.grid(row=2, column=1, sticky=NSEW)

    botonReiniciar= tk.Button(ventanaTablero, text ="reiniciar", command = lambda:reiniciar())
    botonReiniciar.grid( row=2, column=2, sticky=NSEW)

    framebot = tk.Frame(ventanaTablero)
    framebot.grid(row=3, column=0, columnspan=3,sticky=NSEW)
    framebot.grid_columnconfigure((0,1), weight=1, uniform="elemTab2")
    
    botonAbandonar= tk.Button(framebot, text ="Abandonar", command = lambda:abandonarPartida())
    botonAbandonar.grid(row = 0, column=0, sticky=NSEW)
    
    botonSol= tk.Button(framebot, text ="Solucion", command = lambda:autoSolucionar())
    botonSol.grid(row = 0, column=1, sticky=NSEW)



    frameTablero = Frame(ventanaTablero)
    frameTablero.grid(row=1,column = 0, columnspan=3, sticky=NSEW)
    frameTablero.rowconfigure(0, weight=1)
    frameTablero.columnconfigure((0,2), weight=1, uniform="col")
    tablero = crearTablero(frameTablero,laberinto)
    tablero.grid(row=0,column = 1)


    frameCol0 = Frame(frameTablero, bg="red")
    frameCol0.grid(row=0, column=0, sticky=NSEW)
    frameCol0.columnconfigure((0), weight=1, uniform="col1")
    frameCol0.rowconfigure((0,1,2,3,4), weight=1, uniform="row1")
    

    tk.Label(frameCol0, text="Permite movimiento hacia arriba").grid(row=0, column=0,sticky=E)
    tk.Label(frameCol0, relief='sunken', borderwidth=2).grid(row=0, column=1,ipadx=13, ipady=5,padx=5, sticky=E)

    tk.Label(frameCol0, text="Permite movimiento hacia arriba").grid(row=1, column=0,sticky=E)
    tk.Label(frameCol0, relief='sunken', borderwidth=2).grid(row=1, column=1,ipadx=13, ipady=5,padx=5, sticky=E)
    
    tk.Label(frameCol0, text="Permite movimiento hacia arriba").grid(row=2, column=0,sticky=E)
    tk.Label(frameCol0, relief='sunken', borderwidth=2).grid(row=2, column=1,ipadx=13, ipady=5,padx=5, sticky=E)

    tk.Label(frameCol0, text="Permite movimiento hacia arriba").grid(row=3, column=0,sticky=E)
    tk.Label(frameCol0, relief='sunken', borderwidth=2).grid(row=3, column=1,ipadx=13, ipady=5,padx=5, sticky=E)

    tk.Label(frameCol0, text="Permite movimiento hacia arriba").grid(row=4, column=0,sticky=E)
    tk.Label(frameCol0, relief='sunken', borderwidth=2).grid(row=4, column=1,ipadx=13, ipady=5,padx=5, sticky=E)
   
    frameCol2 = Frame(frameTablero, bg="blue")
    frameCol2.grid(row=0, column=2, sticky=NSEW)
    frameCol2.columnconfigure((1), weight=1, uniform="col1")
    frameCol2.rowconfigure((0,1,2,3,4), weight=1, uniform="row1")

    tk.Label(frameCol2, text="Permite movimiento hacia arriba").grid(row=0, column=1,sticky=W)
    tk.Label(frameCol2, relief='sunken', borderwidth=2).grid(row=0, column=0,ipadx=13, ipady=5,padx=5, sticky=W)

    tk.Label(frameCol2, text="Permite movimiento hacia arriba").grid(row=1, column=1,sticky=W)
    tk.Label(frameCol2, relief='sunken', borderwidth=2).grid(row=1, column=0,ipadx=13, ipady=5,padx=5, sticky=W)
    
    tk.Label(frameCol2, text="Permite movimiento hacia arriba").grid(row=2, column=1,sticky=W)
    tk.Label(frameCol2, relief='sunken', borderwidth=2).grid(row=2, column=0,ipadx=13, ipady=5,padx=5, sticky=W)

    tk.Label(frameCol2, text="Permite movimiento hacia arriba").grid(row=3, column=1,sticky=W)
    tk.Label(frameCol2, relief='sunken', borderwidth=2).grid(row=3, column=0,ipadx=13, ipady=5,padx=5, sticky=W)

    tk.Label(frameCol2, text="Permite movimiento hacia arriba").grid(row=4, column=1,sticky=W)
    tk.Label(frameCol2, relief='sunken', borderwidth=2).grid(row=4, column=0,ipadx=13, ipady=5,padx=5, sticky=W)

    if not tablero:
        raise_frame(frames["ventanaPreJuego"],400,500)

    else:
        
        gano = "activo"



def crearPaginaPreJuego():
    global ventana, laberintoSeleccionado, nickname
    cambiarTama(270,400)
    ventanaPreJuego  = crearFrame()
    frames['ventanaPreJuego'] = ventanaPreJuego
    ventanaPreJuego["bg"] = "white"
    #ventanaPreJuego.rowconfigure((1,2,3,4,5,6), weight=1, uniform="ventanaPreJuegofila")

    tk.Label(ventanaPreJuego, text="Seleccionar laberinto", font="ms-sans-serif 12 bold").grid(row=0, column=0,columnspan=2, sticky="nw",padx=(20,0), pady=(32,0))
    tk.Label(ventanaPreJuego,text="Nickname: ").grid(row=1, column=0, sticky="w",padx=(20,0), pady=(35,0))

    nickname = tk.Entry(ventanaPreJuego, justify=LEFT, bg="#f1f1f1")
    nickname.grid(row=2, column=0, columnspan=2, sticky="we", padx=20, ipady=6)

    tk.Label(ventanaPreJuego,text="Laberinto: ").grid(row=3, column=0, sticky="w", padx=20, pady=(30,0))

    
    #laberintoSeleccionado = tk.StringVar(frames["ventanaPreJuego"],value=rutaArchivoLaberinto)
    laberintoSeleccionado = tk.StringVar(frames["ventanaPreJuego"],value="laberinto.txt")

    tk.Label(ventanaPreJuego,textvariable=laberintoSeleccionado, borderwidth=1, relief="sunken", bg="#f1f1f1", anchor="w").grid(row=4, column=0, columnspan=2, sticky="we", padx=20, ipady=6)

    botonArchivo = tk.Button(ventanaPreJuego, text ="Seleccionar laberinto", command = lambda: solicitarArchivo(), bg="#4F67E0", foreground="white")
    botonArchivo.grid(row=5, column=0, columnspan=2, sticky="we", padx=20, pady=(20,0), ipady=6)

    botonIniciarJuego = tk.Button(ventanaPreJuego, text ="Iniciar", command = lambda: iniciarJuego(), bg="#4F67E0", foreground="white")
    botonIniciarJuego.grid(row=6, column=1, sticky="we" ,padx=(5,20),pady=(50,0) , ipady=6)

    botonVolver = tk.Button(ventanaPreJuego, text ="Volver", command = lambda: raise_frame(frames["ventanaInicio"], 270,400), bg="#4F67E0", foreground="white")
    botonVolver.grid(row=6, column=0, sticky="we",padx=(20,5),pady=(50,0)  , ipady=6)

    ventanaPreJuego.grid_columnconfigure((0,1),weight=1, uniform="colPre")

def crearPaginaFinal():
    global ventana, tablero, movRepeticion,laberinto
    cambiarTama(1280,720)
    ventanaFinal = crearFrame()
    ventanaFinal.grid(sticky=NSEW)
    ventanaFinal.columnconfigure((0,1,2),weight=1, uniform="venFinal")
    frames['ventanaFinal'] = ventanaFinal

    tk.Label(ventanaFinal,text="Juego terminado", borderwidth=2, relief="solid").grid(column=0,row=0,columnspan=3,sticky="we")
    tk.Label(ventanaFinal,text="Sugerencias utilizadas: "+str(10-numeroSugerencias), borderwidth=2, relief="solid").grid(column=0,row=1,sticky="we")
    #tk.Label(ventanaFinal,text=10-numeroSugerencias).grid(column=2,row=3)
    tk.Label(ventanaFinal,textvariable=cronometro, borderwidth=2, relief="solid").grid(column=1,row=1,sticky="we")
    tk.Label(ventanaFinal,text="Movimientos: "+str(numeroMovimientos), borderwidth=2, relief="solid").grid(column=2,row=1,sticky="we")

    tablero = crearTablero(ventanaFinal,laberinto)
    tablero.grid(column=0,row=2,columnspan=3)
    
    if gano == "auto":
        mostrarSolucion(tablero)

    tk.Label(ventanaFinal,text="Nickname: "+nickname.get()).grid(column=0,row=3,sticky=NSEW)
    tk.Label(ventanaFinal,text="Finalizó por:"+gano).grid(column=2,row=3)

    botonoEstadisticas = tk.Button(ventanaFinal, text ="Estadísticas", command = lambda: print("estadisticas"))
    botonoEstadisticas.grid(column=0, row=4)

    botonoHome = tk.Button(ventanaFinal, text ="Volver a inicio", command = lambda: raise_frame(frames["ventanaInicio"],400,500))
    botonoHome.grid(column=2, row=4)
    idEstadistica = guardarEstadisticas(nickname.get(),numeroMovimientos, numeroSugerencias,cronometro.get(),gano)

    botonGuardarRepeticion = tk.Button(ventanaFinal, text ="Guardar repetición", command = lambda: guardarRepeticion(idEstadistica))
    botonGuardarRepeticion.grid(column=1, row=4)
    print(movRepeticion)

def crearPaginaEstadisticas(ventanaAnterior):
    global ventana
    cambiarTama(1280,720)
    ventanaEstadisticas = crearFrame()
    ventanaEstadisticas['bg'] = "red"
    ventanaEstadisticas.columnconfigure((0),weight=1, uniform="ventanaEstadisticas")
    ventanaEstadisticas.rowconfigure((2), weight=1)
    frames['ventanaEstadisticas'] = ventanaEstadisticas




    ef1 = tk.Frame(ventanaEstadisticas)
    ef1.grid(column=0, row=0,sticky=NSEW)
    if(ventanaAnterior=="ventanaInicio"):
        x = 270
        y = 400
    elif(ventanaAnterior == "ventanaFinal"):
        x =1280
        y=720
    botonVolver = tk.Button(ef1, text ="Volver", command = lambda: raise_frame(frames[ventanaAnterior],x,y))
    botonVolver.grid(column=0, row=0, sticky=W,padx=2, columnspan=1)
    tk.Label(ef1, text="Estadisticas").grid(column=1, row=0,sticky=W)
   
    indicesTabla = tk.Frame(ventanaEstadisticas)
    indicesTabla.grid(column=0, row=1,sticky=NSEW)
    indicesTabla.columnconfigure((0,1,2,3,4,5), weight=1, uniform="ef2Uni")
    tk.Label(indicesTabla, text="Nickname").grid(column=0, row=0, sticky= "we")
    tk.Label(indicesTabla, text="Movimientos").grid(column=1, row=0, sticky= "we")
    tk.Label(indicesTabla, text="Sugerencias").grid(column=2, row=0, sticky= "we")
    tk.Label(indicesTabla, text="Tiempo").grid(column=3, row=0, sticky= "we")
    tk.Label(indicesTabla, text="Tipo finalización").grid(column=4, row=0, sticky= "we")
    tk.Label(indicesTabla, text="Repetición").grid(column=5, row=0, sticky= "we")
    tk.Label(indicesTabla, text = "tttttttttttttt").grid(column=6, row=0, sticky= "we")


    ef2Scroll = ScrollableFrame(ventanaEstadisticas)
    ef2Scroll.grid(column=0,row=2,sticky=NSEW)
    ef2 = ef2Scroll.scrollable_frame
    ef2.columnconfigure((0,1,2,3,4,5), weight=1, uniform="ef2Uni")
    

    

    listaEstadisticas = getEstadisticas()


    fil = 1 
    for estadistica in listaEstadisticas:
        tk.Label(ef2, text=estadistica[1], borderwidth=2, relief="sunken"   ).grid(column=0, row=fil, sticky="we")
        tk.Label(ef2, text=estadistica[2], borderwidth=2, relief="sunken"   ).grid(column=1, row=fil, sticky="we")
        tk.Label(ef2, text=estadistica[3], borderwidth=2, relief="sunken"   ).grid(column=2, row=fil, sticky="we")
        tk.Label(ef2, text=estadistica[4], borderwidth=2, relief="sunken"   ).grid(column=3, row=fil, sticky="we")
        tk.Label(ef2, text=estadistica[5], borderwidth=2, relief="sunken"   ).grid(column=4, row=fil, sticky="we")
        if os.path.isfile("repeticiones/"+str(estadistica[0])+".txt") and os.path.isfile("laberintos/"+str(estadistica[0])+".txt"):
            tk.Button(ef2, text =estadistica[0],       command = lambda x= estadistica[0]: getPaginaRepeticion(x)).grid(column=5, row=fil, sticky="we")
        else:
            tk.Button(ef2, text ="Repetición no disponible",state=DISABLED).grid(column=5, row=fil, sticky="we")
        fil+=1
    
    print (listaEstadisticas)

def getEstadisticas():
    archivoEstadisticas = open("estadisticas.txt","r")
    estadisticas = archivoEstadisticas.read()
    archivoEstadisticas.close()
    listaEstadisticasTemp = estadisticas.split("\n")
    listaEstadisticas = []
    for i in listaEstadisticasTemp:
        listaEstadisticas += [i.split(",")] 
    listaEstadisticas.pop(-1)
    return listaEstadisticas


def getRepeticion(id):
    archivoRepeticion = open("repeticiones/"+str(id)+".txt", "r")
    strRepeticion = archivoRepeticion.read()
    archivoRepeticion.close()
    listaRepeticionTemp = strRepeticion.split("\n")
    listaRepeticion = []
    for i in listaRepeticionTemp:
        listaRepeticion += [i.split(",")]
    listaRepeticion.pop(-1)
    return listaRepeticion

def getPaginaRepeticion(id):
    global ventana, laberinto
    ventanaRepeticion = crearFrame()
    frames['ventanaRepeticion'] = ventanaRepeticion
    laberintoProlog = prolog.query("getLaberinto('%s',X)." % ("laberintos/"+str(id)+".txt"))
    laberintoRepeticion = transformarLaberinto(laberintoProlog)
    tablero = crearTablero(ventanaRepeticion, laberintoRepeticion)
    if not tablero:
        print("algo pasó")

    else:
        tablero.grid(column=0,row=0)
        repeticion = getRepeticion(id)
        print(repeticion)
        reproducirRepeticion(tablero,repeticion)


def reproducirRepeticion(tablero, repeticion):
    global ventana
    if repeticion == []:
        print("no quedan pasos")
    else:
        print(repeticion[0])
        reproducirRepeticionAux(tablero,repeticion[0])
        repeticion.pop(0)
        ventana.after(1300, reproducirRepeticion, tablero, repeticion)
        #reproducirRepeticion(tablero,repeticion)

def reproducirRepeticionAux(tab,punto):
    global colores,ventana
    child = tab.winfo_children()
    for i in child:
        infoGrid = i.grid_info()
        pos = (infoGrid["row"], infoGrid["column"])
        #print("col: ",infoGrid["column"]," row: ", infoGrid["row"], " texto: ",i["text"])
        if pos == (int(punto[1]),int(punto[2])):
            #i.config(bg=colores[punto[0]])
            if punto[0] =="sugerencia":
                parpadear(i,colores[punto[0]],"black",5)
            else:
                i.config(bg= colores[punto[0]])
            print ("Si")

def parpadear(objeto, col1, col2, cant):
    global ventana
    if cant != 0:
        objeto.config(bg= col2)
        ventana.after(int(1300/cant),parpadear,objeto,col2,col1,cant-1)


def reiniciar():
    global movRepeticion
    guardarEstadisticas(nickname.get(),numeroMovimientos, numeroSugerencias,cronometro.get(),"abandono")
    movRepeticion += [["reinicio",-1,-1]]
    iniciarJuego()

def guardarEstadisticas(pNickname, pCantmov, pCantSug,pTiempo, pTipoFin):
    estadisticas = open("estadisticas.txt","a")
    id = uuid.uuid1().hex
    nuevaEstadistica = str(id)+","+pNickname+","+str(pCantmov)+","+str(10-pCantSug)+","+str(pTiempo)+","+pTipoFin+"\n"
    estadisticas.write(nuevaEstadistica)
    estadisticas.close()
    return id


def guardarRepeticion(id):
    global movRepeticion,rutaArchivoLaberinto
    archivoLab = open(rutaArchivoLaberinto,"r")
    strLab = archivoLab.read()
    archivoLab.close()
    copiaLab = open("laberintos/"+str(id)+".txt","w")
    copiaLab.write(strLab)
    copiaLab.close()
    archivo = open("repeticiones/"+str(id)+".txt","w")

    for i in movRepeticion:
        archivo.write(i[0]+","+str(i[1])+","+str(i[2])+"\n")
    archivo.close


def crearFrame():
    global ventana
    frame = tk.Frame(ventana, height=720)
    frame.grid(column=0, row=0, sticky=NSEW)
    return frame

def solicitarArchivo():
    global rutaArchivoLaberinto, laberintoSeleccionado
    print ("solicitar archivo")
    rutaArchivoLaberinto = filedialog.askopenfilename()
    laberintoSeleccionado.set(rutaArchivoLaberinto)


def reestablecerValores ():
    global posX,posY, finX, finY, gano,numeroMovimientos, numeroSugerencias, tiempoInicio,cronometro, movRepeticion
    posX = 0
    posY = 0

    finX = 0
    finY = 0
    gano = "inactivo"
    numeroMovimientos = 0
    numeroSugerencias = 10
    tiempoInicio = datetime.now()
    cronometro.set(getTiempo())
    movRepeticion = []

def iniciarJuego():
    global laberintoSeleccionado, laberinto
    reestablecerValores()
    
    if nickname.get() != "":
        if laberintoSeleccionado.get() != "":

            laberintoProlog = prolog.query("getLaberinto('%s',X)." % (laberintoSeleccionado.get()))
            #laberintoProlog = prolog.query("getLaberinto('laberinto1.txt',X).")################################################
            laberinto = transformarLaberinto(laberintoProlog)
            print (laberinto)
            obtenerPosicionInicial()
            crearPaginaTablero()
        else:
            print("seleccione un laberinto")
    else:
        print("ingrese un nombre de usuario")

def transformarLaberinto(laberintoProlog):
    laberinto = []
    for i in laberintoProlog: 
        for j in i["X"]:
            fila = []
            for k in j:
                elemento = k.decode("utf-8") #transformar de byte a string
                #listaEle = elemento.strip('][').split(',') #transformar de string a lista
                fila += [elemento]
            laberinto += [fila]
    return laberinto

    

def obtenerPosicionInicial():
    global laberinto, posX, posY, finX, finY,fichaAnterior,numeroMovimientos,  movRepeticion
    numeroMovimientos = 0
    x = 0
    y = 0
    for i in laberinto:
        for j in i:
            if j == 'i':
                posX = x
                posY = y
                laberinto[posX][posY]="O"
                movRepeticion += [["inicio",x,y]]
            if j == "f":
                finX = x
                finY = y
            y+=1
        x+=1
        y=0
    fichaAnterior = "i"
    print("inicial x= ",posX,"inicial y= ",posY)
    print("final x= ",finX,"fin y= ",finY)





def abandonarPartida():
    global gano, movRepeticion
    gano = "abandono"
    movRepeticion +=[["abandono",-1,-1]]
    print (gano)

    crearPaginaFinal()
####################################################################################################################
solucionLaberinto= []

#este algoritmo fue basado en el siguiente articulo https://programmerclick.com/article/67791960095/ 
#tomando en cuenta las diferencias entre los objetivos 
def solucionarLaberinto(laberintoSol, puntoInicio, puntoFinal):
    actual = laberintoSol[puntoInicio[0]][puntoInicio[1]] #obtener actual
    if actual == "O":
        actual = fichaAnterior
    laberintoSol[puntoInicio[0]][puntoInicio[1]] = "v" #marcar
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
def solucionarLaberinto2(laberintoSol, puntoInicio, puntoFinal):
    print("si estoy aqui")
    actual = laberintoSol[puntoInicio[0]][puntoInicio[1]] #obtener actual
    if actual == "O":
        actual = fichaAnterior
    laberintoSol[puntoInicio[0]][puntoInicio[1]] = "v" #marcar
    if puntoInicio == puntoFinal:  #si la posición de la p
        print("llegue al final")
        solucionLaberinto.append(puntoInicio)
        return True
    else:
        puntosMovimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        letrasMovimientos = ['w','s','a','d']
        for i in range(4):
            siguientePunto = (puntoInicio[0] + puntosMovimientos[i][0], puntoInicio[1] + puntosMovimientos[i][1])
            siguiente = laberintoSol[siguientePunto[0]][siguientePunto[1]]
            print("########\nActual: ", actual, "\tsiguiente: ", siguiente, " direccion: ",letrasMovimientos[i])
            movimientosValido = bool(list(prolog.query("permiteMovimiento(%s,'%s',%s)."%(actual, letrasMovimientos[i],siguiente)))) #prolog evalua si el movimiento se puede realizar
            if movimientosValido:
                if solucionarLaberinto2(laberintoSol, siguientePunto, puntoFinal):
                    solucionLaberinto.append(puntoInicio)
                    return True
    return False  # El laberinto no tiene solución


    ##############################################################################################
def solicitarSugerencia():
    global solucionLaberinto,tablero,numeroSugerencias, movRepeticion
    if numeroSugerencias>0:
        obtenerSolucion()
        if solucionLaberinto !=[]:
            sugerencia = solucionLaberinto[1]
            movRepeticion += [["sugerencia",sugerencia[0], sugerencia[1]]]
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
    


def crearTablero(ventanaTablero,laberintoTablero):
    global ventana, laberinto, colores, tablero,flechas
    x = 550
    y = 550
    print("---------------------------------"+str(x))
    tablero = tk.Frame(ventanaTablero)
    tablero.config(width=x ,height=y)
    tablero.grid(column=0,row=0)
    #
    #tablero.columnconfigure(0,weight=1)
    cantFilas= len(laberintoTablero)
    cantCol = len(laberintoTablero[0])
    numFila= 0
    numCol = 0
    for i in laberintoTablero:
        tablero.grid_rowconfigure(numFila,minsize=y/cantFilas,weight=1,uniform="crearTab")
        for j in i:

            tablero.grid_columnconfigure(numCol,minsize=x/cantCol,weight=1, uniform="crearTab")
            try:

                ficha = tk.Label(tablero, text=j,background=colores[j],foreground=colores[j]).grid(column=numCol, row=numFila, sticky=NSEW)
            except:
                return False
            numCol +=1
        numFila +=1
        numCol = 0
    return tablero
    


def autoSolucionar():
    global solucionLaberinto, gano, movRepeticion
    obtenerSolucion()
    if solucionLaberinto !=[]:
        gano = "auto"
        for i in solucionLaberinto:
            movRepeticion += [["auto",i[0],i[1]]]
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
    

def obtenerSolucion():
    global  posX, posY, finX, finY, solucionLaberinto
    solucionLaberinto = []
    laberintoTemp = deepcopy(laberinto)
    solucionarLaberinto2(laberintoTemp,(posX,posY),(finX, finY))
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
    global posX, posY,fichaAnterior, numeroMovimientos, tiempoInicio, laberinto,gano,movRepeticion
    if gano != "activo":
        print("el juego no está activo")
        return
    puntosMovimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    letrasMovimientos = ['w','s','a','d']
    siguientePunto = (posX + puntosMovimientos[i][0], posY + puntosMovimientos[i][1])
    if siguientePunto[0] in range(len(laberinto)) and siguientePunto[1] in range(len(laberinto[siguientePunto[0]])):
        movimientoValido = bool(list(prolog.query("permiteMovimiento(%s,%s,%s)."%(fichaAnterior,letrasMovimientos[i],laberinto[siguientePunto[0]][siguientePunto[1]]))))
        if movimientoValido and gano == "activo":
            movRepeticion += [["normal",siguientePunto[0],siguientePunto[1]]]
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
                movRepeticion += [["exitosa",-1,-1]]
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