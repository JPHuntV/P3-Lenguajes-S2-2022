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


test([],_,_).
test([H|T],X,Y):-
    write(H),
    nth0(X, [H|T], Row),
    %nth0(C,Row,V),
    write(Row),nl,
    test(T,X,Y).
    
