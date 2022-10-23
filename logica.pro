splitFile(Archivo,X) :-
    read_file_to_string(Archivo, Res,[]),%archivo a string
    split_string(Res,".\n", ".\n", X). %string splitter

getLaberinto(Archivo,X):-
    splitFile(Archivo,X).


