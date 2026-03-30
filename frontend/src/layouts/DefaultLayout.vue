<template>
  <div>
    <Navbar />
    <CartSidebar />
    <ToastContainer />
    <main style="min-height: 60vh">
      <RouterView />
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import CartSidebar from '@/components/CartSidebar.vue'
import ToastContainer from '@/components/ToastContainer.vue'
import AppFooter from '@/components/AppFooter.vue'
</script>
