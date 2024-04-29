from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):
    @task
    def start(self):
        response = self.client.get("/start")


class WebsiteUser(HttpUser):
    wait_time = between(5, 9)
    tasks = {UserBehavior: 1}

    def on_start(self):
        self.client.post(
            "/login", json={"username": "demo", "password": "demo"})


if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.getcwd())
    from aiogram import types
    from loader import dp

    dp.message_handler(commands=["start"])(UserBehavior.start)

    from locust import main
    main()
