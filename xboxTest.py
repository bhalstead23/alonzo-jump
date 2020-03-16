'''
import pygame
pygame.init()

def main(): 
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Joystick Testing / XBOX360 Controller")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

    joysticks = []
    clock = pygame.time.Clock()
    keepPlaying = True

    # for al the connected joysticks
    for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print("Detected joystick " + joysticks[-1].get_name())
    while keepPlaying:
        clock.tick(60)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Received event 'Quit', exiting.")
                    keepPlaying = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    print("Escape key pressed, exiting.")
                    keepPlaying = False
                elif event.type == pygame.KEYDOWN:
                    print("Keydown," + event.key)
                elif event.type == pygame.KEYUP:
                    print("Keyup," + event.key)
                #elif event.type == pygame.MOUSEMOTION:
                 #   print "Mouse movement detected."
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print("Mouse button " + event.button + " down at" + pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONUP:
                    print("Mouse button" + event.button + "up at" + pygame.mouse.get_pos())
                elif event.type == pygame.JOYAXISMOTION:
                    print("Joystick '" + str(joysticks[event.joy].get_name())+ "' axis" + str(event.axis) + "motion.")
                elif event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick '" + str(joysticks[event.joy].get_name()) + "' button" + str(event.button) + "down.")
                    if event.button == 0:
                        background.fill((255, 0, 0))
                    elif event.button == 1:
                        background.fill((0, 0, 255))
                elif event.type == pygame.JOYBUTTONUP:
                    print("Joystick '" + str(joysticks[event.joy].get_name()) + "' button" + str(event.button) + "up.")
                    if event.button == 0:
                        background.fill((255, 255, 255))
                    elif event.button == 1:
                        background.fill((255, 255, 255))
                elif event.type == pygame.JOYHATMOTION:
                    print("Joystick '" + str(joysticks[event.joy].get_name()) + "' hat" + str(event.hat) + " moved.")
                    
        screen.blit(background, (0, 0))
        pygame.display.flip()
        print(str(joysticks))

main()
pygame.quit()
'''

import pygame


# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 700))

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
textPrint = TextPrint()

def find_all(string, sub):
    start = 0
    indices = []
    while start < len(string):
        start = string.find(sub, start)
        if start == -1: break
        indices.append(start)
        start += len(sub)
    return indices


string = "I am a very large noob."

print(find_all(string, "x"))







# -------- Main Program Loop -----------
while not done:
    #
    # EVENT PROCESSING STEP
    #
    # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            done = True # Flag that we are done so we exit this loop.
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    #
    # DRAWING STEP
    #
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()

    textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        textPrint.tprint(screen, "Joystick {}".format(i))
        textPrint.indent()

        # Get the name from the OS for the controller/joystick.
        name = joystick.get_name()
        textPrint.tprint(screen, "Joystick name: {}".format(name))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.tprint(screen, "Number of axes: {}".format(axes))
        textPrint.indent()

        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))
        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()

        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.tprint(screen,
                             "Button {:>2} value: {}".format(i, button))
        textPrint.unindent()

        hats = joystick.get_numhats()
        textPrint.tprint(screen, "Number of hats: {}".format(hats))
        textPrint.indent()

        # Hat position. All or nothing for direction, not a float like
        # get_axis(). Position is a tuple of int values (x, y).
        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)))
        textPrint.unindent()

        textPrint.unindent()

    #
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    #

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second.
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()


