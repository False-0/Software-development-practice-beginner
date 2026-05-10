<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { showFailToast, showSuccessToast } from 'vant'
import { useUserStore } from '../store/user'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
})

const goLogin = () => {
  router.push('/login')
}

const onRegister = async () => {
  if (!form.username || !form.password || !form.confirmPassword) {
    showFailToast('请完整填写注册信息')
    return
  }

  if (form.password !== form.confirmPassword) {
    showFailToast('两次密码输入不一致')
    return
  }

  await userStore.register({
    username: form.username,
    password: form.password,
  })

  showSuccessToast('注册成功')
  router.push('/login')
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-shell">
      <div class="auth-card">
        <div class="top-row">
          <van-button class="back-btn" @click="goLogin">返回</van-button>
          <div class="top-title">注册账号</div>
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

          <div class="form-label">确认密码</div>
          <van-field
            v-model="form.confirmPassword"
            class="auth-input"
            type="password"
            placeholder="请再次输入密码"
          />

          <div class="register-wrap">
            <van-button class="register-btn" type="primary" @click="onRegister">注册</van-button>
          </div>

          <div class="link-row">
            已有账号？<span class="link" @click="goLogin">去登录</span>
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

.top-row {
  height: 56px;
  border-bottom: 1px solid #f0f1f3;
  display: flex;
  align-items: center;
  padding: 0 12px;
  gap: 10px;
  background: #fff;
}

.back-btn {
  width: 72px;
  height: 34px;
  border-radius: 18px;
  color: #323233;
  background: #f2f3f5;
  border: 1px solid #ebedf0;
}

.back-btn:hover {
  background: #e8eaee;
}

.back-btn:active {
  transform: scale(0.98);
}

.top-title {
  font-size: 16px;
  font-weight: 600;
  color: #323233;
}

.form-area {
  padding: 24px 18px 24px;
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

.register-wrap {
  margin-top: 10px;
  display: flex;
  justify-content: center;
}

.register-btn {
  width: 100%;
  height: 42px;
  font-size: 15px;
  border-radius: 10px;
  transition: transform 0.1s, opacity 0.2s;
}

.register-btn:active {
  transform: scale(0.98);
  opacity: 0.95;
}

.link-row {
  margin-top: 18px;
  text-align: center;
  color: #646566;
  font-size: 14px;
}

.link {
  color: #1989fa;
  margin-left: 6px;
}

.link:active {
  opacity: 0.8;
}
</style>
