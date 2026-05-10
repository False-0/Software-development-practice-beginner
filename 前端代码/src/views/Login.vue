<script setup>
import { reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showFailToast, showSuccessToast } from 'vant'
import { useUserStore } from '../store/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const form = reactive({
  username: '',
  password: '',
})

const onLogin = async () => {
  if (!form.username || !form.password) {
    showFailToast('请填写用户名和密码')
    return
  }

  await userStore.login({
    username: form.username,
    password: form.password,
  })

  showSuccessToast('登录成功')
  const redirect = route.query.redirect
  if (typeof redirect === 'string' && redirect.startsWith('/')) {
    router.replace(redirect)
  } else {
    router.replace('/home')
  }
}

const goRegister = () => {
  router.push('/register')
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-shell">
      <div class="auth-card">
        <div class="brand-box">
          <div class="brand-title">DuckMed</div>
          <div class="brand-subtitle">医学刷题助手</div>
        </div>

        <div class="form-area">
          <div class="form-label">用户名</div>
          <van-field v-model="form.username" class="auth-input" placeholder="请输入用户名" />

          <div class="form-label">密码</div>
          <van-field
            v-model="form.password"
            class="auth-input"
            type="password"
            placeholder="请输入密码"
          />

          <div class="actions">
            <van-button class="action-btn" type="primary" @click="onLogin">登录</van-button>
            <van-button class="action-btn ghost-btn" @click="goRegister">注册</van-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: #f6f7fb;
  display: flex;
  justify-content: center;
  padding: 16px;
  box-sizing: border-box;
}

.auth-shell {
  width: 100%;
  max-width: 420px;
}

.auth-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.brand-box {
  height: 170px;
  border-bottom: 1px solid #f0f1f3;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(180deg, #fbfcff 0%, #ffffff 100%);
}

.brand-title {
  font-size: 28px;
  font-weight: 700;
  color: #323233;
}

.brand-subtitle {
  font-size: 14px;
  color: #969799;
}

.form-area {
  padding: 28px 18px 24px;
}

.form-label {
  margin: 0 0 8px 2px;
  font-size: 14px;
  color: #646566;
}

.auth-input {
  margin-bottom: 18px;
  border: 1px solid #ebedf0;
  border-radius: 8px;
  background: #fff;
  overflow: hidden;
}

:deep(.auth-input .van-field__control) {
  font-size: 14px;
}

:deep(.auth-input:focus-within) {
  border-color: #1989fa;
}

.actions {
  margin-top: 8px;
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.action-btn {
  flex: 1;
  height: 42px;
  font-size: 15px;
  border-radius: 10px;
  transition: transform 0.1s, opacity 0.2s;
}

.ghost-btn {
  color: #323233;
  background: #f2f3f5;
  border: 1px solid #ebedf0;
}

.ghost-btn:hover {
  background: #e8eaee;
}

.action-btn:active {
  transform: scale(0.98);
  opacity: 0.95;
}
</style>
