import pygame
import os


class Player(pygame.sprite.Sprite):
    """A player object."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.name = None
        self.mark = None

    def get_name(self):
        """
        Returns the object's name.
        Returns a string.
        """
        return self.name

    def get_mark(self):
        """Returns player's mark (X or O)."""
        return self.mark

    def set_mark(self, mark):
        """Sets the player's mark to X or O."""
        self.mark = mark


class Human(Player):
    """The human player."""
    def __init__(self):
        Player.__init__(self)

        self.image = load_image('human.png')
        self.rect = self.image.get_rect()

        self.name = "human"


class Computer(Player):
    """The computer."""
    def __init__(self):
        Player.__init__(self)

        self.image = load_image('computer.png')
        self.rect = self.image.get_rect()

        self.name = "computer"

    def move(self, game):
        """Computer calculates the best move and makes it."""
        move = self.find_best_move(game, not game.player_turn, -1, 1)
        loc = move.get_loc()
        piece = Mark(self.get_mark())

        game.update_message("Your turn!")
        game.place_piece(piece, loc)

    def calculate_score(self, game):
        """Returns 1, 0, or -1 depending on the state of the game board."""
        if game.get_winner() == game.computer.get_mark():
            return 1

        elif game.get_winner() == game.player.get_mark():
            return -1

        return 0

    def find_best_move(self, game, turn, alpha, beta):
        """Finds the best move using the minimax algorithm."""
        if (game.get_winner() is not None or
                len(game.grid_values.get_empty_cells()) == 0):
            return BestPlay(score=self.calculate_score(game))

        best_move = BestPlay()

        if turn:
            best_move.set_score(alpha)
            mark = game.computer.get_mark()

        else:
            best_move.set_score(beta)
            mark = game.player.get_mark()

        for loc in game.grid_values.get_empty_cells():
            game.grid_values.set_cell(loc, mark)
            best_response = self.find_best_move(game, not turn, alpha, beta)
            game.grid_values.set_cell(loc, None)

            m_score = best_move.get_score()
            r_score = best_response.get_score()

            if turn and r_score > m_score:
                best_move.set_loc(loc)
                best_move.set_score(r_score)
                alpha = r_score

            elif not turn and r_score < m_score:
                best_move.set_loc(loc)
                best_move.set_score(r_score)
                beta = r_score

            if alpha >= beta:
                return best_move

        return best_move


class Mark(pygame.sprite.Sprite):
    """A playing mark (X or O)."""
    def __init__(self, mark):
        pygame.sprite.Sprite.__init__(self)

        self.image = load_image(mark + '.png')
        self.rect = self.image.get_rect()

        self.mark = mark

    def get_mark(self):
        """Returns the value (X or O) of the mark."""
        return self.mark


class BestPlay(object):
    """Contains location and score of a best play."""
    def __init__(self, loc=None, score=None):
        self.loc = loc
        self.score = score

    def get_loc(self):
        """Return the location."""
        return self.loc

    def set_loc(self, (x, y)):
        """Set the loc to (x, y)."""
        self.loc = (x, y)

    def get_score(self):
        """Return the score."""
        return self.score

    def set_score(self, score):
        """Set the score to given score."""
        self.score = score


def load_image(filename):
    """
    filename: string
    Load the image located at 'data/filename'.
    Returns a pygame.Surface object.
    """
    location = os.path.join('data', filename)
    image = pygame.image.load(location)

    if __name__ != '__main__':
        return image

    if image.get_alpha is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    return image
