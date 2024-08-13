import json
import os
from operation import *


TASK_JSON_FILE = 'task.json'


# ГЛАВНАЯ ФУНКЦИЯ
def main():
	task = load_tasks()
	while True:
		print('1. Добавление задачи.')
		print('2. Удаление задачи.')
		print('3. Изменение статуса задачи (выполнена/невыполнена).')
		print('4. Просмотр всех задач.')
		print('5. Выход')

		inp = input()
		if inp == '1':
			task = load_tasks()  # ________________________________________ обновляем JSON
			all_tasks(task, check_task_len(task))  # ______________________показываем какие задачи есть
			dis = input('введите описание задачи:  ')
			print()
			add_task(task, dis)
		elif inp == '2':
			task = load_tasks()  # ________________________________________обновляем JSON
			if all_tasks(task, check_task_len(task)):  # ___________________Проверяем есть ли задачи
				task_id = input('введите id для удаления:  ')
				if check_task_int(task, task_id):  # _______Проверяем цифру ввели или чтото другое с перехватом ошибки
					remove_task(task, task_id)  # ___________________________ удаляем задачу
					print('Задача удалена')
				else:
					print('Введите ID задачи')
		elif inp == '3':
			task = load_tasks()  # _________________________________________обновляем JSON
			if all_tasks(task, check_task_len(task)):  # __________________Проверяем есть ли задачи
				id = input('Введите номер задачи:  ')
				if check_task_int(task, id):  # __Проверяем цифру ввели или чтото другое с перехватом ошибки
					st_c = input('Выполненно: complited, Не выполненно: not_complited')
					status_chage(task, st_c, id)  # ___________ меняем статус
				else:
					print('Невернно введен ID')
		elif inp == '4':
			task = load_tasks()  # ___________________________________________обновляем JSON
			all_tasks(task, check_task_len(task))  # ________________________выводим все задачи
		elif inp == '5':
			break
		else:
			print('УКАЖИТЕ ЦИФРУ ИЗ СПИСКА!')


if __name__ == '__main__':
	main()
