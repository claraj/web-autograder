<template>
  <div>
    <h3>Students graded:</h3>
    <span v-for="student in students">{{student}}, </span>

    <h3>Assignments graded:</h3>
    <span v-for="assignment in assignments">{{assignment}}, </span>

  </div>
</template>

<script>

export default {
  name: 'ThingsGradedList',
  props: {
    students: Array,
    assignments: Array
  }
}
</script>
