use_module(library(lists)).

moves(0,1,3).
moves(0,2,5).
moves(1,3,6).
moves(1,4,8).
moves(2,4,7).
moves(2,5,9).
moves(3,6,10).
moves(3,7,12).
moves(4,7,11).
moves(4,8,13).
moves(5,8,12).
moves(5,9,14).
moves(3,4,5).
moves(6,7,8).
moves(7,8,9).
moves(10,11,12).
moves(11,12,13).
moves(12,13,14).

step(Step, Reversed):-
    moves(F, O, T),
    Step     = [F, O, T],
    Reversed = [T, O, F].

init(I, Board):-
    length(L0, 14),
    maplist(=(1), L0),
    nth0(I, Cells, 0, L0),
    Board = [14, Cells].


set_at(Index, List, Val, OldVal, Result):-
    nth0(Index, List,   OldVal, BeforeSet),
    nth0(Index, Result, Val,    BeforeSet).

move(Board, Move, BoardAfterMove):-
    [PegsLeft | [CellList]] = Board,
    [F, O, T] = Move, NewPegsLeft is PegsLeft-1,
    (step(Move, _); step(_, Move)),
    set_at(F, CellList,     0, 1, NewCellList0),
    set_at(O, NewCellList0, 0, 1, NewCellList1),
    set_at(T, NewCellList1, 1, 0, NewCellListFinal),
    BoardAfterMove = [NewPegsLeft, NewCellListFinal].

solve([1, _], []).
solve(Board, Moves):-
    [Move | T] = Moves,
    move(Board, Move, BoardAfter),
    solve(BoardAfter, T).

puzzle(I, Moves):-
    init(I, Board),
    once(solve(Board, Moves)).

puzzle(I, Moves, Board):-
    init(I, Board),
    once(solve(Board, Moves)).


write_indices(_, []).
write_indices(CellList, Indices):-
    [H | T] = Indices,
    ((nth0(H, CellList, 0),write('. '));(nth0(H, CellList, 1),write('x '))),
    write_indices(CellList, T).

show(Board):-once(show(Board, [[4,0,0],[3,1,2],[2,3,5],[1,6,9],[0,10,14]])).
show(Board, LineDescs):-
    [_ | [CellList]] = Board,
    [LineDesc | Others] = LineDescs,
    [T, A, B] = LineDesc,
    tab(T),
    numlist(A, B, Indices),
    write_indices(CellList, Indices),
    nl,
    show(Board, Others).
    
show(_, []).


replay(_, []).
replay(Board, Moves):-
    [Move | TailMoves] = Moves,
    move(Board, Move, BoardAfter),
    show(BoardAfter),
    replay(BoardAfter, TailMoves).


print_elements([]).
print_elements(List):-
    [H | T] = List,
    print(H),nl,
    print_elements(T).


terse():-
    numlist(0, 14, Indices),
    terse(Indices).
        
terse([]).
terse(Indices):-
    [H | T] = Indices,
    puzzle(H, Moves, Board),
    print(Board),
    nl,
    print_elements(Moves),
    nl,
    nl,
    terse(T).
   

