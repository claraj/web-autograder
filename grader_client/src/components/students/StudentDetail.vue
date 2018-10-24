
<template>

  <div>
     All results for one student.
     Links to their assignments at GitHub
     TODO Editable

     <h2>{{student.name}}</h2>

     <p>Name: {{ student.name}} </p>
     <p>GitHub: {{ student.github}} </p>
     <p>Star ID: {{ student.star_id}} </p>
     <p>Org ID: {{ student.org_id}} </p>

     <h2>Assignments</h2>

      <p>TODO fetch the lastest grades for this student. </p>
  </div>

</template>

<script>

export default {
  name: 'StudentDetail',
  data() {
    return {
      student: {},
      id: Number
    }
  },
  mounted() {
    console.log('STUDENT ID', this.$router.params.id)
    this.id = this.$router.params.id
    this.$student_backend.$fetchOne(id).then( data => {
      this.student = data
    })
  }
}


</script>
