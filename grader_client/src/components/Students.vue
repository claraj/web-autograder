
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
      v-bind:attributes="attributes"
      v-bind:action="action"
      v-bind:errors="errors"
      @onConfirmEdit="onConfirmEdit"
      @onCancel="onCancel"
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
        { attr :'name', display: 'name', regex: /^.+$/, message: 'Name is required' },
        {attr: 'github_id', display: 'github id', regex: /^[a-zA-Z_\d-]+$/, message: 'GitHub username can only contain letters, numbers _ and -' },
        {attr: 'org_id', display: 'MCTC id', regex: /^\d{8}$/, message: 'MCTC id should be 8 numbers' },
        {attr:'star_id', display:'star ID', regex: /^[a-z]{2}\d{4}[a-z]{2}$/, message: 'Star ID must be in the form ab1234cd' },
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


    // for example, received from ItemList
    onRequestEdit(id) {
      console.log('recived request to edit ', id)
      this.focusStudent = this.students.filter( student => student.id === id)[0]
      console.log('to edit:', this.focusStudent)
      if (this.focusStudent) {
        // todo remove ID, should not be edited
        this.showAddEditModal = true
        this.action = 'Edit Student'
      }
    },

    onConfirmEdit(student) {
      this.focusStudent = student;
      this.$backend.$editStudent(this.focusStudent).then( () => {
        this.focusStudent = {}
        this.showAddEditModal = false;
        this.fetchStudents()
      })
    },

    onCancel() {
      this.showAddEditModal = false;
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
