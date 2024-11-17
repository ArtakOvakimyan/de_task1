import requests


API_URL = "https://jsonplaceholder.typicode.com/users"

def fetch_users():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }

    response = requests.get(API_URL, headers)
    response.raise_for_status()
    data = response.json()
    users = response.json()
    return users

def generate_html(users):
    html_content = '''
    <html>
    <head>
        <title>Users List</title>
        <style>
            table {
                width: 50%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h1>Users List</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
            </tr>
    '''

    for user in users:
        html_content += f'''
            <tr>
                <td>{user['id']}</td>
                <td>{user['name']}</td>
                <td>{user['email']}</td>
                <td>{user['phone']}</td>
            </tr>
        '''

    html_content += '''
        </table>
        </body>
        </html>
    '''

    return html_content

def save_html(html_content, filename='6_res.html'):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html_content)


if __name__ == '__main__':
    users = fetch_users()
    html_content = generate_html(users)
    save_html(html_content)
