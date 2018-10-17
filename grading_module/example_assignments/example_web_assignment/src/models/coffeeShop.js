const mongoose = require('mongoose')
let uniqueValidator = require('mongoose-unique-validator')

let coffeeShopSchema = new mongoose.Schema({
  name: { type: String, required: true, unique: true, trim: true},
  visited: { type: Boolean, default: false },
  stars: { type: Number, min: 0, max: 5}
})

coffeeShopSchema.plugin(uniqueValidator)

let coffeeShop = mongoose.model('CoffeeShop', coffeeShopSchema)
module.exports = coffeeShop
