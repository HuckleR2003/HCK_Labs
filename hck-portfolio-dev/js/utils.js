// js/utils.js
// simple helpers

window.debounce = function(fn, wait=80){
  let t;
  return function(...args){
    clearTimeout(t);
    t = setTimeout(()=> fn.apply(this, args), wait);
  };
};

window.clamp = function(v, a=0, b=1){
  return Math.max(a, Math.min(b, v));
};
