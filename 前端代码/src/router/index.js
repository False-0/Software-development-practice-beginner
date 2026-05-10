import { createRouter, createWebHistory } from 'vue-router'

function hasLogin() {
  try {
    const raw = localStorage.getItem('user')
    if (!raw) return false
    const parsed = JSON.parse(raw)
    return Boolean(parsed?.token)
  } catch {
    return false
  }
}

const routes = [
  {
    path: '/',
    redirect: '/home',
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/Home.vue'),
  },
  {
    path: '/rank',
    name: 'Rank',
    component: () => import('../views/Rank.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/wrong',
    name: 'Wrong',
    component: () => import('../views/Wrong.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/wrong/records',
    name: 'WrongRecords',
    component: () => import('../views/WrongRecords.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/wrong/stats',
    name: 'WrongStats',
    component: () => import('../views/WrongStats.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/comment/all',
    name: 'CommentAll',
    component: () => import('../views/CommentAll.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/comment/post/:postId',
    name: 'CommentDetail',
    component: () => import('../views/CommentDetail.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/comment',
    name: 'Comment',
    component: () => import('../views/Comment.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/mine',
    name: 'Mine',
    component: () => import('../views/Mine.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/mine/favorites',
    name: 'MineFavorite',
    component: () => import('../views/MineFavorite.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/mine/correct',
    name: 'MineCorrect',
    component: () => import('../views/MineCorrect.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/mine/password',
    name: 'MinePassword',
    component: () => import('../views/MinePassword.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/mine/profile',
    name: 'MineProfile',
    component: () => import('../views/MineProfile.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/practice',
    name: 'Practice',
    component: () => import('../views/Practice.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/practice/nav',
    name: 'PracticeNav',
    component: () => import('../views/PracticeNav.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/question',
    redirect: (to) => ({
      path: '/practice',
      query: to.query,
    }),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !hasLogin()) {
    next({ path: '/login', query: { redirect: to.fullPath } })
    return
  }
  next()
})

export default router
