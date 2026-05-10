<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showFailToast } from 'vant'
import { useUserStore } from '../store/user'
import request from '../utils/request'

const router = useRouter()
const userStore = useUserStore()

const totalDone = ref(0)
const subjects = ref([])
const selectedSubjectId = ref(null)
const chapters = ref([])
const loadingChapters = ref(false)

const authHeaders = computed(() => {
  const token = userStore.token
  if (!token) return {}
  return {
    Authorization: token.startsWith('Bearer ') ? token : `Bearer ${token}`,
  }
})

const subjectOptions = computed(() =>
  subjects.value.map((item) => ({
    text: item.name,
    value: item.id,
  })),
)

const subjectLabel = computed(() => {
  if (!subjectOptions.value.length || !selectedSubjectId.value) {
    return '临床医学（点击切换科目）'
  }
  const current = subjects.value.find((item) => item.id === selectedSubjectId.value)
  return current ? current.name : '临床医学（点击切换科目）'
})

async function fetchRankInfo() {
  const data = await request.get('/api/rank/info', {
    headers: authHeaders.value,
  })
  totalDone.value = data?.totalDone || 0
}

async function fetchSubjects() {
  const data = await request.get('/api/question/subjects', {
    params: {
      skip: 0,
      limit: 100,
    },
    headers: authHeaders.value,
  })
  subjects.value = Array.isArray(data) ? data : []
  if (subjects.value.length) {
    selectedSubjectId.value = subjects.value[0].id
  }
}

async function fetchChapters() {
  if (!selectedSubjectId.value) {
    chapters.value = []
    return
  }

  loadingChapters.value = true
  try {
    const data = await request.get('/api/question/chapters', {
      params: {
        subjectId: selectedSubjectId.value,
        page: 1,
        pageSize: 100,
      },
      headers: authHeaders.value,
    })
    chapters.value = data?.list || []
  } finally {
    loadingChapters.value = false
  }
}

async function onSubjectChange(value) {
  selectedSubjectId.value = value
  await fetchChapters()
}

function goRank() {
  router.push('/rank')
}

function goChapterQuestion(chapter) {
  router.push({
    path: '/practice',
    query: {
      chapterId: chapter.id,
      n: '1',
    },
  })
}

onMounted(async () => {
  try {
    await Promise.all([fetchRankInfo(), fetchSubjects()])
    await fetchChapters()
  } catch (error) {
    showFailToast('首页数据加载失败')
  }
})
</script>

<template>
  <div class="home-page">
    <div class="phone-shell">
      <div class="top-row">
        <div class="done-box">刷题量：{{ totalDone }}</div>
        <button class="rank-btn" @click="goRank">排行榜</button>
      </div>

      <div class="subject-card">
        <van-dropdown-menu active-color="#1989fa">
          <van-dropdown-item
            :model-value="selectedSubjectId"
            :options="subjectOptions"
            :title="subjectLabel"
            @change="onSubjectChange"
          />
        </van-dropdown-menu>
      </div>

      <div class="chapter-list">
        <div
          v-for="chapter in chapters"
          :key="chapter.id"
          class="chapter-item"
          @click="goChapterQuestion(chapter)"
        >
          {{ chapter.name }}
        </div>

        <div v-if="loadingChapters" class="empty-tip">章节加载中...</div>
        <div v-else-if="!chapters.length" class="empty-tip">暂无章节</div>
      </div>
    </div>

    <van-tabbar route fixed active-color="#1989fa" inactive-color="#7d7e80">
      <van-tabbar-item replace to="/home">主页</van-tabbar-item>
      <van-tabbar-item replace to="/wrong">错题</van-tabbar-item>
      <van-tabbar-item replace to="/comment">评论</van-tabbar-item>
      <van-tabbar-item replace to="/mine">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #f6f7fb;
  padding: 16px 16px 66px;
  box-sizing: border-box;
}

.phone-shell {
  max-width: 420px;
  margin: 0 auto;
}

.top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 14px 12px;
}

.done-box {
  font-size: 16px;
  font-weight: 700;
  color: #333;
}

.rank-btn {
  border: none;
  border-radius: 18px;
  background: #f2f3f5;
  color: #323233;
  padding: 8px 16px;
  font-size: 14px;
  transition: background-color 0.2s, transform 0.1s;
}

.rank-btn:hover {
  background: #e8eaee;
}

.rank-btn:active {
  background: #dfe2e7;
  transform: scale(0.98);
}

.subject-card {
  margin-top: 12px;
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
}

:deep(.van-dropdown-menu) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.van-dropdown-menu__bar) {
  height: 52px;
  box-shadow: none;
  background: #fff;
}

:deep(.van-dropdown-menu__item) {
  justify-content: flex-start;
  padding: 0 14px;
}

:deep(.van-dropdown-menu__title) {
  width: 100%;
  font-size: 16px;
  color: #323233;
}

:deep(.van-dropdown-item__option) {
  border-bottom: 1px solid #f0f1f3;
}

:deep(.van-dropdown-item__option:last-child) {
  border-bottom: none;
}

:deep(.van-cell--clickable:active) {
  background: #f7f8fa;
}

:deep(.van-dropdown-item__option--active) {
  color: #1989fa;
  font-weight: 600;
}

.chapter-list {
  margin-top: 12px;
}

.chapter-item {
  min-height: 50px;
  background: #fff;
  border-top: 1px solid #f0f1f3;
  border-bottom: 1px solid #f0f1f3;
  margin-bottom: 8px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  font-weight: 500;
  color: #333;
  transition: background-color 0.2s, transform 0.1s;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.04);
}

.chapter-item:hover {
  background: #f7f8fa;
}

.chapter-item:active {
  background: #eef1f4;
  transform: scale(0.995);
}

.empty-tip {
  margin-top: 8px;
  padding: 18px 0;
  text-align: center;
  color: #888;
  font-size: 14px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #f0f1f3;
}

:deep(.van-tabbar-item) {
  transition: background-color 0.2s;
}

:deep(.van-tabbar-item:active) {
  background: #f2f3f5;
}
</style>
