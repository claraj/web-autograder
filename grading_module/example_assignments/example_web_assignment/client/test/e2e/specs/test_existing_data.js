/* Tests with existing data in the database */

const MongoClient = require('mongodb').MongoClient
const dbUrl = require('../../../../src/db_config')

module.exports = {

  before: function(browser, done) {
    this.client = new MongoClient(dbUrl)
    this.client.connect().then( () => {
      this.db = this.client.db('test_todo')
      this.coffee_collection = this.db.collection('coffeeshops')
      done()
    }).catch((err) => {
      done(err) // TODO fail test
    })
  },

  beforeEach: function(browser, done) {
      this.coffee_collection.deleteMany()
        .then( () => {
          return this.coffee_collection.insertMany([
            { name: 'Beans', stars: 4},
            { name: 'Sporks', stars: 5},
            { name: 'Pies', stars: 1},
          ])
        })
        .then( () => done() )
        .catch(err => done(err))
  },

  after: function(browser, done) {
    this.client.close()
    done()
  },

  'page load list of coffee shops': function (browser) {
    // automatically uses dev Server port from /config.index.js
    // default: http://localhost:8080
    // see nightwatch.conf.js
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer)
      .waitForElementVisible('#app', 5000)
      .assert.elementCount('li', 3)
      .assert.containsText('li:nth-of-type(1)', 'Beans')
      .assert.containsText('li:nth-of-type(1)', '4 stars')
      .assert.containsText('li:nth-of-type(2)', 'Pies')
      .assert.containsText('li:nth-of-type(2)', '1 star')
      .assert.containsText('li:nth-of-type(3)', 'Sporks')
      .assert.containsText('li:nth-of-type(3)', '5 stars')
      .end()
  },

  'can add new coffee shop to existing list': function(browser) {
    browser
      .url(browser.globals.devServerURL)
      .waitForElementVisible('#app', 5000)
      .setValue('input[id=new-name]', 'Java Beans')
      // .setValue('form input[type=range]', '3')   // this does not seem to do anything for 'reasons outside Nightwatch's control'
      .setValue('form input[type=range]', [browser.Keys.RIGHT_ARROW ])
      .click('button[id=add-new-button]')
      .waitForElementVisible('li:nth-of-type(4)', 1000)
      .assert.elementCount('li', 4)
      .assert.containsText('li:nth-of-type(1)', 'Beans')
      .assert.containsText('li:nth-of-type(1)', '4 stars')
      .assert.containsText('li:nth-of-type(2)', 'Java Beans')
      .assert.containsText('li:nth-of-type(2)', '2 stars')
      .assert.containsText('li:nth-of-type(3)', 'Pies')
      .assert.containsText('li:nth-of-type(3)', '1 star')
      .assert.containsText('li:nth-of-type(4)', 'Sporks')
      .assert.containsText('li:nth-of-type(4)', '5 stars')
      .end()
  },

  'can change rating of existing coffee shops': function(browser) {
    browser
      .url(browser.globals.devServerURL)
      .waitForElementVisible('#app', 5000)
      .setValue('#coffee-shop-list input[type=range]', [browser.Keys.RIGHT_ARROW]) // find first slider and change value to 2
      .refresh()
      .waitForElementVisible('#app', 5000)
      .waitForElementVisible('#coffee-shop-list input[type=range]', 5000)
      .assert.value('#coffee-shop-list input[type=range]', '5')
      .assert.containsText('li:nth-of-type(1)', '5 stars')
      .end()
  },

  'can\'t add a new coffee shop with the same name as an existing coffee shop': function(browser) {
    browser
      .url(browser.globals.devServerURL)
      .waitForElementVisible('#app', 5000)
      .setValue('#new-name', 'Pies')
      .click('#add-new-button')
      .waitForElementVisible('#add-errors', 1000)
      .assert.containsText('#add-errors', 'Error, expected `name` to be unique')
      .assert.elementCount('li', 3) // still 3 coffee shops, no new one
      .end()
  }

}
