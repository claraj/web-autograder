window.addEventListener('load', e => {

// rules: at least one student should be selected
// exactly one assigment should be selected

// there is at least one assignment and at least one student

  checkCanStart()

  document.querySelector("#grade-button").addEventListener('mouseover', checkCanStart)
  document.querySelector("#error-message").addEventListener('click', checkCanStart)

  document.querySelectorAll(".assignment-radio-button").forEach( btn => btn.addEventListener('click', checkCanStart))
  document.querySelectorAll(".student-checkbox").forEach( btn => btn.addEventListener('click', checkCanStart))
  document.querySelector("#select-all-students").addEventListener('click', checkCanStart)

});




  function checkCanStart() {

      // There is at least one student, and at least one student is checked...

      let grade_button = document.querySelector("#grade-button")
      let message = document.querySelector("#error-message")

      grade_button.disabled = false;
      let message_text = ""

      let checked_student_checkboxes = document.querySelectorAll("input.student-checkbox:checked")
      let checked_assigment_radio_buttons = document.querySelectorAll("input.assignment-radio-button:checked")

      if (  checked_assigment_radio_buttons.length == 0 ) {
        grade_button.disabled = true
        message_text += "Select the assignment to grade. "
      }

      if (  checked_student_checkboxes.length == 0 ) {
        grade_button.disabled = true
        message_text += "Select at least one student. "
      }

      message.innerHTML = message_text

      return !grade_button.disabled  // return true if can start.


  }
