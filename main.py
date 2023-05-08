import random
import hashlib
import sqlite3

conn = sqlite3.connect('internet_security.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, name TEXT, email TEXT, password TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS scores
             (id INTEGER PRIMARY KEY, user_id INTEGER, score INTEGER, level INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

c.execute('''CREATE TABLE IF NOT EXISTS resources
             (id INTEGER PRIMARY KEY, title TEXT, url TEXT, type TEXT)''')

def create_account():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
    conn.commit()
    print("Account created successfully.")

def generate_question():
    questions = [
        "What is a phishing attack?",
        "What is a strong password?",
        "How can you protect your online privacy?",
        "What is two-factor authentication?",
        "What is encryption?",
        "What is malware?",
        "What is a firewall?",
        "What is a VPN?",
        "What is social engineering?",
        "What is a DDoS attack?",
        "What is a botnet?",
        "What is a vulnerability?",
        "What is a zero-day exploit?",
        "What is a man-in-the-middle attack?",
        "What is a cross-site scripting (XSS) attack?"
    ]
    question = random.choice(questions)
    return question

def play_game(user_id):
    score = 0
    for level in range(1, 4):
        print(f"Level {level}")
        question = generate_question()
        print(f"Question: {question}")
        answer = input("Answer: ")
        if answer == "correct":
            score += 10
            c.execute("INSERT INTO scores (user_id, score, level) VALUES (?, ?, ?)", (user_id, score, level))
            conn.commit()
    print(f"Your score is {score}")

def display_leaderboard():
    c.execute("SELECT users.name, SUM(scores.score) as total_score FROM scores JOIN users ON scores.user_id = users.id GROUP BY users.name ORDER BY total_score DESC LIMIT 10")
    scores = c.fetchall()
    print("Top Scores:")
    for index, score in enumerate(scores):
        name, points = score
        print(f"{index+1}. {name}: {points} points")

def display_resources():
    print("Educational Resources:")
    c.execute("SELECT * FROM resources WHERE type = 'article'")
    articles = c.fetchall()
    if len(articles) > 0:
        print("- Articles:")
        for article in articles:
            print(f"  - {article[1]} ({article[2]})")
    c.execute("SELECT * FROM resources WHERE type = 'video'")
    videos = c.fetchall()
    if len(videos) > 0:
        print("- Videos:")
        for video in videos:
            print(f"  - {video[1]} ({video[2]})")
    c.execute("SELECT * FROM resources WHERE type = 'quiz'")
    quizzes = c.fetchall()
    if len(quizzes) > 0:
        print("- Quizzes:")
        for quiz in quizzes:
            print(f"  - {quiz[1]} ({quiz[2]})")

def main_menu():
    while True:
        print("Internet Security and Safety Learning Platform") 
        print("1. Create account") 
        print("2. Play game") 
        print("3. View leaderboard") 
        print("4. View educational resources") 
        print("5. Exit") 
        choice = input("Enter your choice: ") 
        if choice == "1": 
            create_account() 
        elif choice == "2": 
            email = input("Enter your email: ")
            password = input("Enter your password: ") 
            hashed_password = hashlib.sha256(password.encode()).hexdigest() 
            c.execute("SELECT id FROM users WHERE email=? AND password=?", (email, hashed_password)) 
            user = c.fetchone()
            if user: 
                user_id = user[0] 
                play_game(user_id) 
            else: 
                print("Invalid email or password.") 
        elif choice == "3": 
            display_leaderboard() 
        elif choice == "4": 
            display_resources() 
        elif choice == "5": 
            conn.close() 
            print("Goodbye!") 
            break 
        else: 
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
