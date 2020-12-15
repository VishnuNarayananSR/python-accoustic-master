const fileInput = document.getElementById("file");
const submitBtn = document.querySelector(".submit-btn");
const output = document.querySelector(".output");
let fileToUpload = null;
const csrftoken = getCookie('csrftoken');

let formData = new FormData()

fileInput.addEventListener("change", (e) => {
	// Get the selected file
	const [file] = e.target.files;
  fileToUpload = file;
  formData.append('audiofile', fileToUpload)
	document.querySelector(".selected-file").innerHTML = `${file.name} (${(
		file.size / 1000
	).toFixed(2)}Kb)`;
});

submitBtn.addEventListener("click", (e) => {
	e.preventDefault();
	if (!fileToUpload) return;
	upload(fileToUpload);
});

const upload = (file) => {
  let LOADER = "";
  LOADER += `<div class="loader">
              <div class="line"></div>
              <div class="line"></div>
              <div class="line"></div>
              <div class="line"></div>
            </div>`;
	output.innerHTML = LOADER;
  console.log(file);
fetch("", {
        method: 'POST',
        body: formData,
        headers: { "X-CSRFToken": csrftoken },
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
                  <div class="output-badge">${item}</div>
                </div>`;
			}
			output.innerHTML = HTML;
		})
		.catch(
			(error) => (output.innerHTML = "Error!") // Handle the error response object
		);
};

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

// const loader = document.getElementById('loader')
// const output = document.getElementById('outputBox')
// const fileform = document.getElementById('form')
// document.addEventListener('submit', e => {
//     const form = e.target;
//     const statusBusy = form.querySelector('.status-busy');
//     const statusFailure = form.querySelector('.status-failure');
//     fetch(form.action, {
//         method: form.method,
//         body: new FormData(form)
//       })
//       .then(res => res.text())
//       .then(text => new DOMParser().parseFromString(text, 'text/html'))
//       .then(doc => {
//         const result = document.createElement('div');
//         result.innerHTML = doc.body.innerHTML;
//         result.tabIndex = -1;
//         form.parentNode.replaceChild(result, form);
//         result.focus();
//       })
//     e.preventDefault();
//   });