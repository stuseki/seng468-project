from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    
    @task(1)
    def login(self):
        self.client.post("/auth/login", json={"username":"foo", "password":"bar"})
    
    @task(2)
    def home(self):
        headers = {"Authorization": "Bearer 1HfCiT9fOIFyp8DwbpC8L0cKpcvx3oyn"}
        self.client.get("/documents", headers=headers)
        self.client.get("/search?q=test", headers=headers)
        
    @task(2)
    def upload(self):
        headers = {"Authorization": "Bearer 1HfCiT9fOIFyp8DwbpC8L0cKpcvx3oyn"}
        with open("app/uploads/locust.pdf", "rb") as file:
            self.client.post("/documents", headers=headers, files={"file": file})
            
