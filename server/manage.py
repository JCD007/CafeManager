def deploy():
	"""Run deployment tasks."""
	from server import create_server,db
	from flask_migrate import upgrade, migrate, init, stamp
	from models import User, Product

	server = create_server()
	server.app_context().push()
	db.create_all()

	# migrate database to latest revision
	init()
	stamp()
	migrate()
	upgrade()
	
deploy()