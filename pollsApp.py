//To continue from where we left off, we need to modify and execute the SQL script to make it compatible with SQLite. The script involves several steps:

1. Cleaning the script to remove unsupported commands and replace incompatible syntax.
2. Creating an in-memory SQLite database.
3. Loading the data into the SQLite database.
4. Querying the database to find the summed total results for individual polling units in Delta State (state id: 25).

Given that I can't execute Python code right now, I'll guide you through the steps you can perform in your local Python environment.

### Step 1: Cleaning the SQL Script
The script needs to be modified to remove unsupported commands like `SET` and replace `AUTO_INCREMENT` with `AUTOINCREMENT`.

```python
import re

# Read the SQL file
with open('path_to_your_file/bincom_test.sql', 'r') as file:
    sql_content = file.read()

# Remove unsupported commands and replace incompatible syntax
cleaned_sql_content = re.sub(r'--.*?\n', '', sql_content)  # Remove comments
cleaned_sql_content = re.sub(r'/\*.*?\*/', '', cleaned_sql_content, flags=re.DOTALL)  # Remove multi-line comments
cleaned_sql_content = re.sub(r'\bSET\b.*?;', '', cleaned_sql_content, flags=re.IGNORECASE)  # Remove SET commands
cleaned_sql_content = re.sub(r'AUTO_INCREMENT', 'AUTOINCREMENT', cleaned_sql_content)

# Save cleaned SQL content if needed for verification
with open('path_to_your_file/cleaned_bincom_test.sql', 'w') as file:
    file.write(cleaned_sql_content)
```

### Step 2: Creating an In-Memory SQLite Database
Next, create an in-memory SQLite database and execute the cleaned SQL script.

```python
import sqlite3

# Create an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Execute the cleaned SQL script to create tables and populate them with data
cursor.executescript(cleaned_sql_content)

# List the tables to verify the structure
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(tables)
```

### Step 3: Querying the Database
To get the summed total results for individual polling units in Delta State (state id: 25), you can execute the following query:

```python
# Query to get the summed total results for polling units in Delta State (state id: 25)
query = """
SELECT pu.polling_unit_name, SUM(rs.party_score) as total_score
FROM polling_unit pu
JOIN announced_pu_results rs ON pu.uniqueid = rs.polling_unit_uniqueid
JOIN lga ON pu.lga_id = lga.lga_id
WHERE lga.state_id = 25
GROUP BY pu.polling_unit_name;
"""

# Execute the query and fetch results
cursor.execute(query)
results = cursor.fetchall()

# Print results
for row in results:
    print(row)
```

### Step 4: Creating a Web Page
To display the results on a web page, you can use a simple Flask application.

```python
from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.executescript(cleaned_sql_content)

    query = """
    SELECT pu.polling_unit_name, SUM(rs.party_score) as total_score
    FROM polling_unit pu
    JOIN announced_pu_results rs ON pu.uniqueid = rs.polling_unit_uniqueid
    JOIN lga ON pu.lga_id = lga.lga_id
    WHERE lga.state_id = 25
    GROUP BY pu.polling_unit_name;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Polling Unit Results</title>
    </head>
    <body>
        <h1>Summed Total Results for Polling Units in Delta State</h1>
        <table border="1">
            <tr>
                <th>Polling Unit Name</th>
                <th>Total Score</th>
            </tr>
            {% for row in results %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, results=results)

if __name__ == '__main__':
    app.run(debug=True)
```

//run it using://

//```bash//
//python app.py//
//```//

//You can then access the web page at `http://127.0.0.1:5000/` to see the summed total results for polling units in Delta State.//



            
