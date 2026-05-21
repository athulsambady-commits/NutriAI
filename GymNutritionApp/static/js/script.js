document.addEventListener('DOMContentLoaded', function(){
  // Simple form validation
  const form = document.querySelector('form#calcForm');
  if(form){
    form.addEventListener('submit', function(e){
      const weight = parseFloat(form.weight.value||0);
      const height = parseFloat(form.height.value||0);
      if(!weight || !height){
        e.preventDefault();
        alert('Please provide valid weight and height.');
        return false;
      }
      const btn = document.querySelector('button[type=submit]');
      btn.dataset.original = btn.innerHTML;
      btn.innerHTML = 'Calculating...';
      btn.disabled = true;
    });
  }

  // Scroll reveal
  const observers = document.querySelectorAll('.fade-up');
  const io = new IntersectionObserver(entries=>{
    entries.forEach(e=>{
      if(e.isIntersecting) e.target.classList.add('in-view');
    });
  },{threshold:0.15});
  observers.forEach(o=>io.observe(o));

  // Animated counters
  document.querySelectorAll('.count-up').forEach(node=>{
    const end = parseInt(node.dataset.to||0,10);
    let cur=0;const step=Math.max(1,Math.round(end/60));
    const t=setInterval(()=>{cur+=step; if(cur>=end){node.textContent=end;clearInterval(t)}else node.textContent=cur;},16);
  });
});
