function disableButtons(id){
    for (i = 0; i < id.length; i++) {
        let target = document.querySelector(id[i])
        if (target.hasAttribute("disabled")==false){
          target.setAttribute("disabled", "true")
        }
      }
      }

  function enableButtons(id){
    for (i = 0; i < id.length; i++) {
      let target = document.querySelector(id[i])
    if (target.hasAttribute("disabled")){
      target.removeAttribute("disabled")
    }
  }
}