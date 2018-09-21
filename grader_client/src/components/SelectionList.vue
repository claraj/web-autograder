<template>


  <!--  List of things that are checkable -->
  <div>
    <h3>Select...</h3>
    <input v-model="selectAll" type="checkbox">Select all</a>
    <ul>

      <div v-if="items.length">

        <li v-for="item in items">
          <input v-model="item.selected" type="checkbox" v-on:click="itemSelected(item.id)"/>
          <span>{{item.displayText}}</span>
        </li>
      </div>

      <div v-else>
        <p>No items</p>
      </div>


    </ul>
  </div>

</template>

<script>

export default {
  name: "SelectionList",
  props: {
    items: Array
  },
  data() {
    return {
      selectAll: false
    }
  },
  mounted() {
    console.log('list items:', this.items)
  },
  watch: {
    selectAll: function() {
      this.items.forEach(item => item.selected = this.selectAll)
    }
  },
  methods: {

    itemSelected(id) {
      // emit to parent, id + selected (?)
      // or parent can watch?
      console.log('hello, item id', id)

    }
  }
}

</script>
