import os
from tkinter import font
from pyswip import Prolog
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image  
from copy import deepcopy
from datetime import datetime
import uuid
from scroll import ScrollableFrame


"""
getVentana
E: Ninguna
S: Una Ventana
R: Los recursos solicitados deben existir
O: Crear una ventana para el programa
"""
def getVentana():
    global ventana
    ventana = Tk()
    ventana.iconbitmap("img/icono.ico")
    ventana.title("Laberinto")
    x = 1280
    y = 720

    cambiarTama(x,y)
    ventana.columnconfigure(0,weight=1, uniform="vent")
    ventana.rowconfigure(0,weight=1)
    ventana.resizable(width=False, height=False)
    return ventana



"""
cambiarTama(x,y)
E: x->Ancho de la ventana, y-> alto de la ventana
S: Cambio del tamaño de ventana
R: Los parametros deben ser numericos
O: Cambiar el tamaño de la ventana
"""
def cambiarTama(x, y):
    global ventana
    anchoPantalla = ventana.winfo_screenwidth()
    altoPantalla = ventana.winfo_screenheight()
    centroX = int(anchoPantalla/2 - x / 2)
    centroY = int(altoPantalla/2 - y / 2)
    ventana.geometry(f'{x}x{y}+{centroX}+{centroY}')


ventana = getVentana()
prolog = Prolog()
prolog.consult("logica.pro")

rutaArchivoLaberinto = ""
laberinto = []
tablero = []
posX = 0
posY = 0
inicioX = 0
inicioY=0
finX = 0
finY = 0
gano = "inactivo"

fichaAnterior = "i"
colores = {"x": "#211438",
           "auto": "#9734FA",
           "sugerencia": "#9734FA",
           "O": "#71A85E",
           "◯": "#71A85E",
           "i": "#D7FA0F",
           "inicio": "#D7FA0F",
           "f": "#FA5041",
           "ar": "#C9429E",
           "ab": "#0A56AD",
           "ad": "#E28B48",
           "at": "#F4D03F",
           "inter": "#873600",
           "normal": "#71A85E",
           }
frames= {}
movRepeticion = []
nickname = "Jugador 1"
numeroMovimientos = 0
numeroSugerencias = 10
tiempoInicio = datetime.now()


"""
raise_frame(frame, x, y)
E: frame->un frame, (x,y) -> nuevas dimensiones de la ventana
S: Cambio grafico en la ventana
R: El frame debe existir y las dimensiones deben ser numericas
O: Cambiar la ventana actual
"""
def raise_frame(frame,x,y):
    cambiarTama(x,y)
    frame.tkraise()


"""
crearPaginaInicio
E: ninguna
S: Pagina inicio
R: Ninguna
O: Crear la pagina de inicio
"""
def crearPaginaInicio():
    global ventana,img
    cambiarTama(270,400)
    ventanaInicio  = crearFrame()
    ventanaInicio.tk_setPalette(background = "#1E1E1E")
    ventanaInicio
    ventanaInicio.columnconfigure(0, weight=1)
    ventanaInicio.rowconfigure(1, weight=1)
    frames['ventanaInicio'] = ventanaInicio
    img =ImageTk.PhotoImage(Image.open("img/inicio.jpg").resize((300,180), Image.Resampling.LANCZOS))

    imagenInicio  = tk.Label(ventanaInicio, image=img)
    imagenInicio.grid(row=0,column=0)

    frameBotones = Frame(ventanaInicio)
    frameBotones.grid(column=0, row=1, sticky=NSEW)
    frameBotones.columnconfigure(0, weight=1)
    frameBotones.rowconfigure((0,1),weight=1, uniform="frameBotones")

    botonJuegoNuevo= tk.Button(frameBotones, text ="Juego Nuevo", font="MS-Sans-Serif 11" ,command = lambda: crearPaginaPreJuego(), width=220, height=10,background="#4F67E0", foreground="white")
    botonJuegoNuevo.grid(column=0,row=0, padx = 20,sticky=EW, pady=(50,25))

    botonEstadisticas= tk.Button(frameBotones, text ="Estadisticas", font="MS-Sans-Serif 11" ,command = lambda: crearPaginaEstadisticas("ventanaInicio"), width=220, height=10, background="#4F67E0", foreground="white")
    botonEstadisticas.grid(column=0,row=1, padx=20, sticky=EW, pady=(25,50))


