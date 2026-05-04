from user_admin.entity.UserProf import UserProf


class UserAdminCreateProfileC:
    def createProfile(self, tempProfile):
        return UserProf.createProfile(tempProfile)
