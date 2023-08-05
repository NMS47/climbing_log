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

function addMoreEntries() {
  let template1 = document.getElementById("template1");
  let clone1 = template1.cloneNode(true); // Clone the template with its content
  // clone.style.display = "block"; // Make the cloned element visible
  document.getElementById("codeContainer").appendChild(clone1);
}

function removeEntry(element) {
  let parentDiv = element.closest(".select-grade");
  parentDiv.remove()
  
}
