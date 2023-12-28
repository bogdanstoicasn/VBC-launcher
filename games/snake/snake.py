import pygame
from time import sleep
from random import randint
from ctypes import windll

x_axis, y_axis = 400, 400



def read_highscore():
    # open high score file and read score
    f = open("./games/snake/highscore.txt", "rt")
    highscore = f.read()
    f.close()

    return int(highscore)

def update_highscore(score):
    f = open("./games/snake/highscore.txt", "wt")
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

def draw_snake(snake_body, window):
    # draw snake component by component
    for body in snake_body:
        pygame.draw.rect(window, pygame.Color(0, 255, 0), pygame.Rect(body[0], body[1], 10, 10))

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


def play_snake(window):
    
    pygame.display.set_caption('Snake game!')

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
        draw_snake(body, window)
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

def run_snake():

    # create window on run
    window = window = pygame.display.set_mode((x_axis, y_axis))

    # initialise window to always be in foreground
    SetWindowPos = windll.user32.SetWindowPos
    SetWindowPos(pygame.display.get_wm_info()['window'], -1, x_axis, y_axis, 0,0, 0x0001)

    # wait 3 seconds before start
    sleep(2)
    play_snake(window)

if __name__ == "__main__":
    pygame.init()
    run_snake()   