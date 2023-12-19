import dataclasses
import sys

from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def get(self, field: str):
        return getattr(self, field)

    @property
    def rating_sum(self):
        return self.x + self.m + self.a + self.s

@dataclass
class Rule:
    action: str
    target: str = None
    operation: str = None
    threshold: int = None

    @property
    def is_default(self):
        return self.target is None and self.operation is None and self.threshold is None

@dataclass
class Workflow:
    name: str
    rules: List[Rule]

def can_apply_rule(part, rule):
    """
    Check if this part passes or fails the rule.
    If the part passes, the rule can be applied.
    """
    # always apply the rule if it is the last option
    if rule.is_default:
        return True
    rating = part.get(rule.target)
    if rule.operation == ">":
        return rating > rule.threshold
    elif rule.operation == "<":
        return rating < rule.threshold

def can_accept_part(part, workflows):
    """
    Check if a part will be accepted. Start with the "in"
    workflow and attempt to apply the rules of the workflow
    sequentially. As soon as the part passes a rule, perform
    the action specified by the workflow. This either causes
    immediate acceptance or rejection or moves the part to a
    new workflow. In the last case, the while loop starts
    again with the new workflow.

    If the rule cannot be applied, then attempt to apply the
    next rule in the sequence until the last rule is reached.
    The last rule can always be applied.
    """
    workflow = workflows["in"]
    while True:
        for rule in workflow.rules:
            if can_apply_rule(part, rule):
                if rule.action == "A":
                    # immediately accept part
                    return True
                elif rule.action == "R":
                    # immediately reject part
                    return False
                else:
                    # move part to new workflow
                    workflow = workflows[rule.action]
                    break

@dataclass
class RatingIntervals:
    x: Tuple[int, int] = (1, 4000)
    m: Tuple[int, int] = (1, 4000)
    a: Tuple[int, int] = (1, 4000)
    s: Tuple[int, int] = (1, 4000)

    def update(self, target, interval):
        updated = dataclasses.replace(self)
        setattr(updated, target, interval)
        return updated

    def get(self, field: str):
        return getattr(self, field)

    @property
    def num_combinations(self):
        combinations  = (self.x[1] - self.x[0] + 1)
        combinations *= (self.m[1] - self.m[0] + 1)
        combinations *= (self.a[1] - self.a[0] + 1)
        combinations *= (self.s[1] - self.s[0] + 1)
        return combinations

def count_valid_combinations(name, workflows, intervals):
    """
    Count valid ratings combinations recursively using depth-first
    search on intervals of valid combinations.

    For the current workflow, attempt to apply each rule.
    Each non-default rule splits one interval into left and right
    halves. The half that passes the rule can be accepted, rejected
    or moved to another workflow.

    If the part passes a rule, whichever interval makes the rule
    pass is passed to the next recursive call. One interval splits due
    to each rule a base case is reached. The set of intervals is then
    accepted (in which case the product of the interval lengths is the
    number of valid combinations that pass this set of conditions) or
    the set of intervals is rejected and we stop caring.

    When a rule is not passed, update the intervals with the half 
    that did not pass the rule before moving on to the next rule
    in the sequence.

    Since one interval is split per rule applied (except for the default
    rules), each path taken by the depth-first search is disjoint.
    Summing up the number of combinations for each valid path therefore
    yields the total number of valid combinations.
    """
    workflow = workflows[name]
    valid_combinations = 0
    for rule in workflow.rules[:-1]:
        interval = intervals.get(rule.target)
        if rule.operation == "<":
            # case: rule applied
            left = (interval[0], rule.threshold-1)
            new_intervals = intervals.update(rule.target, left)
            if rule.action == "A": # accept, so count these combinations
                valid_combinations += new_intervals.num_combinations
            elif rule.action != "R": # not rejected, so go to next workflow
                valid_combinations += count_valid_combinations(rule.action, workflows, new_intervals)
            # if rejected, then we just stop working on this path
            # i.e., just ignore it and move on
            # case: rule not applied. continue on to next rule
            # with shrunken interval
            right = (rule.threshold, interval[1])
            intervals = intervals.update(rule.target, right)
        elif rule.operation == ">":
            # case: rule applied
            right = (rule.threshold+1, interval[1])
            new_intervals = intervals.update(rule.target, right)
            if rule.action == "A":
                valid_combinations += new_intervals.num_combinations
            elif rule.action != "R":
                valid_combinations += count_valid_combinations(rule.action, workflows, new_intervals)
            # case: rule not applied. continue on to next rule
            # with shrunken interval
            left = (interval[0], rule.threshold)
            intervals = intervals.update(rule.target, left)
    # handle the default case separately since there is
    # no branching due to the operation
    default_rule = workflow.rules[-1]
    if default_rule.action == "A":
        valid_combinations += intervals.num_combinations
    elif default_rule.action != "R":
        valid_combinations += count_valid_combinations(default_rule.action, workflows, intervals)
    return valid_combinations

def parse_parts(part_text: str) -> List[Part]:
    part_lines = part_text.splitlines()
    parts = []
    for line in part_lines:
        # remove braces and split
        line = line[1:-1].split(",")
        ratings = []
        for rating in line:
            ratings.append(int(rating[2:]))
        part = Part(*ratings)
        parts.append(part)
    return parts

def parse_workflows(workflow_text: str) -> List[Workflow]:
    workflow_lines = workflow_text.splitlines()
    workflows = {}
    for line in workflow_lines:
        name, remainder = line.split("{")
        remainder = remainder[:-1] # remove end bracket
        instructions = remainder.split(",")
        # handle the last rule, which is a default
        # that only gives an action
        default_rule = Rule(action=instructions.pop())

        rules = []
        for instruction in instructions:
            comparison_text, action = instruction.split(":")
            target = comparison_text[0]
            operation = comparison_text[1]
            threshold = int(comparison_text[2:])
            rule = Rule(action, target, operation, threshold)
            rules.append(rule)
        rules.append(default_rule)
        workflows[name] = Workflow(name, rules)
    return workflows

def read_input(input: str):
    with open(input, "r") as f:
        workflow_text, part_text = f.read().strip().split("\n\n")
    parts = parse_parts(part_text)
    workflows = parse_workflows(workflow_text)
    return parts, workflows

if __name__ == "__main__":
    parts, workflows = read_input(sys.argv[1])
    rating_sum = 0
    for part in parts:
        accepted = can_accept_part(part, workflows)
        if accepted:
            rating_sum += part.rating_sum
    print(rating_sum)

    intervals = RatingIntervals()
    valid_combinations = count_valid_combinations("in", workflows, intervals)
    print(valid_combinations)   