from flask import Flask, render_template, request
from api_docs import *

app = Flask(__name__)

test_list = []

def get_item(index):
	item = test_list[index]
	if item is None:
		return ("Index outside of list", 400)

	return {"item": item, "total": len(test_list)}

def put_item(json):
	item = json.get("item", None)
	if item is None:
		return ("Provide an item", 400)
	
	test_list.append(item)
	return ({"item": item, "total": len(test_list)}, 201)

def remove_item(json):
	item = json.get("item", None)
	if item is None:
		return ("Provide an item", 400)
	
	try:
		test_list.remove(item)
	except:
		return ("Item not in list", 400)

	return {"removed_item": item, "total": len(test_list)}

def rename_item(json):
	old_item = json.get("old_item", None)
	new_item = json.get("new_item", None)
	if old_item is None or new_item is None:
		return ("Provide an old and new item names", 400)

	index = -1
	try:
		index = test_list.index(old_item)
	except:
		return ("Item not in list", 400)
	test_list[index] = new_item
	return {"renamed_item": {"old": old_item, "new": new_item}, "total": len(test_list)}

@set_args(PUT={"item": str}, DELETE={"item": str}, PATCH={"old_item": str, "new_item": str})
@app.route("/api/item_list", methods=["GET", "PUT", "DELETE", "PATCH"])
def item_list():
	if request.method == "GET":
		return test_list
	if request.method == "PUT":
		return put_item(request.get_json())
	if request.method == "DELETE":
		return remove_item(request.get_json())
	if request.method == "PATCH":
		return rename_item(request.get_json())

@app.route("/api/item_list/<int:index>", methods=["GET"])
@set_description("These don't work yet :c")
def get_item(index):
	return get_item(index)

@app.route("/api/test", methods=["POST"])
@set_args(POST={"key": int})
@set_description("Here's a description")
def print_num_plus_1():
	json = request.get_json()
	print(json)
	return f"{float(json.get('key', 0)) + 1}"

if __name__ == "__main__":
	add_api_docs(app)
	app.run(debug=True)
