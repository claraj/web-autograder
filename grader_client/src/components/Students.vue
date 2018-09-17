
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
        <td>{{student.id}}</td>
        <td>{{student.name}}</td>
        <td>{{student.github_id}}</td>
        <td>{{student.org_id}}</td>
        <td>{{student.star_id}}</td>
        <td><button @click="showEdit(student.id)">Edit</button></td>
        <td><button @click="deleteStudent(student.id, student.name)">Delete</button></td>

      </tr>
    </table>

    <div>
      <button @click="showAddStudentModal">Add new student</button>
    </div>

    <!--  for dumping a CSV and letting server figure it out -->
    <div>
      <input type="textarea"/>
    </div>


    <div id="edit-modal" v-if="showEditModal">
      <div id="edit-modal-content">
        <h2>{{action}}</h2>
        <p v-if="errors.length"><b>Fix these errors: </b>
          <ul>
            <li v-for="error in errors">{{ error }}</li>
          </ul>
        </p>

        <label for="name">Name</label>
        <input id="name" required="true" v-model="name" />
        <br>
        <label for="github-id">GitHub ID</label>
        <input id="github-id" v-model="github_id"/>
        <br>
        <label for="org-id">Org ID</label>
        <input id="org-id" v-model="org_id" type="number"/>
        <br>
        <label for="star-id">Star ID</label>
        <input id="star-id" v-model="star_id"/>
        <br>
        <button @click="hideModal">Cancel</button>
        <button @click="checkForm">Save</button>
      </div>
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

  #edit-modal {
    position: fixed;
    z-index: 1;
    height: 100%;
    width: 100%;

    top: 0;
    right: 0;
  }

  #edit-modal-content {
    margin: 40% auto;
    padding: 40;
    background-color: lightgreen;
  }

  #edit-modal-content label {
    display: inline-block;
    vertical-align: middle;
    text-align: right;
    width: 100px;
  }

  #edit-modal-content input {
    display: inline-block;
    vertical-align: middle;
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
      id: Number,
      showEditModal: false,
      action: String,
      errors: []
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
      const data = { id: this.id, name: this.name, star_id: this.star_id, org_id: this.org_id, github_id:this.github_id }
      this.$backend.$addStudent(data).then( () => {
        this.name = ""
        this.github_id = ""
        this.org_id = ""
        this.star_id = ""
        this.fetchStudents()
      })
    },
    deleteStudent(id, name) {
      if (confirm(`Delete ${name}?`)){
        this.$backend.$deleteStudent(id).then( () => {
          this.fetchStudents()
        })
      }
    },
    editStudent() {
      const data = { id: this.id, name: this.name, star_id: this.star_id, org_id: this.org_id, github_id:this.github_id }
      this.$backend.$editStudent(data).then( () => {
        this.name = ""
        this.github_id = ""
        this.org_id = ""
        this.star_id = ""
        this.fetchStudents()
      })
    },


    saveStudent() {
      if (this.action === "Add Student") {
        this.hideModal()
        this.addStudent()
      }
      else {
        this.hideModal()
        this.editStudent()
      }
    },


    showEdit(id) {
      this.action = "Edit Student"
      let toEdit = this.students.filter( s => s.id === id)[0]
      this.id = id
      this.name = toEdit.name
      this.star_id = toEdit.star_id
      this.org_id = toEdit.org_id
      this.github_id = toEdit.github_id
      this.showEditModal = true
    },

    hideModal() {
      this.showEditModal = false
    },

    showAddStudentModal() {
      this.action = "Add Student"
      this.name = ""
      this.github_id = ""
      this.org_id = ""
      this.star_id = ""
      this.showEditModal = true;
    },

    cleanForm() {
      this.name = this.name.trim()
      this.star_id = this.star_id.trim()
      this.github_id = this.github_id.trim()
      this.org_id = this.org_id.trim()
    },


    checkForm() {

      this.cleanForm()
      this.errors = []


      if (!this.name) {
        this.errors.push('Name required. ')
      }
      if (this.github_id && !this.validGitHub(this.github_id)) {
        this.errors.push('GitHub name should only be letters, numbers, underscores and hyphens. ')
      }

      if (this.star_id && !this.validStarId(this.star_id)) {
        this.errors.push('Star ID should be in the form ab1234cd. ')
      }

      if (this.org_id && !this.validOrgId(this.org_id)) {
        this.errors.push('Org ID should be 8 digits. ')
      }


      console.log(this.errors)

      if (!this.errors.length) {
        console.log('no errors')
        this.saveStudent()
      } else {
        console.log('validation errors:', this.errors)
      }
    },

    validGitHub(github) {
      return /^[\S_-]+$/.test(github)
    },
    validStarId(starid) {
      console.log('calidsdfsdg')
      return /^[a-z]{2}\d{4}[a-z]{2}$/.test(starid)
    },
    validOrgId(orgid) {
      return /^\d{8}$/.test(orgid)
    }
  }
}

</script>
