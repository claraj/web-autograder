
let db_url = process.env.MONGO_URL

if (process.env.NODE_ENV === 'testing') {
  db_url = process.env.MONGO_URL_TEST
}

module.exports = db_url
