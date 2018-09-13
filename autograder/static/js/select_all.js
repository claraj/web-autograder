window.addEventListener('load', e => {

  let select_all = document.querySelector("#select-all-students")
  let student_checkboxes = document.querySelectorAll('.student-checkbox')


  select_all.addEventListener("click", () => {

    student_checkboxes.forEach( checkbox => checkbox.checked = select_all.checked )

  })


});
