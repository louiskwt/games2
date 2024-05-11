# create animation
import pygame
import random
import time

pygame.init()

def get_image(sheet, frame, width, height, scale, color1):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet,(0, 0), (frame*width, 0, 96, 96))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color1)  
    
    return image

# Main function
def main():
    pygame.font.init() # you have to call this at the startto use this module.

    my_font = pygame.font.SysFont('Comic Sans MS', 28)

    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500
    # BG = (0, 0, 0)
    BG = pygame.image.load("bg_sea2.png")
    BLACK = (0, 0, 0)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Submarine2')

    sprite_sheet_image = pygame.image.load('sub3.png').convert_alpha()
    sprite_star_image = pygame.image.load('bomb3.png').convert_alpha()
    sprite_star_image.set_colorkey(BLACK)
    blust_image = pygame.image.load('blust4.png').convert_alpha()
    blust_image = pygame.transform.scale(blust_image, (200, 200))
    blust_image.set_colorkey(BLACK)

    animation_list = []
    animation_steps = 4
    last_update = pygame.time.get_ticks()
    t0 = last_update
    animation_cooldown = 150
    frame = 0

    for i in range(animation_steps):
        animation_list.append(get_image(sprite_sheet_image, i, 96, 96, 1, BLACK))

    run = True
    x=0
    y=200
    d=20
    x1=10
    y1=0
    dx1=30
    dy1=40
    dy1=0
    flag = True
    flagHit = False
    flagDrop = False
    nhits = 0
    while run:

        screen.blit(BG, (0,0))
        w1=24
        h1=24
        s1=2
        star1 = sprite_star_image
        star1 = pygame.transform.scale(star1, (w1 * s1, h1 * s1))
        star1.set_colorkey(BLACK)

        txt = "Number of hits: " + str(nhits)
        text_surface = my_font.render(txt, False, (250, 250, 250))

        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame +=1
            if x>380:
                flag = True
                x = 0
                y = 200 + 2*random.randint(-40, 40)
            if x<0:
                flag = False
                x = 380
                y = 200 + 2*random.randint(-40, 40)
            
            if flag==True:
                x = x + d
            else:
                x = x -d       

            if frame > len(animation_list)-1:
                frame = 0

            x1 = x1 + dx1
            y1 = y1 + dy1
            s1 = 3
            if abs(x+20-x1)<30 and abs (y+60-y1)<30:
                flagHit = True
                nhits = nhits + 1
                # s1 = 5
                # star1 = pygame.transform.scale(star1, (w1 * s1, h1 * s1))
                star1.set_colorkey(BLACK)
                y1 = 0
                flagDrop = False

                txt = "Number of hits: " + str(nhits)
              
                time.sleep(1)

            if nhits == 10:
                # time.sleep(3)
                run = False
                txt = " Game is over! Hits: " + str(nhits) + "; Time: " + str(round((current_time - t0)/1000.,0)) + "s"

            text_surface = my_font.render(txt, False, (250, 250, 250))

            if y1 > 500 or x1 > 500 or x1 < 0:
                y1 = 0
                flagDrop = False
                x1 = random.randint(50, 450)
                dx1 = random.randint(-20, 20)

            last_update = current_time

        # print('frame = ', frame)
        if flag:    
            screen.blit(animation_list[frame], (x,y))
        else:
            img=animation_list[frame]
            img = pygame.transform.flip(surface=img, flip_x=True, flip_y=False)
            img.set_colorkey(BLACK)
            screen.blit(img, (x,y))
            #image = pygame.transform.flip(surface=image, flip_x=True, flip_y=False)

        star1.set_colorkey(BLACK)
        screen.blit(star1, (x1,y1))  

        screen.blit(text_surface, (10,5))  
        # screen.blit(star1, (x1-20,y1-20))    

        if nhits == 10:
            time.sleep(3)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type ==  pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    flagDrop = True    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    flag = False
                if event.key == pygame.K_RIGHT:
                    flag = True
                y = 200    
                if event.key == pygame.K_UP:
                    y = 150
                if event.key == pygame.K_DOWN:
                    y = 250                 

        if flagDrop == True:
            dy1 = 40
        else:
            flagDrop == False
            dy1 = 0

        if flagHit==True:
            flagHit = False
            screen.blit(blust_image, (x-20,y-20))
            pygame.display.update()
            time.sleep(3)
            x = 0
            y = 200 + 2*random.randint(-40, 40)
        
        if nhits>=10:
            run = False
            screen.blit(text_surface, (0,0))         
            time.sleep(7)

        pygame.display.update()



    pygame.quit()

if __name__ == "__main__":
    main()