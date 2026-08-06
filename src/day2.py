class FrequencyCounter:
    def __init__(self, numbers):
        self.numbers = numbers

    def validate_input(self):
        if not isinstance(self.numbers, list):
            raise TypeError("Error - Input must be a list.")

        if len(self.numbers) == 0:
            raise ValueError("Error - Input list cannot be empty.")

    def count_frequency(self):
        frequency = {}

        for item in self.numbers:
            if item in frequency:
                frequency[item] += 1
            else:
                frequency[item] = 1

        return dict(sorted(frequency.items()))

    def display_result(self):
        frequency = self.count_frequency()
        print("Frequency Dictionary:", frequency)

        # Bonus Challenge
        most_frequent = max(frequency, key=frequency.get)
        least_frequent = min(frequency, key=frequency.get)

        print("Most Frequent Element:", most_frequent)
        print("Least Frequent Element:", least_frequent)
        print("Unique Elements:", len(frequency))
        print("Duplicate Elements:",
              sum(1 for value in frequency.values() if value > 1))


def main():
    numbers = [1, 2, 2, 3, 1, 5, 4, 2, 5, 5]

    try:
        counter = FrequencyCounter(numbers)
        counter.validate_input()
        counter.display_result()

    except (TypeError, ValueError) as e:
        print(e)


if __name__ == "__main__":
    main()