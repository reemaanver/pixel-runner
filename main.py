import pygame
from sys import exit
from random import randint

def display_score(): 
  current_score = pygame.time.get_ticks() // 1000 - start_time 
  score_surf = text_font.render(f'Score: {current_score}', False, (64, 64, 64))
  score_rect = score_surf.get_rect(center = (400, 50))
  pygame.draw.rect(screen, '#c0e8ec', score_rect) 
  pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
  screen.blit(score_surf, score_rect)
  return current_score
def obstacle_movement(obstacle_list):
  if obstacle_list:
    for obs_rect in obstacle_list:
      obs_rect.x -= 5 

      if obs_rect.bottom == 300:
        screen.blit(snail_surface, obs_rect)
      else:
        screen.blit(fly_surface, obs_rect)

    obstacle_list = [i for i in obstacle_list if i.x > -100]

    return obstacle_list
  else: 
    return []
def collision(player_rect, obstacle_list):
  for obs in obstacle_list:
    if obs.colliderect(player_rect):
      return False
  return True

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Pixel Runner')
clock = pygame.time.Clock()
text_font = pygame.font.Font('Font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# obstacles
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surface = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()

obstacle_rect_list = []

player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0 

# Loading screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = text_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = text_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 330))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

    if game_active:
      if event.type == pygame.MOUSEBUTTONDOWN:
        if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300: 
          player_gravity = -20


      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
          player_gravity = -20

      if event.type == obstacle_timer:
        if randint(0, 2):
          obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900, 1100), 300)))
        else:
          obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900, 1100), 210)))
    else:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
          game_active = True
          start_time = pygame.time.get_ticks() // 1000 
    
  if game_active:
    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0, 300))
    score = display_score()

    #player
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 300:
      player_rect.bottom = 300
    screen.blit(player_surface, player_rect)

    # obstacle logic
    obstacle_rect_list = obstacle_movement(obstacle_rect_list)

    # collision
    game_active = collision(player_rect, obstacle_rect_list)
    
  else:
    screen.fill((94, 129, 162))
    screen.blit(game_name, game_name_rect)
    screen.blit(player_stand, player_stand_rect)
    player_rect.midbottom = (80, 300)
    player_gravity = 0
    obstacle_rect_list.clear()

    score_message = text_font.render(f'Your score: {score}', False, (111, 196, 169))
    score_message_rect = score_message.get_rect(center = (400, 330))
    if score != 0: screen.blit(score_message, score_message_rect)
    else: screen.blit(game_message, game_message_rect)
    

  pygame.display.update()
  clock.tick(60)