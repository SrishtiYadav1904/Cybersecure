import sqlite3

def migrate():
    conn = sqlite3.connect('cyberguard.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA table_info(predictions)')
    cols = [r[1] for r in cursor.fetchall()]
    print('Existing predictions columns:', cols)
    if 'dataset_version' not in cols:
        cursor.execute("ALTER TABLE predictions ADD COLUMN dataset_version VARCHAR(50) DEFAULT 'CB-DATA-002'")
        conn.commit()
        print("Added dataset_version column to predictions table!")
    else:
        print("dataset_version column already present.")

if __name__ == "__main__":
    migrate()
