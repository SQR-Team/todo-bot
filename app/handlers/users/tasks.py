import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import dp, cur, conn

logger = logging.getLogger(__name__)


class Task(StatesGroup):
    text = State()
    category = State()
    deadline = State()


class Delete(StatesGroup):
    delete = State()


class Complete(StatesGroup):
    complete = State()


@dp.message_handler(commands=['add'])
async def add_task(message: types.Message):
    try:
        await message.reply("Please enter your task:")
        await Task.text.set()
        logger.info(f"User {message.from_user.id} started to add the task.")
    except Exception as e:
        print(f"User {message.from_user.id}, error while adding task\n{e}")
        logger.error(f"User {message.from_user.id}, error while adding task\n{e}n")


@dp.message_handler(state=Task.text)
async def save_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.reply("Please enter the category (e.g., personal, work):")
    await Task.next()


@dp.message_handler(state=Task.category)
async def save_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.reply("Please enter the deadline (format: YYYY-MM-DD HH:MM):")
    await Task.next()


@dp.message_handler(state=Task.deadline)
async def save_deadline(message: types.Message, state: FSMContext):
    deadline = message.text
    async with state.proxy() as data:
        text = data['text']
        category = data['category']

        cur.execute('''INSERT INTO tasks (user_id, task, category, deadline) VALUES (?, ?, ?, ?)''',
                    (message.from_user.id, text, category, deadline))
        conn.commit()
    await state.finish()
    await message.reply("Task added successfully!")


@dp.message_handler(commands=['list'])
async def list_tasks(message: types.Message):
    try:
        user_id = message.from_user.id
        cur.execute('''SELECT * FROM tasks WHERE user_id=?''', (user_id,))
        tasks = cur.fetchall()
        if tasks:
            task_list = "\n".join(
                [f"{task[0]}. {task[2]} - Category: {task[3]}, Deadline: {task[4]}, Completed: {'Yes' if task[5] else 'No'}"
                 for task in tasks])
            await message.reply(f"Your tasks:\n{task_list}")
        else:
            await message.reply("No tasks found.")
    except Exception as e:
        print(f"User {message.from_user.id}, error while listing all tasks\n{e}")
        logger.error(f"User {message.from_user.id}, error while listing all tasks\n{e}n")


@dp.message_handler(commands=['delete'])
async def delete_task(message: types.Message):
    try:
        await message.reply("Please enter the name of the task you want to delete:")
        await Delete.delete.set()
        logger.info(f"User {message.from_user.id} started to delete the task.")
    except Exception as e:
        print(f"User {message.from_user.id}, error while deleting task\n{e}")
        logger.error(f"User {message.from_user.id}, error while deleting task\n{e}n")


@dp.message_handler(state=Delete.delete)
async def perform_delete(message: types.Message, state: FSMContext):
    task_name = message.text
    cur.execute('''DELETE FROM tasks WHERE task=?''', (task_name,))
    conn.commit()
    await state.finish()
    await message.reply("Task deleted successfully!")


@dp.message_handler(commands=['complete'])
async def complete_task(message: types.Message):
    try:
        await message.reply("Please enter the name of the task you want to mark as completed:")
        await Complete.complete.set()
        logger.info(f"User {message.from_user.id} started to mark the task as completed.")
    except Exception as e:
        print(f"User {message.from_user.id}, error while marking task as completed\n{e}")
        logger.error(f"User {message.from_user.id}, error while marking task as completed\n{e}n")


@dp.message_handler(state=Complete.complete)
async def perform_complete(message: types.Message, state: FSMContext):
    task_name = message.text
    cur.execute('''UPDATE tasks SET completed=1 WHERE task=?''', (task_name,))
    conn.commit()
    await state.finish()
    await message.reply("Task marked as completed!")
