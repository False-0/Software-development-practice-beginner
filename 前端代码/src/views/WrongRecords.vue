<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showConfirmDialog, showFailToast, showSuccessToast } from 'vant'
import { deleteErrorByQuestionId, fetchAllErrors } from '../api/error'

const router = useRouter()

const loading = ref(true)
const list = ref([])
/** 选中的题目 ID（与删除接口路径参数一致） */
const selectedIds = ref([])

function normalizeRow(item) {
  return {
    ...item,
    optionA: item.optionA ?? item.option_a ?? '',
    optionB: item.optionB ?? item.option_b ?? '',
    optionC: item.optionC ?? item.option_c ?? '',
    optionD: item.optionD ?? item.option_d ?? '',
  }
}

async function loadList() {
  loading.value = true
  try {
    const raw = await fetchAllErrors()
    list.value = raw.map(normalizeRow)
    selectedIds.value = selectedIds.value.filter((id) =>
      list.value.some((row) => row.id === id),
    )
  } catch {
    showFailToast('错题列表加载失败')
    list.value = []
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.replace('/wrong')
}

function clearSelection() {
  selectedIds.value = []
}

async function batchDelete() {
  if (!selectedIds.value.length) {
    showFailToast('请先选择要删除的错题')
    return
  }
  try {
    await showConfirmDialog({
      title: '删除错题',
      message: `确定删除选中的 ${selectedIds.value.length} 条记录吗？`,
    })
  } catch {
    return
  }

  const ids = [...selectedIds.value]
  try {
    await Promise.all(ids.map((id) => deleteErrorByQuestionId(id)))
    showSuccessToast('删除成功')
    selectedIds.value = []
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
  <div class="records-page">
    <div class="shell">
      <header class="top-bar">
        <button type="button" class="ghost-btn" @click="goBack">返回</button>
        <button type="button" class="mid-btn" @click="clearSelection">清空</button>
        <button type="button" class="ghost-btn danger" @click="batchDelete">删除</button>
      </header>

      <div v-if="loading" class="state-card">
        <van-loading type="spinner" color="#1989fa" size="28px" />
        <span class="state-text">加载中...</span>
      </div>

      <van-checkbox-group v-else v-model="selectedIds" class="list-wrap">
        <div v-if="!list.length" class="empty-tip">暂无错题记录</div>

        <div
          v-for="item in list"
          :key="item.errorId ?? item.id"
          class="q-card"
        >
          <van-checkbox :name="item.id" class="q-check" icon-size="20px" />
          <div class="q-body">
            <div class="q-title">{{ item.title }}</div>
            <div class="q-opts">
              <div class="opt-line"><span class="opt-key">a.</span>{{ item.optionA }}</div>
              <div class="opt-line"><span class="opt-key">b.</span>{{ item.optionB }}</div>
              <div class="opt-line"><span class="opt-key">c.</span>{{ item.optionC }}</div>
              <div class="opt-line"><span class="opt-key">d.</span>{{ item.optionD }}</div>
            </div>
            <div class="q-answer">
              正确答案为：<span class="ans-val">{{ String(item.answer || '').toUpperCase() }}</span>
            </div>
          </div>
        </div>
      </van-checkbox-group>
    </div>
  </div>
</template>

<style scoped>
.records-page {
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
  gap: 8px;
  margin-bottom: 12px;
}

.ghost-btn {
  flex: 1;
  border: none;
  border-radius: 8px;
  background: #fff;
  color: #323233;
  padding: 10px 8px;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: background-color 0.2s, transform 0.1s;
}

.ghost-btn:active {
  background: #f2f3f5;
  transform: scale(0.98);
}

.ghost-btn.danger {
  color: #ee0a24;
}

.mid-btn {
  flex: 1;
  border: none;
  border-radius: 8px;
  background: #fff;
  color: #1989fa;
  padding: 10px 8px;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.mid-btn:active {
  background: #f2f3f5;
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

.q-check {
  position: absolute;
  top: 12px;
  right: 10px;
}

.q-body {
  min-width: 0;
}

.q-title {
  font-size: 15px;
  font-weight: 600;
  color: #323233;
  line-height: 1.5;
  margin-bottom: 10px;
  padding-right: 4px;
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