"""
crearPaginaPreJuego
E: Ninguna
S: Pagina pre juego
R: Se deben seleccionar nickname y laberinto 
O: Solicitar los datos para la creación del laberinto
"""  
def crearPaginaPreJuego():
    global ventana, laberintoSeleccionado, nickname
    cambiarTama(270,400)
    ventanaPreJuego  = crearFrame()
    frames['ventanaPreJuego'] = ventanaPreJuego

    tk.Label(ventanaPreJuego, text="Seleccionar laberinto", font="ms-sans-serif 14 bold").grid(row=0, column=0,columnspan=2, sticky="nw",padx=(20,0), pady=(30,0))
    tk.Label(ventanaPreJuego,text="Nickname: ").grid(row=1, column=0, sticky="w",padx=(20,0), pady=(25,0))

    nickname = tk.Entry(ventanaPreJuego, justify=LEFT, bg="#f1f1f1", fg="black")
    nickname.grid(row=2, column=0, columnspan=2, sticky="we", padx=20, ipady=6)

    tk.Label(ventanaPreJuego,text="Laberinto: ").grid(row=3, column=0, sticky="w", padx=20, pady=(30,0))
    laberintoSeleccionado = tk.StringVar(frames["ventanaPreJuego"],value=rutaArchivoLaberinto)
    tk.Label(ventanaPreJuego, textvariable=laberintoSeleccionado, borderwidth=1, relief="sunken",
             bg="#f1f1f1", fg="black", anchor="w").grid(row=4, column=0, columnspan=2, sticky="we", padx=20, ipady=6)

    botonArchivo = tk.Button(ventanaPreJuego, text ="Seleccionar laberinto", command = lambda: solicitarArchivo(), bg="#4F67E0", foreground="white")
    botonArchivo.grid(row=5, column=0, columnspan=2, sticky="we", padx=20, pady=(20,0), ipady=4)

    botonIniciarJuego = tk.Button(ventanaPreJuego, text ="Iniciar", command = lambda: iniciarJuego(), bg="#4F67E0", foreground="white")
    botonIniciarJuego.grid(row=6, column=1, sticky="we" ,padx=(5,20),pady=(50,0) , ipady=5)

    botonVolver = tk.Button(ventanaPreJuego, text ="Volver", command = lambda: raise_frame(frames["ventanaInicio"], 270,400), bg="#4F67E0", foreground="white")
    botonVolver.grid(row=6, column=0, sticky="we",padx=(20,5),pady=(50,0)  , ipady=5)

    ventanaPreJuego.grid_columnconfigure((0,1),weight=1, uniform="colPre")


"""
crearPaginaTablero
E: Ninguna
S: Pagina tablero
R: Se debe haber seleccionado un nombre y laberinto previamente
O: Brindar una interfaz para jugar
"""
def crearPaginaTablero():
    global ventana, contadorMov, contadorSug, gano, laberinto, tablero
    cambiarTama(1280,720)
    ventanaTablero  = crearFrame()
    frames['ventanaTablero'] = ventanaTablero
    ventanaTablero.grid(sticky=NSEW)
    ventanaTablero.columnconfigure((0,1,2),weight=1, uniform="elemTab")

    contadorSug = tk.StringVar(frames["ventanaTablero"],value="Sugerencias disponibles: "+str(numeroSugerencias))
    tk.Label(ventanaTablero,textvariable=contadorSug, bg="#4F67E0", fg="white", font="ms-sans-serif 14").grid(row=0, column=0, sticky=NSEW)

    tk.Label(ventanaTablero, textvariable=cronometro,  bg="#4F67E0", fg="white", font="ms-sans-serif 26").grid(row=0, column=1, sticky=NSEW)

    contadorMov = tk.StringVar(frames["ventanaTablero"],value="Numero de movimientos: "+str(numeroMovimientos))
    tk.Label(ventanaTablero,textvariable=contadorMov,  bg="#4F67E0", fg="white", font="ms-sans-serif 14").grid(row=0, column=2, sticky=NSEW)

    botSolicitarSugerencia= tk.Button(ventanaTablero, text ="Solicitar Sugerencia", command = lambda:solicitarSugerencia(botSolicitarSugerencia), bg="#4F67E0", foreground="white")
    botSolicitarSugerencia.grid(row=2, column=0, sticky=NSEW, padx=20,pady=(0,10))
    
    botonVerificar= tk.Button(ventanaTablero, text ="Verificar posición", command = lambda:verificar(botonVerificar), bg="#4F67E0", foreground="white")
    botonVerificar.grid(row=2, column=1, sticky=NSEW, padx=20,pady=(0,10), ipady=5)

    botonReiniciar= tk.Button(ventanaTablero, text ="Reiniciar", command = lambda:reiniciar(), bg="#4F67E0", foreground="white")
    botonReiniciar.grid( row=2, column=2, sticky=NSEW, padx=20,pady=(0,10), ipady=5)

    framebot = tk.Frame(ventanaTablero)
    framebot.grid(row=3, column=0, columnspan=3,sticky=NSEW)
    framebot.grid_columnconfigure((0,1), weight=1, uniform="elemTab2")
    
    botonSol= tk.Button(framebot, text ="Autosolucionar", command = lambda:autoSolucionar(), bg="#4F67E0", fg="white")
    botonSol.grid(row = 0, column=0, sticky=NSEW, padx=20, pady=(0,10), ipady=5)
    
    botonAbandonar= tk.Button(framebot, text ="Abandonar partida", command = lambda:abandonarPartida(), bg="#4F67E0", fg="white")
    botonAbandonar.grid(row = 0, column=1, sticky=NSEW, padx=20, pady=(0,10), ipady=5)
    
    frameTablero = Frame(ventanaTablero)
    frameTablero.grid(row=1,column = 0, columnspan=3, sticky=NSEW)
    frameTablero.rowconfigure(0, weight=1)
    frameTablero.columnconfigure((0,2), weight=1, uniform="col")
    tablero = crearTablero(frameTablero,laberinto)
    tablero.grid(row=0,column = 1, pady=15)

    frameCol0 = Frame(frameTablero)
    frameCol0.grid(row=0, column=0, sticky=NSEW)
    frameCol0.columnconfigure((0), weight=1, uniform="col1")
    frameCol0.rowconfigure((0,1,2,3,4), weight=1, uniform="row1")
    
    tk.Label(frameCol0, text="Permite movimiento hacia arriba", font="ms-sans-serif 10").grid(row=0, column=0,sticky=E)
    tk.Label(frameCol0, relief='raised', borderwidth=2, bg=colores["ar"]).grid(row=0, column=1,ipadx=13, ipady=5,padx=5, sticky=E)

    tk.Label(frameCol0, text="Permite movimiento hacia abajo", font="ms-sans-serif 10").grid(row=1, column=0,sticky=E)
    tk.Label(frameCol0, relief='raised', borderwidth=2, bg=colores["ab"]).grid(row=1, column=1,ipadx=13, ipady=5,padx=5, sticky=E)
    
    tk.Label(frameCol0, text="Permite movimiento hacia atras", font="ms-sans-serif 10").grid(row=2, column=0,sticky=E)
    tk.Label(frameCol0, relief='raised', borderwidth=2, bg=colores["at"]).grid(row=2, column=1,ipadx=13, ipady=5,padx=5, sticky=E)

    tk.Label(frameCol0, text="Permite movimiento hacia adelante", font="ms-sans-serif 10").grid(row=3, column=0,sticky=E)
    tk.Label(frameCol0, relief='raised', borderwidth=2, bg=colores["ad"]).grid(row=3, column=1,ipadx=13, ipady=5,padx=5, sticky=E)

    tk.Label(frameCol0, text="Permite movimiento en las cuatro direcciones", font="ms-sans-serif 10").grid(row=4, column=0,sticky=E)
    tk.Label(frameCol0, relief='raised', borderwidth=2, bg=colores["inter"]).grid(row=4, column=1,ipadx=13, ipady=5,padx=5, sticky=E)
   
    frameCol2 = Frame(frameTablero)
    frameCol2.grid(row=0, column=2, sticky=NSEW)
    frameCol2.columnconfigure((1), weight=1, uniform="col1")
    frameCol2.rowconfigure((0,1,2,3,4), weight=1, uniform="row1")

    tk.Label(frameCol2, text="Posición actual").grid(row=0, column=1,sticky=W)
    tk.Label(frameCol2, relief='raised', borderwidth=2,bg=colores["O"]).grid(row=0, column=0,ipadx=13, ipady=5,padx=5, sticky=W)

    tk.Label(frameCol2, text="Muro").grid(row=1, column=1,sticky=W)
    tk.Label(frameCol2, relief='raised', borderwidth=2, bg=colores["x"]).grid(row=1, column=0,ipadx=13, ipady=5,padx=5, sticky=W)
    
    tk.Label(frameCol2, text="Inicio").grid(row=2, column=1,sticky=W)
    tk.Label(frameCol2, relief='raised', borderwidth=2, bg=colores["i"]).grid(row=2, column=0,ipadx=13, ipady=5,padx=5, sticky=W)

    tk.Label(frameCol2, text="Final").grid(row=3, column=1,sticky=W)
    tk.Label(frameCol2, relief='raised', borderwidth=2, bg=colores["f"]).grid(row=3, column=0,ipadx=13, ipady=5,padx=5, sticky=W)

    tk.Label(frameCol2, text="Sugerencia/Autosolución").grid(row=4, column=1,sticky=W)
    tk.Label(frameCol2, relief='raised', borderwidth=2, bg = colores["sugerencia"]).grid(row=4, column=0,ipadx=13, ipady=5,padx=5, sticky=W)

    if not tablero:
        raise_frame(frames["ventanaPreJuego"],400,500)
    else:
        gano = "activo"


