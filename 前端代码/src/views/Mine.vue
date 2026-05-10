<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showFailToast, showToast } from 'vant'
import { fetchUserInfo } from '../api/user'
import { useUserStore } from '../store/user'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const showService = ref(false)

async function loadProfile() {
  loading.value = true
  try {
    const data = await fetchUserInfo()
    userStore.setUserInfo(data)
  } catch {
    showFailToast('用户信息加载失败')
  } finally {
    loading.value = false
  }
}

function displayNickname() {
  const u = userStore.userInfo
  if (!u) return '未登录'
  return u.nickname || u.username || '未设置昵称'
}

function displayBio() {
  const u = userStore.userInfo
  if (!u?.bio) return '暂无个性签名'
  return u.bio
}

function avatarUrl() {
  return userStore.userInfo?.avatar || ''
}

function goProfile() {
  router.push('/mine/profile')
}

function goFavorites() {
  router.push('/mine/favorites')
}

function goCorrect() {
  router.push('/mine/correct')
}

function goPassword() {
  router.push('/mine/password')
}

function openService() {
  showService.value = true
}

function onFeedback() {
  showToast('感谢您的反馈，功能即将上线')
}

function logout() {
  userStore.logout()
  router.replace('/login')
}

onMounted(() => {
  loadProfile()
})
</script>

<template>
  <div class="mine-page">
    <div class="shell">
      <button type="button" class="profile-card" @click="goProfile">
        <div class="avatar-wrap">
          <img
            v-if="avatarUrl()"
            :src="avatarUrl()"
            alt="头像"
            class="avatar-img"
          >
          <div v-else class="avatar-ph">头像</div>
        </div>
        <div class="profile-text">
          <div class="nick-row">
            <span class="label">昵称：</span>
            <span class="value">{{ displayNickname() }}</span>
          </div>
          <div class="bio-row">
            <span class="label">个性签名：</span>
            <span class="value ellipsis">{{ displayBio() }}</span>
          </div>
        </div>
      </button>

      <div v-if="loading" class="state-inline">
        <van-loading type="spinner" color="#1989fa" size="22px" />
      </div>

      <div class="menu-list">
        <button type="button" class="menu-item" @click="goFavorites">
          我的收藏题目
          <van-icon name="arrow" class="arrow" />
        </button>
        <button type="button" class="menu-item" @click="goCorrect">
          已斩题目记录
          <van-icon name="arrow" class="arrow" />
        </button>
        <button type="button" class="menu-item" @click="goPassword">
          修改密码
          <van-icon name="arrow" class="arrow" />
        </button>
        <button type="button" class="menu-item" @click="openService">
          联系客服
          <van-icon name="arrow" class="arrow" />
        </button>
        <button type="button" class="menu-item" @click="onFeedback">
          意见反馈
          <van-icon name="arrow" class="arrow" />
        </button>
      </div>

      <button type="button" class="logout-btn" @click="logout">
        退出登录
      </button>
    </div>

    <van-popup
      v-model:show="showService"
      round
      position="center"
      :close-on-click-overlay="true"
      class="svc-popup"
    >
      <div class="svc-panel">
        <div class="svc-title">联系客服</div>
        <div class="svc-num">520</div>
        <van-button type="primary" block round @click="showService = false">
          关闭
        </van-button>
      </div>
    </van-popup>

    <van-tabbar route fixed active-color="#1989fa" inactive-color="#7d7e80">
      <van-tabbar-item replace to="/home">主页</van-tabbar-item>
      <van-tabbar-item replace to="/wrong">错题</van-tabbar-item>
      <van-tabbar-item replace to="/comment">评论</van-tabbar-item>
      <van-tabbar-item replace to="/mine">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<style scoped>
.mine-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 16px;
  padding-bottom: 66px;
  box-sizing: border-box;
}

.shell {
  max-width: 420px;
  margin: 0 auto;
}

.profile-card {
  width: 100%;
  display: flex;
  gap: 14px;
  align-items: center;
  padding: 16px;
  border: none;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 12px;
  text-align: left;
  transition: background 0.2s;
}

.profile-card:active {
  background: #f7f8fa;
}

.avatar-wrap {
  flex-shrink: 0;
}

.avatar-img {
  width: 64px;
  height: 64px;
  border-radius: 10px;
  object-fit: cover;
  display: block;
}

.avatar-ph {
  width: 64px;
  height: 64px;
  border-radius: 10px;
  background: #f2f3f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  color: #969799;
}

.profile-text {
  flex: 1;
  min-width: 0;
}

.nick-row,
.bio-row {
  font-size: 14px;
  color: #323233;
  line-height: 1.5;
}

.bio-row {
  margin-top: 6px;
}

.label {
  color: #969799;
}

.value {
  font-weight: 600;
}

.ellipsis {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.state-inline {
  display: flex;
  justify-content: center;
  padding: 8px 0 12px;
}

.menu-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 16px 14px;
  border: none;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  font-size: 15px;
  font-weight: 600;
  color: #323233;
}

.menu-item:active {
  background: #f7f8fa;
}

.arrow {
  color: #c8c9cc;
  transform: rotate(-90deg);
}

.logout-btn {
  width: 100%;
  margin-top: 18px;
  padding: 14px;
  border: none;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  font-size: 15px;
  font-weight: 600;
  color: #ee0a24;
}

.logout-btn:active {
  background: #fff5f5;
}

.svc-panel {
  width: 72vw;
  max-width: 300px;
  padding: 20px 18px;
  box-sizing: border-box;
}

.svc-title {
  text-align: center;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.svc-num {
  text-align: center;
  font-size: 28px;
  font-weight: 700;
  color: #1989fa;
  letter-spacing: 2px;
  margin-bottom: 16px;
}
</style>

<style>
.svc-popup.van-popup--center {
  border-radius: 12px;
}
</style>
