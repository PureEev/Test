import subprocess
import sys
import os

# URL репозитория
repo_url = "https://github.com/PureEev/Test"
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_dir = os.path.join(script_dir, 'Test')  # Папка, куда клонируется репозиторий
project_dir = os.path.join(repo_dir, 'test_task')  # Основная директория проекта
manage_py_path = os.path.join(project_dir, 'manage.py')

# Клонирование репозитория, если папка отсутствует
if not os.path.exists(repo_dir):
    print(f"Клонирование репозитория {repo_url} в {repo_dir}...")
    result = subprocess.run(["git", "clone", repo_url, repo_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Ошибка при клонировании репозитория:\n{result.stderr.decode().strip()}")
        sys.exit(1)
    print("Репозиторий успешно клонирован.")

# Проверка наличия manage.py
if not os.path.exists(manage_py_path):
    print(f"Не найден manage.py по пути {manage_py_path}")
    sys.exit(1)

# Путь к виртуальному окружению
venv_path = os.path.join(repo_dir, '.venv')  # Учитывается, что .venv находится внутри Test

if not os.path.exists(venv_path):
    print(f"Виртуальное окружение не найдено по пути {venv_path}")
    sys.exit(1)

venv_python = os.path.join(venv_path, 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join(venv_path, 'bin', 'python')

if not os.path.exists(venv_python):
    print(f"Интерпретатор Python не найден в виртуальном окружении: {venv_python}")
    sys.exit(1)

# Запуск сервера
subprocess.run([venv_python, manage_py_path, 'runserver'])
