from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/books")
        headers = {'actions':[{"name":"delay", "value":"20"}]}