import pygame
import game
import board
import os

class Menu:
    def __init__(self, screen):

        self.menu_nr = 1
        self.screen = screen
        self.gamemode = 0
        self.difficulty_selected = 0

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 80, 80)
        self.GREEN = (111, 192, 99)
        self.BLUE = (90, 202, 235)
        self.USER_BLUE = (111,205,244)
        self.USER_RED = (242, 107, 102)

        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768

        self.LOGO = pygame.image.load(os.path.join('assets', 'LESS_logo.png'))
        self.LOGO = pygame.transform.scale(self.LOGO, (int(self.LOGO.get_width()/5), int(self.LOGO.get_height()/5)))

        self.back_arrow = pygame.image.load(os.path.join('assets', 'back_arrow.png'))

        self.font = pygame.font.SysFont('arialBlack', 30)
        self.winner_font = pygame.font.SysFont('arialBlack', 80)

        self.draw_menu()

        self.board = board.Board(self.screen)
        

    def create_rect(self, text, x, y, color):
        rect = text.get_rect()
        rect.width += 10
        rect.height += 10
        rect.center = (x, y)

        pygame.draw.rect(self.screen, color, rect, 2, 10)
        return rect
    

    def draw_menu(self):
        if self.menu_nr == 1:
            self.screen.fill(self.WHITE)

            play_buttonPvP = self.font.render('Player vs Player', True, self.RED)
            play_buttonPvAI = self.font.render('Player vs AI', True, self.RED)
            play_buttonAIvAI = self.font.render('AI vs AI', True, self.RED)

            self.button1_rect = self.create_rect(play_buttonPvP, self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/3+50, self.RED)
            self.button2_rect = self.create_rect(play_buttonPvAI, self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/3 + 150, self.RED)
            self.button3_rect = self.create_rect(play_buttonAIvAI, self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/3 + 250, self.RED)
            
            self.screen.blit(play_buttonPvP, (self.button1_rect.x + 5, self.button1_rect.y + 5))
            self.screen.blit(play_buttonPvAI, (self.button2_rect.x + 5, self.button2_rect.y + 5))
            self.screen.blit(play_buttonAIvAI, (self.button3_rect.x + 5, self.button3_rect.y + 5))

            logo_rect = self.LOGO.get_rect()
            logo_rect.center = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2 - 200)

            self.screen.blit(self.LOGO, logo_rect)

            pygame.display.update()

        elif self.menu_nr == 2:
            self.screen.fill(self.WHITE)

            back_arrow_rect = self.back_arrow.get_rect()
            back_arrow_rect.center = (30, 40)

            self.screen.blit(self.back_arrow, back_arrow_rect)

            #Choose difficulty text
            difficulty_text = self.font.render('Choose difficulty', True, self.BLACK)
            difficulty_text_rect = difficulty_text.get_rect()
            difficulty_text_rect.center = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/3-100)
            self.screen.blit(difficulty_text, difficulty_text_rect)

            #Select difficulty
            easy_button = self.font.render('Easy', True, self.GREEN)
            medium_button = self.font.render('Medium', True, self.BLUE)
            hard_button = self.font.render('Hard', True, self.RED)

            self.button1_rect = self.create_rect(easy_button, self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/3+50, self.GREEN)
            self.button2_rect = self.create_rect(medium_button, self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/3 + 150, self.BLUE)
            self.button3_rect = self.create_rect(hard_button, self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/3 + 250, self.RED)

            self.screen.blit(easy_button, (self.button1_rect.x + 5, self.button1_rect.y + 5))
            self.screen.blit(medium_button, (self.button2_rect.x + 5, self.button2_rect.y + 5))
            self.screen.blit(hard_button, (self.button3_rect.x + 5, self.button3_rect.y + 5))

            pygame.display.update()
    
    def update_menu(self, event):
        if event == None:
            return None
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if event.button == 1:
            if self.menu_nr == 1:
                if self.button1_rect.collidepoint(event.pos):
                    return self.start_pvp()

                elif self.button2_rect.collidepoint(event.pos):
                    self.menu_nr = 2
                    self.draw_menu()

                elif self.button3_rect.collidepoint(event.pos):
                    return self.start_ai_vs_ai()

            elif self.menu_nr == 2:
                if self.back_arrow.get_rect().collidepoint(event.pos):
                    self.menu_nr = 1
                    self.draw_menu()
                elif self.button1_rect.collidepoint(event.pos):
                    self.difficulty_selected = 1
                    return self.start_player_vs_ai()
                elif self.button2_rect.collidepoint(event.pos):
                    self.difficulty_selected = 2
                    return self.start_player_vs_ai()
                elif self.button3_rect.collidepoint(event.pos):
                    self.difficulty_selected = 3
                    return self.start_player_vs_ai()
        return None
    def check_match_ended(self):
        if self.game.state.game_over != 0:
            self.menu_nr = 1
            self.gamemode = 0
            self.draw_winner(self.game.state.game_over)
            self.board = board.Board(self.screen)
            self.draw_menu()
            return False
        return True

    def check_match_end(self, event):
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.back_arrow.get_rect().collidepoint(event.pos)
        ):
            self.menu_nr = 1
            self.gamemode = 0
            self.board = board.Board(self.screen)
            self.draw_menu()

        if self.game.state.game_over != 0:
            self.menu_nr = 1
            self.gamemode = 0
            self.draw_winner(self.game.state.game_over)
            self.board = board.Board(self.screen)
            self.draw_menu()
            return False
        return True

    def draw_winner(self, winner):
        if winner == 1:
            winner_text = self.font.render('Player 1 wins!', True, self.USER_RED)
        elif winner == 2:
            winner_text = self.font.render('Player 2 wins!', True, self.USER_BLUE)

        winner_text_rect = winner_text.get_rect()
        winner_text_rect.center = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)

        self.screen.blit(winner_text, winner_text_rect)

        pygame.display.update()

        pygame.time.wait(3000)
    

    def start_pvp(self):
        return self.initialize_game_with_mode(1, 2)
    
    def start_player_vs_ai(self):
        return self.initialize_game_with_mode(2, 1)
    
    def start_ai_vs_ai(self):
        return self.initialize_game_with_mode(3, 0)

    def initialize_game_with_mode(self, gamemode, num_of_players):
        self.menu_nr = 0
        self.gamemode = gamemode
        self.game = game.Game(num_of_players, self.board)
        return self.game
    