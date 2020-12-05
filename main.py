import pygame
import random
import Flota

pygame.mixer.pre_init()
pygame.mixer.init(frequency = 44100, size = -16, channels = 2, buffer = 2**12)

channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)

fondo = pygame.mixer.Sound('fondo.mp3')
tocado_sound = pygame.mixer.Sound("tocado.mp3")
fallado_sound = pygame.mixer.Sound("fail.mp3")

channel1.play(fondo)

M = Flota.hacer_mat(10)
Flota.mostrar(M)
N = Flota.hacer_mat(10)
Flota.mostrar(N)

blueP = (20, 34, 238)
greenP = (20, 240, 50)
redP = (230, 0, 20)
yel = (255, 255, 0)
BLACK = (0, 0, 0)
sizeSquare = 60

mx = 0
my = 0

clas_x = 0
clas_y = 0

Start = False
Done = False

barcos = []
barcos_enem = []

Turno = 0
Tocado = None

num_of_cubes = 10
size = (1260, 600)
cube_size= int(size[1]/num_of_cubes)
line_thikness = 2
line_cube = cube_size - line_thikness


pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Battleships")
clock = pygame.time.Clock()
gameOver = False

while not gameOver:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
    screen.fill(BLACK)

    Fuente = pygame.font.Font('Alice and the Wicked Monster.ttf', 16)

    #Text variables
    Tx = 0
    Ty = 0
    for i in range(1, 600, cube_size):
        for j in range(1, size[1], cube_size):
            pygame.draw.rect(screen, blueP, [i, j, line_cube, line_cube], 0)

        Texto = Fuente.render(str(Tx), True, greenP)
        screen.blit(Texto, [i, 2])
        if Tx != 0:
            screen.blit(Texto, [2, i + 16])
        Tx += 1
        Ty = 0
    Tx = 0
    Ty = 0
    for i in range(660, 1260, cube_size):
        for j in range(1, size[1], cube_size):
            pygame.draw.rect(screen, blueP, [i, j, line_cube, line_cube], 0)

        Texto = Fuente.render(str(Tx), True, greenP)
        screen.blit(Texto, [i, 2])
        if Tx != 0:
            screen.blit(Texto, [2, i + 16])
        Tx += 1
        Ty = 0

    #Posicionar barcos
    mouse_buttons = pygame.mouse.get_pressed(num_buttons=3)

    if mouse_buttons[0] == True:
        mouse_pos = pygame.mouse.get_pos()
        mx = mouse_pos[0]
        my = mouse_pos[1]
        clas_y = 0
        clas_x = 0

        while mx > 60:
            mx = mx - 60
            clas_x = clas_x + 1
        while my> 60:
            my = my - 60
            clas_y = clas_y + 1

        if Start == True:
            if Turno == 0 and clas_x > 10:
                N,LL,Tocado = Flota.disparar(N, clas_x - 11, clas_y,LL)
                Flota.mostrar(N)


            elif Turno == 1 and clas_x < 10:
                M,L,Tocado = Flota.disparar(M, clas_x, clas_y,L)
                Flota.mostrar(M)
            if Tocado:
                channel2.play(tocado_sound)

            else:
                channel2.play(fallado_sound)


            print("TURNO: ",Turno)
        else:
            if clas_x != 10:
                if [clas_x, clas_y] not in barcos and clas_x < 10 and Turno == 0:
                    barcos.append([clas_x, clas_y])
                    print("1:",clas_x, clas_y)
                if [clas_x, clas_y] not in barcos_enem and clas_x > 9 and Turno == 1:
                    barcos_enem.append([clas_x - 11, clas_y])
                    print("2:",clas_x - 11, clas_y)

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        if Turno == 0:
            Turno = 1
        elif Turno == 1:
            Turno = 0

    if pygame.key.get_pressed()[pygame.K_RETURN]:
        if Turno == 0:
            M = Flota.colocar_barcos(M, barcos)
            Flota.mostrar(M)
            L = Flota.crear_barcos(M)
            print(L)
            E = Flota.detectar_errores(M, L)
            print(E)
            Flota.mostrar(M)
            if E != 0:
                print("Fallaste 1")
                M = Flota.hacer_mat(10)
                Flota.mostrar(M)
            else:
                barcos = []
                Turno = 1

        elif Turno == 1:
            N = Flota.colocar_barcos(N, barcos_enem)
            Flota.mostrar(N)
            LL = Flota.crear_barcos(N)
            print(L)
            E2 = Flota.detectar_errores(N, LL)
            print(E2)
            Flota.mostrar(N)

            if E2 != 0:
                print("Fallaste 2")
                N = Flota.hacer_mat(10)
                Flota.mostrar(N)
            else:
                barcos_enem = []
                Turno = 0
                Start = True


    if Start == True and L == []:
        gameOver = True

    if pygame.key.get_pressed()[pygame.K_DELETE]:
        Start = False
        barcos = []

    #Delete boats
    if mouse_buttons[2] == True:
        mouse_pos = pygame.mouse.get_pos()
        clas_y = 0
        clas_x = 0
        mx = mouse_pos[0]
        my = mouse_pos[1]
        while mx > 60:
            mx = mx - 60
            clas_x = clas_x + 1
        while my> 60:
            my = my - 60
            clas_y = clas_y + 1
        if clas_x < 10 and Turno == 0:
            if [clas_x, clas_y] in barcos:
                barcos.remove([clas_x, clas_y])
        if clas_x > 10 and Turno == 1:
            if [clas_x - 11, clas_y] in barcos_enem:
                barcos_enem.remove([clas_x - 11, clas_y])
    #Mostrar barcos

    for i in range(len(M)):
        for j in range(len(M[i])):
            if M[i][j] == '~' and Turno == 1:
                pygame.draw.rect(screen, yel, [j* cube_size + 1, i* cube_size + 1, 58, 58], 0)
            if M[i][j] == 'x' and Turno == 1:
                pygame.draw.rect(screen, redP, [j* cube_size + 1, i* cube_size + 1, 58, 58], 0)
            if M[i][j] == '1' and Start == True and Turno == 0:
                pygame.draw.rect(screen, greenP, [j* cube_size + 1, i* cube_size + 1, 58, 58], 0)

    for i in range(len(N)):
        for j in range(len(N[i])):
            if N[i][j] == '~' and Turno == 0:
                pygame.draw.rect(screen, yel, [(j + 11)* cube_size + 1, i* cube_size + 1, 58, 58], 0)
            if N[i][j] == 'x' and Turno == 0:
                pygame.draw.rect(screen, redP, [(j + 11)* cube_size + 1, i* cube_size + 1, 58, 58], 0)
            if N[i][j] == '1' and Start == True and Turno == 1:
                pygame.draw.rect(screen, greenP, [(j + 11)* cube_size + 1, i* cube_size + 1, 58, 58], 0)

    if Start == False and Turno == 0:
        for i in range(len(barcos)):
            pygame.draw.rect(screen, greenP, [barcos[i][0]* cube_size + 1, barcos[i][1]* cube_size + 1, 58, 58], 0)

    if Start == False and Turno == 1:
        for i in range(len(barcos_enem)):
            pygame.draw.rect(screen, greenP, [(barcos_enem[i][0]+11)* cube_size + 1, barcos_enem[i][1]* cube_size + 1, 58, 58], 0)


    pygame.display.flip()
    clock.tick(12)

pygame.quit()
