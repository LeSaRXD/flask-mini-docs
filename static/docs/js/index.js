window.addEventListener("load", () => {
	
	for (let title of document.querySelectorAll(".collapse-title")) {
		title.onclick = () => {
			if (title.parentElement.classList.contains("collapsed")) title.parentElement.classList.remove("collapsed");
			else title.parentElement.classList.add("collapsed");
		}
	}

});

let send_request = async (button) => {
	let { url, method } = button.dataset;
	if(!url || !method) return;
	
	let options = {
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},
		method: button.dataset.method,
	};

	for (let arg_input of button.parentElement.querySelectorAll(".arg-input[data-arg-position='url']")) {
		let val = arg_input.value || null;
		if (val && arg_input.dataset.type == "bool") val = arg_input.checked;
		url = url.replace(`<${arg_input.dataset.type}:${arg_input.dataset.arg}>`, val.toString());
	}

	if (method !== "GET") {
		let body = {};
		for (let arg_input of button.parentElement.querySelectorAll(".arg-input[data-arg-position='body']")) {
			let val = arg_input.value || null;
			if (val) {
				if (arg_input.dataset.type == "int") val = parseInt(val);
				else if (arg_input.dataset.type == "float") val = parseFloat(val);
				else if (arg_input.dataset.type == "bool") val = arg_input.checked;
			}
			body[arg_input.dataset.arg] = val;
		}
		options.body = JSON.stringify(body);
	}

	let res = await fetch(url, options);
	
	let res_div = button.parentElement.querySelector(".response");
	res_div.style.display = "block";
	res_div.innerText = `${res.status} ${res.statusText.toLowerCase()}`

	let text = await res.text();
	try {
		let json = JSON.parse(text);
		res_div.innerText += `\n\n${JSON.stringify(json, null, 4)}`;
	} catch (e) {
		if (text.length > 0)
			res_div.innerText += `\n\n${text}`;
	}
}

let clear_request = (button) => {
	let res_div = button.parentElement.querySelector(".response");
	res_div.style.display = "none";
	res_div.innerText = "";	
	for (let arg_input of button.parentElement.querySelectorAll(".arg-input")) {
		arg_input.value = "";
	}
}
