from user_admin.entity.UserAcct import UserAcct


class UserAdminCreateAccountC:
    def createAccount(self, temp):
        print("Executing UserAdminCreateAccountC.createAccount()")
        return UserAcct.createAccount(temp)
