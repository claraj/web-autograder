window.addEventListener('load', e => {

// rules: at least one student should be selected
// exactly one assigment should be selected

// there is at least one assignment and at least one student


  let grade_button = document.querySelector("#grade-button")
  let message = document.querySelector("#error-message")

  checkCanStart()

  grade_button.disabled = true;

  grade_button.addEventListener('mouseover', checkCanStart)
  grade_button.addEventListener('click', checkCanStart)

  document.querySelectorAll(".assigment-radio-button").forEach( btn => btn.addEventListener('click', checkCanStart))
  document.querySelectorAll(".student-checkbox").forEach( btn => btn.addEventListener('click', checkCanStart))



  function checkCanStart() {
    console.log('event!')

      // There is at least one student, and at least one student is checked...

      let student_checkboxes = document.querySelectorAll("input.student-checkbox:checked")
      let assigment_radio_buttons = document.querySelectorAll("input.assignment-radio-button:checked")

      if (  student_checkboxes.length == 0 ) {
        grade_button.disabled = true
        message.innerHTML = "Select at least one student."
        return
      }

      if (  assigment_radio_buttons.length == 0 ) {

      grade_button.disabled = true
      message.innerHTML = "Select at least one student."
      return
      }

      grade_button.disabled = false
      message.innerHTML = ""


  }

});
