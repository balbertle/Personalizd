import sqlite3

conn = sqlite3.connect('C:\Users\alber\OneDrive\Desktop\Personalizd\personalizd.db')
cursor = conn.cursor()

# Create the movie_ratings table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS movie_ratingss (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rating INTEGER,
        movie_id INTEGER,
        user_id INTEGER,
        total_ratings INTEGER,
        FOREIGN KEY (movie_id) REFERENCES movies(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

conn.commit()
conn.close()