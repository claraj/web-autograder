
<template>

  <div>
    <h1>Students</h1>

      <table>
        <tr><th>id</th>
        <th>name</th>
      <th>github</th>
    <th>org id</th>
  <th>star id</th>
</tr>
      <tr v-for="student in students" v-bind:key="student.id">
        <td>{{ student.id}}</td>
        <td>{{student.name}}</td>
        <td>{{ student.github_id}}</td>
        <td>{{ student.org_id}}</td>
        <td>{{ student.star_id}}</td>
        <td><button>Edit</button></td>
        <td><button @click="deleteStudent(student.id)">Delete</button></td>

      </tr>
    </table>

    <div>
    <button @click="addStudent">Add new student</button>
  </div>

    <!--  for dumping a CSV and letting server figure it out -->
    <div>
    <input type="textarea"/>
  </div>

  </div>
</template>

<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }
  tr,td,th,table {
    border: 1px solid black;
  }
</style>

<script>

/* eslint-disable */


export default {
  name: 'Students',
  data () {
    return {
      students: [],
      name: String,
      star_id: String,
      org_id: String,
      github_id: String,
      id: Number
    }
  },
  mounted () {
    this.fetchStudents()
  },
  methods: {
    fetchStudents() {
      this.$backend.$fetchStudents().then(data => {
        this.students = data
        console.log(this.students)
      })
    },
    addStudent() {
      const data = { name: "bork", star_id: "sp1234rk", github_id: "test", org_id: "12345678" }
      this.$backend.$addStudent(data).then( () => {
        this.name = ""
        this.github_id = ""
        this.org_id = ""
        this.star_id = ""

        this.fetchStudents()
      })
    },
    editStudent() {
      const data = { id, name, star_id, org_id, github_id}
      this.$backend.$editStudent(data).then( () => {
        this.name = ""
        this.github_id = ""
        this.org_id = ""
        this.star_id = ""
        this.fetchStudents()
      })
    },
    deleteStudent(id) {
      this.$backend.$deleteStudent(id).then( () => {
          this.fetchStudents()
      })
    }
  }
}

</script>
