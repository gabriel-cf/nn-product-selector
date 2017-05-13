from ..io.mongoconnector.mongohandler import MongoHandler
from ..model.user import User
from datetime import datetime

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def getUserByID(u_username):
	#Retrieve user from DB
	client = MongoHandler()
	db_user = client.getUsersByParameters(username=u_username, one_only=True)
	user = None
	if not db_user is None:
		# Retrieve username, gender, age and nationality
		username = db_user['login']['username']
       	gender = db_user['gender']
        dateOfBirth = db_user['dob'] #yyyy-mm-dd
        nationality = db_user['nat']
        # Transform string date to date object
        dateOfBirth = datetime.strptime(dateOfBirth.split(' ')[0], '%Y-%m-%d')
        #logger.debug("{};{};{};{}".format(username, gender, dateOfBirth.year, nationality))
        user = User(username, gender, dateOfBirth, nationality)
    else:
    	logger.warning("Could not find user with username '%s'" % u_username)
	
	return user
