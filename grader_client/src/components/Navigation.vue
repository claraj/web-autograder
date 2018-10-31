<template>

  <div id="navigation-links">  
      <p class="nav">
      <router-link to="/students">Student Management</router-link>
      </p>
      <p class="nav">
      <router-link to="/assignments">Assignment Management</router-link>
      </p>
      <p class="nav">
      <router-link to="/classes">Class Management</router-link>
      </p>
      <p class="nav">
      <router-link to="/enrollment">Add Students/Assignments to Classes</router-link>
      </p>
      <p class="nav">
      <router-link to="/graderlaunch">Launch Grader</router-link>
      </p>
      <p class="nav">
      <router-link to="/gradingbatches">Grading Batches and Results</router-link>
      </p>

  </div>
</template>

<script>

export default {
  name: 'App'
}

</script>

<style>

  .nav {
    display: inline;
    margin: 20px;
    white-space: nowrap;
  }
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  color: #2c3e50;
  margin: 30px;

}

#icon-credit {
  padding: 10px;
  font-size: 10px;
}

#content {
    text-align: center;
    padding: 15px;
}

header {
  position: relative;
  padding: 15px;
    border: 1px grey solid;
}

header h1 {
  display: inline-block;
  position: absolute;
  top: -5px;
  padding: 25px;
  margin: 0px;

}

header img {
  height: 63px;
  width: 63px;
  padding-left: 15px;
  /* position: absolute; */

}

</style>
