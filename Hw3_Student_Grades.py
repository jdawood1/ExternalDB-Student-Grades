import pandas as pd
import sqlite3


def prepare_student_data_file():
    """
    Creates StudentA_B_Data.csv with StudentA and StudentB scores.
    """
    data = {
        'Name': ['StudentA', 'StudentB'],
        'Quizzes': [85, 40],
        'Homework': [130, 100],
        'Team Project': [60, 50],
        'Final Exam': [80, 65]
    }
    df = pd.DataFrame(data)
    df.to_csv('StudentA_B_Data.csv', index=False)
    print("StudentA_B_Data.csv created successfully.")


def import_to_database(csv_file: str, db_file: str) -> None:
    """
    Imports data for Student1, Student2, and Student3 from a CSV file into an SQLite database.
    """
    try:
        df = pd.read_csv(csv_file)
        conn = sqlite3.connect(db_file)
        df.to_sql('Students', conn, if_exists='replace', index=False)
        conn.commit()
        conn.close()
        print(f"Data from {csv_file} imported to {db_file} successfully.")
    except Exception as e:
        print(f"Failed to import data: {e}")


def read_csv_file(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Data read from {file_path} successfully.")
        return df
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame()


def combine_data(db_file: str, csv_file: str) -> pd.DataFrame:
    """
    Combines data from an SQLite database and a CSV file into a DataFrame.
    """
    try:
        conn = sqlite3.connect(db_file)
        db_df = pd.read_sql_query("SELECT * FROM Students", conn)
        conn.close()

        csv_df = read_csv_file(csv_file)

        combined_df = pd.concat([db_df, csv_df], ignore_index=True)
        print("Data combined successfully.")
        return combined_df
    except Exception as e:
        print(f"Failed to combine data: {e}")
        return pd.DataFrame()


def calculate_final_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the final scores for all students based on the provided weights.
    """
    try:
        df['Final Score'] = (
                df['Quizzes'] * 0.2 +
                df['Homework'] * 0.3 +
                df['Team Project'] * 0.25 +
                df['Final Exam'] * 0.25
        )
        print("Final scores calculated successfully.")
        return df
    except Exception as e:
        print(f"Error calculating final scores: {e}")
        return df


def save_results(df: pd.DataFrame, output_file: str) -> None:
    """
    Saves the final results to a CSV file.
    """
    try:
        df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file} successfully.")
    except Exception as e:
        print(f"Failed to save results: {e}")


def main():
    """
    The main function, used to grab the data and pass it to
    your answer functions. You are not expected to edit this
    as part of the assignment. Feel free to edit it if needed
    while testing, but remember that the graders will be using
    this exact version when grading your answers.
    :return:
    """
    # File paths in the project directory
    first_csv_file = "Python-HW-WeightedSums-Data.csv"
    second_csv_file = "StudentA_B_Data.csv"
    db_file = "StudentData.db"

    try:
        prepare_student_data_file()
        import_to_database(first_csv_file, db_file)
        combined_data = combine_data(db_file, second_csv_file)
        final_results = calculate_final_scores(combined_data)
        save_results(final_results, "FinalStudentGrades.csv")

        # Display the final results
        print("Final Grades:\n")
        print(final_results.to_string(index=False))
    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found.")


# Execute the main function when the script is run
if __name__ == "__main__":
    main()