"""
crearPaginaFinal
E: Ninguna
S: Pagina final
R: El estado de juego no puede ser "activo"
O: Mostrar la información de la partida al momento de terminar
"""
def crearPaginaFinal():
    global ventana, tablero, movRepeticion,laberinto
    cambiarTama(1280,720)
    ventanaFinal = crearFrame()
    ventanaFinal.grid(sticky=NSEW)
    ventanaFinal.columnconfigure((0,1,2),weight=1, uniform="venFinal")
    ventanaFinal.rowconfigure((0,1,3), weight=1)
    ventanaFinal.rowconfigure(2, weight=1)
    frames['ventanaFinal'] = ventanaFinal

    tk.Label(ventanaFinal,text="Juego terminado", bg="#4F67E0", fg="white", font="ms-sans-serif 20").grid(column=1,row=0,sticky=NSEW)
    tk.Label(ventanaFinal,text="Nickname: "+nickname.get() , bg="#4F67E0", fg="white", font="ms-sans-serif 14").grid(column=0,row=0,sticky=NSEW)
    tk.Label(ventanaFinal,text="Finalizó por: "+gano , bg="#4F67E0", fg="white", font="ms-sans-serif 14").grid(column=2,row=0,sticky=NSEW)


    tk.Label(ventanaFinal,text="Sugerencias utilizadas: "+str(10-numeroSugerencias),bg="#4F67E0", fg="white", font="ms-sans-serif 14").grid(column=0,row=1,sticky=NSEW)
    tk.Label(ventanaFinal,textvariable=cronometro,bg="#4F67E0", fg="white", font="ms-sans-serif 16").grid(column=1,row=1,sticky=NSEW)
    tk.Label(ventanaFinal,text="Movimientos: "+str(numeroMovimientos),bg="#4F67E0", fg="white", font="ms-sans-serif 14").grid(column=2,row=1,sticky=NSEW)

    tablero = crearTablero(ventanaFinal,laberinto)
    tablero.grid(column=0,row=2,columnspan=3)
    
    if gano == "auto":
        mostrarSolucion(tablero)

    botonoEstadisticas = tk.Button(ventanaFinal, text ="Estadísticas", bg="#4F67E0", foreground="white",font="ms-sans-serif 12", command = lambda: crearPaginaEstadisticas("ventanaFinal"))
    botonoEstadisticas.grid(column=0, row=4, padx=50, ipady=5, pady=(0,15), sticky="we")

    botonoHome = tk.Button(ventanaFinal, text ="Volver a inicio", bg="#4F67E0", foreground="white", font="ms-sans-serif 12", command = lambda: raise_frame(frames["ventanaInicio"],270,400))
    botonoHome.grid(column=2, row=4, padx=50, ipady=5,pady=(0,15), sticky="we")
    idEstadistica = guardarEstadisticas(nickname.get(),numeroMovimientos, numeroSugerencias,cronometro.get(),gano)

    botonGuardarRepeticion = tk.Button(ventanaFinal, text ="Guardar repetición", bg="#4F67E0", foreground="white",font="ms-sans-serif 12",  command = lambda: guardarRepeticion(idEstadistica))
    botonGuardarRepeticion.grid(column=1, row=4, padx=50, ipady=5,pady=(0,15), sticky="we")


