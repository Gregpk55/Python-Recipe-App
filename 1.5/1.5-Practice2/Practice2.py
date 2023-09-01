class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches

    def __str__(self):
        return f"{self.feet} feet, {self.inches} inches"

    def __add__(self, other):
        total_inches = (self.feet * 12 + self.inches) + (other.feet * 12 + other.inches)
        return Height(total_inches // 12, total_inches % 12)

    def __sub__(self, other):
        total_inches = (self.feet * 12 + self.inches) - (other.feet * 12 + other.inches)
            
        return Height(total_inches // 12, total_inches % 12)


person_A_height = Height(5, 10)
person_B_height = Height(3, 9)
height_difference = person_A_height - person_B_height
print("Height difference:", height_difference)
