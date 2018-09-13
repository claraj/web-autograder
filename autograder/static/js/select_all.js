window.addEventListener('load', e => {

  // select the first radio button
  let firstRadioButton = document.querySelector('.assignment-radio-button')
  if (firstRadioButton) { firstRadioButton.checked = true; }


  let select_all = document.querySelector("#select-all-students")
  let student_checkboxes = document.querySelectorAll('.student-checkbox')

  select_all.addEventListener("click", () => {

    student_checkboxes.forEach( checkbox => checkbox.checked = select_all.checked )

  })


});
