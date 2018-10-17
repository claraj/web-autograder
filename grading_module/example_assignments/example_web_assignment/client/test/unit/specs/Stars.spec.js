import Stars from '@/components/Stars'
import { mount } from '@vue/test-utils'

describe('Stars.vue', () => {
  it('should render a range slider with min = 1 and max = 5', () => {
    const wrapper = mount(Stars, {propsData: {stars: 4, _id: '2'}})
    const slider = wrapper.find('.star-range-slider')
    expect(slider.attributes('min')).to.be.equal('1')
    expect(slider.attributes('max')).to.be.equal('5')
    expect(slider.element.value).to.be.equal('4')
  })

  it('should render the text "3 stars" if the value is 3', () => {
    const wrapper = mount(Stars, {propsData: {stars: 3, _id: '2'}})
    const starText = wrapper.find('.star-text-display')
    expect(starText.text()).to.be.equal('3 stars')
  })

  it('should render the text "1 star" if the value is 1', () => {
    const wrapper = mount(Stars, {propsData: {stars: 1, _id: '2'}})
    const starText = wrapper.find('.star-text-display')
    expect(starText.text()).to.be.equal('1 star')
  })

  it('should update the text number of stars on when slider is moved', () => {
    const wrapper = mount(Stars, {propsData: {stars: 1}})
    const starRange = wrapper.find('.star-range-slider')
    // starRange.element.value = 2  // This is equivalent to the long below
    starRange.setValue(2)
    starRange.trigger('input')

    const starText = wrapper.find('.star-text-display')
    expect(starText.text()).to.be.equal('2 stars')

    starRange.element.value = 5
    starRange.trigger('input')
    expect(starText.text()).to.be.equal('5 stars')
  })

  it('should emit event when slider is moved', () => {
    const wrapper = mount(Stars, {propsData: {_id: '3'}})
    const starRange = wrapper.find('.star-range-slider')
    starRange.element.value = 2
    starRange.trigger('input')
    expect(wrapper.emitted('onStarsChanged').length).to.be.equal(1)
    expect(wrapper.emitted('onStarsChanged')).to.be.eql([['3', 2]])
  })
})
