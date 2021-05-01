# Dictionary:
# miniship = a position in the matrix with a fragment of a ship
# ships' head/ mi miniships' head = the most left or top miniship inside a big ship

def hacer_mat(n): #Creates an n by n matrix filled with 'o'

    M = []
    for i in range(n):
        a = ['o'] * n
        M.append(a)
    return M
def colocar_barcos(M, list_of_miniships): #Puts in the matrix M '1' in the positions in list_of_miniships
    for x in range(len(list_of_miniships)):
        M[list_of_miniships[x][1]][list_of_miniships[x][0]] = '1'
    return M
def mostrar(M): #Prints the matrix M in console
    print()
    for y in range(len(M)):
        for x in range(len(M[y])):
            print(M[y][x], end='')
        print()
def disparar(M, x, y, list_of_ships): #Checks if a position in matrix M[y][x] has a miniship
    player_boat_touch = False
    if M[y][x] == 'x' or M[y][x] == '~': #If the position has already been checked
        print("Casilla ya comprobada")
    elif M[y][x] == 'o': #If the position doesn't have a miniship
        M[y][x] = '~'
        print("Fallaste")
    else: #If the position has a miniship
        M[y][x] = 'x'
        print("player_boat_touch")
        player_boat_touch = True
        while x-1 >= 0: #Search for the miniships' head in X axis
            if (M[y][x-1] == '1') or (M[y][x-1] == 'x'):
                x = x - 1
            else:
                break
        while y-1 >= 0: #Search for the miniships' head in Y axis
            if (M[y-1][x] == '1') or (M[y-1][x] == 'x'):
                y = y - 1
            else:
                break
        position = 0 #Position of the ship in the list_of_ships
        while position < len(list_of_ships):
            if (list_of_ships[position][0] == x) and (list_of_ships[position][1] == y): #Search in list_of_ships the ship that contains the shooted miniship
                list_of_ships[position][3] = list_of_ships[position][3] - 1 #Reduce the ship living miniships
                if list_of_ships[position][3] == 0: #If the ship doen't have remaining miniships (it has sinked)
                    M = tocado_y_hundido(M, list_of_ships, position)
                    print("Barco {} hundido".format(list_of_ships[position]))
                    list_of_ships.remove(list_of_ships[position])
                break
            position = position + 1
    return M, list_of_ships, player_boat_touch
def crear_barcos(M): #Search over the matrix miniships and then add the big ship they are part of to list_of_ships
    list_of_ships = []
    for y in range(len(M)):
        for x in range(len(M[y])):
            ship = [] #Big ship of wich the miniship is part of
            if M[y][x] == '1':
                ship = buscar_barco(M, x, y)
                if not (ship in list_of_ships):
                    list_of_ships.append(ship)
    return list_of_ships
def buscar_barco(M, x, y): #Checks if a miniship is part of a big ship and returns it in a list [posX, posY, size, living miniships, orientation(1 Horizontal, 2 Vertical)]
    if M[y-1][x] == '1' and y - 1 >= 0: #If the ship is vertical
        y = y-1
        while y-1 >= 0: #Search for the miniships' head
            if M[y-1][x] == '1':
                y = y-1
            else:
                break
        size = 1
        while y+1 < len(M): #Calculate the big ship size
            if M[y+1][x] == '1':
                y = y+1
                size = size+1
            else:
                break
        A = [x, y+1-size, size, size, 2]
    elif M[y][x-1] == '1' and x - 1 >= 0: #If the ship is horizontal
        x = x-1
        while x-1 >= 0: #Search for the miniships' head
            if M[y][x-1] == '1':
                x = x-1
            else:
                break
        size = 1
        while x+1 < len(M): #Calculate the big ship size
            if M[y][x+1] == '1':
                x = x+1
                size = size+1
            else:
                break
        A = [x+1-size, y, size, size, 1]
    else: #If the miniship is already the ships' head or is in the left/supperior edge
        if (x+2 > len(M[y])) and (y+2 > len(M)): #If the miniship is at the bottom right vertex
            A = [x, y, 1, 1, 1]
        elif x+2 > len(M[y]): #If the miniship is at the right edge
            size = 1
            while y+1 < len(M): #Calculate the big ship size
                if M[y+1][x] == '1':
                    y = y+1
                    size = size+1
                else:
                    break
            A = [x, y+1-size, size, size, 2]
        elif y+2 > len(M): #If the miniship is at the bottom edge
            size = 1
            while x+1 < len(M): #Calculate the big ship size
                if M[y][x+1] == '1':
                    x = x+1
                    size = size+1
                else:
                    break
            A = [x+1-size, y, size, size, 1]
        else: #If the miniship is clearly the ships' head
            if M[y+1][x] == '1': #If the ship is horizontal
                size = 1
                while y+1 < len(M): #Calculate the big ship size
                    if M[y+1][x] == '1':
                        y = y+1
                        size = size+1
                    else:
                        break
                A = [x, y+1-size, size, size, 2]
            elif M[y][x+1] == '1': #If the ship is vertical
                size = 1
                while x+1 < len(M): #Calculate the big ship size
                    if M[y][x+1] == '1':
                        x = x+1
                        size = size+1
                    else:
                        break
                A = [x+1-size, y, size, size, 1]
            else: #If the ship is a 1 sized ship
                A = [x, y, 1, 1, 1]
    return A
