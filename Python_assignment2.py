import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    return pd.read_excel(file_path)

def rename_columns(data_frame):
    new_df = data_frame.rename(columns=str.lower)
    return new_df.rename(columns={'min delay': 'min_delay', 'min gap': 'min_gap'})

def convert_data_types(data_frame):
    data_frame[['incident', 'day', 'direction']] = data_frame[['incident', 'day', 'direction']].astype('category')
    return data_frame

def create_derived_column(data_frame):
    data_frame['seconds_delay'] = data_frame['min_delay'].astype('int64') * 60
    return data_frame.drop(['min_delay'], axis=1)

def create_subset_loc(data_frame, condition):
    return data_frame.loc[condition]

def create_subset_query(data_frame, condition):
    return data_frame.query(condition)

def create_dataframe_with_nans(data_frame):
    return data_frame[data_frame.isnull().any(axis=1)]

def create_dataframe_subset_nans(data_frame, subset_columns):
    subset_columns_exist = all(col in data_frame.columns for col in subset_columns)

    if subset_columns_exist:
        condition = data_frame[subset_columns].isnull().any(axis=1)
        return data_frame[condition]
    else:
        print(f"Columns {subset_columns} do not exist in the DataFrame.")
        return pd.DataFrame()  # Return an empty DataFrame or handle it as per your requirement

def drop_records_with_nans(data_frame, columns):
    return data_frame.dropna(subset=columns)

def group_and_plot(data_frame, group_column, value_column):
    grouped_data = data_frame.groupby(group_column).agg({value_column: 'mean'}).reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=group_column, y=value_column, data=grouped_data, palette='viridis')
    plt.xlabel(f'{group_column} Type')
    plt.ylabel(f'Average {value_column} (seconds)')
    plt.title(f'Average {value_column} for Each {group_column} Type')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    
    # Save the plot as a .png file
    plt.savefig(f'average_{value_column}_plot.png')

def save_to_csv(data_frame, file_name):
    data_frame.to_csv(file_name, index=False)

# Example usage:

file_path = "ttc-bus-delay-data-2023.xlsx"
df = load_data(file_path)

# Processing steps
df = rename_columns(df)
df = convert_data_types(df)
df = create_derived_column(df)

# Example usage of functions
subset_loc = create_subset_loc(df, df['direction'].isna())
subset_query = create_subset_query(df, 'seconds_delay > 6000')

df_with_nans = create_dataframe_with_nans(df)
df_subset_nans = create_dataframe_subset_nans(df, ['Route', 'Direction'])

df_no_nans = drop_records_with_nans(df, ['route', 'direction'])

group_and_plot(df, 'incident', 'seconds_delay')

# Save DataFrames to CSV
save_to_csv(df, 'Dhanani_Nihar_python_assignment2_proc.csv')
save_to_csv(df_with_nans, 'df_with_nans.csv')
save_to_csv(df_subset_nans, 'df_subset_nans.csv')