"""
crearPaginaEstadisticas
E: ventanaAnterior-> nombre de la ventana anterior para poder volver a ella
S: Pagina de estadisticas
R: Ninguna
O: Mostrar las estadisticas de las partidas
"""
def crearPaginaEstadisticas(ventanaAnterior):
    global ventana
    cambiarTama(1280,720)
    ventanaEstadisticas = crearFrame()
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
    botonVolver = tk.Button(ef1, text ="<", font="ms-sans-serif 18 bold",borderwidth=0, command = lambda: raise_frame(frames[ventanaAnterior],x,y))
    botonVolver.grid(column=0, row=0, sticky=W,padx=2, columnspan=1)
    tk.Label(ef1, text="Estadísticas",font="ms-sans-serif 18 bold").grid(column=1, row=0,sticky=W)
   
    indicesTabla = tk.Frame(ventanaEstadisticas)
    indicesTabla.grid(column=0, row=1,sticky=NSEW)
    indicesTabla.columnconfigure((0,1,2,3,4,5), weight=1, uniform="ef2Uni")
    tk.Label(indicesTabla, text="Nickname", font="ms-sans-serif 14", bg="#4F67E0", fg="white").grid(column=0, row=0, sticky= "we", ipady=10)
    tk.Label(indicesTabla, text="Movimientos", font="ms-sans-serif 14", bg="#4F67E0", fg="white").grid(column=1, row=0, sticky= "we", ipady=10)
    tk.Label(indicesTabla, text="Sugerencias", font="ms-sans-serif 14", bg="#4F67E0", fg="white").grid(column=2, row=0, sticky= "we", ipady=10)
    tk.Label(indicesTabla, text="Tiempo", font="ms-sans-serif 14", bg="#4F67E0", fg="white").grid(column=3, row=0, sticky= "we", ipady=10)
    tk.Label(indicesTabla, text="Tipo finalización", font="ms-sans-serif 14", bg="#4F67E0", fg="white").grid(column=4, row=0, sticky= "we", ipady=10)
    tk.Label(indicesTabla, text="Repetición", font="ms-sans-serif 14", bg="#4F67E0", fg="white").grid(column=5, row=0, sticky= "we", ipady=10)
 
    ef2Scroll = ScrollableFrame(ventanaEstadisticas)
    ef2Scroll.grid(column=0,row=2,sticky=NSEW)
    ef2 = ef2Scroll.scrollable_frame
    ef2.columnconfigure(0, weight=1)
    ef2.columnconfigure((0,1,2,3,4,5), weight=1, uniform="ef2Uni2")
    listaEstadisticas = getEstadisticas()
    fil = 1 
    for estadistica in listaEstadisticas:
        tk.Label(ef2, text=estadistica[1], font="ms-sans-serif 10", bg="#323232"  ).grid(column=0, row=fil, sticky="we",ipadx = 10,  ipady=5)
        tk.Label(ef2, text=estadistica[2], font="ms-sans-serif 10", bg="#323232" ).grid(column=1, row=fil, sticky="we",ipadx = 10,  ipady=5)
        tk.Label(ef2, text=estadistica[3],font="ms-sans-serif 10", bg="#323232"   ).grid(column=2, row=fil, sticky="we",ipadx = 10,  ipady=5)
        tk.Label(ef2, text=estadistica[4],font="ms-sans-serif 10" , bg="#323232"  ).grid(column=3, row=fil, sticky="we",ipadx = 10,  ipady=5)
        tk.Label(ef2, text=estadistica[5],font="ms-sans-serif 10", bg="#323232"   ).grid(column=4, row=fil, sticky="we",ipadx = 10,  ipady=5)
        if os.path.isfile("repeticiones/"+str(estadistica[0])+".txt") and os.path.isfile("laberintos/"+str(estadistica[0])+".txt"):

            tk.Button(ef2, text =" Ver repetición ",command = lambda x= estadistica: getPaginaRepeticion(x) , bg="#4F67E0", fg="white", font="ms-sans-serif 10").grid(column=5, row=fil, sticky="we",ipadx=25, padx=5, pady=4)
        else:
            tk.Button(ef2, text ="Repetición no disponible",state=DISABLED, bg="#4F67E0", fg="white", font="ms-sans-serif 10").grid(column=5, row=fil, sticky="we", ipadx=25, padx=5, pady=4)
        fil+=1


"""
getEstadisticas
E: Ninguna
S: lista de estadisticas almacenadas
R: Debe existir el archivo de estadisticas
O: Obtener un registro de todas las estadisticas almacenadas
"""
def getEstadisticas():
    archivoEstadisticas = open("estadisticas.txt","r")
    estadisticas = archivoEstadisticas.read()
    archivoEstadisticas.close()
    listaEstadisticasTemp = estadisticas.split("\n")
    listaEstadisticas = []
    for i in listaEstadisticasTemp:
        listaEstadisticas += [i.split(",")] 
    listaEstadisticas.pop(-1)
    return reversed(listaEstadisticas)


"""
getRepeticion
E: id-> id del archivo en donde se encuentra la repetición
S: lista de movimientos de la partida guardada
R: el id debe existir
O: Obtener la lista de movimientos de una repetición
"""
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


