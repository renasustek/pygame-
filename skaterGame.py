import pygame
import random

pygame.init()
BLACK = 0, 0, 0
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
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
        self.pos_x = player_pos_x
        self.pos_y = player_pos_y
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
        self.hitbox = pygame.Rect(self.pos_x + 20, self.pos_y + 20, 20, 60)

    def draw(self, window):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
        if not self.standing:
            if self.left:
                window.blit(walk_left[self.walk_count // 3], (self.pos_x, self.pos_y))
                self.walk_count += 1
            elif self.right:
                window.blit(walk_right[self.walk_count // 3], (self.pos_x, self.pos_y))
                self.walk_count += 1
        else:
            if self.right:
                window.blit(walk_right[0], (self.pos_x, self.pos_y))
            else:
                window.blit(walk_left[0], (self.pos_x, self.pos_y))
        self.hitbox = pygame.Rect(self.pos_x + 17, self.pos_y + 10, 31, 57)
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 1)

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and character.pos_x > character.velocity:
            character.pos_x -= character.velocity
            character.left = True
            character.right = False
            character.standing = False

        elif keys[pygame.K_RIGHT] and character.pos_x < window_width - character.player_width - character.velocity:
            character.pos_x += character.velocity
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
                character.pos_y -= (character.jump_height ** 2) * 0.5 * neg
                character.jump_height -= 1
            else:
                character.jump = False
                character.jump_height = character.max_jump_height

    def collision(self, obs):
        return self.hitbox.colliderect(obs)

    def reset(self):
        self.pos_x = self.pos_x - 20
        self.walk_count = 0


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
            player.reset()

    def draw(self, window):
        pygame.draw.rect(window, self.colour, self, 0)


class Coin(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.score = 0
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
            self.score += 1
            return True
        else:
            return False

    def get_score(self):
        return self.score

    def draw(self, window):
        if not self.collided:
            window.blit(self.coin_image, (self.x, self.y))


character = Player(100, 265, 64, 64)
wall = RectObstacle(200, 230, (13, 122, 35), 25, 105)
coin = Coin(random.randint(0, window_width), 295, 16, 16)
font = pygame.font.SysFont('comicsans', 18)


def redraw_display():
    game_window.blit(bg, (0, 0))
    text = font.render(
        'W: ' + str(window_width) + ' H: ' + str(window_height) + ' X: ' + str(character.pos_x) + ' Y: ' + str(
            character.pos_y), 1, (0, 0, 0))
    score_display = font.render("Score: " + str(coin.get_score()), 1, (1, 0, 0))
    game_window.blit(text, (10, 10))
    game_window.blit(score_display,(200, 10))
    coin.draw(game_window)
    wall.draw(game_window)
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