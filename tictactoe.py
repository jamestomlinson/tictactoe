import pygame
import ui
import game_objects


class Game(object):
    """Main game object."""
    def __init__(self):
        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.grey = (125, 125, 125)

        # Screen
        self.screen_width = 300
        self.screen_height = 400
        self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height)
                )
        self.screen_pos = (0, 0)

        # Title
        pygame.display.set_caption("Tic Tac Toe")

        # Framerate object
        self.clock = pygame.time.Clock()

        # Background
        self.background = pygame.Surface(self.screen.get_size())
        self.background.convert()

        # Playing grid
        self.grid = ui.Grid(3, 3, cell_width=100, cell_height=100,
                color=self.grey, border=2)

        self.grid_values = ui.Grid(3, 3)

        # User response buttons
        self.buttons = ui.Grid(2, 1, x=25, y=350,
                cell_width=100, cell_height=25,
                x_spacing=50,
                color=self.grey, border=2)

        self.player = game_objects.Human()
        self.buttons.add_sprite(self.player, (0, 0))

        self.computer = game_objects.Computer()
        self.buttons.add_sprite(self.computer, (1, 0))

        # Playing pieces
        self.X = "X"
        self.O = "O"

        # Initial game conditions
        self.player_turn = False
        self.game_over = True
        self.winner = None

        self.game_message = ui.Status(None, 25, self.white, (150, 325))
        self.game_message.set_text("Welcome. Who goes first?")

        self.draw_screen()

    def draw_screen(self):
        """Draws the entire initial game screen."""
        self.background.fill(self.black)

        self.grid.draw(self.background)
        self.buttons.draw(self.background)
        self.game_message.draw(self.background)

        self.screen.blit(self.background, self.screen_pos)
        pygame.display.update()

    def process_click(self, pos):
        """Process a click on the screen."""
        if self.game_over:
            loc = self.buttons.get_loc(pos)

            if loc is not None:
                self.button_click(loc)

        elif self.player_turn:
            loc = self.grid.get_loc(pos)

            if loc is not None:
                self.grid_click(loc)

    def button_click(self, loc):
        """Process a click on one of the buttons."""
        player = self.buttons.get_cell(loc)

        if player.get_name() == "human":
            self.switch_turn()
            self.player.set_mark(self.X)
            self.computer.set_mark(self.O)

        else:
            self.computer.set_mark(self.X)
            self.player.set_mark(self.O)

        self.start_game()

    def grid_click(self, loc):
        """Process a click on the playing field."""
        if self.grid.get_cell(loc) is None:
            mark = self.player.get_mark()

            self.place_piece(game_objects.Mark(mark), loc)

    def place_piece(self, piece, loc):
        """Places an X or O on the grid."""
        rects = []

        self.grid.add_sprite(piece, loc)
        self.grid_values.set_cell(loc, piece.get_mark())

        rects.append(piece.rect)

        self.grid.draw(self.background)

        self.screen.blit(self.background, self.screen_pos)
        pygame.display.update(rects)

        self.switch_turn()

        self.winner = self.get_winner()

        if self.winner is not None:
            self.end_game()

    def update_message(self, text):
        """Updates the game message with given text."""
        self.game_message.set_text(text)

        old_pos = self.game_message.get_old_pos()
        pos = self.game_message.get_pos()

        rects = []
        rects.append(old_pos)

        filler = pygame.Surface((self.screen_width, self.screen_height))
        filler.fill(self.black)

        self.background.blit(filler, old_pos, old_pos)

        rects.append(pos)

        self.game_message.draw(self.background)
        self.screen.blit(self.background, self.screen_pos)

        pygame.display.update(rects)

    def start_game(self):
        """Starts the game."""
        self.game_over = False

        self.grid.clear()
        self.grid_values.clear()

        self.draw_screen()

        self.update_message("Game on!")

    def get_winner(self):
        """Returns the winner (X or O) or None if there isn't one."""
        win_states = (((0, 0), (1, 0), (2, 0)),     # Top row
                      ((0, 1), (1, 1), (2, 1)),     # Middle row
                      ((0, 2), (1, 2), (2, 2)),     # Bottom row
                      ((0, 0), (0, 1), (0, 2)),     # Left column
                      ((1, 0), (1, 1), (1, 2)),     # Middle column
                      ((2, 0), (2, 1), (2, 2)),     # Right column
                      ((0, 0), (1, 1), (2, 2)),     # Negative diagonal
                      ((2, 0), (1, 1), (0, 2)))     # Positive diagonal

        for loc in win_states:
            a = self.grid_values.get_cell(loc[0])
            b = self.grid_values.get_cell(loc[1])
            c = self.grid_values.get_cell(loc[2])

            if a == b == c is not None:
                return a

        return None

    def end_game(self):
        """Ends the game."""
        self.player_turn = False
        self.game_over = True

        if self.winner == self.player.get_mark():
            self.update_message("This should not happen. Oops!")

        elif self.winner == self.computer.get_mark():
            self.update_message("You lose. Play again?")

        else:
            self.update_message("Game tied! Play again?")

    def switch_turn(self):
        """Switches whose turn it is."""
        self.player_turn = not self.player_turn

    def main(self):
        """Main game loop."""
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.process_click(pos)

            if len(self.grid.items) == 9:
                self.end_game()

            # Computer's turn
            if not self.game_over and not self.player_turn:
                self.update_message("Thinking...")
                self.computer.move(self)

            self.clock.tick(20)


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.main()
    pygame.quit()
