from flask import render_template
from CTFd.utils import admins_only, is_admin
from CTFd.models import db, Challenges, Keys, Awards, Solves, Files, Tags, Teams
from CTFd import utils
from logging import getLogger, basicConfig,DEBUG,ERROR
from CTFd.plugins import challenges
from CTFd import utils, CTFdFlask
from flask import session




basicConfig(level=ERROR)
logger = getLogger(__name__)

class SmartCityChallenge(Challenges):
	__mapper_args__ = {'polymorphic_identity': 'smart_city'}
	id = db.Column(None, db.ForeignKey('challenges.id'), primary_key=True)
	buildingId = db.Column(db.String(5))

	def __init__(self, name, description, value, category, buildingId, type): 
		self.name = name
		self.description = description
		self.value = value
		self.category = category
		self.type = type
		#smart_city Challenege value
		self.buildingId = buildingId


class SmartCity(challenges.BaseChallenge):
	id = "smart_city"
	name = "smart_city"
	
	def create(request):
		"""
		This method is used to process the challege creation request.
		
		:param request:
		:return:
		"""
		chal = SmartCityChallenge(
			name= request.form['name'],
			description = request.form['description'],
			value = request.form['value'],
			buildingId = request.form['buildingId'],
			type=request.form['type']
		
		)
                
		if 'hidden' in request.form:
			chal.hidden = True
		else:
			chal.hidden = False

		files = request.files.getlist('files[]')
		for f in files:
			utils.upload_file(file=f, chalid=chal.id)


		logger.debug("Genereted buildingId " + chal.buildingId + " for challenge " + chal.name)
		
		db.session.add(chal)
		db.session.commit()  
		

def load(app):
    """load overrides for smart_city to work properly"""
    logger.setLevel(app.logger.getEffectiveLevel())
    app.db.create_all()
    
    #challenges.CHALLENGE_CLASSES["smart_city"] = SmartCity
    #def view_challenges():
        #return render_template('page.html', content="<h1>Challenges are currently closed</h1>")

    # The format used by the view_functions dictionary is blueprint.view_function_name
    #app.view_functions['challenges.challenges_view'] = view_challenges
