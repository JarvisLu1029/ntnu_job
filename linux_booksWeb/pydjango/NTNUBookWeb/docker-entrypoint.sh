#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Make migrations 創建資料庫模型的遷移文件
echo "Make migrations"
python manage.py makemigrations

# Apply database migrations 資料庫模型的遷移文件應用到資料庫中
echo "Apply database migrations"
python manage.py migrate

echo "Run server"
python manage.py runserver 0.0.0.0:8000

# 將腳本所接收到的命令行參數傳遞給另一個程序執行
exec "$@"