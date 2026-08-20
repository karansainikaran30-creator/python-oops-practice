import os

import numpy as np
import pandas as pd


class RemoveDuplicates:
    def __init__(self, numbers):
        """Constructor to initialize the RemoveDuplicates object."""
        self.numbers = numbers

    def validate_input(self):
        """Validates that the input is a list. Raises TypeError otherwise."""
        if not isinstance(self.numbers, list):
            raise TypeError("Input must be a list.")

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

        most_frequent = max(frequency, key=frequency.get)
        least_frequent = min(frequency, key=frequency.get)

        print("Most Frequent Element:", most_frequent)
        print("Least Frequent Element:", least_frequent)
        print("Unique Elements:", len(frequency))
        print("Duplicate Elements:",
              sum(1 for value in frequency.values() if value > 1))


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
                raise ValueError("Input must contain only numerical values.")

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


class MissingValueHandler:
    def __init__(self, data):
        self.data = data
        self.cleaned_data = None

    def validate_input(self):
        if not isinstance(self.data, list):
            raise ValueError("Input must be a list.")

        if len(self.data) == 0:
            raise ValueError("Input list cannot be empty.")

        for value in self.data:
            if value is not None and not isinstance(value, (int, float)):
                raise ValueError("Dataset contains invalid values.")

    def find_missing_indexes(self):
        indexes = []
        for i in range(len(self.data)):
            if self.data[i] is None:
                indexes.append(i)
        return indexes

    def count_missing_values(self):
        count = 0
        for value in self.data:
            if value is None:
                count += 1
        return count

    def calculate_mean(self):
        total = 0
        count = 0

        for value in self.data:
            if value is not None:
                total += value
                count += 1

        if count == 0:
            raise ValueError("No valid values exist to calculate the mean.")

        return total / count

    def fill_missing_values(self):
        mean = self.calculate_mean()
        self.cleaned_data = self.data.copy()

        for i in range(len(self.cleaned_data)):
            if self.cleaned_data[i] is None:
                self.cleaned_data[i] = mean

        return self.cleaned_data

    def display_report(self):
        missing_indexes = self.find_missing_indexes()
        missing_values = self.count_missing_values()
        mean = self.calculate_mean()
        cleaned_data = self.fill_missing_values()
        available_values = len(self.data) - missing_values

        print("========================================")
        print("         MISSING VALUE REPORT")
        print("========================================")
        print("Original Data:")
        print(self.data)
        print("Total Values :", len(self.data))
        print("Missing Values :", missing_values)
        print("Missing Indexes :", missing_indexes)
        print("Available Values :", available_values)
        print("Mean :", mean)
        print("Cleaned Data:")
        print(cleaned_data)
        print("========================================")


class FeatureScaler:
    def __init__(self, data):
        self.data = data
        self.scaled_data = None

    def validate_input(self):
        if not isinstance(self.data, list):
            raise ValueError("Input must be a list.")

        if len(self.data) == 0:
            raise ValueError("Input list cannot be empty.")

        for value in self.data:
            if not isinstance(value, (int, float)):
                raise ValueError("Dataset contains invalid values.")

    def find_minimum(self):
        minimum = self.data[0]
        for value in self.data:
            if value < minimum:
                minimum = value
        return minimum

    def find_maximum(self):
        maximum = self.data[0]
        for value in self.data:
            if value > maximum:
                maximum = value
        return maximum

    def scale_data(self):
        minimum = self.find_minimum()
        maximum = self.find_maximum()

        if minimum == maximum:
            raise ValueError("Cannot scale data because all values are identical.")

        self.scaled_data = []
        for value in self.data:
            scaled_value = (value - minimum) / (maximum - minimum)
            self.scaled_data.append(scaled_value)

        return self.scaled_data

    def display_report(self):
        minimum = self.find_minimum()
        maximum = self.find_maximum()
        scaled_data = self.scale_data()

        print("========================================")
        print("         FEATURE SCALING REPORT")
        print("========================================")
        print("Original Data :", self.data)
        print("Minimum :", minimum)
        print("Maximum :", maximum)
        print("Scaled Data :", scaled_data)
        print("========================================")


