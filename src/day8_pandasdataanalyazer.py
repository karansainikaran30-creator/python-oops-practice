import pandas as pd


class PandasDataAnalyzer:

    def __init__(self, data):
        self.data = data
        self.df = None
        self.cleaned_df = None

    # Step 3: Create DataFrame
    def create_dataframe(self):
        self.df = pd.DataFrame(
            self.data,
            columns=["Customer", "Age", "Income", "Experience", "Purchased"]
        )
        return self.df

    # Step 4: Validate Input
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

        # Check every record has 5 values
        for record in self.data:
            if len(record) != 5:
                raise ValueError("All records must contain exactly 5 values.")

        # Check required columns
        if self.df is not None:
            for column in required_columns:
                if column not in self.df.columns:
                    raise ValueError(f"Missing required column: {column}")

        return True

    # Step 5: Dataset Information
    def get_dataset_info(self):
        print("\n--- DATASET INFORMATION ---")
        print("Rows:", self.df.shape[0])
        print("Columns:", self.df.shape[1])
        print("Column Names:", list(self.df.columns))
        print("\nData Types:")
        print(self.df.dtypes)
        print("\nShape:", self.df.shape)

    # Step 6: Find Missing Values
    def find_missing_values(self):
        print("\n--- MISSING VALUES ---")
        missing = self.df.isnull()
        print(missing)

        return missing

    # Count Missing Values
    def count_missing_values(self):
        print("\n--- MISSING VALUE COUNT ---")
        missing_count = self.df.isnull().sum()
        print(missing_count)

        print("\nTotal Missing Values:", missing_count.sum())

        return missing_count

    # Step 7: Find Duplicates
    def find_duplicates(self):
        print("\n--- DUPLICATE RECORDS ---")

        duplicates = self.df[self.df.duplicated()]

        print(duplicates)
        print("Duplicate Records:", len(duplicates))

        return duplicates

    # Step 8: Remove Duplicates
    def remove_duplicates(self):
        self.cleaned_df = self.df.drop_duplicates().copy()

        print("\n--- AFTER REMOVING DUPLICATES ---")
        print(self.cleaned_df)

        return self.cleaned_df

    # Step 9: Fill Missing Income
    def fill_missing_values(self):
        if self.cleaned_df is None:
            self.cleaned_df = self.df.drop_duplicates().copy()

        income_mean = self.cleaned_df["Income"].mean()

        self.cleaned_df["Income"] = self.cleaned_df["Income"].fillna(
            income_mean
        )

        print("\n--- AFTER FILLING MISSING INCOME ---")
        print(self.cleaned_df)

        print("\nMean Income Used:", income_mean)

        return self.cleaned_df

    # Step 10: Filtering
    def filter_customers(self, min_income):
        result = self.cleaned_df[
            self.cleaned_df["Income"] >= min_income
        ]

        print(f"\n--- CUSTOMERS WITH INCOME >= {min_income} ---")
        print(result)

        return result

    # Step 11: Sorting
    def sort_by_income(self, ascending=True):
        result = self.cleaned_df.sort_values(
            by="Income",
            ascending=ascending
        )

        print("\n--- SORTED BY INCOME ---")
        print(result)

        return result

    # Step 12: Statistics
    def calculate_statistics(self):
        numerical_columns = [
            "Age",
            "Income",
            "Experience",
            "Purchased"
        ]

        statistics = self.cleaned_df[numerical_columns].agg(
            ["mean", "min", "max", "std"]
        )

        print("\n--- NUMERICAL STATISTICS ---")
        print(statistics)

        return statistics

    # Step 13: Feature Analysis
    def analyze_features(self):
        print("\n--- FEATURE ANALYSIS ---")

        features = [
            "Age",
            "Income",
            "Experience",
            "Purchased"
        ]

        for feature in features:
            print(f"\n{feature}")
            print("Mean:", self.cleaned_df[feature].mean())
            print("Minimum:", self.cleaned_df[feature].min())
            print("Maximum:", self.cleaned_df[feature].max())
            print("Std Dev:", self.cleaned_df[feature].std())

    # Step 14: Target Analysis
    def analyze_target(self):
        print("\n--- PURCHASE ANALYSIS ---")

        purchased = (
            self.cleaned_df["Purchased"] == 1
        ).sum()

        not_purchased = (
            self.cleaned_df["Purchased"] == 0
        ).sum()

        print("Purchased:", purchased)
        print("Not Purchased:", not_purchased)

        return purchased, not_purchased

    # Step 15: EDA
    def perform_eda(self):
        print("\n--- EXPLORATORY DATA ANALYSIS ---")

        customer_count = len(self.cleaned_df)
        average_age = self.cleaned_df["Age"].mean()
        average_income = self.cleaned_df["Income"].mean()
        highest_income = self.cleaned_df["Income"].max()
        average_experience = self.cleaned_df["Experience"].mean()

        number_of_purchasers = (
            self.cleaned_df["Purchased"] == 1
        ).sum()

        print("Customer Count:", customer_count)
        print("Average Age:", average_age)
        print("Average Income:", average_income)
        print("Highest Income:", highest_income)
        print("Average Experience:", average_experience)
        print("Number of Purchasers:", number_of_purchasers)

    # Bonus Challenge
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

    # Step 16: Final Report
    def display_report(self):
        print("\n")
        print("=" * 50)
        print("       CUSTOMER DATA ANALYSIS")
        print("=" * 50)

        print("\nOriginal Dataset Shape:", self.df.shape)

        print(
            "Missing Income Values:",
            self.df["Income"].isnull().sum()
        )

        print(
            "Duplicate Records:",
            self.df.duplicated().sum()
        )

        print(
            "Rows After Cleaning:",
            len(self.cleaned_df)
        )

        self.calculate_statistics()
        self.analyze_target()
        self.perform_eda()


# ------------------------------------------------
# TEST CASES
# ------------------------------------------------

def run_tests():

    print("\n" + "=" * 50)
    print("             TEST CASES")
    print("=" * 50)

    # Test Case 1: Normal Dataset
    data = [
        ["C001", 25, 30000, 2, 0],
        ["C002", 30, 45000, 5, 1],
        ["C003", 35, None, 8, 1],
        ["C004", 40, 80000, 12, 1],
        ["C005", 45, 100000, 15, 0],
        ["C002", 30, 45000, 5, 1]
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

    # Filtering
    analyzer.filter_customers(50000)

    # Sorting
    analyzer.sort_by_income(ascending=True)
    analyzer.sort_by_income(ascending=False)

    # Statistics
    analyzer.calculate_statistics()

    # Feature Analysis
    analyzer.analyze_features()

    # Target Analysis
    analyzer.analyze_target()

    # EDA
    analyzer.perform_eda()

    # Bonus
    analyzer.group_by_purchase_status()

    # Final Report
    analyzer.display_report()


# ------------------------------------------------
# MAIN
# ------------------------------------------------

def main():

    try:
        run_tests()

    except ValueError as error:
        print("\nValidation Error:", error)

    except Exception as error:
        print("\nUnexpected Error:", error)


if __name__ == "__main__":
    main()