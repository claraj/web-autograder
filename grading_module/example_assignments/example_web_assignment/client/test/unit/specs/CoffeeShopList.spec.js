/*

Does it display a list of shops with correct name and stars?
Does it emit an event when a star rating is changed?

*/

import Vue from 'vue'
import { mount } from '@vue/test-utils'
import CoffeeShopList from '@/components/CoffeeShopList'
import sinon from 'sinon'

describe('CoffeeShopList. vue', () => {
  it('should display a list of coffee shops', () => {
    const exampleShops = [
      {_id: '1', name: 'Java Beans', stars: 3},
      {_id: '2', name: 'Cakes and Coffee', stars: 5}
    ]
    const Constructor = Vue.extend(CoffeeShopList)
    const vm = new Constructor({
      propsData: {
        coffeeShops: exampleShops,
        errors: {
          fetchAll: '',
          changeStars: ''
        }
      }
    }).$mount()

    const shopListElements = Array.from(vm.$el.querySelectorAll('li'))

    for (let i = 0; i < exampleShops.length; i++) {
      expect(shopListElements[i].textContent).to.include(exampleShops[i].name)
      expect(shopListElements[i].textContent).to.include(exampleShops[i].stars)
    }
  })

  it('should display a No Shops message if the list of shops is empty', () => {
    const exampleShops = []
    const Constructor = Vue.extend(CoffeeShopList)
    const vm = new Constructor({
      propsData: {
        coffeeShops: exampleShops,
        errors: {
          fetchAll: '',
          changeStars: ''
        }
      }
    }).$mount()

    const shopListElements = Array.from(vm.$el.querySelectorAll('li'))
    expect(shopListElements.length).to.be.equal(0)
    const noShopMessage = vm.$el.querySelector('#no-shops')
    expect(noShopMessage.textContent).to.include('No Coffee Shops')
  })

  it('should emit an event when a star rating is changed', () => {
    const exampleShops = [
      {_id: '1', name: 'Java Beans', stars: 3},
      {_id: '2', name: 'Cakes and Coffee', stars: 5}
    ]

    const spyUpddateStars = sinon.spy()

    const wrapper = mount(CoffeeShopList, {
      propsData: {
        coffeeShops: exampleShops,
        errors: {fetchAll: '', changeStars: ''}
      },
      methods: {
        onStarsChanged: spyUpddateStars
      }
    })

    // console.log('shop 1 is here:', wrapper.find('#shop-1').html())
    // console.log(wrapper.find('#shop-1 .star-range-slider').text())

    const javaBeansSlider = wrapper.find('#shop-1 .star-range-slider')
    javaBeansSlider.setValue(4)
    javaBeansSlider.trigger('input')
    spyUpddateStars.should.have.been.calledWith('1', 4)

    // Click on another star rating
    const cakesCoffeeSlider = wrapper.find('#shop-2 .star-range-slider')
    cakesCoffeeSlider.setValue(3)
    cakesCoffeeSlider.trigger('input')
    spyUpddateStars.should.have.been.calledWith('2', 3)

    cakesCoffeeSlider.setValue(4)
    cakesCoffeeSlider.trigger('input')
    spyUpddateStars.should.have.been.calledWith('2', 4)

    cakesCoffeeSlider.setValue(5)
    cakesCoffeeSlider.trigger('input')
    spyUpddateStars.should.have.been.calledWith('2', 5)

    cakesCoffeeSlider.setValue(1)
    cakesCoffeeSlider.trigger('input')
    spyUpddateStars.should.have.been.calledWith('2', 1)
  })
})
