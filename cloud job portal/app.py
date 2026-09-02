from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "jobportal.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL,
            salary TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            resume TEXT NOT NULL
        )
    """)

    # Add sample jobs only if database is empty
    count = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]

    if count == 0:
        sample_jobs = [
            (
                "Python Developer",
                "Tech Solutions",
                "Chennai",
                "₹4 - ₹6 LPA",
                "Develop and maintain Python-based web applications."
            ),
            (
                "Frontend Developer",
                "Creative Technologies",
                "Bangalore",
                "₹3 - ₹5 LPA",
                "Build responsive websites using HTML, CSS and JavaScript."
            ),
            (
                "Data Analyst",
                "Data Insights Pvt Ltd",
                "Hyderabad",
                "₹4 - ₹7 LPA",
                "Analyze business data and prepare meaningful reports."
            )
        ]

        conn.executemany("""
            INSERT INTO jobs
            (title, company, location, salary, description)
            VALUES (?, ?, ?, ?, ?)
        """, sample_jobs)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    jobs = conn.execute(
        "SELECT * FROM jobs ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("index.html", jobs=jobs)


@app.route("/jobs")
def jobs():
    conn = get_db()
    jobs = conn.execute(
        "SELECT * FROM jobs ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("jobs.html", jobs=jobs)


@app.route("/add-job", methods=["GET", "POST"])
def add_job():
    if request.method == "POST":
        title = request.form["title"]
        company = request.form["company"]
        location = request.form["location"]
        salary = request.form["salary"]
        description = request.form["description"]

        conn = get_db()

        conn.execute("""
            INSERT INTO jobs
            (title, company, location, salary, description)
            VALUES (?, ?, ?, ?, ?)
        """, (title, company, location, salary, description))

        conn.commit()
        conn.close()

        return redirect(url_for("jobs"))

    return render_template("add_job.html")


@app.route("/apply/<int:job_id>", methods=["GET", "POST"])
def apply(job_id):
    conn = get_db()

    job = conn.execute(
        "SELECT * FROM jobs WHERE id = ?",
        (job_id,)
    ).fetchone()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        resume = request.form["resume"]

        conn.execute("""
            INSERT INTO applications
            (job_id, name, email, phone, resume)
            VALUES (?, ?, ?, ?, ?)
        """, (job_id, name, email, phone, resume))

        conn.commit()
        conn.close()

        return """
        <script>
            alert("Application submitted successfully!");
            window.location.href = "/";
        </script>
        """

    conn.close()

    return render_template("apply.html", job=job)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
    from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Cloud Job Portal</title>
        </head>
        <body>
            <h1>Welcome to Cloud Job Portal</h1>
            <p>Flask is working successfully!</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)