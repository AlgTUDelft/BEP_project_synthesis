

class IllegalActionException(Exception):
    """Raised when an illegal Action is applied to a Completable Token or a Program"""
    pass


class ApplyingIncompleteTokenException(Exception):
    """"Raised when you try to apply a CompletableToken on an environment while this token has not been completed yet"""
    pass


class TokenAlreadyCompletedException(Exception):
    """Raised when a Token is already complete,
    but you try to do an action/method call that is only possible for incomplete tokens"""
    pass


class ProgramAlreadyCompletedException(Exception):
    """Is raised when a method/action is called that should only be called on an incomplete program"""
    pass


class MaxNumberOfIterationsExceededException(Exception):
    """Raised when the maximum number of iterations is exceeded"""
    pass


class CannotInterpIncompleteProgram(Exception):
    """Raised when a program is interpret while not yet completed"""
    pass