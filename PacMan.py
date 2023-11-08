import keyboard
import time
import random
import os
import json
clear = lambda: os.system("cls")

with open("levels.json") as map: data = json.load(map)
map = data["level1"]

units_pos = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
units_future_pos = units_pos.copy()
tile = [0, 0, 0, 0]
direction = [4, 4, 4, 4, 4]
turn, turns, score, scoreMax = 0, 0, 0, 0
pattern = ["focus", "ambush", "avoid", "random"]

def loadLevel():
    global score, scoreMax, units_pos, units_future_pos

    # Calcul du score max
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 3:
                score += 10
            if map[i][j] == 5:
                score += 50
    scoreMax = score
    score = 0

    # On remplit le tableau avec les units_positions des unités
    for i in range(len(map)):
        for j in range(len(map[0])):
            match map[i][j]:
                case 2:
                    units_pos[0][0], units_pos[0][1] = i, j
                case 4:
                    units_pos[1][0], units_pos[1][1] = i, j
                case 6:
                    units_pos[2][0], units_pos[2][1] = i, j
                case 7:
                    units_pos[3][0], units_pos[3][1] = i, j
                case 8:
                    units_pos[4][0], units_pos[4][1] = i, j

    units_future_pos = units_pos.copy()

def MoveUnits(pattern, id, unit, directUnit, tileUnit, obstacles):
    global units_future_pos
    new_x, new_y = unit[0], unit[1]
    targetX = units_pos[0][0] if pattern == "focus" else units_future_pos[0][0]
    targetY = units_pos[0][1] if pattern == "focus" else units_future_pos[0][1]

    if   keyboard.is_pressed('up')   : direction[0] = 0
    elif keyboard.is_pressed('down') : direction[0] = 1
    elif keyboard.is_pressed('left') : direction[0] = 2
    elif keyboard.is_pressed('right'): direction[0] = 3

    if  random.randint(1, 2) == 1  and                                           \
        direction[directUnit] == 0 and map[unit[0] - 1][unit[1]] in obstacles or \
        direction[directUnit] == 1 and map[unit[0] + 1][unit[1]] in obstacles or \
        direction[directUnit] == 2 and map[unit[0]][unit[1] - 1] in obstacles or \
        direction[directUnit] == 3 and map[unit[0]][unit[1] + 1] in obstacles or \
        direction[directUnit] == 4: 
        match pattern:
            case "focus" | "ambush":
                if   targetX < unit[0]: direction[directUnit] = 0 if map[unit[0] - 1][unit[1]] not in obstacles else random.randint(2, 3)
                elif targetX > unit[0]: direction[directUnit] = 1 if map[unit[0] + 1][unit[1]] not in obstacles else random.randint(2, 3)
                elif targetY < unit[1]: direction[directUnit] = 2 if map[unit[0]][unit[1] - 1] not in obstacles else random.randint(0, 1)
                else:                   direction[directUnit] = 3 if map[unit[0]][unit[1] + 1] not in obstacles else random.randint(0, 1)
            case "escape":
                if   targetX < unit[0]: direction[directUnit] = 1 if map[unit[0] - 1][unit[1]] not in obstacles else random.randint(2, 3)
                elif targetX > unit[0]: direction[directUnit] = 0 if map[unit[0] + 1][unit[1]] not in obstacles else random.randint(2, 3)
                elif targetY < unit[1]: direction[directUnit] = 3 if map[unit[0]][unit[1] - 1] not in obstacles else random.randint(0, 1)
                else:                   direction[directUnit] = 2 if map[unit[0]][unit[1] + 1] not in obstacles else random.randint(0, 1)
            case "random": direction[directUnit] = random.randint(0, 3)
            case _: pass
    
    if   direction[directUnit] == 0: new_x, new_y = unit[0] - 1, unit[1]
    elif direction[directUnit] == 1: new_x, new_y = unit[0] + 1, unit[1]
    elif direction[directUnit] == 2:
        if unit == [11,0]: # Téléportation gauche-droite
            map[11][18] = id
            map[11][0]  = 0
        new_x, new_y = unit[0], unit[1] - 1
    elif direction[directUnit] == 3:
        if unit == [11,19]: # Téléportation droite-gauche
            map[11][0]  = id
            map[11][18] = 0
        new_x, new_y = unit[0], unit[1] + 1
    
    if map[new_x][new_y] not in obstacles:
        if pattern == "player":
            map[unit[0]][unit[1]] = 0
            units_future_pos[0] = [new_x, new_y]
            return
        
        map[unit[0]][unit[1]] = tile[tileUnit]       # On efface le fantôme
        if map[new_x][new_y] != 2:                   # Dans tous les cas sauf si c'est PacMan
            tile[tileUnit] = map[new_x][new_y]       # On enregistre l'element de la case ciblée  
        units_future_pos[tileUnit + 1] = [new_x, new_y]

    elif pattern == "random": MoveUnits("random", 8, units_pos[4], 4, 3, [1, 4, 6, 7])
      
