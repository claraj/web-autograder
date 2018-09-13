window.addEventListener('load', e => {

  let more_blanks_button = document.querySelector("#more-blank-fields");

  let new_student_container =  document.querySelector("#new-student-container")
  let blank_fields =  document.querySelector("div.new-student-data")

  more_blanks_button.addEventListener('click', e => {
    let clone_blanks = blank_fields.clone(False)
    new_student_container.appendChild(clone_blanks)
  });


  let save_new_students = document.querySelector('#submit-new-students')
  save_new_students.addEventListener('click', e => {
    // save all the things

    let new_student_datas = document.querySelectorAll('.new-student-data')
    new_student_datas.forEach( student_data => {
      //TODO VALIDATION!

      //
    })
  })
})
