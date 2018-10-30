
<template>

  <div>

     <h2>{{student.name}}</h2>

     <p>Name: {{ student.name}} </p>
     <p>GitHub: {{ student.github_id}} </p>
     <p>Star ID: {{ student.star_id}} </p>
     <p>Org ID: {{ student.org_id}} </p>

     <h2>Grades</h2>

      <p>TODO fetch the lastest grades for this student. </p>

<P>

Class Java
Week 1: grade 4/5 link to full report detail http://127.0.0.1:8000/spa/#/gradereportdetail?id=604   [REGRADE BUTTON]
Week 2: grade 6/100 link to full report detail  "       "       "             "         "           [REGRADE BUTTON]

Class Spork Appreciation
Week 4: grade 3/3 link to full report [REGRADE]

</p>

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
    this.id = this.$route.params.id
    this.fetchData()
  },
  methods: {
    fetchData () {

      let vue = this
      async function getStudent() {
        this.student = await vue.$student_backend.$fetchOne(this.id)
        //get student's grades
        // GET /api/grade?student=1  

      }

      getStudent()

  }
  }
}


</script>