class NumpyFeatureProcessor:
    def __init__(self, data):
        self.data = data
        self.array = None
        self.min_max_data = None
        self.standardized_data = None

    def validate_input(self):
        if not isinstance(self.data, list):
            raise ValueError("Input must be a list.")

        if len(self.data) == 0:
            raise ValueError("Input list cannot be empty.")

        if not all(isinstance(x, (int, float, np.number)) and not isinstance(x, bool)
                   for x in self.data):
            raise ValueError("Dataset contains non-numeric values.")

    def convert_to_array(self):
        self.array = np.array(self.data)

    def get_array_info(self):
        print("\nNumPy Array:")
        print(self.array)
        print("Data Type:", self.array.dtype)
        print("Dimensions:", self.array.ndim)
        print("Shape:", self.array.shape)
        print("Size:", self.array.size)

    def calculate_minimum(self):
        return np.min(self.array)

    def calculate_maximum(self):
        return np.max(self.array)

    def calculate_mean(self):
        return np.mean(self.array)

    def calculate_standard_deviation(self):
        return np.std(self.array)

    def min_max_scale(self):
        minimum = self.calculate_minimum()
        maximum = self.calculate_maximum()

        if maximum == minimum:
            raise ValueError("Min-Max Scaling cannot be performed because all values are same.")

        self.min_max_data = (self.array - minimum) / (maximum - minimum)
        return self.min_max_data

    def standardize(self):
        mean = self.calculate_mean()
        std = self.calculate_standard_deviation()

        if std == 0:
            raise ValueError("Z-Score Standardization cannot be performed because standard deviation is zero.")

        self.standardized_data = (self.array - mean) / std
        return self.standardized_data

    def compare_scaling_methods(self):
        min_max = self.min_max_scale()
        z_score = self.standardize()

        print("\nComparison Table")
        print("-" * 50)
        print(f"{'Original':<15}{'Min-Max':<15}{'Z-Score':<15}")
        print("-" * 50)

        for original, mm, zs in zip(self.array, min_max, z_score):
            print(f"{original:<15}{mm:<15.4f}{zs:<15.4f}")

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
        print("Standard Deviation:", round(self.calculate_standard_deviation(), 4))

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


class NumpyDatasetAnalyzer:
    def __init__(self, data):
        self.data = data
        self.array = None

    def validate_input(self):
        if not isinstance(self.data, list):
            raise ValueError("Dataset must be a list.")

        if len(self.data) == 0:
            raise ValueError("Dataset cannot be empty.")

        if not all(isinstance(row, list) for row in self.data):
            raise ValueError("Each row must be a list.")

        number_of_columns = len(self.data[0])

        if number_of_columns == 0:
            raise ValueError("Rows cannot be empty.")

        for row in self.data:
            if len(row) != number_of_columns:
                raise ValueError("All rows must contain the same number of columns.")

        for row in self.data:
            for value in row:
                if not isinstance(value, (int, float, np.number)) or isinstance(value, bool):
                    raise ValueError("Dataset contains non-numeric values.")

    def convert_to_array(self):
        self.array = np.array(self.data)

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

    def get_column(self, column_index):
        if column_index < 0 or column_index >= self.array.shape[1]:
            raise IndexError("Invalid column index.")
        return self.array[:, column_index]

    def get_row(self, row_index):
        if row_index < 0 or row_index >= self.array.shape[0]:
            raise IndexError("Invalid row index.")
        return self.array[row_index]

    def calculate_column_mean(self):
        return np.mean(self.array, axis=0)

    def calculate_column_minimum(self):
        return np.min(self.array, axis=0)

    def calculate_column_maximum(self):
        return np.max(self.array, axis=0)

    def calculate_column_std(self):
        return np.std(self.array, axis=0)

    def scale_features(self):
        minimum = self.calculate_column_minimum()
        maximum = self.calculate_column_maximum()
        difference = maximum - minimum

        scaled = np.zeros_like(self.array, dtype=float)
        non_constant = difference != 0

        scaled[:, non_constant] = (self.array[:, non_constant] - minimum[non_constant]) / difference[non_constant]
        scaled[:, ~non_constant] = 0.0

        return scaled

    def feature_summary(self):
        print("\nFeature Summary:")
        print("-" * 65)

        means = self.calculate_column_mean()
        minimums = self.calculate_column_minimum()
        maximums = self.calculate_column_maximum()
        stds = self.calculate_column_std()

        print(f"{'Feature':<15}{'Mean':<15}{'Minimum':<15}{'Maximum':<15}{'Std':<15}")
        print("-" * 65)

        for i in range(self.array.shape[1]):
            print(f"Feature {i:<8}{means[i]:<15.2f}{minimums[i]:<15.2f}{maximums[i]:<15.2f}{stds[i]:<15.2f}")

    def split_features_target(self, target_index):
        if target_index < 0 or target_index >= self.array.shape[1]:
            raise IndexError("Invalid target index.")

        X = np.delete(self.array, target_index, axis=1)
        y = self.array[:, target_index]
        return X, y

    def display_report(self):
        print("=" * 65)
        print("          NUMPY 2D DATASET ANALYZER REPORT")
        print("=" * 65)

        print("\nOriginal Data:")
        print(self.data)

        self.get_dataset_info()

        print("\nColumn Statistics:")
        print("Mean:", np.round(self.calculate_column_mean(), 2))
        print("Minimum:", self.calculate_column_minimum())
        print("Maximum:", self.calculate_column_maximum())
        print("Standard Deviation:", np.round(self.calculate_column_std(), 4))

        self.feature_summary()

        print("\nColumn Extraction:")
        print("Column 0:", self.get_column(0))

        print("\nRow Extraction:")
        print("Row 0:", self.get_row(0))

        print("\nMin-Max Scaled Features:")
        print(np.round(self.scale_features(), 4))

        print("\nBonus: Features and Target")
        X, y = self.split_features_target(self.array.shape[1] - 1)
        print("X (Features):")
        print(X)
        print("\ny (Target):")
        print(y)

        print("=" * 65)


