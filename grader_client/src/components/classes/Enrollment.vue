<!-- For adding students and assignments to classes. -->
<template>
  <div>

    <h3>Add Assignments and Students to Classes</h3>

    Select class: <select v-on:change="onClassChanged" v-model="selectedClass">
      <option v-for="programmingClass in programmingClasses" v-bind:value="programmingClass" v-bind:key="programmingClass.id">
        {{programmingClass.name}}, {{programmingClass.semester_human_string}}
      </option>
    </select>

    <p v-if="error" class="error-message">{{error}}</p>

    <div v-if="selectedClass" class="grid-container">
      <div class="row">
        <h3>Assignments <span v-if="selectedClass.name"> in {{selectedClass.name}}</span></h3>
        <button class="danger-button" v-on:click="removeSelectedAssignments">Remove selected assignments</button>
        <SelectionList v-bind:items="assignmentsInClass"></SelectionList>

      </div>

      <div class="row">
        <h3>Students<span v-if="selectedClass.name"> in {{selectedClass.name}}</span></h3>
        <button class="danger-button" v-on:click="removeSelectedStudents">Remove selected students</button>
        <SelectionList v-bind:items="studentsInClass"></SelectionList>
      </div>
    </div>

    <p v-else>Select a class</p>

    <hr>
    <p v-if="error" class="error-message">{{error}}</p>

    <div class="grid-container">
      <div class="row">
        <h3>All Assignments</h3>
        <button class="action-button" v-on:click="addSelectedAssignments">Add selected assignments to class</button>
        <div class="filter"><span>Search</span> <input v-model="assignmentFilter"/></div>
        <SelectionList v-bind:items="filteredAssignments"></SelectionList>
      </div>

      <div class="row">
        <h3>All Students</h3>
        <button class="action-button" v-on:click="addSelectedStudents">Add selected students to class</button>
        <div class="filter"><span>Search</span> <input v-model="studentFilter"/></div>
        <SelectionList v-bind:items="filteredStudents"></SelectionList>
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
      studentsInClass: [],
      assignmentsInClass: [],
      allStudents: [],
      allAssignments: [],
      studentFilter: '',
      assignmentFilter: '',
      error: '',
      loaded: false,
      initialClass: {}
    }
  },
  computed: {
    filteredStudents: function() {
      if (! this.studentFilter) { return this.allStudents }
      return this.allStudents.filter(st => { return st.name.toLowerCase().includes(this.studentFilter.toLowerCase()) || st.github_id.includes(this.studentFilter)})
    },
    filteredAssignments: function() {
      if (! this.assignmentFilter) { return this.allAssignments }
      return this.allAssignments
          .filter( as => { return as.week.toString().includes(this.assignmentFilter) || as.instructor_repo.toLowerCase().includes(this.assignmentFilter)})
    }
  },
  mounted () {
    this.initialClass = this.$route.query.selectedClass
    this.loadAll()
  },
  methods: {
    loadAll () {
      this.$classes_backend.$fetchItems().then(data => {
        this.programmingClasses = data
        if (!this.loaded && this.initialClass) {
          console.log(this.initialClass, this.prog)
          let selection = this.programmingClasses.find( pc => pc.id==this.initialClass)
          console.log(selection)
          if (selection) { this.selectedClass = selection }
        }
        this.loaded = true
        this.loadItemsForClass()
      })

      this.$assignment_backend.$fetchItems().then(data => {
        this.allAssignments = data
        this.allAssignments.forEach(as => {
          as.displayText = `Week ${as.week}, ${as.instructor_repo}`
        })
      })

      this.$student_backend.$fetchItems().then(data => {
        this.allStudents = data
        this.allStudents.forEach(st => {
          st.displayText = `${st.name}, GitHub ${st.github_id}`
        })
      })
    },
    onClassChanged () {
      this.loadItemsForClass()
    },
    loadItemsForClass () {

      if (!this.selectedClass.id) {
        if (this.programmingClasses[0]) { this.selectedClass = this.programmingClasses[0] } // Select first item in dropdown
        else { return }
      }
      // Create display text for each list item
      this.$enrollment_backend.$fetchProgrammingClassStudents(this.selectedClass.id).then(data => {
        this.studentsInClass = data
        this.studentsInClass.forEach(st => { st.displayText = `${st.name}, GitHub ${st.github_id}`
        })
      })

      this.$enrollment_backend.$fetchProgrammingClassAssignments(this.selectedClass.id).then(data => {
        this.assignmentsInClass = data
        this.assignmentsInClass.forEach(as => {
          as.displayText = `Week ${as.week}, ${as.instructor_repo}`
        })

      })
    },
    addSelectedStudents () {

      if (!this.selectedClass) { this.error = 'select a class'; return }
      let studentsToAdd = this.allStudents.filter(s => s.selected).map(s => s.id)
      if (studentsToAdd.length == 0)  {
        this.error = 'Select at least one student'
        return
      }
      this.error = ''
      this.$enrollment_backend.$addStudentsToProgrammingClass(this.selectedClass.id, studentsToAdd).then( () => {
        this.loadAll()
      })

    },
    addSelectedAssignments () {
      if (!this.selectedClass) { this.error = 'select a class'; return}
      let assignmentsToAdd = this.allAssignments.filter(a => a.selected).map(a => a.id)
      if (assignmentsToAdd.length == 0) {
        this.error = 'Select at least one assignment';
        return}
      this.error = ''
      this.$enrollment_backend.$addAssignmentsToProgrammingClass(this.selectedClass.id, assignmentsToAdd).then( () => {
        this.loadAll()
      })
    },

    removeSelectedStudents () {

      if (!this.selectedClass) { this.error = 'select a class'; return }
      let studentsToRemove = this.studentsInClass.filter(s => s.selected).map(s => s.id)
      if (studentsToRemove.length == 0) {
        this.error = 'Select at least one student to remove';
        return
      }
      this.error = ''

      this.$enrollment_backend.$removeStudentsFromProgrammingClass(this.selectedClass.id, studentsToRemove).then( () => {
        this.loadAll()
      })
    },

    removeSelectedAssignments () {
      if (!this.selectedClass) { this.error = 'select a class'; return }
      let assignmentsToRemove = this.assignmentsInClass.filter(a => a.selected).map(a => a.id)
      if (assignmentsToRemove.length == 0) {
        this.error = 'Select at least one assignment to remove'
        return
      }
      this.error = ''
      this.$enrollment_backend.$removeAssignmentsFromProgrammingClass(this.selectedClass.id, assignmentsToRemove).then( () => {
        this.loadAll()
      })
    }
  }
}
</script>

<style>
.grid-container {
  display: grid;
  grid-template-columns: 50% 50%;
}

.filter {
  padding: 15px 0 5px 0;
}

.filter span {
  float: left;
  padding-right: 10px;
}
.filter input {
}

li {
  word-wrap: break-word;
}


button {
  border-radius: 5px;
  box-shadow: 0 2px 5px 0 rgba(0,0,0,0.2), 0 3px 5px 0 rgba(0,0,0,0.19);
}

.add-button {
  background-color: #DAF7A6;
}

.remove-button {
  background-color: #cc3300;
  color: white
}
</style>
