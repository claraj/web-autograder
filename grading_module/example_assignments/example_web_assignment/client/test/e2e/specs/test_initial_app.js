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
    console.log('deleting all!')
      this.coffee_collection.deleteMany().then((err, reply) =>{
        done()
    }).catch(err => done(err))
  },

  after: function(browser, done) {
    this.client.close()
    done()
  },

  'page load contents correctly': function (browser) {
    // automatically uses dev Server port from /config.index.js
    // default: http://localhost:8080
    // see nightwatch.conf.js
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer)
      .waitForElementVisible('#app', 5000)
      // .assert.elementPresent('.hello')
      .assert.containsText('h1', 'Coffee Shops')
      .assert.elementCount('img', 1)
      .assert.elementPresent('input[id=new-name]')
      .assert.elementPresent('form input[type=range]')
      .assert.containsText('#no-shops', 'No Coffee Shops. Try adding some!')
      // and form and list with no elements in
      .end()
  },

  'can add new coffee shop': function(browser) {
    browser
      .url(browser.globals.devServerURL)
      .waitForElementVisible('#app', 5000)
      .setValue('input[id=new-name]', 'Java Beans')
      // .setValue('form input[type=range]', '3')   // this does not seem to do anything for 'reasons outside Nightwatch's control'
      .setValue('form input[type=range]', [browser.Keys.RIGHT_ARROW, browser.Keys.RIGHT_ARROW ])
      .click('button[id=add-new-button]')
      .waitForElementVisible('li', 1000)
      .assert.elementCount('li', 1)
      .assert.containsText('li', 'Java Beans')
      .assert.containsText('li', '3 stars')
      .end()
  },

  // passes, yay.
  'can\'t add new coffee shop without a name': function(browser) {
    browser
      .url(browser.globals.devServerURL)
      .waitForElementVisible('#app', 5000)
      .click('button[id=add-new-button]')
      .waitForElementVisible('#form-errors', 1000)
      .assert.containsText('#form-errors', 'You must enter a name')
      .assert.elementNotPresent('li')
      .end()
  },
}
