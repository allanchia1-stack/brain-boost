from user_admin.entity.UserAcct import UserAcct


class UserAdminCreateAccountC:
    def createAccount(self, tempAccount):
        return UserAcct.createAccount(tempAccount)
