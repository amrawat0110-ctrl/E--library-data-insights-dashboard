import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class LibraryDashboard:
    REQUIRED_COLUMNS = ["Transaction ID", "Date", "User ID", "Book Title", "Genre", "Borrowing Duration (Days)"]

    def __init__(self):
        self.df = None
        self.file_path = "library_transactions.csv"

    def load_data(self):

        try:
            self.df = pd.read_csv(self.file_path) 
            
        except FileNotFoundError:
            print("ERROR: File not found.")
            return False

        missing = [c for c in self.REQUIRED_COLUMNS if c not in self.df.columns]
        if missing:
            print("ERROR: Missing columns:", missing)
            return False

        self.df["Date"] = pd.to_datetime(self.df["Date"], errors="coerce")
        self.df["Borrowing Duration (Days)"] = pd.to_numeric(
            self.df["Borrowing Duration (Days)"], errors="coerce"
        )
        return True 

        missing_values = int(self.df.isnull().sum().sum())
        duplicate_rows = int(self.df.duplicated().sum())
        self.df = self.df.dropna().drop_duplicates()
        self.df = self.df[self.df["Borrowing Duration (Days)"] > 0].copy()

        print("\n" + "=" * 60)
        print("DATA LOADED SUCCESSFULLY")
        print("=" * 60)
        print("Total valid transactions :", len(self.df))
        print("Missing values found     :", missing_values)
        print("Duplicate rows removed   :", duplicate_rows)
        return True

    def show_data(self):
        print("\nFIRST 10 RECORDS")
        print(self.df.head(10).to_string(index=False))

    def calculate_statistics(self):
        durations = np.array(self.df["Borrowing Duration (Days)"])
        book_counts = self.df["Book Title"].value_counts()
        daily_counts = self.df["Date"].dt.date.value_counts()

        print("\n" + "=" * 60)
        print("LIBRARY STATISTICS")
        print("=" * 60)
        print("Most borrowed book      :", book_counts.idxmax())
        print("Times borrowed          :", int(book_counts.max()))
        print(f"Average borrowing time  : {np.mean(durations):.2f} days")
        print(f"Standard deviation      : {np.std(durations):.2f} days")
        print("Minimum duration        :", int(np.min(durations)), "days")
        print("Maximum duration        :", int(np.max(durations)), "days")
        print("Busiest borrowing date  :", daily_counts.idxmax())
        print("Transactions that day   :", int(daily_counts.max()))

        print("\nBorrowings by Genre:")
        print(self.df.groupby("Genre").size().sort_values(ascending=False))
        print("\nAverage Duration by Genre:")
        print(self.df.groupby("Genre")["Borrowing Duration (Days)"].mean().round(2))

    def filter_transactions(self, condition):
        filtered = self.df.copy()

        if condition.get("genre"):
            filtered = filtered[
                filtered["Genre"].str.lower() == condition["genre"].lower()
            ]
        if condition.get("start_date"):
            filtered = filtered[filtered["Date"] >= pd.to_datetime(condition["start_date"])]
        if condition.get("end_date"):
            filtered = filtered[filtered["Date"] <= pd.to_datetime(condition["end_date"])]
        if condition.get("min_duration") is not None:
            filtered = filtered[
                filtered["Borrowing Duration (Days)"] >= condition["min_duration"]
            ]
        if condition.get("max_duration") is not None:
            filtered = filtered[
                filtered["Borrowing Duration (Days)"] <= condition["max_duration"]
            ]
        return filtered

    def generate_report(self):
        report = pd.DataFrame({
            "Metric": ["Total Transactions", "Unique Users", "Unique Books",
                       "Average Borrowing Duration", "Most Borrowed Book"],
            "Value": [len(self.df), self.df["User ID"].nunique(),
                      self.df["Book Title"].nunique(),
                      f'{self.df["Borrowing Duration (Days)"].mean():.2f} days',
                      self.df["Book Title"].value_counts().idxmax()]
        })
        print("\nSUMMARY REPORT")
        print(report.to_string(index=False))
        report.to_csv("library_summary_report.csv", index=False)
        print("\nReport saved as: library_summary_report.csv")

    def create_visualizations(self):
        top_books = self.df["Book Title"].value_counts().head(5)
        plt.figure(figsize=(10, 6))
        top_books.plot(kind="bar")
        plt.title("Top 5 Most Borrowed Books")
        plt.xlabel("Book Title")
        plt.ylabel("Borrowings")
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        plt.savefig("top_5_books.png")
        plt.show()

        temp = self.df.copy()
        temp["Month"] = temp["Date"].dt.to_period("M").astype(str)
        monthly = temp.groupby("Month").size()
        plt.figure(figsize=(10, 6))
        plt.plot(monthly.index, monthly.values, marker="o")
        plt.title("Borrowing Trends Over Months")
        plt.xlabel("Month")
        plt.ylabel("Borrowings")
        plt.tight_layout()
        plt.savefig("borrowing_trends.png")
        plt.show()

        genre = self.df["Genre"].value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(genre.values, labels=genre.index, autopct="%1.1f%%")
        plt.title("Books Borrowed by Genre")
        plt.tight_layout()
        plt.savefig("genre_distribution.png")
        plt.show()

        heat = self.df.copy()
        heat["Day"] = heat["Date"].dt.day_name()
        heat["Week"] = heat["Date"].dt.isocalendar().week.astype(int)
        table = pd.crosstab(heat["Day"], heat["Week"])
        plt.figure(figsize=(12, 6))
        sns.heatmap(table, annot=True, fmt="d")
        plt.title("Borrowing Activity by Day and Week")
        plt.tight_layout()
        plt.savefig("borrowing_heatmap.png")
        plt.show()

        print("\nGraphs saved successfully.")

