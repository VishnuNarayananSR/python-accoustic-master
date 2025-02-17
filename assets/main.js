const fileInput = document.getElementById("file");
const submitBtn = document.querySelector(".submit-btn");
const output = document.querySelector(".output");
const warn = document.querySelector(".warning")
let fileToUpload = null;
let type = null
const csrftoken = getCookie('csrftoken');
let formData = new FormData()
fileInput.addEventListener("change", (e) => {
	// Get the selected file
  const [file] = e.target.files;
  fileToUpload = file;
  type = file.type
  formData.append('audiofile', fileToUpload)
	document.querySelector(".selected-file").innerHTML = `${file.name} (${(
		file.size / 1000
	).toFixed(2)}Kb)`;
});

submitBtn.addEventListener("click", (e) => {
  e.preventDefault();
  console.log(type)
  if (!fileToUpload) return;
  if (type.slice(0,5) != 'audio') {
    document.querySelector(".selected-file").innerHTML = `I Expected an audio file but got filetype ${type}`;
    return;
  } 
  if (!type.includes('wav')){
  warn.innerHTML = `Audio formats other than 'wav' loss features due to compression. This might result in low accuracy`;
  }
	upload(fileToUpload);
});

const upload = (file) => {
  let LOADER = "";
  LOADER += `<p>Please wait...</p>
            <div class="loader">
              <div class="line"></div>
              <div class="line"></div>
              <div class="line"></div>
              <div class="line"></div>
            </div>`;
	output.innerHTML = LOADER;

fetch("", {
        method: 'POST',
        body: formData,
        headers: { "X-CSRFToken": csrftoken },
})
		.then(
			(response) => response.json() // if the response is a JSON object
		)
		.then((data) => {
      warn.classList.add("invisible")
			let HTML = `<p>Showing results:</p>`;
			for (const item of data) {
        HTML += `<div class="output-badge">
                  ${item}
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
