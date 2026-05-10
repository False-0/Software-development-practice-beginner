<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showFailToast } from 'vant'
import { fetchForumList } from '../api/forum'

const router = useRouter()

const list = ref([])
const loading = ref(false)
const finished = ref(false)
const page = ref(1)

async function onLoad() {
  if (finished.value) return
  loading.value = true
  try {
    const data = await fetchForumList({
      page: page.value,
      pageSize: 15,
    })
    const chunk = data?.list || []
    list.value.push(...chunk)
    const hasMore = Boolean(data?.hasMore)
    if (!hasMore || !chunk.length) {
      finished.value = true
    } else {
      page.value += 1
    }
  } catch {
    showFailToast('加载失败')
    finished.value = true
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.replace('/comment')
}

function goDetail(postId) {
  router.push(`/comment/post/${postId}`)
}

</script>

<template>
  <div class="all-page">
    <div class="shell">
      <header class="top-bar">
        <button type="button" class="ghost-btn" @click="goBack">返回</button>
        <span class="title">全部帖子</span>
        <span class="spacer" />
      </header>

      <van-list
        v-model:loading="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="onLoad"
      >
        <div v-if="!list.length && finished && !loading" class="empty-tip">
          暂无帖子
        </div>

        <button
          v-for="item in list"
          :key="item.postId"
          type="button"
          class="post-row"
          @click="goDetail(item.postId)"
        >
          <span class="post-title">{{ item.title }}</span>
        </button>
      </van-list>
    </div>
  </div>
</template>

<style scoped>
.all-page {
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

.empty-tip {
  text-align: center;
  padding: 48px 16px;
  color: #969799;
  font-size: 14px;
}

.post-row {
  width: 100%;
  display: block;
  padding: 14px 12px;
  margin-bottom: 10px;
  border: none;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  text-align: left;
}

.post-row:active {
  background: #f7f8fa;
}

.post-title {
  font-size: 15px;
  font-weight: 600;
  color: #323233;
  line-height: 1.45;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
