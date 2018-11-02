<template>
  <div id="app">

    <Header></Header>

    <div id="content">

      <Navigation></Navigation>
      <router-view/>

    </div>

    <Footer></Footer>

  </div>
</template>

<script>

import Header from '@/components/Header.vue'
import Navigation from '@/components/Navigation.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'App',
  components: { Navigation, Header, Footer }
}

</script>

<style>

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 30px;
}

#content {
    text-align: center;
    padding: 15px;
}

.error-message {
  font-weight: bold;
  color: darkred;
}

.warning-message {
  font-weight: bold;
  font-style: italic;
  color: #600826;
}

button {
  padding-bottom: 3px;
  border-radius: 5px;
  margin: 3px;
  box-shadow: 1px 2px 5px 0 rgba(0,0,0,0.2)
}

.danger-button {
  background-color: #cc3300; /* Orange-red */
  color: white;
}

.action-button {
  background-color: #DAF7A6;  /* Light green */
}

.important-button {
  background-color: orange;
}

.neutral-button {
  background-color: lightblue;
}

.title {
  font-weight: bold;
}

</style>
