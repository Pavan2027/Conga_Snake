import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = 3
        self.prev_pos = self.pos

    def update(self, movement = (0,0)):
        self.prev_pos[0] = self.pos[0]
        self.prev_pos[1] = self.pos[1]

        self.pos[0] += movement[0] * 3
        self.pos[1] += movement[1] * 3

    def update_pos(self, pos):
        self.prev_pos[0] = self.pos[0]
        self.prev_pos[1] = self.pos[1]
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]

    def render(self, surf, no):
        surf.blit(self.game.player_assets[int(no)], self.pos)
