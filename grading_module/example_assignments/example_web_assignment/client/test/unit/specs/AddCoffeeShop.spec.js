import { mount } from '@vue/test-utils'
import AddCoffeeShop from '@/components/AddCoffeeShop'

describe('Add Coffee Shop form', () => {
  it('should display an error message and not emit anything if no name provided in the form', () => {
    const wrapper = mount(AddCoffeeShop, {
      propsData: {
        errors: {
          addNew: ''
        }
      }
    })
    wrapper.setData({ name: '' })
    wrapper.find('#add-new-button').trigger('click')
    let formErrors = wrapper.find('#form-errors')
    expect(formErrors.text()).to.be.equal('You must enter a name.')
    // should not be an event emitted
    expect(wrapper.emitted().onAddNew).to.be.undefined
  })

  it('should emit an event with new coffee shop info if form is complete and submitted', () => {
    const wrapper = mount(AddCoffeeShop, {
      propsData: {
        errors: {
          addNew: ''
        }
      }
    })
    const data = {name: 'Example Shop', stars: 3}
    wrapper.vm.name = 'Example Shop'
    wrapper.vm.stars = 3
    // click
    wrapper.find('#add-new-button').trigger('click')
    expect(wrapper.contains('#form-errors')).to.be.false
    expect(wrapper.emitted().onAddNew.length).to.be.equal(1)
    expect(wrapper.emitted().onAddNew[0]).to.be.eql([data])
  })

  it('should display an error message if error prop is set', () => {
    const wrapper = mount(AddCoffeeShop, {
      propsData: {
        errors: {
          addNew: ''
        }
      }
    })
    wrapper.setProps({errors: {addNew: 'oops'}})
    expect(wrapper.find('#add-errors').text()).to.be.equal('oops')
  })
})
