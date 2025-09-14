

class PhysicsError(BaseException):

    def __init__(self, *args, **kwargs):
        if len(args):
            self.message = args[0]
        else:
            self.message = ''
        self.args = args
        self.kwargs = kwargs
        super(PhysicsError, self).__init__(*args, **kwargs)


class ConvergenceError(PhysicsError):
    pass


class EquilibriumError(PhysicsError):
    pass

