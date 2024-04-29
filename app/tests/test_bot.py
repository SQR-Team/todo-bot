import unittest

from aiogram_unittest import Requester
from aiogram_unittest.handler import MessageHandler
from aiogram_unittest.types.dataset import MESSAGE
from app.handlers.users.start import start
from app.handlers.users.help import help_command
from app.handlers.users.tasks import add_task, complete_task, delete_task


class TestBot(unittest.IsolatedAsyncioTestCase):
    async def test_add_task(self):
        request = Requester(request_handler=MessageHandler(add_task))
        calls = await request.query(message=MESSAGE.as_object(text="Hello, Bot!"))
        answer_message = calls.send_message.fetchone()
        self.assertEqual(answer_message.text, "Please enter your task:")

    async def test_delete_task(self):
        request = Requester(request_handler=MessageHandler(delete_task))
        calls = await request.query(message=MESSAGE.as_object())
        answer_message = calls.send_message.fetchone()
        self.assertEqual(
            answer_message.text, "Please enter the id of the task you want to delete:"
        )

    async def test_complete_task(self):
        request = Requester(request_handler=MessageHandler(complete_task))
        calls = await request.query(message=MESSAGE.as_object())
        answer_message = calls.send_message.fetchone()
        self.assertEqual(
            answer_message.text,
            "Please enter the id of the task you want to mark as completed:",
        )

    async def test_bot_start(self):
        request = Requester(request_handler=MessageHandler(start))
        calls = await request.query(message=MESSAGE.as_object())
        answer_message = calls.send_message.fetchone()
        self.assertEqual(
            answer_message.text,
            "Welcome to the To-Do List Manager! Use /add to add a task, /delete to delete a task, "
            "/complete to mark a task as completed, /list to view your tasks, and /help for assistance.",
        )

    async def test_bot_help(self):
        request = Requester(request_handler=MessageHandler(help_command))
        calls = await request.query(message=MESSAGE.as_object())
        answer_message = calls.send_message.fetchone()
        help_text = """
    Available commands:\n
    /add - Add a new task\n
    /delete - Delete a task\n
    /complete - Mark a task as completed\n
    /list - List all tasks\n
    /help - Show this help message
    """
        self.assertEqual(answer_message.text, help_text)
