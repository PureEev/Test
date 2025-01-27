import subprocess
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

project_dir = os.path.join(script_dir, 'test_task')

manage_py_path = os.path.join(project_dir, 'manage.py')

if not os.path.exists(manage_py_path):
    print(f"Не найден manage.py по пути {manage_py_path}")
    sys.exit(1)

venv_path = os.path.join(script_dir, '.venv')  # Замените на правильный путь к вашему виртуальному окружению

if not os.path.exists(venv_path):
    print(f"Виртуальное окружение не найдено по пути {venv_path}")
    sys.exit(1)

venv_python = os.path.join(venv_path, 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join(venv_path, 'bin', 'python')

if not os.path.exists(venv_python):
    print(f"Интерпретатор Python не найден в виртуальном окружении: {venv_python}")
    sys.exit(1)

subprocess.run([venv_python, manage_py_path, 'runserver'])
