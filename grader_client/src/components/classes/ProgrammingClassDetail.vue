<!--



TODO


MAKE INTO PROGRAMMING CLASS

 details about one programmingClass, possibly students who have completed it?  -->

<template>

  <div v-if="programmingClass">
    <h2>ProgrammingClass Details</h2>

    <p><span class="title">ID:</span> {{programmingClass.id}}</p>

    <p v-if="programmingClass.programming_classes">
      <span class="title">Programming classes:</span>
        <li v-for="pc in programmingClass.programming_classes">
          <router-link :to="{ name: 'programmingclass', params: {id: pc.id} }">{{pc.name}}</router-link></router-link>, {{pc.semester_human_string}}</li>
    </p>

    <p><span class="title">Week:</span> {{programmingClass.week}}</p>
    <p><span class="title">GitHub organization:</span> {{programmingClass.github_org}}</p>
    <p><span class="title">Github programmingClass base:</span> {{programmingClass.github_base}}</p>
    <p><span class="title">Instructor repo:</span> <a :href="programmingClass.instructor_repo">{{programmingClass.instructor_repo}}</a></p>
    <p><span class="title">D2L gradebook:</span> <a :href="programmingClass.d2l_gradebook_url">{{programmingClass.d2l_gradebook_url}}</a></p>

  </div>
  <div v-else>
    {{status}}
  </div>

</template>

<script>

export default {
  name: 'ProgrammingClassDetail',
  data() {
    return {
      programmingClass: {},
      status: 'Loading programmingClass information...'
    }
  },
  mounted() {
    let programmingClass_id = this.$route.params.id

    let vue = this

    async function getProgrammingClass() {

      let programmingClass = await vue.$programmingClass_backend.$fetchOne(programmingClass_id)
      vue.programmingClass = programmingClass

      console.log(programmingClass)

      let prog_classes = []

      for (const pc of programmingClass.programming_classes) {
        let res = await vue.$classes_backend.$fetchOne(pc)
        prog_classes.push(res)
      }

      vue.programmingClass.programming_classes = prog_classes
    }

    getProgrammingClass()
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
