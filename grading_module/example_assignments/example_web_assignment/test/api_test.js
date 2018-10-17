const MongoClient = require('mongodb').MongoClient
const dbUrl = require('../src/db_config')

let server = require('../src/app')
let chai = require('chai')
let expect = chai.expect
let chaiHttp = require('chai-http')

chai.use(chaiHttp)
let chai_server = chai.request(server).keepOpen()


describe('api crud tests', () => {

  before('connect to DB and clear data', (done) => {
    this.client = new MongoClient(dbUrl)
    this.client.connect().then( () => {
      this.db = this.client.db('test_todo')
      this.coffeeCollection = this.db.collection('coffeeshops')
      done()
    }).catch(err => {
      console.log(err)
      done(err)
    })
  })

  after('close database connection', (done) => {
    this.client.close()
      .then( () => done())
      .then( () => chai_server.close() )
      .catch(err=> {console.log(err);  done(err)})
  })

  describe('api crud tests with no data in DB', () => {

    beforeEach('clear data', (done) => {
      this.coffeeCollection.deleteMany().then( () => done() ).catch(err=> {console.log(err);  done(err)})
    })

    it('can add a new coffee shop', (done) => {
      chai_server
      .post('/api/v1/coffeeshop')
      .send( {name: 'Java Beans', stars: 4})
      .end( (err, res) => {
        expect(res.status).to.equal(201)
        this.coffeeCollection.find().toArray()
        .then(docs => {
          expect(docs).to.have.lengthOf(1)
          expect(docs[0]).to.have.property('name').equal('Java Beans')
          expect(docs[0]).to.have.property('stars').equal(4)
          done()
        })
        .catch(err=> {console.log(err);  done(err)})
      })
    })


    it('will not a new coffee shop without a name', (done) => {
      chai_server
      .post('/api/v1/coffeeshop')
      .send( {stars: 4})
      .end( (err, res) => {
        expect(res.status).to.equal(400)
        expect(res.error.text).to.include('CoffeeShop validation failed: name: Path `name` is required.')
        this.coffeeCollection.find().toArray()
        .then(docs => {
          expect(docs).to.have.lengthOf(0)
          done()
        })
        .catch(err=> {console.log(err);  done(err)})
      })
    })

  })  // end of crud describe


  describe('api crud tests with test data in DB', () => {

    beforeEach( (done) => {

      example = [
        { name: 'Average Joe', stars: 2},
        { name: 'Cakes and Coffee', stars: 3},
        { name: 'Java Beans', stars: 4},
      ]

      this.coffeeCollection
        .deleteMany({})
        .then( () => {
          this.coffeeCollection.insertMany(example)
            .then( (res) => {
              this.example = res.ops
              this.example.sort( (a, b) =>  a.name > b.name )
              done()
            })
            .catch(err=> {console.log(err);  done(err)})

      } )
      .catch(err=> {console.log(err);  done(err)})
    })

    it('can return a list of coffee shops, sorted in name order', (done) => {

      chai_server
      .get('/api/v1/coffeeshop/')
      .end( (err, res) => {
        let actual = res.body
        expect(actual).to.have.lengthOf(30000)
        for (let s= 0; s < this.example.length; s++) {
          let expectedShop = this.example[s]
          let actualShop = actual[s]
          expect(actualShop).to.have.property('name').equal(expectedShop.name)
          expect(actualShop).to.have.property('stars').equal(expectedShop.stars)
        }
        done()
      })
    })

    it('can change the rating of a coffee shop', (done) => {

      let changeShop = this.example[0]

      chai_server
      .patch(`/api/v1/coffeeshop/${changeShop._id}`)
      .send({ stars: 4})
      .end( (err, res) => {
        this.coffeeCollection.find({name: changeShop.name}).toArray().then(docs => {
          expect(docs).to.have.lengthOf(1)
          expect(docs[0]).to.have.property('stars').equal(4)
          done()
        }).catch(err=> {console.log(err);  done(err)})
      })

    })

    it('can add a new coffee shop', (done) => {
      chai_server
      .post(`/api/v1/coffeeshop/`)
      .send( {name: 'Starblocks', stars: 1})
      .end( (err, res) => {
        expect(res.status).to.equal(201)
        this.coffeeCollection.find({ name: 'Starblocks'})
        .toArray()
        .then( docs => {
          expect(docs).to.have.lengthOf(1)
          expect(docs[0]).to.have.property('name').equal('Starblocks')
          return this.coffeeCollection.find().toArray()
        })
        .then( (docs) => {
          expect(docs).to.have.lengthOf(4)
          done()
        }).catch(err=> {console.log(err);  done(err)})
      })

    })

  })

})
