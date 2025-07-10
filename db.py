import sqlite3


class DatabaseManager:

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._create_structure()

    def _execute(self, sql: str, params: tuple = ()):
        try:
            # isolation_level None for autocommit
            with sqlite3.connect(self.db_path, isolation_level=None) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                # If is a SELECT, return data.
                if sql.strip().upper().startswith("SELECT"):
                    return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Errore del database: {e}")

    def _create_structure(self) -> None:
        self._execute("""
            CREATE TABLE IF NOT EXISTS User (
                user_id BIGINT PRIMARY KEY, 
                session_id VARCHAR(256) NOT NULL
            )
        """)

    def user_session_exists(self, user_id: int | str) -> bool:
        sql = "SELECT * FROM User WHERE user_id = ?;"
        query_data = self._execute(sql, (user_id,))
        # If user doesn't exist returns empty list
        return bool(query_data)

    def add_user_session(self, user_id: int | str, session_id: str):
        sql = "INSERT INTO User (user_id, session_id) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET session_id = excluded.session_id;"
        self._execute(sql, (user_id, session_id))
        # print(f"Utente aggiunto: {user_id}")

    def get_user_session(self, user_id: int | str) -> str | None:
        sql = "SELECT session_id FROM User WHERE user_id = ?;"
        query_data = self._execute(sql, (user_id,))
        return query_data[0][0] if query_data else None

    def delete_user_session(self, user_id: int | str) -> None:
        sql = "DELETE FROM User WHERE user_id = ?;"
        self._execute(sql, (user_id,))


# All possible cases for testing the methods
# db = DatabaseManager("storage/users.db")
# print(db.user_session_exists(123))
# print(db.delete_user_session(123))
# print(db.get_user_session(123))
# print(db.add_user_session(123, "ciaociaociao"))
# print(db.user_session_exists(123))
# print(db.get_user_session(123))
# print(db.delete_user_session(123))
# print(db.user_session_exists(123))
# print(db.get_user_session(123))

