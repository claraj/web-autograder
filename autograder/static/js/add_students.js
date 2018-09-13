window.addEventListener('load', e => {

  let more_blanks_button = document.querySelector("#more-blank-fields");

  let new_student_container =  document.querySelector("#new-student-container")
  let blank_fields =  document.querySelector("div.new-student-data")

  more_blanks_button.addEventListener('click', e => {
    let clone_blanks = blank_fields.cloneNode(true)
    console.log(clone_blanks)
    new_student_container.appendChild(clone_blanks)
  });


  let save_new_students = document.querySelector('#submit-new-students')
  save_new_students.addEventListener('click', e => {
    // save all the things

    let students = []

    let new_student_datas = document.querySelectorAll('.new-student-data')

    for (let student_data of new_student_datas) {

      let org_id = student_data.querySelector('.student-org-id').value.trim()
      let name = student_data.querySelector('.student-name').value.trim()
      let github_id = student_data.querySelector('.student-github-id').value.trim()
      let star_id = student_data.querySelector('.student-star-id').value.trim()

      if (!org_id && !name && !github_id && !star_id) {
        continue;   // empty, ignore
      }

      if (!name) {
        alert("all students must have at least a name");
        break;
      }

      students.push({ org_id, name, star_id, github_id } )
    }

    console.log('students', students)

    if (students.length > 0) {

      console.log('there are students, about to fetch. ')

      data = { students, 'csrfmiddlewaretoken': Cookies.get("csrftoken")}

      fetch("manage_students", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "X-CSRFToken": Cookies.get("csrftoken"),
          "Content-Type": "application/json"
         },
         credentials: 'same-origin'
      })
      .then( response => { alert("saved")})
      .catch( err => { alert("error saving")})

    } else {
      alert('enter some student data. All students need a name.')
    }

  })
})
