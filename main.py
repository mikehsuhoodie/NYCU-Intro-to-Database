from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
import hashlib #hashing password

import os


os.chdir(os.path.dirname(__file__))


# Flask App Initialization
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration
# db_config = {
#     'host': 'localhost',  # Change this to your MySQL host
#     'user': 'root',  # Change this to your MySQL username
#     'password': '1234',  # Change this to your MySQL password
#     'database': 'FinalProject'  # Change this to your MySQL database name
# }

# Database Configuration on MikeHsu's PC 
db_config = {
    'host': 'localhost',  # Change this to your MySQL host
    'user': 'root',  # Change this to your MySQL username
    'password': '153648mike',  # Change this to your MySQL password
    'database': 'FinalProject'  # Change this to your MySQL database name
}



# Database Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Main page
@app.route("/", methods=["GET"])
def main():
    is_logged_in = 'username' in session 
    username = session.get('username') 
    return render_template('main.html', is_logged_in=is_logged_in,username=username)
# Search Page
@app.route('/search_results', methods=['POST'])
def search():
    description = request.form.get('search')

    # Read the SQL script
    with open('search_script.sql', 'r', encoding='utf8') as searchfile:
        sql_script = searchfile.read()

    sql_script = sql_script.replace(
        "SET @inputDescription = 'Belvedere Vodka';",
        "SET @inputDescription = %s;"
    )

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    results = []

    try:
        for statement in sql_script.split(';'):
            if statement.strip(): # ensure statement is non-empty.
                if "SET @inputDescription" in statement:
                    # statement=> SET @inputDescription = %s;
                    # description=> a search term from user
                    cursor.execute(statement, (description,)) #  parameterized input
                else:
                    cursor.execute(statement)

        results = cursor.fetchall()
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return render_template('search_results.html', search_term=description, results=results)

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        #create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # TODO # 4: Hash the password using SHA-256
        hash_password=hashlib.sha256(password.encode()).hexdigest()
        
        # TODO # 2. Check if the user exists in the database and whether the password is correct
        # Query to check the user
        cursor.execute("SELECT * FROM users WHERE username = %s AND password= %s",(username,hash_password))
        result = cursor.fetchone() # fetchone() returns None if no record is found

        if result:
            # password matches
            session['loggedin']=True
            session['username']=result[1]
            next_url = session.pop('next', '/')
            cursor.close()
            conn.close()
            return redirect(next_url)
        else:
            # failed match
            flash("Invalid username or password", "danger")
        
        # Close the connection
        cursor.close()
        conn.close()
    if 'next' not in session and request.referrer:
        session['next'] = request.referrer
    return render_template("login.html")

# discussion Page
@app.route('/discussion')
def discussion():

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('discussion.html', posts=posts)

#discussion page - add post
@app.route('/discussion/add', methods=['POST'])
def add_post():
    if 'username' not in session:
        return redirect("/login")
    title = request.form['title']
    content = request.form['content']
    usname = session['username']
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO posts (title, content,username) VALUES (%s, %s, %s)", (title, content,usname))
        conn.commit()
        flash('Post added successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect("/discussion")

#discussion page - edit post
@app.route('/discussion/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    if 'username' not in session:
        return redirect("/login")
    
    conn = None
    cur = None

    try:
        # Establish database connection
        conn = get_db_connection()
        cur = conn.cursor()
        
        if request.method == 'POST':
            # Handle POST request (update post)
            title = request.form['title']
            content = request.form['content']
            
            cur.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s", (title, content, id))
            conn.commit()
            
            flash('Post updated successfully!', 'success')
            return redirect("/discussion")
        else:# Handle GET 
            cur.execute("SELECT * FROM posts WHERE id = %s", (id,))
            post = cur.fetchone()

            if not post:
                flash("Post not found!", "danger")
                return redirect("/discussion")
            return render_template('edit_post.html', post=post)
        
    except mysql.connector.Error as db_error:
        flash(f"Database error: {str(db_error)}", "danger")
    except Exception as e:
        flash(f"Unexpected error: {str(e)}", "danger")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return redirect("/discussion")


#discussion page - delete post
@app.route('/discussion/delete/<int:id>', methods=['POST'])
def delete_post(id):
    if 'username' not in session:
        return redirect("/login")
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM posts WHERE id = %s", (id,))
        conn.commit()
        flash('Post deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect("/discussion")




# about us Page
@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


# Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        # TODO # 4: Hash the password using SHA-256
        hash_password = hashlib.sha256(password.encode()).hexdigest()

        # TODO # 3: Add the query to insert a new user into the database
        try:
            # Insert new user into the database
            cursor.execute('SELECT * FROM users WHERE username = %s AND password= %s',(username,hash_password,))
            result=cursor.fetchone()

            cursor.execute('INSERT INTO users (username,password) VALUES (%s,%s)',(username,hash_password,))
            conn.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect("/login")
        except mysql.connector.Error as err:
            flash(f"The account already exists.", "danger")
        finally:
            cursor.close()
            conn.close()
    
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
