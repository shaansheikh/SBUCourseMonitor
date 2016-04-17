from database import Database

__all__ = ['AuthDatabase']

class AuthDatabase(Database):
	def usernameToID(self,username):
		return self._execute("SELECT userID from Users WHERE identifier=?;",(username,))[0][0]

	def isUser(self, username):
		return self._execute("SELECT * FROM Users WHERE identifier=?;",(username,))

	def addUser(self, username):
		if len(isUser) ==0:
			self._execute('INSERT INTO Users(medium,identifier,state) values(0,?,1);',(username,))

	def changeState(self, username,state):
		self._execute('UPDATE Users SET state=? WHERE identifier=?;',(state,username))

	def addJob(self,username,coursenum):
		userid = self.usernameToID(username)
		self._execute('INSERT INTO Courses(userID,coursenum) values(?,?)',(userid,coursenum))

	def getJobs():
		return self._execute('SELECT * FROM Courses')