
<!-- Summary for one graded assignment for one student.  -->

<template>

  <div v-if="result">

    <h4>
      <img src="@/assets/list.png">
      <span class="report-id">{{result.id}}</span>
      <span>Assignment Week {{ result.assignment.week }}</span>

      <span>for {{ result.student.name }}</span>

      <router-link :to="{name: 'grade-detail', query: {id: result.id} }">Full Report</router-link>
    </h4>

    <p><span class="title">Grade:</span> {{ result.score }}</p>
    <P><span class="title">Overall Instructor Comments:</span></p>
    <textarea v-model="report.overall_instructor_comments" v-on:change="updateInstructorComments"></textarea>
    <P><span class="title">Student GitHub:</span> <a v-bind:href="result.student_github_url">{{ result.student_github_url}}</a></p>
  </div>

  <div v-else>
    <p>No report</p>
  </div>

</template>

<script>

export default {
  name: "GradeResultSummary",
  props: {
    result: Object,
    programmingClass: Object
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
      this.$emit('onUpdateInstructorComments', this.result.id, JSON.stringify(this.report))
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
