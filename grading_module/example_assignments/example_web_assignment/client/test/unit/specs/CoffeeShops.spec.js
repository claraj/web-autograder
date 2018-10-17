/*
TODO does this contain a AddCoffeeShop and a CoffeeShopList ?

// mock emit message rec'd from list and assert data updates
// mock emit message rec'd from add and assert data updates

// mock/spy the CoffeeShopService methods

*/

import { mount } from '@vue/test-utils'
import CoffeeShops from '@/components/CoffeeShops'
import CoffeeShopList from '@/components/CoffeeShopList'
import AddCoffeeShop from '@/components/AddCoffeeShop'
import sinon from 'sinon'
import CoffeeShopService from '@/services/coffee_shop_service'

import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)

let stubAddNew
let stubFetchAll
let stubChangeStars

describe('CoffeeShop', () => {
  beforeEach('create stubs', () => {
    stubAddNew = sinon.stub(CoffeeShopService, 'addNew')
    stubFetchAll = sinon.stub(CoffeeShopService, 'fetchAll')
    stubChangeStars = sinon.stub(CoffeeShopService, 'updateStars')
  })

  afterEach('restore stubs', () => {
    stubAddNew.restore()
    stubFetchAll.restore()
    stubChangeStars.restore()
  })

  it('should contain a list component and an add form component', () => {
    stubFetchAll.resolves([])
    const wrapper = mount(CoffeeShops)

    // Have to wait until the next tick to check the assertions so the Promise can resolve
    return Vue.nextTick().then(() => {
      expect(wrapper.contains(CoffeeShopList)).to.be.true
      expect(wrapper.contains(AddCoffeeShop)).to.be.true
    })
  })

  it('should fetch a list of coffee shops when launched', () => {
    const exampleShops = [
      {_id: '1', name: 'Launch Java Beans', stars: 3},
      {_id: '2', name: 'Launch Cakes and Coffee', stars: 5}
    ]

    stubFetchAll.resolves(exampleShops) // returns a promise that resolves to exampleShops
    const wrapper = mount(CoffeeShops)

    return Vue.nextTick().then(() => {
      // Data is set, and rendered in the Component
      expect(wrapper.vm.coffeeShops).to.be.equal(exampleShops)
      expect(wrapper.text()).to.include('Launch Java Beans')
      expect(wrapper.text()).to.include('3 stars')
      expect(wrapper.text()).to.include('Launch Cakes and Coffee')
      expect(wrapper.text()).to.include('5 stars')
    })
  })

  it('should show an error message if not possible to fetch coffee shop list', () => {
    stubFetchAll.rejects('oh dear')
    const wrapper = mount(CoffeeShops)

    // wait two ticks (why?)
    return Vue.nextTick().then(() => {
      return Vue.nextTick().then(() => {
        expect(wrapper.find('#errors-fetch').text()).to.include('Error fetching coffee shops')
      })
    })
  })

  it('should request a new coffee shop created when addNew message received and update list of shops', () => {
    let newShop = {name: 'java beans', stars: 3}

    stubAddNew.resolves('whatever')
    stubFetchAll.resolves([])

    const wrapper = mount(CoffeeShops)

    return Vue.nextTick().then(() => {
      stubFetchAll.resolves([newShop]) // prepare to return new data
      wrapper.vm.onAddNew(newShop)
      return Vue.nextTick().then(() => {
        stubAddNew.should.have.been.calledWith(newShop)
        expect(wrapper.vm.coffeeShops).to.be.eql([newShop])
        expect(wrapper.text()).to.include('java beans')
        expect(wrapper.text()).to.include('3 stars')
      })
    })
  })

  // it('should show an error message if not possible to add new coffee shop', () => {
  //   let badNewShop = {stars: 3} // no name, not that it matters, because the promise is going to reject
  //
  //   stubFetchAll.resolves([])
  //   stubAddNew.rejects({message: 'Error adding new coffee shop'})
  //
  //   const wrapper = mount(CoffeeShops)
  //
  //   return Vue.nextTick().then(() => { // wait for stubFetchAll to resolve after mounting
  //     wrapper.vm.onAddNew(badNewShop) // add new message
  //     return Vue.nextTick().then(() => { // wait for addNew to resolve
  //       return Vue.nextTick().then(() => { // wait for addNew to resolve
  //         console.log(wrapper.text())
  //         expect(wrapper.find('#add-errors').text()).to.include('Error adding new coffee shop')
  //       })
  //     })
  //   })
  // }),


  it('should show an error message if not possible to add new coffee shop', () => {
    let badNewShop = {stars: 3} // no name, not that it matters, because the promise is going to reject

    stubFetchAll.resolves([])
    stubAddNew.rejects({message: 'Error adding new coffee shop'})

    const wrapper = mount(CoffeeShops)

    return Vue.nextTick()
      .then(() => { // wait for stubFetchAll to resolve after mounting
        wrapper.vm.onAddNew(badNewShop) // add new message
        return Vue.nextTick()
      })
      .then(() => { // wait for addNew to resolve
        return Vue.nextTick() // wait for addNew to resolve
      })
      .then(() => {
        console.log(wrapper.text())
        expect(wrapper.find('#add-errors').text()).to.include('Error adding new coffee shop')
      })
  }),


  it('should request the number of stars are changed when onStarsChanged message received and update list of shops', () => {
    const exampleShops = [
      {_id: '1', name: 'Change Stars Java Beans', stars: 3},
      {_id: '2', name: 'Change Stars Cakes and Coffee', stars: 5}
    ]

    const exampleShopsUpdated = [
      {_id: '1', name: 'Change Stars Java Beans', stars: 3},
      {_id: '2', name: 'Change Stars Cakes and Coffee', stars: 1}
    ]

    stubFetchAll.resolves(exampleShops)
    stubChangeStars.resolves('whatever')

    const wrapper = mount(CoffeeShops)

    return Vue.nextTick().then(() => {
      return Vue.nextTick().then(() => {
        stubFetchAll.resolves(exampleShopsUpdated) // prepare to return updated data
        wrapper.vm.onStarsChanged('2', 1) // send message to component
        return Vue.nextTick().then(() => {
          expect(wrapper.find('#shop-2').text()).to.include('1 star')
        })
      })
    })
  })

  it('should show an error message if not possible to update coffee shop stars', () => {
    const exampleShops = [
      {_id: '1', name: 'Error Stars Java Beans', stars: 3},
      {_id: '2', name: 'Error Stars Cakes and Coffee', stars: 5}
    ]

    stubFetchAll.resolves(exampleShops)
    stubChangeStars.rejects('oops')

    const wrapper = mount(CoffeeShops)

    return Vue.nextTick().then(() => {
      wrapper.vm.onStarsChanged('2', 3) // whatever
      return Vue.nextTick().then(() => {
        expect(wrapper.text()).to.include('Error changing stars')
      })
    })
  })
})
