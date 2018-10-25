
<template>
<div>
  <p>{{report}}</p>

  <div v-if="formattedReport.error">
    <P>Error running grader</p>
      <p>{{formattedReport.message}}</p>
  </div>
  <div v-else>
    <P>Messages</p>
    <p v-for="msg in formattedReport">{{msg}}</p>

    <table>
      <th>
        <td>Question</td>
        <td>Test Files</td>
        <td>Messages</td>
        <td>Points</td>
        <td>Adjusted Points</td>
        <td>Comments</td>
      </th>
      <tr v-for:"question in reports">
        <td>{{question.number}}</td>
        <td>{{question.testfiles}}</td>
        <td>{{question.messages}}</td>
        <td>{{question.points}}</td>
        <td><input v-model:"question.adjustedPoints" v-on:"adjustPoints(question.id)"></td>
        <td><input v-model:"question.comments" v-on:"editComments(question.id)"</td>
      </tr>
    </table>

  </div>
</div>

</template>

<script>

export default {
  name: "GeneratedGradeReport",
  props: {
    report: String
  },
  data() {
    return {

    }
  },
  computed: {
    formattedReport: function() {
      if (this.report.startsWith('Error running grader because')) {
        return {
          error: true,
          message: this.report.replace('Error running grader because', '')
        }
      }
      else {
        return this.report.split('/n')  // TODO


        /*

        Structure:

        question  testfile   messages  grade for q  edited grade for q (textbox)  comments

        */
      }
    }
  }
}


</script>

<!--  examples -->

<!-- Error running grader because
error cloning kjkljkjkjkljkl into /Users/admin/Development/pyth......
-->


<!--Q: {'question': 1, 'source_file': 'hello', 'points': 5,
'test_files':
['test_hello.TestHello']}, file hello, reports ['test_hello.TestHello'], pts 5, earned 0, Messages: 'hello' != 'goodbye' - hello + goodbye : The hello function should return the string "Hello".

Q: {'question': 1, 'source_file': 'author_book', 'points': 15, 'test_files': ['test_author_book.TestAuthorBook']}, file author_book, reports ['test_author_book.TestAuthorBook'], pts 15, earned 0,
Messages:
module 'lab_questions.author_book' has no attribute 'add_book'
 module 'lab_questions.author_book' has no attribute 'add_book'
 module 'lab_questions.author_book' has no attribute 'delete_book'
 module 'lab_questions.author_book' has no attribute 'delete_book'
 module 'lab_questions.author_book' has no attribute 'edit_book'
 module 'lab_questions.author_book' has no attribute 'edit_book' module 'lab_questions.author_book' has no attribute 'find_book' module 'lab_questions.author_book' has no attribute 'find_book' module 'lab_questions.author_book' has no attribute 'view_books'
-->
