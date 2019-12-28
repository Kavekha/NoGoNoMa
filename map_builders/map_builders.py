class Rect:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height

    def intersect(self, other):
        if self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1:
            return True
        return False

    def center(self):
        return (self.x1 + self.x2)//2, (self.y1 + self.y2) // 2
