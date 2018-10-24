<template>
  <div id="app">

    <header>
      <img src="./assets/coding.png">
      <h1>Autograder</h1>
    </header>

    <div id="content">

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
      <router-link to="/graderlaunch">Launch Grader</router-link>
      </p>
      <!-- <p class="nav">
      <router-link to="/graderresults">Grader Results</router-link>
      </p> -->
      <p class="nav">
      <router-link to="/gradingbatches">Grading Batches</router-link>
      </p>


    <router-view/>

    </div>

    <div id='icon-credit'>Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

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
    padding: 20px;
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
