<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showFailToast, showSuccessToast } from 'vant'
import { updatePassword } from '../api/user'

const router = useRouter()

const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const submitting = ref(false)

function goBack() {
  router.replace('/mine')
}

function validate() {
  if (!oldPassword.value.trim()) {
    showFailToast('请输入旧密码')
    return false
  }
  if (newPassword.value.length < 6) {
    showFailToast('新密码长度不少于6位')
    return false
  }
  if (newPassword.value !== confirmPassword.value) {
    showFailToast('新密码与确认密码不一致')
    return false
  }
  return true
}

async function onSubmit() {
  if (!validate() || submitting.value) return
  submitting.value = true
  try {
    await updatePassword({
      oldPassword: oldPassword.value,
      newPassword: newPassword.value,
    })
    showSuccessToast('密码修改成功')
    router.replace('/mine')
  } catch {
    /* 拦截器已提示 */
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="pwd-page">
    <div class="shell">
      <header class="top-bar">
        <button type="button" class="ghost-btn" @click="goBack">返回</button>
        <span class="title">修改密码</span>
        <span class="spacer" />
      </header>

      <section class="card">
        <div class="field-block">
          <div class="lab">旧密码</div>
          <van-field
            v-model="oldPassword"
            type="password"
            placeholder="请输入旧密码"
            class="field"
          />
        </div>
        <div class="field-block">
          <div class="lab">新密码</div>
          <van-field
            v-model="newPassword"
            type="password"
            placeholder="不少于6位"
            class="field"
          />
        </div>
        <div class="field-block">
          <div class="lab">确认密码</div>
          <van-field
            v-model="confirmPassword"
            type="password"
            placeholder="再次输入新密码"
            class="field"
          />
        </div>

        <van-button
          type="primary"
          block
          round
          class="submit-btn"
          :loading="submitting"
          @click="onSubmit"
        >
          确认修改
        </van-button>
      </section>
    </div>
  </div>
</template>

<style scoped>
.pwd-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 16px;
  box-sizing: border-box;
}

.shell {
  max-width: 420px;
  margin: 0 auto;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.ghost-btn {
  border: none;
  border-radius: 8px;
  background: #fff;
  color: #323233;
  padding: 8px 14px;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.title {
  font-size: 17px;
  font-weight: 700;
  color: #323233;
}

.spacer {
  width: 64px;
}

.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 16px 14px 20px;
}

.field-block + .field-block {
  margin-top: 8px;
}

.lab {
  font-size: 14px;
  color: #646566;
  margin-bottom: 6px;
}

.field {
  padding: 8px 12px;
  background: #f7f8fa;
  border-radius: 8px;
}

.submit-btn {
  margin-top: 24px;
}
</style>
