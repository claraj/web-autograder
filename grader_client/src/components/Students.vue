<template>

  <div>
  <h1>Students</h1>
  <ul>
  <li v-for="student in students">{{ student.name}}</li>
  </ul>

  </div>
</template>

<script>

export default {
name: "Students", 
data() {
  return {
    students: []
  }
},
mounted() {
  this.fetchStudents()
},
methods: {
  fetchStudents() {
    this.$backend.$fetchStudents().then(data => {
      this.students = data;
    })
  }
}
}

</script>
