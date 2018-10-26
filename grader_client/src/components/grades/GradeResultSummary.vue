
<!-- Summary for one graded assignment for one student.  -->

<template>

  <div>

    <!-- todo look up student name; assignment name, probably in container component
    Make these clickable to student or assigmment page
    Student page should have all student's assignments and scores
    Assignment page should have all student's results
    -->

    <h4>
      <img src="@/assets/list.png">
      <span class="report-id">{{result.id}}</span>
      <span v-if="result.fullAssignmentInfo">Assignment Week {{ result.fullAssignmentInfo.week }}</span>
      <span v-else>Assignment internal ID: {{ result.assignment }}</span>

      <span v-if="result.fullStudentInfo">for {{ result.fullStudentInfo.name }}</span>
      <span v-else>Student internal ID: {{ result.student }}</span>

  <router-link :to="{name: 'grade-detail', query: {id: result.id} }">Full Report</router-link>
    </h4>

    <!-- <p>Result ID {{ result.id }}</p> -->
    <p><span class="title">Grade:</span> {{ result.score }}</p>

    <P><span class="title">Overall Instructor Comments:</span></p>
      <textarea v-model="report.overall_instructor_comments" v-on:change="updateInstructorComments"></textarea>
    <P><span class="title">Student GitHub:</span> <a v-bind:href="result.student_github_url">{{ result.student_github_url}}</a></p>
  </div>

</template>

<script>

export default {
  name: "GradeResultDetail",
  props: {
    result: Object,
  },
  data() {
    return {
    }
  },
  mounted() {
    console.log('my object is', this.result)
  },
  computed: {
    report: function() {
      return JSON.parse(this.result.generated_report)
    }
  },
  methods: {
    updateInstructorComments() {
      console.log('must save comments for ', this.result.id, this.report)
      this.$emit('onUpdatedInstructorComments', this.result.id, JSON.stringify(this.report))
    }
  }
}

</script>

<style>
  textarea {
    width: 100%;
  }

  .report-id {
    font-weight: lighter;

  }
</style>
