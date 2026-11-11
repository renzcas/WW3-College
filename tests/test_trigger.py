# tests/test_trigger.py
import unittest
from models.trigger import TriggerEvaluator

class TestTriggerEvaluator(unittest.TestCase):
    def test_single_condition(self):
        state = {"food": 5.0, "stability": 25.0}
        rule = {"state": "food", "operator": "<", "value": 10}
        self.assertTrue(TriggerEvaluator.evaluate(rule, state))

    def test_and_condition(self):
        state = {"food": 5.0, "stability": 25.0}
        rule = {
            "operator": "AND",
            "conditions": [
                {"state": "food", "operator": "<", "value": 10},
                {"state": "stability", "operator": "<", "value": 30}
            ]
        }
        self.assertTrue(TriggerEvaluator.evaluate(rule, state))

    def test_or_condition(self):
        state = {"food": 15.0, "stability": 25.0}
        rule = {
            "operator": "OR",
            "conditions": [
                {"state": "food", "operator": "<", "value": 10},
                {"state": "stability", "operator": "<", "value": 30}
            ]
        }
        self.assertTrue(TriggerEvaluator.evaluate(rule, state))

    def test_not_condition(self):
        state = {"trust": 60.0}
        rule = {
            "operator": "NOT",
            "condition": {"state": "trust", "operator": ">", "value": 50}
        }
        self.assertFalse(TriggerEvaluator.evaluate(rule, state))

if __name__ == "__main__":
    unittest.main()