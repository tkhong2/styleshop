<template>
  <div class="review-section">
    <div class="review-header">
      <h2>Đánh giá sản phẩm</h2>
      <div class="rating-summary" v-if="reviews.length > 0">
        <span class="big-rating">{{ avgRating.toFixed(1) }}</span>
        <div>
          <div class="stars-row">
            <span v-for="i in 5" :key="i" class="star" :class="{ filled: i <= Math.round(avgRating) }">★</span>
          </div>
          <p class="review-count">{{ reviews.length }} đánh giá</p>
        </div>
      </div>
    </div>

    <!-- Rating bars -->
    <div v-if="reviews.length > 0" class="rating-bars">
      <div v-for="n in [5,4,3,2,1]" :key="n" class="bar-row">
        <span class="bar-label">{{ n }}★</span>
        <div class="bar-track">
          <div class="bar-fill" :style="{ width: ratingPct(n) + '%' }"></div>
        </div>
        <span class="bar-count">{{ ratingCount(n) }}</span>
      </div>
    </div>

    <!-- Write review -->
    <div class="write-review">
      <h3>Viết đánh giá</h3>
      <div class="star-select">
        <span v-for="i in 5" :key="i" class="star-btn"
          :class="{ active: i <= form.rating, hover: i <= hoverRating }"
          @mouseenter="hoverRating = i" @mouseleave="hoverRating = 0"
          @click="form.rating = i">★</span>
        <span class="rating-text">{{ ratingLabels[form.rating - 1] || 'Chọn số sao' }}</span>
      </div>
      <div class="form-row">
        <input v-model="form.user_name" type="text" placeholder="Tên của bạn *" class="review-input" />
      </div>
      <textarea v-model="form.comment" placeholder="Nhận xét của bạn *" rows="3" class="review-input"></textarea>
      <button class="submit-btn" @click="submitReview" :disabled="submitting || !form.rating || !form.comment || !form.user_name">
        <span v-if="submitting"><i class="fas fa-spinner fa-spin"></i></span>
        <span v-else><i class="fas fa-paper-plane"></i> Gửi đánh giá</span>
      </button>
    </div>

    <!-- Reviews list -->
    <div v-if="reviews.length === 0" class="no-reviews">
      <i class="fas fa-comment-slash"></i>
      <p>Chưa có đánh giá nào. Hãy là người đầu tiên!</p>
    </div>
    <div v-else class="reviews-list">
      <div v-for="r in reviews" :key="r.id" class="review-item">
        <div class="review-avatar">{{ r.user_name[0]?.toUpperCase() }}</div>
        <div class="review-body">
          <div class="review-meta">
            <span class="reviewer-name">{{ r.user_name }}</span>
            <div class="review-stars">
              <span v-for="i in 5" :key="i" :class="['star', { filled: i <= r.rating }]">★</span>
            </div>
            <span class="review-date">{{ formatDate(r.created_at) }}</span>
          </div>
          <p class="review-comment">{{ r.comment }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { reviewService } from '@/services/reviewService.js'
import { useAuthStore } from '@/stores/auth.js'
import { useToastStore } from '@/stores/toast.js'

const props = defineProps({ productId: Number })
const auth = useAuthStore()
const toast = useToastStore()

const reviews = ref([])
const submitting = ref(false)
const hoverRating = ref(0)
const form = ref({ rating: 0, user_name: auth.user?.name || '', comment: '' })
const ratingLabels = ['Rất tệ', 'Tệ', 'Bình thường', 'Tốt', 'Xuất sắc']

onMounted(async () => {
  try { reviews.value = await reviewService.getByProduct(props.productId) } catch {}
})

const avgRating = computed(() => {
  if (!reviews.value.length) return 0
  return reviews.value.reduce((s, r) => s + r.rating, 0) / reviews.value.length
})

function ratingCount(n) { return reviews.value.filter(r => r.rating === n).length }
function ratingPct(n) { return reviews.value.length ? (ratingCount(n) / reviews.value.length) * 100 : 0 }

async function submitReview() {
  if (!form.value.rating || !form.value.comment.trim() || !form.value.user_name.trim()) return
  submitting.value = true
  try {
    const review = await reviewService.create({
      product_id: props.productId,
      user_id: auth.user?.email || null,
      user_name: form.value.user_name,
      rating: form.value.rating,
      comment: form.value.comment,
    })
    reviews.value.unshift(review)
    form.value = { rating: 0, user_name: auth.user?.name || '', comment: '' }
    toast.success('Cảm ơn bạn đã đánh giá!')
  } catch { toast.error('Không thể gửi đánh giá') }
  finally { submitting.value = false }
}

function formatDate(d) { return new Date(d).toLocaleDateString('vi-VN') }
</script>

<style scoped>
.review-section { margin-top: 48px; padding-top: 40px; border-top: 1px solid var(--gray2); }
.review-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.review-header h2 { font-size: 20px; font-weight: 700; }
.rating-summary { display: flex; align-items: center; gap: 12px; }
.big-rating { font-size: 40px; font-weight: 800; color: #f59e0b; line-height: 1; }
.stars-row { display: flex; gap: 2px; }
.star { font-size: 18px; color: #e2e8f0; }
.star.filled { color: #f59e0b; }
.review-count { font-size: 13px; color: #888; margin-top: 2px; }

.rating-bars { display: flex; flex-direction: column; gap: 6px; margin-bottom: 28px; max-width: 300px; }
.bar-row { display: flex; align-items: center; gap: 8px; font-size: 12px; }
.bar-label { width: 24px; color: #888; text-align: right; }
.bar-track { flex: 1; height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; background: #f59e0b; border-radius: 4px; transition: width 0.4s; }
.bar-count { width: 20px; color: #888; }

.write-review { background: #f8fafc; border-radius: 12px; padding: 20px; margin-bottom: 28px; }
.write-review h3 { font-size: 15px; font-weight: 700; margin-bottom: 14px; }
.star-select { display: flex; align-items: center; gap: 4px; margin-bottom: 12px; }
.star-btn { font-size: 28px; cursor: pointer; color: #e2e8f0; transition: color 0.15s; line-height: 1; }
.star-btn.active, .star-btn.hover { color: #f59e0b; }
.rating-text { font-size: 13px; color: #888; margin-left: 8px; }
.form-row { margin-bottom: 10px; }
.review-input { width: 100%; padding: 10px 14px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 14px; font-family: inherit; outline: none; resize: vertical; background: #fff; }
.review-input:focus { border-color: var(--black); }
textarea.review-input { margin-bottom: 12px; }
.submit-btn { display: flex; align-items: center; gap: 8px; padding: 11px 20px; background: var(--black); color: #fff; border-radius: 8px; font-size: 13px; font-weight: 600; }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.no-reviews { text-align: center; padding: 40px; color: #aaa; display: flex; flex-direction: column; align-items: center; gap: 10px; }
.no-reviews i { font-size: 32px; }
.reviews-list { display: flex; flex-direction: column; gap: 16px; }
.review-item { display: flex; gap: 14px; padding: 16px; background: #fff; border-radius: 10px; border: 1px solid var(--gray2); }
.review-avatar { width: 40px; height: 40px; border-radius: 50%; background: var(--black); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 16px; flex-shrink: 0; }
.review-meta { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; flex-wrap: wrap; }
.reviewer-name { font-size: 14px; font-weight: 600; }
.review-stars { display: flex; gap: 1px; }
.review-stars .star { font-size: 13px; color: #e2e8f0; }
.review-stars .star.filled { color: #f59e0b; }
.review-date { font-size: 12px; color: #aaa; }
.review-comment { font-size: 14px; color: #555; line-height: 1.6; }
</style>