# Déplaçement de tous les fantômes
def Move():
    MoveUnits("player"  , 2, units_pos[0], 0, None, [1]         )
    MoveUnits(pattern[0], 4, units_pos[1], 1,    0, [1, 6, 7, 8])
    MoveUnits(pattern[1], 6, units_pos[2], 2,    1, [1, 4, 7, 8])
    MoveUnits(pattern[2], 7, units_pos[3], 3,    2, [1, 4, 6, 8])
    MoveUnits(pattern[3], 8, units_pos[4], 4,    3, [1, 4, 6, 7])

def update():
    global units_pos, score, pattern, turns, turn, direction
    turns += 1
    # Les valeurs associées aux éléments sur la carte
    element_values = {
        3: 10,
        5: 50,
        4: 100,
        6: 100,
        7: 100,
        8: 100
    }

    # Mettre à jour le score en fonction de la nouvelle units_position de Pac-Man
    element_value = element_values.get(map[units_future_pos[0][0]][units_future_pos[0][1]], 0)
    score += element_value

    if element_value == 50: 
        turn = turns
        for i in range(len(pattern))     : pattern[i]   = "escape"
        for i in range(1, len(direction)): direction[i] = 4
    if turn + 40 == turns : 
        pattern[0] = "focus"
        pattern[1] = "ambush"
        pattern[2] = "avoid"
        pattern[3] = "random"
        for i in range(1, len(direction)): direction[i] = 4
        turn = 0
    
    if turn != 0 and turn + 40 > turns:
        print("Bonus activé !")
        if   units_future_pos[0] == units_future_pos[1]: units_future_pos[1] = [10,  8]
        elif units_future_pos[0] == units_future_pos[2]: units_future_pos[2] = [10, 10]
        elif units_future_pos[0] == units_future_pos[3]: units_future_pos[3] = [12,  8]
        elif units_future_pos[0] == units_future_pos[4]: units_future_pos[4] = [12, 10]
    else:
        if units_future_pos[0] == units_future_pos[1] or \
           units_future_pos[0] == units_future_pos[2] or \
           units_future_pos[0] == units_future_pos[3] or \
           units_future_pos[0] == units_future_pos[4]: GameOver()

    elements_to_update = [2, 4, 6, 7, 8]
    for (x, y), element in zip(units_future_pos, elements_to_update):
        map[x][y] = element
        
    # Mettre à jour les units_positions des unités
    units_pos = units_future_pos

def render():
  clear()
  
  for lines in map:
    cell = ""
    for cells in lines:
      match cells:
          case 0 : cell += "\033[38;5;15m   "       # Espaces vides
          case 2 : cell += "\033[38;5;220m █ "      # PacMan (jaune)
          case 3 : cell += "\033[38;5;220m . "      # Points (jaune)
          case 4 : cell += "\033[38;5;196m ■ "      # Fantome rouge
          case 5 : cell += "\033[38;5;220m O "      # Bonus (jaune)
          case 6 : cell += "\033[38;5;206m ■ "      # Fantome rose
          case 7 : cell += "\033[38;5;33m ■ "       # Fantome bleu
          case 8 : cell += "\033[38;5;208m ■ "      # Fantome orange
          case _ : cell += "\033[38;5;45m███"       # Murs (bleu clair)
    print(cell)  

  print(f"Score : {score} / {scoreMax} points")

def GameOver(): input("You lose...\nAppuyez pour quitter"); exit()

def run():
  render()
  Move()
  update()

loadLevel()

while score < scoreMax:
  run()
  time.sleep(0.09)

print("You win !\nVoulez-vous rejouer ? (y/n)"); exit()