import numpy as np


class NumpyFeatureProcessor:

    def __init__(self, data):
        self.data = data
        self.array = None
        self.min_max_data = None
        self.standardized_data = None

    # Step 7: Input Validation
    def validate_input(self):
        if not isinstance(self.data, list):
            raise ValueError("Input must be a list.")

        if len(self.data) == 0:
            raise ValueError("Input list cannot be empty.")

        if not all(isinstance(x, (int, float, np.number))
                   and not isinstance(x, bool)
                   for x in self.data):
            raise ValueError("Dataset contains non-numeric values.")

    # Step 8: Convert to NumPy Array
    def convert_to_array(self):
        self.array = np.array(self.data)

    # Step 9: Array Information
    def get_array_info(self):
        print("\nNumPy Array:")
        print(self.array)

        print("Data Type:", self.array.dtype)
        print("Dimensions:", self.array.ndim)
        print("Shape:", self.array.shape)
        print("Size:", self.array.size)

    # Step 10: Minimum
    def calculate_minimum(self):
        return np.min(self.array)

    # Step 11: Maximum
    def calculate_maximum(self):
        return np.max(self.array)

    # Step 12: Mean
    def calculate_mean(self):
        return np.mean(self.array)

    # Step 13: Standard Deviation
    def calculate_standard_deviation(self):
        return np.std(self.array)

    # Step 14: Min-Max Scaling
    def min_max_scale(self):

        minimum = self.calculate_minimum()
        maximum = self.calculate_maximum()

        if maximum == minimum:
            raise ValueError(
                "Min-Max Scaling cannot be performed because all values are same."
            )

        self.min_max_data = (
            self.array - minimum
        ) / (maximum - minimum)

        return self.min_max_data

    # Step 15: Z-Score Standardization
    def standardize(self):

        mean = self.calculate_mean()
        std = self.calculate_standard_deviation()

        if std == 0:
            raise ValueError(
                "Z-Score Standardization cannot be performed because standard deviation is zero."
            )

        self.standardized_data = (
            self.array - mean
        ) / std

        return self.standardized_data

    # Bonus: Compare Scaling Methods
    def compare_scaling_methods(self):

        min_max = self.min_max_scale()
        z_score = self.standardize()

        print("\nComparison Table")
        print("-" * 50)
        print(f"{'Original':<15}{'Min-Max':<15}{'Z-Score':<15}")
        print("-" * 50)

        for original, mm, zs in zip(
            self.array, min_max, z_score
        ):
            print(f"{original:<15}{mm:<15.4f}{zs:<15.4f}")

    # Step 18: Display Report
    def display_report(self):

        print("=" * 50)
        print("       NUMPY FEATURE PROCESSING REPORT")
        print("=" * 50)

        print("\nOriginal Data:")
        print(self.data)

        self.get_array_info()

        print("\nStatistics:")
        print("Minimum:", self.calculate_minimum())
        print("Maximum:", self.calculate_maximum())
        print("Mean:", self.calculate_mean())
        print(
            "Standard Deviation:",
            round(self.calculate_standard_deviation(), 4)
        )

        print("\nMin-Max Scaled:")

        try:
            scaled = self.min_max_scale()
            print(np.round(scaled, 4))
        except ValueError as e:
            print("Error:", e)

        print("\nZ-Score Standardized:")

        try:
            standardized = self.standardize()
            print(np.round(standardized, 4))
        except ValueError as e:
            print("Error:", e)

        print("=" * 50)


# Step 19: Main Function
def main():

    # Step 20: Dataset
    data = [10, 20, 30, 40, 50]

    try:

        # Step 21: Create Object
        obj = NumpyFeatureProcessor(data)

        # Step 22: Validate
        obj.validate_input()

        # Convert to NumPy
        obj.convert_to_array()

        # Display Report
        obj.display_report()

        # Bonus Challenge
        print("\nBONUS: Scaling Comparison")
        obj.compare_scaling_methods()

    except ValueError as e:
        print("Error:", e)

    except Exception as e:
        print("Unexpected Error:", e)


# Step 24: Entry Point
if __name__ == "__main__":
    main()