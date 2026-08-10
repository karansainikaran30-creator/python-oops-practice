# src/remove_duplicates.py

class RemoveDuplicates:
    def __init__(self, numbers):
        """
        Constructor to initialize the RemoveDuplicates object.

        Args:
            numbers (list): List of numbers (may contain duplicates).
        """
        self.numbers = numbers

    def validate_input(self):
        """Validates that the input is a list. Raises TypeError otherwise."""
        if not isinstance(self.numbers, list):
            raise TypeError('Input must be a list.')

    def remove_duplicates(self):
        """Removes duplicate values from self.numbers and returns a new list."""
        unique_numbers = []
        for value in self.numbers:
            if value not in unique_numbers:
                unique_numbers.append(value)
        return unique_numbers

    def display_result(self):
        """Prints the original list and the list with duplicates removed."""
        unique_numbers = self.remove_duplicates()
        print("Original List :", self.numbers)
        print("Unique List   :", unique_numbers)


def main():
    numbers = [10, 20, 10, 30, 40, 20, 50, 30]

    try:
        rd = RemoveDuplicates(numbers)
        rd.validate_input()
        rd.display_result()
    except TypeError as e:
        print("Error:", e)


if __name__ == '__main__':
    main()