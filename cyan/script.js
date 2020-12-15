const fileInput = document.getElementById("file");
const submitBtn = document.querySelector(".submit-btn");
const output = document.querySelector(".output");

let fileToUpload = null;

fileInput.addEventListener("change", (e) => {
	// Get the selected file
	const [file] = e.target.files;
	fileToUpload = file;
	document.querySelector(".selected-file").innerHTML = `${file.name} (${(
		file.size / 1000
	).toFixed(2)}Kb)`;
});

submitBtn.addEventListener("click", (e) => {
	e.preventDefault();
	if (!fileToUpload) return;
	upload(fileToUpload);
});

// This will upload the file after having read it
const upload = (file) => {
	output.innerHTML = "Loading...";
	console.log(file);
	fetch("/upload", {
		// Your POST endpoint
		method: "POST",
		body: file, // This is your file object
	})
		.then(
			(response) => response.json() // if the response is a JSON object
		)
		.then((data) => {
			// map your data to html
			let HTML = "";
			for (const item of data) {
				// just an example, map this data accordingly
				HTML += `<div class="post">
                  <h3>${item.title}</h3>
                  <p>${item.body}</p>
                </div>`;
			}
			output.innerHTML = HTML;
		})
		.catch(
			(error) => (output.innerHTML = "Error!") // Handle the error response object
		);
};
