<template>

  <div v-if="programmingClass">
    <h2>Programming Class Details</h2>

    <p><span class="title">ID:</span> {{programmingClass.id}}</p>
    <p><span class="title">Name:</span> {{programmingClass.name}}</p>
    <p><span class="title">Semester Code:</span> {{programmingClass.semester_code}}</p>
    <p><span class="title">Human Semester Code:</span> {{programmingClass.semester_human_string}}</p>

    <button class="neutral-button" v-on:click="edit">Edit</button>

    <AddEditItem
    v-bind:item="programmingClass"
    v-bind:attributes="attributes"
    v-bind:visible="editVisible"
    v-bind:action="action"
    v-bind:name="name"
    v-on:onCancelAddEdit="onCancelEdit"
    v-on:onConfirmAddEditSubmit="onConfirmEdit"
    ></AddEditItem>


    <div>
      <div>
        <h3>Assignments in this class</h3>
        <ul v-if="assignments.length > 0"><li v-for="assignment in assignments">
          <router-link :to="{ name: 'assignment', params: {id: assignment.id} }">id {{assignment.id}}</router-link>,
          Week {{assignment.week}}, <a :href="assignment.instructor_repo">{{assignment.instructor_repo}}</a>
        </li>
      </ul>
      <p v-else>No assignments. <router-link :to="{ name: 'enrollment', query: {selectedClass:programmingClass.id}}">Add some?</router-link></p>
    </div>

    <div>
      <h3>Students in this class</h3>
      <ul v-if="students.length > 0">
        <li v-for="student in students">
          <router-link :to="{ name: 'student', params: {id: student.id} }">id {{student.id}}</router-link>,
          {{student.name}}, GitHub <a :href=" 'https://github.com/' + student.github_id">{{student.github_id}}</a>
        </li>
      </ul>
      <p v-else>No students. <router-link :to="{ name: 'enrollment', query: {selectedClass:programmingClass.id}}">Add some?</router-link></p>

    </div>
  </div>

</div>
<div v-else>
  {{status}}
</div>

</template>

<script>

import AddEditItem from '@/components/parts/AddEditItem'

export default {
  name: 'ProgrammingClassDetail',
  components: { AddEditItem },
  data() {
    return {
      programmingClass: {},
      status: 'Loading programmingClass information...',
      assignments: [],
      students: [],
      attributes: [
              { attr: 'id', display: 'ID', noEdit: true, omitFromForms: true, linkToDetails: true },
              { attr: 'name', display: 'Name' },
              { attr: 'semester_code', display: 'Semester' },
              { attr: 'semester_human_string', display: 'Semester Name', noEdit: true },
            ],
      name: 'Programming Class',
      action: 'Edit',
      editVisible: false
    }
  },
  mounted() {
    let programmingClassId = this.$route.params.id

    let vue = this

    async function getProgrammingClass() {

      let programmingClass = await vue.$classes_backend.$fetchOne(programmingClassId)
      vue.programmingClass = programmingClass

      console.log(programmingClass)

      // Get students enrolled in this class
      // Get assignments assigned in this class
      vue.students = await vue.$enrollment_backend.$fetchProgrammingClassStudents(programmingClassId)
      vue.assignments = await vue.$enrollment_backend.$fetchProgrammingClassAssignments(programmingClassId)

      vue.status = ''

    }
    getProgrammingClass()
  },
  methods:  {
    edit() {
      this.editVisible = true
    },
    onCancelEdit() {
      this.editVisible = false
    },
    onConfirmEdit(editedClass) {
      console.log('edit', editedClass)
      this.editVisible = false
      this.$classes_backend.$editItem(editedClass).then(response => {
        console.log(response.data)
        this.programmingClass = response.data
      })
    }
  }
}

</script>

<style>

  div {
    text-align: left;
  }

</style>
