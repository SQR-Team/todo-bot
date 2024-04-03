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


@dp.message_handler(commands=['add'])
async def add_task(message: types.Message):
    await message.reply("Please enter your task:")
    await Task.text.set()
    logger.info(f"User {message.from_user.id} started to add the task.")


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


@dp.message_handler(commands=['delete'])
async def delete_task(message: types.Message):
    await message.reply("Please enter the ID of the task you want to delete:")
    await dp.register_next_step_handler(message, perform_delete)


async def perform_delete(message: types.Message):
    task_id = message.text
    cur.execute('''DELETE FROM tasks WHERE id=?''', (task_id,))
    conn.commit()
    await message.reply("Task deleted successfully!")


@dp.message_handler(commands=['complete'])
async def complete_task(message: types.Message):
    await message.reply("Please enter the ID of the task you want to mark as completed:")
    await dp.register_next_step_handler(message, perform_complete)


async def perform_complete(message: types.Message):
    task_id = message.text
    cur.execute('''UPDATE tasks SET completed=1 WHERE id=?''', (task_id,))
    conn.commit()
    await message.reply("Task marked as completed!")
