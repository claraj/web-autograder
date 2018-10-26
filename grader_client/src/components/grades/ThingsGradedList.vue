<template>
  <div>
    <p>
      <span class="title">Students graded: </span>
      <span>{{studentNames}}</span>
    </p>

    <p>
      <span class="title">Assignments graded: </span>
      <span>{{assignmentNames}}</span>
    </p>
  </div>

</template>

<script>

export default {
  name: 'ThingsGradedList',
  props: {
    students: Array,
    assignments: Array
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
        return this.assignments.sort().join(', ')
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

</style>
