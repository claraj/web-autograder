<template>
  <div>

    <h2>Coffee Shop Ratings</h2>

    <div id='errors-fetch' v-if="errors.fetchAll">{{errors.fetchAll}}</div>
    <div id='errors-change-stars' v-if="errors.changeStars">{{errors.changeStars}}</div>

    <div id='no-shops' v-if="!coffeeShops.length">No Coffee Shops. Try adding some!</div>

    <div v-else>
      <p>Change star rating by clicking on the stars for a coffee shop</p>

      <p class="error" v-if="errors.fetchAll">{{errors.fetchAll}}</p>
      <p class="error" v-if="errors.changeStars">{{errors.changeStars}}</p>

      <ul id='coffee-shop-list'>
        <li v-for="shop in coffeeShops" :key="shop._id" v-bind:id="`shop-${shop._id}`">

          {{shop.name}}, {{shop.stars}} <span v-if="shop.stars==1">star</span> <span v-else>stars</span>

          <Stars
            v-bind:stars="shop.stars"
            v-bind:_id="shop._id"
            @onStarsChanged="onStarsChanged">
          </Stars>

        </li>
      </ul>
    </div>
  </div>
</template>

<script>

import Stars from './Stars'

export default {
  name: 'CoffeeShops',
  components: { Stars },
  props: {
    coffeeShops: Array,
    errors: Object
  },
  methods: {
    onStarsChanged (id, stars) {
      this.$emit('onStarsChanged', id, stars)
    }
  }
}

</script>

<style scoped>
ul {
  padding: 0;
}
li {
  margin: 0 10px;
  list-style-type: none;
}
.error {
  color: red;
}
</style>
