from flask import Flask, render_template

args = {}
descriptions = {}

def set_args(**kwargs):
	def inner(func):
		args[func.__name__] = kwargs
		return func
	return inner

def set_description(description):
	def inner(func):
		descriptions[func.__name__] = description
		return func
	return inner

def add_api_docs(app: Flask, base_url: str = "/api"):
	api_requests = []

	for rule in app.url_map.iter_rules():
		if not str(rule).startswith(base_url):
			continue
		if "HEAD" in rule.methods:
			rule.methods.remove("HEAD")
		if "OPTIONS" in rule.methods:
			rule.methods.remove("OPTIONS")
		for method in rule.methods:
			endpoint_args = args.get(rule.endpoint, {})
			current_args = endpoint_args.get(method, {})

			if (isinstance(current_args, list)):
				current_args = {key: str for key in current_args}
			current_args = {key: value.__name__ for (key, value) in current_args.items()}

			current_desc = descriptions.get(rule.endpoint, None)

			api_requests.append({"url": str(rule), "method": method, "args": current_args, "description": current_desc})

	@app.route(f"{base_url}/docs")
	def docs():
		return render_template("api_docs.html", api_requests=api_requests, name=f"{base_url} documentation")
