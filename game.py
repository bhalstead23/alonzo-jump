'''alonzo-jump'''

import pygame

BLACK = (0, 0, 0)
SKYBLUE = (176, 223, 229)
TIFFANYBLUE = (0, 180, 171)

# Stuff to do:
    # consider making a level class or maybe a screen class
    # generate_map.start_point is defined in generate_map
    # one level, multiple maps
class XboxControl():
    '''maps xbox joystick position directly to the given velocity'''
    def __init__(self):
        self.xbox_joy = pygame.joystick.Joystick(0)
        self.xbox_joy.init()
        self.jump_timer = 0
        # print("Joystick xboxJoy initialized!")

    def update(self, player, run_speed, jump_power, gravity, can_jump):
        '''call to do physics.
        Pass in instance of Player class and a bunch of self explanatory garbage.'''
        player.vel[0] = self.xbox_joy.get_axis(0) * run_speed
        if self.xbox_joy.get_button(0) == 1 and can_jump:
            player.vel[1] += -jump_power
        else: player.vel[1] += gravity

    def jump_charge(self, player, max_charge):
        if player.vel[1] == 0 and self.jump_timer < 1:
            self.jump_timer = 1
        elif player.vel[1] == 0 and self.jump_timer == 1:
            self.jump_timer = max_charge
        elif player.vel[1] != 0 and self.jump_timer > 0:
            self.jump_timer -= 1
        # print(self.jump_timer)


class Platform(pygame.sprite.Sprite):
    '''Game piece on which Alonzo can stand.'''
    def __init__(self, coords):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load("bricc.png") 
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
    '''placeholder docstring'''

    def __init__(self, coords, picture):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.coords = coords
        self.vel = [0, 0]
        self.image = pygame.transform.scale(pygame.image.load(picture), (50, 59))
        self.rect = self.image.get_rect()
        self.rect.x = self.coords[0]
        self.rect.y = self.coords[1]
        self.mask = pygame.mask.from_surface(self.image)


