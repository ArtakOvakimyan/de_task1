import pandas as pd

def main(input_file, output_file, results_file):
    df = pd.read_csv(input_file, sep=',')

    if 'category' in df.columns:
        df.drop(columns=['category'], inplace=True)

    average_rating = df['rating'].mean()
    max_price = df['price'].max()
    min_quantity = df['quantity'].min()

    filtered_df = df[df['category'] != 'Напитки'] if 'category' in df.columns else df
    filtered_df.to_csv(output_file, index=False)

    with open(results_file, 'w') as f:
        f.write(f"{average_rating}\n")
        f.write(f"{max_price}\n")
        f.write(f"{min_quantity}")

if __name__ == '__main__':
    input_file = './data/fourth_task.txt'
    output_file = './4_modified_18.csv'
    results_file = './4_result_18.txt'
    main(input_file, output_file, results_file)
