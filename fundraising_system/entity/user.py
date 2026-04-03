class User:
    def __init__(self, user_id, name, email, role, status="active"):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.status = status

    def suspend(self):
        self.status = "suspended"

    def activate(self):
        self.status = "active"

    def __str__(self):
        return f"{self.user_id} - {self.name} ({self.role}) [{self.status}]"