"""
getPaginaRepeticion
E: id-> id de la repeticion
S: Pagina repeticion
R: el id debe existir
O: Crear una pagina para reproducir la repetición
"""
def getPaginaRepeticion(id):
    global ventana, laberinto, nickname
    ventanaRepeticion = crearFrame()
    ventanaRepeticion.grid(sticky=NSEW)
    ventanaRepeticion.columnconfigure((0,1,2),weight=1, uniform="ventanaRepeticion")
    ventanaRepeticion.rowconfigure((0,1,3), weight=1)
    ventanaRepeticion.rowconfigure(2, weight=1)
    frames['ventanaRepeticion'] = ventanaRepeticion
    laberintoProlog = prolog.query("getLaberinto('%s',X)." % ("laberintos/"+str(id[0])+".txt"))
    laberintoRepeticion = transformarLaberinto(laberintoProlog)

    tk.Label(ventanaRepeticion,text="Repetición", bg="#4F67E0", fg="white", font="ms-sans-serif 18").grid(column=1,row=0,sticky=NSEW)
    tk.Label(ventanaRepeticion,text="Nickname: "+id[1] , bg="#4F67E0", fg="white", font="ms-sans-serif 12").grid(column=0,row=0,sticky=NSEW)
    tk.Label(ventanaRepeticion,text="Finalizó por: "+id[5] , bg="#4F67E0", fg="white", font="ms-sans-serif 12").grid(column=2,row=0,sticky=NSEW)


    tk.Label(ventanaRepeticion,text="Sugerencias utilizadas: "+id[3],bg="#4F67E0", fg="white", font="ms-sans-serif 12").grid(column=0,row=1,sticky=NSEW)
    tk.Label(ventanaRepeticion,text=id[4],bg="#4F67E0", fg="white", font="ms-sans-serif 14").grid(column=1,row=1,sticky=NSEW)
    tk.Label(ventanaRepeticion,text="Movimientos: "+id[2],bg="#4F67E0", fg="white", font="ms-sans-serif 12").grid(column=2,row=1,sticky=NSEW)


    frameTablero = Frame(ventanaRepeticion)
    frameTablero.grid(row=2,column = 0, columnspan=3, sticky=NSEW)
    frameTablero.rowconfigure(0, weight=1)
    frameTablero.columnconfigure((0,2), weight=1, uniform="col")
    tablero = crearTablero(frameTablero,laberintoRepeticion)
    
    frameCol0 = Frame(frameTablero)
    frameCol0.grid(row=0, column=0, sticky=NSEW)
    frameCol0.columnconfigure((0), weight=1, uniform="col1")
    frameCol0.rowconfigure((0,1,2,3,4), weight=1, uniform="row1")
    

    tk.Label(frameCol0, text="Permite movimiento hacia arriba", font="ms-sans-serif 10").grid(row=0, column=0,sticky=E)
    tk.Label(frameCol0, relief='raised', borderwidth=2, bg=colores["ar"]).grid(row=0, column=1,ipadx=13, ipady=5,padx=5, sticky=E)

    tk.Label(frameCol0, text="Permite movimiento hacia abajo", font="ms-sans-serif 10").grid(row=1, column=0,sticky=E)
    tk.Label(frameCol0, relief='raised', borderwidth=2, bg=colores["ab"]).grid(row=1, column=1,ipadx=13, ipady=5,padx=5, sticky=E)
    
    tk.Label(frameCol0, text="Permite movimiento hacia atras", font="ms-sans-serif 10").grid(row=2, column=0,sticky=E)
    tk.Label(frameCol0, relief='raised', borderwidth=2, bg=colores["at"]).grid(row=2, column=1,ipadx=13, ipady=5,padx=5, sticky=E)

    tk.Label(frameCol0, text="Permite movimiento hacia adelante", font="ms-sans-serif 10").grid(row=3, column=0,sticky=E)
    tk.Label(frameCol0, relief='raised', borderwidth=2, bg=colores["ad"]).grid(row=3, column=1,ipadx=13, ipady=5,padx=5, sticky=E)

    tk.Label(frameCol0, text="Permite movimiento en las cuatro direcciones", font="ms-sans-serif 10").grid(row=4, column=0,sticky=E)
    tk.Label(frameCol0, relief='raised', borderwidth=2, bg=colores["inter"]).grid(row=4, column=1,ipadx=13, ipady=5,padx=5, sticky=E)
   
    frameCol2 = Frame(frameTablero)
    frameCol2.grid(row=0, column=2, sticky=NSEW)
    frameCol2.columnconfigure((1), weight=1, uniform="col1")
    frameCol2.rowconfigure((0,1,2,3,4), weight=1, uniform="row1")

    tk.Label(frameCol2, text="Posición actual").grid(row=0, column=1,sticky=W)
    tk.Label(frameCol2, relief='raised', borderwidth=2,bg=colores["O"]).grid(row=0, column=0,ipadx=13, ipady=5,padx=5, sticky=W)

    tk.Label(frameCol2, text="Muro").grid(row=1, column=1,sticky=W)
    tk.Label(frameCol2, relief='raised', borderwidth=2, bg=colores["x"]).grid(row=1, column=0,ipadx=13, ipady=5,padx=5, sticky=W)
    
    tk.Label(frameCol2, text="Inicio").grid(row=2, column=1,sticky=W)
    tk.Label(frameCol2, relief='raised', borderwidth=2, bg=colores["i"]).grid(row=2, column=0,ipadx=13, ipady=5,padx=5, sticky=W)

    tk.Label(frameCol2, text="Final").grid(row=3, column=1,sticky=W)
    tk.Label(frameCol2, relief='raised', borderwidth=2, bg=colores["f"]).grid(row=3, column=0,ipadx=13, ipady=5,padx=5, sticky=W)

    tk.Label(frameCol2, text="Sugerencia/Autosolución").grid(row=4, column=1,sticky=W)
    tk.Label(frameCol2, relief='raised', borderwidth=2, bg = colores["sugerencia"]).grid(row=4, column=0,ipadx=13, ipady=5,padx=5, sticky=W)

    tk.Button(ventanaRepeticion, text ="Volver", bg="#4F67E0", fg="white", font="ms-sans-serif 14", width=350, command=lambda: raise_frame(frames["ventanaEstadisticas"],1280,720)).grid(column=1, row=3)
    if tablero:
        tablero.grid(row=0,column = 1, pady=15)
        repeticion = getRepeticion(id[0])
        reproducirRepeticion(tablero,repeticion[:-1])


