#!/usr/bin/python3
# Cracker Barrel peg puzzle: 
# see https://shop.crackerbarrel.com/toys-games/games/travel-games/peg-game/606154

# from,over,to : describes moves
moves = (
  (0,1,3),
  (0,2,5),
  (1,3,6),
  (1,4,8),
  (2,4,7),
  (2,5,9),
  (3,6,10),
  (3,7,12),
  (4,7,11),
  (4,8,13),
  (5,8,12),
  (5,9,14),
  (3,4,5),
  (6,7,8),
  (7,8,9),
  (10,11,12),
  (11,12,13),
  (12,13,14)
)

# generator for moves and their oposites
def step() :
  for m in moves :
    f,o,t = m
    yield m
    yield t,o,f

# builds cells, 1 if full 0 if empty  
# returns as a pair a count k of the full ones and the cells
def init(i) :
  cells = [1]*15
  cells[i] = 0
  return (14,cells)

# performs, if possible, a move
# given the current occupancy of the cells
def move(kd,fot) :
   k,d=kd
   f,o,t=fot
   if d[f]==1 and d[o]==1 and d[t]==0 :
     c=list(d)
     c[f]=0 # moved away
     c[o]=0 # remove jumped over
     c[t]=1 # landing here after jump
     return (k-1,c)
   else :
     return None

# generator that yields all possible solutions
# given a cell configuration
def solve(kd) :
   k,d=kd
   if k<2 :
     yield (None,kd)
   else :
     for m in step() :
       kc = move(kd,m)
       if kc :
         for r in solve(kc) :
           ms,newkd=r
           yield (m,ms),newkd

# sets initial position with empty at i
# picks first solution
# collects path made of moves to a list
def puzzle(i) :
  kd = init(i)
  ms,newkd = next(solve(kd))
  mlist = []
  while ms :
    m,ms = ms
    mlist.append(m)
  return kd,mlist,newkd  

# shows the result by printing out successive states
def show(kd) :
  k,d=kd
  lines = [(4,0,0),(3,1,2),(2,3,5),(1,6,9),(0,10,14)]
  for l in lines :
    t,a,b=l
    tab=' '*t
    print(tab,end='')
    for i in range(a,b+1) :
      if d[i]==0 : c='. '
      else : c = 'x '
      print(c,end='')
    print('')
  print('') 

# replay a sequence of moves, showing the state of cells  
def replay(ms,kd) :  
   for m in ms :
     show(kd)
     #print(kd)
     k,d=kd
     d=list(d)
     f,o,t=m
     d[f]=0
     d[o]=0
     d[t]=1
     kd=k-1,d
   show(kd)

# prints out a terse view of solutions for each missing peg   
def terse() :
  for i in range(15) :
    kd1,ms,kd2 = puzzle(i)  
    print(kd1)
    for m in ms : print(m)
    print(kd2)
    print('')

# visualizes a solution for each first 5 positions
# others look the same after 120 degrees rotations
def go() :
  for i in range(5) :
    print('='*3,i,'='*3)
    kd1,ms,kd2 = puzzle(i)  
    replay(ms,kd1)
    print('')
  
'''
>>> go()
=== 0 ===
    . 
   x x 
  x x x 
 x x x x 
x x x x x 

    x 
   . x 
  . x x 
 x x x x 
x x x x x 

    x 
   x x 
  . . x 
 x x . x 
x x x x x 

    x 
   x x 
  x . x 
 . x . x 
. x x x x 

    x 
   . x 
  . . x 
 x x . x 
. x x x x 

    x 
   . x 
  . x x 
 x . . x 
. . x x x 

    x 
   . . 
  . . x 
 x x . x 
. . x x x 

    x 
   . x 
  . . . 
 x x . . 
. . x x x 

    . 
   . . 
  . . x 
 x x . . 
. . x x x 

    . 
   . . 
  . . x 
 . . x . 
. . x x x 

    . 
   . . 
  . . x 
 . . x . 
. x . . x 

    . 
   . . 
  . . . 
 . . . . 
. x x . x 

    . 
   . . 
  . . . 
 . . . . 
. . . x x 

    . 
   . . 
  . . . 
 . . . . 
. . x . . 


=== 1 ===
...
etc.

'''
  
