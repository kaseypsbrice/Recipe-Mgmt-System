import { mount } from '@vue/test-utils'
import Signup from '@/views/Signup.vue'
import axios from 'axios'
import { vi } from 'vitest'

vi.mock('axios')

const mockPush = vi.fn()

vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: mockPush
  })
}))

describe('Signup.vue', () => {
  it('submits form and redirects on success', async () => {
    axios.post.mockResolvedValueOnce({})

    const wrapper = mount(Signup)

    await wrapper.find('input[placeholder="Username"]').setValue('testuser')
    await wrapper.find('input[placeholder="Password"]').setValue('testpass123')
    await wrapper.find('form').trigger('submit.prevent')

    expect(axios.post).toHaveBeenCalledWith('/users/create_user', {
      username: 'testuser',
      password: 'testpass123',
    })

    expect(mockPush).toHaveBeenCalledWith('/login')
  })
})
