
<template>

  <div>
    <h1>Students</h1>

    <ItemList
      v-bind:items="students"
      v-bind:attributes="attributes"
      @onRequestEdit="onRequestEdit"
      @onRequestDelete="onRequestDelete"
    />

    <div id="newStudent">
      <h2>Add New Students</h2>
      <button @click="showAddStudentModal">Add new student</button>
    </div>

    <AddEditItem
      v-bind:visible="showAddEditModal"
      v-bind:item="focusStudent"
      v-bind:attributes="attributes"
      v-bind:action="action"
      v-bind:errors="errors"
      @onConfirmSubmit="onConfirmSubmit"
      @onCancel="onCancel"
    />


    <BulkAdd
      v-bind:instructions="bulkCSVOrder"
      v-bind:errors="bulkErrors"
      v-bind:countAdded="bulkStudentsAdded"
      v-bind:itemType="itemType"
      @onSubmitBulk="onSubmitBulk"
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
        { attr :'name', display: 'name', regex: /^.+$/, required:true, message: 'Name is required' },
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
      bulkErrors: [],
      bulkCSVOrder: "name,GitHubID,OrgID,StarID",
      bulkStudentsAdded: 0,
      itemType: 'Students'

    }
  },
  mounted () {
    this.fetchStudents()
  },
  methods: {

    /* Fetching students from server */
    fetchStudents() {
      this.$backend.$fetchStudents().then(data => {
        this.students = data
        console.log('Student component fetched these students', this.students)
      })
    },


    onConfirmSubmit(student) {

      this.focusStudent = student

      if (this.action == 'Add Student') {
        this.addStudent()
      }
      else {
        this.editStudent();
      }
    },

    /* Editing student info */
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

    editStudent() {
      const data = this.focusStudent; // { id: this.id, name: this.name, star_id: this.star_id, org_id: this.org_id, github_id:this.github_id }
      this.$backend.$editStudent(data).then( () => {
          this.focusStudent = {}
          this.showAddEditModal = false;
          this.fetchStudents()
        })
    },

    onCancel() {
      this.showAddEditModal = false;
    },


    /* Adding students */
    showAddStudentModal() {
      this.focusStudent = {}
      this.action = "Add Student"
      this.showAddEditModal = true;
    },

    addStudent() {
      const data = this.focusStudent; // { id: this.id, name: this.name, star_id: this.star_id, org_id: this.org_id, github_id:this.github_id }
      this.$backend.$addStudent(data).then( () => {
        this.focusStudent = {}
        this.fetchStudents()
      })
    },

    onSubmitBulk(rawData) {
      console.log('app bulk add')
      console.log(rawData)
      this.$backend.$bulkAdd(rawData).then( (resp) => {
        console.log('server response', resp)
        // this.rawData = ""
        this.bulkStudentsAdded = resp.created
        this.bulkErrors = resp.errors
        this.fetchStudents();
      })
    },


    /* Deleting students */
    onRequestDelete(id) {
      console.log('delete student ', id)
      const student = this.students.filter(student => student.id === id)[0]
      if (student)
      if (confirm(`Delete ${student.name}?`)){
        this.$backend.$deleteStudent(id).then( () => {
          this.fetchStudents()
        })
      }
    },
  }
}

</script>


<style>

  #newStudent {
    padding: 15px;
  }
</style>
