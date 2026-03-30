import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

const ADMIN_EMAILS = ['khachong2102005@gmail.com']

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    children: [
      { path: '', component: () => import('@/views/Home.vue') },
      { path: 'products', component: () => import('@/views/Products.vue') },
      { path: 'products/:id', component: () => import('@/views/ProductDetail.vue') },
      { path: 'cart', component: () => import('@/views/Cart.vue') },
      { path: 'wishlist', component: () => import('@/views/Wishlist.vue') },
      { path: 'profile', component: () => import('@/views/Profile.vue') },
      { path: 'collections', component: () => import('@/views/Collections.vue') },
      { path: 'collections/:slug', component: () => import('@/views/Collections.vue') },
      { path: 'huong-dan-chon-size', component: () => import('@/views/support/SizeGuide.vue') },
      { path: 'cau-hoi-thuong-gap', component: () => import('@/views/support/FAQ.vue') },
      { path: 'chinh-sach-doi-tra', component: () => import('@/views/support/ReturnPolicy.vue') },
      { path: 'thanh-toan-giao-nhan', component: () => import('@/views/support/Shipping.vue') },
      { path: 'chinh-sach-bao-mat', component: () => import('@/views/support/Privacy.vue') },
    ]
  },
  { path: '/login', component: () => import('@/views/Login.vue') },
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    beforeEnter: (to, from, next) => {
      const auth = useAuthStore()
      if (!auth.isLoggedIn) {
        next('/login?redirect=' + to.fullPath)
      } else if (!ADMIN_EMAILS.includes(auth.user?.email)) {
        next('/')
      } else {
        next()
      }
    },
    children: [
      { path: '', component: () => import('@/views/admin/Dashboard.vue') },
      { path: 'orders', component: () => import('@/views/admin/Orders.vue') },
      { path: 'products', component: () => import('@/views/admin/Products.vue') },
      { path: 'customers', component: () => import('@/views/admin/Customers.vue') },
      { path: 'categories', component: () => import('@/views/admin/Categories.vue') },
      { path: 'stats', component: () => import('@/views/admin/Stats.vue') },
      { path: 'coupons', component: () => import('@/views/admin/Coupons.vue') },
      { path: 'profile', component: () => import('@/views/admin/AdminProfile.vue') },
    ]
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

export default router
