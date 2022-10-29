movimientoValido(ad, d).
movimientoValido(ab, s).
movimientoValido(at, a).
movimientoValido(ar, w).

movimientoValido(inter, w).
movimientoValido(inter, s).
movimientoValido(inter, a).
movimientoValido(inter, d).

movimientoValido(i, w).
movimientoValido(i, s).
movimientoValido(i, a).
movimientoValido(i, d).

posValida(i).
posValida(f).
posValida(ad).
posValida(at).
posValida(ab).
posValida(ar).
posValida(inter).


permiteMovimiento(Ficha,Direccion,Siguiente):-
    movimientoValido(Ficha,Direccion),
    posValida(Siguiente).

splitFile(Archivo,X) :-
    read_file_to_string(Archivo, Res,[]),%archivo a string
    split_string(Res,".\n", ".\n", X). %string splitter
    
    

%getLaberinto(Archivo,X):-
%    splitFile(Archivo,X).


printList([]).
printList([X|Y]):-
    write(X),nl,
    printList(Y).

getLaberinto(Archivo,B):-
    %getLaberinto(Archivo,A),
    splitFile(Archivo,A),
    maplist(dividirFila, A,B).
    
dividirFila(X,Y):-
    split_string(X, ",", "[]", Y).



ttt(LaberintoSol,X,Y,FichaAnterior,Res):-
    Lista = [],
    nb_setval(soluGlobal,Lista),
    %b_setval(laberintoTest,LaberintoSol),
    test(LaberintoSol,X,Y,FichaAnterior,Res),
    nb_getval(soluGlobal,SoluFinal),
    nb_setval(continuar,0),
    write("Solucion: "),write(SoluFinal).


test([],_,_,_,Res):-
    nb_getval(soluGlobal,NuevoX),
    write(NuevoX),
    Res = NuevoX.
test(LaberintoSol,X,Y,FichaAnterior,Res):-
    nl,nl,
    nth0(0,X,PuntoInicio0),
    nth0(1,X,PuntoInicio1),
    %write(PuntoInicio0), write("\t"), write(PuntoInicio1),nl,
    

    %Actual
    nth0(PuntoInicio0, LaberintoSol, FilaActual),
    nth0(PuntoInicio1,FilaActual,Actual),

    b_setval(actual, Actual),
    b_getval(actual, Actual1),
    
    %write(FilaActual),write(Actual),write(Actual1),nl,
    (Actual1 = 'O' ->
        %write("Es igual"),
        b_setval(actual,FichaAnterior)
        ;
        %write("no es igual"),
        true),

    %write(Actual),nl,
    %marcar
    replace(FilaActual,PuntoInicio1,'v',ActualT),
    replace(LaberintoSol,PuntoInicio0,ActualT,ListaT),

    %b_setval(laberintoTest, ListaT),
    %b_getval(laberintoTest, LaberintoS1),
    %nl,write("Laberinto------------"),nl,
    %printList(ListaT),
    %if puntoInicio == puntoFinal: 
    write("X: "),write(X), write("Y: "),write(Y),nl,
    (X = Y ->
        write("agruego "),
        nb_getval(soluGlobal,Sg1),
        append(Sg1,[X],NuevoX),
        nb_setval(soluGlobal,NuevoX),
        test([],_,_,_,Res)
        ;

        PuntosMovimientos = [[-1, 0], [1, 0], [0, -1], [0, 1]],
        LetrasMovimientos = ['w','s','a','d'],
        b_getval(actual,Actual2),
        recorrerDireciones(0,4,X,PuntosMovimientos,LetrasMovimientos,ListaT,Actual2,Y,FichaAnterior)
        ),
    nb_setval(tt,0).
 
    
recorrerDireciones(M,N,X,PuntosMovimientos,LetrasMovimientos,LaberintoSol,Actual,PuntoFinal,FichaAnterior):-
    N1 is N-1,
    between(M, N1, I),
    nb_getval(soluGlobal,Test1),
    %write(Test1),
    %write(I),

    nth0(0,X,PuntoInicio0),
    nth0(1,X,PuntoInicio1),

    nth0(I, PuntosMovimientos, PuntoMovFil),
    nth0(0,PuntoMovFil,PuntoMov0),
    nth0(1,PuntoMovFil,PuntoMov1),

    SiguientePunto0 is PuntoInicio0 + PuntoMov0,
    SiguientePunto1 is PuntoInicio1 + PuntoMov1,
    SiguientePunto = [SiguientePunto0,SiguientePunto1],

    nth0(SiguientePunto0, LaberintoSol, FilaActual),
    nth0(SiguientePunto1,FilaActual,Siguiente),
    nth0(I,LetrasMovimientos,Letra),
    write("#####Actual: "),write(Actual),write("\tSiguiente: "),write(Siguiente),write(" direccion: "),write(Letra),nl,
    (permiteMovimiento(Actual,Letra,Siguiente),
    test(LaberintoSol,SiguientePunto,PuntoFinal,FichaAnterior,Res),
    write("resssssssssss:   "),write(Res),\+Res = []->
        nb_getval(soluGlobal, Sg3),
        append(Sg3,[X],NuevoX),
        nb_setval(soluGlobal,NuevoX)
  
    ),
    (
    (I >= N), !,
    recorrerDireciones(M,I,X,PuntosMovimientos,LetrasMovimientos,LaberintoSol,Actual,PuntoFinal,FichaAnterior)).


replace([_|T], 0, X, [X|T]).
replace([H|T], I, X, [H|R]):- 
    I > -1, 
    NI is I-1, 
    replace(T, NI, X, R), !.
replace(L, _, _, L).