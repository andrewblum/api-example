from locust import HttpLocust, TaskSet, task, between


class UserBehavior(TaskSet):
    # def on_start(self):
    #     """ on_start is called when a Locust start before any task is scheduled """
    #     self.login()

    # def on_stop(self):
    #     """ on_stop is called when the TaskSet is stopping """
    #     self.logout()

    # def login(self):
    #     self.client.post("/login", {"username":"ellen_key", "password":"education"})

    # def logout(self):
    #     self.client.post("/logout", {"username":"ellen_key", "password":"education"})

    @task(2)
    def index(self):
        self.client.get("/students/")

    @task(1)
    def profile(self):
        self.client.get("/exams/")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 9)
