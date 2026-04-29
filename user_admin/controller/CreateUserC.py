from user_admin.entity.UserAcct import UserAcct

class CreateUserC:
    def create_user(self, name, phone, address, role, email, password):
        # Add basic validation here if needed
        return UserAcct.create_user(name, phone, address, role, email, password)