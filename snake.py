import pygame
import pygame.freetype
import random

WIDTH = 640
HEIGHT = 480
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

corner_ne = pygame.image.load('./res/corner_ne.png')
corner_nw = pygame.image.load('./res/corner_nw.png')
corner_se = pygame.image.load('./res/corner_se.png')
corner_sw = pygame.image.load('./res/corner_sw.png')
head_d = pygame.image.load('./res/head_d.png')
head_l = pygame.image.load('./res/head_l.png')
head_r = pygame.image.load('./res/head_r.png')
head_u = pygame.image.load('./res/head_u.png')
straight_d = pygame.image.load('./res/straight_d.png')
straight_l = pygame.image.load('./res/straight_l.png')
straight_r = pygame.image.load('./res/straight_r.png')
straight_u = pygame.image.load('./res/straight_u.png')
tail_d = pygame.image.load('./res/tail_d.png')
tail_l = pygame.image.load('./res/tail_l.png')
tail_r = pygame.image.load('./res/tail_r.png')
tail_u = pygame.image.load('./res/tail_u.png')
appleimg = pygame.image.load('./res/apple.png')
ggfade = pygame.image.load('./res/gameover_fadein.png').convert()
ggnew = pygame.image.load('./res/gameover_newhigh.png')
ggold = pygame.image.load('./res/gameover_oldhigh.png')
game_bg = pygame.image.load('./res/game_bg.png')
sfx_eat = pygame.mixer.Sound('./res/sfx_eat.mp3')
sfx_pause = pygame.mixer.Sound('./res/sfx_pause.mp3')
sfx_gameover = pygame.mixer.Sound('./res/sfx_gameover.mp3')
sfx_newhigh = pygame.mixer.Sound('./res/sfx_newhigh.mp3')
hudfont = pygame.freetype.Font("./res/smb1_hud.ttf", 16)
title_bg1 = pygame.image.load('./res/title_bg1.png')
title_bg2 = pygame.image.load('./res/title_bg2.png')
title_bg3 = pygame.image.load('./res/title_bg3.png')
title_bg4 = pygame.image.load('./res/title_bg4.png')
title_stuff = pygame.image.load('./res/title_stuff.png')
blackimg = pygame.image.load('./res/black.png').convert()

pygame.display.set_icon(head_r)

def fadeout ():
    fadeofc = 0
    while fadeofc < 255:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        blackimg.set_alpha(fadeofc)
        if fadeofc < 255:
            fadeofc += 15
        screen.blit(blackimg, (0, 0))
        
        pygame.display.flip()

