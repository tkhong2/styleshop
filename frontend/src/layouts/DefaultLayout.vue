<template>
  <div>
    <Navbar />
    <CartSidebar />
    <ToastContainer />
    <PromoPopup />
    <QuickView :product="quickViewProduct" @close="quickViewProduct = null" />
    <main class="main-content">
      <RouterView @quickview="openQuickView" />
    </main>
    <AppFooter />
    <BottomNav />
  </div>
</template>

<script setup>
import { ref, provide } from 'vue'
import Navbar from '@/components/Navbar.vue'
import CartSidebar from '@/components/CartSidebar.vue'
import ToastContainer from '@/components/ToastContainer.vue'
import QuickView from '@/components/QuickView.vue'
import PromoPopup from '@/components/PromoPopup.vue'
import AppFooter from '@/components/AppFooter.vue'
import BottomNav from '@/components/BottomNav.vue'

const quickViewProduct = ref(null)
function openQuickView(product) { quickViewProduct.value = product }
provide('openQuickView', openQuickView)
</script>

<style scoped>
/* Thêm padding bottom trên mobile để không bị bottom nav che */
.main-content {
  min-height: 60vh;
}

@media (max-width: 768px) {
  .main-content {
    padding-bottom: 70px;
  }
}
</style>
