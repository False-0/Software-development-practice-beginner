<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showFailToast, showSuccessToast } from 'vant'
import { checkFavorite, addFavorite, cancelFavorite } from '../api/favorite'
import { submitAnswer } from '../api/practice'
import { usePracticeStore } from '../store/practice'

const route = useRoute()
const router = useRouter()
const practiceStore = usePracticeStore()

const selectedAnswer = ref(null)
const submitted = ref(false)
const submitResult = ref(null)
const isFavorite = ref(false)
const submitting = ref(false)
const favoriteLoading = ref(false)

const chapterIdStr = computed(() => {
  const c = route.query.chapterId
  return c != null ? String(c) : ''
})

const questionNo = computed(() => {
  const n = Number(route.query.n)
  if (!Number.isFinite(n) || n < 1) return 1
  return Math.floor(n)
})

const questions = computed(() => practiceStore.questions)

const currentIndex = computed(() => {
  const len = questions.value.length
  if (!len) return 0
  const idx = questionNo.value - 1
  if (idx < 0) return 0
  if (idx >= len) return len - 1
  return idx
})

const currentQuestion = computed(() => questions.value[currentIndex.value] || null)

const isFirst = computed(() => currentIndex.value <= 0)
const isLast = computed(() => {
  const len = questions.value.length
  return len === 0 || currentIndex.value >= len - 1
})

const optionRows = computed(() => {
  const q = currentQuestion.value
  if (!q) return []
  return [
    { key: 'A', text: q.optionA },
    { key: 'B', text: q.optionB },
    { key: 'C', text: q.optionC },
    { key: 'D', text: q.optionD },
  ]
})

function optionClass(key) {
  const cls = ['opt-row']
  if (selectedAnswer.value === key) cls.push('is-selected')
  if (!submitted.value || !submitResult.value) return cls.join(' ')
  const correct = String(submitResult.value.correct_answer || submitResult.value.correctAnswer || '').toUpperCase()
  if (key === correct) cls.push('is-correct')
  if (selectedAnswer.value === key && key !== correct) cls.push('is-wrong')
  return cls.join(' ')
}

function onPickOption(key) {
  if (submitted.value) return
  selectedAnswer.value = key
}

async function loadFavorite() {
  const id = currentQuestion.value?.id
  if (id == null) return
  try {
    const data = await checkFavorite(id)
    isFavorite.value = data?.isFavorite === true
  } catch {
    isFavorite.value = false
  }
}

async function toggleFavorite() {
  const id = currentQuestion.value?.id
  if (id == null || favoriteLoading.value) return
  favoriteLoading.value = true
  try {
    if (isFavorite.value) {
      try {
        await cancelFavorite(id)
      } catch {
        /* 404 等由拦截器提示；仍同步本地状态 */
      }
      isFavorite.value = false
      showSuccessToast('已取消收藏')
    } else {
      await addFavorite(id)
      isFavorite.value = true
      showSuccessToast('收藏成功')
    }
  } finally {
    favoriteLoading.value = false
  }
}

async function onSubmit() {
  const q = currentQuestion.value
  if (!q?.id || !selectedAnswer.value || submitted.value || submitting.value) return
  submitting.value = true
  try {
    const data = await submitAnswer(q.id, selectedAnswer.value)
    submitted.value = true
    submitResult.value = data
  } catch {
    submitted.value = false
    submitResult.value = null
  } finally {
    submitting.value = false
  }
}

function syncRouteIfNeeded() {
  const len = questions.value.length
  if (!len) return
  let n = questionNo.value
  if (n < 1) n = 1
  if (n > len) n = len
  if (String(route.query.n) !== String(n) || String(route.query.chapterId) !== chapterIdStr.value) {
    router.replace({
      path: '/practice',
      query: { chapterId: chapterIdStr.value, n: String(n) },
    })
  }
}

/** 固定回到首页章节列表，避免从导航页进入刷题后「返回」落到导航页 */
function goBack() {
  router.replace('/home')
}

function openNav() {
  if (!chapterIdStr.value) return
  router.push({
    path: '/practice/nav',
    query: {
      chapterId: chapterIdStr.value,
      n: String(questionNo.value),
    },
  })
}

function goPrev() {
  if (isFirst.value || !chapterIdStr.value) return
  router.replace({
    path: '/practice',
    query: { chapterId: chapterIdStr.value, n: String(questionNo.value - 1) },
  })
}

function goNext() {
  if (isLast.value || !chapterIdStr.value) return
  router.replace({
    path: '/practice',
    query: { chapterId: chapterIdStr.value, n: String(questionNo.value + 1) },
  })
}

watch(
  () => currentQuestion.value?.id,
  () => {
    selectedAnswer.value = null
    submitted.value = false
    submitResult.value = null
    loadFavorite()
  },
)

watch([questions, () => route.query.n, chapterIdStr], () => {
  syncRouteIfNeeded()
})

onMounted(() => {
  if (!chapterIdStr.value) {
    showFailToast('缺少章节参数')
    router.replace('/home')
  }
})

watch(
  () => [chapterIdStr.value, practiceStore.loading],
  async ([cid]) => {
    if (!cid) return
    await practiceStore.ensureChapter(cid)
    if (!practiceStore.loading && !practiceStore.questions.length) {
      showFailToast('暂无题目')
    }
    syncRouteIfNeeded()
  },
  { immediate: true },
)
</script>

