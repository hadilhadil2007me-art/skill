/* مهنتي – Opportunities Page Logic */

const OPPORTUNITIES = [
  { id: 1, icon: '⚡', profession: 'electricity', title: 'تدريب في الكهرباء المنزلية والصناعية', craftsman: 'الأستاذ كريم بلحاج', wilaya: 'الجزائر العاصمة', duration: '2 أشهر', spots: 3, rating: 4.9, reviews: 24, badge: 'open', badgeText: 'مفتوح' },
  { id: 2, icon: '🔧', profession: 'mechanics', title: 'تدريب على ميكانيك السيارات الحديثة', craftsman: 'ورشة الإخوة مزهود', wilaya: 'وهران', duration: '3 أشهر', spots: 2, rating: 4.8, reviews: 18, badge: 'few', badgeText: 'أماكن محدودة' },
  { id: 3, icon: '🍳', profession: 'cooking', title: 'تعلم الطبخ العربي والحلويات التقليدية', craftsman: 'الشيف نورة بن عيسى', wilaya: 'قسنطينة', duration: '6 أسابيع', spots: 5, rating: 5.0, reviews: 31, badge: 'open', badgeText: 'مفتوح' },
  { id: 4, icon: '🧵', profession: 'sewing', title: 'خياطة عصرية وأزياء تقليدية جزائرية', craftsman: 'أتيليه سمر', wilaya: 'البليدة', duration: '3 أشهر', spots: 4, rating: 4.7, reviews: 15, badge: 'open', badgeText: 'مفتوح' },
  { id: 5, icon: '🪚', profession: 'carpentry', title: 'نجارة وأثاث: من الأساسيات إلى الاحتراف', craftsman: 'محترف النجارة رضا', wilaya: 'سطيف', duration: '2 أشهر', spots: 2, rating: 4.6, reviews: 12, badge: 'few', badgeText: 'أماكن محدودة' },
  { id: 6, icon: '❄️', profession: 'cooling', title: 'تركيب وصيانة أنظمة التبريد والتكييف', craftsman: 'مؤسسة برودة المثالية', wilaya: 'عنابة', duration: '10 أسابيع', spots: 3, rating: 4.8, reviews: 20, badge: 'open', badgeText: 'مفتوح' },
  { id: 7, icon: '💻', profession: 'programming', title: 'تطوير تطبيقات الويب – HTML, CSS, JS', craftsman: 'مختبر الكود', wilaya: 'الجزائر العاصمة', duration: '4 أشهر', spots: 6, rating: 4.9, reviews: 42, badge: 'open', badgeText: 'مفتوح' },
  { id: 8, icon: '🎨', profession: 'design', title: 'التصميم الجرافيكي وهوية الأعمال', craftsman: 'استوديو الإبداع', wilaya: 'وهران', duration: '3 أشهر', spots: 4, rating: 4.7, reviews: 28, badge: 'open', badgeText: 'مفتوح' },
  { id: 9, icon: '⚡', profession: 'electricity', title: 'كهرباء الطاقة الشمسية وأنظمة الألواح', craftsman: 'الأستاذ حمزة طاهر', wilaya: 'بجاية', duration: '6 أسابيع', spots: 2, rating: 4.8, reviews: 9, badge: 'few', badgeText: 'أماكن محدودة' },
  { id: 10, icon: '🔧', profession: 'mechanics', title: 'صيانة الدراجات النارية والمحركات الصغيرة', craftsman: 'ورشة الأخ سفيان', wilaya: 'مسيلة', duration: '1.5 شهر', spots: 5, rating: 4.5, reviews: 7, badge: 'open', badgeText: 'مفتوح' },
  { id: 11, icon: '🍳', profession: 'cooking', title: 'صناعة المعجنات والكيك والحلويات الغربية', craftsman: 'مخبزة السعادة', wilaya: 'الجزائر العاصمة', duration: 'شهر', spots: 6, rating: 4.9, reviews: 35, badge: 'open', badgeText: 'مفتوح' },
  { id: 12, icon: '💻', profession: 'programming', title: 'تطوير تطبيقات الجوال مع Flutter', craftsman: 'المطور يونس مقدم', wilaya: 'قسنطينة', duration: '5 أشهر', spots: 3, rating: 5.0, reviews: 18, badge: 'open', badgeText: 'مفتوح' },
];

function renderCard(opp) {
  return `
    <div class="opp-card" id="opp-card-${opp.id}" data-profession="${opp.profession}">
      <div class="opp-icon-wrapper">${opp.icon}</div>
      <div class="opp-main">
        <span class="opp-badge badge-${opp.badge}">${opp.badgeText}</span>
        <h3>${opp.title}</h3>
        <div class="opp-meta">
          <span class="opp-tag">👤 ${opp.craftsman}</span>
          <span class="opp-tag">📍 ${opp.wilaya}</span>
          <span class="opp-tag">⏱ ${opp.duration}</span>
          <span class="opp-tag">👥 ${opp.spots} أماكن</span>
        </div>
      </div>
      <div style="text-align:center; flex-shrink:0; min-width:80px;">
        <div class="opp-rating">⭐ ${opp.rating}</div>
        <div style="font-size:0.75rem;color:var(--gray-400);margin-bottom:12px;">(${opp.reviews} تقييم)</div>
        <a href="register.html?type=trainee" class="btn btn-primary" id="apply-${opp.id}" style="padding:10px 20px;font-size:0.85rem;">تقدّم الآن</a>
      </div>
    </div>
  `;
}

function renderAll(list) {
  const grid = document.getElementById('opp-grid');
  if (!grid) return;
  if (list.length === 0) {
    grid.innerHTML = `<div style="text-align:center;padding:60px 0;color:var(--gray-400)"><div style="font-size:4rem">🔍</div><p style="margin-top:16px;font-size:1.1rem">لا توجد فرص تطابق بحثك</p></div>`;
    return;
  }
  grid.innerHTML = list.map(renderCard).join('');
}

document.addEventListener('DOMContentLoaded', () => {
  renderAll(OPPORTUNITIES);

  // Filter by profession via URL param
  const params = new URLSearchParams(window.location.search);
  const profParam = params.get('profession');
  if (profParam) {
    const filtered = OPPORTUNITIES.filter(o => o.profession === profParam);
    renderAll(filtered.length ? filtered : OPPORTUNITIES);
  }

  // Search button
  const searchBtn = document.getElementById('btn-search');
  if (searchBtn) {
    searchBtn.addEventListener('click', () => {
      const query = (document.getElementById('search-input')?.value || '').toLowerCase();
      const wilaya = document.getElementById('search-wilaya')?.value;
      const profession = document.getElementById('search-profession')?.value;
      let filtered = OPPORTUNITIES;
      if (query) filtered = filtered.filter(o => o.title.includes(query) || o.craftsman.includes(query));
      if (wilaya) filtered = filtered.filter(o => {
        const map = { '16': 'الجزائر العاصمة', '31': 'وهران', '25': 'قسنطينة', '09': 'البليدة', '06': 'بجاية', '23': 'عنابة', '19': 'سطيف', '29': 'مسيلة' };
        return o.wilaya === map[wilaya];
      });
      if (profession) filtered = filtered.filter(o => o.profession === profession);
      renderAll(filtered);
    });
  }

  // Filter sidebar
  document.querySelectorAll('.filter-option').forEach(opt => {
    opt.addEventListener('click', function() {
      const siblings = this.parentElement.querySelectorAll('.filter-option');
      siblings.forEach(s => s.classList.remove('active'));
      this.classList.add('active');
    });
  });
});
