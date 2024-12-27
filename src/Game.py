from Field import Field

class Game(Field):
    """
    Represents a game field with specific attributes and methods for games.

    Inherits from:
        Field: The parent class providing shared functionality for games and practices.

    Attributes:
        _identifier (str): A unique string identifier for the game field.
    """
    def __init__(self, league: str, tier: str, div: str):
        super().__init__(league, tier, div)
        self._identifier = f"{league} {tier} DIV {div}"

    def get_identifier(self):
        """Returns the unique identifier for the game."""
        return self._identifier

    def print_info(self):
        """
        Prints all relevant information about the game, including:
        - Basic details like ID, identifier, league, tier, and division
        - Non-compatible fields
        - Unwanted time slots
        - Preferences
        - Pairing and partial assignment details
        """

        print("---GAME INFO---")
        print("ID: ", self._id)
        print("Identifier: ", self._identifier)
        print("League: ", self.league)
        print("Tier: ", self.tier)
        print("Div: ", self.div)

        print("Non-compatible fields:")
        self.print_not_compatible()

        print("Unwanted slots:")
        self.print_unwanted()

        print("Preferences:")
        self.print_preferences()

        if self._partial_assign is not None:
            print("Partial assign: ", self._partial_assign.get_all_info())
        print("---------------")
