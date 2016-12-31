import pygame
import random
pygame.init()
breadth=600
length=500
#colors
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)


def text(surf,text,size,x,y):
    font=pygame.font.SysFont("calibri.ttf",size)
    text_surf=font.render(text,True,red)
    text_rect=text_surf.get_rect()
    text_rect.center=(x,y)
    surf.blit(text_surf,text_rect)
    

                
        
  #player class  
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("spaceship.png").convert()
        self.image.set_colorkey(white)
        self.rect=self.image.get_rect()
        self.radius=int(self.rect.width/2)
        self.rect.centerx=length/2
        self.rect.centery=breadth-60
        self.xspeed=0
        self.health=3
    def update(self):
        self.xspeed=0
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
                self.xspeed=-5
        if keystate[pygame.K_RIGHT]:
                self.xspeed=5
        if self.rect.right>length:
                self.rect.right=length
        if self.rect.left<0:
                self.rect.left=0
        self.rect.x+=self.xspeed
    def shoot(self):
        bullet=Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bulletsp.add(bullet)
#enemy class        
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1=pygame.image.load("asterois.png").convert()
            self.image1.set_colorkey(white)
            self.image=self.image1.copy()
            self.rect=self.image1.get_rect()
            self.radius=int(self.rect.width/2)
            self.rect.x=random.randrange(0,length-20)
            self.rect.y=random.randrange(-400,-300)
            self.yspeed=random.randrange(3,9)
            self.rotation=0
            self.rot_speed=random.randrange(-10,10)
            self.time=pygame.time.get_ticks()
    
    def rotate(self):
        now=pygame.time.get_ticks()
        if now-self.time>50:
            self.time=now
            self.rotation=(self.rotation+self.rot_speed)%360
            new_img=pygame.transform.rotate(self.image1,self.rotation)
            old_center=self.rect.center
            self.image=new_img
            self.rect=self.image.get_rect()
            self.rect.center=old_center
    def update(self):
         self.rotate()
         if self.rect.top>breadth+10:
               self.rect.x=random.randrange(0,length)
               self.rect.y=random.randrange(-400,-300)
         self.rect.y+=self.yspeed

#bullet
class Bullet(pygame.sprite.Sprite):
            def __init__(self,x,y):
                pygame.sprite.Sprite.__init__(self)
                self.image=pygame.Surface((10,20))
                self.image.fill(green)
                self.rect=self.image.get_rect()
                self.rect.bottom=y
                self.rect.centerx=x
                self.yspeed=-10
            def update(self):
                self.rect.y+=self.yspeed
                if self.rect.bottom<0:
                    self.kill()
#powerup class
class Power(pygame.sprite.Sprite):
                    def __init__(self,x,y):
                        pygame.sprite.Sprite.__init__(self)
                        self.image=power_img["shield"][0]
                        self.image.set_colorkey(black)
                        self.rect=self.image.get_rect()
                        self.rect.centery=y
                        self.rect.centerx=x
                        self.yspeed=+3
                    def update(self):
                        self.rect.y+=self.yspeed
                        if self.rect.top>breadth-10:
                            self.kill()
#explosion

class explosion(pygame.sprite.Sprite):
    def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.image=explode_anim["lg"][0]
            self.rect=self.image.get_rect()
            self.image.set_colorkey(black)
            self.rect.centerx=x
            self.rect.centery=y
            self.frame=0
            self.last_update=pygame.time.get_ticks()
            self.frame_lim=60
    def update(self):
        now=pygame.time.get_ticks()
        if now-self.last_update>self.frame_lim:
            self.frame+=1
            self.last_update=now
            if self.frame==len(explode_anim["lg"]):
               self.kill()
        else:
            center=self.rect.center
            self.image=explode_anim["lg"][self.frame]
            self.rect=self.image.get_rect()
            self.rect.center=center
        
        
        
        
def life(surf,x,y,phealth):
    bar_len=(phealth/3)*100
    bar_width=20
    if phealth==3:
        color=green
    elif phealth==2:
        color=white
    else:
        color=red
    pygame.draw.rect(surf,white,pygame.Rect(x,y,100,bar_width),2)
    pygame.draw.rect(surf,color,(x,y,bar_len,bar_width))
    
   
#mainscreen

pygame.mixer.init()
GameDisplay=pygame.display.set_mode((length,breadth))
backgrd=pygame.image.load("space.png").convert()
backgrd_rect=backgrd.get_rect()
pygame.display.set_caption("Space Invaders")
clock=pygame.time.Clock()
all_sprites=pygame.sprite.Group()
explode=pygame.sprite.Group()
bulletsp=pygame.sprite.Group()
mob=pygame.sprite.Group()
powerups=pygame.sprite.Group()
player=Player()
all_sprites.add(player)
count=0
shoot_sound=pygame.mixer.Sound("sniper.wav")
crash=pygame.mixer.Sound("crashtree.wav")
for i in range(12):
    enemy=Enemy()
    mob.add(enemy)
    all_sprites.add(enemy)
explode_anim={}
explode_anim["lg"]=[]
for i in range(9):
    img=pygame.image.load("explosions/regularExplosion0{}.png".format(i)).convert()
    img_lg=pygame.transform.scale(img,(58,60))
    explode_anim["lg"].append(img_lg)
power_img={}
pimg=pygame.image.load("bolt.png").convert()
scale_pimg=pygame.transform.scale(pimg,(30,30))
power_img["shield"]=[]
power_img["shield"].append(scale_pimg)

#game loop
play=True
while play:
    
    clock.tick(60)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            play=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                player.shoot()
    #Update entity
    all_sprites.update()
    explode.update()
    #collision check
    hit2=pygame.sprite.groupcollide(bulletsp,mob,True,True)
    for hits in hit2:
       shoot_sound.play()
       count+=15
       enemy=Enemy()
       ex=explosion(hits.rect.centerx,hits.rect.centery)
       mob.add(enemy)
       all_sprites.add(enemy)
       all_sprites.add(ex)
       powe=Power(hits.rect.centerx,hits.rect.centery)
       if random.random()>0.95:
           all_sprites.add(powe)
           powerups.add(powe)
    inc=pygame.sprite.spritecollide(player,powerups,True,pygame.sprite.collide_circle)
    if inc:
        player.health+=1
        if player.health>3:
            player.health=3
    hit=pygame.sprite.spritecollide(player,mob,True,pygame.sprite.collide_circle)
    if hit:
        
        player.health-=1
        crash.play()
        enemy=Enemy()
        mob.add(enemy)
        all_sprites.add(enemy)
        if player.health<0:
            pygame.time.wait(400)                                                                            
            player.health=0
            play=False
     #GameDisplay.fill(black)
    GameDisplay.blit(backgrd,backgrd_rect)
    #after draw
    all_sprites.draw(GameDisplay)
    life(GameDisplay,350,20,player.health)
    text(GameDisplay,"score : "+str(count),40,80,25)
    pygame.display.update()

pygame.quit()
    