"""
reproducirRepeticion(tablero, repeticion)
E: tablero->matriz de fichas , repetición->lista de movimientos
S: reproduccion de la repetición
R: deben existir tablero y archivo con el id indicado previamente
O: representar graficamente la repetición de la partida
"""
def reproducirRepeticion(tablero, repeticion):
    global ventana
    if repeticion != []:
        reproducirRepeticionAux(tablero,repeticion[0])
        repeticion.pop(0)
        tempo = 1300
        if repeticion != []:
            if repeticion[0][0] == "auto":
                tempo = 900
            ventana.after(tempo, reproducirRepeticion, tablero, repeticion)


"""
reproducirRepeticionAux(tab, punto)
E: tab -> matriz de fichas, punto-> indice de la ficha a modificar
S: cambio grafico en una ficha especifica
R: el punto debe pertenecer al tablero 
O: Cambiar el color de la ficha segun el tipo de movimiento 
"""
def reproducirRepeticionAux(tab,punto):
    global colores,ventana
    child = tab.winfo_children()
    for i in child:
        infoGrid = i.grid_info()
        pos = (infoGrid["row"], infoGrid["column"])
        if pos == (int(punto[1]),int(punto[2])):
            if punto[0] =="sugerencia":
                parpadear(i,colores[punto[0]],"#71A85E",6)
            else:
                i.config(bg= colores[punto[0]], fg = colores[punto[0]])


"""
parpadear
E: objeto -> objeto a resaltar, (col1, col2) ->colores , cant ->cantidad de veces a repetir el cambio
S: Cambio grafico de la ficha
R: El objeto debe existir y tener una propiedad ["bg"], los colores deben ser validos y cant >0
O: Cambia los colores de un objeto para que este parpadee graficamente
"""
def parpadear(objeto, col1, col2, cant):
    global ventana
    if cant != 0:
        objeto.config(bg = col1, fg =col1)
        ventana.after(int(1300/cant),parpadear,objeto,col2,col1,cant-1)


"""
reiniciar
E: ninguna
S: reinicio del juego
R: ninguna
O: Reinicia el laberinto y guarda la partida como abandono
"""
def reiniciar():
    global movRepeticion
    guardarEstadisticas(nickname.get(),numeroMovimientos, numeroSugerencias,cronometro.get(),"abandono")
    movRepeticion += [["reinicio",-1,-1]]
    iniciarJuego()


"""
guardarEstadisticas
E: pNickname-> nickname del usuario , pCantmov->cantidad de movimientos realizados, 
    pCantSug->cantidad de sugerencias solicitadas, pTiempo -> tiempo que tardo en completar el laberinto, pTipoFin ->de que manera termino el laberinto
S: id de la nueva entrada
R: nicname, tiempo y tipofin deben ser cadenas de text
O: Guardar la partida terminada en estadisticas
"""
def guardarEstadisticas(pNickname, pCantmov, pCantSug,pTiempo, pTipoFin):
    estadisticas = open("estadisticas.txt","a")
    id = uuid.uuid1().hex
    nuevaEstadistica = str(id)+","+pNickname+","+str(pCantmov)+","+str(10-pCantSug)+","+str(pTiempo)+","+pTipoFin+"\n"
    estadisticas.write(nuevaEstadistica)
    estadisticas.close()
    return id


"""
guardarRepeticion
E: id -> id de la partida recien registrada en estadisticas
S: nuevo archivo de repetición
R: ninguna
O: guardar la repetición y el laberinto jugado en sus respectivas carpetas
"""
def guardarRepeticion(id):
    global movRepeticion,rutaArchivoLaberinto, frames
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

    crearPaginaEstadisticas("ventanaFinal")


"""
crearFrame
E: ninguna
S: Nuevo frame
R: Debe existir ventana
O: Crear un nuevo frame
"""
def crearFrame():
    global ventana
    frame = tk.Frame(ventana, height=720)
    frame.grid(column=0, row=0, sticky=NSEW)
    return frame


"""
solicitarArchivo
E: ningua
S: ruta del archivo seleccionado
R: ninguna
O: Seleccionar el laberinto que se desea jugar
"""
def solicitarArchivo():
    global rutaArchivoLaberinto, laberintoSeleccionado
    rutaArchivoLaberinto = filedialog.askopenfilename()
    laberintoSeleccionado.set(rutaArchivoLaberinto)