class PandasDataAnalyzer:
    def __init__(self, data):
        self.data = data
        self.df = None
        self.cleaned_df = None

    def create_dataframe(self):
        self.df = pd.DataFrame(
            self.data,
            columns=["Customer", "Age", "Income", "Experience", "Purchased"]
        )
        return self.df

    def validate_input(self):
        if not isinstance(self.data, list) or len(self.data) == 0:
            raise ValueError("Input dataset must be a non-empty list.")

        required_columns = [
            "Customer",
            "Age",
            "Income",
            "Experience",
            "Purchased"
        ]

        for record in self.data:
            if len(record) != 5:
                raise ValueError("All records must contain exactly 5 values.")

        if self.df is not None:
            for column in required_columns:
                if column not in self.df.columns:
                    raise ValueError(f"Missing required column: {column}")

        return True

    def get_dataset_info(self):
        print("\n--- DATASET INFORMATION ---")
        print("Rows:", self.df.shape[0])
        print("Columns:", self.df.shape[1])
        print("Column Names:", list(self.df.columns))
        print("\nData Types:")
        print(self.df.dtypes)
        print("\nShape:", self.df.shape)

    def find_missing_values(self):
        print("\n--- MISSING VALUES ---")
        missing = self.df.isnull()
        print(missing)
        return missing

    def count_missing_values(self):
        print("\n--- MISSING VALUE COUNT ---")
        missing_count = self.df.isnull().sum()
        print(missing_count)
        print("\nTotal Missing Values:", missing_count.sum())
        return missing_count

    def find_duplicates(self):
        print("\n--- DUPLICATE RECORDS ---")
        duplicates = self.df[self.df.duplicated()]
        print(duplicates)
        print("Duplicate Records:", len(duplicates))
        return duplicates

    def remove_duplicates(self):
        self.cleaned_df = self.df.drop_duplicates().copy()
        print("\n--- AFTER REMOVING DUPLICATES ---")
        print(self.cleaned_df)
        return self.cleaned_df

    def fill_missing_values(self):
        if self.cleaned_df is None:
            self.cleaned_df = self.df.drop_duplicates().copy()

        income_mean = self.cleaned_df["Income"].mean()
        self.cleaned_df["Income"] = self.cleaned_df["Income"].fillna(income_mean)

        print("\n--- AFTER FILLING MISSING INCOME ---")
        print(self.cleaned_df)
        print("\nMean Income Used:", income_mean)
        return self.cleaned_df

    def filter_customers(self, min_income):
        result = self.cleaned_df[self.cleaned_df["Income"] >= min_income]
        print(f"\n--- CUSTOMERS WITH INCOME >= {min_income} ---")
        print(result)
        return result

    def sort_by_income(self, ascending=True):
        result = self.cleaned_df.sort_values(by="Income", ascending=ascending)
        print("\n--- SORTED BY INCOME ---")
        print(result)
        return result

    def calculate_statistics(self):
        numerical_columns = ["Age", "Income", "Experience", "Purchased"]
        statistics = self.cleaned_df[numerical_columns].agg(["mean", "min", "max", "std"])
        print("\n--- NUMERICAL STATISTICS ---")
        print(statistics)
        return statistics

    def analyze_features(self):
        print("\n--- FEATURE ANALYSIS ---")
        features = ["Age", "Income", "Experience", "Purchased"]

        for feature in features:
            print(f"\n{feature}")
            print("Mean:", self.cleaned_df[feature].mean())
            print("Minimum:", self.cleaned_df[feature].min())
            print("Maximum:", self.cleaned_df[feature].max())
            print("Std Dev:", self.cleaned_df[feature].std())

    def analyze_target(self):
        print("\n--- PURCHASE ANALYSIS ---")
        purchased = (self.cleaned_df["Purchased"] == 1).sum()
        not_purchased = (self.cleaned_df["Purchased"] == 0).sum()
        print("Purchased:", purchased)
        print("Not Purchased:", not_purchased)
        return purchased, not_purchased

    def perform_eda(self):
        print("\n--- EXPLORATORY DATA ANALYSIS ---")
        customer_count = len(self.cleaned_df)
        average_age = self.cleaned_df["Age"].mean()
        average_income = self.cleaned_df["Income"].mean()
        highest_income = self.cleaned_df["Income"].max()
        average_experience = self.cleaned_df["Experience"].mean()
        number_of_purchasers = (self.cleaned_df["Purchased"] == 1).sum()

        print("Customer Count:", customer_count)
        print("Average Age:", average_age)
        print("Average Income:", average_income)
        print("Highest Income:", highest_income)
        print("Average Experience:", average_experience)
        print("Number of Purchasers:", number_of_purchasers)

    def group_by_purchase_status(self):
        print("\n--- GROUP BY PURCHASE STATUS ---")
        result = self.cleaned_df.groupby("Purchased").agg(
            Customer_Count=("Customer", "count"),
            Average_Age=("Age", "mean"),
            Average_Income=("Income", "mean"),
            Average_Experience=("Experience", "mean")
        )
        print(result)
        return result

    def display_report(self):
        print("\n")
        print("=" * 50)
        print("       CUSTOMER DATA ANALYSIS")
        print("=" * 50)
        print("\nOriginal Dataset Shape:", self.df.shape)
        print("Missing Income Values:", self.df["Income"].isnull().sum())
        print("Duplicate Records:", self.df.duplicated().sum())
        print("Rows After Cleaning:", len(self.cleaned_df))
        self.calculate_statistics()
        self.analyze_target()
        self.perform_eda()


