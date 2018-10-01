<template>

  <div>

    <!-- todo look up student name; assignment name, probably in container component
    Make these clickable to student or assigmment page
    Student page should have all student's assignments and scores
    Assignment page should have all student's results
    -->

    <h4>Result ID {{ result.id }}</h4>
    <P>Assignment id {{ result.assignment}}</P>
    <P>Student id {{ result.student}}</P>
    <p>Grade {{ result.score }}</p>
    <P>Generated Report {{ result.generated_report}}</p>
    <P>Instructor Comments <textarea v-model="result.instructor_comments" v-on:change="updateInstructorComments"></textarea></P>
    <P>Student GitHub <a v-bind:href="result.student_github_url">{{ result.student_github_url}}</a></p>
  </div>

</template>

<script>

export default {
  name: "GradeResultDetail",
  props: {
    result: Object,
    // assignmentLookup: Object,
    // studentLookup: Object
  },
  data() {
    return {

    }
  },
  mounted() {
    console.log('my object is', this.result)

    // Sort by assignment and then by student
    // TODO get student names and assignment weeks


  },

  methods: {
      updateInstructorComments() {
        console.log('must save comments for ', this.result.id, this.result.instructor_comments)
 // todo emit to parent
        this.$emit('onChildUpdatedInstructorComments', this.result.id, this.result.instructor_comments)
      }
  }
}

</script>
