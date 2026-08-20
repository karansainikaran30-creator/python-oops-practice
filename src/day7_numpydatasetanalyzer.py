import numpy as np


class NumpyDatasetAnalyzer:

    # Constructor
    def __init__(self, data):
        self.data = data
        self.array = None

    # Input Validation
    def validate_input(self):

        if not isinstance(self.data, list):
            raise ValueError("Dataset must be a list.")

        if len(self.data) == 0:
            raise ValueError("Dataset cannot be empty.")

        # Check every row is a list
        if not all(isinstance(row, list) for row in self.data):
            raise ValueError("Each row must be a list.")

        # Check rows have same number of columns
        number_of_columns = len(self.data[0])

        if number_of_columns == 0:
            raise ValueError("Rows cannot be empty.")

        for row in self.data:
            if len(row) != number_of_columns:
                raise ValueError(
                    "All rows must contain the same number of columns."
                )

        # Check numerical values
        for row in self.data:
            for value in row:
                if not isinstance(value, (int, float, np.number)) \
                        or isinstance(value, bool):
                    raise ValueError(
                        "Dataset contains non-numeric values."
                    )

    # Convert to NumPy Array
    def convert_to_array(self):
        self.array = np.array(self.data)

    # Dataset Information
    def get_dataset_info(self):

        rows, columns = self.array.shape

        print("\nNumPy Array:")
        print(self.array)

        print("\nDataset Information:")
        print("Rows:", rows)
        print("Columns:", columns)
        print("Dimensions:", self.array.ndim)
        print("Shape:", self.array.shape)
        print("Size:", self.array.size)
        print("Data Type:", self.array.dtype)

    # Column Extraction
    def get_column(self, column_index):

        if column_index < 0 or column_index >= self.array.shape[1]:
            raise IndexError("Invalid column index.")

        return self.array[:, column_index]

    # Row Extraction
    def get_row(self, row_index):

        if row_index < 0 or row_index >= self.array.shape[0]:
            raise IndexError("Invalid row index.")

        return self.array[row_index]

    # Column Mean
    def calculate_column_mean(self):
        return np.mean(self.array, axis=0)

    # Column Minimum
    def calculate_column_minimum(self):
        return np.min(self.array, axis=0)

    # Column Maximum
    def calculate_column_maximum(self):
        return np.max(self.array, axis=0)

    # Column Standard Deviation
    def calculate_column_std(self):
        return np.std(self.array, axis=0)

    # Feature Scaling
    def scale_features(self):

        minimum = self.calculate_column_minimum()
        maximum = self.calculate_column_maximum()

        difference = maximum - minimum

        # Copy to avoid modifying original data
        scaled = np.zeros_like(
            self.array,
            dtype=float
        )

        # Handle normal features
        non_constant = difference != 0

        scaled[:, non_constant] = (
            self.array[:, non_constant]
            - minimum[non_constant]
        ) / difference[non_constant]

        # Constant features remain 0
        scaled[:, ~non_constant] = 0.0

        return scaled

    # Feature Summary
    def feature_summary(self):

        print("\nFeature Summary:")
        print("-" * 65)

        means = self.calculate_column_mean()
        minimums = self.calculate_column_minimum()
        maximums = self.calculate_column_maximum()
        stds = self.calculate_column_std()

        print(
            f"{'Feature':<15}"
            f"{'Mean':<15}"
            f"{'Minimum':<15}"
            f"{'Maximum':<15}"
            f"{'Std':<15}"
        )

        print("-" * 65)

        for i in range(self.array.shape[1]):
            print(
                f"Feature {i:<8}"
                f"{means[i]:<15.2f}"
                f"{minimums[i]:<15.2f}"
                f"{maximums[i]:<15.2f}"
                f"{stds[i]:<15.2f}"
            )

    # Bonus: Split Features and Target
    def split_features_target(self, target_index):

        if target_index < 0 or target_index >= self.array.shape[1]:
            raise IndexError("Invalid target index.")

        X = np.delete(self.array, target_index, axis=1)
        y = self.array[:, target_index]

        return X, y

    # Display Complete Report
    def display_report(self):

        print("=" * 65)
        print("          NUMPY 2D DATASET ANALYZER REPORT")
        print("=" * 65)

        print("\nOriginal Data:")
        print(self.data)

        self.get_dataset_info()

        print("\nColumn Statistics:")

        print(
            "Mean:",
            np.round(self.calculate_column_mean(), 2)
        )

        print(
            "Minimum:",
            self.calculate_column_minimum()
        )

        print(
            "Maximum:",
            self.calculate_column_maximum()
        )

        print(
            "Standard Deviation:",
            np.round(self.calculate_column_std(), 4)
        )

        self.feature_summary()

        print("\nColumn Extraction:")
        print("Column 0:", self.get_column(0))

        print("\nRow Extraction:")
        print("Row 0:", self.get_row(0))

        print("\nMin-Max Scaled Features:")
        print(np.round(self.scale_features(), 4))

        print("\nBonus: Features and Target")

        X, y = self.split_features_target(
            self.array.shape[1] - 1
        )

        print("X (Features):")
        print(X)

        print("\ny (Target):")
        print(y)

        print("=" * 65)


# Main Function
def main():

    # Dataset given in assignment
    data = [
        [25, 30000, 2],
        [30, 45000, 5],
        [35, 60000, 8],
        [40, 80000, 12],
        [45, 100000, 15]
    ]

    try:

        # Create Object
        obj = NumpyDatasetAnalyzer(data)

        # Validate
        obj.validate_input()

        # Convert to NumPy
        obj.convert_to_array()

        # Display Report
        obj.display_report()

    except ValueError as e:
        print("Error:", e)

    except IndexError as e:
        print("Index Error:", e)

    except Exception as e:
        print("Unexpected Error:", e)


# Entry Point
if __name__ == "__main__":
    main()