import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk

# Function to load a CSV file
def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        messagebox.showinfo("Success", "CSV file loaded successfully.")
        return df
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
        return None
    except pd.errors.EmptyDataError:
        messagebox.showerror("Error", "The file is empty.")
        return None
    except pd.errors.ParserError:
        messagebox.showerror("Error", "The file could not be parsed.")
        return None

# Show a summary of the data
def show_summary(df):
    summary_window = tk.Toplevel()
    summary_window.title("File Summary")
    text = tk.Text(summary_window, wrap='word')
    text.insert('1.0', str(df.describe()) + "\n" + str(df.info()))
    text.pack(expand=True, fill='both')

# Show the first rows of the file
def show_data(df, num_rows=5):
    data_window = tk.Toplevel()
    data_window.title("First Rows of the File")
    text = tk.Text(data_window, wrap='word')
    text.insert('1.0', str(df.head(num_rows)))
    text.pack(expand=True, fill='both')

# Filter data by column and value
def filter_data(df, column, value):
    filtered_df = df[df[column] == value]
    return filtered_df

# Filter data by a range of values
def filter_range(df, column, min_value, max_value):
    filtered_df = df[(df[column] >= min_value) & (df[column] <= max_value)]
    return filtered_df

# Sort data by a column
def sort_data(df, column, ascending=True):
    sorted_df = df.sort_values(by=column, ascending=ascending)
    return sorted_df

# Drop rows with null values
def drop_nulls(df):
    df_no_nulls = df.dropna()
    return df_no_nulls

# Fill null values with a specific value
def fill_nulls(df, column, value):
    df[column] = df[column].fillna(value)
    return df

# Data visualization with different types of plots
def visualize_data(df, plot_type, column_x, column_y=None):
    if plot_type == 'histogram':
        plt.figure(figsize=(10, 6))
        sns.histplot(df[column_x], kde=True)
        plt.title('Histogram of {}'.format(column_x))
    elif plot_type == 'scatter' and column_y:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=column_x, y=column_y, data=df)
        plt.title('Scatter Plot of {} vs {}'.format(column_x, column_y))
    elif plot_type == 'bar':
        plt.figure(figsize=(10, 6))
        sns.countplot(x=column_x, data=df)
        plt.title('Bar Plot of {}'.format(column_x))
    elif plot_type == 'box':
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=column_x, data=df)
        plt.title('Box Plot of {}'.format(column_x))
    elif plot_type == 'heatmap' and column_y:
        plt.figure(figsize=(10, 6))
        pivot_table = df.pivot_table(values=column_y, index=column_x, aggfunc=np.mean)
        sns.heatmap(pivot_table, annot=True, cmap='coolwarm')
        plt.title('Heatmap of {} vs {}'.format(column_x, column_y))
    else:
        messagebox.showerror("Error", "Unsupported plot type or column y not specified.")
        return
    plt.show()

# Save the modified DataFrame to a new CSV file
def save_csv(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Success", "CSV file saved successfully to {}".format(file_path))
    except Exception as e:
        messagebox.showerror("Error", "Error saving the file: {}".format(e))

# Create a new CSV file
def create_csv():
    columns = simpledialog.askstring("Input", "Enter column names separated by commas:")
    if columns:
        columns_list = [col.strip() for col in columns.split(',')]
        num_rows = simpledialog.askinteger("Input", "Enter number of rows:")
        if num_rows is not None:
            data = {col: ["" for _ in range(num_rows)] for col in columns_list}
            df = pd.DataFrame(data)
            save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if save_path:
                save_csv(df, save_path)

# GUI Interface
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        global data
        data = load_csv(file_path)

def show_summary_gui():
    if data is not None:
        show_summary(data)
    else:
        messagebox.showerror("Error", "No data loaded.")

def show_data_gui():
    if data is not None:
        num_rows = simpledialog.askinteger("Input", "Enter number of rows to display:")
        if num_rows is not None:
            show_data(data, num_rows)
    else:
        messagebox.showerror("Error", "No data loaded.")

def visualize_data_gui():
    if data is not None:
        plot_type = simpledialog.askstring("Input", "Enter plot type (histogram, scatter, bar, box, heatmap):")
        column_x = simpledialog.askstring("Input", "Enter column for x-axis:")
        column_y = None
        if plot_type == 'scatter' or plot_type == 'heatmap':
            column_y = simpledialog.askstring("Input", "Enter column for y-axis:")
        visualize_data(data, plot_type, column_x, column_y)
    else:
        messagebox.showerror("Error", "No data loaded.")

def save_csv_gui():
    if data is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            save_csv(data, file_path)
    else:
        messagebox.showerror("Error", "No data loaded.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("CSV Data Viewer")
    root.geometry("400x400")

    data = None

    open_button = ttk.Button(root, text="Open CSV File", command=open_file)
    open_button.pack(pady=10)

    create_button = ttk.Button(root, text="Create CSV File", command=create_csv)
    create_button.pack(pady=10)

    summary_button = ttk.Button(root, text="Show Summary", command=show_summary_gui)
    summary_button.pack(pady=10)

    data_button = ttk.Button(root, text="Show Data", command=show_data_gui)
    data_button.pack(pady=10)

    visualize_button = ttk.Button(root, text="Visualize Data", command=visualize_data_gui)
    visualize_button.pack(pady=10)

    save_button = ttk.Button(root, text="Save CSV File", command=save_csv_gui)
    save_button.pack(pady=10)

    root.mainloop()