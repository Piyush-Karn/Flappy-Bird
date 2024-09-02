import random 
import sys 
import pygame
from pygame.locals import *

FPS = 32
screen_width = 600
screen_height = 500
SCREEN = pygame.display.set_mode((screen_width, screen_height))
GROUNDY = screen_height * 0.8
game_images = {}
game_sounds = {}
player = 'bird.png'
background = 'background.png'
pipe = 'pipe.png'
pygame.mixer.init()
pygame.mixer.music.load("background_music.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Creates Welcome Screeen
def welcomeScreen():
    playerx = int(screen_width/5)
    playery = int((screen_height - game_images['player'].get_height())/2)
    messagex = int(0)
    messagey = int(0)
    basex = 0
    while True:
        for event in pygame.event.get():
            
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:    
                SCREEN.blit(game_images['message'], (messagex,messagey ))      
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(screen_width/5)
    playery = int(screen_width/2)
    basex = 0

    
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': screen_width+200, 'y':newPipe1[0]['y']},
        {'x': screen_width+200+(screen_width/2), 'y':newPipe2[0]['y']},
    ]
    lowerPipes = [
        {'x': screen_width+200, 'y':newPipe1[1]['y']},
        {'x': screen_width+200+(screen_width/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 
    playerFlapped = False 


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) 
        if crashTest:
            return     

        playerMidPos = playerx + game_images['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_images['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                game_sounds['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = game_images['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -game_images['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        SCREEN.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(game_images['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(game_images['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(game_images['base'], (basex, 350))
        SCREEN.blit(game_images['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += game_images['numbers'][digit].get_width()
        Xoffset = (screen_width - width)/2

        for digit in myDigits:
            SCREEN.blit(game_images['numbers'][digit], (Xoffset, screen_height*0.12))
            Xoffset += game_images['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 100  or playery<0:
        game_sounds['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = game_images['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < game_images['pipe'][0].get_width()):
            game_sounds['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + game_images['player'].get_height()-15 > pipe['y']) and abs(playerx - pipe['x']) < game_images['pipe'][0].get_width():
            game_sounds['hit'].play()
            return True

    return False

def getRandomPipe():
    # Creates Pipes at Bottom AND Top Position
    pipeHeight = game_images['pipe'][0].get_height()
    offset = screen_height/3
    y2 = offset + random.randrange(0, int(screen_height - game_images['base'].get_height()  - 1.2 *offset))
    pipeX = screen_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, 
        {'x': pipeX, 'y': y2} 
    ]
    return pipe




pygame.init() 
FPSCLOCK = pygame.time.Clock()
pygame.display.set_caption('Flappy Bird by Piyush Kumar')
game_images['numbers'] = (
    pygame.image.load('0.png').convert_alpha(),
    pygame.image.load('1.png').convert_alpha(),
    pygame.image.load('2.png').convert_alpha(),
    pygame.image.load('3.png').convert_alpha(),
    pygame.image.load('4.png').convert_alpha(),
    pygame.image.load('5.png').convert_alpha(),
    pygame.image.load('6.png').convert_alpha(),
    pygame.image.load('7.png').convert_alpha(),
    pygame.image.load('8.png').convert_alpha(),
    pygame.image.load('9.png').convert_alpha(),
    )

game_images['message'] =pygame.transform.scale(pygame.image.load('message.png'),(screen_width,screen_height)).convert_alpha()
game_images['base'] =pygame.transform.scale(pygame.image.load('base.png'),(screen_width,150)).convert_alpha()
game_images['pipe'] =(pygame.transform.rotate(pygame.image.load( pipe).convert_alpha(), 180), 
pygame.image.load(pipe).convert_alpha())

    
game_sounds['die'] = pygame.mixer.Sound('die.wav')
game_sounds['hit'] = pygame.mixer.Sound('hit.wav')
game_sounds['point'] = pygame.mixer.Sound('point.wav')
game_sounds['swoosh'] = pygame.mixer.Sound('swoosh.wav')


game_images['background'] = pygame.transform.scale(pygame.image.load(background),(screen_width,screen_height)).convert()
game_images['player'] = pygame.image.load(player).convert_alpha()

while True:
    welcomeScreen() 
    mainGame() 
