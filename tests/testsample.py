import unittest
from themstates import StateMachine

class SampleTests(unittest.TestCase):
    def test_example(self):
        sm = StateMachine()

        sm.define("neutral -> gearup -> first")
        sm.define("first -> gearup -> second")
        sm.define("first -> geardown -> neutral")
        sm.define("second -> geardown -> first")

        def some_action_function(event, payload):
            print(event, payload)

        sm.add_action("first", some_action_function)
        sm.start("neutral")

        self.assertTrue(sm.get_last_state() == None)

        sm.handle("gearup", "changed gear")
        self.assertTrue(sm.get_last_state() == "neutral")
        self.assertTrue(sm.get_current_state() == "first")
        sm.handle("GEARUP", "changed gear")
        self.assertTrue(sm.get_current_state() == "second")
        sm.handle("geardown", "changed gear")
        self.assertTrue(sm.get_current_state() == "first")
        sm.reset()
        self.assertTrue(sm.get_current_state() == "neutral")
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
