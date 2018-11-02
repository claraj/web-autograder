<template>
  <!--  List of things that are checkable -->
  <div id="content">
    <!-- <h3>Select...</h3> -->
    <input v-model="selectAll" type="checkbox"/><span id="select-all">Select all</span>
    <ul>

      <div v-if="items && items.length > 0 ">
        <li v-for="item in items" :key="item.id">
          <input v-model="item.selected" type="checkbox" v-on:click="itemSelected(item.id, item.selected)"/>
          <span>{{prefix}} {{item.displayText}}</span>
        </li>
      </div>

      <div v-else>
        <p class="empty">No items</p>
      </div>


    </ul>
  </div>

</template>

<script>

export default {
  name: "SelectionList",
  props: {
    items: Array,
    prefix: String
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
      console.log('mod sa')
      this.items.forEach(item => item.selected = this.selectAll)
    },
    items: {
      handler: function() {
        console.log('mod i')
        if (this.items.length == 0) {
          this.selectAll = false
          return
        }
        if (this.items.filter(item => item.selected).length == 0) {
          this.selectAll = false
        }
        if (this.items.filter(item => !item.selected).length == 0) {
          this.selectAll = true
        }
      },
      deep: true
    }
  },
  methods: {
    itemSelected(id, selected) {
      this.$nextTick().then(() => {
      this.$emit('itemsSelected', this.items.filter(i => i.selected))
      })
    }
  }
}

</script>

<style>

div#content {
  text-align: left;
  padding: 5px;
}
ul {
  padding: 0px;
}
li {
  list-style-type: none;
  margin: 0px;
  padding: 0px;
}
.empty {
  font-style: italic;
}

#select-all {
  font-weight: 500;
}
</style>
