import pygame
import random
import Flota


M = Flota.hacer_mat(10)
Flota.mostrar(M)
M = Flota.colocar_barcos(M, [[1, 2],[7, 9], [2, 5], [1, 3], [1, 4], [1, 5], [9, 9], [8, 9], [1, 6]])
Flota.mostrar(M)
L = Flota.crear_barcos(M)
print(L)
E = Flota.detectar_errores(M, L)
print(E)
M = Flota.disparar(M, 2, 2)
Flota.mostrar(M)


blueP = (20, 34, 238)
greenP = (20, 240, 50)
redP = (230, 0, 20)
BLACK = (0, 0, 0)
sizeSquare = 60

mx = 0
my = 0

clas_x = 0
clas_y = 0

barcos = []
barcos_enem = []
num_of_cubes = 10
size = (1260, 600)
cube_size= int(size[1]/num_of_cubes)
line_thikness = 2
line_cube = cube_size - line_thikness
for i in range(10):
    barco_ene = [random.randint(0, 9),random.randint(0, 9)]
    if barco_ene not in barcos_enem:
        barcos_enem.append(barco_ene)

pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Grid on PYGAME")
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
        if [clas_x, clas_y] not in barcos:
            barcos.append([clas_x, clas_y])

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
        if [clas_x, clas_y] in barcos:
            barcos.remove([clas_x, clas_y])
    #Mostrar barcos
    for i in range(len(barcos)):
        pygame.draw.rect(screen, greenP, [barcos[i][0]* cube_size + 1, barcos[i][1]* cube_size + 1, 58, 58], 0)
    for i in range(len(barcos_enem)):
        pygame.draw.rect(screen, redP, [barcos_enem[i][0]* cube_size + 1, barcos_enem[i][1]* cube_size + 1, 58, 58], 0)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
