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


test([],_,_,_,NuevoX,Res):-
    Res = NuevoX.
test(LaberintoSol,X,Y,FichaAnterior,Solucion,Res):-
    b_setval(laberintoTest,LaberintoSol),
    nth0(0,X,PuntoInicio0),
    nth0(1,X,PuntoInicio1),nl,nl,
    write(PuntoInicio0), write("\t"), write(PuntoInicio1),nl,
    
 
    %Actual
    nth0(PuntoInicio0, LaberintoSol, FilaActual),
    nth0(PuntoInicio1,FilaActual,Actual),

    b_setval(actual, Actual),
    b_getval(actual, Actual1),
    
    write(FilaActual),write(Actual),write(Actual1),nl,
    (Actual = 'O' ->
        write("Es igual"),
        b_setval(actual,FichaAnterior)
        ;
        write("no es igual"),
        true),

    write(Actual),nl,
    %marcar
    replace(FilaActual,PuntoInicio1,'v',ActualT),
    replace(LaberintoSol,PuntoInicio0,ActualT,ListaT),
    b_setval(laberintoTest, ListaT),
    b_getval(laberintoTest, LaberintoS1),
    write("Laberinto------------"),nl,
    printList(LaberintoS1),
    %if puntoInicio == puntoFinal: 
    (X = Y ->
        append(Solucion,[X],NuevoX),
        test([],_,_,_,NuevoX,Res)
        ;

        PuntosMovimientos = [[-1, 0], [1, 0], [0, -1], [0, 1]],
        LetrasMovimientos = ['w','s','a','d'],
        b_getval(laberintoTest,LaberintoS2),
        b_getval(actual,Actual2),
        recorrerDireciones(0,4,X,PuntosMovimientos,LetrasMovimientos,LaberintoS2,Actual2,Y,Solucion),
        %nl,write("estoy aqui"),
        Res = Solucion).
 
    
recorrerDireciones(M,N,X,PuntosMovimientos,LetrasMovimientos,LaberintoSol,Actual,PuntoFinal,Solucion):-
    N1 is N-1,
    between(M, N1, I),
    write(I),

    nth0(0,X,PuntoInicio0),
    nth0(1,X,PuntoInicio1),

    nth0(I, PuntosMovimientos, PuntoMovFil),
    write(PuntoMovFil),nl,
    nth0(0,PuntoMovFil,PuntoMov0),
    nth0(1,PuntoMovFil,PuntoMov1),

    SiguientePunto0 is PuntoInicio0 + PuntoMov0,
    SiguientePunto1 is PuntoInicio1 + PuntoMov1,
    SiguientePunto = [SiguientePunto0,SiguientePunto1],
    nl,write("Actual: "),write(Actual),nl,
    write("Siguiente punto: "),write(SiguientePunto),nl,
    nth0(SiguientePunto0, LaberintoSol, FilaActual),
    nth0(SiguientePunto1,FilaActual,Siguiente),
    write("Siguiente: "), write(Siguiente),nl,
    nth0(I,LetrasMovimientos,Letra),
    (permiteMovimiento(Actual,Letra,Siguiente)->
        write("si me puedo mover"),nl,nl,nl
        ;
        write("no me puedo mover"),nl,nl,nl
    ),
    I >= N, !.
    recorrerDireciones(M,I,X,PuntosMovimientos,LetrasMovimientos,LaberintoSol,Actual,PuntoFinal,Solucion).


replace([_|T], 0, X, [X|T]).
replace([H|T], I, X, [H|R]):- 
    I > -1, 
    NI is I-1, 
    replace(T, NI, X, R), !.
replace(L, _, _, L).