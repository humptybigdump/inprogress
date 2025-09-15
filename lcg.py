class LCG:
    
    def __init__(self, seed, a, c, m):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m
    
    def genNumbers(self, length):
        numbers = []
        
        number = self.seed
        for i in range(length):
            number = (self.a*number+self.c)%self.m
            numbers.append(number/self.m)
        
        return numbers


