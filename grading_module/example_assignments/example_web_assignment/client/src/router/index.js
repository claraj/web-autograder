import Vue from 'vue'
import Router from 'vue-router'
import CoffeeShops from '@/components/CoffeeShops'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'CoffeeShops',
      component: CoffeeShops
    }
  ]
})
