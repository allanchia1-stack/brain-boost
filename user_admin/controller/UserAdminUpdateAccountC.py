from user_admin.entity.UserAcct import UserAcct


class UserAdminUpdateAccountC:
    @staticmethod
    def updateUser(tempAccount):
        return UserAcct.updateUser(tempAccount)
