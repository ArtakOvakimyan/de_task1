import pandas as pd
from bs4 import BeautifulSoup

def extract_table_from_html(html_file, output_csv):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')

    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip())

    data = []
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        cols = [elem.text.strip() for elem in cols]
        data.append(cols)

    df = pd.DataFrame(data, columns=headers)
    df.to_csv(output_csv, index=False)

if __name__ == '__main__':
    html_file = './data/fifth_task.html'
    output_csv = './5_res_18.csv'
    extract_table_from_html(html_file, output_csv)
