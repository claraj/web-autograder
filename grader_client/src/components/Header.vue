<template>
    <header>
      <img src="@/assets/coding.png">
      <h1>Autograder</h1>
    </header>
</template>

<script>

export default {
  name: 'Header',
}

</script>

<style>

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
}

</style>
