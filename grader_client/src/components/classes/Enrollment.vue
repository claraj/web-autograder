<!-- For adding students and assignments to classes. -->
<template>
  <div>

    <p>Select a class:</p>

    <select v-on:change="changeClass" v-model="selectedClass">
      <option v-for="programmingClass in programmingClasses" v-bind:value="programmingClass">
        {{programmingClass.name}} {{programmingClass.humanCode}}
      </option>
    </select>

    <p v-if="error">{{error}}</p>

    <div class="grid-container">
      <div class="row">
        <h3>Assignments <span v-if="selectedClass.name"> in {{selectedClass.name}}</span></h3>
        <SelectionList v-bind:items="displayAssignmentsInClass" v-on:itemsSelected="assignmentsInClassSelected"></SelectionList>
        <button v-on:click="removeSelectedAssignments">Remove selected assignments</button>

      </div>

      <div class="row">
        <h3>Students<span v-if="selectedClass.name"> in {{selectedClass.name}}</span></h3>
        <SelectionList v-bind:items="displayStudentsInClass" v-on:itemsSelected="studentsInClassSelected"></SelectionList>
        <button v-on:click="removeSelectedStudents">Remove selected students</button>
      </div>
    </div>
    <hr>

    <div class="grid-container">

      <div class="row">
        <h3>All Assignments</h3>
        <button v-on:click="addSelectedAssignments">Add Selected Assignments to Class</button>
        <div class="filter"><span>Filter?</span> <input v-model="assignmentFilter"/></div>
        <SelectionList v-bind:items="filteredAssignments" v-on:itemsSelected="assignmentsFromAllSelected"></SelectionList>
      </div>

      <div class="row">
        <h3>All Students</h3>
        <button v-on:click="addSelectedStudents">Add Selected Students to Class</button>
        <div class="filter"><span>Filter?</span> <input v-model="studentFilter"/></div>
        <SelectionList v-bind:items="filteredStudents" v-on:itemsSelected="studentsFromAllSelected"></SelectionList>
      </div>
    </div>

  </div>
</div>

</template>
<script>

import SelectionList from '@/components/parts/SelectionList'

export default {
  name: 'Enrollment',
  components: { SelectionList},
  data() {
    return {
      programmingClasses: [],
      selectedClass: {},
      assignmentsInClass: [],
      selectedAssignmentsInClass: [],
      selectedAssignmentsToAdd: [],
      studentsInClass: [],
      selectedStudentsInClass: [],
      selectedStudentsToAdd: [],
      allStudents: [],
      allAssignments: [],
      studentFilter: '',
      assignmentFilter: '',
      error: ''
    }
  },
  computed: {
    filteredStudents: function() {
      let filtered = this.allStudents
      if (this.studentFilter) {
        filtered = this.allStudents
          .filter(st => { return st.name.toLowerCase().includes(this.studentFilter.toLowerCase()) || st.github_id.includes(this.studentFilter)})
        }
      return filtered.map(st => { return {id: st.id, displayText: `${st.name}, GitHub ${st.github_id}`}})
    },
    filteredAssignments: function() {
      let filtered = this.allAssignments
      if (this.assignmentFilter) {
        this.filtered = this.allAssignments
          .filter( as => { return as.week.toString().includes(this.assignmentFilter) || as.instructor_repo.toLowerCase().includes(this.assignmentFilter)})
      }
      return filtered.map(as => { return {id: as.id, displayText: `Week ${as.week}, ${as.instructor_repo}`}} )
    },
    displayStudentsInClass: function() {
      return this.studentsInClass.map( st => { return {id: st.id, displayText: `${st.name}, GitHub ${st.github_id}`}})
    },
    displayAssignmentsInClass: function() {
      return this.assignmentsInClass.map( as => { return {id: as.id, displayText: `Week ${as.week}, ${as.instructor_repo}`}})
    }
  },
  created() {
    this.getAllData()
  },
  methods: {
    getAllData() {
      this.$classes_backend.$fetchItems().then(data => this.programmingClasses = data)
      this.$assignment_backend.$fetchItems().then(data => { this.allAssignments = data; this.assignmentFilter=''})
      this.$student_backend.$fetchItems().then(data => { this.allStudents = data; this.studentFilter='' })
      this.loadItemsForClass()
    },
    changeClass () {
      this.loadItemsForClass()
    },
    loadItemsForClass () {
      if (!this.selectedClass.id) return

      this.$classes_backend.$itemsInCollection(this.selectedClass.id, 'students').then(data => {
        this.studentsInClass = data
      })

      this.$classes_backend.$itemsInCollection(this.selectedClass.id, 'assignments').then(data => {
        this.assignmentsInClass = data
      })
    },

    /* Select and add students to the selected class */

    assignmentsFromAllSelected(items) {
      this.selectedAssignmentsInClass = items
    },
    studentsFromAllSelected(items) {
      this.selectedStudentsInClass = items
    },
    addSelectedStudents () {
      if (!this.selectedClass) { this.error = 'select a class'; return }
      this.error = ''
      console.log('students to add..', this.selectedStudentsInClass)
    },

    addSelectedAssignments () {
      if (!this.selectedClass) { this.error = 'select a class'; return}
      this.error = ''
      console.log('todo add selected asg', this.selectedAssignmentsInClass)
    },

    /* Select and remove students from class */
    assignmentsInClassSelected(items) {
      console.log('todo remove these assigments ', items)
      this.selectedAssignmentsInClass = items
    },
    studentsInClassSelected(items) {
      this.selectedStudentsInClass = items
    },
    removeSelectedStudents () {
      console.log('todo remove these students:', this.selectedStudentsInClass)
    },
    removeSelectedAssignments () {
      console.log('todo remove asgts', this.selectedAssignmentsInClass)
    }
  }
}


</script>

<style>
.grid-container {
  display: grid;
  grid-template-columns: auto auto;
}

.filter {
  padding-top: 5px;
}
</style>
