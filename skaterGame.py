import pygame

pygame.init()
BLACK = 0, 0, 0

####window####
windowWidth = 704
windowHeight = 416
game_window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("SKATER EXTREMMZ")

clock = pygame.time.Clock()

#### all the images ####
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
char = pygame.image.load('standing.png')
bg = pygame.image.load("background.png")


class Player:
    def __init__(self, playerPosX, playerPosY, playerWidth, playerHeight):
        self.playerPosX = playerPosX
        self.playerPosY = playerPosY
        self.playerWidth = playerWidth
        self.playerHeight = playerHeight
        self.velocity = 5
        self.jump = False
        self.jumpHeight = 10
        self.maxJumpHeight = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.playerPosX + 20, self.playerPosY, 20, 60)

    def draw(self, window):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                window.blit(walkLeft[self.walkCount // 3], (self.playerPosX, self.playerPosY))
                self.walkCount += 1
            elif self.right:
                window.blit(walkRight[self.walkCount // 3], (self.playerPosX, self.playerPosY))
                self.walkCount += 1
        else:
            if self.right:
                window.blit(walkRight[0], (self.playerPosX, self.playerPosY))
            else:
                window.blit(walkLeft[0], (self.playerPosX, self.playerPosY))
        self.hitbox = (self.playerPosX + 17, self.playerPosY + 2, 31, 57)  # NEW
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 1)


class RectObstacle(pygame.Rect):
    def __init__(self, obstacle_position_x, obstacle_position_y, obstacle_colour, obstacle_width, obstacle_height):
        super().__init__(obstacle_position_x, obstacle_position_y, obstacle_width, obstacle_height)
        # self.obstacle_position_x = obstacle_position_x
        # self.obstacle_position_y = obstacle_position_y
        self.obstacle_colour = obstacle_colour
        # self.obstacle_height = obstacle_height
        # self.obstacle_position_x = obstacle_position_x
        # self.hitbox = (self.obstacle_position_x + 20, self.obstacle_position_y, 20, 60)
        # self.image = pygame.Surface((obstacle_width, obstacle_height))
        # self.image.fill(BLACK)

    def draw(self, window):
        pygame.draw.rect(window, self.obstacle_colour, self, 0)

character = Player(100, 265, 64, 64)
wall = RectObstacle(200, 225, (0, 0, 0), 50, 50)


def redrawDisplay():
    global walkCount
    game_window.blit(bg, (0, 0))
    wall.draw(game_window)
    character.draw(game_window)
    pygame.display.update()


run = True

while run:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # controls
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and character.playerPosX > character.velocity:
        character.playerPosX -= character.velocity
        character.left = True
        character.right = False
        character.standing = False
    elif keys[pygame.K_RIGHT] and character.playerPosX < 852 - character.playerWidth - character.velocity:
        character.playerPosX += character.velocity
        character.left = False
        character.right = True
        character.standing = False
    else:
        character.standing = True
        character.walkCount = 0

    if not character.jump:
        if keys[pygame.K_UP]:
            character.jump = True
            character.left = False
            character.right = False
            character.walkCount = 0
    else:
        if character.jumpHeight >= -character.maxJumpHeight:
            neg = 1
            if character.jumpHeight < 0:
                neg = -1
            character.playerPosY -= (character.jumpHeight ** 2) * 0.5 * neg
            character.jumpHeight -= 1
        else:
            character.jump = False
            character.jumpHeight = character.maxJumpHeight

    redrawDisplay()

pygame.quit()
