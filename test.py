import pandas as pd

def func():
# Create a DataFrame with your data
    data = {
        'name': ['John', 'Anna'],
        'year': [2025, 2026],
        'number': [101, 102],
        'grade': ['A', 'B'],
        'priceone': [20.5, 22.5],
        'pricetwo': [25.5, 28.5]
    }
    df = pd.DataFrame(data)

    # Path to your Excel file
    file_path = 'test.xlsx'

    # Use pandas ExcelWriter with mode='a' to append the data
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)

func()
func()

print("Data appended successfully!")
