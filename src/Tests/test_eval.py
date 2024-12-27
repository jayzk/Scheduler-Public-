import unittest
from datetime import datetime

# NOTE: MAKE SURE TO IMPORT THIS
import sys
sys.path.append('../../src')

from Parser import Parser
from State import State
from Datatypes.SlotType import SlotType
from Datatypes.Day import Day
from Schedule import Schedule
import eval

# NOTE: THIS UNIT TEST IS OUT OF DATE
class TestEval(unittest.TestCase):

    def tearDown(self):
        State.clear()

    def test1_minfilled(self):
        # set up for test case 1
        Parser.parse_file("../../Examples/SoftMinTest1.txt")
        State.pen_gamemin = 2
        State.pen_practicemin = 3

        # get game and practice slot to assign
        time = datetime.strptime("8:00", '%H:%M').time()
        game_slot = State.lookup_simple_slots(SlotType.GAME, Day.MONDAY, time)
        practice_slot = State.lookup_simple_slots(SlotType.PRACTICE, Day.MONDAY, time)

        # create new schedule for testing
        schedule = Schedule(State.games, State.practices)

        # add assignment
        schedule.add_assign("CMSA U13T3 DIV 01", game_slot)
        schedule.add_assign("CMSA U13T3 DIV 01 PRC 01", practice_slot)

        # Get penalties
        game_pen = eval.eval_minfilled("CMSA U13T3 DIV 01", schedule)
        practice_pen = eval.eval_minfilled("CMSA U13T3 DIV 01 PRC 01", schedule)

        # Test
        self.assertEqual(2, game_pen)
        self.assertEqual(6, practice_pen)

    def test2_minfilled(self):
        # set up for test case 2
        Parser.parse_file("../../Examples/SoftMinTest2.txt")
        State.pen_gamemin = 2
        State.pen_practicemin = 3

        # get game and practice slot to assign
        time = datetime.strptime("8:00", '%H:%M').time()
        game_slot = State.lookup_simple_slots(SlotType.GAME, Day.MONDAY, time)
        practice_slot = State.lookup_simple_slots(SlotType.PRACTICE, Day.MONDAY, time)

        # create new schedule for testing
        schedule = Schedule(State.games, State.practices)

        # add assignment
        schedule.add_assign("CMSA U13T3 DIV 01", game_slot)
        schedule.add_assign("CMSA U13T3 DIV 01 PRC 01", practice_slot)

        # Get penalties
        game_pen = eval.eval_minfilled("CMSA U13T3 DIV 01", schedule)
        practice_pen = eval.eval_minfilled("CMSA U13T3 DIV 01 PRC 01", schedule)

        # Test
        self.assertEqual(8, game_pen)
        self.assertEqual(9, practice_pen)

    def test3_minfilled(self):
        # set up for test case 3
        Parser.parse_file("../../Examples/SoftMinTest3.txt")
        State.pen_gamemin = 2
        State.pen_practicemin = 3

        # get game and practice slot to assign
        time = datetime.strptime("8:00", '%H:%M').time()
        game_slot = State.lookup_simple_slots(SlotType.GAME, Day.MONDAY, time)
        practice_slot = State.lookup_simple_slots(SlotType.PRACTICE, Day.MONDAY, time)

        # create new schedule for testing
        schedule = Schedule(State.games, State.practices)

        # add assignment
        schedule.add_assign("CMSA U13T3 DIV 01", game_slot)
        schedule.add_assign("CMSA U13T3 DIV 02", game_slot)
        schedule.add_assign("CMSA U13T3 DIV 01 PRC 01", practice_slot)
        schedule.add_assign("CMSA U13T3 DIV 01 OPN 02", practice_slot)

        # Get penalties
        game1_pen = eval.eval_minfilled("CMSA U13T3 DIV 01", schedule)
        game2_pen = eval.eval_minfilled("CMSA U13T3 DIV 02", schedule)
        practice1_pen = eval.eval_minfilled("CMSA U13T3 DIV 01 PRC 01", schedule)
        practice2_pen = eval.eval_minfilled("CMSA U13T3 DIV 01 OPN 02", schedule)

        # Test
        self.assertEqual(0, game1_pen)
        self.assertEqual(0, game2_pen)
        self.assertEqual(0, practice1_pen)
        self.assertEqual(0, practice2_pen)

    def test1_pref(self):
        # set up for test case 1
        Parser.parse_file("../../Examples/SoftPrefTest1.txt")

        # get game and practice slot to assign
        time = datetime.strptime("9:30", '%H:%M').time()
        game_slot = State.lookup_simple_slots(SlotType.GAME, Day.TUESDAY, time)

        time = datetime.strptime("8:00", '%H:%M').time()
        practice_slot = State.lookup_simple_slots(SlotType.PRACTICE, Day.MONDAY, time)

        # create new schedule for testing
        schedule = Schedule(State.games, State.practices)

        # add assignment
        schedule.add_assign("CMSA U13T3 DIV 01", game_slot)
        schedule.add_assign("CMSA U13T3 DIV 01 PRC 01", practice_slot)

        # Get penalties
        game_pen = eval.eval_pref("CMSA U13T3 DIV 01", schedule)
        practice_pen = eval.eval_pref("CMSA U13T3 DIV 01 PRC 01", schedule)

        # Test
        self.assertEqual(0, game_pen)
        self.assertEqual(0, practice_pen)

    def test2_pref(self):
        # set up for test case 2
        Parser.parse_file("../../Examples/SoftPrefTest2.txt")

        # get game and practice slot to assign
        time = datetime.strptime("8:00", '%H:%M').time()
        game_slot = State.lookup_simple_slots(SlotType.GAME, Day.MONDAY, time)
        practice_slot = State.lookup_simple_slots(SlotType.PRACTICE, Day.TUESDAY, time)

        # create new schedule for testing
        schedule = Schedule(State.games, State.practices)

        # add assignment
        schedule.add_assign("CMSA U13T3 DIV 01", game_slot)
        schedule.add_assign("CMSA U13T3 DIV 01 PRC 01", practice_slot)

        # Get penalties
        game_pen = eval.eval_pref("CMSA U13T3 DIV 01", schedule)
        practice_pen = eval.eval_pref("CMSA U13T3 DIV 01 PRC 01", schedule)

        # Test
        self.assertEqual(13, game_pen)
        self.assertEqual(3, practice_pen)

    def test1_pair(self):
        # set up for test case 2
        Parser.parse_file("../../Examples/SoftPairTest1.txt")
        State.pen_notpaired = 3

        # get game and practice slot to assign
        time = datetime.strptime("8:00", '%H:%M').time()
        game_slot = State.lookup_simple_slots(SlotType.GAME, Day.MONDAY, time)
        practice_slot = State.lookup_simple_slots(SlotType.PRACTICE, Day.MONDAY, time)

        # create new schedule for testing
        schedule = Schedule(State.games, State.practices)

        # add assignment
        schedule.add_assign("CMSA U13T3 DIV 01", game_slot)
        schedule.add_assign("CUSA 018 DIV 01", game_slot)
        schedule.add_assign("CMSA U13T3 DIV 01 PRC 01", practice_slot)
        schedule.add_assign("CUSA 018 DIV 01 PRC 01", practice_slot)

        # Get penalties
        game1_pen = eval.eval_pair("CMSA U13T3 DIV 01", schedule)
        game2_pen = eval.eval_pair("CUSA 018 DIV 01", schedule)
        practice1_pen = eval.eval_pair("CMSA U13T3 DIV 01 PRC 01", schedule)
        practice2_pen = eval.eval_pair("CUSA 018 DIV 01 PRC 01", schedule)

        # Test
        self.assertEqual(0, game1_pen)
        self.assertEqual(0, game2_pen)
        self.assertEqual(0, practice1_pen)
        self.assertEqual(0, practice2_pen)

    def test2_pair(self):
        # set up for test case 2
        Parser.parse_file("../../Examples/SoftPairTest2.txt")
        State.pen_notpaired = 3

        # get game and practice slot to assign
        time = datetime.strptime("8:00", '%H:%M').time()
        game_slot = State.lookup_simple_slots(SlotType.GAME, Day.MONDAY, time)
        practice_slot = State.lookup_simple_slots(SlotType.PRACTICE, Day.MONDAY, time)

        # create new schedule for testing
        schedule = Schedule(State.games, State.practices)

        # add assignment
        schedule.add_assign("CMSA U13T3 DIV 01", game_slot)
        schedule.add_assign("CMSA U13T3 DIV 01 PRC 01", practice_slot)

        # Get penalties
        game_pen = eval.eval_pair("CMSA U13T3 DIV 01", schedule)
        practice_pen = eval.eval_pair("CMSA U13T3 DIV 01 PRC 01", schedule)

        # Test
        self.assertEqual(0, game_pen)
        self.assertEqual(0, practice_pen)

    def test3_pair(self):
        # set up for test case 3
        Parser.parse_file("../../Examples/SoftPairTest3.txt")
        State.pen_notpaired = 3

        # get game and practice slot to assign
        time = datetime.strptime("9:30", '%H:%M').time()
        game_slot = State.lookup_simple_slots(SlotType.GAME, Day.TUESDAY, time)

        time = datetime.strptime("8:00", '%H:%M').time()
        practice_slot = State.lookup_simple_slots(SlotType.PRACTICE, Day.MONDAY, time)

        # create new schedule for testing
        schedule = Schedule(State.games, State.practices)

        # add assignment
        schedule.add_assign("CMSA U13T3 DIV 01", game_slot)
        schedule.add_assign("CMSA U13T3 DIV 01 PRC 01", practice_slot)

        # Get penalties
        game_pen = eval.eval_pair("CMSA U13T3 DIV 01", schedule)
        practice_pen = eval.eval_pair("CMSA U13T3 DIV 01 PRC 01", schedule)

        # Test
        self.assertEqual(6, game_pen)
        self.assertEqual(3, practice_pen)

    def test4_pair(self):
        # set up for test case 4
        Parser.parse_file("../../Examples/SoftPairTest4.txt")
        State.pen_notpaired = 3

        # get game and practice slot to assign
        time = datetime.strptime("9:30", '%H:%M').time()
        game_slot = State.lookup_simple_slots(SlotType.GAME, Day.TUESDAY, time)
        practice_slot = State.lookup_simple_slots(SlotType.PRACTICE, Day.TUESDAY, time)

        # create new schedule for testing
        schedule = Schedule(State.games, State.practices)

        # add assignment
        schedule.add_assign("CMSA U13T3 DIV 01", game_slot)
        schedule.add_assign("CMSA U13T3 DIV 01 PRC 01", practice_slot)

        # Get penalties
        game_pen = eval.eval_pair("CMSA U13T3 DIV 01", schedule)
        practice_pen = eval.eval_pair("CMSA U13T3 DIV 01 PRC 01", schedule)

        # Test
        self.assertEqual(3, game_pen)
        self.assertEqual(0, practice_pen)

if __name__ == '__main__':
    unittest.main()
