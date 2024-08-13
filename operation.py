import json
import os
from main import *



# ЗАГРУЗКА ФАЙЛА JSON
def load_tasks():
	try:
		if os.path.exists(TASK_JSON_FILE):
			with open(TASK_JSON_FILE, 'r') as json_file:
				return json.load(json_file)
		return []
	except(IOError, json.JSONDecodeError) as eror_2:
		print(f'Ошибка загрузки файла {eror_2}')


# СОХРАНЕНИЕ ФАЙЛА JSON
def save_tasks(tasks):
	try:
		with open(TASK_JSON_FILE, 'w') as json_file:
			json.dump(tasks, json_file, indent=4)
	except IOError as eror:
		print(f'Ошибка сохранения файла {eror}')


# ДОБАВЛЕНИЕ ЗАДАЧ
def add_task(tasks, dis):
	task = {
		'id': len(tasks) + 1,
		'dis': dis,
		'complited': False
	}
	tasks.append(task)
	save_tasks(tasks)
	print('Задача добавлена')
	print()


# ИЗМЕНЕНИЕ СТАТУСА ЗАДАЧИ
def status_chage(tasks, st_c, id):
	for task in tasks:
		if task['id'] == id:
			if st_c == 'complited':
				task['complited'] = True
			elif st_c == 'not_complited':
				task['complited'] = False
	save_tasks(tasks)


# ПОКАЗ ВСЕХ ЗАДАЧ
def all_tasks(tasks, check):
	if check == True:
		for task in tasks:
			print(f'Номер задачи: {task["id"]}|| Описание задачи: {task["dis"]}||  Статус задачи: {task["complited"]}')
		return True
	elif check == False:
		print('Нельзя удалить задач которых нет! Сначала добавте задачу')


# УДАЛЕНИЕ ЗАДАЧИ
def remove_task(tasks, task_id):
	tasks[:] = [task for task in tasks if task['id'] != int(task_id)]
	save_tasks(tasks)


# ПРОВЕРКА НА НАЛИЧИЕ ЗАДАЧ
def check_task_len(tasks):
	return len(tasks) > 0


# Проверяем num на соостветствие типу int, с перехватом ошибки ValueError
def check_task_int(tasks, num):
	try:
		num != int(num)
	except ValueError:
		return False
	for i in tasks:
		if i['id'] == int(num):
			return True
	return False
