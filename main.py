import sys
import pygame
from Scripts.entities import PhysicsEntity
from Scripts.utils import load_image
from random import randint

'''
TODO
-> Follower character
-> Self-collisions
'''


class Game:
    def __init__(self):
        pygame.init()
        
        pygame.display.set_caption("Conga, Conga, Conga!")
        self.screen = pygame.display.set_mode([1080, 720])

        self.clock = pygame.time.Clock()

        self.ymovement = [False, False]
        self.xmovement = [False, False]

        self.top_border = pygame.Rect(0, 0, 1080, 80)
        self.bottom_border = pygame.Rect(0, 640, 1080, 80)
        self.right_border = pygame.Rect(0, 0, 80, 720)
        self.left_border = pygame.Rect(1000, 0, 80, 720)

        self.top_border_des = pygame.Rect(0, 0, 1080, 82)
        self.bottom_border_des = pygame.Rect(0, 638, 1080, 82)
        self.right_border_des = pygame.Rect(0, 0, 82, 720)
        self.left_border_des = pygame.Rect(998, 0, 82, 720)

        self.player_assets = [
            load_image('tile084.png'),
            load_image('tile072.png'),
            load_image('tile088.png'),
            load_image('tile076.png'),
            load_image('tile092.png'),
            load_image('tile078.png'),
            load_image('tile094.png'),
            load_image('tile074.png'),
            load_image('tile090.png'),
            load_image('tile020.png')
        ]
        self.animate = False
        self.player_animate_no = 0
        self.cur_state = 0

        self.followerSpawn = True
        self.count_start = True
        self.count = 0
        self.x = randint(100, 1080-180)
        self.y = randint(100, 720-180)

        self.player = PhysicsEntity(self, 'player', (540, 360), (13, 16))
        self.followerList = []

    def run(self):
        while True:  
            self.screen.fill((14, 219, 24))
            pygame.draw.rect(self.screen, (0,0,0), self.top_border_des)
            pygame.draw.rect(self.screen, (0,0,0), self.bottom_border_des)
            pygame.draw.rect(self.screen, (0,0,0), self.right_border_des)
            pygame.draw.rect(self.screen, (0,0,0), self.left_border_des)
            pygame.draw.rect(self.screen, (255,255,255), self.top_border)
            pygame.draw.rect(self.screen, (255,255,255), self.bottom_border)
            pygame.draw.rect(self.screen, (255,255,255), self.right_border)
            pygame.draw.rect(self.screen, (255,255,255), self.left_border)

            if self.count == 10:
                img = (pygame.font.SysFont("Arial", 50, True)).render("Game Over!", True, (0, 0, 0))
                self.screen.blit(img, (400, 10))
                img = (pygame.font.SysFont("Arial", 50, True)).render("Followers = " + str(self.count), True, (0, 0, 0))
                self.screen.blit(img, (400, 650))
            else:
                img = (pygame.font.SysFont("Arial", 50, True)).render("Conga, Conga, Conga!", True, (0, 0, 0))
                self.screen.blit(img, (320, 10))
                img = (pygame.font.SysFont("Arial", 50, True)).render("Followers = " + str(self.count), True, (0, 0, 0))
                self.screen.blit(img, (400, 650))

                if self.followerSpawn:
                    self.count_start = True
                    self.follower = PhysicsEntity(self, 'follower', (self.x, self.y), (13,16))
                    self.follower.render(self.screen, 9)
                else:
                    self.x = randint(100, 1080-180)
                    self.y = randint(100, 720-180)
                    self.followerSpawn = True
                    if self.count_start:
                        self.count += 1
                        self.count_start = False

                        if len(self.followerList) == 0:
                            self.follower.pos = self.player.prev_pos
                        else:
                            tempprev = self.followerList[-1]
                            self.follower.pos = tempprev.prev_pos
                        (self.followerList).append(self.follower)
                        continue   

                if self.animate:
                    self.player_animate_no += 0.055
                    if self.player_animate_no >= self.cur_state:
                        self.player_animate_no = self.cur_state - 2
                    self.player.render(self.screen, self.player_animate_no)
                else:
                    self.player.render(self.screen, 0)
                    self.player_animate_no = 1
                
                if self.count > 0:
                    for follower in self.followerList:
                        if self.followerList.index(follower) == 0:
                            follower.update_pos(self.player.prev_pos)
                        else:
                            follower.update_pos(self.followerList[(self.followerList.index(follower)-1)].prev_pos)
                        follower.render(self.screen, 9)

                self.player.update((self.xmovement[1] - self.xmovement[0], self.ymovement[1] - self.ymovement[0]))

                player_r = pygame.Rect(self.player.pos[0], self.player.pos[1], 39, 48)
                follower_food_r = pygame.Rect(self.follower.pos[0], self.follower.pos[1], 39, 48)
                
                if player_r.colliderect(self.top_border):
                    self.player.pos[1] = 640 - 48
                if player_r.colliderect(self.bottom_border):
                    self.player.pos[1] = 80
                if player_r.colliderect(self.right_border):
                    self.player.pos[0] = 1000 - 39
                if player_r.colliderect(self.left_border):
                    self.player.pos[0] = 80

                if player_r.colliderect(follower_food_r):
                    self.followerSpawn = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and not self.ymovement[1]:
                        self.ymovement[0] = True
                        self.ymovement[1] = False
                        self.xmovement[0] = False
                        self.xmovement[1] = False
                        self.animate = True
                        self.cur_state = 3
                        self.player_animate_no = self.cur_state - 2
                    if event.key == pygame.K_DOWN and not self.ymovement[0]:
                        self.ymovement[1] = True
                        self.ymovement[0] = False
                        self.xmovement[0] = False
                        self.xmovement[1] = False
                        self.animate = True
                        self.cur_state = 5
                        self.player_animate_no = self.cur_state - 2
                    if event.key == pygame.K_LEFT and not self.xmovement[1]:
                        self.xmovement[0] = True
                        self.xmovement[1] = False
                        self.ymovement[0] = False
                        self.ymovement[1] = False
                        self.animate = True
                        self.cur_state = 7
                        self.player_animate_no = self.cur_state - 2
                    if event.key == pygame.K_RIGHT and not self.xmovement[0]:
                        self.xmovement[1] = True
                        self.xmovement[0] = False
                        self.ymovement[0] = False
                        self.ymovement[1] = False
                        self.animate = True
                        self.cur_state = 9
                        self.player_animate_no = self.cur_state - 2
            
            pygame.display.update()
            self.clock.tick(60)

Game().run()