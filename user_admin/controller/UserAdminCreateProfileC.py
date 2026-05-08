from user_admin.entity.UserProf import UserProf


class UserAdminCreateProfileC:

    def createProfile(self, temp):
        print("Running UserAdminCreateProfileC.createProfile")
        return UserProf.createProfile(temp)
    

