class StatisticalAnalyzer:

    def __init__(self, numbers):
        self.numbers = numbers

    def validate_input(self):
        if not isinstance(self.numbers, list):
            raise ValueError("Input must be a list.")

        if len(self.numbers) == 0:
            raise ValueError("Input list cannot be empty.")

        for value in self.numbers:
            if not isinstance(value, (int, float)):
                raise ValueError(
                    "Input must contain only numerical values."
                )

        return True

    def calculate_mean(self):
        return sum(self.numbers) / len(self.numbers)

    def calculate_median(self):
        sorted_data = sorted(self.numbers)
        n = len(sorted_data)

        middle = n // 2

        if n % 2 == 1:
            return sorted_data[middle]
        else:
            return (sorted_data[middle - 1] + sorted_data[middle]) / 2

    def calculate_mode(self):
        frequency = {}

        for value in self.numbers:
            if value in frequency:
                frequency[value] += 1
            else:
                frequency[value] = 1

        max_frequency = max(frequency.values())

        if max_frequency == 1:
            return "No unique mode"

        modes = []

        for value, count in frequency.items():
            if count == max_frequency:
                modes.append(value)

        return modes

    def find_minimum(self):
        return min(self.numbers)

    def find_maximum(self):
        return max(self.numbers)

    def count_unique_values(self):
        unique_values = set(self.numbers)
        return len(unique_values)

    def display_result(self):
        print("=" * 32)
        print("       STATISTICAL REPORT")
        print("=" * 32)

        print("Original Data :", self.numbers)
        print("Mean          :", round(self.calculate_mean(), 2))
        print("Median        :", self.calculate_median())
        print("Mode          :", self.calculate_mode())
        print("Minimum       :", self.find_minimum())
        print("Maximum       :", self.find_maximum())
        print("Unique Values :", self.count_unique_values())

        print("=" * 32)


def main():

    numbers = [10, 20, 20, 30, 40, 50]

    try:
        analyzer = StatisticalAnalyzer(numbers)

        analyzer.validate_input()

        analyzer.display_result()

    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()