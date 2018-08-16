class calls(object):
    total = 0

    @staticmethod
    def count(f):
        def wrapped(*args, **kwargs):
            wrapped.calls += 1
            calls.total += 1
            return f(*args, **kwargs)
        wrapped.calls = 0
        return wrapped

    @staticmethod
    def sum():
        return calls.total
