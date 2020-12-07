
def hacer_mat(n): #Crea la matriz tamaño

    M = []
    for i in range(n):
        a = ['o'] * n
        M.append(a)
    return M

def colocar_barcos(M, ships): #Coloca los bascos de la lista ships
    for x in range(len(ships)):
        M[ships[x][1]][ships[x][0]] = '1'
    return M
def mostrar(M): #Printea la matriz M
    print()
    for y in range(len(M)):
        for x in range(len(M[y])):
            print(M[y][x], end='')
        print()
def disparar(M, x, y, player1_boats): #Comprueba si una casilla tiene un barco o no
    player_boat_touch = False
    if M[y][x] == 'x' or M[y][x] == '~':
        print("Casilla ya comprobada")
    elif M[y][x] == 'o':
        M[y][x] = '~'
        print("Fallaste")
    else:
        M[y][x] = 'x'
        print("player_boat_touch")
        player_boat_touch = True
        while x-1 >= 0:
            if (M[y][x-1] == '1') or (M[y][x-1] == 'x'):
                x = x - 1
            else:
                break
        while y-1 >= 0:
            if (M[y-1][x] == '1') or (M[y-1][x] == 'x'):
                y = y - 1
            else:
                break
        B = 0 #Posicion del barco en la lista
        while B < len(player1_boats):
            if (player1_boats[B][0] == x) and (player1_boats[B][1] == y):
                player1_boats[B][3] = player1_boats[B][3] - 1
                if player1_boats[B][3] == 0:
                    M = tocado_y_hundido(M, player1_boats, B)
                    print("Barco {} hundido".format(player1_boats[B]))
                    player1_boats.remove(player1_boats[B])
                break
            B = B + 1
    return M, player1_boats,player_boat_touch
def crear_barcos(M): #Busca por toda la matriz mini-player1_boats y los va añadiendo a player1_boats (lista de listas)
    player1_boats = []
    for y in range(len(M)):
        for x in range(len(M[y])):
            B = []
            if M[y][x] == '1':
                B = buscar_barco(M, x, y)
                if not (B in player1_boats):
                    player1_boats.append(B)
    return player1_boats
def buscar_barco(M, x, y): #crea una lista [posX, posY, tamaño, mini-player1_boats vivos, orientación (1 H, 2 V)]
    if M[y-1][x] == '1' and y - 1 >= 0:
        y = y-1
        while y-1 >= 0:
            if M[y-1][x] == '1':
                y = y-1
            else:
                break
        tam = 1
        while y+1 < len(M):
            if M[y+1][x] == '1':
                y = y+1
                tam = tam+1
            else:
                break
        A = [x, y+1-tam, tam, tam, 2]
    elif M[y][x-1] == '1' and x - 1 >= 0:
        x = x-1
        while x-1 >= 0:
            if M[y][x-1] == '1':
                x = x-1
            else:
                break
        tam = 1
        while x+1 < len(M):
            if M[y][x+1] == '1':
                x = x+1
                tam = tam+1
            else:
                break
        A = [x+1-tam, y, tam, tam, 1]
    else:
        if (x+2 > len(M[y])) and (y+2 > len(M)):
            A = [x, y, 1, 1, 1]
        elif x+2 > len(M[y]):
            tam = 1
            while y+1 < len(M):
                if M[y+1][x] == '1':
                    y = y+1
                    tam = tam+1
                else:
                    break
            A = [x, y+1-tam, tam, tam, 2]
        elif y+2 > len(M):
            tam = 1
            while x+1 < len(M):
                if M[y][x+1] == '1':
                    x = x+1
                    tam = tam+1
                else:
                    break
            A = [x+1-tam, y, tam, tam, 1]
        else:
            if M[y+1][x] == '1':
                tam = 1
                while y+1 < len(M):
                    if M[y+1][x] == '1':
                        y = y+1
                        tam = tam+1
                    else:
                        break
                A = [x, y+1-tam, tam, tam, 2]
            elif M[y][x+1] == '1':
                tam = 1
                while x+1 < len(M):
                    if M[y][x+1] == '1':
                        x = x+1
                        tam = tam+1
                    else:
                        break
                A = [x+1-tam, y, tam, tam, 1]
            else:
                A = [x, y, 1, 1, 1]
    return A #Comprueba si un mini-barco pertenece a un barco grande y lo devuelve en una lista [posX, posY, tamaño, mini-player1_boats a flote]
def detectar_errores(M, player1_boats):
    Error_player1 = 0
    X = 1
    Y = 1

    necesito = [5, 4, 3, 3, 2, 2, 2, 1, 1, 1]
    while (Error_player1 == 0) and (Y < len(M)):
        X = 1
        while (Error_player1 == 0) and (X < len(M[Y])):
            y = Y
            x = X
            if M[y][x] == '1':
                if M[y-1][x] == '1' :
                    while y-1 >= 0:
                        if M[y][x-1] == '1' or M[y-1][x] != '1':
                            break
                        else:
                            y = y-1
                    if M[y][x-1] == '1':
                        Error_player1 = Error_player1 + 1
                        print("ERROR: ",x,y)
                elif M[y][x-1] == '1' :
                    while x-1 >= 0:
                        if M[y-1][x] == '1' or M[y][x - 1] != '1':
                            break
                        else:
                            x = x-1
                    if M[y-1][x] == '1':
                        Error_player1 = Error_player1 + 1
                        print("ERROR: ",x,y)
            X = X+1
        Y = Y+1 #Suma 1 si hay dos player1_boats juntos (o más)
    for x in range(len(player1_boats)): #Suma 2 si hay player1_boats de tamaños incorrectos
        if (player1_boats[x][2] in necesito):
            necesito.remove(player1_boats[x][2])
        else:
            Error_player1 = Error_player1 + 2
            break
    if len(necesito) != 0:
        Error_player1 = Error_player1 + 2
    return Error_player1
def tocado_y_hundido(M, player1_boats, B):
    x = player1_boats[B][0]
    y = player1_boats[B][1]
    if player1_boats[B][4] == 1:
        if y-1 >= 0:
            for i in range(player1_boats[B][2]):
                M[y-1][x+i] = '~'
        if x-1 >= 0:
            M[y][x-1] = '~'
        if y+1 < len(M):
            for i in range(player1_boats[B][2]):
                M[y+1][x+i] = '~'
        if x+player1_boats[B][2] < len(M[y]):
            M[y][x+player1_boats[B][2]] = '~'
    else:
        if x-1 >= 0:
            for i in range(player1_boats[B][2]):
                M[y+i][x-1] = '~'
        if y-1 >= 0:
            M[y-1][x] = '~'
        if x+1 < len(M[y]):
            for i in range(player1_boats[B][2]):
                M[y+i][x+1] = '~'
        if y+player1_boats[B][2] < len(M):
            M[y+player1_boats[B][2]][x] = '~'
    return M
