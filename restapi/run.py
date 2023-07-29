from os import system
from time import sleep

if __name__ == '__main__':
    sleep(5)
    system("python manage.py migrate")
    system("python manage.py seed")
    system("python manage.py runserver 0.0.0.0:8000")
