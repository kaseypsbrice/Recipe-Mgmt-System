import { mount } from '@vue/test-utils'
import Signup from '@/views/Signup.vue'

describe('Signup.vue', () => {
  it('shows alert if fields are missing on submit', async () => {
    const alertMock = vi.fn()
    global.alert = alertMock

    const wrapper = mount(Signup)
    await wrapper.find('form').trigger('submit.prevent')

    expect(alertMock).toHaveBeenCalled()
    expect(alertMock.mock.calls[0][0]).toContain('Signup failed')
  })
})
