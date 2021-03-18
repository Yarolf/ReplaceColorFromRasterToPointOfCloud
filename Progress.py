class Progress:
    max_value = 0
    current_value = 0
    prev_percent = -1

    def __init__(self, max_value):
        self.max_value = max_value

    def __print_percent(self):
        percent = self.current_value / (self.max_value / 100)
        percent = round(percent, 1)
        if self.prev_percent != percent:
            print('\r', end='')
            self.prev_percent = percent
            print(percent, '%', end='')

    def step(self):
        self.current_value += 1
        self.__print_percent()

    def reset(self):
        self.current_value = 0
        self.prev_percent = 0


