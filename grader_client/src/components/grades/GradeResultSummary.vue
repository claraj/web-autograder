
<!-- Summary for one graded assignment for one student.  -->

<template>

  <div>

    <!-- todo look up student name; assignment name, probably in container component
    Make these clickable to student or assigmment page
    Student page should have all student's assignments and scores
    Assignment page should have all student's results
    -->

    <h4>Result ID {{ result.id }}</h4>

    <P v-if="result.fullAssignmentInfo">Assignment Week: {{ result.fullAssignmentInfo.week }}</P>
    <P v-else>Assignment internal ID: {{ result.assignment }}</P>

    <p v-if="result.fullStudentInfo">Student Name: {{ result.fullStudentInfo.name }}</p>
    <P v-else>Student internal ID: {{ result.student }}</P>

    <p>Grade: {{ result.score }}</p>
    <!-- <P>Generated Report {{result.generated_report}}</p> -->
    <!-- <GeneratedGradeReport v-bind:report="result.generated_report"></GeneratedGradeReport> -->

    <P>Instructor Comments <textarea v-model="result.instructor_comments" v-on:change="updateInstructorComments"></textarea></P>
    <P>Student GitHub <a v-bind:href="result.student_github_url">{{ result.student_github_url}}</a></p>
  </div>

</template>

<script>

// import GeneratedGradeReport from './GeneratedGradeReport'

export default {
  name: "GradeResultDetail",
  // components: { GeneratedGradeReport },
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
        this.$emit('onUpdatedInstructorComments', this.result.id, this.result.instructor_comments)
      }
  }
}

</script>
