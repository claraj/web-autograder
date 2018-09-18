
<template>

  <div>
    <h1>Assignments</h1>

    <table id="assignment-detail-table">
      <tr><th>id</th>
        <th>week</th>
        <th>github base</th>
        <th>instructor repo</th>
        <th>d2l gradebook url</th>
      </tr>
      <tr v-for="assignment in assignments" v-bind:key="assignment.id">
        <td>{{assignment.id}}</td>
        <td>{{assignment.week}}</td>
        <td>{{assignment.github_base}}</td>
        <td>{{assignment.instructor_repo}}</td>
        <td>{{assignment.d2l_gradebook_url}}</td>
        <td><button @click="showEdit(assignment.id)">Edit</button></td>
        <td><button @click="deleteAssignment(assignment.id, assignment.week)">Delete</button></td>

      </tr>
    </table>

    <div>
      <button @click="showAddAssignmentModal">Add new assignment</button>
    </div>

    <!--  for dumping a CSV and letting server figure it out -->
    <div id="bulk-add">
      <h2>Bulk Add</h2>
      <p>Provide data in CSV format in the order <em>week,githubBase,instructorrepo,d2lgradebookurl</em></p>
      <P>Missing fields are ok.</p>
      <textarea rows="6" columns="100" v-model="rawData">bodgdgf dfgdf gdfg dgfdfg</textarea>
      <br>
      <button @click="bulkAdd">Upload</button>

      <ul>
        <li v-for="error in bulkErrors">{{ error }}</li>
      </ul>

      <p>{{ bulkAssignmentsAdded}} assignments added.</p>
    </div>


    <div id="edit-modal" v-if="showEditModal">
      <div id="edit-modal-content">
        <h2>{{action}}</h2>
        <p v-if="errors.length"><b>Fix these errors: </b>
          <ul>
            <li v-for="error in errors">{{ error }}</li>
          </ul>
        </p>

        <label for="week">Week</label>
        <input id="week" required="true" v-model="week" />
        <br>
        <label for="github-base">GitHub Base</label>
        <input id="github-base" v-model="github_base"/>
        <br>
        <label for="instructor-repo">Instructor Repo</label>
        <input id="instructor-repo" v-model="instructor_repo" type="number"/>
        <br>
        <label for="d2l-url">D2L Gradebook URL</label>
        <input id="d2l-url" v-model="d2l_gradebook_url"/>
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

  textarea {
    width: 100%;
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
    width: 200px;
  }

  #edit-modal-content input {
    display: inline-block;
    vertical-align: middle;
    width: 400px;
  }
</style>

<script>

/* eslint-disable */


export default {
  week: 'Assignments',
  data () {
    return {
      assignments: [],
      week: "",
      d2l_gradebook_url: "",
      instructor_repo: "",
      github_base: "",
      id: 0,
      showEditModal: false,
      action: "",
      errors: [],
      rawData: "testing,sdfsdf\ntesting2\ntesting3,gh,qw2323we,12345678",
      bulkErrors: [],
      bulkAssignmentsAdded: 0
    }
  },
  mounted () {
    this.fetchAssignments()
  },
  methods: {
    fetchAssignments() {
      this.$backend.$fetchAssignments().then(data => {
        this.assignments = data
        console.log(this.assignments)
      })
    },
    addAssignment() {
      const data = { id: this.id, week: this.week, d2l_gradebook_url: this.d2l_gradebook_url, instructor_repo: this.instructor_repo, github_base:this.github_base }
      this.$backend.$addAssignment(data).then( () => {
        this.week = ""
        this.github_base = ""
        this.instructor_repo = ""
        this.d2l_gradebook_url = ""
        this.fetchAssignments()
      })
    },
    deleteAssignment(id, week) {
      if (confirm(`Delete ${week}?`)){
        this.$backend.$deleteAssignment(id).then( () => {
          this.fetchAssignments()
        })
      }
    },
    editAssignment() {
      const data = { id: this.id, week: this.week, d2l_gradebook_url: this.d2l_gradebook_url, instructor_repo: this.instructor_repo, github_base:this.github_base }
      this.$backend.$editAssignment(data).then( () => {
        this.week = ""
        this.github_base = ""
        this.instructor_repo = ""
        this.d2l_gradebook_url = ""
        this.fetchAssignments()
      })
    },

    bulkAdd() {
      console.log('app bulk add')
      console.log(this.rawData)
      const rawData = this.rawData;
      this.$backend.$bulkAdd(rawData).then( (resp) => {
        console.log('server response', resp)
        // this.rawData = ""
        this.bulkAssignmentsAdded = resp.created
        this.bulkErrors = resp.errors
        this.fetchAssignments();
      })
    },


    saveAssignment() {
      if (this.action === "Add Assignment") {
        this.hideModal()
        this.addAssignment()
      }
      else {
        this.hideModal()
        this.editAssignment()
      }
    },


    showEdit(id) {
      this.action = "Edit Assignment"
      let toEdit = this.assignments.filter( s => s.id === id)[0]
      this.id = id
      this.week = toEdit.week
      this.d2l_gradebook_url = toEdit.d2l_gradebook_url
      this.instructor_repo = toEdit.instructor_repo
      this.github_base = toEdit.github_base
      this.showEditModal = true
    },

    hideModal() {
      this.showEditModal = false
    },

    showAddAssignmentModal() {
      this.action = "Add Assignment"
      this.week = ""
      this.github_base = ""
      this.instructor_repo = ""
      this.d2l_gradebook_url = ""
      this.showEditModal = true;
    },

    cleanForm() {
      this.week = this.week.trim()
      this.d2l_gradebook_url = this.d2l_gradebook_url.trim()
      this.github_base = this.github_base.trim()
      this.instructor_repo = this.instructor_repo.trim()
    },


    checkForm() {

      this.cleanForm()
      this.errors = []


      if (!this.week) {
        this.errors.push('Name required. ')
      }
      if (this.github_base && !this.validGitHub(this.github_base)) {
        this.errors.push('GitHub week should only be letters, numbers, underscores and hyphens. ')
      }

      if (this.d2l_gradebook_url && !this.validStarId(this.d2l_gradebook_url)) {
        this.errors.push('Star ID should be in the form ab1234cd. ')
      }

      if (this.instructor_repo && !this.validOrgId(this.instructor_repo)) {
        this.errors.push('Org ID should be 8 digits. ')
      }


      console.log(this.errors)

      if (!this.errors.length) {
        console.log('no errors')
        this.saveAssignment()
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
