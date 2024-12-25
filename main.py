from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
import hashlib #hashing password

# Flask App Initialization
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration
db_config = {
    'host': 'localhost',  # Change this to your MySQL host
    'user': 'root',  # Change this to your MySQL username
    'password': '1234',  # Change this to your MySQL password
    'database': 'final_project'  # Change this to your MySQL database name
}

# Database Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# main Page
@app.route("/")
def main():
    return render_template("main.html")

# homepage Page
@app.route("/main")
def homepage():
    return render_template("main.html")

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
            cursor.close()
            conn.close()
            return redirect("/")
        else:
            # failed match
            flash("Invalid username or password", "danger")
        
        # Close the connection
        cursor.close()
        conn.close()

    return render_template("login.html")

# discussion Page
@app.route("/discussion")
def discussion():
    if 'username' not in session:
        return redirect("/login")
    return render_template("discussion.html")

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
            flash(f"Error: {err}", "danger")
        finally:
            cursor.close()
            conn.close()
    
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
