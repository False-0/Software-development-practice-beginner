<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showFailToast } from 'vant'
import { fetchErrorStatistics } from '../api/error'

const router = useRouter()

const loading = ref(true)
const showTotal = ref(false)
const showToday = ref(false)

const stats = ref({
  totalErrorCount: 0,
  todayErrorCount: 0,
})

async function loadStats() {
  loading.value = true
  try {
    const data = await fetchErrorStatistics()
    stats.value = {
      totalErrorCount: data?.totalErrorCount ?? 0,
      todayErrorCount: data?.todayErrorCount ?? 0,
    }
  } catch {
    showFailToast('统计数据加载失败')
  } finally {
    loading.value = false
  }
}

function openTotal() {
  showTotal.value = true
}

function openToday() {
  showToday.value = true
}

function goRecords() {
  router.push('/wrong/records')
}

function goStats() {
  router.push('/wrong/stats')
}

onMounted(() => {
  loadStats()
})
</script>

<template>
  <div class="wrong-home">
    <div class="shell">
      <h1 class="page-title">错题中心</h1>

      <div v-if="loading" class="state-card">
        <van-loading type="spinner" color="#1989fa" size="28px" />
        <span class="state-text">加载中...</span>
      </div>

      <div v-else class="menu-grid">
        <button type="button" class="menu-card" @click="openTotal">
          <span class="menu-label">总错题量</span>
          <van-icon name="arrow" class="menu-arrow" />
        </button>
        <button type="button" class="menu-card" @click="openToday">
          <span class="menu-label">今日错题量</span>
          <van-icon name="arrow" class="menu-arrow" />
        </button>
        <button type="button" class="menu-card" @click="goRecords">
          <span class="menu-label">错题记录</span>
          <van-icon name="arrow" class="menu-arrow" />
        </button>
        <button type="button" class="menu-card" @click="goStats">
          <span class="menu-label">错题统计</span>
          <van-icon name="arrow" class="menu-arrow" />
        </button>
      </div>
    </div>

    <van-popup
      v-model:show="showTotal"
      round
      position="center"
      :close-on-click-overlay="true"
      class="wrong-popup-root"
    >
      <div class="popup-panel popup-panel--primary">
        <button type="button" class="popup-close" aria-label="关闭" @click="showTotal = false">
          ×
        </button>
        <div class="popup-body">
          <p class="popup-line">总错题量为：{{ stats.totalErrorCount }}</p>
        </div>
      </div>
    </van-popup>

    <van-popup
      v-model:show="showToday"
      round
      position="center"
      :close-on-click-overlay="true"
      class="wrong-popup-root"
    >
      <div class="popup-panel">
        <button type="button" class="popup-close" aria-label="关闭" @click="showToday = false">
          ×
        </button>
        <div class="popup-body">
          <p class="popup-line">今日错题量为：{{ stats.todayErrorCount }}</p>
          <p class="popup-tip">
            今日错得最多的是哪个章节的题目，继续努力哦！
          </p>
        </div>
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
.wrong-home {
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

.page-title {
  margin: 0 0 16px;
  font-size: 20px;
  font-weight: 700;
  color: #323233;
  text-align: center;
}

.state-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 48px 16px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.state-text {
  font-size: 14px;
  color: #969799;
}

.menu-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.menu-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 18px 16px;
  border: none;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  font-size: 16px;
  font-weight: 600;
  color: #323233;
  transition: background-color 0.2s, transform 0.1s;
}

.menu-card:active {
  background: #f7f8fa;
  transform: scale(0.995);
}

.menu-arrow {
  color: #c8c9cc;
  transform: rotate(-90deg);
}

.popup-panel {
  position: relative;
  width: 78vw;
  max-width: 320px;
  padding: 22px 18px 20px;
  background: #fff;
  border-radius: 12px;
  box-sizing: border-box;
}

.popup-panel--primary {
  border: 2px solid #1989fa;
}

.popup-close {
  position: absolute;
  top: 8px;
  right: 10px;
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  font-size: 22px;
  line-height: 1;
  color: #969799;
}

.popup-body {
  text-align: center;
  padding-top: 4px;
}

.popup-line {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  color: #323233;
  line-height: 1.5;
}

.popup-tip {
  margin: 14px 0 0;
  font-size: 14px;
  color: #646566;
  line-height: 1.55;
}
</style>

<style>
.wrong-popup-root.van-popup--center {
  background: transparent;
}
</style>
