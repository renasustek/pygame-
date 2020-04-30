import pygame
import random

pygame.init()
BLACK = 0, 0, 0
score = 0
####window####
window_width = 704
window_height = 416
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("SKATER EXTREMMZ")

clock = pygame.time.Clock()

#### all the images ####
walk_right = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
              pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
              pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walk_left = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
             pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
             pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
char = pygame.image.load('standing.png')
bg = pygame.image.load("background.png")


class Player:
    def __init__(self, player_pos_x, player_pos_y, player_width, player_height):
        self.player_pos_x = player_pos_x
        self.player_pos_y = player_pos_y
        self.player_width = player_width
        self.player_height = player_height
        self.velocity = 5
        self.jump = False
        self.jump_height = 10
        self.max_jump_height = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.hitbox = pygame.Rect(self.player_pos_x + 20, self.player_pos_y, 20, 60)

    def draw(self, window):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
        if not self.standing:
            if self.left:
                window.blit(walk_left[self.walk_count // 3], (self.player_pos_x, self.player_pos_y))
                self.walk_count += 1
            elif self.right:
                window.blit(walk_right[self.walk_count // 3], (self.player_pos_x, self.player_pos_y))
                self.walk_count += 1
        else:
            if self.right:
                window.blit(walk_right[0], (self.player_pos_x, self.player_pos_y))
            else:
                window.blit(walk_left[0], (self.player_pos_x, self.player_pos_y))
        self.hitbox = pygame.Rect(self.player_pos_x + 17, self.player_pos_y + 10, 31, 57)
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 1)

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and character.player_pos_x > character.velocity:
            character.player_pos_x -= character.velocity
            character.left = True
            character.right = False
            character.standing = False

        elif keys[pygame.K_RIGHT] and character.player_pos_x < 852 - character.player_width - character.velocity:
            character.player_pos_x += character.velocity
            character.left = False
            character.right = True
            character.standing = False

        else:
            character.standing = True
            character.walk_count = 0

        if not character.jump:
            if keys[pygame.K_UP]:
                character.jump = True
                character.left = False
                character.right = False
                character.walk_count = 0
        else:
            if character.jump_height >= -character.max_jump_height:
                neg = 1
                if character.jump_height < 0:
                    neg = -1
                character.player_pos_y -= (character.jump_height ** 2) * 0.5 * neg
                character.jump_height -= 1
            else:
                character.jump = False
                character.jump_height = character.max_jump_height

    def collision(self, obs):
        return self.hitbox.colliderect(obs)


class RectObstacle(pygame.Rect):
    def __init__(self, x, y, colour, width, height):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour

    def collision(self, player: Player):
        if self.colliderect(player.hitbox):
            player.player_pos_x = player.player_pos_x - 20
            player.walk_count = 0

    def draw(self, window):
        pygame.draw.rect(window, self.colour, self, 0)


class Coin(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.collided = False
        self.coin_image = pygame.image.load('coin.png')
        self.sound = pygame.mixer.Sound('coin.wav')

    def collision(self, player: Player):
        if self.collided:
            return False
        elif self.colliderect(player.hitbox):
            self.sound.play()
            self.collided = True
            return True
        else:
            return False

    def draw(self, window):
        if not self.collided:
            window.blit(self.coin_image, (self.x, self.y))


character = Player(100, 265, 64, 64)
wall = RectObstacle(200, 230, (13, 122, 35), 25, 105)
coin = Coin(random.randint(0, window_width), 295, 16, 16)


def redraw_display():
    game_window.blit(bg, (0, 0))
    wall.draw(game_window)
    coin.draw(game_window)
    character.draw(game_window)
    pygame.display.update()


run = True
while run:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    wall.collision(character)
    coin.collision(character)

    # controls
    character.movement()

    redraw_display()

pygame.quit()
