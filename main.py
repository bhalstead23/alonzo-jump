'''alonzo-jump'''

import random
import pygame

KEYDICT = {
    "space": pygame.K_SPACE, "esc": pygame.K_ESCAPE, "up": pygame.K_UP, "down": pygame.K_DOWN,
    "left": pygame.K_LEFT, "right": pygame.K_RIGHT,
    "a": pygame.K_a,
    "b": pygame.K_b,
    "c": pygame.K_c,
    "d": pygame.K_d,
    "e": pygame.K_e,
    "f": pygame.K_f,
    "g": pygame.K_g,
    "h": pygame.K_h,
    "i": pygame.K_i,
    "j": pygame.K_j,
    "k": pygame.K_k,
    "l": pygame.K_l,
    "m": pygame.K_m,
    "n": pygame.K_n,
    "o": pygame.K_o,
    "p": pygame.K_p,
    "q": pygame.K_q,
    "r": pygame.K_r,
    "s": pygame.K_s,
    "t": pygame.K_t,
    "u": pygame.K_u,
    "v": pygame.K_v,
    "w": pygame.K_w,
    "x": pygame.K_x,
    "y": pygame.K_y,
    "z": pygame.K_z,
    "1": pygame.K_1,
    "2": pygame.K_2,
    "3": pygame.K_3,
    "4": pygame.K_4,
    "5": pygame.K_5,
    "6": pygame.K_6,
    "7": pygame.K_7,
    "8": pygame.K_8,
    "9": pygame.K_9,
    "0": pygame.K_0
}

BLACK = (0, 0, 0)
SKYBLUE = (176, 223, 229)


class XboxControl():
    '''maps xbox joystick position directly to the given velocity'''

    def __init__(self):
        self.xbox_joy = pygame.joystick.Joystick(0)
        self.xbox_joy.init()
        # print("Joystick xboxJoy initialized!")

    def update(self, player, run_speed, jump_power, gravity):
        '''call to do physics.
        Pass in instance of Player class and a bunch of self explanatory garbage.'''
        player.vel[0] = self.xbox_joy.get_axis(0) * run_speed
        if self.xbox_joy.get_button(0) == 1 and player.vel[1] == 0:
            player.vel[1] = -jump_power
        else: player.vel[1] += gravity


class Platform(pygame.sprite.Sprite):
    '''Game piece on which Alonzo can stand.'''
    def __init__(self, coords, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color) 
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]


class Player(pygame.sprite.Sprite):
    '''placeholder docstring'''

    def __init__(self, coords, picture):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.coords = coords
        self.vel = [0, 0]
        self.image = pygame.image.load(picture)
        self.rect = self.image.get_rect()
        self.rect.x = self.coords[0]
        self.rect.y = self.coords[1]
        self.mask = pygame.mask.from_surface(self.image)


def generate_map():
    '''randomly generates map consisting of 16-block-long rows of one block each'''
    platform_map = [
        list("...............*"),
        list("..............*."),
        list(".............*.."),
        list("............*..."),
        list("...........*...."),
        list("..........*....."),
        list(".........*......"),
        list("........*......."),
        list(".......*........"),
        list("......*........."),
        list(".....*.........."),
        list("....*..........."),
        list("...*............"),
        list("..*............."),
        list(".*..............")
    ]

    generate_map.platform_list = []
    generate_map.platform_group = pygame.sprite.Group()
    random.shuffle(platform_map)
    platform_map.append("****************")

    for line in platform_map:
        for index in find_all(line, '*'):
            generate_map.platform_list.append(
                Platform([index * 50, platform_map.index(line) * 50], BLACK, 50, 50))
    for i in generate_map.platform_list:
        generate_map.platform_group.add(i)
    # print(len(generate_map.platform_list))

def find_all(search_list, elem):
    '''finds all locations of element elem in list searchList and returns them in list indices'''
    indices = []
    for i in range(0, len(search_list)):
        if search_list[i] == elem:
            indices.append(i)
    return indices

def main():
    '''placeholder docstring'''

    pygame.init()

    pygame.display.set_caption("crab game")
    width, height = 800, 800
    background_color = SKYBLUE
    done = False

    control = XboxControl()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))

    # alonzoRight = alonzo.image
    # alonzoLeft = pygame.transform.flip(alonzo.image, True, False)
    pygame.mixer.music.load("02 Nanobots.mp3")
    # pygame.mixer.music.play()

    generate_map()

    alonzo = Player([300, 200], "3D Alonzo.png")
    while isinstance(pygame.sprite.spritecollideany(alonzo, generate_map.platform_group),
                     pygame.sprite.Sprite):
        alonzo.coords = [random.randint(100, 700), random.randint(100, 700)]

    # main game loop:
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True

        screen.fill(background_color)
        control.update(alonzo, 10, 20, 1)
        # keyControl(alonzo.vel, 0.1, 0.99)
        if (alonzo.rect.left + alonzo.vel[0]) < 0 or (alonzo.rect.right + alonzo.vel[0]) > width:
            alonzo.vel[0] = 0
        if (alonzo.rect.top + alonzo.vel[1]) < 0 or (alonzo.rect.bottom + alonzo.vel[1]) > height:
            alonzo.vel[1] = 0
        for i in generate_map.platform_list:
            if i.rect.colliderect(alonzo.rect.move(alonzo.vel[0], 0)):
                alonzo.vel[0] = 0
            if i.rect.colliderect(alonzo.rect.move(0, alonzo.vel[1])):
                alonzo.vel[1] = 0
        # if pygame.key.get_pressed()[K_d] : alonzo.image = alonzoRight
        # elif pygame.key.get_pressed()[K_a]: alonzo.image = alonzoLeft
        olist = alonzo.mask.outline()
        pygame.draw.polygon(screen, (200, 150, 150), olist, 0)

        screen.blit(alonzo.image, alonzo.rect)
        # print(generate_map.platform_list)
        for i in generate_map.platform_list:
            screen.blit(i.image, i.rect)
            i.rect = i.rect.move(-alonzo.vel[0], -alonzo.vel[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True

        pygame.display.flip()
        clock.tick(60)

main()
pygame.quit()
