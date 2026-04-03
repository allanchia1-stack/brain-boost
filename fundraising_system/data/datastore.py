class DataStore:
    def __init__(self):
        self.users = []
        self.user_profiles = []
        self.user_accounts = []
        self.activities = []
        self.favourites = []
        self.donations = []
        self.categories = []
        self.reports = []

    def generate_id(self, prefix, collection):
        return f"{prefix}{len(collection) + 1}"