<template>
  <div class="practice-page">
    <div class="shell">
      <header class="top-bar">
        <button type="button" class="ghost-btn" @click="goBack">返回</button>
        <button
          type="button"
          class="menu-btn"
          aria-label="题目导航"
          @click="openNav"
        >
          <span class="menu-line" />
          <span class="menu-line" />
          <span class="menu-line" />
        </button>
      </header>

      <div v-if="practiceStore.loading" class="state-card">
        <van-loading type="spinner" color="#1989fa" />
        <span class="state-text">题目加载中...</span>
      </div>

      <template v-else-if="currentQuestion">
        <section class="card question-card">
          <button
            type="button"
            class="fav-btn"
            :disabled="favoriteLoading"
            aria-label="收藏"
            @click="toggleFavorite"
          >
            <van-icon
              :name="isFavorite ? 'star' : 'star-o'"
              :class="['fav-icon', { 'is-on': isFavorite }]"
            />
          </button>

          <div class="progress">
            {{ currentIndex + 1 }} / {{ questions.length }}
          </div>

          <div class="question-title">{{ currentQuestion.title }}</div>

          <div class="options">
            <button
              v-for="row in optionRows"
              :key="row.key"
              type="button"
              :class="optionClass(row.key)"
              @click="onPickOption(row.key)"
            >
              <span class="opt-key">{{ row.key }}.</span>
              <span class="opt-text">{{ row.text }}</span>
            </button>
          </div>

          <van-button
            class="submit-btn"
            type="primary"
            block
            round
            :disabled="!selectedAnswer || submitted || submitting"
            :loading="submitting"
            @click="onSubmit"
          >
            {{ submitted ? '已提交' : '提交答案' }}
          </van-button>

          <div v-if="submitted && submitResult" class="answer-block">
            <div class="answer-label">正确答案为：</div>
            <div class="answer-value">
              {{ String(submitResult.correct_answer || submitResult.correctAnswer || currentQuestion.answer || '—').toUpperCase() }}
            </div>
            <div
              class="result-tip"
              :class="submitResult.is_correct ? 'is-ok' : 'is-bad'"
            >
              {{ submitResult.is_correct ? '回答正确' : '回答错误' }}
            </div>
          </div>
        </section>
      </template>

      <div v-else-if="!practiceStore.loading" class="state-card">
        <span class="state-text">暂无题目</span>
      </div>

      <footer class="footer-nav">
        <button
          type="button"
          class="nav-lg"
          :class="{ 'is-disabled': isFirst }"
          :disabled="isFirst"
          @click="goPrev"
        >
          上一题
        </button>
        <button
          type="button"
          class="nav-lg"
          :class="{ 'is-disabled': isLast }"
          :disabled="isLast"
          @click="goNext"
        >
          下一题
        </button>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.practice-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 16px;
  padding-bottom: 100px;
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

.menu-btn {
  width: 44px;
  height: 36px;
  border: none;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 0 10px;
  transition: background-color 0.2s;
}

.menu-btn:active {
  background: #f2f3f5;
}

.menu-line {
  display: block;
  width: 18px;
  height: 2px;
  background: #323233;
  border-radius: 1px;
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

.question-card {
  position: relative;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 16px 14px 18px;
}

.fav-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 40px;
  height: 40px;
  border: none;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.fav-icon {
  font-size: 22px;
  color: #c8c9cc;
}

.fav-icon.is-on {
  color: #ff976a;
}

.progress {
  font-size: 13px;
  color: #969799;
  margin-bottom: 8px;
  padding-right: 36px;
}

.question-title {
  font-size: 16px;
  font-weight: 600;
  color: #323233;
  line-height: 1.55;
  margin-bottom: 16px;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
}

.opt-row {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  width: 100%;
  text-align: left;
  padding: 12px 12px;
  border-radius: 10px;
  border: 1px solid #ebedf0;
  background: #fafafa;
  font-size: 15px;
  color: #323233;
  transition: border-color 0.2s, background 0.2s;
}

.opt-row.is-selected {
  border-color: #1989fa;
  background: #ecf5ff;
}

.opt-row.is-correct {
  border-color: #07c160;
  background: #e8f7ef;
}

.opt-row.is-wrong {
  border-color: #ee0a24;
  background: #ffe9ec;
}

.opt-key {
  flex-shrink: 0;
  font-weight: 700;
  color: #646566;
}

.opt-text {
  flex: 1;
  line-height: 1.45;
}

.submit-btn {
  margin-bottom: 14px;
}

.answer-block {
  padding-top: 4px;
  border-top: 1px solid #f0f1f3;
}

.answer-label {
  font-size: 14px;
  color: #646566;
  margin-bottom: 6px;
}

.answer-value {
  font-size: 20px;
  font-weight: 700;
  color: #1989fa;
  margin-bottom: 8px;
}

.result-tip {
  font-size: 14px;
  font-weight: 600;
}

.result-tip.is-ok {
  color: #07c160;
}

.result-tip.is-bad {
  color: #ee0a24;
}

.footer-nav {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  max-width: 420px;
  margin: 0 auto;
  padding: 12px 16px calc(12px + env(safe-area-inset-bottom));
  display: flex;
  gap: 12px;
  background: linear-gradient(180deg, rgba(245, 247, 250, 0) 0%, #f5f7fa 16%);
  box-sizing: border-box;
}

.nav-lg {
  flex: 1;
  border: none;
  border-radius: 10px;
  padding: 12px 16px;
  font-size: 15px;
  font-weight: 600;
  background: #fff;
  color: #323233;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  transition: transform 0.1s, opacity 0.2s;
}

.nav-lg:active:not(:disabled) {
  transform: scale(0.98);
}

.nav-lg.is-disabled,
.nav-lg:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  box-shadow: none;
}
</style>
