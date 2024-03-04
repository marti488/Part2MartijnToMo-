import pygame

pygame.init()

# Font that is used to render the text
font20 = pygame.font.Font('freesansbold.ttf', 20)

# RGB values of standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Basic parameters of the screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
FPS = 30


# The Striker class handles the player information: this means score, green rectangle, etc.

class Striker:
    # Take the initial position, dimensions, speed and color of the object
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        # Rect that is used to control the position and collision of the object
        self.leerlingRect = pygame.Rect(posx, posy, width, height)
        # Object that is put on the screen
        self.leerling = pygame.draw.rect(screen, self.color, self.leerlingRect)

    # Used to display the object on the screen
    def display(self):
        self.leerling = pygame.draw.rect(screen, self.color, self.leerlingRect)

    # Used to move the striker up or down
    def update(self, yFac):
        self.posy = self.posy + self.speed * yFac

        # Restricting the striker to be below the top surface of the screen
        if self.posy <= 0:
            self.posy = 0
        # Restricting the striker to be above the bottom surface of the screen
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height

        # Updating the rect with the new values
        self.leerlingRect = (self.posx, self.posy, self.width, self.height)

    # displays the score for the user
    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)

    def getRect(self):
        return self.leerlingRect


# Ball class

class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1

    # draw the ball
    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)

    # update the ball's position to it's next point in time
    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac

        # If the ball hits the top or bottom surfaces,
        # then the sign of yFac is changed and
        # it results in a reflection
        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1

        # If the ball hits the right or left of the screen, return -1 or +1 to signify which user has won a point.
        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    # when the ball goes out of bounds, reset its position to the middle of the screen
    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        # reverse the balls direction horizontally: if the ball went out of bounds on the left side,
        # it spawns moving to the right (and vice versa)
        self.xFac *= -1
        self.firstTime = 1

    # Used to reflect the ball along the X-axis
    def hit(self):
        self.xFac *= -1

    def getRect(self):
        return self.ball


# The 'Game Manager': this main function handles input and updates the game in time.

def main():
    running = True

    # Defining the objects
    leerling1 = Striker(20, 0, 10, 100, 10, GREEN)
    # the posx of striker 2 is 30 from the edge, because it's width is 10 units in the x-axis direction.
    # this means both strikers will be seperated from the wall by 20 units.
    leerling2 = Striker(WIDTH - 30, 0, 10, 100, 10, GREEN)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 7, WHITE)


    listOfleerlings = [leerling1, leerling2]

    # Initial parameters of the players
    leerling1Score, leerling2Score = 0, 0
    leerling1YFac, leerling2YFac = 0, 0

    # the main loop. User inputs are gathered and handled.
    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            # if the user quits the game via the x button on the top right, the loop stops.
            if event.type == pygame.QUIT:
                running = False

            # when a key is pressed, update the rectangles velocity accordingly:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    leerling2YFac = -1
                if event.key == pygame.K_DOWN:
                    leerling2YFac = 1
                if event.key == pygame.K_z:
                    leerling1YFac = -1
                if event.key == pygame.K_s:
                    leerling1YFac = 1

            # when a key is no longer pressed, reset the rectangles velocity to zero:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    leerling2YFac = 0
                if event.key == pygame.K_z or event.key == pygame.K_s:
                    leerling1YFac = 0

        # Collision detection
        for leerling in listOfleerlings:
            if pygame.Rect.colliderect(ball.getRect(), leerling.getRect()):
                ball.hit()

        # Updating the objects
        leerling1.update(leerling1YFac)
        leerling2.update(leerling2YFac)
        # point receives 0, +1 or -1
        point = ball.update()

        # -1 -> leerling_1 has scored
        # +1 -> leerling_2 has scored
        # 0 -> None of them scored
        if point == -1:
            leerling1Score += 1
        elif point == 1:
            leerling2Score += 1

        # Someone has scored
        # a point and the ball is out of bounds.
        # So, we reset its position
        if point:
            ball.reset()

        # Displaying the objects on the screen: balls and player rectangles. This does not yet show them on screen,
        # it only tells the pygame application what it will need to display when it updates.
        leerling1.display()
        leerling2.display()
        ball.display()

        # Displaying the scores of the players
        leerling1.displayScore("leerling_1 : ",
                           leerling1Score, 100, 20, WHITE)
        leerling2.displayScore("leerling_2 : ",
                           leerling2Score, WIDTH - 100, 20, WHITE)

        # update the visuals after everything else has been handled
        pygame.display.update()

        # go to a new frame after 1/30th of a second (current fps rate)
        clock.tick(FPS)

# if we play this program as the main program (and not import it from somewhere else e.g.), execute the main function
if __name__ == "__main__":
    main()
    pygame.quit()
