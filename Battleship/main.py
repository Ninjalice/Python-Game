import pygame #Pygame module to make the game in window mode and with sounds
import Flota #We add another file full of functions to make prettier the main.py program

#Music configuration for the sound of the game

pygame.mixer.pre_init()
pygame.mixer.init(frequency = 44100, size = -16, channels = 2, buffer = 2**12)

channel1 = pygame.mixer.Channel(0) #Music channel 1
channel2 = pygame.mixer.Channel(1) #Music channel 2

sound_background = pygame.mixer.Sound('fondo.mp3') #Music sound 1
sound_touch = pygame.mixer.Sound("tocado.mp3") #Music sound 2
sound_miss = pygame.mixer.Sound("fail.mp3") #Music sound 3

channel1.play(sound_background)

#Empty matrices for computing the game
Mat_player_1 = Flota.hacer_mat(10)
Flota.mostrar(Mat_player_1)
Mat_player_2 = Flota.hacer_mat(10)
Flota.mostrar(Mat_player_2)

#Color pallete for the game
color_blue = (20, 34, 238)
color_green = (20, 240, 50)
color_red = (230, 0, 20)
color_yellow = (255, 255, 0)
color_black = (0, 0, 0)
color_purple = (87, 35, 100)

#Other variables for the game
mx = 0
my = 0

clas_x = 0
clas_y = 0

game_started = False

player1_boats = []
player2_boats = []

player_turn = 0
player_boat_touch = None

sizeSquare = 60
num_of_cubes = 10
size = (1260, 600)
cube_size= int(size[1]/num_of_cubes)
line_thikness = 2
line_cube = cube_size - line_thikness



#Game initializes
pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Battleships")
clock = pygame.time.Clock()
gameOver = False

text_font = pygame.font.Font('Alice and the Wicked Monster.ttf', 16)
important_font = pygame.font.SysFont('Alice and the Wicked Monster.ttf', 100)

Text_player1_won = important_font.render("Player 1 Won", True, color_green)
Text_player2_won = important_font.render("Player 2 Won", True, color_green)
Text_change_player = important_font.render("Change player", True, color_yellow)