"""
reestablecerValores
E: ninguna
S: valores en su estado inicial
R: ninguna
O: Reestablece todos los valores a su estado inicial
"""
def reestablecerValores ():
    global posX,posY, inicioX, inicioY, finX, finY, gano,numeroMovimientos, numeroSugerencias, tiempoInicio,cronometro, movRepeticion
    posX = 0
    posY = 0
    inicioX = 0
    inicioY = 0
    finX = 0
    finY = 0
    gano = "inactivo"
    numeroMovimientos = 0
    numeroSugerencias = 10
    tiempoInicio = datetime.now()
    cronometro.set(getTiempo())
    movRepeticion = []


"""
iniciarJuego
E: ninguna
S: Inicio del juego 
R: se debe haber indicado nickname y laberinto
O: Iniciar la partida
"""
def iniciarJuego():
    global laberintoSeleccionado, laberinto
    reestablecerValores()  
    if nickname.get() != "":
        if laberintoSeleccionado.get() != "":
            laberintoProlog = prolog.query("getLaberinto('%s',X)." % (laberintoSeleccionado.get()))
            laberinto = transformarLaberinto(laberintoProlog)
            obtenerPosicionInicial()
            crearPaginaTablero()


"""
transformarLaberinto
E: laberintoProlog -> matriz del laberinto en formato de prolog
S: matriz del laberinto formato python
R: ninguna
O: Parsear la entrada recibida por prolog
"""
def transformarLaberinto(laberintoProlog):
    laberinto = []
    for i in laberintoProlog: 
        for j in i["X"]:
            fila = []
            for k in j:
                elemento = k.decode("utf-8") #transformar de byte a string
                fila += [elemento]
            laberinto += [fila]
    return laberinto


"""
obternerPosicionInicial
E: ninguna
S: posiciones iniciales y finales del laberinto
R: debe existir un laberinto cargado
O: Obtener las posiciones del laberinto
"""
def obtenerPosicionInicial():
    global laberinto, posX, posY, finX, finY,fichaAnterior,numeroMovimientos,  movRepeticion, inicioX, inicioY
    numeroMovimientos = 0
    x = 0
    y = 0
    for i in laberinto:
        for j in i:
            if j == 'i':
                posX = x
                posY = y
                inicioX = x
                inicioY = y
                laberinto[posX][posY]="O"
                movRepeticion += [["inicio",x,y]]
            if j == "f":
                finX = x
                finY = y
            y+=1
        x+=1
        y=0
    fichaAnterior = "i"


"""
abandonarPartida
E: ninguna
S: termina la partida
R: El juego debe haber comenzado
O: Abandonar una partida
"""
def abandonarPartida():
    global gano, movRepeticion
    gano = "abandono"
    movRepeticion +=[["abandono",-1,-1]]
    crearPaginaFinal()


solucionLaberinto= []


"""
solucionarLaberinto
E: laberintoSol -> laberinto a solucionar, puntoInicio -> punto de inicio del laberinto, puntoFinal -> punto final del laberinto
S: lista con los puntos solución del laberinto
R: puntoInicio y puntoFinal deben ser tuplas (x,y), laberintoSol una copia del laberinto original
O: Obtener solución del laberinto
este algoritmo fue basado en el siguiente articulo https://programmerclick.com/article/67791960095/ 
tomando en cuenta las diferencias entre los objetivos
""" 
def solucionarLaberinto(laberintoSol, puntoInicio, puntoFinal):
    actual = laberintoSol[puntoInicio[0]][puntoInicio[1]] #obtener actual
    if actual == "O" or actual =="◯":
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

"""
solicitarSugerencia
E: boton -> botono de solicitar sugerencia
S: cambio grafico en el punto sugerido y el boton de solicitar
R: Debe existir una solución
O: Obtener una sugerencia para el movimiento
"""
def solicitarSugerencia(boton):
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
                if sugerencia == pos:
                    i.config(bg="purple", fg = "purple")
                    ventana.after(3000,mostrarSugerencia,i)
                    numeroSugerencias -=1
                    contadorSug.set("Sugerencias disponibles: "+str(numeroSugerencias))
                    break
        else:
            boton["bg"]="red"
            boton["text"] = "No hay solución, GG"
    else:
        boton["bg"]="red"
        boton["text"] = "No quedan sugerencias"


"""
mostrarSugerencia
E: ficha -> ficha a sugerir
S: cambio grafico en ficha
R: ninguna
O: mostrar graficamente la sugerencia
"""
def mostrarSugerencia(ficha):
   ficha.config(bg=colores[ficha["text"]],fg=colores[ficha["text"]])
    

"""
crearTablero
E: ventanaTablero -> ventana en donde se creará el tablero, laberintoTablero-> laberinto en el que se basará el tablero
S: Representación grafica del laberinto en la ventana indicada
R: debe existir el laberinto y ventana indicados
O: Crear un tablero 
"""
def crearTablero(ventanaTablero,laberintoTablero):
    global ventana, laberinto, colores, tablero
    x = 550
    y = 550
    tablero = tk.Frame(ventanaTablero)
    tablero.config(width=x ,height=y)
    tablero.grid(column=0,row=0)
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
    

"""
autoSolucionar
E:boton -> boton de autosolución
S: Pagina final
R: el laberinto debe haber iniciado
O: solicitar autosolución del laberinto
"""
def autoSolucionar():
    global solucionLaberinto, gano, movRepeticion, posX, posY, inicioX, inicioY
    obtenerSolucion()
    if solucionLaberinto !=[]:
        gano = "auto"
        for i in solucionLaberinto:
            movRepeticion += [["auto",i[0],i[1]]]
        crearPaginaFinal()
    else:
        posX = inicioX
        posY = inicioY
        autoSolucionar()


