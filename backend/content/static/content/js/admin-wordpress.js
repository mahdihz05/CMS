(function(){
  document.documentElement.lang='fa'; document.documentElement.dir='rtl';
  const map={'0':'۰','1':'۱','2':'۲','3':'۳','4':'۴','5':'۵','6':'۶','7':'۷','8':'۸','9':'۹'};
  const convert=(root)=>{const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let node;while(node=walker.nextNode()){if(node.parentElement&& !node.parentElement.closest('input,textarea,code,pre,[contenteditable=true]'))node.nodeValue=node.nodeValue.replace(/[0-9]/g,d=>map[d]);}};
  document.addEventListener('DOMContentLoaded',()=>{
    document.title=document.title.replace('Wagtail','مدیریت ویژنا');
    const loginTitle=document.querySelector('.login h1');if(loginTitle)loginTitle.textContent='ورود به مدیریت ویژنا';
    convert(document.body);
    const title=document.querySelector('#id_seo_title'), description=document.querySelector('#id_search_description'), slug=document.querySelector('#id_slug');
    if(title&&description){
      const box=document.createElement('section');box.className='visiona-serp';box.innerHTML='<div class="visiona-serp__label">پیش‌نمایش نتیجه گوگل</div><div class="visiona-serp__title"></div><div class="visiona-serp__url"></div><div class="visiona-serp__description"></div><hr><div class="visiona-serp__label">ارزیابی زنده سئو</div><ul class="visiona-seo-health"></ul>';
      title.closest('.w-panel')?.prepend(box);
      const update=()=>{box.querySelector('.visiona-serp__title').textContent=title.value||document.querySelector('#id_title')?.value||'عنوان صفحه';box.querySelector('.visiona-serp__url').textContent=location.origin+'/'+(slug?.value||'page')+'/';box.querySelector('.visiona-serp__description').textContent=description.value||'توضیحات متای این صفحه در اینجا نمایش داده می‌شود.';const checks=[[title.value.length>=30&&title.value.length<=60,'طول عنوان مناسب است','عنوان بهتر است ۳۰ تا ۶۰ نویسه باشد'],[description.value.length>=70&&description.value.length<=160,'طول توضیحات مناسب است','توضیحات بهتر است ۷۰ تا ۱۶۰ نویسه باشد']];const list=box.querySelector('.visiona-seo-health');list.replaceChildren(...checks.map(([ok,good,bad])=>{const li=document.createElement('li');li.className=ok?'is-good':'is-warning';li.textContent=ok?'✓ '+good:'⚠ '+bad;return li;}));};
      [title,description,slug].filter(Boolean).forEach(el=>el.addEventListener('input',update));update();
    }
    const ogTitle=document.querySelector('#id_og_title'),ogDescription=document.querySelector('#id_og_description');
    if(ogTitle&&ogDescription){const social=document.createElement('section');social.className='visiona-serp visiona-social';social.innerHTML='<div class="visiona-serp__label">پیش‌نمایش شبکه‌های اجتماعی</div><div class="visiona-social__image">تصویر اشتراک‌گذاری</div><div class="visiona-serp__title"></div><div class="visiona-serp__description"></div>';ogTitle.closest('.w-panel')?.prepend(social);const updateSocial=()=>{social.querySelector('.visiona-serp__title').textContent=ogTitle.value||title?.value||document.querySelector('#id_title')?.value||'عنوان صفحه';social.querySelector('.visiona-serp__description').textContent=ogDescription.value||description?.value||'توضیحات شبکه اجتماعی';};[ogTitle,ogDescription,title,description].filter(Boolean).forEach(el=>el.addEventListener('input',updateSocial));updateSocial();}
    if(slug&&slug.value){const initial=slug.value;slug.addEventListener('input',()=>{let warning=document.querySelector('.visiona-slug-warning');if(slug.value!==initial&&!warning){warning=document.createElement('p');warning.className='visiona-slug-warning';warning.textContent='با انتشار تغییر نامک، یک Redirect خودکار از نشانی قبلی ساخته می‌شود.';slug.parentElement.append(warning);}else if(slug.value===initial&&warning)warning.remove();});}
  });
})();
