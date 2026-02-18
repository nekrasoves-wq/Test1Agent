# Простой веб-сервер для работы с SQLite базой данных
from flask import Flask, request, jsonify, render_template_string
from database import DatabaseManager
import json

app = Flask(__name__)
db = DatabaseManager('users.db')

# HTML шаблон для веб-интерфейса
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>База данных - Управление</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #00ff00 0%, #228b22 100%);
            min-height: 100vh;
            padding: 20px;
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        h1 { text-align: center; margin-bottom: 30px; }
        .section {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 5px;
            font-size: 1rem;
        }
        button {
            padding: 12px 30px;
            background: #fff;
            color: #228b22;
            border: none;
            border-radius: 5px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            margin-right: 10px;
        }
        button:hover {
            background: #f0f0f0;
            transform: translateY(-2px);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            overflow: hidden;
        }
        th, td {
            padding: 12px;
            text-align: left;
            color: #333;
        }
        th {
            background: #228b22;
            color: white;
        }
        tr:nth-child(even) {
            background: rgba(0, 255, 0, 0.1);
        }
        .actions button {
            padding: 5px 15px;
            font-size: 0.9rem;
        }
        .message {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            display: none;
        }
        .success {
            background: #4caf50;
            color: white;
        }
        .error {
            background: #f44336;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗄️ Управление базой данных</h1>
        
        <div id="message" class="message"></div>
        
        <!-- Форма добавления -->
        <div class="section">
            <h2>➕ Добавить пользователя</h2>
            <form id="addForm">
                <div class="form-group">
                    <label>Фамилия:</label>
                    <input type="text" id="lastName" required>
                </div>
                <div class="form-group">
                    <label>Имя:</label>
                    <input type="text" id="firstName" required>
                </div>
                <div class="form-group">
                    <label>Отчество:</label>
                    <input type="text" id="middleName">
                </div>
                <button type="submit">Добавить</button>
            </form>
        </div>
        
        <!-- Поиск -->
        <div class="section">
            <h2>🔍 Поиск</h2>
            <input type="text" id="searchInput" placeholder="Введите имя, фамилию или отчество...">
            <button onclick="searchUsers()">Найти</button>
            <button onclick="loadAllUsers()">Показать всех</button>
        </div>
        
        <!-- Таблица пользователей -->
        <div class="section">
            <h2>👥 Пользователи</h2>
            <div id="usersTable"></div>
        </div>
    </div>
    
    <script>
        // Загрузка всех пользователей при старте
        window.onload = function() {
            loadAllUsers();
        };
        
        // Добавление пользователя
        document.getElementById('addForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const data = {
                last_name: document.getElementById('lastName').value,
                first_name: document.getElementById('firstName').value,
                middle_name: document.getElementById('middleName').value
            };
            
            const response = await fetch('/api/users', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            showMessage(result.message, result.status);
            
            if (result.status === 'success') {
                this.reset();
                loadAllUsers();
            }
        });
        
        // Загрузка всех пользователей
        async function loadAllUsers() {
            const response = await fetch('/api/users');
            const data = await response.json();
            displayUsers(data.users);
        }
        
        // Поиск пользователей
        async function searchUsers() {
            const searchTerm = document.getElementById('searchInput').value;
            const response = await fetch(`/api/users/search?q=${searchTerm}`);
            const data = await response.json();
            displayUsers(data.users);
        }
        
        // Отображение пользователей в таблице
        function displayUsers(users) {
            let html = '<table><tr><th>ID</th><th>Фамилия</th><th>Имя</th><th>Отчество</th><th>Дата добавления</th><th>Действия</th></tr>';
            
            users.forEach(user => {
                html += `<tr>
                    <td>${user[0]}</td>
                    <td>${user[1]}</td>
                    <td>${user[2]}</td>
                    <td>${user[3] || '-'}</td>
                    <td>${user[4]}</td>
                    <td class="actions">
                        <button onclick="deleteUser(${user[0]})">Удалить</button>
                    </td>
                </tr>`;
            });
            
            html += '</table>';
            document.getElementById('usersTable').innerHTML = html;
        }
        
        // Удаление пользователя
        async function deleteUser(id) {
            if (!confirm('Удалить этого пользователя?')) return;
            
            const response = await fetch(`/api/users/${id}`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            showMessage(result.message, result.status);
            loadAllUsers();
        }
        
        // Показ сообщений
        function showMessage(message, status) {
            const msgDiv = document.getElementById('message');
            msgDiv.textContent = message;
            msgDiv.className = 'message ' + status;
            msgDiv.style.display = 'block';
            
            setTimeout(() => {
                msgDiv.style.display = 'none';
            }, 3000);
        }
    </script>
</body>
</html>
'''

# API endpoints
@app.route('/')
def index():
    """Главная страница"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/users', methods=['GET'])
def get_users():
    """Получить всех пользователей"""
    users = db.get_all_users()
    return jsonify({'status': 'success', 'users': users})

@app.route('/api/users', methods=['POST'])
def add_user():
    """Добавить пользователя"""
    data = request.get_json()
    user_id = db.add_user(
        data.get('last_name'),
        data.get('first_name'),
        data.get('middle_name', '')
    )
    
    if user_id:
        return jsonify({'status': 'success', 'message': 'Пользователь добавлен!', 'id': user_id})
    else:
        return jsonify({'status': 'error', 'message': 'Ошибка добавления'})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Удалить пользователя"""
    success = db.delete_user(user_id)
    
    if success:
        return jsonify({'status': 'success', 'message': 'Пользователь удалён!'})
    else:
        return jsonify({'status': 'error', 'message': 'Ошибка удаления'})

@app.route('/api/users/search', methods=['GET'])
def search_users():
    """Поиск пользователей"""
    search_term = request.args.get('q', '')
    users = db.search_users(search_term)
    return jsonify({'status': 'success', 'users': users})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Запуск веб-сервера для работы с базой данных...")
    print("📍 Откройте в браузере: http://127.0.0.1:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
