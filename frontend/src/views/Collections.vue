<template>
  <div class="container page">
    <h1 class="page-title">Bộ Sưu Tập</h1>
    <div class="collections-grid">
      <RouterLink v-for="col in collections" :key="col.title" :to="col.href" class="col-card">
        <img :src="col.img" :alt="col.title" />
        <div class="col-overlay">
          <p class="col-sub">{{ col.sub }}</p>
          <h3>{{ col.title }}</h3>
          <p class="col-desc">{{ col.desc }}</p>
          <span class="col-cta">KHÁM PHÁ NGAY</span>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
const collections = [
  { title: 'Summer Wanted', sub: 'Bộ sưu tập hè 2026', desc: 'Một sắc đỏ cháy phố, một làn gió biển xanh mát...', img: 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=800&q=80', href: '/products?collection=summer' },
  { title: 'Dazzling Aura', sub: 'Bộ sưu tập đặc biệt', desc: 'Toả sáng theo cách của riêng bạn', img: 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=800&q=80', href: '/products?collection=dazzling' },
  { title: "Juno's Club", sub: 'Bộ sưu tập mới', desc: 'Những thiết kế trẻ trung, năng động', img: 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&q=80', href: '/products?collection=club' },
  { title: 'The Sweetest Spring', sub: 'Bộ sưu tập xuân', desc: 'Mở màn đầu xuân bằng những điều ngọt ngào nhất', img: 'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800&q=80', href: '/products?collection=spring' },
  { title: 'Jingle All Twinkle', sub: 'Bộ sưu tập đông', desc: 'Lấp lánh trong từng khoảnh khắc', img: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80', href: '/products?collection=winter' },
  { title: 'Áo Dài Giai Duyên', sub: 'Bộ sưu tập áo dài', desc: 'Câu chuyện về giai nhân duyên dáng', img: 'https://images.unsplash.com/photo-1594938298603-c8148c4b4357?w=800&q=80', href: '/products?collection=aodai' },
]
</script>

<style scoped>
.page { padding: 40px 20px 80px; }
.page-title { font-size: 28px; font-weight: 700; margin-bottom: 32px; text-transform: uppercase; letter-spacing: 1px; }
.collections-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.col-card { position: relative; aspect-ratio: 3/4; overflow: hidden; border-radius: 10px; display: block; }
.col-card img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s; }
.col-card:hover img { transform: scale(1.04); }
.col-overlay { position: absolute; inset: 0; background: linear-gradient(transparent 30%, rgba(0,0,0,0.75)); display: flex; flex-direction: column; justify-content: flex-end; padding: 28px; color: #fff; }
.col-sub { font-size: 11px; letter-spacing: 2px; text-transform: uppercase; opacity: 0.7; margin-bottom: 6px; }
.col-overlay h3 { font-size: 22px; font-weight: 700; margin-bottom: 8px; }
.col-desc { font-size: 13px; opacity: 0.8; margin-bottom: 14px; }
.col-cta { font-size: 12px; font-weight: 700; letter-spacing: 1px; border-bottom: 1px solid rgba(255,255,255,0.6); padding-bottom: 2px; width: fit-content; }
@media (max-width: 900px) { .collections-grid { grid-template-columns: 1fr 1fr; } }
@media (max-width: 600px) { .collections-grid { grid-template-columns: 1fr; } }
</style>