while not gameOver:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    screen.fill(color_black)

    #Text variables for the numbers of the topside.
    Tx = 0
    Ty = 0
    for i in range(1, 600, cube_size):
        for j in range(1, size[1], cube_size):
            pygame.draw.rect(screen, color_blue, [i, j, line_cube, line_cube], 0)

        Text = text_font.render(str(Tx), True, color_green)
        screen.blit(Text, [i, 2])
        if Tx != 0:
            screen.blit(Text, [2, i + 16])
        Tx += 1
        Ty = 0
    Tx = 0
    Ty = 0
    for i in range(660, 1260, cube_size):
        for j in range(1, size[1], cube_size):
            pygame.draw.rect(screen, color_blue, [i, j, line_cube, line_cube], 0)

        Text = text_font.render(str(Tx), True, color_green)
        screen.blit(Text, [i, 2])
        if Tx != 0:
            screen.blit(Text, [2, i + 16])
        Tx += 1
        Ty = 0

    #This part checks if the mouse is getting pressed
    mouse_buttons = pygame.mouse.get_pressed(num_buttons=3)

    if mouse_buttons[0] == True and mouse_pressed != True:
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

        if game_started == True:
            if player_turn == 0 and clas_x > 10: #This part shows the board of the second player while the first player attacks
                Mat_player_2,Boats_on_float_player2,player_boat_touch = Flota.disparar(Mat_player_2, clas_x - 11, clas_y,Boats_on_float_player2)
                Flota.mostrar(Mat_player_2)

            #This part shows the board of the first player while the second player attacks
            elif player_turn == 1 and clas_x < 10:
                Mat_player_1 , Boats_on_float_player1 , player_boat_touch = Flota.disparar(Mat_player_1, clas_x, clas_y,Boats_on_float_player1)
                Flota.mostrar(Mat_player_1)
            #Plays the sound of the miss or the hit
            if player_boat_touch:
                channel2.play(sound_touch)
            else:
                channel2.play(sound_miss)
            print("TURN: ",player_turn)
        #This part is for adding the boats
        else:
            if clas_x != 10:
                if [clas_x, clas_y] not in player1_boats and clas_x < 10 and player_turn == 0:
                    player1_boats.append([clas_x, clas_y])
                    print("1:",clas_x, clas_y)
                if [clas_x, clas_y] not in player2_boats and clas_x > 9 and player_turn == 1:
                    player2_boats.append([clas_x - 11, clas_y])
                    print("2:",clas_x - 11, clas_y)

        mouse_pressed = True

    if mouse_buttons[0] == False:
        mouse_pressed = False
    #This part is for setting the turns: the turn 0 is the turn of the first player, the turn 1 is the one of the second player and turn -1 and -2
    #are intermediate states for the change of turns between players
    if pygame.key.get_pressed()[pygame.K_SPACE] and space_pressed != True:
        space_pressed = True
        if player_turn == 0:
            player_turn = -1
        elif player_turn == -1:
            player_turn = 1
        elif player_turn == 1:
            player_turn = -2
        elif player_turn == -2:
            player_turn = 0

    if pygame.key.get_pressed()[pygame.K_SPACE] ==False:
        space_pressed = False

    if pygame.key.get_pressed()[pygame.K_RETURN] and return_pressed != True:
        return_pressed = True
        #Inputs the boats of the boats of the first player, checks if there is any error and shows the board.
        if player_turn == 0:
            Mat_player_1 = Flota.colocar_barcos(Mat_player_1, player1_boats)
            Flota.mostrar(Mat_player_1)
            Boats_on_float_player1 = Flota.crear_barcos(Mat_player_1)
            print(Boats_on_float_player1)
            Error_player1 = Flota.detectar_errores(Mat_player_1, Boats_on_float_player1)
            print(Error_player1)
            Flota.mostrar(Mat_player_1)

            if Error_player1 != 0:
                print("Miss of player 1")
                Mat_player_1 = Flota.hacer_mat(10)
                Flota.mostrar(Mat_player_1)
            else:
                player1_boats = []
                player_turn = -1
        #Inputs the boats of the boats of the second player, checks if there is any error and shows the board.
        elif player_turn == 1:
            Mat_player_2 = Flota.colocar_barcos(Mat_player_2, player2_boats)
            Flota.mostrar(Mat_player_2)
            Boats_on_float_player2 = Flota.crear_barcos(Mat_player_2)
            print(Boats_on_float_player1)
            Error_player2 = Flota.detectar_errores(Mat_player_2, Boats_on_float_player2)
            print(Error_player2)
            Flota.mostrar(Mat_player_2)
            #If there is an error the matrix is restarted
            if Error_player2 != 0:
                print("Miss of player 2")
                Mat_player_2 = Flota.hacer_mat(10)
                Flota.mostrar(Mat_player_2)
            else:
                player2_boats = []
                player_turn = -2
                game_started = True

    if pygame.key.get_pressed()[pygame.K_RETURN] ==False:
        return_pressed = False
    #Delete player_boats
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
        if clas_x < 10 and player_turn == 0:
            if [clas_x, clas_y] in player1_boats:
                player1_boats.remove([clas_x, clas_y])
        if clas_x > 10 and player_turn == 1:
            if [clas_x - 11, clas_y] in player2_boats:
                player2_boats.remove([clas_x - 11, clas_y])


    #Display boats of both player depending of the turn
    for i in range(len(Mat_player_1)):
        for j in range(len(Mat_player_1[i])):
            if Mat_player_1[i][j] == '~' and player_turn == 1:
                pygame.draw.rect(screen, color_yellow, [j* cube_size + 1, i* cube_size + 1, 58, 58], 0)
            if Mat_player_1[i][j] == 'x' and player_turn == 1:
                pygame.draw.rect(screen, color_red, [j* cube_size + 1, i* cube_size + 1, 58, 58], 0)
            if Mat_player_1[i][j] == '1' and game_started == True and player_turn == 0:
                pygame.draw.rect(screen, color_green, [j* cube_size + 1, i* cube_size + 1, 58, 58], 0)

    for i in range(len(Mat_player_2)):
        for j in range(len(Mat_player_2[i])):
            if Mat_player_2[i][j] == '~' and player_turn == 0:
                pygame.draw.rect(screen, color_yellow, [(j + 11)* cube_size + 1, i* cube_size + 1, 58, 58], 0)
            if Mat_player_2[i][j] == 'x' and player_turn == 0:
                pygame.draw.rect(screen, color_red, [(j + 11)* cube_size + 1, i* cube_size + 1, 58, 58], 0)
            if Mat_player_2[i][j] == '1' and game_started == True and player_turn == 1:
                pygame.draw.rect(screen, color_green, [(j + 11)* cube_size + 1, i* cube_size + 1, 58, 58], 0)

    #Display boats in the boat placement state
    if game_started == False and player_turn == 0:
        for i in range(len(player1_boats)):
            pygame.draw.rect(screen, color_green, [player1_boats[i][0]* cube_size + 1, player1_boats[i][1]* cube_size + 1, 58, 58], 0)

    if game_started == False and player_turn == 1:
        for i in range(len(player2_boats)):
            pygame.draw.rect(screen, color_green, [(player2_boats[i][0]+11)* cube_size + 1, player2_boats[i][1]* cube_size + 1, 58, 58], 0)

    if game_started == True and Boats_on_float_player1 == []:
        screen.blit(Text_player2_won, (350,300))
    if game_started == True and Boats_on_float_player2 == []:
        screen.blit(Text_player1_won, (350,300))
    if player_turn == -1 or player_turn == -2:
        screen.blit(Text_change_player, (350,300))

    pygame.display.flip()
    clock.tick(12)

pygame.quit()
