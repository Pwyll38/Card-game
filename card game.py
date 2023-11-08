#Import section
import pygame
import random

pygame.init()
pygame.font.init()

#Constants
CLOCK = pygame.time.Clock()
WIN_HEIGHT = 540
WIN_WIDTH = 960
WINDOW_SIZE = (WIN_WIDTH,WIN_HEIGHT)
FONT_DEBUG = pygame.font.Font('Grand9K Pixel.ttf', 20)
CARD_POSITIONS = [70, 240, 410, 580, 750]
TEXT_DEFAUT_MAX_WIDTH = 250

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)

#Window
pygame.display.set_caption("Card game")
window = pygame.display.set_mode(WINDOW_SIZE, 0, 0)

#global functs

def blit_text(surface, text, pos, font,max_width, color=pygame.Color('black')):   #taken from stackoverflow
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

#classes
#player
class Player():
    def __init__(self) -> None:
        self.x = 100
        self.y = 150
        self.hp = 100
        self.WIDTH = 50
        self.HEIGHT = 50
    
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
    
    def render_health(self):
        health_rect = pygame.Rect(20,20, self.hp*2, 30)
        pygame.draw.rect(window, (0,250,0), health_rect)
        blit_text(window, str(self.hp), (240, -10), FONT_DEBUG,TEXT_DEFAUT_MAX_WIDTH, BLACK)

    def render(self):
        self.rect.update(self.x, self.y, self.WIDTH, self.HEIGHT)

        pygame.draw.rect(window, BLACK, self.rect)
        self.render_health()

    def update(self):
        self.render()
        
player = Player()

class Enemy():
    def __init__(self) -> None:
        self.x = 810
        self.y = 150
        self.hp = 100
        self.WIDTH = 50
        self.HEIGHT = 50
        self.alive = True
    
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
    
    def render_health(self):
        health_rect = pygame.Rect(730,20, self.hp*2, 30)
        pygame.draw.rect(window, (250,0,0), health_rect)
        blit_text(window, str(self.hp), (670, -10), FONT_DEBUG,TEXT_DEFAUT_MAX_WIDTH, BLACK)

    def render(self):
        if(self.alive):
            self.rect.update(self.x, self.y, self.WIDTH, self.HEIGHT)
            pygame.draw.rect(window, (200,0,0), self.rect)

            self.render_health()

        else:
            blit_text(window, "He dededed", (self.x-10, self.y - 70), FONT_DEBUG,TEXT_DEFAUT_MAX_WIDTH, BLACK)

    def update(self):
        if(self.hp<=0):
            self.alive = False
        
        self.render()
        
enemy = Enemy()

#Cards

cards = []
class Card():
    def __init__(self, position) -> None:
        self.x = CARD_POSITIONS[position]
        self.y = 300
        self.WIDTH = 150
        self.HEIGHT = 200
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def render(self):
        pygame.draw.rect(window, BLACK, self.rect, 10)

        blit_text(window, self.text, (self.x+15, self.y+30), FONT_DEBUG,900, BLACK)

    def update(self, event_list):

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.effect()

        self.render()

class Heal_Card(Card):
    def __init__(self, position) -> None:
        self.heal = random.randint(5,25)
        self.text = "Heal " + str(self.heal) + " hp"
        super().__init__(position)

    def effect(self):
        player.hp += self.heal
        cards.remove(self)

class Damage_Card(Card):
    def __init__(self, position) -> None:
        self.dmg = random.randint(1,10)
        self.text = "Deal "+str(self.dmg)+" dmg"
        super().__init__(position)

    def effect(self):
        enemy.hp -= self.dmg
        cards.remove(self)

#Buttons

class Button():
    def __init__(self) -> None:
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def render(self):
            pygame.draw.rect(window, BLACK, self.rect, 10)
            blit_text(window,self.text, (self.x+self.text_pos_x, self.y+self.text_pos_y), FONT_DEBUG, 900, BLACK)

    def update(self, event_list):

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.effect()

        self.render()

class Shuffle_Button(Button):
    def __init__(self) -> None:
        self.x = 370
        self.y = 30
        self.WIDTH = 190
        self.HEIGHT = 50
        self.text = "Shuffle cards"
        self.text_pos_x = 15
        self.text_pos_y = 10

        super().__init__()
        

    def effect(self):
        cards.clear()
        for i in range(0,5):
            type = random.randint(0,1)
            if (type == 0):
                cards.append(Heal_Card(i))
            if (type == 1):
                cards.append(Damage_Card(i))

shuffle_btn = Shuffle_Button()

class End_Turn_Button(Button):
    def __init__(self) -> None:
        self.x = 700
        self.y = 220
        self.WIDTH = 190
        self.HEIGHT = 50
        self.text = "End turn"
        self.text_pos_x = 15
        self.text_pos_y = 10

        super().__init__()
        

    def effect(self):
        player.hp -= random.randrange(10,30)

end_turn = End_Turn_Button()


#mainloop
def mainloop():
    running = True
    while(running):

        #Keys control
        keys = []
        event_list =  pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                keys.append(event.key)
                if event.key == pygame.K_ESCAPE:
                    running = False

        #renders
        window.fill(WHITE)
        player.update()
        enemy.update()
        shuffle_btn.update(event_list)
        end_turn.update(event_list)


        for card in cards:
            card.update(event_list)


        #Finalize
        pygame.display.update()
        CLOCK.tick(60)

if __name__ == "__main__":
    mainloop()