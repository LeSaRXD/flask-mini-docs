from flask import Flask, render_template
import re

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

def add_api_docs(app: Flask, base_url: str = "/api") -> bool:
	if not base_url.startswith("/"):
		return False

	api_requests = []

	for rule in app.url_map.iter_rules():
		rule_url = str(rule)
		if not rule_url.startswith(base_url):
			continue

		if "HEAD" in rule.methods:
			rule.methods.remove("HEAD")
		if "OPTIONS" in rule.methods:
			rule.methods.remove("OPTIONS")
		
		for method in rule.methods:
			current_desc = descriptions.get(rule.endpoint, None)

			endpoint_args = args.get(rule.endpoint, {})
			body_args = endpoint_args.get(method, {})

			if (isinstance(body_args, list)):
				body_args = {key: "str" for key in body_args}
			else:
				body_args = {key: value.__name__ for (key, value) in body_args.items()}

			url_args = {}
			for match in re.finditer(r"<([^:]+):([^:]+)>", rule_url):
				url_args[match[2]] = match[1]
			for match in re.finditer(r"<([^:]+)>", rule_url):
				url_args[match[1]] = "str"

			api_requests.append({
				"url": str(rule),
				"method": method,
				"body_args": body_args,
				"url_args": url_args,
				"description": current_desc
			})

	@app.route(f"{base_url if len(base_url) > 1 else ''}/docs")
	def docs():
		return render_template("api_docs.html", api_requests=api_requests, name=f"{base_url} documentation")

	return True
