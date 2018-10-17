<template>
  <div>

    <h1>Coffee Shops</h1>

    <b-container fluid>
      <b-row>
        <b-col>
          <AddCoffeeShop
            v-bind:errors="errors"
            @onAddNew="onAddNew">
          </AddCoffeeShop>
          <img src="../assets/coffee.jpg">
        </b-col>

        <b-col>
          <CoffeeShopList
            v-bind:coffeeShops="coffeeShops"
            v-bind:errors="errors"
            @onStarsChanged="onStarsChanged">
          </CoffeeShopList>
        </b-col>
      </b-row>

    </b-container>

  </div>
</template>

<script>

import CoffeeShopService from '../services/coffee_shop_service'
import CoffeeShopList from './CoffeeShopList'
import AddCoffeeShop from './AddCoffeeShop'

export default {
  name: 'CoffeeShops',
  components: { AddCoffeeShop, CoffeeShopList },
  data () {
    return {
      coffeeShops: [],
      errors: {fetchAll: '', changeStars: '', addNew: ''}
    }
  },
  mounted () {
    this.errors = {fetchAll: '', changeStars: '', addNew: ''}
    this.fetchShops()
  },
  methods: {
    fetchShops () {
      CoffeeShopService.fetchAll()
        .then(data => {
          console.log('COFFEE SHOPS ARE', data)
          this.coffeeShops = data
          this.coffeeShops.forEach(shop => {
            if (!shop.stars) { shop.stars = 0 }
            this.errors.fetchAll = ''
          })
        })
        .catch(err => {
          this.errors.fetchAll = 'Error fetching coffee shops'
          console.log('Error fetching coffee shops', err, this.errors)
        })
    },

    onStarsChanged (id, stars) {
      CoffeeShopService.updateStars(id, stars)
        .then(data => {
          console.log(`updated stars for ${id} to ${stars}`, data)
          this.errors.changeStars = ''
          this.fetchShops()
        })
        .catch(err => {
          this.errors.changeStars = 'Error changing stars'
          console.log(`Error changing stars to ${stars} for id ${id} `, err, this.errors)
        })
    },

    onAddNew (data) {
      CoffeeShopService.addNew(data)
        .then(data => {
          console.log(`added new.`, data)
          this.errors.addNew = ''
          this.fetchShops()
        })
        .catch(err => {
          this.errors.addNew = err.message
          console.log(`Error adding new shop with data ${JSON.stringify(data)} `, err, this.errors)
        })
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

img {
  border-radius: 10px;
  margin: 20px;
}

h1 {
  margin: 20px;
}

</style>
