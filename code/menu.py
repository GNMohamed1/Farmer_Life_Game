import pygame, sys
from settings import *
from timer import Timer
from button import Button


class Menu:
    def __init__(self, player, toggle_menu):

        # general setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surf = pygame.display.get_surface()
        self.font = pygame.font.Font("../font/LycheeSoda.ttf", 30)

        # options
        self.width = 400
        self.space = 10
        self.padding = 8

        # movement
        self.idx = 0
        self.timer = Timer(200)

    def input(self):
        # get input
        keys = pygame.key.get_pressed()
        self.timer.update()

        # if player presses esc then exit the menu
        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.idx -= 1
                self.timer.activate()

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.idx += 1
                self.timer.activate()

            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                self.timer.activate()
                self.space_action()

    def space_action(self):
        pass

    def update(self):
        self.input()


class ShopMenu(Menu):
    def __init__(self, player, toggle_menu):
        super().__init__(player, toggle_menu)
        # entries
        self.options = list(self.player.item_inventory.keys()) + list(
            self.player.seed_inventory.keys()
        )
        self.sell_border = len(self.player.item_inventory) - 1
        self.setup()

    def setup(self):
        # create the text surfaces
        self.text_surfs = []
        self.total_height = 0

        for item in self.options:
            text_surf = self.font.render(item, False, "Black")
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)

        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.menu_left = SCREEN_WIDTH / 2 - self.width / 2
        self.menu_rect = pygame.Rect(
            self.menu_left, self.menu_top, self.width, self.total_height
        )

        # buy / sell text surface
        self.buy_text = self.font.render("buy", False, "Black")
        self.sell_text = self.font.render("sell", False, "Black")

    def display_money(self):
        text_surf = self.font.render(f"${self.player.money}", False, "Black")
        text_rect = text_surf.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.display_surf, "White", text_rect.inflate(10, 10), 0, 4)
        self.display_surf.blit(text_surf, text_rect)

    def input(self):
        super().input()
        # clamo the value
        if self.idx < 0:
            self.idx = len(self.options) - 1
        elif self.idx > len(self.options) - 1:
            self.idx = 0

    def space_action(self):

        # get item
        current_item = self.options[self.idx]

        # sell
        if self.idx <= self.sell_border:
            if self.player.item_inventory[current_item] > 0:
                self.player.item_inventory[current_item] -= 1
                self.player.money += SALE_PRICES[current_item]

        else:
            seed_price = PURCHASE_PRICES[current_item]
            if self.player.money >= seed_price:
                self.player.seed_inventory[current_item] += 1
                self.player.money -= seed_price

    def show_entry(self, text_surf, amount, top, selected: bool):

        # background
        bg_rect = pygame.Rect(
            self.menu_rect.left,
            top,
            self.width,
            text_surf.get_height() + (self.padding * 2),
        )
        pygame.draw.rect(self.display_surf, "White", bg_rect, 0, 4)

        # text
        text_rect = text_surf.get_rect(
            midleft=(self.menu_rect.left + 20, bg_rect.centery)
        )
        self.display_surf.blit(text_surf, text_rect)

        # amount
        amount_surf = self.font.render(str(amount), False, "Black")
        amount_rect = amount_surf.get_rect(
            midright=(self.menu_rect.right - 20, bg_rect.centery)
        )
        self.display_surf.blit(amount_surf, amount_rect)

        # selected
        if selected:
            pygame.draw.rect(self.display_surf, "Black", bg_rect, 4, 4)
            if self.idx <= self.sell_border:  # sell
                pos_rect = self.sell_text.get_rect(
                    midleft=(self.menu_rect.left + 150, bg_rect.centery)
                )
                self.display_surf.blit(self.sell_text, pos_rect)
            else:  # buy
                pos_rect = self.buy_text.get_rect(
                    midleft=(self.menu_rect.left + 150, bg_rect.centery)
                )
                self.display_surf.blit(self.buy_text, pos_rect)

    def update(self):
        super().update()
        self.display_money()
        for text_idx, text_surf in enumerate(self.text_surfs):
            top = self.menu_rect.top + text_idx * (
                text_surf.get_height() + (self.padding * 2) + self.space
            )
            amount_list = list(self.player.item_inventory.values()) + list(
                self.player.seed_inventory.values()
            )
            amount = amount_list[text_idx]
            self.show_entry(text_surf, amount, top, self.idx == text_idx)


class MainMenu:
    def __init__(self, menu_start):
        # setup
        self.display_surf = pygame.display.get_surface()
        self.btn_width = 256
        self.btn_height = 128
        self.padding = ((SCREEN_WIDTH // 2) - self.btn_width // 2, -self.btn_height)
        self.start = menu_start

        # buttons
        self.buttons = []
        self.setup()

    def exit(self):
        pygame.quit()
        sys.exit()

    def setup(self):
        # start button
        pos = (self.padding[0], self.padding[1] * 2)
        self.buttons.append(
            Button("Start", self.btn_width, self.btn_height, pos, self.start)
        )

        # exit button
        pos = (pos[0], self.padding[1])
        self.buttons.append(
            Button("Exit", self.btn_width, self.btn_height, pos, self.exit)
        )

    def update(self):
        for btn in self.buttons:
            if isinstance(btn, Button):
                btn.update()


class PauseMenu:
    def __init__(self, continue_func):
        # setup
        self.display_surf = pygame.display.get_surface()
        self.btn_width = 256
        self.btn_height = 128
        self.padding = ((SCREEN_WIDTH // 2) - self.btn_width // 2, self.btn_height)
        self.continue_func = continue_func

        # buttons
        self.buttons = []
        self.setup()

    def exit(self):
        pygame.quit()
        sys.exit()

    def setup(self):
        # continue button
        pos = (self.padding[0], SCREEN_HEIGHT // 2 - self.btn_height // 2)
        self.buttons.append(
            Button("Continue", self.btn_width, self.btn_height, pos, self.continue_func)
        )

        # exit button
        pos = (pos[0], pos[1] + self.padding[1])
        self.buttons.append(
            Button("Exit", self.btn_width, self.btn_height, pos, self.exit)
        )

    def update(self):
        bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_surface.fill((0, 0, 0))
        bg_surface.set_alpha(50)
        self.display_surf.blit(bg_surface, (0, 0))
        for btn in self.buttons:
            if isinstance(btn, Button):
                btn.update()
