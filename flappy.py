# This is the flappy bird project
import random  # For some randomness in program e.g. random no. generation
import sys  # For sudden exit
import pygame
from pygame.locals import *

# Declaring global variables required for the game
FPS = 32
SCREENWIDTH = 288
SCREENHEIGHT = 512
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

# Initializing window for the display
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'

# welcomeScreen function
def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH-GAME_SPRITES['messages'].get_width()))/2
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # if user clicks space or uparrow
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))  # To show on the screen
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['messages'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

# Generating random pipes
def getRandompipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()- 1.2 * offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipex, 'y': -y1},
        {'x': pipex, 'y': y2},
    ]
    return pipe

# Checking for collision
def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS["hit"].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery< pipeHeight + pipe['y'] and abs(playerx-pipe['x'])<GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS["hit"].play()
            return True

    for pipe in lowerPipes:
        # pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery + GAME_SPRITES['player'].get_height()>pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS["hit"].play()
            return True

    return False

# mainGame function
def mainGame():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    basex = 0

    # Creating two pipes for blitting on the screen
    newPipe1 = getRandompipe()
    newPipe2 = getRandompipe()

    # list of upperpipes
    upperPipes = [
        {'x':SCREENWIDTH+200,'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[0]['y']}
    ]

    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False  # true when bird is flapping

    while True:

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        # Crash Test
        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes)
        if crashTest:
            return score

        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score+=1
                # print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY,GROUNDY-playery-playerHeight)

        # moving pipes to the left
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX

            # Adding new pipe when the first pipe is about to cross the leftmsot part
        if 0 <upperPipes[0]['x'] <5:
            newpipe = getRandompipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))

        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))

        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['highscore'], (SCREENWIDTH * 0.3, SCREENHEIGHT * 0.9))
        high_score = list(gethighscore())
        width_num = 0
        for item in high_score:
            num = int(item)
            SCREEN.blit(GAME_SPRITES['numbers'][num], ((SCREENWIDTH * 0.7)+width_num, SCREENHEIGHT * 0.89))
            width_num += GAME_SPRITES['numbers'][num].get_width()


        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digits in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digits],(Xoffset,SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digits].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def gethighscore():
    f = open("highscore.txt")
    return f.read()


def sethighscore(user_score):
    f = open('highscore.txt', 'r+')
    high = f.read()
    if high == "":
        f.write(str(user_score))
    else:
        # print(high)
        if int(high) < user_score:
            f.seek(0)
            f.write(str(user_score))
    f.close()
    welcomeScreen()


# program logic starts from here
if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird - PJ10")
    GAME_SPRITES['numbers'] = (
                                pygame.image.load('gallery/sprites/0.png').convert_alpha(),
                                pygame.image.load('gallery/sprites/1.png').convert_alpha(),
                                pygame.image.load('gallery/sprites/2.png').convert_alpha(),
                                pygame.image.load('gallery/sprites/3.png').convert_alpha(),
                                pygame.image.load('gallery/sprites/4.png').convert_alpha(),
                                pygame.image.load('gallery/sprites/5.png').convert_alpha(),
                                pygame.image.load('gallery/sprites/6.png').convert_alpha(),
                                pygame.image.load('gallery/sprites/7.png').convert_alpha(),
                                pygame.image.load('gallery/sprites/8.png').convert_alpha(),
                                pygame.image.load('gallery/sprites/9.png').convert_alpha(),
                              )
    GAME_SPRITES['messages'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load('gallery/sprites/pipe.png').convert_alpha(),180),
                            pygame.image.load(PIPE).convert_alpha())
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['highscore'] = pygame.image.load('gallery/sprites/highscore.png').convert_alpha()

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcomeScreen()  # Shows the main screen until any button is pressed
        user_score = mainGame()  # The game officially starts here
        sethighscore(user_score)



