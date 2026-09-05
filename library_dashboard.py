import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

class LibraryDashboard:
    def __init__(self):
        self.df = None

    def load_data(self, file_path):
        """Load and validate the dataset using Pandas and Control Structures."""
        if not os.path.exists(file_path):
            print(f"Error: The file '{file_path}' was not found.")
            return False

        try:
            self.df = pd.read_csv(file_path)
            
            # Control Structure & Arrays: Validate columns
            expected_columns = ['Transaction ID', 'Date', 'User ID', 'Book Title', 'Genre', 'Borrowing Duration (Days)']
            for col in expected_columns:
                if col not in self.df.columns:
                    print(f"Error: Missing expected column '{col}' in CSV.")
                    return False

            # Handle missing data using Pandas/Control logic
            initial_rows = len(self.df)
            self.df.dropna(inplace=True)
            self.df.drop_duplicates(inplace=True)
            
            # Convert Date to datetime format
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            print(f"Success: Loaded {len(self.df)} valid records (Cleaned {initial_rows - len(self.df)} invalid/duplicate rows).")
            return True

        except Exception as e:
            print(f"An error occurred while loading data: {e}")
            return False

    def calculate_statistics(self):
        """Calculate metrics like most borrowed book, average borrowing time, and standard deviation using NumPy & Pandas."""
        if self.df is None or self.df.empty:
            print("Dataset is empty or not loaded.")
            return

        # Pandas aggregation for most borrowed book
        most_borrowed = self.df['Book Title'].mode()[0]
        
        # NumPy integration for statistics on borrowing duration
        durations = self.df['Borrowing Duration (Days)'].to_numpy()
        avg_duration = np.mean(durations)
        std_duration = np.std(durations)

        print("\n--- Library Usage Statistics ---")
        print(f"Most Borrowed Book: {most_borrowed}")
        print(f"Average Borrowing Duration: {avg_duration:.2f} days")
        print(f"Standard Deviation of Duration: {std_duration:.2f} days")

    def filter_transactions(self, genre=None, min_duration=None):
        """Filter transactions based on user-defined criteria like genre or duration."""
        if self.df is None:
            print("Dataset not loaded.")
            return None

        filtered_df = self.df.copy()
        
        if genre:
            filtered_df = filtered_df[filtered_df['Genre'].str.lower() == genre.lower()]
        if min_duration:
            filtered_df = filtered_df[filtered_df['Borrowing Duration (Days)'] >= min_duration]
            
        return filtered_df

    def generate_report(self):
        """Generate a summary report of the analysis."""
        if self.df is None:
            return
        
        print("\n--- Summary Report ---")
        print(f"Total Transactions: {len(self.df)}")
        print(f"Unique Users: {self.df['User ID'].nunique()}")
        print(f"Unique Books: {self.df['Book Title'].nunique()}")
        print(f"Genres Available: {', '.join(self.df['Genre'].unique())}")

    def generate_visualizations(self):
        """Create insightful visualizations using Matplotlib & Seaborn."""
        if self.df is None:
            return

        sns.set_theme(style="whitegrid")
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('E-Library Data Insights Dashboard', fontsize=16, fontweight='bold')

        # 1. Bar Chart: Top 5 most borrowed books
        top_books = self.df['Book Title'].value_counts().head(5)
        sns.barplot(x=top_books.values, y=top_books.index, ax=axes[0, 0], palette='viridis')
        axes[0, 0].set_title('Top 5 Most Borrowed Books')
        axes[0, 0].set_xlabel('Borrow Count')
        axes[0, 0].set_ylabel('Book Title')

        # 2. Line Graph: Borrowing trends over months
        self.df['Month'] = self.df['Date'].dt.to_period('M').astype(str)
        monthly_trends = self.df.groupby('Month').size()
        axes[0, 1].plot(monthly_trends.index, monthly_trends.values, marker='o', color='b', linestyle='-')
        axes[0, 1].set_title('Borrowing Trends Over Months')
        axes[0, 1].set_xlabel('Month')
        axes[0, 1].set_ylabel('Number of Borrowings')
        axes[0, 1].tick_params(axis='x', rotation=45)

        # 3. Pie Chart: Distribution of books borrowed by genre
        genre_dist = self.df['Genre'].value_counts()
        axes[1, 0].pie(genre_dist.values, labels=genre_dist.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
        axes[1, 0].set_title('Distribution of Books Borrowed by Genre')

        # 4. Heatmap/Countplot representation for activity
        sns.countplot(data=self.df, x='Genre', ax=axes[1, 1], palette='coolwarm')
        axes[1, 1].set_title('Borrowing Activity by Genre Count')
        axes[1, 1].set_xlabel('Genre')
        axes[1, 1].set_ylabel('Count')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

# Execution workflow
if __name__ == "__main__":
    dashboard = LibraryDashboard()
    
    # Load dataset
    file_name = "library_transactions.csv"
    if dashboard.load_data(file_name):
        dashboard.generate_report()
        dashboard.calculate_statistics()
        
        # Example Filter usage
        print("\nFiltering for 'Fiction' genre:")
        print(dashboard.filter_transactions(genre='Fiction'))
        
        # Generate graphs
        dashboard.generate_visualizations()
