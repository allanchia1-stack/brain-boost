from user_admin.controller.UserAdminCreateAccountC import UserAdminCreateAccountC
from user_admin.entity.UserAcct import UserAcct


class CreateUserC(UserAdminCreateAccountC):
    def create_user(self, name, phone, address, role, email, password):
        return self.createAccount(UserAcct(email=email, password=password, name=name, phone=phone, address=address, role=role))
