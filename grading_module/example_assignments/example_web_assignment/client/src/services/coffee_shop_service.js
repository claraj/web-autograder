import axios from 'axios'

function CoffeeShopService () {
  this.base = '/api/v1'

  this.$crud = axios.create({
    baseURL: this.base,
    headers: {
      'Content-Type': 'application/json'
      // 'Access-Control-Allow-Origin': 'http://127.0.0.1:3000'
    }
  })

  CoffeeShopService.prototype.fetchAll = () => {
    return this.$crud.get(`/coffeeshop/`, {params: {sort: 'name'}})
      .then(response => response.data)
  }

  CoffeeShopService.prototype.updateStars = (id, stars) => {
    return this.$crud.patch(`/coffeeshop/${id}`, {'stars': stars})
  }

  CoffeeShopService.prototype.addNew = (data) => {
    return this.$crud.post(`/coffeeshop`, data)
      .then(response => response.data)
      .catch(err => {
        console.log(err.request)
        throw err.response.data
      })
  }
}

export default new CoffeeShopService()
