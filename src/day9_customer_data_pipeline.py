import os
import pandas as pd
import numpy as np


class CustomerDataPipeline:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.cleaned_df = None
        self.summary = {}

    # 1. Validate CSV file
    def validate_file(self):
        if not isinstance(self.file_path, str):
            raise ValueError("File path must be a string.")

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(
                f"CSV file does not exist: {self.file_path}"
            )

        if not self.file_path.lower().endswith(".csv"):
            raise ValueError("Only CSV files are supported.")

        print("File validation successful.")

    # 2. Load CSV
    def load_data(self):
        self.df = pd.read_csv(self.file_path)

        print("\n--- CSV DATA LOADED ---")
        print(self.df)

        return self.df

    # 3. Validate required columns
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
            column
            for column in required_columns
            if column not in self.df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Required columns are missing: {missing_columns}"
            )

        print("\nColumn validation successful.")

    # 4. Inspect dataset
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

    # 5. Generate data quality report
    def generate_quality_report(self):

        print("\n" + "=" * 50)
        print("DATA QUALITY REPORT")
        print("=" * 50)

        total_rows = len(self.df)

        report = pd.DataFrame({
            "Data Type": self.df.dtypes.astype(str),
            "Missing Count": self.df.isnull().sum(),
            "Missing Percentage":
                (self.df.isnull().sum() / total_rows) * 100,
            "Unique Values": self.df.nunique()
        })

        print(report)

        self.summary["quality_report"] = report

        return report

    # 6. Find duplicates
    def find_duplicates(self):

        duplicates = self.df[self.df.duplicated()]

        print("\n" + "=" * 50)
        print("DUPLICATE RECORDS")
        print("=" * 50)

        print(duplicates)
        print("\nDuplicate Count:", len(duplicates))

        return duplicates

    # 7. Remove duplicates
    def remove_duplicates(self):

        self.cleaned_df = self.df.drop_duplicates().copy()

        print("\nDuplicates removed.")
        print("Rows before:", len(self.df))
        print("Rows after:", len(self.cleaned_df))

        return self.cleaned_df

    # 8. Handle missing values
    def handle_missing_values(self):

        numerical_columns = [
            "Age",
            "Income",
            "PurchaseAmount"
        ]

        print("\n" + "=" * 50)
        print("MEDIAN IMPUTATION")
        print("=" * 50)

        for column in numerical_columns:

            missing_before = self.cleaned_df[column].isnull().sum()

            if missing_before > 0:

                median_value = self.cleaned_df[column].median()

                self.cleaned_df[column] = (
                    self.cleaned_df[column].fillna(median_value)
                )

                print(
                    f"{column}: {missing_before} missing values "
                    f"filled with median = {median_value}"
                )

        return self.cleaned_df

    # 9. Validate cleaned data
    def validate_cleaned_data(self):

        print("\n" + "=" * 50)
        print("CLEANED DATA VALIDATION")
        print("=" * 50)

        # Missing values
        total_missing = self.cleaned_df.isnull().sum().sum()

        # Duplicate values
        duplicate_count = self.cleaned_df.duplicated().sum()

        # Purchased values
        purchased_values = set(
            self.cleaned_df["Purchased"].dropna().unique()
        )

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
            raise ValueError(
                "Purchased column must contain only 0 or 1."
            )

        print("\nCleaned data validation successful.")

    # 10. Detect invalid values
    def detect_invalid_values(self):

        print("\n" + "=" * 50)
        print("INVALID VALUE DETECTION")
        print("=" * 50)

        invalid_age = self.cleaned_df[
            self.cleaned_df["Age"] <= 0
        ]

        invalid_income = self.cleaned_df[
            self.cleaned_df["Income"] < 0
        ]

        invalid_experience = self.cleaned_df[
            self.cleaned_df["Experience"] < 0
        ]

        invalid_purchase = self.cleaned_df[
            self.cleaned_df["PurchaseAmount"] < 0
        ]

        invalid_target = self.cleaned_df[
            ~self.cleaned_df["Purchased"].isin([0, 1])
        ]

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

    # 11. Create features
    def create_features(self):

        # Handle Experience = 0
        self.cleaned_df["IncomePerExperience"] = np.where(
            self.cleaned_df["Experience"] == 0,
            0,
            self.cleaned_df["Income"] /
            self.cleaned_df["Experience"]
        )

        # Purchase Category
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

    # 12. Create age group
    def create_age_group(self):

        self.cleaned_df["AgeGroup"] = np.select(
            [
                self.cleaned_df["Age"] < 30,
                (self.cleaned_df["Age"] >= 30) &
                (self.cleaned_df["Age"] <= 40),
                self.cleaned_df["Age"] > 40
            ],
            [
                "Young",
                "Adult",
                "Senior"
            ],
            default="Unknown"
        )

        print("\nAge groups created.")

        return self.cleaned_df

    # 13. High value customers
    def get_high_value_customers(self):

        result = self.cleaned_df[
            self.cleaned_df["PurchaseAmount"] > 5000
        ]

        print("\n" + "=" * 50)
        print("HIGH VALUE CUSTOMERS")
        print("=" * 50)

        print(result)

        return result

    # 14. Sort by purchase amount
    def sort_by_purchase_amount(self):

        result = self.cleaned_df.sort_values(
            by="PurchaseAmount",
            ascending=False
        )

        print("\n" + "=" * 50)
        print("SORTED BY PURCHASE AMOUNT")
        print("=" * 50)

        print(result)

        return result

    # 15. Calculate statistics
    def calculate_statistics(self):

        columns = [
            "Age",
            "Income",
            "Experience",
            "PurchaseAmount",
            "IncomePerExperience"
        ]

        statistics = self.cleaned_df[columns].agg(
            [
                "mean",
                "median",
                "min",
                "max",
                "std"
            ]
        )

        print("\n" + "=" * 50)
        print("STATISTICS")
        print("=" * 50)

        print(statistics)

        return statistics

    # 16. Calculate correlation
    def calculate_correlation(self):

        columns = [
            "Age",
            "Income",
            "Experience",
            "PurchaseAmount",
            "Purchased"
        ]

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

    # 17. Group by purchase status
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

    # 18. Perform EDA
    def perform_eda(self):

        total_customers = len(self.cleaned_df)

        average_age = self.cleaned_df["Age"].mean()
        average_income = self.cleaned_df["Income"].mean()
        median_income = self.cleaned_df["Income"].median()

        highest_purchase = self.cleaned_df[
            "PurchaseAmount"
        ].max()

        average_purchase = self.cleaned_df[
            "PurchaseAmount"
        ].mean()

        purchasers = (
            self.cleaned_df["Purchased"] == 1
        ).sum()

        non_purchasers = (
            self.cleaned_df["Purchased"] == 0
        ).sum()

        most_common_age_group = (
            self.cleaned_df["AgeGroup"].mode()[0]
        )

        most_common_purchase_category = (
            self.cleaned_df["PurchaseCategory"].mode()[0]
        )

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
        print(
            "Most Common Purchase Category:",
            most_common_purchase_category
        )

    # 19. Export cleaned data
    def export_clean_data(self):

        output_folder = "output"

        os.makedirs(output_folder, exist_ok=True)

        output_file = os.path.join(
            output_folder,
            "cleaned_customer_data.csv"
        )

        self.cleaned_df.to_csv(
            output_file,
            index=False
        )

        print("\n" + "=" * 50)
        print("EXPORT")
        print("=" * 50)

        print("Cleaned dataset exported to:")
        print(output_file)

        return output_file

    # 20. Bonus: ML Ready Data
    def generate_ml_ready_data(self):

        feature_columns = [
            "Age",
            "Income",
            "Experience",
            "PurchaseAmount",
            "IncomePerExperience"
        ]

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

    # 21. Complete Pipeline
    def run_pipeline(self):

        print("\n")
        print("=" * 60)
        print("       CUSTOMER DATA CSV PIPELINE")
        print("=" * 60)

        # Validate file
        self.validate_file()

        # Load CSV
        self.load_data()

        # Validate columns
        self.validate_columns()

        # Inspect
        self.inspect_dataset()

        # Quality report
        self.generate_quality_report()

        # Find duplicates
        self.find_duplicates()

        # Remove duplicates
        self.remove_duplicates()

        # Handle missing values
        self.handle_missing_values()

        # Validate cleaned data
        self.validate_cleaned_data()

        # Detect invalid values
        self.detect_invalid_values()

        # Feature engineering
        self.create_features()

        # Age group
        self.create_age_group()

        # High-value customers
        self.get_high_value_customers()

        # Sorting
        self.sort_by_purchase_amount()

        # Statistics
        self.calculate_statistics()

        # Correlation
        self.calculate_correlation()

        # Group analysis
        self.analyze_by_purchase_status()

        # EDA
        self.perform_eda()

        # ML-ready data
        self.generate_ml_ready_data()

        # Export
        self.export_clean_data()

        print("\n")
        print("=" * 60)
        print("          PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)


# ---------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------

def main():

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


# Entry Point
if __name__ == "__main__":
    main()