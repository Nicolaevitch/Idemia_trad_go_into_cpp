class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, grade):
        if 0 <= grade <= 20:
            self.grades.append(grade)
        else:
            raise ValueError("La note doit être comprise entre 0 et 20.")

    def average(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def has_passed(self):
        return self.average() >= 10
