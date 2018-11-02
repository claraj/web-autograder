<!-- details about one assignment, possibly students who have completed it?  -->

<template>

  <div v-if="assignment">
    <h2>Assignment Details</h2>

    <p><span class="title">ID:</span> {{assignment.id}}</p>

    <p v-if="assignment.programming_classes">
      <span class="title">Programming classes:</span>
        <li v-for="pc in assignment.programming_classes">
          <router-link :to="{ name: 'programmingclass', params: {id: pc.id} }">{{pc.name}}</router-link></router-link>, {{pc.semester_human_string}}</li>
    </p>

    <p><span class="title">Week:</span> {{assignment.week}}</p>
    <p><span class="title">GitHub organization:</span> {{assignment.github_org}}</p>
    <p><span class="title">Github assignment base:</span> {{assignment.github_base}}</p>
    <p><span class="title">Instructor repo:</span> <a :href="assignment.instructor_repo">{{assignment.instructor_repo}}</a></p>
    <p><span class="title">D2L gradebook:</span> <a :href="assignment.d2l_gradebook_url">{{assignment.d2l_gradebook_url}}</a></p>

    <button class="neutral-button" v-on:click="edit">Edit</button>

    <AddEditItem
    v-bind:item="assignment"
    v-bind:attributes="attributes"
    v-bind:visible="editVisible"
    v-bind:action="action"
    v-bind:name="name"
    v-on:onCancelAddEdit="onCancelEdit"
    v-on:onConfirmAddEditSubmit="onConfirmEdit"
    ></AddEditItem>

  </div>
  <div v-else>
    {{status}}
  </div>

</template>

<script>

import AddEditItem from '@/components/parts/AddEditItem'


export default {
  name: 'AssignmentDetail',
  components: { AddEditItem },
  data() {
    return {
      assignment: {},
      status: 'Loading assignment information...',
      attributes: [
          { attr: 'id', display: 'id', noEdit: true, omitFromForms: true, linkToDetails: true},
          { attr :'week', display: 'Week', regex: /^.+$/, required:true, message: 'Name is required' },
          { attr: 'github_base', display: 'GitHub Base', regex: /^[a-zA-Z_\d-]+$/, required: true, message: 'GitHub base can only contain letters, numbers _ and -' },
          { attr: 'github_org', display: 'GitHub Organization', required:true },
          { attr: 'instructor_repo', display: 'Instructor Repo', required:true, hyperlink: true },
          { attr: 'd2l_gradebook_url', display: 'D2L Gradebook URL', hyperlink: true },
        ],
      name: 'Assignment',
      action: 'Edit',
      editVisible: false
    }
  },
  mounted() {
    let assignment_id = this.$route.params.id

    let vue = this

    async function getAssignment() {

      let assignment = await vue.$assignment_backend.$fetchOne(assignment_id)
      vue.assignment = assignment

      console.log(assignment)

      let prog_classes = []

      for (const pc of assignment.programming_classes) {
        let res = await vue.$classes_backend.$fetchOne(pc)
        prog_classes.push(res)
      }

      vue.assignment.programming_classes = prog_classes
    }

    getAssignment()
  },
  methods:  {
    edit() {
      this.editVisible = true
    },
    onCancelEdit() {
      this.editVisible = false
    },
    onConfirmEdit(edited) {
      this.editVisible = false
      this.$assignment_backend.$editItem(edited).then(response => {
        this.assignment = response.data
      })
    }
  }
}

</script>

<style>

div {
  text-align: left;
}
.title {
  font-weight: bold;
}
</style>
