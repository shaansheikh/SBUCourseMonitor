from database import Database

__all__ = ['AuthDatabase']

class AuthDatabase(Database):
	def usernameToID(self,username):
		a = self._execute("SELECT userID from Users WHERE identifier=?;",(username,))
		if len(a) > 0:
			return a[0][0]
		return -1

	def isUser(self, username):
		return self._execute("SELECT * FROM Users WHERE identifier=?;",(username,))

	def addUser(self, username):
		if len(self.isUser(username)) ==0:
			self._execute('INSERT INTO Users(medium,identifier,state) values(0,?,1);',(username,))

	def changeState(self, username,state):
		self._execute('UPDATE Users SET state=? WHERE identifier=?;',(state,username))

	def addJob(self,username,coursenum):
		userid = self.usernameToID(username)
		self._execute('INSERT INTO Courses(userID,coursenum) values(?,?)',(userid,coursenum))

	def getJobs(self):
		return self._execute('SELECT * FROM Courses')

	def getFollowingCourses(self,username):
		userID = self.usernameToID(username)
		return self._execute('SELECT coursenum FROM Courses where userID=?',(userID,))

	def addTemp(self,username,id):
		self._execute('UPDATE Users SET temp=? where identifier=?',(id,username))

	def getTemp(self,username):
		return self._execute('SELECT temp FROM Users where identifier=?',(username,))[0][0]

	def getUserByID(self,userid):
		return self._execute('SELECT * FROM Users where userID=?',(userID,))

	def reset(self,username):
		self._execute('DELETE FROM Courses WHERE userID=?',(self.usernameToID(username),))
		self._execute('DELETE FROM Users where identifier=?',(username,))