
<template>

  <div>
    <h1>Students</h1>

    <ItemList
      v-bind:items="students"
      v-bind:attributes="attributes"
      @onRequestEdit="onRequestEdit"
    />

    <div>
      <button @click="showAddStudentModal">Add new student</button>
    </div>

    <!-- <BulkAdd/> -->

    <AddEditItem
      v-bind:visible="showAddEditModal"
      v-bind:item="focusStudent"
      v-bind:action="action"
      @onConfirmEdit="onConfirmEdit"
    />

  </div>
</template>

<script>

/* eslint-disable */

import ItemList from './ItemList.vue'
import BulkAdd from './BulkAdd.vue'
import AddEditItem from './AddEditItem.vue'

export default {
  name: 'Students',
  components: { ItemList, BulkAdd, AddEditItem },
  data () {
    return {
      students: [],
      attributes: [
        { attr: 'id', display: 'id' },
        { attr :'name', display: 'name' },
        {attr: 'github_id', display: 'github id'},
        {attr: 'org_id', display: 'MCTC id'},
        {attr:'star_id', display:'star ID'},
        { attr: 'programming_class', display: 'class session'}
      ],
      focusStudent: {},
      id: 0,
      showAddEditModal: false,
      action: "",
      errors: [],
      rawData: "testing,sdfsdf\ntesting2\ntesting3,gh,qw2323we,12345678",
      bulkErrors: [],
      bulkStudentsAdded: 0
    }
  },
  mounted () {
    this.fetchStudents()
  },
  methods: {

    onRequestEdit(id) {
      console.log('recived request to edit ', id)
      // populate this student's id etc.
      this.focusStudent = this.students.filter( student => student.id === id)[0]
      if (this.focusStudent) {
        this.showAddEditModal = true
        this.action = 'Edit Student'
      }
    },

    onConfirmEdit(id) {
      this.$backend.$editStudent(focusStudent).then( () => {
        this.focusStudent = {}
        this.fetchStudents()
      })
    },

    fetchStudents() {
      this.$backend.$fetchStudents().then(data => {
        this.students = data
        console.log('Student component fetched these students', this.students)
      })
    },

    addStudent() {
      const data = this.focusStudent; // { id: this.id, name: this.name, star_id: this.star_id, org_id: this.org_id, github_id:this.github_id }
      this.$backend.$addStudent(data).then( () => {
        // this.name = ""
        // this.github_id = ""
        // this.org_id = ""
        // this.star_id = ""
        this.focusStudent = {}
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
    //editStudent() {
      // const data = { id: this.id, name: this.name, star_id: this.star_id, org_id: this.org_id, github_id:this.github_id }
      // this.$backend.$editStudent(data).then( () => {
      //   this.name = ""
      //   this.github_id = ""
      //   this.org_id = ""
      //   this.star_id = ""
      //   this.fetchStudents()
      // })
    //},

    bulkAdd() {
      console.log('app bulk add')
      console.log(this.rawData)
      const rawData = this.rawData;
      this.$backend.$bulkAdd(rawData).then( (resp) => {
        console.log('server response', resp)
        // this.rawData = ""
        this.bulkStudentsAdded = resp.created
        this.bulkErrors = resp.errors
        this.fetchStudents();
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



<style>
  /* table {
    width: 100%;
    border-collapse: collapse;
  }
  tr,td,th,table {
    border: 1px solid black;
  } */

  /* textarea {
    width: 100%;
  }

*/
</style>
