import { createRouter, createWebHistory } from 'vue-router'

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
    ]
  },
  { path: '/login', component: () => import('@/views/Login.vue') },
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    children: [
      { path: '', component: () => import('@/views/admin/Dashboard.vue') },
      { path: 'orders', component: () => import('@/views/admin/Orders.vue') },
      { path: 'products', component: () => import('@/views/admin/Products.vue') },
      { path: 'customers', component: () => import('@/views/admin/Customers.vue') },
      { path: 'categories', component: () => import('@/views/admin/Categories.vue') },
      { path: 'stats', component: () => import('@/views/admin/Stats.vue') },
    ]
  },
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})