def quit_check():
    '''quits if the user has closed the program by closing the window or pressing escape'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()

def generate_map(map_num):
    '''randomly generates map consisting of 16-block-long rows of one block each
    starting_coords is defined with centerpoint [400, 400] as origin
    '''

    def find_all(search_list, elem):
        '''finds all locations of element elem in list searchList and returns them in list indices'''
        indices = []
        for i in range(0, len(search_list)):
            if search_list[i] == elem:
                indices.append(i)
        return indices

    platform_map = [
        [ # First Map
            list("*.................................**********"),
            list(".............................***............"),
            list(".............****....*****.................."),
            list("........*..................................."),
            list("...........*................................"),
            list("........*..................................."),
            list("........*..................................."),
            list("............................................"),
            list(".....*****.................................."),
            list("............................................"),
            list("........*..................................."),
            list("............*..............................."),
            list("............................................"),
            list("...............*............................"),
            list("........*...*..............................."),
            list("****........................................")
        ],
        [ # Second Map
            list("*.................................**********"),
            list(".............................***............"),
            list(".............****....*****.................."),
            list("........*..................................."),
            list("...........*................................"),
            list("........*..................................."),
            list("........*..................................."),
            list("............................................"),
            list(".....********.......*********..............."),
            list("............................................"),
            list("........*..................................."),
            list("............*..............................."),
            list("............................................"),
            list("...............*............................"),
            list("........*...*..............................."),
            list("****........................................")
        ],
        [ # Third Map
            list("*.................................**********"),
            list(".............................***............"),
            list(".............****....*****.................."),
            list("........*..................................."),
            list("...........*............***................."),
            list("........*...............***................."),
            list("........*...............***................."),
            list("............................................"),
            list(".....*****.................................."),
            list("............................................"),
            list("........*..................................."),
            list("............*...********************........"),
            list("............................................"),
            list("..*******......*............................"),
            list("........*...*..............................."),
            list("****........................................")
        ]
    ]
    start_points = [
        [-300, -200], # start point for first map
        [-300, -200], # start point for second map
        [-300, -150]  # start point for third map
    ]
    start_point = start_points[map_num]
    generate_map.platform_list = []
    generate_map.starting_coords = []
    generate_map.platform_group = pygame.sprite.Group()

    # adds a safety platform at the bottom for testing
    # platform_map.append("****************")

    for line in platform_map[map_num]:
        for index in find_all(line, '*'):
            generate_map.platform_list.append(
                Platform([index * 50 - start_point[0], platform_map[map_num].index(line) * 50 + start_point[1]]))
    for i in generate_map.platform_list:
        generate_map.starting_coords.append([i.rect.x, i.rect.y])
        generate_map.platform_group.add(i)
    # print(len(generate_map.platform_list))

def title_screen():
    '''displays static title image and waits for user to press A button'''

    screen = pygame.display.set_mode((main.width, main.height))
    clock = pygame.time.Clock()

    done = False
    released = False
    while not done:

        quit_check()

        title = pygame.image.load('title.png')

        if not main.control.xbox_joy.get_button(0):
            released = True
        if main.control.xbox_joy.get_button(0) and released:
            done = True
        screen.blit(title, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def level_screen(level_num):
    '''plays first level. requires running, jumping, and a bit of hanging'''

    screen = pygame.display.set_mode((main.width, main.height))
    clock = pygame.time.Clock()
    alonzo = Player([400, 400], "3D Alonzo.png")
    background_color = SKYBLUE
    # while isinstance(pygame.sprite.spritecollideany(alonzo, generate_map.platform_group),
    #                  pygame.sprite.Sprite):
    #     alonzo.coords = [random.randint(100, 700), random.randint(100, 700)]
    generate_map(level_num)
    # main game loop:
    done = False
    jump_charged = False
    # print("charged!")
    while not done:

        quit_check()

        screen.fill(background_color)
        main.control.update(alonzo, 10, 2, 1.5, jump_charged)
        for i in generate_map.platform_list:
            # olist.append(i.mask.outline())
            # print(i.mask.outline())
            # pygame.draw.polygon(i.image, (200, 150, 150), olist[len(olist)-1], 0)
            if alonzo.rect.colliderect(i.rect.move(-alonzo.vel[0], 0)):
                # if isinstance(pygame.sprite.collide_mask(alonzo, i), tuple):
                #     alonzo.vel[0] = 0
                alonzo.vel[0] = -0.1*alonzo.vel[0]

            if alonzo.rect.colliderect(i.rect.move(0, -alonzo.vel[1])):
                # 
                # print(pygame.sprite.collide_mask(alonzo, i))
                # if isinstance(pygame.sprite.collide_mask(alonzo, i), tuple):
                #     alonzo.vel[1] = 0
                
                alonzo.vel[1] = 0

        main.control.jump_charge(alonzo, 10)
        if main.control.jump_timer > 1:
            jump_charged = True
            # print("charged!")
        else:
            jump_charged = False
        # Uncomment this code to draw the shape of the mask
        # aolist = alonzo.mask.outline()
        # pygame.draw.polygon(alonzo.image, (200, 150, 150), aolist, 0)
        
        screen.blit(alonzo.image, alonzo.rect)
        # print(generate_map.platform_list)
        # dx += -alonzo.vel[0] 
        # dy += -alonzo.vel[1]
        # print("dx:"+str(dx))
        # print("dy:"+str(dy))
        for i in generate_map.platform_list:
            screen.blit(i.image, i.rect)
            i.rect = i.rect.move(-alonzo.vel[0], -alonzo.vel[1])

        # print("x = "+str(generate_map.platform_list[0].rect.x))
        # print("y = "+str(generate_map.platform_list[0].rect.y))
        if generate_map.platform_list[0].rect.y > 450 and generate_map.platform_list[0].rect.x < -1760:
            done = True
        if generate_map.platform_list[0].rect.y < generate_map.starting_coords[0][1] - 500:
            # for i in generate_map.platform_list:
            #     i.rect = i.rect.move(-dx, -dy)
            for i in range(0, len(generate_map.platform_list)):
                generate_map.platform_list[i].rect.x = generate_map.starting_coords[i][0]
                generate_map.platform_list[i].rect.y = generate_map.starting_coords[i][1]
            alonzo.vel = [0, 0]
        pygame.display.flip()
        clock.tick(60)

def level_complete_screen():
    '''displays static level completed image and waits for user to press A button'''
    screen = pygame.display.set_mode((main.width, main.height))
    clock = pygame.time.Clock()

    done = False
    released = False
    while not done:

        quit_check()
        title = pygame.image.load('levelcomplete.png')

        if not main.control.xbox_joy.get_button(0) and not main.control.xbox_joy.get_button(1) and not main.control.xbox_joy.get_button(1):
            released = True
        if main.control.xbox_joy.get_button(0) and released:
            done = True
            return True
        elif main.control.xbox_joy.get_button(1) and released:
            done = True
            return False
        elif main.control.xbox_joy.get_button(2) and released:
            pygame.quit()
        
        screen.blit(title, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def win_screen():
    '''displays static victory image. user can press A button to replay game or press B button to exit.'''

    screen = pygame.display.set_mode((main.width, main.height))
    clock = pygame.time.Clock()
    released = False
    done = False

    while not done:

        quit_check()
        title = pygame.image.load('win.png')

        if not main.control.xbox_joy.get_button(0) and not main.control.xbox_joy.get_button(1):
            released = True

        if main.control.xbox_joy.get_button(1) and released:
            done = True
            return True
        if main.control.xbox_joy.get_button(0) and released:
            return False

        screen.blit(title, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def main():
    '''placeholder docstring'''
    pygame.init()

    pygame.display.set_caption("crab game")
    main.width, main.height = 800, 800

    main.control = XboxControl()

    # alonzoRight = alonzo.image
    # alonzoLeft = pygame.transform.flip(alonzo.image, True, False)
    pygame.mixer.music.load("02 Nanobots.mp3")
    pygame.mixer.music.play()

    done = False
    level = 0
    title_screen()
    while not done:
        level_screen(level)
        if level_complete_screen():
            level += 1
        if level == 3:
            done = win_screen()
            if not done:
                level = 0

main()
pygame.quit()
