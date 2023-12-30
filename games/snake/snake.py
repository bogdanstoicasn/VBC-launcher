import pygame
from time import sleep
from random import randint
from ctypes import windll

x_axis, y_axis = 400, 400

def read_highscore():
    # open high score file and read score

    f = open("./games/snake/highscore.txt", "a+")
    f.seek(0)
    highscore = f.read()

    # initialise highscore file base if not created already
    if highscore == "":
        highscore = 0
        update_highscore(0)

    f.close()

    return int(highscore)

def update_highscore(score):
    f = open("./games/snake/highscore.txt", "w+")
    f.write(str(score))
    f.close()

    return int(score)

def game_over(score, window):

    highscore = read_highscore()

    # update in file but also locally
    if highscore < score:
        highscore = update_highscore(score)

    # initialise final score and high score texts
    over_font = pygame.font.SysFont("times new roman", 50)
    highscore_font = pygame.font.SysFont("times new roman", 20)

    over_surface = over_font.render("Your score: " + str(score), True, pygame.Color(255, 255, 255))
    highscore_surface = highscore_font.render("Your high score: " + str(highscore), True, pygame.Color(255, 255, 255))

    # change text box positions
    over_rectangle = over_surface.get_rect(midtop=(x_axis / 2, y_axis / 4))
    highscore_rectangle = highscore_surface.get_rect(midtop=(x_axis / 2, y_axis / 2 - 40))

    # wait 2 seconds after collision and wipe screen
    sleep(2)
    window.fill(pygame.Color(0,0,0))

    window.blit(over_surface, over_rectangle)
    window.blit(highscore_surface, highscore_rectangle)
    pygame.display.flip()

    # wait for manual quit after loss
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

