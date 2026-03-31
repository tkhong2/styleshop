/**
 * Composable để set meta tags SEO cho từng trang
 */
export function useSEO({ title, description, image, url } = {}) {
  const siteName = 'StyleShop'
  const defaultDesc = 'Thời trang chất lượng cao, phong cách hiện đại cho mọi người.'
  const defaultImg = 'https://styleshop-nine.vercel.app/favicon.svg'

  const fullTitle = title ? `${title} | ${siteName}` : siteName
  const metaDesc = description || defaultDesc
  const metaImg = image || defaultImg

  // Title
  document.title = fullTitle

  // Helper
  function setMeta(name, content, prop = false) {
    const attr = prop ? 'property' : 'name'
    let el = document.querySelector(`meta[${attr}="${name}"]`)
    if (!el) { el = document.createElement('meta'); el.setAttribute(attr, name); document.head.appendChild(el) }
    el.setAttribute('content', content)
  }

  setMeta('description', metaDesc)
  setMeta('og:title', fullTitle, true)
  setMeta('og:description', metaDesc, true)
  setMeta('og:image', metaImg, true)
  setMeta('og:type', 'website', true)
  setMeta('og:site_name', siteName, true)
  if (url) setMeta('og:url', url, true)
  setMeta('twitter:card', 'summary_large_image')
  setMeta('twitter:title', fullTitle)
  setMeta('twitter:description', metaDesc)
  setMeta('twitter:image', metaImg)
}
