/* For editing existing students */

window.addEventListener('load', e => {

  console.log("token is ", Cookies.get("csrftoken"))

  let saveButton = document.querySelector('#submit-student-changes')
  saveButton.addEventListener('click', e => {

    e.preventDefault();

    let student_containers = document.querySelectorAll('.student-data')

    let students = []

    student_containers.forEach( studentEl => {

      let student_pk = studentEl.querySelector('.student-pk').value
      let student_org_id = studentEl.querySelector('.student-org-id').value
      let student_name = studentEl.querySelector('.student-name').value
      let student_star_id = studentEl.querySelector('.student-star-id').value
      let student_github_id = studentEl.querySelector('.student-github-id').value


      students.push( { pk: student_pk, org_id: student_org_id, name: student_name, star_id: student_star_id, github_id: student_github_id} )


    })

    console.log(students)

    data = { students, 'csrfmiddlwaretoken': Cookies.get("csrftoken") }
    console.log('data', data)

    fetch("manage_students", {
      method: "PUT",
      headers: {
        "X-CSRFToken": Cookies.get("csrftoken"),
        "Content-Type": "application/json"
       },
      body: JSON.stringify(data),
      credentials: 'same-origin'
    })
      .then( response => { alert("saved")})
      .catch( err => alert('error saving'));   // TODO

  })

})
