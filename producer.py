#!/bin/python3
import random
import time


class RandomGenerator:
    def __init__(self) -> None:
        self.operations = ["-", "+", "*", "/"]

    def generate_number(self, exclude_zero=False):
        low = 1 if exclude_zero else 0
        return random.randint(low, 9)

    def generate_operation(self):
        return random.choice(self.operations)
    
    def generate_line(self):
        a = self.generate_number()
        o = self.generate_operation()
        b = self.generate_number(exclude_zero=(o == "/"))
        return f"{a}{o}{b}"
    
    def generate_lines(self, n):
        lst = []
        for i in range(n):
            lst.append(self.generate_line())
        return lst


if __name__ == "__main__":
    N = random.randint(120, 180)
    sleep_time = 1
    generator = RandomGenerator()
    for line in generator.generate_lines(N):
        print(line)
        time.sleep(sleep_time)
