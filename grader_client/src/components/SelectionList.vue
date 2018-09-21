<template>


  <!--  List of things that are checkable -->
  <div>
    <h3>Select...</h3>
    <input v-model="selectAll" type="checkbox">Select all</a>
    <ul>

      <div v-if="items.length">

        <li v-for="item in items">
          <input v-model="item.selected" type="checkbox" onclick="@itemSelected(item.id)"/>
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
  methods: {
    itemSelected() {
      // emit to parent, id + selected (?)
      // or parent can watch?

    }
  }
}

</script>
