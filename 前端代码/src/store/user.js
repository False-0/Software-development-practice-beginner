import { defineStore } from 'pinia'
import { loginApi, registerApi } from '../api/user'

export const useUserStore = defineStore(
  'user',
  {
    state: () => ({
      token: '',
      userInfo: null,
    }),
    actions: {
      setLoginData(data) {
        this.token = data?.token || ''
        this.userInfo = data?.userInfo || null
      },
      async login(payload) {
        const data = await loginApi(payload)
        this.setLoginData(data)
        return data
      },
      async register(payload) {
        const data = await registerApi(payload)
        this.setLoginData(data)
        return data
      },
      logout() {
        this.token = ''
        this.userInfo = null
      },
      setUserInfo(info) {
        this.userInfo = info
      },
    },
    persist: true,
  },
)
