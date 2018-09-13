
let grade_button = document.querySelector('#grade-button')
grade_button.addEventListener("click", () => {


  if (!checkCanStart()) { console.log('cant start');
  return }

  // read all the checked stuff and then request server starts grading.


  let checked_student_checkboxes = document.querySelectorAll("input.student-checkbox:checked")
  let checked_assigment_radio_button = document.querySelector("input.assignment-radio-button:checked")

  let grade_student_pks = [...checked_student_checkboxes].map( checkbox => checkbox.id.replace('student-', '') )

  let grade_assignment_pk = checked_assigment_radio_button.id.replace('asgt-', '')

  data = { assignment: grade_assignment_pk, students: grade_student_pks,  'csrfmiddlwaretoken': Cookies.get("csrftoken") }

  fetch('/grade', {
    method: 'POST',
    headers: {
      "X-CSRFToken": Cookies.get("csrftoken"),
      "Content-Type": "application/json"
     },
    body: JSON.stringify(data),
    credentials: 'same-origin'
  }).then()
  .catch()  // todo do something

})
