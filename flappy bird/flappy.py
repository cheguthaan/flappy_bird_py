import pygame, sys,random

def draw_floor():
     screen.blit(floor_surface,(floor_x_pos,900))
     screen.blit(floor_surface,(floor_x_pos+576,900))#while the value changes in loop its form a movimg motion

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midtop=(700,random_pipe_pos))#random value from list
    bottom_pipe = pipe_surface.get_rect(midbottom=(700,random_pipe_pos-300))
    return top_pipe,bottom_pipe

def new_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -=5# takes all pipes and move to left -5
    return pipes  

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:#only top pipr touches full height
          screen.blit(pipe_surface,pipe)  
    else:
        flip_pipe = pygame.transform.flip(pipe_surface,False,True)# flip the pipe in x-false flip in y pos -true
        screen.blit(flip_pipe,pipe)  
      
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe): #whether bird collide with pipe
            death_sound.play()
            return False#game stops
        if bird_rect.top <=-100 or bird_rect.bottom >= 900:#on top or hits floor(900)   
            return False
        return True# else game runs 
    
def rotated_bird(bird):#bird animation
    new_bird = pygame.transform.rotozoom(bird,-bird_movement*3,1)#object,rotation value(curvy motion),scale
    return new_bird
   
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))# again arect around bird rect
    return new_bird_rect,new_bird
    
def score_display(game_state):
    if game_state == 'main_game':#if game active
        score_surface = game_font.render(str(int(score)),True,(255,255,255))#render font text,value,rgb,actual score typecasted to int from float
        score_rect = score_surface.get_rect(center=(288,100))#create a rect to display
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':   #if game over
        score_surface = game_font.render(f'Score:{int(score)}',True,(255,255,255))#render font text,value,rgb,actual score typecasted to int from float
        score_rect = score_surface.get_rect(center=(288,100))#create a rect to display
        screen.blit(score_surface,score_rect)
        
        high_score_surface = game_font.render(f'High Score:{int(score)}',True,(255,255,255))#render font text,value,rgb,actual score typecasted to int from float
        high_score_rect = score_surface.get_rect(center=(288,800))#create a rect to display
        screen.blit(high_score_surface,high_score_rect)
   
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score    
 
pygame.mixer.pre_init(frequency = 44100,size=16,channels =1,buffer=512)    #initialize theze before pygame init for sync             
pygame.init()
screen = pygame.display.set_mode((576,1024))#empty background
clock = pygame.time.Clock()#duration for frame
game_font = pygame.font.Font('04B_19.ttf',40)#font style,size
floor_x_pos = 0

#bird variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/background-day.png').convert()#load image
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)

bird_downflip = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())#alpha while adding rotation it gets a black bg to remove it
bird_midflip = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflip = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflip,bird_upflip,bird_midflip]#random choice for diffent bird image
bird_index = 0
bird_surface = bird_frames[bird_index]#based 9n index the bird img changes
bird_rect = bird_surface.get_rect(center=(100,512))# rectangle with top,b,r,l..topright...etc

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)#every 200ms changes 

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT#event triggered bt timer
pygame.time.set_timer(SPAWNPIPE,1200)#setting time 
pipe_height = [400,600,800]
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over = game_over_surface.get_rect(center=(288,512))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')#apply sound
death_sound =pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()  
          sys.exit() 
          
      if event.type == pygame.KEYDOWN:#on key press
          if event.key == pygame.K_SPACE and game_active:# spacebar
              bird_movement = 0 #initial position
              bird_movement -= 12 #bird moves a bit up 0n tap 
              flap_sound.play()#play sound on space bar
              
          if event.key == pygame.K_SPACE and game_active == False:# if game over restart
              game_active = True#restart
              pipe_list.clear()#clear all pipes
              bird_rect.center = (100,512)#initial bird pos
              bird_movement = 0#initial
              score=0#set score to 0 when gets restarts
                  
      if event.type == SPAWNPIPE:
          pipe_list.extend(create_pipe())
          
      if event.type == BIRDFLAP:
          if bird_index < 2:
              bird_index +=1
          else:
              bird_index = 0# only 3 index available ie bird img       
          bied_surface,bird_rect = bird_animation()  #create rect around surface   
    
    screen.blit(bg_surface,(0,0)) #size of loaded image..while the value for image size changes by for loop it form the motion 
    
    if game_active:    #bird
        bird_movement += gravity
        rotated_bird = rotated_bird(bird_surface)#for animation
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_activ = check_collision(pipe_list)# game active is based on collosion 
        
        #pipes
        pipe_list = new_pipes(pipe_list)
        draw_pipes(pipe_list)
        score +=0.01 #score speed
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        high_score = update_score(score,high_score)
        score_display('game_over')    
    #floor
    floor_x_pos -= 1
    draw_floor()   
    if floor_x_pos <=576:
        floor_x_pos = 0 #when reaches 576 it goes back to zero 
    
    pygame.display.update()
    clock.tick(120)# frame rate