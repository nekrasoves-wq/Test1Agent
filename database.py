import sqlite3
from datetime import datetime

class DatabaseManager:
    """Класс для управления SQLite базой данных"""
    
    def __init__(self, db_name='users.db'):
        """Инициализация подключения к базе данных"""
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_table()
    
    def connect(self):
        """Подключение к базе данных"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"✅ Подключение к базе данных '{self.db_name}' успешно!")
        except sqlite3.Error as e:
            print(f"❌ Ошибка подключения к базе данных: {e}")
    
    def create_table(self):
        """Создание таблицы пользователей"""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    last_name TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    middle_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.connection.commit()
            print("✅ Таблица 'users' создана или уже существует")
        except sqlite3.Error as e:
            print(f"❌ Ошибка создания таблицы: {e}")
    
    def add_user(self, last_name, first_name, middle_name=''):
        """Добавление нового пользователя"""
        try:
            self.cursor.execute('''
                INSERT INTO users (last_name, first_name, middle_name)
                VALUES (?, ?, ?)
            ''', (last_name, first_name, middle_name))
            self.connection.commit()
            print(f"✅ Пользователь '{last_name} {first_name}' добавлен в базу данных")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"❌ Ошибка добавления пользователя: {e}")
            return None
    
    def get_all_users(self):
        """Получение всех пользователей"""
        try:
            self.cursor.execute('SELECT * FROM users')
            users = self.cursor.fetchall()
            return users
        except sqlite3.Error as e:
            print(f"❌ Ошибка получения пользователей: {e}")
            return []
    
    def get_user_by_id(self, user_id):
        """Получение пользователя по ID"""
        try:
            self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            user = self.cursor.fetchone()
            return user
        except sqlite3.Error as e:
            print(f"❌ Ошибка получения пользователя: {e}")
            return None
    
    def search_users(self, search_term):
        """Поиск пользователей по имени или фамилии"""
        try:
            self.cursor.execute('''
                SELECT * FROM users 
                WHERE last_name LIKE ? OR first_name LIKE ? OR middle_name LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            users = self.cursor.fetchall()
            return users
        except sqlite3.Error as e:
            print(f"❌ Ошибка поиска: {e}")
            return []
    
    def update_user(self, user_id, last_name, first_name, middle_name=''):
        """Обновление данных пользователя"""
        try:
            self.cursor.execute('''
                UPDATE users 
                SET last_name = ?, first_name = ?, middle_name = ?
                WHERE id = ?
            ''', (last_name, first_name, middle_name, user_id))
            self.connection.commit()
            print(f"✅ Данные пользователя с ID {user_id} обновлены")
            return True
        except sqlite3.Error as e:
            print(f"❌ Ошибка обновления: {e}")
            return False
    
    def delete_user(self, user_id):
        """Удаление пользователя"""
        try:
            self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            self.connection.commit()
            print(f"✅ Пользователь с ID {user_id} удалён")
            return True
        except sqlite3.Error as e:
            print(f"❌ Ошибка удаления: {e}")
            return False
    
    def get_user_count(self):
        """Получение количества пользователей"""
        try:
            self.cursor.execute('SELECT COUNT(*) FROM users')
            count = self.cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            print(f"❌ Ошибка подсчёта: {e}")
            return 0
    
    def display_all_users(self):
        """Отображение всех пользователей в красивом формате"""
        users = self.get_all_users()
        if not users:
            print("\n📋 База данных пуста")
            return
        
        print("\n" + "="*80)
        print("📋 СПИСОК ВСЕХ ПОЛЬЗОВАТЕЛЕЙ")
        print("="*80)
        print(f"{'ID':<5} {'Фамилия':<20} {'Имя':<20} {'Отчество':<20} {'Дата добавления':<20}")
        print("-"*80)
        
        for user in users:
            user_id, last_name, first_name, middle_name, created_at = user
            middle_name = middle_name or '-'
            print(f"{user_id:<5} {last_name:<20} {first_name:<20} {middle_name:<20} {created_at:<20}")
        
        print("="*80)
        print(f"Всего пользователей: {len(users)}")
    
    def close(self):
        """Закрытие соединения с базой данных"""
        if self.connection:
            self.connection.close()
            print("✅ Соединение с базой данных закрыто")


# Пример использования
if __name__ == "__main__":
    # Создаём экземпляр менеджера базы данных
    db = DatabaseManager('users.db')
    
    print("\n" + "="*80)
    print("🗄️  ДЕМОНСТРАЦИЯ РАБОТЫ С БАЗОЙ ДАННЫХ SQLite")
    print("="*80)
    
    # Добавляем тестовых пользователей
    print("\n1️⃣  ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ:")
    db.add_user('Иванов', 'Иван', 'Иванович')
    db.add_user('Петров', 'Пётр', 'Петрович')
    db.add_user('Сидорова', 'Анна', 'Сергеевна')
    
    # Отображаем всех пользователей
    print("\n2️⃣  ОТОБРАЖЕНИЕ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ:")
    db.display_all_users()
    
    # Поиск пользователя
    print("\n3️⃣  ПОИСК ПОЛЬЗОВАТЕЛЕЙ ПО ИМЕНИ 'Иван':")
    results = db.search_users('Иван')
    for user in results:
        print(f"   Найден: {user[1]} {user[2]} {user[3] or ''}")
    
    # Получаем количество пользователей
    print(f"\n4️⃣  ВСЕГО ПОЛЬЗОВАТЕЛЕЙ В БАЗЕ: {db.get_user_count()}")
    
    # Закрываем соединение
    print("\n" + "="*80)
    db.close()
