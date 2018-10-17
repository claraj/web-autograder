<template>

  <div>
    <h2>Add new Coffee Shop</h2>
    <b-form>
      <b-form-input label="Name" v-model="name" placeholder="Name" id="new-name"/>

      <span>How many stars?</span>
      <Stars v-bind:stars="stars" @onStarsChanged="onStarsChanged"></Stars>

      <p id="add-errors" v-if="errors.addNew">{{errors.addNew}}</p>
      <p id="form-errors" v-if="formErrors">{{formErrors}}</p>
      <b-button id="add-new-button" v-on:click="addNewCoffeeShop">Add</b-button>
    </b-form>
  </div>
</template>

<script>

// import CoffeeShopService from '../services/coffee_shop_service'
import Stars from './Stars'

export default {
  name: 'NewCoffeeShop',
  components: { Stars },
  props: {
    errors: Object
  },
  data () {
    return {
      name: '',
      stars: 1,
      formErrors: ''
    }
  },
  methods: {
    onStarsChanged (id, stars) {
      this.stars = stars
    },
    addNewCoffeeShop () {
      if (!this.name) {
        this.formErrors = 'You must enter a name.'
        return
      }
      this.$emit('onAddNew', {name: this.name, stars: this.stars})
      this.name = ''
      this.stars = 1
      this.formErrors = ''
    }
  }
}

</script>
