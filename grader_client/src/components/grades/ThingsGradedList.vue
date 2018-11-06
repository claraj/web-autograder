<template>
  <div>
      <span v-if="programmingClass"><span class="title">Programming class: </span>{{programmingClass.name}}, {{programmingClass.semester_human_string}}<br></span>
      <span class="title">Students graded: </span>
      <span>{{studentNames}}</span>
      <br>
      <span class="title">Assignments graded: </span>
      <span>{{assignmentNames}}</span>
  </div>

</template>

<script>

export default {
  name: 'ThingsGradedList',
  props: {
    students: Array,
    assignments: Array,
    programmingClass: Object
  },
  computed: {
    studentNames: function() {
      if (this.students) {
        return this.students.sort().join(', ')
      }
      return 'None yet...'
    },
    assignmentNames: function() {
      if (this.assignments) {
        return this.assignments.map(a => `Week ${a}`).sort().join(', ')
      }
      return 'None yet...'
    }
  }
}
</script>

<style>

.title {
  font-weight: bold;
}

div {
  text-align: left;
}

</style>
