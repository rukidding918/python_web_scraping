
class Exam:
    def __init__(self,guk,eng,math, option):
        self.guk = guk
        self.eng = eng
        self.math = math

    def proc(self):
        a = self.banolim(self.guk)
        b = self.banolim(self.eng)
        c = self.banolim(self.math)
        self.avg(a, b, c)

    def banolim(self, guk):
        pass


if __name__ == '__main__':
    ex1 = Exam(11,22,33,'')
    ex2 = Exam(11, 22, 33, '')
    ex3 = Exam(11, 22, 33, '')
