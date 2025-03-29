from user import User


class UserFactory:

    def __init__(self):
        self.users = {}
        self.create_users()
        self.ind = 0

    def create_users(self):
        for i in range(60):
            self.users[i] = User(i)

    def get_user(self,index:int) -> User:
        return self.users[index]

    def __contains__(self, item):
        return item in self.users

    def __iter__(self):
        return self

    def __next__(self) -> User:
        if self.ind < len(self.users):
            nextitem = self.users[self.ind]
            self.ind+=1
            return nextitem
        else:
            raise StopIteration
