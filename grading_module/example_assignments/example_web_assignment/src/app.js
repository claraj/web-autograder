const express = require('express')
const bodyParser = require('body-parser')
const methodOverride = require('method-override')
const mongoose = require('mongoose')
const restify = require('express-restify-mongoose')
const app = express()
const router = express.Router()
const serveStatic = require('serve-static')
const path = require('path')
const dbConfig = require('./db_config')

console.log('the database to use is ', dbConfig)
const staticPath = path.join(__dirname, '..', 'client', 'dist')

console.log(staticPath)
app.use(serveStatic(staticPath))

app.use(bodyParser.json())
app.use(methodOverride())

mongoose.connect(dbConfig)
  .then(() => console.log('Connected'))
  .catch(err => { console.log(err) })

const coffeeShop = require('./models/coffeeShop')

restify.serve(router, coffeeShop, { onError: (err, req, res, next) => {
  const statusCode = req.erm.statusCode
  console.log(err)
  console.log(err.message)
  res.status(statusCode).json({
    message: err.message
  })
}})

app.use(router)

app.listen(process.env.PORT || 3000, () => {
  console.log('Express server on port 3000')
})

module.exports = app
