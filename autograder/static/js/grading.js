
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
  })
  .then( res => {
    const reader = res.body.getReader();
    console.log(reader)
    const decoder = new TextDecoder('utf-8')

//https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream
//https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Uint8Array
    const stream = new ReadableStream({
      start(controller) {
        function push() {
          reader.read().then( ({done, value}) => {
            if (done) {
              controller.close()
              return;
            }

            controller.enqueue(value);
            console.log(value)

            let valueString = decoder.decode(value)
            console.log(valueString)

            resultReceived(valueString)
              // string s = value.map( i => )
            // turn to String
            push()
          });
        };
        push()
      }
    });

    return new Response(stream, {headers: { 'Content-Type': 'text/html'} })
    //
  })
  .then( result => {
    console.log('all done', result)
  })
  .catch( err => console.log(err))  // todo do something




})


function resultReceived(result) {

  let resultsList = document.querySelector('#results-list')
  let newListElement = document.createElement('li')
  newListElement.innerHTML = result
  resultsList.appendChild(newListElement)

 }
