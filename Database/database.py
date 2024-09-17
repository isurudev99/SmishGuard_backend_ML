import sqlite3
from urllib.parse import urlparse

conn = sqlite3.connect('Database/database.db')
cursor = conn.cursor()


def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    if not domain:
        domain = parsed_url.netloc
    return domain


# # Create the "domains" table if it doesn't exist
# cursor.execute('''CREATE TABLE IF NOT EXISTS domains
#                   (URL TEXT, 
#                   value INTEGER)''')

# # ================add phishing values to database=========================
# # Read URLs from a text file and insert them into the table
# with open('urls.txt', 'r') as file:
#     for url in file:
#         url = url.strip()  # Remove leading/trailing whitespace
#         if url:  # Skip empty lines
#             cursor.execute("INSERT INTO domains (URL, value) VALUES (?, ?)", (url, 1))

# # # ================add legitimate values to database=========================
# with open('legitimatedomains.txt', 'r', encoding='cp1252') as file:
#     for url in file:
#         url = url.strip()  # Remove leading/trailing whitespace
#         if url:  # Skip empty lines
#             cursor.execute("INSERT INTO domains (URL, value) VALUES (?, ?)", (url, 0))


# # Execute the query to search for the URL
# cursor.execute('SELECT * FROM domains WHERE value = 0 AND URL = ?', (search_url,))
# row = cursor.fetchall()

# # cursor.execute("SELECT * FROM domains")
# # rows = cursor.fetchall()

# for row in row:
#     print(row)


def databaseSearch(search_url):
    url = extract_domain(search_url)
    print(url)
    # call to the function for extract the domain name from URL

    # Execute the query to search for the URL
    cursor.execute("SELECT value FROM domains WHERE URL=?", (url,))
    row = cursor.fetchone()

    # Check if the URL was found and retrieve its value
    if row is not None:
        value = row[0]
        print(f"The value of URL '{search_url}' is {value}")
        return value
    else:
        print(f"The URL '{search_url}' was not found in the table")
        return None


# Commit the changes and close the connection
conn.commit()


# conn.close()

def close_connection():
    conn.close()
    print("Database Connection Closed")


# # Specify the URL to search
# search_url = "https://www.courseweb.sliit.lk"
# output = databaseSearch(search_url)
# print(output)
# close_connection()
