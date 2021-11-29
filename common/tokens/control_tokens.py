from typing import Union

from common.tokens.abstract_tokens import *
from common.prorgam import Program


class If(ControlToken):
    """If statement ControlToken."""

    def __init__(self, cond: BoolToken, e1: List[EnvToken], e2: List[EnvToken]):
        """Creates a new If ControlToken. When applied, 'cond' is executed. If that yields true, 'e1' is execute, otherwise 'e2'."""
        self.cond = cond
        self.e1 = e1
        self.e2 = e2

    def apply(self, env: Environment) -> Environment:
        if self.cond.apply(env):
            for token in self.e1:
                env = token.apply(env)
            return env
        for token in self.e2:
            env = token.apply(env)
        return env
        #Program(self.e2).interp(env, False)

    def number_of_tokens(self, control_cost=2) -> int:
        return control_cost + \
               sum([t.number_of_tokens(control_cost) for t in self.e1]) + \
               sum([t.number_of_tokens(control_cost) for t in self.e2])

    def __str__(self):
        return "If(%s [%s] [%s])" % (self.cond, ", ".join(list(map(str, self.e1))), ", ".join(list(map(str, self.e2))))

    def __repr__(self):
        return "If(%s [%s] [%s])" % (self.cond, ", ".join(list(map(str, self.e1))), ", ".join(list(map(str, self.e2))))

    def to_formatted_string(self):
        result = "if %s:\n\t%s" % (
            self.cond.to_formatted_string(),
            "\n\t".join([t.to_formatted_string().replace("\n", "\n\t") for t in self.e1])
        )
        if self.e2:
            result += "\nelse:\n\t%s" % (
                "\n\t".join([t.to_formatted_string().replace("\n", "\n\t") for t in self.e2])
            )
        return result

class Recurse(ControlToken):
    """Recursive calling ControlToken."""

    def __init__(self, cond: Union[None, BoolToken], base_case: List[EnvToken], recursive_case: List[EnvToken]):
        """Creates a new Recurse ControlToken. When applied, 'cond' is executed. If that yields true, 'recursive_case' is executed and the whole program is called recursively, otherwise 'base_case' is executed. Note that this Token needs a pointer to its parent program to be able to call it recursively."""
        self.cond = cond
        self.base_case = base_case
        self.recursive_case = recursive_case
        self.calls = 0

    def apply(self, env: Environment) -> Environment:
        # Raise exception if recursive call limit is reached
        if self.calls >= env.program.recursive_call_limit:
            raise RecursiveCallLimitReached()

        self.calls += 1

        # if the condition is None or true, make recursive call
        if self.cond is None or self.cond.apply(env):
            env = Program(self.recursive_case).interp(env, False)
            return env.program.interp(env)

        # else, base case
        return Program(self.base_case).interp(env, False)

    def number_of_tokens(self, control_cost=2) -> int:
        return control_cost + \
               sum([t.number_of_tokens(control_cost) for t in self.base_case]) + \
               sum([t.number_of_tokens(control_cost) for t in self.recursive_case])

    def __str__(self):
        return "Recurse(%s [%s] [%s])" % \
               (self.cond, ", ".join(list(map(str, self.base_case))), ", ".join(list(map(str, self.recursive_case))))

    def __repr__(self):
        return "Recurse(%s [%s] [%s])" % \
               (self.cond, ", ".join(list(map(str, self.base_case))), ", ".join(list(map(str, self.recursive_case))))

    def to_formatted_string(self):
        result = "while %s do:\n\t%s" % (
            self.cond.to_formatted_string(),
            "\n\t".join([t.to_formatted_string().replace("\n", "\n\t") for t in self.recursive_case])
        )
        if self.base_case:
            result += "\nfinally:\n\t%s" % (
                "\n\t".join([t.to_formatted_string().replace("\n", "\n\t") for t in self.base_case])
            )
        return result

class LoopWhile(ControlToken):
    """Loop ControlToken."""

    def __init__(self, cond: BoolToken, loop_body: List[EnvToken]):
        """Creates a new Loop ControlToken. 'loop_body' will run as long as 'cond' is true."""
        self.cond = cond
        self.loop_body = loop_body

    def apply(self, env: Environment) -> Environment:
        # Raise exception if recursive call limit is reached
        # if the condition is None or true, make recursive call
        self.calls = 0
        while self.cond.apply(env):
            if self.calls >= 100:
                raise LoopIterationLimitReached()
            self.calls += 1

            for token in self.loop_body:
                token.apply(env)

        return env

    def number_of_tokens(self, control_cost=2) -> int:
        return control_cost + sum([t.number_of_tokens(control_cost) for t in self.loop_body])

    def __str__(self):
        return "LoopWhile(%s [%s])" % \
               (self.cond, ", ".join(list(map(str, self.loop_body))))

    def __repr__(self):
        return "LoopWhile(%s [%s])" % \
               (self.cond, ", ".join(list(map(str, self.loop_body))))

    def to_formatted_string(self):
        result = "while %s do:\n\t%s" % (
            self.cond.to_formatted_string(),
            "\n\t".join([t.to_formatted_string().replace("\n", "\n\t") for t in self.loop_body])
        )
        return result


class RecursiveCallLimitReached(Exception):
    """"Exception raised when the recursive call limit, set in the Program constructor is reached."""
    pass


class LoopIterationLimitReached(Exception):
    """"Exception raised when the recursive call limit, set in the Program constructor is reached."""
    pass