def gamecore (mode = 7):
    pygame.mixer.music.load('./res/bgm_game.mp3')
    pygame.mixer.music.play(-1)
    
    apple = 7009
    queue = [7003, 7004, 7005,]
    length = 3
    direction = 1
    cdirection = 1
    blacktrans = 0
    ggflicker = 0
    paused = False
    newhigh = False
    tempsfx = False
    
    f = open("./res/hiscore.ghs", 'r')
    normal_hs, fast_hs = f.readline().split()
    normal_hs = int(normal_hs)
    fast_hs = int(fast_hs)
    f.close()
    
    running = True
    countdown = mode
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and cdirection != 1:
                    direction = -1
                elif event.key == pygame.K_UP and cdirection != 1000:
                    direction = -1000
                elif event.key == pygame.K_RIGHT and cdirection != -1:
                    direction = 1
                elif event.key == pygame.K_DOWN and cdirection != -1000:
                    direction = 1000
                elif event.key == pygame.K_RETURN:
                    if countdown != -1:
                        sfx_pause.play()
                        if paused:
                            pygame.mixer.music.unpause()
                            paused = False
                        else:
                            pygame.mixer.music.pause()
                            paused = True
                    else:
                        pygame.mixer.stop()
                        fadeout()
                        return
        
        if paused:
            continue
        
        if countdown > 0:
            countdown -= 1
        if countdown == 0:
            cdirection = direction
            queue.append(queue[length-1] + cdirection)
            if queue[length] == apple:
                sfx_eat.play()
                length += 1
                temp = random.randint(1, 225-length)
                last = -1
                count = 0
                while count < temp:
                    count += 1
                    last += 1
                    if last % 1000 >= 15:
                        last = last + 1000 - 15
                    for x in queue:
                        if last == x:
                            count -= 1
                            break
                apple = last
            
            elif queue[length] % 1000 >= 15 or queue[length] >= 15000 or queue[length] < 0:
                countdown = -1
            
            else:
                queue.pop(0)
                occur = 0
                for x in queue:
                    if queue[length-1] == x:
                        occur += 1
                if occur >= 2:
                    countdown = -1
                
            if countdown >= 0: 
                countdown = mode
        
        screen.blit(game_bg, (0, 0))
        hudfont.render_to(screen, (25, 25), "APPLES " + str(length-3), WHITE)
        if mode == 7:
            hudfont.render_to(screen, (450-len(str(normal_hs))*16, 25), "HIGHSCORE " + str(normal_hs), WHITE)
        else:
            hudfont.render_to(screen, (450-len(str(fast_hs))*16, 25), "HIGHSCORE " + str(fast_hs), WHITE)
        
        prevdir = queue[1] - queue[0]
        for x in range(length):
            coordinate = ((WIDTH-375)/2 + queue[x]%1000*25, (HEIGHT-375)*3/4 + queue[x]//1000*25)
            if x == 0:
                if prevdir == -1000:
                    screen.blit(tail_d, coordinate)
                elif prevdir == 1000:
                    screen.blit(tail_u, coordinate)
                elif prevdir == -1:
                    screen.blit(tail_r, coordinate)
                else:
                    screen.blit(tail_l, coordinate)
            elif x == length - 1:
                prevdir = queue[x] - queue[x-1]
                if prevdir == -1000:
                    screen.blit(head_u, coordinate)
                elif prevdir == 1000:
                    screen.blit(head_d, coordinate)
                elif prevdir == 1:
                    screen.blit(head_r, coordinate)
                else:
                    screen.blit(head_l, coordinate)
            else:
                prevdir = queue[x+1] - queue[x-1]
                if prevdir == -2:
                    screen.blit(straight_l, coordinate)
                elif prevdir == 2:
                    screen.blit(straight_r, coordinate)
                elif prevdir == -2000:
                    screen.blit(straight_u, coordinate)
                elif prevdir == 2000:
                    screen.blit(straight_d, coordinate)
                else:
                    turn1, turn2 = queue[x] - queue[x-1], queue[x+1] - queue[x]
                    if (turn1 == 1 and turn2 == 1000) or (turn1 == -1000 and turn2 == -1):
                        screen.blit(corner_ne, coordinate)
                    elif (turn1 == 1 and turn2 == -1000) or (turn1 == 1000 and turn2 == -1):
                        screen.blit(corner_se, coordinate)
                    elif (turn1 == -1 and turn2 == 1000) or (turn1 == -1000 and turn2 == 1):
                        screen.blit(corner_nw, coordinate)
                    else:
                        screen.blit(corner_sw, coordinate)
        
        coordinate = ((WIDTH-375)/2 + apple%1000*25, (HEIGHT-375)*3/4 + apple//1000*25)
        screen.blit(appleimg, coordinate)
        
        if countdown == -1:
            pygame.mixer.music.fadeout(500)
            ggfade.set_alpha(blacktrans)
            if blacktrans < 255:
                blacktrans += 15
            else:
                ggflicker = (ggflicker + 1) % 40
            if ggflicker < 20:
                screen.blit(ggfade, (0, 0))
            else:
                if newhigh or (mode == 7 and length-3 > normal_hs) or (mode == 4 and length-3 > fast_hs):
                    screen.blit(ggnew, (0, 0))
                    if mode == 7:
                        normal_hs = length - 3
                    else:
                        fast_hs = length - 3
                    if newhigh == False:
                        sfx_newhigh.play()
                        f = open("./res/hiscore.ghs", 'w')
                        f.write(str(normal_hs) + " " + str(fast_hs))
                        f.close()
                    newhigh = True
                else:
                    if tempsfx == False:
                        sfx_gameover.play()
                        tempsfx = True
                    screen.blit(ggold, (0, 0))
        
        pygame.display.flip()
    
    pygame.quit()


menumusic = False
menurun = True
choice = 5.5
framecnt = 0
while menurun:
    if menumusic == False:
        pygame.mixer.music.load('./res/bgm_menu.mp3')
        pygame.mixer.music.play(-1)
        menumusic = True
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menurun = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                choice = 7
            elif event.key == pygame.K_RIGHT:
                choice = 4
            elif event.key == pygame.K_RETURN and choice != 5.5:
                menumusic = False
                pygame.mixer.music.fadeout(1000)
                fadeout()
                gamecore(choice)
    
    framecnt += 1
    if framecnt >= 20:
        framecnt -= 20
    if framecnt < 5:
        screen.blit(title_bg1, (0, 0))
    elif framecnt < 10:
        screen.blit(title_bg2, (0, 0))
    elif framecnt < 15:
        screen.blit(title_bg3, (0, 0))
    else:
        screen.blit(title_bg4, (0, 0))
    
    screen.blit(title_stuff, (0, 0))
    screen.blit(appleimg, (308 + (5.5-choice)*75, 354))
    
    pygame.display.flip()

pygame.quit()