<template>
  <div class="support-page">
    <div class="container">
      <div class="breadcrumb">
        <RouterLink to="/">Trang chủ</RouterLink> /
        <span>Hướng dẫn chọn size</span>
      </div>

      <h1 class="page-title"><i class="fas fa-ruler"></i> Hướng dẫn chọn size</h1>

      <div class="content-grid">
        <div class="main-content">
          <!-- Áo -->
          <div class="section-card">
            <h2><i class="fas fa-tshirt"></i> Bảng size Áo</h2>
            <div class="table-wrap">
              <table class="size-table">
                <thead>
                  <tr><th>Size</th><th>Chiều cao (cm)</th><th>Cân nặng (kg)</th><th>Vòng ngực (cm)</th><th>Vòng eo (cm)</th></tr>
                </thead>
                <tbody>
                  <tr><td class="size-label">XS</td><td>150–155</td><td>40–45</td><td>76–80</td><td>60–64</td></tr>
                  <tr><td class="size-label">S</td><td>155–160</td><td>45–52</td><td>80–84</td><td>64–68</td></tr>
                  <tr><td class="size-label">M</td><td>160–165</td><td>52–58</td><td>84–88</td><td>68–72</td></tr>
                  <tr><td class="size-label">L</td><td>165–170</td><td>58–65</td><td>88–92</td><td>72–76</td></tr>
                  <tr><td class="size-label">XL</td><td>170–175</td><td>65–72</td><td>92–96</td><td>76–80</td></tr>
                  <tr><td class="size-label">XXL</td><td>175–180</td><td>72–80</td><td>96–100</td><td>80–84</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Quần -->
          <div class="section-card">
            <h2><i class="fas fa-male"></i> Bảng size Quần Jeans</h2>
            <div class="table-wrap">
              <table class="size-table">
                <thead>
                  <tr><th>Size (inch)</th><th>Vòng eo (cm)</th><th>Vòng mông (cm)</th><th>Dài quần (cm)</th></tr>
                </thead>
                <tbody>
                  <tr><td class="size-label">28</td><td>71–73</td><td>89–91</td><td>98–100</td></tr>
                  <tr><td class="size-label">29</td><td>74–76</td><td>92–94</td><td>99–101</td></tr>
                  <tr><td class="size-label">30</td><td>77–79</td><td>95–97</td><td>100–102</td></tr>
                  <tr><td class="size-label">31</td><td>80–82</td><td>98–100</td><td>101–103</td></tr>
                  <tr><td class="size-label">32</td><td>83–85</td><td>101–103</td><td>102–104</td></tr>
                  <tr><td class="size-label">34</td><td>87–89</td><td>105–107</td><td>103–105</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Váy/Đầm -->
          <div class="section-card">
            <h2><i class="fas fa-female"></i> Bảng size Váy & Đầm</h2>
            <div class="table-wrap">
              <table class="size-table">
                <thead>
                  <tr><th>Size</th><th>Vòng ngực (cm)</th><th>Vòng eo (cm)</th><th>Vòng mông (cm)</th></tr>
                </thead>
                <tbody>
                  <tr><td class="size-label">XS</td><td>76–80</td><td>60–64</td><td>84–88</td></tr>
                  <tr><td class="size-label">S</td><td>80–84</td><td>64–68</td><td>88–92</td></tr>
                  <tr><td class="size-label">M</td><td>84–88</td><td>68–72</td><td>92–96</td></tr>
                  <tr><td class="size-label">L</td><td>88–92</td><td>72–76</td><td>96–100</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Cách đo -->
          <div class="section-card">
            <h2><i class="fas fa-info-circle"></i> Cách đo số đo cơ thể</h2>
            <div class="measure-grid">
              <div class="measure-item" v-for="m in measures" :key="m.name">
                <div class="measure-icon"><i :class="m.icon"></i></div>
                <div>
                  <p class="measure-name">{{ m.name }}</p>
                  <p class="measure-desc">{{ m.desc }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar tips -->
        <aside class="sidebar">
          <div class="tip-card">
            <h3><i class="fas fa-lightbulb"></i> Mẹo chọn size</h3>
            <ul>
              <li>Nếu số đo nằm giữa 2 size, chọn size lớn hơn</li>
              <li>Với áo form rộng/oversize, có thể chọn nhỏ hơn 1 size</li>
              <li>Đo vào buổi sáng khi cơ thể chưa bị phù</li>
              <li>Đo trên người, không đo trên quần áo</li>
            </ul>
          </div>
          <div class="tip-card contact">
            <h3><i class="fas fa-headset"></i> Cần tư vấn?</h3>
            <p>Liên hệ hotline để được tư vấn size miễn phí</p>
            <a href="tel:18001162" class="contact-btn">
              <i class="fas fa-phone"></i> 091 708 0222
            </a>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
const measures = [
  { name: 'Vòng ngực', icon: 'fas fa-arrows-alt-h', desc: 'Đo vòng quanh phần ngực rộng nhất, giữ thước nằm ngang' },
  { name: 'Vòng eo', icon: 'fas fa-compress-alt', desc: 'Đo vòng quanh phần eo nhỏ nhất, thường trên rốn 2–3cm' },
  { name: 'Vòng mông', icon: 'fas fa-arrows-alt-h', desc: 'Đo vòng quanh phần mông rộng nhất' },
  { name: 'Chiều cao', icon: 'fas fa-arrows-alt-v', desc: 'Đứng thẳng, đo từ đỉnh đầu đến gót chân' },
]
</script>

<style scoped>
.support-page { padding: 40px 0 80px; background: #fafafa; min-height: 100vh; }
.breadcrumb { font-size: 13px; color: #888; margin-bottom: 24px; }
.breadcrumb a { color: #888; } .breadcrumb a:hover { color: #1a1a1a; }
.page-title { font-size: 28px; font-weight: 800; margin-bottom: 32px; display: flex; align-items: center; gap: 12px; }
.page-title i { color: #3b82f6; }
.content-grid { display: grid; grid-template-columns: 1fr 280px; gap: 28px; align-items: start; }
.section-card { background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.section-card h2 { font-size: 17px; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.section-card h2 i { color: #3b82f6; }
.table-wrap { overflow-x: auto; }
.size-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.size-table th { background: #1a1a1a; color: #fff; padding: 10px 14px; text-align: center; font-size: 12px; font-weight: 600; }
.size-table td { padding: 10px 14px; text-align: center; border-bottom: 1px solid #f0f0f0; }
.size-table tr:hover td { background: #f8fafc; }
.size-label { font-weight: 700; background: #eff6ff; color: #3b82f6; border-radius: 4px; }
.measure-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.measure-item { display: flex; gap: 12px; align-items: flex-start; padding: 12px; background: #f8fafc; border-radius: 8px; }
.measure-icon { width: 36px; height: 36px; background: #eff6ff; color: #3b82f6; border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.measure-name { font-size: 13px; font-weight: 600; margin-bottom: 4px; }
.measure-desc { font-size: 12px; color: #666; line-height: 1.5; }
.sidebar { display: flex; flex-direction: column; gap: 16px; position: sticky; top: 80px; }
.tip-card { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.tip-card h3 { font-size: 14px; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
.tip-card h3 i { color: #f59e0b; }
.tip-card ul { padding-left: 16px; display: flex; flex-direction: column; gap: 8px; }
.tip-card li { font-size: 13px; color: #555; line-height: 1.5; }
.tip-card.contact h3 i { color: #10b981; }
.tip-card p { font-size: 13px; color: #666; margin-bottom: 12px; }
.contact-btn { display: flex; align-items: center; justify-content: center; gap: 8px; background: #1a1a1a; color: #fff; padding: 11px; border-radius: 8px; font-size: 14px; font-weight: 600; }
.contact-btn:hover { background: #333; }
@media (max-width: 900px) { .content-grid { grid-template-columns: 1fr; } .sidebar { position: static; } .measure-grid { grid-template-columns: 1fr; } }
</style>
