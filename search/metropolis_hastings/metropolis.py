from typing import Tuple
from common_environment.abstract_tokens import Token
from interpreter.interpreter import Program
from myparser.experiment import TestCase
from search.abstract_search import SearchAlgorithm


class MetropolisHasting(SearchAlgorithm):
    
    def search(test_case: TestCase, trans_tokens: set[Token], bool_tokens: set[Token]) -> Tuple[Program, int, int]:
        program: Program = Program([])
        return program
        