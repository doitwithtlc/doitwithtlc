// TLC's owner-approved GA4 property. Never send form answers or board decisions.
(()=>{
 const id='G-7LYBLBWC4C';
 if(!['doitwithtlc.com','www.doitwithtlc.com'].includes(location.hostname)||location.pathname.startsWith('/website-preview/')||window.tlcAnalyticsLoaded)return;
 window.tlcAnalyticsLoaded=true;
 const page=new URL(location.href);page.search='';page.hash='';
 // Keep campaign attribution while dropping arbitrary inquiry/personal query values.
 const query=new URLSearchParams(location.search);
 for(const key of ['utm_source','utm_medium','utm_campaign','utm_id','utm_term','utm_content']){
  const value=query.get(key);if(value&&!/@|%40/i.test(value))page.searchParams.set(key,value.slice(0,100));
 }
 let referrer='';try{const ref=new URL(document.referrer);referrer=ref.origin+ref.pathname;}catch{}
 window.dataLayer=window.dataLayer||[];
 window.gtag=window.gtag||function(){window.dataLayer.push(arguments);};
 window.gtag('js',new Date());
 window.gtag('config',id,{
  page_location:page.href,page_referrer:referrer,
  allow_google_signals:false,allow_ad_personalization_signals:false
 });
 const script=document.createElement('script');script.async=true;
 script.src='https://www.googletagmanager.com/gtag/js?id='+id;
 document.head.append(script);
})();
