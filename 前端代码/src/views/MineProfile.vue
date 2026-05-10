<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showConfirmDialog, showFailToast, showSuccessToast } from 'vant'
import { fetchUserInfo, updateUser } from '../api/user'
import { useUserStore } from '../store/user'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const saving = ref(false)

const nickname = ref('')
const bio = ref('')
const phone = ref('')
const avatar = ref('')

const snapshot = ref({
  nickname: '',
  bio: '',
  phone: '',
  avatar: '',
})

const fileRef = ref(null)

const currentState = computed(() => ({
  nickname: nickname.value,
  bio: bio.value,
  phone: phone.value,
  avatar: avatar.value,
}))

const isDirty = computed(
  () => JSON.stringify(currentState.value) !== JSON.stringify(snapshot.value),
)

function applyUser(u) {
  nickname.value = u?.nickname ?? ''
  bio.value = u?.bio ?? ''
  phone.value = u?.phone ?? ''
  avatar.value = u?.avatar ?? ''
  snapshot.value = {
    nickname: nickname.value,
    bio: bio.value,
    phone: phone.value,
    avatar: avatar.value,
  }
}

async function load() {
  loading.value = true
  try {
    const data = await fetchUserInfo()
    applyUser(data)
    userStore.setUserInfo(data)
  } catch {
    showFailToast('加载失败')
  } finally {
    loading.value = false
  }
}

function triggerFile() {
  fileRef.value?.click()
}

function onFileChange(e) {
  const file = e.target?.files?.[0]
  if (!file) return
  if (!file.type.startsWith('image/')) {
    showFailToast('请选择图片文件')
    return
  }
  if (file.size > 3 * 1024 * 1024) {
    showFailToast('图片请小于 3MB')
    return
  }
  const reader = new FileReader()
  reader.onload = () => {
    const url = typeof reader.result === 'string' ? reader.result : ''
    avatar.value = url
  }
  reader.readAsDataURL(file)
  e.target.value = ''
}

async function save() {
  saving.value = true
  try {
    const data = await updateUser({
      nickname: nickname.value.trim() || undefined,
      bio: bio.value.trim() || undefined,
      phone: phone.value.trim() || undefined,
      avatar: avatar.value || undefined,
    })
    const merged = data || {
      ...userStore.userInfo,
      nickname: nickname.value,
      bio: bio.value,
      phone: phone.value,
      avatar: avatar.value,
    }
    userStore.setUserInfo(merged)
    applyUser(merged)
    showSuccessToast('保存成功')
  } catch {
    /* 拦截器提示 */
  } finally {
    saving.value = false
  }
}

async function onBack() {
  if (!isDirty.value) {
    router.replace('/mine')
    return
  }
  try {
    await showConfirmDialog({
      title: '提示',
      message: '有未保存的修改，是否保存？',
      confirmButtonText: '保存',
      cancelButtonText: '不保存',
    })
  } catch {
    router.replace('/mine')
    return
  }
  try {
    await save()
    router.replace('/mine')
  } catch {
    /* 保存失败留在当前页 */
  }
}

onMounted(() => {
  load()
})
</script>

<template>
  <div class="profile-page">
    <div class="shell">
      <div v-if="loading" class="state-card">
        <van-loading type="spinner" color="#1989fa" size="28px" />
      </div>

      <template v-else>
        <section class="card">
          <div class="avatar-block">
            <button type="button" class="avatar-hit" @click="triggerFile">
              <img
                v-if="avatar"
                :src="avatar"
                alt="头像"
                class="avatar-img"
              >
              <div v-else class="avatar-ph">头像框</div>
              <span class="avatar-tip">点击上传</span>
            </button>
            <input
              ref="fileRef"
              type="file"
              accept="image/*"
              class="hidden-input"
              @change="onFileChange"
            >
          </div>

          <div class="field-block">
            <div class="lab">昵称</div>
            <van-field v-model="nickname" placeholder="昵称" class="field" />
          </div>
          <div class="field-block">
            <div class="lab">个人简介</div>
            <van-field
              v-model="bio"
              type="textarea"
              rows="3"
              autosize
              placeholder="个性签名"
              class="field"
            />
          </div>
          <div class="field-block">
            <div class="lab">手机号</div>
            <van-field
              v-model="phone"
              type="tel"
              placeholder="手机号"
              class="field"
            />
          </div>

          <van-button
            type="primary"
            block
            round
            class="save-btn"
            :loading="saving"
            @click="save"
          >
            保存修改
          </van-button>
        </section>

        <button type="button" class="back-bottom" @click="onBack">返回</button>
      </template>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 16px;
  padding-bottom: 32px;
  box-sizing: border-box;
}

.shell {
  max-width: 420px;
  margin: 0 auto;
}

.state-card {
  display: flex;
  justify-content: center;
  padding: 48px 16px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 18px 14px 20px;
}

.avatar-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 18px;
}

.avatar-hit {
  border: none;
  background: transparent;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.avatar-img {
  width: 88px;
  height: 88px;
  border-radius: 12px;
  object-fit: cover;
  border: 2px solid #ebedf0;
}

.avatar-ph {
  width: 88px;
  height: 88px;
  border-radius: 12px;
  background: #f2f3f5;
  border: 2px dashed #dcdee0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #969799;
}

.avatar-tip {
  font-size: 12px;
  color: #1989fa;
}

.hidden-input {
  display: none;
}

.field-block + .field-block {
  margin-top: 12px;
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

.save-btn {
  margin-top: 20px;
}

.back-bottom {
  width: 100%;
  margin-top: 16px;
  padding: 14px;
  border: none;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  font-size: 15px;
  font-weight: 600;
  color: #323233;
}

.back-bottom:active {
  background: #f7f8fa;
}
</style>