def main():
    file_path = "library_transactions.csv"

    dashboard = LibraryDashboard() 
class LibraryDashboard:
    REQUIRED_COLUMNS = ['Transaction ID', 'User ID', 'Book ID', 'Borrow Date', 'Return Date', 'Status', 'Date', 'Borrowing Duration (Days)']

    def load_data(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
            print("\nCSV file loaded successfully.")
        except FileNotFoundError:
            print(f"ERROR: File not found at {file_path}")
            return False
        
        missing = [c for c in self.REQUIRED_COLUMNS if c not in self.df.columns]
        if missing:
            print("ERROR: Missing columns:", missing)
            return False
        
        self.df["Date"] = pd.to_datetime(self.df["Date"], errors="coerce")
        self.df["Borrowing Duration (Days)"] = pd.to_numeric(
            self.df["Borrowing Duration (Days)"], errors="coerce"
        )
        return True

def main():
    file_path = r"C:\Users\Armin Khareghat\OneDrive\Desktop\AI ML data science\Python\python-projects\E- Library data insights dashboard \library_transactions.csv"
    dashboard = LibraryDashboard()
    if not dashboard.load_data(file_path):
        return
    
    while True:
        print("\n1. View Dataset")
        print("2. Calculate Statistics")
        print("3. Filter Transactions")
        print("4. Generate Summary Report")
        print("5. Create Visualizations")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()

def bar_chart_top_books(self):
    top_books = self.df["Book Title"].value_counts().head(5)

plt.figure(figsize=(10, 6))
top_books.plot(kind="bar")
plt.title("Top 5 Most Borrowed Books")
plt.xlabel("Book Title")
plt.ylabel("Borrowings")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.show()  

def line_chart_borrowing_trends(self):
    temp = self.df.copy()
temp["Month"] = temp["Date"].dt.to_period("M").astype(str)

monthly = temp.groupby("Month").size()

plt.figure(figsize=(10, 6))
plt.plot(monthly.index, monthly.values, marker="o")
plt.title("Borrowing Trends Over Months")
plt.xlabel("Month")
plt.ylabel("Borrowings")
plt.tight_layout()
plt.show()

def pie_chart_genre_distribution(self):
    genre = self.df["Genre"].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(
    genre.values,
    labels=genre.index,
    autopct="%1.1f%%"
)

plt.title("Books Borrowed by Genre")
plt.tight_layout()
plt.show()

def heatmap_borrowing_activity(self):
    heat = self.df.copy()

heat["Day"] = heat["Date"].dt.day_name()
heat["Week"] = heat["Date"].dt.isocalendar().week.astype(int)

table = pd.crosstab(
    heat["Day"],
    heat["Week"]
)

plt.figure(figsize=(12, 6))

sns.heatmap(
    table,
    annot=True,
    fmt="d"
)

plt.title("Borrowing Activity by Day and Week")
plt.tight_layout()
plt.show()


if __name__ == "__main__":
    main()