"""
mostrarSolucion
E: tab ->tablero 
S: representasión grafica de la solución
R: debe existir una solución
O: representar graficamente la solución del laberinto
"""
def mostrarSolucion(tab):
    child = tab.winfo_children()
    for i in child:
        infoGrid = i.grid_info()
        pos = (infoGrid["row"], infoGrid["column"])
        i.config(bg=colores[i["text"]])
        if pos in solucionLaberinto:
            i.config(bg="purple", fg="white", text="◯")
    

"""
obtenerSolucion
E: ninguna
S: solicitud de solución del laberinto
R: ninguna
O: Solicitar la solucióndel laberinto
"""
def obtenerSolucion():
    global  posX, posY, finX, finY, solucionLaberinto
    solucionLaberinto = []
    laberintoTemp = deepcopy(laberinto)
    solucionarLaberinto(laberintoTemp,(posX,posY),(finX, finY))
    solucionLaberinto.reverse()
    
"""
verificar
E: boton -> botono de verificar posición
S: cambio grafico que indica si es valido o no 
R: ninguna
O: Indicar graficamente si la posición actual forma parte de la solución
"""   
def verificar(boton):
    global ventana, solucionLaberinto, gano
    obtenerSolucion()
    if solucionLaberinto !=[]:
        boton["bg"] = "green"
        boton["text"] = "✓"
        ventana.after(5000, verificarAux,boton)
    else:
        boton["bg"] = "red"
        boton["text"] = "✕"
        ventana.after(5000, verificarAux,boton)


"""
verificarAux
E: boton -> boton de verificar
S: reestablece la apariencia del boton
R: ninguna
O: reestablecer la apariencia del boton
"""
def verificarAux(boton):
    boton["bg"] = "#4F67E0"
    boton["text"] = "Verificar posición"

"""
moverFichaAux
E: fichaActual  -> posición actual en tablero , fichaSiguiente->destino en tablero 
S: cambio grafico del tablero
R: deben existir las posiciónes indicadas
O: Mover la ficha de manera grafica
"""
def moverFichaAux(fichaActual, fichaSiguiente):
    global tablero, fichaAnterior
    child = tablero.winfo_children()
    for i in child:
        infoGrid = i.grid_info()
        pos = (infoGrid["row"], infoGrid["column"])
        if fichaActual == pos:
            i["bg"] = colores[fichaAnterior]
            i["fg"] = colores[fichaAnterior]
            i["text"] = fichaAnterior
        elif fichaSiguiente == pos:
            i["bg"] = colores["O"]
            i["fg"] ="white"
            i["text"] ="◯"


"""
moverFicha
E: i-> indice representativo de la dirección
S: cambio de la posición de la ficha
R: el movimiento debe ser valido 
O: Mover la ficha en el tablero 
"""
def moverFicha(i):
    global posX, posY,fichaAnterior, numeroMovimientos, tiempoInicio, laberinto,gano,movRepeticion
    if gano != "activo":
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
            laberinto[siguientePunto[0]][siguientePunto[1]] = '◯'
            posY+=puntosMovimientos[i][1]
            posX+=puntosMovimientos[i][0]
            numeroMovimientos+=1
            contadorMov.set("Numero de movimientos: "+str(numeroMovimientos)) 
 
            if fichaAnterior =="f":
                gano = "exitosa"
                movRepeticion += [["exitosa",-1,-1]]
                crearPaginaFinal()
    
    if numeroMovimientos == 1:
        tiempoInicio = datetime.now()
        refrescarTiempo()


"""
moverIzquierda
E: evento de presionar la tecla direccional
S: Solicitud de mover la ficha
R: ninguna
O: Detectar la entrada de la tecla
"""
def moverIzquierda(event):
    moverFicha(2)
    

"""
moverDerecha
E: evento de presionar la tecla direccional
S: Solicitud de mover la ficha
R: ninguna
O: Detectar la entrada de la tecla
"""
def moverDerecha(event):
    moverFicha(3)
    

"""
moverArriba
E: evento de presionar la tecla direccional
S: Solicitud de mover la ficha
R: ninguna
O: Detectar la entrada de la tecla
"""
def moverArriba(event):
    moverFicha(0)


"""
moverAbajo
E: evento de presionar la tecla direccional
S: Solicitud de mover la ficha
R: ninguna
O: Detectar la entrada de la tecla
"""
def moverAbajo(event):
    moverFicha(1)


"""
formatearTiempo
E: segundos ->cantidad de segundos transcurridos
S: Formato de tiempo en horas:minutos:segundos
R: segundos debe ser un numero entero
O: Darle formato al tiempo del cronometro
"""    
def formatearTiempo(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas*60*60
    minutos = int(segundos/60)
    segundos -= minutos*60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


"""
getTiempo
E: hora del sistema
S: tiempo transcurrido
R: ninguna
O: Obtener el tiempo transcurrido
"""
def getTiempo():
    segundos_transcurridos= (datetime.now() - tiempoInicio).total_seconds()
    return formatearTiempo(int(segundos_transcurridos))

"""
refrescarTiempo
E: Ninguna
S: Actualiza el tiempo una vez realizado el primer movimiento 
R: El juego debe estar en espera
O: Arrancar el cronometro
"""
def refrescarTiempo():
    global ventana
    if numeroMovimientos >=1 and gano == "activo":
        cronometro.set(getTiempo())
        ventana.after(500, refrescarTiempo)

#la funcionalidad del cronometro se basa en esta implementación https://parzibyte.me/blog/2021/08/23/cronometro-tkinter-python/
cronometro = tk.StringVar(ventana, value=getTiempo())

crearPaginaInicio()
ventana.bind("<Left>", moverIzquierda)
ventana.bind("<Right>", moverDerecha)
ventana.bind("<Up>", moverArriba)
ventana.bind("<Down>", moverAbajo)

ventana.mainloop()