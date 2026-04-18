(function(){
  var PASS_HASH = '6c65696e6c65696e';
  function toHex(s){return s.split('').map(function(c){return c.charCodeAt(0).toString(16)}).join('')}
  if(sessionStorage.getItem('_auth') === PASS_HASH) return;
  document.documentElement.style.visibility='hidden';
  window.addEventListener('DOMContentLoaded',function(){
    document.body.style.visibility='hidden';
    var overlay=document.createElement('div');
    overlay.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;background:#f5f5f5;display:flex;align-items:center;justify-content:center;z-index:999999;visibility:visible';
    overlay.innerHTML='<div style="text-align:center;font-family:-apple-system,sans-serif"><h2 style="color:#333;margin-bottom:20px">このページは限定公開です</h2><input id="_pw" type="password" placeholder="パスワードを入力" style="padding:12px 16px;font-size:16px;border:2px solid #ddd;border-radius:8px;width:240px;outline:none"><br><button id="_btn" style="margin-top:12px;padding:10px 32px;font-size:15px;background:#333;color:#fff;border:none;border-radius:8px;cursor:pointer">確認</button><p id="_err" style="color:#e33;margin-top:10px;display:none">パスワードが違います</p></div>';
    document.body.appendChild(overlay);
    var inp=document.getElementById('_pw'),btn=document.getElementById('_btn'),err=document.getElementById('_err');
    function check(){
      if(toHex(inp.value)===PASS_HASH){sessionStorage.setItem('_auth',PASS_HASH);overlay.remove();document.documentElement.style.visibility='';document.body.style.visibility=''}
      else{err.style.display='block';inp.value='';inp.focus()}
    }
    btn.addEventListener('click',check);
    inp.addEventListener('keydown',function(e){if(e.key==='Enter')check()});
    inp.focus();
  });
})();
