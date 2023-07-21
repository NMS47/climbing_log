function disableButtons(id) {
  if (!id) {
    return; // If id is null or undefined, simply return without doing anything
  }

  for (let i = 0; i < id.length; i++) {
    let target = document.querySelector(id[i]);
    if (target && !target.hasAttribute("disabled")) {
      target.setAttribute("disabled", "true");
    }
  }
}

function enableButtons(id) {
  if (!id) {
    return; // If id is null or undefined, simply return without doing anything
  }

  for (let i = 0; i < id.length; i++) {
    let target = document.querySelector(id[i]);
    if (target && target.hasAttribute("disabled")) {
      target.removeAttribute("disabled");
    }
  }
}