def init_fruit():
    # generate random fruit on table
    fruit = [randint(1, (x_axis - 10) // 10) * 10, randint(3, (y_axis - 10) // 10) * 10]
    return fruit

def draw_snake(snake_body, window, skin):

    # draw snake component by component
    for body in snake_body:
        pygame.draw.rect(window, skin, pygame.Rect(body[0], body[1], 10, 10))

def check_collision(head, snake_body):
    # check if snake has hit wall
    if head[0] < 0 or head[1] < 20 or head[0] > x_axis - 10 or head[1] > y_axis - 10:
        return True
    # check if snake hit body
    if head in snake_body[1:]:
        return True

    return False

def get_score(score, window):
    pygame.font.init()
    font = pygame.font.SysFont('times new roman', 20)
    surface = font.render('Score: ' + str(score), True, pygame.Color(0, 255, 0))

    rectangle = surface.get_rect()
    window.blit(surface, rectangle)

def play_snake(window, skin):

    # initialise snake as one block on start
    head = [100, 100]
    body = [ [100, 100] ]
    fruit = init_fruit()

    # initial direction down and score 0
    direction = "DOWN"
    score = 0
    fps = pygame.time.Clock()

    cond = True

    while cond:

        # erase board after every clock cycle
        window.fill(pygame.Color(0,0,0))

        # draw snake and fruit
        draw_snake(body, window, skin)
        pygame.draw.rect(window, pygame.Color(255, 0, 0), pygame.Rect(fruit[0], fruit[1], 10, 10))
        pygame.display.flip() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cond = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    cond = False
                    break
                # avoid stopping snake by moving in opposit direction    
                elif event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"                 

        if direction == "UP":
            head[1] -= 10
        elif direction == "DOWN":
            head[1] += 10
        elif direction == "LEFT":
            head[0] -= 10
        elif direction == "RIGHT":
            head[0] += 10

        # push to list new position and pop tail if no fruit was eaten
        body.insert(0, list(head))

        if head[0] == fruit[0] and head[1] == fruit[1]:
            score += 10
            fruit = init_fruit()
        else:
            body.pop()    

        if check_collision(head, body):
            cond = game_over(score, window)

        # display score on screen and update every cycle
        get_score(score, window)

        pygame.display.update()

        # set 10 fps speed of snake
        fps.tick(10)                
                        
    pygame.quit()      

def title_screen(window):
    
    # wipe screen
    window.fill(pygame.Color(0,0,0))

    # initialise title screen text
    pygame.font.init()
    title_font = pygame.font.SysFont("times new roman", 50)
    continue_font = pygame.font.SysFont("times new roman", 20)

    title_surface = title_font.render("SNAKE GAME", True, pygame.Color(0, 255, 0))
    continue_surface = continue_font.render("Press Enter to continue...", True, pygame.Color(255, 255, 255))

    # change text box positions
    title_rectangle = title_surface.get_rect(midtop=(x_axis / 2, y_axis / 4))
    continue_rectangle = continue_surface.get_rect(midtop=(x_axis / 2, y_axis / 2 + 160))

    # display text
    window.blit(title_surface, title_rectangle)
    window.blit(continue_surface, continue_rectangle)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_RETURN:
                    return True    

def print_skin_text(window):

    pygame.font.init()
    green_font = pygame.font.SysFont("times new roman", 30)
    blue_font = pygame.font.SysFont("times new roman", 30)
    orange_font = pygame.font.SysFont("times new roman", 30)

    green_surface = green_font.render("GREEN", True, pygame.Color(0, 255, 0))
    blue_surface = blue_font.render("BLUE", True, pygame.Color(0, 0, 255))
    orange_surface = orange_font.render("ORANGE", True, pygame.Color(255, 165, 0))

    green_rectangle = green_surface.get_rect(midtop=(x_axis / 2, y_axis / 2 - 80))
    blue_rectangle = blue_surface.get_rect(midtop=(x_axis / 2, y_axis / 2))
    orange_rectangle = orange_surface.get_rect(midtop=(x_axis / 2, y_axis / 2 + 80))

    window.blit(green_surface, green_rectangle)
    window.blit(blue_surface, blue_rectangle)
    window.blit(orange_surface, orange_rectangle)

def print_hover_selection(window, center):

    # draw triangle to signal skin choice next to text
    x_coord = (x_axis / 4 - 10, y_axis / 2 + center - 20)
    y_coord = (x_axis / 4 - 10, y_axis / 2 + center + 20)
    z_coord = (x_axis / 4 + 10, y_axis / 2 + center)

    pygame.draw.polygon(window, pygame.Color(255, 0, 0), (x_coord, y_coord, z_coord))

def choose_skin(window):

    # choose from green, blue or orange skin
    skins = [ pygame.Color(0, 255,0), pygame.Color(0, 0, 255), pygame.Color(255, 165, 0)]

    # green will be the default color in our menu
    selected_skin = 0
    green_pos = -65
    blue_pos = 15
    orange_pos = 95

    pygame.font.init()

    while True:

        window.fill(pygame.Color(0,0,0))

        choose_font = pygame.font.SysFont("times new roman", 50)
        choose_surface = choose_font.render("Choose a skin!", True, pygame.Color(255, 255, 255))
        choose_rectangle = choose_surface.get_rect(midtop=(x_axis / 2, 0))

        window.blit(choose_surface, choose_rectangle)   

        # add to screen the text for the three skins
        print_skin_text(window)

        # print triangle next to skin hovered for selection
        if selected_skin == 0:
            print_hover_selection(window, green_pos)
        elif selected_skin == 1:
            print_hover_selection(window, blue_pos)
        elif selected_skin == 2:
            print_hover_selection(window, orange_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "exit"
                elif event.key == pygame.K_DOWN:
                    selected_skin = (selected_skin + 1) % 3
                elif event.key == pygame.K_UP:
                    selected_skin = (selected_skin + 2) % 3    
                elif event.key == pygame.K_RETURN:
                    # wipe screen before gameplay
                    window.fill(pygame.Color(0,0,0))
                    pygame.display.flip()
                    return skins[selected_skin]
        

def run_snake():

    # create window on run
    window = pygame.display.set_mode((x_axis, y_axis))

    # initialise window to always be in foreground
    SetWindowPos = windll.user32.SetWindowPos
    SetWindowPos(pygame.display.get_wm_info()['window'], -1, x_axis, y_axis, 0,0, 0x0001)

    pygame.display.set_caption('Snake game!')

    # check if game wasnt exited on title screen
    if not title_screen(window):
        pygame.quit()
        return "Exit game"

    # check if game wasn't exited on skin choosing screen
    skin = choose_skin(window)

    if skin == "exit":
        pygame.quit()
        return "Exit game"

    # wait 2 seconds before start
    sleep(2)
    play_snake(window, skin)

if __name__ == "__main__":
    pygame.init()
    run_snake()   