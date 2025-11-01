def modifying(func):
	def wrapper(*args, **kwargs):
		result = func(*args, **kwargs)
		from database import db
		db.session.commit()
		db.session.flush()
		return result
	return wrapper