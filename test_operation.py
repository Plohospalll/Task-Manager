import unittest
from operation import *
from unittest.mock import patch
from io import StringIO


class test_status_chage(unittest.TestCase):
	"""1.setUp: Метод, который инициализирует список задач перед каждым тестом,
	 чтобы тесты были изолированы и не влияли друг на друга.

	2.test_status_change_to_complited: Проверяет, что задача с id = 2
	 меняет статус на True, если вызывается с st_c = 'complited'.

	3.test_status_change_to_not_complited: Проверяет, что задача с id = 3
	меняет статус на False, если вызывается с st_c = 'not_complited'.

	4.test_status_not_change_for_different_id: Убеждается,
	что задачи с другими id не изменяют статус.

	5.test_status_change_no_matching_id: Проверяет, что если передан
	 несуществующий id, никакие задачи не изменят свой статус."""

	def setUp(self):
		self.tasks = [{'id': 1, 'complited': False},
		              {'id': 2, 'complited': False},
		              {'id': 3, 'complited': True}]

	def test_status_chage_complited(self):
		status_chage(self.tasks, 'complited', 2)
		self.assertTrue(self.tasks[1]['complited'])

	def test_status_chage_not_complited(self):
		status_chage(self.tasks, 'not_complited', 3)
		self.assertFalse(self.tasks[2]['complited'])

	def test_status_chage_not_deferently_complited(self):
		status_chage(self.tasks, 'complited', 3)
		self.assertFalse(self.tasks[1]['complited'])
		self.assertTrue(self.tasks[2]['complited'])

	def test_status_chage_no_match_id(self):
		status_chage(self.tasks, 'complited', 99)
		self.assertFalse(self.tasks[0]['complited'])
		self.assertFalse(self.tasks[1]['complited'])
		self.assertTrue(self.tasks[2]['complited'])


class test_add_task(unittest.TestCase):
	"""1.setUp: Этот метод инициализирует список задач для каждого теста. Он гарантирует,
	 что каждый тест начинается с одинакового состояния списка задач.

	2.test_add_task: Этот тест проверяет основные функциональные аспекты функции add_task:
	Убедитесь, что новая задача добавлена в список.
	Проверьте, что у новой задачи корректный ID (должен быть на 1 больше, чем у последней задачи).
	Проверьте, что задача по умолчанию не выполнена (complited = False).
	Используя patch, убедитесь, что функция save_tasks была вызвана.

	3.@patch('__main__.save_tasks'): Этот декоратор используется для подмены функции save_tasks
	в тестах, чтобы проверить факт ее вызова, но не выполнять фактическую функцию сохранения данных.
			"""

	def setUp(self):
		self.tasks = [{'id': 1, 'dis': '123', 'complited': False}, ]

	@patch('operation.save_tasks')
	def test_add_task_corect_append(self, mock_save_tasks):
		add_task(self.tasks, "New task")
		self.assertEqual(len(self.tasks), 2)
		self.assertEqual(self.tasks[1]['dis'], "New task")
		self.assertEqual(self.tasks[1]['id'], 2)
		self.assertFalse(self.tasks[1]['complited'])

		mock_save_tasks.assert_called_once_with(self.tasks)


class TestAllTasks(unittest.TestCase):
	"""1.@patch('sys.stdout', new_callable=StringIO): Этот декоратор используется для подмены стандартного вывода
	(stdout) на объект StringIO, что позволяет перехватывать и проверять то, что функция выводит на экран.

	2.test_all_tasks_with_tasks: Тест проверяет, что при наличии задач и значении check = True
	функция выводит все задачи и возвращает True.

	3.test_all_tasks_with_no_tasks: Тест проверяет, что при отсутствии задач и значении
	check = False функция выводит соответствующее сообщение."""

	@patch('sys.stdout', new_callable=StringIO)
	def test_all_tasks_with_tasks(self, mock_stdout):
		tasks = [
			{'id': 1, 'dis': "Задача 1", 'complited': False},
			{'id': 2, 'dis': "Задача 2", 'complited': True},
		]
		result = all_tasks(tasks, True)
		output = mock_stdout.getvalue().strip()

		expected_output = (
			'Номер задачи: 1|| Описание задачи: Задача 1||  Статус задачи: False\n'
			'Номер задачи: 2|| Описание задачи: Задача 2||  Статус задачи: True'
		)

		self.assertEqual(output, expected_output)
		self.assertTrue(result)

	@patch('sys.stdout', new_callable=StringIO)
	def test_all_tasks_with_no_tasks(self, mock_stdout):
		tasks = []
		all_tasks(tasks, False)
		output = mock_stdout.getvalue().strip()

		expected_output = 'Нельзя удалить задач которых нет! Сначала добавте задачу'

		self.assertEqual(output, expected_output)


class Test_remove_task(unittest.TestCase):
	"""test_remove_existing_task:
	Этот тест проверяет удаление задачи, которая существует в списке (например, с id=2).
	После удаления проверяется, что задача с этим id больше не существует в списке.
	Также проверяется, что функция save_tasks была вызвана с обновленным списком задач.

	test_remove_non_existing_task:
	Этот тест проверяет случай, когда задача с указанным id не существует (например, с id=99).

	может возникнуть проблемы с тем что remove_task что функция remove_task работает с копией списка tasks,
	а не с оригинальным объектом. Когда внутри функции происходит фильтрация, новый список создается,
	но старый список в вызывающем коде остается неизменным.
	 РЕШЕНИЕ: Для того чтобы изменения были видны за пределами функции, можно изменить оригинальный список tasks напрямую:
	 tasks[:] = [task for task in tasks if task['id'] != int(task_id)]
	 Здесь используется срез tasks[:], чтобы заменить содержимое оригинального списка.
	 Это гарантирует, что изменения в списке tasks будут видны за пределами функции remove_task."""

	def setUp(self):
		# Инициализация списка задач для каждого теста
		self.tasks = [
			{'id': 1, 'dis': "First task", 'complited': False},
			{'id': 2, 'dis': "Second task", 'complited': True},
			{'id': 3, 'dis': "Third task", 'complited': False}
		]

	@patch('operation.save_tasks')
	def test_remove_existing_task(self, mock_save_tasks):
		remove_task(self.tasks, 2)

		# Проверяем, что задача с id=2 удалена
		self.assertEqual(len(self.tasks), 2)
		self.assertFalse(any(task['id'] == 2 for task in self.tasks))

		# Проверяем, что save_tasks была вызвана
		mock_save_tasks.assert_called_once_with(self.tasks)

	@patch('operation.save_tasks')
	def test_remove_not_existing_task(self, mock_save_tasks):
		remove_task(self.tasks, 1)
		# проверяем что после удаления не удилились другие задачи
		self.assertTrue(any(task['id'] == 2 for task in self.tasks))
		self.assertTrue(any(task['id'] == 3 for task in self.tasks))

		mock_save_tasks.assert_called_once_with(self.tasks)

	@patch('operation.save_tasks')
	def test_remove_not_existing_task(self, mock_save_tasks):
		remove_task(self.tasks, 99)
		# проверяем что при попытке удаления не существующего ID ни чего не удаляется
		self.assertEqual(len(self.tasks), 3)
		self.assertEqual(self.tasks[0]['id'], 1)
		self.assertEqual(self.tasks[1]['id'], 2)
		self.assertEqual(self.tasks[2]['id'], 3)

		mock_save_tasks.assert_called_once_with(self.tasks)


if __name__ == '__main__':
	unittest.main()
