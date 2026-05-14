from user_admin.entity.UserAcct import UserAcct


class UserAdminUpdateAccountC:
    @staticmethod
    def updateUser(tempAccount):
        #print("Executing UserAdminUpdateAccountC.updateUser()")
        return UserAcct.updateUser(tempAccount)
