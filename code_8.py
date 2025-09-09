class MyRange:
    def __init__(self, end: int):
        self.end: int = end
        self.index: int = -1

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.index < self.end - 1:
            self.index += 1
            return self.index
        else:
            raise StopIteration

for i in MyRange(10):
    print(f"{i=}")
