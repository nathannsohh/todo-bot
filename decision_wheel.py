import pygame
import math
import random

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define width, height and radius
WIDTH = 640
HEIGHT = 480
RADIUS = 200
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

class DecisionWheel:
    def __init__(self, num_segments: int, options: list) -> None:
        self.num_segments = num_segments
        self.options = options
        self.seg_angle = 360 / num_segments
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Decision Wheel")
        self.screen.fill(WHITE)

        # Define font
        self.font = pygame.font.Font(None, 18)

        self.spin_speed = 0
        self.angle = 0
        self.spinning = False
        self.selection = ""

    # draw some text into an area of a surface
    # automatically wraps words
    # returns any text that didn't get blitted
    def draw_text(self, text, rect, max_width, center_x, center_y):
        rect = pygame.Rect(rect)
        y = rect.top
        lineSpacing = -2

        # get the height of the font
        fontHeight = self.font.size("Tg")[1]
        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while self.font.size(text[:i])[0] < max_width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word      
            # if i < len(text): 
            #     i = text.rfind(" ", 0, i) + 1

            image = self.font.render(text[:i], True, BLACK)
            text_rect = image.get_rect()
            text_rect.center = (center_x, center_y)
            angle_to_horizontal = math.degrees(math.atan2(center_y-CENTER_Y, center_x-CENTER_X))
            rotated_text = pygame.transform.rotate(image, -angle_to_horizontal)

            self.screen.blit(rotated_text, text_rect)
            y += fontHeight + lineSpacing
            center_y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

        return text


    # Define function to draw a segment
    def draw_segment(self, color, start_angle, end_angle, option):
        points = [(self.center_x, self.center_y)]
        center_angle = (start_angle + end_angle) / 2
        for i in range(start_angle, end_angle+1):
            x = CENTER_X + int(RADIUS * math.cos(math.radians(i)))
            y = CENTER_Y + int(RADIUS * math.sin(math.radians(i)))
            points.append((x, y))
        points.append((self.center_x, self.center_y))
        segment = pygame.draw.polygon(self.screen, color, points)
        segment_width = abs(int(RADIUS * math.cos(math.radians(start_angle))) - int(RADIUS * math.cos(math.radians(end_angle))))
        text = self.font.render(option, True, BLACK)
        text_rect = text.get_rect()
        text_center_x = CENTER_X + int(RADIUS*0.6*math.cos(math.radians(center_angle)))
        text_center_y = CENTER_Y + int(RADIUS*0.6*math.sin(math.radians(center_angle)))
        text_rect.center = (text_center_x, text_center_y)
        angle_to_horizontal = math.degrees(math.atan2(text_center_y-CENTER_Y, text_center_x-CENTER_X))
        rotated_text = pygame.transform.rotate(text, -angle_to_horizontal)
        # self.draw_text(option, segment, segment_width, text_center_x, text_center_y)
        self.screen.blit(rotated_text, text_rect)


    # Define function to spin the wheel
    def spin_wheel(self):
        global angle, spinning, selection
        # self.spin_speed = random.randint(30, 50)
        self.spin_speed = 0.5
        angle = 0
        self.spinning = True
        while self.spin_speed > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.screen.fill(WHITE)
            for i in range(self.num_segments):
                start_angle = int(i * self.seg_angle + angle)
                end_angle = int((i+1) * self.seg_angle + angle - 1)
                color = [RED, GREEN, YELLOW, BLUE][i%4]
                self.draw_segment(color, start_angle, end_angle, self.options[i])
            pygame.draw.circle(self.screen, BLACK, (self.center_x, self.center_y), RADIUS, 5)
            angle += self.spin_speed
            self.spin_speed -= 0.0000001
            pygame.display.flip()
        self.spinning = False
        self.selection = self.get_selection()

    # Define function to get the selection
    def get_selection(self):
        global angle
        for i in range(self.num_segments):
            start_angle = i * self.seg_angle + angle
            end_angle = (i+1) * self.seg_angle + angle - 1
            if start_angle <= 360 <= end_angle:
                return "Segment " + str(i+1)
            
    def run(self):
        # Main game loop
        running = True
        self.spin_wheel()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.spinning:
                        self.spin_wheel()
            if self.spinning:
                text = self.font.render("Spinning...", True, BLACK)
            elif self.selection:
                text = self.font.render(selection, True, BLACK)
            else:
                text = self.font.render("Click to spin!", True, BLACK)

if __name__ == "__main__":
    decisionWheel = DecisionWheel(5, ["Talking till the sun rises", "Test2343111111", "Test3", "Test4", "Test5"])
    decisionWheel.run()

