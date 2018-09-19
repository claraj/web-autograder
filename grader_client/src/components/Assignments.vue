
<template>

  <div>
    <h1>Assignment Management</h1>

    <ItemList
      v-bind:items="assignments"
      v-bind:attributes="attributes"
      v-bind:itemType="itemType"
      @onRequestEdit="onRequestEdit"
      @onRequestDelete="onRequestDelete"
    />

    <div id="newAssignment">
      <h2>Add New Assignments</h2>
      <button @click="showAddAssignmentModal">Add new assignment</button>
    </div>

    <AddEditItem
      v-bind:visible="showAddEditModal"
      v-bind:item="focusAssignment"
      v-bind:attributes="attributes"
      v-bind:action="action"
      v-bind:errors="errors"
      @onConfirmSubmit="onConfirmSubmit"
      @onCancel="onCancel"
    />

    <BulkAdd
      v-bind:instructions="bulkCSVOrder"
      v-bind:errors="bulkErrors"
      v-bind:countAdded="bulkAssignmentsAdded"
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
  name: 'Assignments',
  components: { ItemList, BulkAdd, AddEditItem },
  data () {
    return {
      assignments: [],
      attributes: [
        { attr: 'id', display: 'id' },
        { attr :'week', display: 'Week', regex: /^.+$/, required:true, message: 'Name is required' },
        { attr: 'github_base', display: 'GitHub Base', regex: /^[a-zA-Z_\d-]+$/, message: 'GitHub base can only contain letters, numbers _ and -' },
        { attr: 'instructor_repo', display: 'Instructor Repo', required:true },
        { attr:'d2l_gradebook_url', display: 'D2L Gradebook URL' },
        { attr: 'programming_class', display: 'Class Session'}
      ],
      focusAssignment: {},
      id: 0,
      showAddEditModal: false,
      action: "",
      errors: [],
      bulkErrors: [],
      bulkCSVOrder: "Week,GitHub_Base,Instructor_Repo,D2L_Url",
      bulkAssignmentsAdded: 0,
      itemType: 'Assignments'

    }
  },
  mounted () {
    this.fetchAssignments()
  },
  methods: {

    /* Fetching assignments from server */
    fetchAssignments() {
      this.$backend.$fetchAssignments().then(data => {
        this.assignments = data
        console.log('Assignment component fetched these assignments', this.assignments)
      })
    },


    onConfirmSubmit(assignment) {

      this.focusAssignment = assignment

      if (this.action == 'Add Assignment') {
        this.addAssignment()
      }
      else {
        this.editAssignment();
      }
    },

    /* Editing assignment info */
    onRequestEdit(id) {
      console.log('recived request to edit ', id)
      this.focusAssignment = this.assignments.filter( assignment => assignment.id === id)[0]
      console.log('to edit:', this.focusAssignment)
      if (this.focusAssignment) {
        // todo remove ID, should not be edited
        this.showAddEditModal = true
        this.action = 'Edit Assignment'
      }
    },

    editAssignment() {
      const data = this.focusAssignment; // { id: this.id, name: this.name, star_id: this.star_id, org_id: this.org_id, github_id:this.github_id }
      this.$backend.$editAssignment(data).then( () => {
          this.focusAssignment = {}
          this.showAddEditModal = false;
          this.fetchAssignments()
        })
    },

    onCancel() {
      this.showAddEditModal = false;
    },


    /* Adding assignments */
    showAddAssignmentModal() {
      this.focusAssignment = {}
      this.action = "Add Assignment"
      this.showAddEditModal = true;
    },

    addAssignment() {
      const data = this.focusAssignment; // { id: this.id, name: this.name, star_id: this.star_id, org_id: this.org_id, github_id:this.github_id }
      this.$backend.$addAssignment(data).then( () => {
        this.focusAssignment = {}
        this.fetchAssignments()
      })
    },

    onSubmitBulk(rawData) {
      console.log('app bulk add')
      console.log(rawData)
      this.$backend.$bulkAddAssignment(rawData).then( (resp) => {
        console.log('server response', resp)
        // this.rawData = ""
        this.bulkAssignmentsAdded = resp.created
        this.bulkErrors = resp.errors
        this.fetchAssignments();
      })
    },


    /* Deleting assignments */
    onRequestDelete(id) {
      console.log('delete assignment ', id)
      const assignment = this.assignments.filter(assignment => assignment.id === id)[0]
      if (assignment)
      if (confirm(`Delete assignment for week ${assignment.week}?`)){
        this.$backend.$deleteAssignment(id).then( () => {
          this.fetchAssignments()
        })
      }
    },
  }
}

</script>


<style>

  #newAssignment {
    padding: 15px;
  }
</style>
