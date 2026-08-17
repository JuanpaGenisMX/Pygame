### Libraries ###
try:
    import pygame, sys, random, os, math, numpy
    from pygame.locals import *
except ModuleNotFoundError as err:
    print(f"module not found, {err}")
except ImportError as err:
    print(f"couldn't load module, {err}")

#### Global variables ###
run = True
fps = 60

playerSpeed = 500
playerHealth = 100
playerDamage = 8

#### Classes ###
# Player class
class Player():
    def __init__(self, sprite, pos, hp, speed, damage):
        self.sprite = sprite
        self.position = pos
        self.health = hp
        self.speed = speed
        self.damage = damage

    def Movement(self, delta):
        inputs = numpy.array([0.0, 0.0])
        pressedKey = pygame.key.get_pressed()

        if pressedKey[pygame.K_w] and pressedKey[pygame.K_s]:
            inputs[1] = 0
        else:
            if pressedKey[pygame.K_w]:
                inputs[1] = -1.0
            if pressedKey[pygame.K_s]:
                inputs[1] = 1.0

        if pressedKey[pygame.K_a] and pressedKey[pygame.K_d]:
            inputs[0] = 0
        else:
            if pressedKey[pygame.K_a]:
                inputs[0] = -1.0
            if pressedKey[pygame.K_d]:
                inputs[0] = 1.0

        magnitud = inputs[0]**2 + inputs[1]**2

        if magnitud > 1.0:
            inputs /= math.sqrt(magnitud)

        self.position.x += inputs[0] * self.speed * delta
        self.position.y += inputs[1] * self.speed * delta

    def Shoot(self):
        pass

    def RecieveDamage(self):
        pass

    def Die(self):
        pass

# Enemy Class
class Enemy():
    def __init__(self, sprite, pos, hp, speed, damage):
        self.sprite = sprite
        self.position = pos
        self.health = hp
        self.speed = speed
        self.damage = damage

    def Movement(self):
        pass

    def Damage(self):
        pass

### Game ###
def Main():
    # Variables
    global run, playerSpeed, playerHealth, fps

    spritesWidth = 100

    # Initialize pygame
    pygame.init()
    ClearTerminal()

    # Screen config
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("a014")
    clock = pygame.time.Clock()

    # Entities
    player = Player (
        LoadSprite("Assets/Player.png", spritesWidth, spritesWidth),
        pygame.Vector2((screen.get_width() / 2) - spritesWidth, screen.get_height() / 2),
        playerHealth, playerSpeed, playerDamage
    )

    # Posible errors
    RenderingErrorHandler (
        player.sprite
    )

    # Game loop
    while run:
        # Quit game
        for events in pygame.event.get():
            if events.type == QUIT:
                run = False

        # Physiscs
        clockDeltatime = clock.tick(fps) / 1000.0

        # Game Logic
        if CanMove(player, spritesWidth, screen):
            player.Movement(clockDeltatime)

        # Rendering
        screen.fill("white")
        screen.blit(player.sprite, (player.position))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

### Functions ###
# Player Movement
def CanMove(entity, size, screen):
    screenSize = numpy.array([screen.get_width(), screen.get_height()])
    entityPos = numpy.array([entity.position.x, entity.position.y])

    canMove = True

    if entityPos[0] < 0:
        canMove = Collitions(entity, "-", "x")

    if entityPos[1] < 0:
        canMove = Collitions(entity, "-", "y")

    if entityPos[0] + size > screenSize[0]:
        canMove = Collitions(entity, "+", "x")

    if entityPos[1] + size > screenSize[1]:
        canMove = Collitions(entity, "+", "y")

    return canMove

# Collition Correction
def Collitions(entity, side, axis):
    if axis == "x":
        if side == "-":
            entity.position.x += 1
        else:
            entity.position.x -= 1

    elif axis == "y":
        if side == "-":
            entity.position.y += 1
        else:
            entity.position.y -= 1

    return False

# Rendering assets
def LoadSprite(sprite, sizeX, sizeY):
    try:
        return pygame.transform.scale(pygame.image.load(sprite).convert_alpha(), (sizeX, sizeY))
    except:
        print(f"File in route '{sprite}' not found")
        return None

def RenderingErrorHandler(*errs):
    global run
    for errors in errs:
        if errors == None:
            run = False
            break

def ClearTerminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

if __name__ == "__main__":
    Main()