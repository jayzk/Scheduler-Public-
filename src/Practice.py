from Field import Field

class Practice(Field):
    """
    Represents a practice field with specific attributes and methods for practices.

    Inherits from:
        Field: The parent class providing shared functionality for games and practices.

    Attributes:
        practice_type (str): The type of practice (PRC or OPN).
        practice_num (str): The number associated with the practice.
        _identifier (str): A unique identifier for the practice.
    """
    def __init__(self, league: str, tier: str, div: str, practice_type: str, practice_num: str):
        super().__init__(league, tier, div)
        self._identifier = set_identifier(league, tier, div, practice_type, practice_num)
        self.practice_type = practice_type
        self.practice_num = practice_num

    def print_info(self):
        """
        Prints all relevant information about the practice, including:
        - Basic details like ID, identifier, league, tier, division, type, and number
        - Non-compatible fields
        - Unwanted time slots
        - Preferences
        - Pairing and partial assignment details
        """
        print("---PRACTICE INFO---")
        print("ID: ", self._id)
        print("Identifier: ", self._identifier)
        print("League: ", self.league)
        print("Tier: ", self.tier)
        print("Div: ", self.div)
        print("Practice type: ", self.practice_type)
        print("Practice num: ", self.practice_num)

        print("Non-compatible fields:")
        self.print_not_compatible()

        print("Unwanted slots:")
        self.print_unwanted()

        print("Preferences:")
        self.print_preferences()

        if self._partial_assign is not None:
            print("Partial assign: ", self._partial_assign.get_all_info())
        print("-------------------")

    def get_identifier(self):
        """Returns the unique identifier for the practice."""
        return self._identifier

    def get_type(self):
        """Returns the type of practice."""
        return self.practice_type

    def get_practice_num(self):
        """Returns the practice number."""
        return self.practice_num

    def __eq__(self, other):
        return self._identifier == other.get_identifier()

# Helper functions
def set_identifier(league: str, tier: str, div: str, practice_type: str, practice_num: str):
    """
    Generates a unique identifier for practice based on its attributes.

    Args:
        league (str): The league to which the practice belongs.
        tier (str): The tier of the league.
        div (str): The division within the league.
        practice_type (str): The type of practice.
        practice_num (str): The practice number.

    Returns:
        str: A formatted unique identifier for the practice.
    """
    if div == "0":
        identifier = f"{league} {tier} {practice_type} {practice_num}"
    else:
        identifier = f"{league} {tier} DIV {div} {practice_type} {practice_num}"
    return identifier

