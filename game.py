#import libraries
import pygame 
import random

pygame.mixer.init()
#initialise pygame
pygame.init()
#game window dimensions
SCREEN_WIDTH=400
SCREEN_HEIGHT=600

#create game window
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Jumpy')

#game variables
Scroll_Thresh= 200
Gravity = 1
Max_platforms=10
bg_scroll=0
game_over=False
score=0
high_score=0

#define colors
Black= (0,0,0)

#define text
font_small= pygame.font.SysFont('Arial Black',20)
font_large= pygame.font.SysFont('Arial Black',24)

#set frame rate
clock=pygame.time.Clock()
FPS=60

#load music
pygame.mixer.music.load('sounds/music1.mp3')
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1,0.0)
jump_fx = pygame.mixer.Sound('sounds/jump.mp3')
jump_fx.set_volume(0.5)
game_end =pygame.mixer.Sound('sounds/audio.mp3')
game_end.set_volume(0.5)


#adding images
bg1_image= pygame.image.load('images/clouds.jpg').convert_alpha()
#to fit background image in screen window
bg_image= pygame.transform.scale(bg1_image,(400,600))
jumpy_image= pygame.image.load('images/jumpy.png').convert_alpha()
platform_image= pygame.image.load('images/wood.png').convert_alpha()

def draw_text(text,font,text_color,x,y):
    """function for outputting text onto the screen"""
    img= font.render(text,True,text_color)
    screen.blit(img,(x,y))
    
def draw_panel():
    draw_text(f"Score: {score}",font_small,Black,0,0)

def draw_bg(bg_scroll):
    """function for drawing the background"""
    screen.blit(bg_image,(0,0+bg_scroll))
    screen.blit(bg_image,(0,-600+bg_scroll))
    
#player class
class Player():
    def __init__(self,x,y):
        self.image= pygame.transform.scale(jumpy_image,(45,45))
        self.width= 25
        self.height= 40
        self.rect= pygame.Rect(0,0,self.width,self.height)
        self.rect.center= (x,y)
        self.vel_y =0
    
    def move(self): 
        """This function will move the player in right,left,up and down"""
        #reset variables
        scroll=0
        dx=0
        dy=0
        
        #process keypresses
        key= pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx = -10
        if key[pygame.K_RIGHT]:
            dx = +10
            
        #gravity
        self.vel_y +=Gravity
        dy +=self.vel_y
        
        # to ensure player does not go off the screen
        if self.rect.left + dx < 0:
            dx=-self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx= SCREEN_WIDTH-self.rect.right
            
        #check collision with platforms
        for platform in platform_group:
            #collision iin y direction
            if platform.rect.colliderect(self.rect.x,self.rect.y,self.width,self.height):
            #check if player is above the platform
                if self.rect.bottom > platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy=0
                        self.vel_y= -20
                        jump_fx.play()
            
        #check if the player has bounced to the top of the screen
        if self.rect.top <= Scroll_Thresh:
            if self.vel_y<0:
              scroll=-dy
                    
        #update rectangle position
        self.rect.x +=dx
        self.rect.y +=dy+scroll
        
        return scroll
        
    def draw(self):
        """This function will draw the player in rectangle frame"""
        screen.blit(self.image,(self.rect.x-12, self.rect.y-5))

#platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,width):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.transform.scale(platform_image,(width,10))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        
    def update(self,scroll):
        """updates platform's vertical position and checks if platform has gone off the screen"""
        self.rect.y +=scroll
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        
#player instance
jumpy= Player(SCREEN_WIDTH //2, SCREEN_HEIGHT-150)

#create sprite groups
platform_group= pygame.sprite.Group()

#create starting platform
platform= Platform(SCREEN_WIDTH//2-50,SCREEN_HEIGHT-50,100)
platform_group.add(platform)

#game loop
run= True
while run:
    clock.tick(FPS)
    
    if game_over==False:
        scroll= jumpy.move()
    
        #draw background
        bg_scroll += scroll
        if bg_scroll>=600:
          bg_scroll=0
        draw_bg(bg_scroll)
    
        #generate platforms
        if len(platform_group)<=Max_platforms:
            p_w= random.randint(40,60)
            p_x=random.randint(0,SCREEN_WIDTH-p_w)
            p_y=platform.rect.y -random.randint(80,120)
            platform= Platform(p_x,p_y,p_w)
            platform_group.add(platform)
    
        #update platforms
        platform_group.update(scroll)
        
        #update score
        if scroll>0:
            score+=scroll
     
        #draw sprites
        platform_group.draw(screen)
        jumpy.draw()
        
        #draw panel
        draw_panel()
    
        #check game over
        if jumpy.rect.top > SCREEN_HEIGHT:
            game_over=True
            game_end.play()
    else:
        draw_text('GAME OVER!',font_large, Black,115,200)
        draw_text(f"SCORE: {score}",font_large, Black,130,250)
        draw_text("Press space to play again",font_large, Black,30,300)
        key= pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            game_over=False
            score=0
            scroll=0
        #resetting jumpy's position
        jumpy.rect.center= (SCREEN_WIDTH //2, SCREEN_HEIGHT-150)
        #reset platforms
        platform_group.empty()
        #create starting platform
        platform= Platform(SCREEN_WIDTH//2-50,SCREEN_HEIGHT-50,100)
        platform_group.add(platform)
        
    #event handler
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            
    #updating display window
    pygame.display.update()
            
pygame.quit()


