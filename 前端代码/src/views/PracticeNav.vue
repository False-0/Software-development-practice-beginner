<script setup>
import { computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showFailToast } from 'vant'
import { usePracticeStore } from '../store/practice'

const route = useRoute()
const router = useRouter()
const practiceStore = usePracticeStore()

const chapterIdStr = computed(() => {
  const c = route.query.chapterId
  return c != null ? String(c) : ''
})

const activeNo = computed(() => {
  const n = Number(route.query.n)
  let no = Number.isFinite(n) && n >= 1 ? Math.floor(n) : 1
  const t = total.value
  if (t > 0 && no > t) no = t
  return no
})

const total = computed(() => practiceStore.questions.length)

const numbers = computed(() => {
  const t = total.value
  return Array.from({ length: t }, (_, i) => i + 1)
})

function goBack() {
  if (!chapterIdStr.value) {
    router.replace('/home')
    return
  }
  router.push({
    path: '/practice',
    query: {
      chapterId: chapterIdStr.value,
      n: String(Math.min(activeNo.value, Math.max(total.value, 1))),
    },
  })
}

function selectNo(no) {
  if (!chapterIdStr.value) return
  router.push({
    path: '/practice',
    query: {
      chapterId: chapterIdStr.value,
      n: String(no),
    },
  })
}

watch(
  () => [chapterIdStr.value],
  async ([cid]) => {
    if (!cid) {
      showFailToast('缺少章节参数')
      router.replace('/home')
      return
    }
    await practiceStore.ensureChapter(cid)
    if (!practiceStore.loading && !practiceStore.questions.length) {
      showFailToast('暂无题目')
    }
  },
  { immediate: true },
)
</script>

<template>
  <div class="nav-page">
    <div class="shell">
      <header class="top-bar">
        <button type="button" class="ghost-btn" @click="goBack">返回</button>
        <span class="title">题目导航</span>
        <span class="spacer" />
      </header>

      <div v-if="practiceStore.loading" class="state-card">
        <van-loading type="spinner" color="#1989fa" />
        <span class="state-text">加载中...</span>
      </div>

      <section v-else class="card grid-card">
        <div class="hint">点击题号跳转</div>
        <div class="num-grid">
          <button
            v-for="no in numbers"
            :key="no"
            type="button"
            class="num-btn"
            :class="{ 'is-current': no === activeNo }"
            @click="selectNo(no)"
          >
            {{ no }}
          </button>
        </div>
        <div v-if="!numbers.length" class="empty">暂无题号</div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.nav-page {
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
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: background-color 0.2s, transform 0.1s;
}

.ghost-btn:active {
  background: #f2f3f5;
  transform: scale(0.98);
}

.title {
  font-size: 17px;
  font-weight: 700;
  color: #323233;
}

.spacer {
  width: 64px;
}

.state-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  padding: 40px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.state-text {
  font-size: 14px;
  color: #969799;
}

.grid-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 16px 14px 20px;
}

.hint {
  font-size: 13px;
  color: #969799;
  margin-bottom: 14px;
}

.num-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.num-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 1px solid #ebedf0;
  background: #f7f8fa;
  color: #323233;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.1s, background 0.2s, border-color 0.2s, color 0.2s;
}

.num-btn:active {
  transform: scale(0.96);
}

.num-btn.is-current {
  background: #1989fa;
  border-color: #1989fa;
  color: #fff;
  box-shadow: 0 2px 8px rgba(25, 137, 250, 0.35);
}

.empty {
  text-align: center;
  color: #969799;
  font-size: 14px;
  padding: 24px 0;
}
</style>
