


def _convert_to_sanic_path(path):
	""" 
	convert based on route syntax.
	"""
	return path.replace("{", "<").replace("}", ">")
