import pygame
import sys
import random


class Button:
    def __init__(self, surface, color, x, y, width, height, text=''):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.active = True

    def draw(self, outline=None):
        if outline:
            pygame.draw.rect(self.surface, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(self.surface, self.color if self.active else (100, 100, 100),
                         (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont(None, 30)
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
            self.surface.blit(text_surface, text_rect)

    def is_over(self, pos):
        if self.active:
            if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
                return True
        return False


class Key:
    def __init__(self, surface, image_path, x, y):
        self.surface = surface
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw_key(self):
        if not self.clicked:
            self.surface.blit(self.image, self.rect)

    def is_clicked(self, pos):
        if not self.clicked and self.rect.collidepoint(pos):
            self.clicked = True
            return True
        return False

class Textbox:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 200, 30)
        self.text = ""
        self.active = False
        self.color = (0, 0, 0)
        self.visible = True

    def handle_event(self, event):
        if self.visible:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = (255, 0, 0) if self.active else (0, 0, 0)

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, self.color, self.rect, 2)
            font = pygame.font.Font(None, 36)
            text_surface = font.render(self.text, True, (0, 0, 0))
            screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def get_text(self):
        return self.text


class SkærmTæller:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        #pygame.mixer.music.load("MGR.mp3")
        #pygame.mixer.music.play(-1)
        self.skaerm_bredde = 800
        self.skaerm_hoejde = 600
        self.skaerm = pygame.display.set_mode((self.skaerm_bredde, self.skaerm_hoejde))
        pygame.display.set_caption("Skærmtæller")
        self.font = pygame.font.SysFont(None, 30)
        self.koerer = True
        self.nuvaerende_skaerm = 0
        self.skaerm_stack = []

        self.start_button = Button(self.skaerm, (0, 0, 0), 400, 275, 200, 50, "Start")
        self.left_button = Button(self.skaerm, (0, 0, 0), 50, 200, 50, 200, "Venstre")
        self.right_button = Button(self.skaerm, (0, 0, 0), 700, 200, 50, 200, "Højre")

        self.key1 = Key(self.skaerm, "KEy_2.png", 100, 100)
        self.key2 = Key(self.skaerm, "KEy_1.png", 600, 100)
        self.key3 = Key(self.skaerm, "KEy_2.png", 300, 100)

        self.key1_clicked = False
        self.key2_clicked = False
        self.key3_clicked = False

        self.screen_4_button = Button(self.skaerm, (255, 0, 255), 300, 300, 50, 50, "Æg")
        self.screen_5_button = Button(self.skaerm, (255, 0, 255), 300, 200, 50, 50, "Æble")
        self.screen_6_button = Button(self.skaerm, (255, 0, 255), 300, 100, 50, 50, "Mælk")
        self.screen_9_button = Button(self.skaerm, (255, 0, 255), 400, 200, 50, 50, "Banan")
        self.screen_10_button = Button(self.skaerm, (255, 0, 255), 400, 300, 50, 50, "Sten")
        self.screen_11_button = Button(self.skaerm, (255, 0, 255), 300, 400, 50, 50, "Gren")
        self.screen_12_button = Button(self.skaerm, (255, 0, 255), 400, 100, 50, 50, "Stol")
        self.screen_13_button = Button(self.skaerm, (255, 0, 255), 400, 400, 50, 50, "Cement")

        self.buttons_clicked = {self.screen_4_button: False,
                                self.screen_5_button: False,
                                self.screen_6_button: False,
                                self.screen_9_button: False}

        self.screen_14_button = Button(self.skaerm, (0, 0, 255), 600, 100, 50, 50, "Bold")
        self.screen_15_button = Button(self.skaerm, (0, 0, 255), 200, 500, 50, 50, "Hold")
        self.screen_16_button = Button(self.skaerm, (0, 0, 255), 500, 400, 50, 50, "Hop")
        self.screen_17_button = Button(self.skaerm, (0, 0, 255), 200, 300, 50, 50, "Op")
        self.screen_18_button = Button(self.skaerm, (0, 0, 255), 600, 500, 50, 50, "Skål")
        self.screen_19_button = Button(self.skaerm, (0, 0, 255), 200, 100, 50, 50, "Mål")
        self.screen_20_button = Button(self.skaerm, (0, 0, 255), 500, 500, 50, 50, "Trommer")
        self.screen_21_button = Button(self.skaerm, (0, 0, 255), 200, 400, 50, 50, "Sommer")
        self.screen_22_button = Button(self.skaerm, (0, 0, 255), 600, 300, 50, 50, "Kat")
        self.screen_23_button = Button(self.skaerm, (0, 0, 255), 200, 200, 50, 50, "At")
        self.screen_24_button = Button(self.skaerm, (0, 0, 255), 500, 100, 50, 50, "Granit")
        self.screen_25_button = Button(self.skaerm, (0, 0, 255), 600, 200, 50, 50, "Kamel")
        self.screen_26_button = Button(self.skaerm, (0, 0, 255), 500, 300, 50, 50, "Fedt")
        self.screen_27_button = Button(self.skaerm, (0, 0, 255), 600, 400, 50, 50, "Kanin")
        self.screen_28_button = Button(self.skaerm, (0, 0, 255), 500, 200, 50, 50, "Måne")
        self.screen_29_button = Button(self.skaerm, (0, 0, 255), 600, 200, 50, 50, "Fandt")
        self.screen_30_button = Button(self.skaerm, (0, 0, 255), 200, 500, 50, 50, "Blandt")
        self.screen_31_button = Button(self.skaerm, (0, 0, 255), 500, 400, 50, 50, "Hund")
        self.screen_32_button = Button(self.skaerm, (0, 0, 255), 200, 300, 50, 50, "Stund")
        self.screen_33_button = Button(self.skaerm, (0, 0, 255), 500, 300, 50, 50, "Stråle")
        self.screen_34_button = Button(self.skaerm, (0, 0, 255), 200, 100, 50, 50, "Åle")
        self.screen_35_button = Button(self.skaerm, (0, 0, 255), 500, 500, 50, 50, "Ballade")
        self.screen_36_button = Button(self.skaerm, (0, 0, 255), 200, 400, 50, 50, "Marmelade")
        self.screen_37_button = Button(self.skaerm, (0, 0, 255), 500, 100, 50, 50, "Hest")
        self.screen_38_button = Button(self.skaerm, (0, 0, 255), 200, 200, 50, 50, "Bedst")
        self.screen_39_button = Button(self.skaerm, (0, 0, 255), 600, 300, 50, 50, "Østers")
        self.screen_40_button = Button(self.skaerm, (0, 0, 255), 600, 100, 50, 50, "Bavian")
        self.screen_41_button = Button(self.skaerm, (0, 0, 255), 600, 500, 50, 50, "Mand")
        self.screen_42_button = Button(self.skaerm, (0, 0, 255), 600, 400, 50, 50, "Joe")
        self.screen_43_button = Button(self.skaerm, (0, 0, 255), 500, 200, 50, 50, "Bord")

        self.textbox = Textbox(300, 200)
        self.textbox1 = Textbox(300, 160)
        self.textbox2 = Textbox(300, 120)
        self.textbox3 = Textbox(300, 80)



        self.right_button_active = False

        button_names = [
            "button_14_clicked",
            "button_15_clicked",
            "button_16_clicked",
            "button_17_clicked",
            "button_18_clicked",
            "button_19_clicked",
            "button_20_clicked",
            "button_21_clicked",
            "button_22_clicked",
            "button_23_clicked",
            "button_29_clicked",
            "button_30_clicked",
            "button_31_clicked",
            "button_32_clicked",
            "button_33_clicked",
            "button_34_clicked",
            "button_35_clicked",
            "button_36_clicked",
            "button_37_clicked",
            "button_38_clicked"
        ]

        for button_name in button_names:
            setattr(self, button_name, False)

        self.message_printed = False
        self.message2_printed = False
        self.message3_printed = False
        self.message4_printed = False
        self.message5_printed = False
        self.message6_printed = False
        self.message7_printed = False
        self.message8_printed = False
        self.message9_printed = False
        self.message10_printed = False

        self.point_6 = 0
        self.point_9 = 0
        self.correct_count = 0
        self.right_button_active = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.koerer = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if len(self.skaerm_stack) > 0:
                        self.nuvaerende_skaerm = self.skaerm_stack.pop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.nuvaerende_skaerm == 0:
                    if event.button == pygame.BUTTON_LEFT and self.start_button.is_over(event.pos):
                        self.nuvaerende_skaerm = 1
                elif self.nuvaerende_skaerm >= 1:
                    if event.button == pygame.BUTTON_LEFT and self.right_button.is_over(event.pos):
                        self.nuvaerende_skaerm += 1
                        self.skaerm_stack.append(self.nuvaerende_skaerm - 1)
                        if self.nuvaerende_skaerm == 2:
                            self.skaerm.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                            self.key1_clicked = False

                        elif self.nuvaerende_skaerm == 3:
                            self.skaerm.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                            self.key2_clicked = False

                        elif self.nuvaerende_skaerm == 4:
                            self.skaerm.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                            self.key3_clicked = False

                            for button in self.buttons_clicked:
                                self.buttons_clicked[button] = False
                        elif self.nuvaerende_skaerm == 6:
                            self.right_button_active = False
                    elif event.button == pygame.BUTTON_LEFT and self.left_button.is_over(event.pos):
                        if self.nuvaerende_skaerm != 1:
                            self.nuvaerende_skaerm -= 1
                    elif event.button == pygame.BUTTON_LEFT and self.key1.is_clicked(event.pos):
                        self.key1_clicked = True
                        print("The first key has been clicked")

                    elif event.button == pygame.BUTTON_LEFT and self.key2.is_clicked(event.pos):
                        self.key2_clicked = True
                        print("The second key has been clicked")

                    elif event.button == pygame.BUTTON_LEFT and self.key3.is_clicked(event.pos):
                        self.key3_clicked = True
                        print("The third key has been clicked")

                    elif (event.button == pygame.BUTTON_LEFT and

                          self.nuvaerende_skaerm == 4 and
                          (self.screen_4_button.is_over(event.pos) or
                           self.screen_5_button.is_over(event.pos) or
                           self.screen_6_button.is_over(event.pos) or
                           self.screen_9_button.is_over(event.pos))):
                        for button in self.buttons_clicked:
                            if button.is_over(event.pos):
                                self.buttons_clicked[button] = True
                        if all(self.buttons_clicked.values()):
                            print("All buttons on screen 4 have been clicked")
                            self.right_button_active = True

                    elif self.nuvaerende_skaerm == 6:
                        button_map = {
                            "button_14_clicked": self.screen_14_button,
                            "button_15_clicked": self.screen_15_button,
                            "button_16_clicked": self.screen_16_button,
                            "button_17_clicked": self.screen_17_button,
                            "button_18_clicked": self.screen_18_button,
                            "button_19_clicked": self.screen_19_button,
                            "button_20_clicked": self.screen_20_button,
                            "button_21_clicked": self.screen_21_button,
                            "button_22_clicked": self.screen_22_button,
                            "button_23_clicked": self.screen_23_button
                        }

                        for button_name, screen_button in button_map.items():
                            if screen_button.is_over(event.pos):
                                setattr(self, button_name, True)

                        if self.button_14_clicked and self.button_15_clicked and not self.message_printed:
                            print("Bold og hold")
                            self.message_printed = True
                            self.point_6 += 1
                        if self.button_16_clicked and self.button_17_clicked and not self.message2_printed:
                            print("Hop og op")
                            self.message2_printed = True
                            self.point_6 += 1
                        if self.button_18_clicked and self.button_19_clicked and not self.message3_printed:
                            print("Skål og mål")
                            self.message3_printed = True
                            self.point_6 += 1
                        if self.button_20_clicked and self.button_21_clicked and not self.message4_printed:
                            print("Trommer og sommer")
                            self.message4_printed = True
                            self.point_6 += 1
                        if self.button_22_clicked and self.button_23_clicked and not self.message5_printed:
                            print("Kat og at")
                            self.message5_printed = True
                            self.point_6 += 1

                    elif self.nuvaerende_skaerm == 9:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.screen_29_button.is_over(event.pos):
                                self.button_29_clicked = True
                            if self.screen_30_button.is_over(event.pos):
                                self.button_30_clicked = True
                            if self.screen_31_button.is_over(event.pos):
                                self.button_31_clicked = True
                            if self.screen_32_button.is_over(event.pos):
                                self.button_32_clicked = True
                            if self.screen_33_button.is_over(event.pos):
                                self.button_33_clicked = True
                            if self.screen_34_button.is_over(event.pos):
                                self.button_34_clicked = True
                            if self.screen_35_button.is_over(event.pos):
                                self.button_35_clicked = True
                            if self.screen_36_button.is_over(event.pos):
                                self.button_36_clicked = True
                            if self.screen_37_button.is_over(event.pos):
                                self.button_37_clicked = True
                            if self.screen_38_button.is_over(event.pos):
                                self.button_38_clicked = True

                        if self.button_29_clicked and self.button_30_clicked and not self.message6_printed:
                            print("Fandt og blandt")
                            self.message6_printed = True
                            self.point_9 += 1
                        if self.button_31_clicked and self.button_32_clicked and not self.message7_printed:
                            print("Hund og stund")
                            self.message7_printed = True
                            self.point_9 += 1
                        if self.button_33_clicked and self.button_34_clicked and not self.message8_printed:
                            print("Stråle og åle")
                            self.message8_printed = True
                            self.point_9 += 1
                        if self.button_35_clicked and self.button_36_clicked and not self.message9_printed:
                            print("Ballade og marmelade")
                            self.message9_printed = True
                            self.point_9 += 1
                        if self.button_37_clicked and self.button_38_clicked and not self.message10_printed:
                            print("Hest og bedst")
                            self.message10_printed = True
                            self.point_9 += 1
            # Handle textbox inputs
            self.textbox.handle_event(event)
            self.textbox1.handle_event(event)
            self.textbox2.handle_event(event)
            self.textbox3.handle_event(event)

            if self.textbox2.get_text().lower() == "æble":
                print("Korrekt! Du indtastede 'Æble'. Yderligere input deaktiveret.")
                self.textbox2.visible = False
                self.textbox2.text = ""
                self.correct_count += 1
            if self.textbox.get_text().lower() == "banan":
                print("Korrekt! Du indtastede 'Banan'. Yderligere input deaktiveret.")
                self.textbox.visible = False
                self.textbox.text = ""
                self.correct_count += 1

            if self.textbox1.get_text().lower() == "mælk":
                print("Korrekt! Du indtastede 'Mælk'. Yderligere input deaktiveret.")
                self.textbox1.visible = False
                self.textbox1.text = ""
                self.correct_count += 1

            if self.textbox3.get_text().lower() == "æg":
                print("Korrekt! Du indtastede 'Æg'. Yderligere input deaktiveret.")
                self.textbox3.visible = False
                self.textbox3.text = ""
                self.correct_count += 1

            elif self.nuvaerende_skaerm == 9:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.screen_29_button.is_over(event.pos):
                        self.button_29_clicked = True
                    if self.screen_30_button.is_over(event.pos):
                        self.button_30_clicked = True
                    if self.screen_31_button.is_over(event.pos):
                        self.button_31_clicked = True
                    if self.screen_32_button.is_over(event.pos):
                        self.button_32_clicked = True
                    if self.screen_33_button.is_over(event.pos):
                        self.button_33_clicked = True
                    if self.screen_34_button.is_over(event.pos):
                        self.button_34_clicked = True
                    if self.screen_35_button.is_over(event.pos):
                        self.button_35_clicked = True
                    if self.screen_36_button.is_over(event.pos):
                        self.button_36_clicked = True
                    if self.screen_37_button.is_over(event.pos):
                        self.button_37_clicked = True
                    if self.screen_38_button.is_over(event.pos):
                        self.button_38_clicked = True






    def draw_screen(self):
        if self.nuvaerende_skaerm == 0:
            pygame.mixer_music.load("")
            background_img = pygame.image.load("Startskrm_eksamensprojekt.png")
            background_img = pygame.transform.scale(background_img, (self.skaerm_bredde, self.skaerm_hoejde))

            self.skaerm.blit(background_img, (0, 0))

            self.start_button.active = True
            self.start_button.draw()
        elif self.nuvaerende_skaerm >= 1 and self.nuvaerende_skaerm < 4:
            if self.nuvaerende_skaerm == 1:
                self.skaerm.fill((255, 255, 255))
                if not self.key1_clicked:
                    self.key1.draw_key()
            elif self.nuvaerende_skaerm == 2:
                self.skaerm.fill((255, 0, 0))
                if not self.key2_clicked:
                    self.key2.draw_key()
            elif self.nuvaerende_skaerm == 3:
                self.skaerm.fill((0, 255, 0))
                if not self.key3_clicked:
                    self.key3.draw_key()

            skaermtal_tekst = self.font.render(f"Skærm {self.nuvaerende_skaerm}", True, (0, 0, 0))
            self.skaerm.blit(skaermtal_tekst, (self.skaerm_bredde // 2 - skaermtal_tekst.get_width() // 2, 20))

            if self.nuvaerende_skaerm != 1:
                self.left_button.active = True
                self.left_button.color = (0, 0, 0)
                self.left_button.draw()

            if self.nuvaerende_skaerm == 1 and self.key1.clicked:
                self.right_button.active = True
                self.right_button.draw()
            elif self.nuvaerende_skaerm == 2 and self.key2.clicked:
                self.right_button.active = True
                self.right_button.draw()
            elif self.nuvaerende_skaerm == 3 and self.key3.clicked:
                self.right_button.active = True
                self.right_button.draw()
            else:
                self.right_button.active = False

        elif self.nuvaerende_skaerm == 4:
            self.skaerm.fill((0, 0, 255))
            self.left_button.active = True
            self.left_button.color = (0, 0, 0)
            self.left_button.draw()
            self.screen_4_button.draw()
            self.screen_5_button.draw()
            self.screen_6_button.draw()
            self.screen_9_button.draw()
            self.screen_10_button.draw()
            self.screen_11_button.draw()
            self.screen_12_button.draw()
            self.screen_13_button.draw()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.screen_10_button.is_over(event.pos):
                        print("Click Sten")
                    elif self.screen_11_button.is_over(event.pos):
                        print("Click Gren")
                    elif self.screen_12_button.is_over(event.pos):
                        print("Click Stol")
                    elif self.screen_13_button.is_over(event.pos):
                        print("Click Cement")
                    elif (self.nuvaerende_skaerm == 4 and
                          (self.screen_4_button.is_over(event.pos) or
                           self.screen_5_button.is_over(event.pos) or
                           self.screen_6_button.is_over(event.pos) or
                           self.screen_9_button.is_over(event.pos))):
                        for button in self.buttons_clicked:
                            if button.is_over(event.pos):
                                self.buttons_clicked[button] = True
                        if all(self.buttons_clicked.values()):
                            print("All buttons on screen 4 have been clicked")
                            self.right_button_active = True

            skaermtal_tekst = self.font.render(f"Skærm {self.nuvaerende_skaerm}", True, (0, 0, 0))
            self.skaerm.blit(skaermtal_tekst, (self.skaerm_bredde // 2 - skaermtal_tekst.get_width() // 2, 20))

            if self.right_button_active:
                self.right_button.active = True
                self.right_button.color = (0, 0, 0)
                self.right_button.draw()
            else:
                self.right_button.active = False
        elif self.nuvaerende_skaerm == 5:
            self.skaerm.fill((255, 255, 0))
            # Draw screen number
            skaermtal_tekst = self.font.render(f"Skærm {self.nuvaerende_skaerm}", True, (0, 0, 0))
            self.skaerm.blit(skaermtal_tekst, (self.skaerm_bredde // 2 - skaermtal_tekst.get_width() // 2, 20))
            # Draw the "Venstre" button on screen 5
            self.left_button.active = True
            self.left_button.color = (0, 0, 0)
            self.left_button.draw()
            # Draw the "Højre" button on screen 5
            self.right_button.active = True
            self.right_button.color = (0, 0, 0)
            self.right_button.draw()
        elif self.nuvaerende_skaerm == 6:
            self.skaerm.fill((255, 0, 255))
            self.screen_14_button.draw()
            self.screen_15_button.draw()
            self.screen_16_button.draw()
            self.screen_17_button.draw()
            self.screen_18_button.draw()
            self.screen_19_button.draw()
            self.screen_20_button.draw()
            self.screen_21_button.draw()
            self.screen_22_button.draw()
            self.screen_23_button.draw()
            self.screen_24_button.draw()
            self.screen_25_button.draw()
            self.screen_26_button.draw()
            self.screen_27_button.draw()
            self.screen_28_button.draw()

            skaermtal_tekst = self.font.render(f"Skærm {self.nuvaerende_skaerm}", True, (0, 0, 0))
            self.skaerm.blit(skaermtal_tekst, (self.skaerm_bredde // 2 - skaermtal_tekst.get_width() // 2, 20))

            self.left_button.active = True
            self.left_button.color = (0, 0, 0)
            self.left_button.draw()

            if self.point_6 == 5:
                self.right_button.active = True
                self.right_button.color = (0, 0, 0)
                self.right_button.draw()
            else:
                self.right_button.active = False


        elif self.nuvaerende_skaerm == 7:
            self.skaerm.fill((0, 255, 255))
            # Draw screen number
            skaermtal_tekst = self.font.render(f"Skærm {self.nuvaerende_skaerm}", True, (0, 0, 0))
            self.skaerm.blit(skaermtal_tekst, (self.skaerm_bredde // 2 - skaermtal_tekst.get_width() // 2, 20))
            # Draw the "Venstre" button on screen 7
            self.left_button.active = True
            self.left_button.color = (0, 0, 0)
            self.left_button.draw()
            # Draw the "Højre" button on screen 7
            self.right_button.active = True
            self.right_button.color = (0, 0, 0)
            self.right_button.draw()

        elif self.nuvaerende_skaerm == 8:
            self.skaerm.fill((0, 255, 255))
            self.textbox.draw(self.skaerm)
            self.textbox1.draw(self.skaerm)
            self.textbox2.draw(self.skaerm)
            self.textbox3.draw(self.skaerm)
            skaermtal_tekst = self.font.render(f"Skærm {self.nuvaerende_skaerm}", True, (0, 0, 0))
            self.skaerm.blit(skaermtal_tekst, (self.skaerm_bredde // 2 - skaermtal_tekst.get_width() // 2, 20))
            self.left_button.active = True
            self.left_button.color = (0, 0, 0)
            self.left_button.draw()

            if self.correct_count == 4:
                self.right_button.active = True
                self.right_button.color = (0, 0, 0)
                self.right_button.draw()
            else:
                self.right_button.active = False

        elif self.nuvaerende_skaerm == 9:
            self.skaerm.fill((0, 255, 79))
            self.screen_29_button.draw()
            self.screen_30_button.draw()
            self.screen_31_button.draw()
            self.screen_32_button.draw()
            self.screen_33_button.draw()
            self.screen_34_button.draw()
            self.screen_35_button.draw()
            self.screen_36_button.draw()
            self.screen_37_button.draw()
            self.screen_38_button.draw()
            self.screen_39_button.draw()
            self.screen_40_button.draw()
            self.screen_41_button.draw()
            self.screen_42_button.draw()
            self.screen_43_button.draw()

            skaermtal_tekst = self.font.render(f"Skærm {self.nuvaerende_skaerm}", True, (0, 0, 0))
            self.skaerm.blit(skaermtal_tekst, (self.skaerm_bredde // 2 - skaermtal_tekst.get_width() // 2, 20))


            self.left_button.active = True
            self.left_button.color = (0, 0, 0)
            self.left_button.draw()

            if self.point_9 == 5:
                self.right_button.active = True
                self.right_button.color = (0, 0, 0)
                self.right_button.draw()
            else:
                self.right_button.active = False

        if self.nuvaerende_skaerm == 10:
            self.skaerm.fill((0, 0, 0))

        pygame.display.flip()

    def run(self):
        while self.koerer:
            self.handle_events()
            self.draw_screen()
            pygame.display.flip()

if __name__ == "__main__":
    app = SkærmTæller()
    app.run()
    spil = SkærmTæller()