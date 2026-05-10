<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showConfirmDialog, showFailToast, showSuccessToast } from 'vant'
import { cancelFavorite, fetchAllFavorites, clearAllFavorites } from '../api/favorite'

const router = useRouter()

const loading = ref(true)
const list = ref([])

function normalizeRow(item) {
  return {
    ...item,
    optionA: item.optionA ?? item.option_a ?? '',
    optionB: item.optionB ?? item.option_b ?? '',
    optionC: item.optionC ?? item.option_c ?? '',
    optionD: item.optionD ?? item.option_d ?? '',
  }
}

function questionText(item) {
  return item.content || item.title || '—'
}

function hasOptions(item) {
  return !!(item.optionA || item.optionB || item.optionC || item.optionD)
}

async function loadList() {
  loading.value = true
  try {
    const raw = await fetchAllFavorites()
    list.value = raw.map(normalizeRow)
  } catch {
    showFailToast('收藏列表加载失败')
    list.value = []
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.replace('/mine')
}

async function onUnfavorite(item) {
  const id = item.id
  if (id == null) return
  try {
    await cancelFavorite(id)
    showSuccessToast('已取消收藏')
    await loadList()
  } catch {
    await loadList()
  }
}

async function onClearAll() {
  if (!list.value.length) {
    showFailToast('暂无收藏')
    return
  }
  try {
    await showConfirmDialog({
      title: '清空收藏',
      message: '确定清空全部收藏题目吗？',
    })
  } catch {
    return
  }
  try {
    await clearAllFavorites()
    showSuccessToast('已清空')
    await loadList()
  } catch {
    await loadList()
  }
}

onMounted(() => {
  loadList()
})
</script>

<template>
  <div class="fav-page">
    <div class="shell">
      <header class="top-bar">
        <button type="button" class="ghost-btn" @click="goBack">返回</button>
        <button type="button" class="ghost-btn warn" @click="onClearAll">清空</button>
      </header>

      <div v-if="loading" class="state-card">
        <van-loading type="spinner" color="#1989fa" size="28px" />
        <span class="state-text">加载中...</span>
      </div>

      <div v-else class="list-wrap">
        <div v-if="!list.length" class="empty-tip">暂无收藏题目</div>

        <div
          v-for="item in list"
          :key="item.favoriteId ?? item.id"
          class="q-card"
        >
          <button
            type="button"
            class="star-btn"
            aria-label="取消收藏"
            @click="onUnfavorite(item)"
          >
            <van-icon name="star" class="star-on" />
          </button>
          <div class="q-body">
            <div v-if="item.title && item.content" class="q-sub">{{ item.title }}</div>
            <div class="q-title">{{ questionText(item) }}</div>
            <div v-if="hasOptions(item)" class="q-opts">
              <div class="opt-line"><span class="opt-key">a.</span>{{ item.optionA }}</div>
              <div class="opt-line"><span class="opt-key">b.</span>{{ item.optionB }}</div>
              <div class="opt-line"><span class="opt-key">c.</span>{{ item.optionC }}</div>
              <div class="opt-line"><span class="opt-key">d.</span>{{ item.optionD }}</div>
            </div>
            <div v-if="item.answer" class="q-answer">
              正确答案为：<span class="ans-val">{{ String(item.answer).toUpperCase() }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fav-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 16px;
  padding-bottom: 24px;
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
  gap: 12px;
  margin-bottom: 12px;
}

.ghost-btn {
  flex: 1;
  border: none;
  border-radius: 8px;
  background: #fff;
  color: #323233;
  padding: 10px 14px;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.ghost-btn.warn {
  color: #ee0a24;
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

.list-wrap {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.empty-tip {
  text-align: center;
  padding: 36px 16px;
  color: #969799;
  font-size: 14px;
  background: #fff;
  border-radius: 12px;
  border: 1px solid #f0f1f3;
}

.q-card {
  position: relative;
  padding: 14px 12px;
  padding-right: 44px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
}

.star-btn {
  position: absolute;
  top: 10px;
  right: 8px;
  width: 40px;
  height: 40px;
  border: none;
  background: transparent;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.star-on {
  font-size: 22px;
  color: #ff976a;
}

.q-body {
  min-width: 0;
}

.q-sub {
  font-size: 12px;
  color: #969799;
  margin-bottom: 4px;
}

.q-title {
  font-size: 15px;
  font-weight: 600;
  color: #323233;
  line-height: 1.5;
  margin-bottom: 10px;
}

.q-opts {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 10px;
}

.opt-line {
  font-size: 14px;
  color: #646566;
  line-height: 1.45;
}

.opt-key {
  display: inline-block;
  width: 22px;
  font-weight: 600;
  color: #969799;
}

.q-answer {
  font-size: 13px;
  color: #646566;
  padding-top: 8px;
  border-top: 1px solid #f0f1f3;
}

.ans-val {
  font-weight: 700;
  color: #1989fa;
}
</style>
