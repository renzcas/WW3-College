# src/models/trigger.py

class TriggerEvaluator:
    @staticmethod
    def evaluate(rule: dict, node_state: dict) -> bool:
        """
        Recursively evaluates compound trigger rules (AND, OR, NOT, or single condition).
        """
        if "state" in rule:
            return TriggerEvaluator._evaluate_condition(rule, node_state)

        op = rule.get("operator")
        if op == "AND":
            return all(TriggerEvaluator.evaluate(c, node_state) for c in rule.get("conditions", []))
        elif op == "OR":
            return any(TriggerEvaluator.evaluate(c, node_state) for c in rule.get("conditions", []))
        elif op == "NOT":
            return not TriggerEvaluator.evaluate(rule.get("condition", {}), node_state)
        
        return False

    @staticmethod
    def _evaluate_condition(condition: dict, node_state: dict) -> bool:
        stat = condition.get("state")
        op = condition.get("operator")
        target_value = condition.get("value")

        current_value = node_state.get(stat, 0.0)

        if op == "<":
            return current_value < target_value
        elif op == "<=":
            return current_value <= target_value
        elif op == ">":
            return current_value > target_value
        elif op == ">=":
            return current_value >= target_value
        elif op == "==":
            return current_value == target_value
        elif op == "!=":
            return current_value != target_value
        
        return False