import sqlite3
#database connection
DB_NAME = 'remedial_class.db'

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_schema():
    conn = get_connection()
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT CHECK(role IN ('admin', 'teacher', 'student')) NOT NULL
    );
    ''')

    # Create Students table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        course TEXT,
        year INTEGER
    );
    ''')

    # Create Teachers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Teachers (
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        subject TEXT
    );
    ''')

    # Create Subjects table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Subjects (
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT
    );
    ''')

    # Create RemedialClasses table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS RemedialClasses (
        class_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        teacher_id INTEGER,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        room TEXT,
        FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id),
        FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)
    );
    ''')

    # Create StudentClassMapping table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS StudentClassMapping (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        class_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES Students(student_id),
        FOREIGN KEY (class_id) REFERENCES RemedialClasses(class_id)
    );
    ''')

    # Create Attendance table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Attendance (
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,
        student_id INTEGER,
        status TEXT CHECK(status IN ('present', 'absent')),
        date TEXT NOT NULL,
        FOREIGN KEY (class_id) REFERENCES RemedialClasses(class_id),
        FOREIGN KEY (student_id) REFERENCES Students(student_id)
    );
    ''')

    # Create Performance table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Performance (
        performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        score_before REAL,
        score_after REAL,
        date TEXT,
        FOREIGN KEY (student_id) REFERENCES Students(student_id),
        FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
    );
    ''')

    # Create Feedback table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Feedback (
        feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,
        student_id INTEGER,
        comment TEXT,
        rating INTEGER CHECK(rating >= 1 AND rating <= 5),
        FOREIGN KEY (class_id) REFERENCES RemedialClasses(class_id),
        FOREIGN KEY (student_id) REFERENCES Students(student_id)
    );
    ''')

    conn.commit()
    conn.close()
    print("✅ Database and tables initialized.")
    