def detectar_errores(M, list_of_ships): #Checks that the ships are legally placed
    error = 0 #Error
    X = 1
    Y = 1
    necesito = [5, 4, 3, 3, 2, 2, 2, 1, 1, 1] #Size and number of the ships needed
    while (error == 0) and (Y < len(M)): #Add 1 to error if al least one ship isn't linear (there are two crossed ships)
        X = 1
        while (error == 0) and (X < len(M[Y])):
            y = Y
            x = X
            if M[y][x] == '1':
                if M[y-1][x] == '1': #If the ship is vertical
                    while y-1 >= 0: #While there is space on the left
                        if M[y][x-1] == '1' or M[y-1][x] != '1': #If there is also a miniship above or there isn't a mini ship on the left
                            break
                        else:
                            y = y-1
                    if M[y][x-1] == '1': #Add error if a horizontal ship has a vertical segment
                        error = error + 1
                        print("ERROR: ",x,y)
                elif M[y][x-1] == '1': #If the ship is horizontal
                    while x-1 >= 0: #While there is space above
                        if M[y-1][x] == '1' or M[y][x - 1] != '1': #If there is also a miniship on the left or there isn't a mini ship above
                            break
                        else:
                            x = x-1
                    if M[y-1][x] == '1': #Add error if a vertical ship has an horizontal segment
                        error = error + 1
                        print("ERROR: ",x,y)
            X = X+1
        Y = Y+1
    for pos in range(len(list_of_ships)): #Add 2 to error if there aren't enought ships of the needed sizes
        if (list_of_ships[pos][2] in necesito): #Search in necesito the size of the ship in list_of_ships[pos] and remove it from necesito
            necesito.remove(list_of_ships[pos][2])
        else: #If it isn't there, then add a error
            error = error + 2
            break
    if len(necesito) != 0 and (error == 0 or error == 1): #In case there are more than needed ships add 2 to error
        error = error + 2
    return error
def tocado_y_hundido(M, list_of_ships, position): #Sorround the sinked ship with checked water (because there can't be a ship next to another)
    x = list_of_ships[position][0]
    y = list_of_ships[position][1]
    if list_of_ships[position][4] == 1: #If the ship is horizontal
        if y-1 >= 0:
            for i in range(list_of_ships[position][2]):
                M[y-1][x+i] = '~'
        if x-1 >= 0:
            M[y][x-1] = '~'
        if y+1 < len(M):
            for i in range(list_of_ships[position][2]):
                M[y+1][x+i] = '~'
        if x+list_of_ships[position][2] < len(M[y]):
            M[y][x+list_of_ships[position][2]] = '~'
    else: #If the ship is vartical
        if x-1 >= 0:
            for i in range(list_of_ships[position][2]):
                M[y+i][x-1] = '~'
        if y-1 >= 0:
            M[y-1][x] = '~'
        if x+1 < len(M[y]):
            for i in range(list_of_ships[position][2]):
                M[y+i][x+1] = '~'
        if y+list_of_ships[position][2] < len(M):
            M[y+list_of_ships[position][2]][x] = '~'
    return M
