
<template>

  <div>
    
     <h2>{{student.name}}</h2>

     <p>Name: {{ student.name}} </p>
     <p>GitHub: {{ student.github_id}} </p>
     <p>Star ID: {{ student.star_id}} </p>
     <p>Org ID: {{ student.org_id}} </p>

     <h2>Grades</h2>

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
    console.log('STUDENT ID', this.$route.params.id)
    this.id = this.$route.params.id
    this.$student_backend.$fetchOne(this.id).then( data => {
      this.student = data
    })
  }
}


</script>
