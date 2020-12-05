
def hacer_mat(n): #Crea la matriz tamaño n
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
def disparar(M, x, y, barcos): #Comprueba si una casilla tiene un barco o no
    Tocado = False
    if M[y][x] == 'x' or M[y][x] == '~':
        print("Casilla ya comprobada")
    elif M[y][x] == 'o':
        M[y][x] = '~'
        print("Fallaste")
    else:
        M[y][x] = 'x'
        print("Tocado")
        Tocado = True
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
        while B < len(barcos):
            if (barcos[B][0] == x) and (barcos[B][1] == y):
                barcos[B][3] = barcos[B][3] - 1
                if barcos[B][3] == 0:
                    M = tocado_y_hundido(M, barcos, B)
                    print("Barco {} hundido".format(barcos[B]))
                    barcos.remove(barcos[B])
                break
            B = B + 1
    return M, barcos,Tocado
def crear_barcos(M): #Busca por toda la matriz mini-barcos y los va añadiendo a barcos (lista de listas)
    barcos = []
    for y in range(len(M)):
        for x in range(len(M[y])):
            B = []
            if M[y][x] == '1':
                B = buscar_barco(M, x, y)
                if not (B in barcos):
                    barcos.append(B)
    return barcos
def buscar_barco(M, x, y): #crea una lista [posX, posY, tamaño, mini-barcos vivos, orientación (1 H, 2 V)]
    if M[y-1][x] == '1':
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
    elif M[y][x-1] == '1':
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
                while y+1 <= len(M):
                    if M[y+1][x] == '1':
                        y = y+1
                        tam = tam+1
                    else:
                        break
                A = [x, y+1-tam, tam, tam, 2]
            elif M[y][x+1] == '1':
                tam = 1
                while x+1 <= len(M):
                    if M[y][x+1] == '1':
                        x = x+1
                        tam = tam+1
                    else:
                        break
                A = [x+1-tam, y, tam, tam, 1]
            else:
                A = [x, y, 1, 1, 1]
    return A #Comprueba si un mini-barco pertenece a un barco grande y lo devuelve en una lista [posX, posY, tamaño, mini-barcos a flote]
def detectar_errores(M, barcos):
    E = 0
    X = 1
    Y = 1
    necesito = [5, 4, 3, 3, 2, 2, 2, 1, 1, 1]
    while (E == 0) and (Y < len(M)):
        X = 0
        while (E == 0) and (X < len(M[Y])):
            y = Y
            x = X
            if M[y][x] == '1':
                if M[y-1][x] == '1':
                    while y-1 >= 0:
                        if M[y][x-1] == '1':
                            break
                        else:
                            y = y-1
                    if M[y][x-1] == '1':
                        E = E + 1
                elif M[y][x-1] == '1':
                    while x-1 >= 0:
                        if M[y-1][x] == '1':
                            break
                        else:
                            x = x-1
                    if M[y-1][x] == '1':
                        E = E + 1
            X = X+1
        Y = Y+1 #Suma 1 si hay dos barcos juntos (o más)
    for x in range(len(barcos)): #Suma 2 si hay barcos de tamaños incorrectos
        if (barcos[x][2] in necesito):
            necesito.remove(barcos[x][2])
        else:
            E = E + 2
            break
    if len(necesito) != 0:
        E = E + 2
    return E
def tocado_y_hundido(M, barcos, B):
    x = barcos[B][0]
    y = barcos[B][1]
    if barcos[B][4] == 1:
        if y-1 >= 0:
            for i in range(barcos[B][2]):
                M[y-1][x+i] = '~'
        if x-1 >= 0:
            M[y][x-1] = '~'
        if y+1 < len(M):
            for i in range(barcos[B][2]):
                M[y+1][x+i] = '~'
        if x+barcos[B][2] < len(M[y]):
            M[y][x+barcos[B][2]] = '~'
    else:
        if x-1 >= 0:
            for i in range(barcos[B][2]):
                M[y+i][x-1] = '~'
        if y-1 >= 0:
            M[y-1][x] = '~'
        if x+1 < len(M[y]):
            for i in range(barcos[B][2]):
                M[y+i][x+1] = '~'
        if y+barcos[B][2] < len(M):
            M[y+barcos[B][2]][x] = '~'
    return M
