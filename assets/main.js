const loader = document.getElementById('loader')
const output = document.getElementById('outputBox')
const fileform = document.getElementById('form')
document.addEventListener('submit', e => {
    const form = e.target;
    const statusBusy = form.querySelector('.status-busy');
    const statusFailure = form.querySelector('.status-failure');
    fetch(form.action, {
        method: form.method,
        body: new FormData(form)
      })
      .then(res => res.text())
      .then(text => new DOMParser().parseFromString(text, 'text/html'))
      .then(doc => {
        const result = document.createElement('div');
        result.innerHTML = doc.body.innerHTML;
        result.tabIndex = -1;
        form.parentNode.replaceChild(result, form);
        result.focus();
      })
    e.preventDefault();
  });