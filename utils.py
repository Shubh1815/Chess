import pygame as pg


class Label:

    def __init__(self, string):
        self.string = string
        self.style = {
            'color': (0, 0, 0),
            'font_family': "helvetica",
            'font_size': 16,
        }

        font = pg.font.SysFont(self.style['font_family'], self.style['font_size'])
        self.text = font.render(self.string, True, self.style['color'])

    def config(self, color=(0, 0, 0), font_family="helvetica", font_size=16):
        self.style = {
            'color': color,
            'font_family': font_family,
            'font_size': font_size,
        }

        font = pg.font.SysFont(self.style['font_family'], self.style['font_size'])
        self.text = font.render(self.string, True, self.style['color'])

    def change_text(self, string):
        self.string = string

        font = pg.font.SysFont(self.style['font_family'], self.style['font_size'])
        self.text = font.render(self.string, True, self.style['color'])

    def draw(self, screen, pos_x, pos_y):
        screen.blit(self.text, (pos_x, pos_y))

    def get_rect(self):
        return self.text.get_rect()


class Button:

    def __init__(self, text, pos, on_click):
        self.on_click = on_click
        self.pos = pos
        self.text = text

        self.style = {
            'bg': (0, 0, 0),
            'fg': (255, 255, 255),
            'hover': (0, 0, 0),
            'outline': True
        }

        self.hovered = 0

    def config(self, bg=(0, 0, 0), fg=(255, 255, 255), hover=(0, 0, 0), outline=True):
        self.style = {
            'bg': bg,
            'fg': fg,
            'hover': hover,
            'outline': outline
        }

    def draw(self, screen):
        pos_x, pos_y, width, height = self.pos
        bg = self.style['bg'] if not self.hovered else self.style['hover']

        if self.style['outline']:
            pg.draw.rect(
                screen,
                self.style['fg'],
                (pos_x - 2, pos_y - 2, width + 4, height + 4)    
            )

        button_rect = pg.draw.rect(
            screen,
            bg,
            (pos_x, pos_y, width, height)
        )

        text = Label(self.text)
        text.config(
            color=self.style['fg'],
            font_size=24
        )
        text_rect = text.get_rect()
        text_rect.center = button_rect.center
        text.draw(screen, text_rect.x, text_rect.y)

    def collide(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        pos_x, pos_y, width, height = self.pos

        if pos_x <= mouse_x <= pos_x + width and \
           pos_y <= mouse_y <= pos_y + height:

            self.on_click()

    def mouseover(self, screen, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        pos_x, pos_y, width, height = self.pos

        if pos_x <= mouse_x <= pos_x + width and \
           pos_y <= mouse_y <= pos_y + height:

            self.hovered = 1
            self.draw(screen)

        elif self.hovered:

            self.hovered = 0
            self.draw(screen)