class CustomerDataPipeline:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.cleaned_df = None
        self.summary = {}

    def validate_file(self):
        if not isinstance(self.file_path, str):
            raise ValueError("File path must be a string.")

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"CSV file does not exist: {self.file_path}")

        if not self.file_path.lower().endswith(".csv"):
            raise ValueError("Only CSV files are supported.")

        print("File validation successful.")

    def load_data(self):
        self.df = pd.read_csv(self.file_path)
        print("\n--- CSV DATA LOADED ---")
        print(self.df)
        return self.df

    def validate_columns(self):
        required_columns = [
            "CustomerID",
            "Age",
            "Income",
            "Experience",
            "PurchaseAmount",
            "Purchased"
        ]

        missing_columns = [
            column for column in required_columns if column not in self.df.columns
        ]

        if missing_columns:
            raise ValueError(f"Required columns are missing: {missing_columns}")

        print("\nColumn validation successful.")

    def inspect_dataset(self):
        print("\n" + "=" * 50)
        print("DATASET INSPECTION")
        print("=" * 50)
        print("Shape:", self.df.shape)
        print("Rows:", self.df.shape[0])
        print("Columns:", self.df.shape[1])
        print("\nColumn Names:")
        print(list(self.df.columns))
        print("\nData Types:")
        print(self.df.dtypes)
        print("\nMemory Information:")
        self.df.info()

    def generate_quality_report(self):
        print("\n" + "=" * 50)
        print("DATA QUALITY REPORT")
        print("=" * 50)

        total_rows = len(self.df)
        report = pd.DataFrame({
            "Data Type": self.df.dtypes.astype(str),
            "Missing Count": self.df.isnull().sum(),
            "Missing Percentage": (self.df.isnull().sum() / total_rows) * 100,
            "Unique Values": self.df.nunique()
        })

        print(report)
        self.summary["quality_report"] = report
        return report

    def find_duplicates(self):
        duplicates = self.df[self.df.duplicated()]
        print("\n" + "=" * 50)
        print("DUPLICATE RECORDS")
        print("=" * 50)
        print(duplicates)
        print("\nDuplicate Count:", len(duplicates))
        return duplicates

    def remove_duplicates(self):
        self.cleaned_df = self.df.drop_duplicates().copy()
        print("\nDuplicates removed.")
        print("Rows before:", len(self.df))
        print("Rows after:", len(self.cleaned_df))
        return self.cleaned_df

    def handle_missing_values(self):
        numerical_columns = ["Age", "Income", "PurchaseAmount"]
        print("\n" + "=" * 50)
        print("MEDIAN IMPUTATION")
        print("=" * 50)

        for column in numerical_columns:
            missing_before = self.cleaned_df[column].isnull().sum()
            if missing_before > 0:
                median_value = self.cleaned_df[column].median()
                self.cleaned_df[column] = self.cleaned_df[column].fillna(median_value)
                print(f"{column}: {missing_before} missing values filled with median = {median_value}")

        return self.cleaned_df

    def validate_cleaned_data(self):
        print("\n" + "=" * 50)
        print("CLEANED DATA VALIDATION")
        print("=" * 50)

        total_missing = self.cleaned_df.isnull().sum().sum()
        duplicate_count = self.cleaned_df.duplicated().sum()
        purchased_values = set(self.cleaned_df["Purchased"].dropna().unique())
        valid_purchased = purchased_values.issubset({0, 1})

        print("Total Missing Values:", total_missing)
        print("Duplicate Records:", duplicate_count)
        print("Purchased Values:", purchased_values)
        print("Purchased Values Valid:", valid_purchased)

        if total_missing != 0:
            raise ValueError("Missing values still exist.")

        if duplicate_count != 0:
            raise ValueError("Duplicate records still exist.")

        if not valid_purchased:
            raise ValueError("Purchased column must contain only 0 or 1.")

        print("\nCleaned data validation successful.")

    def detect_invalid_values(self):
        print("\n" + "=" * 50)
        print("INVALID VALUE DETECTION")
        print("=" * 50)

        invalid_age = self.cleaned_df[self.cleaned_df["Age"] <= 0]
        invalid_income = self.cleaned_df[self.cleaned_df["Income"] < 0]
        invalid_experience = self.cleaned_df[self.cleaned_df["Experience"] < 0]
        invalid_purchase = self.cleaned_df[self.cleaned_df["PurchaseAmount"] < 0]
        invalid_target = self.cleaned_df[~self.cleaned_df["Purchased"].isin([0, 1])]

        print("Invalid Age:", len(invalid_age))
        print("Invalid Income:", len(invalid_income))
        print("Invalid Experience:", len(invalid_experience))
        print("Invalid PurchaseAmount:", len(invalid_purchase))
        print("Invalid Purchased:", len(invalid_target))

        if len(invalid_age) > 0:
            raise ValueError("Invalid Age detected.")
        if len(invalid_income) > 0:
            raise ValueError("Invalid Income detected.")
        if len(invalid_experience) > 0:
            raise ValueError("Invalid Experience detected.")
        if len(invalid_purchase) > 0:
            raise ValueError("Invalid PurchaseAmount detected.")
        if len(invalid_target) > 0:
            raise ValueError("Invalid Purchased value detected.")

        print("\nNo invalid values found.")

    def create_features(self):
        self.cleaned_df["IncomePerExperience"] = np.where(
            self.cleaned_df["Experience"] == 0,
            0,
            self.cleaned_df["Income"] / self.cleaned_df["Experience"]
        )

        self.cleaned_df["PurchaseCategory"] = pd.cut(
            self.cleaned_df["PurchaseAmount"],
            bins=[-np.inf, 2000, 5000, np.inf],
            labels=["Low", "Medium", "High"],
            right=True
        )

        print("\n" + "=" * 50)
        print("FEATURE ENGINEERING")
        print("=" * 50)
        print(self.cleaned_df)
        return self.cleaned_df

    def create_age_group(self):
        self.cleaned_df["AgeGroup"] = np.select(
            [
                self.cleaned_df["Age"] < 30,
                (self.cleaned_df["Age"] >= 30) & (self.cleaned_df["Age"] <= 40),
                self.cleaned_df["Age"] > 40
            ],
            ["Young", "Adult", "Senior"],
            default="Unknown"
        )
        print("\nAge groups created.")
        return self.cleaned_df

    def get_high_value_customers(self):
        result = self.cleaned_df[self.cleaned_df["PurchaseAmount"] > 5000]
        print("\n" + "=" * 50)
        print("HIGH VALUE CUSTOMERS")
        print("=" * 50)
        print(result)
        return result

    def sort_by_purchase_amount(self):
        result = self.cleaned_df.sort_values(by="PurchaseAmount", ascending=False)
        print("\n" + "=" * 50)
        print("SORTED BY PURCHASE AMOUNT")
        print("=" * 50)
        print(result)
        return result

    def calculate_statistics(self):
        columns = ["Age", "Income", "Experience", "PurchaseAmount", "IncomePerExperience"]
        statistics = self.cleaned_df[columns].agg(["mean", "median", "min", "max", "std"])
        print("\n" + "=" * 50)
        print("STATISTICS")
        print("=" * 50)
        print(statistics)
        return statistics

    def calculate_correlation(self):
        columns = ["Age", "Income", "Experience", "PurchaseAmount", "Purchased"]
        correlation = self.cleaned_df[columns].corr()
        print("\n" + "=" * 50)
        print("CORRELATION MATRIX")
        print("=" * 50)
        print(correlation)
        print("\nCorrelation Explanation:")
        print("Positive correlation: both variables tend to increase together.")
        print("Negative correlation: one tends to increase when the other decreases.")
        print("Near-zero correlation: little or no linear relationship.")
        return correlation

    def analyze_by_purchase_status(self):
        result = self.cleaned_df.groupby("Purchased").agg(
            Customer_Count=("CustomerID", "count"),
            Average_Age=("Age", "mean"),
            Average_Income=("Income", "mean"),
            Average_Purchase=("PurchaseAmount", "mean")
        )
        print("\n" + "=" * 50)
        print("ANALYSIS BY PURCHASE STATUS")
        print("=" * 50)
        print(result)
        return result

    def perform_eda(self):
        total_customers = len(self.cleaned_df)
        average_age = self.cleaned_df["Age"].mean()
        average_income = self.cleaned_df["Income"].mean()
        median_income = self.cleaned_df["Income"].median()
        highest_purchase = self.cleaned_df["PurchaseAmount"].max()
        average_purchase = self.cleaned_df["PurchaseAmount"].mean()
        purchasers = (self.cleaned_df["Purchased"] == 1).sum()
        non_purchasers = (self.cleaned_df["Purchased"] == 0).sum()
        most_common_age_group = self.cleaned_df["AgeGroup"].mode()[0]
        most_common_purchase_category = self.cleaned_df["PurchaseCategory"].mode()[0]

        print("\n" + "=" * 50)
        print("EXPLORATORY DATA ANALYSIS")
        print("=" * 50)
        print("Total Customers:", total_customers)
        print("Average Age:", average_age)
        print("Average Income:", average_income)
        print("Median Income:", median_income)
        print("Highest Purchase:", highest_purchase)
        print("Average Purchase:", average_purchase)
        print("Purchasers:", purchasers)
        print("Non-Purchasers:", non_purchasers)
        print("Most Common Age Group:", most_common_age_group)
        print("Most Common Purchase Category:", most_common_purchase_category)

    def export_clean_data(self):
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, "cleaned_customer_data.csv")
        self.cleaned_df.to_csv(output_file, index=False)
        print("\n" + "=" * 50)
        print("EXPORT")
        print("=" * 50)
        print("Cleaned dataset exported to:")
        print(output_file)
        return output_file

    def generate_ml_ready_data(self):
        feature_columns = ["Age", "Income", "Experience", "PurchaseAmount", "IncomePerExperience"]
        X = self.cleaned_df[feature_columns].copy()
        y = self.cleaned_df["Purchased"].copy()

        print("\n" + "=" * 50)
        print("ML READY DATA")
        print("=" * 50)
        print("\nFeatures X:")
        print(X)
        print("\nTarget y:")
        print(y)
        return X, y

    def run_pipeline(self):
        print("\n")
        print("=" * 60)
        print("       CUSTOMER DATA CSV PIPELINE")
        print("=" * 60)

        self.validate_file()
        self.load_data()
        self.validate_columns()
        self.inspect_dataset()
        self.generate_quality_report()
        self.find_duplicates()
        self.remove_duplicates()
        self.handle_missing_values()
        self.validate_cleaned_data()
        self.detect_invalid_values()
        self.create_features()
        self.create_age_group()
        self.get_high_value_customers()
        self.sort_by_purchase_amount()
        self.calculate_statistics()
        self.calculate_correlation()
        self.analyze_by_purchase_status()
        self.perform_eda()
        self.generate_ml_ready_data()
        self.export_clean_data()

        print("\n")
        print("=" * 60)
        print("          PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)


def run_day1():
    print("\n=== Day 1: Remove Duplicates ===")
    numbers = [10, 20, 10, 30, 40, 20, 50, 30]
    try:
        rd = RemoveDuplicates(numbers)
        rd.validate_input()
        rd.display_result()
    except TypeError as e:
        print("Error:", e)


def run_day2():
    print("\n=== Day 2: Frequency Counter ===")
    numbers = [1, 2, 2, 3, 1, 5, 4, 2, 5, 5]
    try:
        counter = FrequencyCounter(numbers)
        counter.validate_input()
        counter.display_result()
    except (TypeError, ValueError) as e:
        print(e)


def run_day3():
    print("\n=== Day 3: Statistical Analyzer ===")
    numbers = [10, 20, 20, 30, 40, 50]
    try:
        analyzer = StatisticalAnalyzer(numbers)
        analyzer.validate_input()
        analyzer.display_result()
    except ValueError as error:
        print("Error:", error)


def run_day4():
    print("\n=== Day 4: Missing Value Handler ===")
    data = [25, 30, None, 40, None, 35, 28]
    try:
        obj = MissingValueHandler(data)
        obj.validate_input()
        obj.display_report()
    except ValueError as error:
        print("Error:", error)


def run_day5():
    print("\n=== Day 5: Feature Scaler ===")
    data = [10, 20, 30, 40, 50]
    try:
        obj = FeatureScaler(data)
        obj.validate_input()
        obj.display_report()
    except ValueError as error:
        print("Error:", error)


def run_day6():
    print("\n=== Day 6: NumPy Feature Processor ===")
    data = [10, 20, 30, 40, 50]
    try:
        obj = NumpyFeatureProcessor(data)
        obj.validate_input()
        obj.convert_to_array()
        obj.display_report()
        print("\nBONUS: Scaling Comparison")
        obj.compare_scaling_methods()
    except ValueError as e:
        print("Error:", e)
    except Exception as e:
        print("Unexpected Error:", e)


def run_day7():
    print("\n=== Day 7: NumPy Dataset Analyzer ===")
    data = [
        [25, 30000, 2],
        [30, 45000, 5],
        [35, 60000, 8],
        [40, 80000, 12],
        [45, 100000, 15],
    ]
    try:
        obj = NumpyDatasetAnalyzer(data)
        obj.validate_input()
        obj.convert_to_array()
        obj.display_report()
    except ValueError as e:
        print("Error:", e)
    except IndexError as e:
        print("Index Error:", e)
    except Exception as e:
        print("Unexpected Error:", e)


def run_day8():
    print("\n=== Day 8: Pandas Data Analyzer ===")
    data = [
        ["C001", 25, 30000, 2, 0],
        ["C002", 30, 45000, 5, 1],
        ["C003", 35, None, 8, 1],
        ["C004", 40, 80000, 12, 1],
        ["C005", 45, 100000, 15, 0],
        ["C002", 30, 45000, 5, 1],
    ]

    analyzer = PandasDataAnalyzer(data)
    analyzer.create_dataframe()
    analyzer.validate_input()
    analyzer.get_dataset_info()
    analyzer.find_missing_values()
    analyzer.count_missing_values()
    analyzer.find_duplicates()
    analyzer.remove_duplicates()
    analyzer.fill_missing_values()
    analyzer.filter_customers(50000)
    analyzer.sort_by_income(ascending=True)
    analyzer.sort_by_income(ascending=False)
    analyzer.calculate_statistics()
    analyzer.analyze_features()
    analyzer.analyze_target()
    analyzer.perform_eda()
    analyzer.group_by_purchase_status()
    analyzer.display_report()


def run_day9():
    print("\n=== Day 9: Customer Data Pipeline ===")
    file_path = "data/customer_data.csv"
    try:
        pipeline = CustomerDataPipeline(file_path)
        pipeline.run_pipeline()
    except FileNotFoundError as error:
        print("\nFile Error:", error)
    except ValueError as error:
        print("\nValidation Error:", error)
    except Exception as error:
        print("\nUnexpected Error:", error)


def main():
    run_day1()
    run_day2()
    run_day3()
    run_day4()
    run_day5()
    run_day6()
    run_day7()
    run_day8()
    run_day9()


if __name__ == "__main__":
    main()
    print("\n=== Day 1: Remove Duplicates ===")
    numbers = [10, 20, 10, 30, 40, 20, 50, 30]
    try:
        rd = RemoveDuplicates(numbers)
        rd.validate_input()
        rd.display_result()
    except TypeError as e:
        print("Error:", e)


def run_day2():
    print("\n=== Day 2: Frequency Counter ===")
    numbers = [1, 2, 2, 3, 1, 5, 4, 2, 5, 5]
    try:
        counter = FrequencyCounter(numbers)
        counter.validate_input()
        counter.display_result()
    except (TypeError, ValueError) as e:
        print(e)


def run_day3():
    print("\n=== Day 3: Statistical Analyzer ===")
    numbers = [10, 20, 20, 30, 40, 50]
    try:
        analyzer = StatisticalAnalyzer(numbers)
        analyzer.validate_input()
        analyzer.display_result()
    except ValueError as error:
        print("Error:", error)


def run_day4():
    print("\n=== Day 4: Missing Value Handler ===")
    data = [25, 30, None, 40, None, 35, 28]
    try:
        obj = MissingValueHandler(data)
        obj.validate_input()
        obj.display_report()
    except ValueError as error:
        print("Error:", error)


def run_day5():
    print("\n=== Day 5: Feature Scaler ===")
    data = [10, 20, 30, 40, 50]
    try:
        obj = FeatureScaler(data)
        obj.validate_input()
        obj.display_report()
    except ValueError as error:
        print("Error:", error)


def run_day6():
    print("\n=== Day 6: NumPy Feature Processor ===")
    data = [10, 20, 30, 40, 50]
    try:
        obj = NumpyFeatureProcessor(data)
        obj.validate_input()
        obj.convert_to_array()
        obj.display_report()
        print("\nBONUS: Scaling Comparison")
        obj.compare_scaling_methods()
    except ValueError as e:
        print("Error:", e)
    except Exception as e:
        print("Unexpected Error:", e)


def run_day7():
    print("\n=== Day 7: NumPy Dataset Analyzer ===")
    data = [
        [25, 30000, 2],
        [30, 45000, 5],
        [35, 60000, 8],
        [40, 80000, 12],
        [45, 100000, 15],
    ]
    try:
        obj = NumpyDatasetAnalyzer(data)
        obj.validate_input()
        obj.convert_to_array()
        obj.display_report()
    except ValueError as e:
        print("Error:", e)
    except IndexError as e:
        print("Index Error:", e)
    except Exception as e:
        print("Unexpected Error:", e)


def main():
    run_day1()
    run_day2()
    run_day3()
    run_day4()
    run_day5()
    run_day6()
    run_day7()


if __name__ == "__main__":
    main()
