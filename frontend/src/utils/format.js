export function formatPrice(price) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price)
}

export function discountPercent(original, current) {
  if (!original || original <= current) return 0
  return Math.round((1 - current / original) * 100)
}
