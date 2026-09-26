/* 뉴스레터 구독 제출.
   Apps Script 웹앱은 CORS 헤더를 주지 않으므로 no-cors 로 보낸다.
   응답 본문을 읽을 수 없으므로 전송 성공 여부만 낙관적으로 표시하고,
   실제 수신 확인은 Apps Script 가 보내는 메일 알림으로 한다. */
(function () {

  /* ── 공통 제출 처리 ──────────────────────────────
     본문 하단 폼(.nlbox)과 팝업 폼(.nlpop)이 같이 쓴다.
     팝업 폼에는 전화번호·광고동의 칸이 없으므로 있는 것만 읽는다. */
  function init(form) {
    var endpoint = form.getAttribute('data-nl-endpoint');
    var msg = form.querySelector('.nlbox__msg');
    var btn = form.querySelector('.nlbox__submit');

    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var email = form.email.value.trim();

      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
        return say('이메일 주소를 확인해 주세요.', 'is-err');
      }
      if (!form.consent.checked) {
        return say('개인정보 수집·이용 동의가 필요합니다.', 'is-err');
      }

      btn.disabled = true;
      say('전송 중…', '');

      /* 고른 관심 분야. 하나도 안 고르면 공통으로 본다. */
      var picked = [];
      var boxes = form.querySelectorAll('input[name=domain]:checked');
      for (var i = 0; i < boxes.length; i++) picked.push(boxes[i].value);
      if (!picked.length) picked = ['AX 공통'];

      fetch(endpoint, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'text/plain;charset=utf-8' },
        body: JSON.stringify({
          email: email,
          phone: form.phone ? form.phone.value.trim() : '',
          consent: true,
          marketing: form.marketing ? form.marketing.checked : false,
          domains: picked.join('·'),
          website: form.website.value,
          source: location.pathname
        })
      }).then(function () {
        form.reset();
        say('구독 신청이 접수됐습니다. 감사합니다.', 'is-ok');
        form.dispatchEvent(new CustomEvent('nl:success', { bubbles: true }));
      }).catch(function () {
        say('전송에 실패했습니다. 잠시 후 다시 시도해 주세요.', 'is-err');
      }).then(function () {
        btn.disabled = false;
      });
    });

    function say(text, cls) { msg.textContent = text; msg.className = 'nlbox__msg ' + cls; }
  }


  /* ── 읽는 중 팝업 ────────────────────────────────
     본문 55% 지점에서 한 번 뜬다.
     닫으면 5분간, 구독하면 영구히 다시 뜨지 않는다. */
  var SNOOZE_MS = 5 * 60 * 1000;
  var KEY_SNOOZE = 'nlpop_snooze';
  var KEY_DONE = 'nlpop_done';

  /* 시크릿 창이나 저장소 차단 시 접근 자체가 예외를 던진다 */
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  function suppressed() {
    if (get(KEY_DONE)) return true;
    var t = parseInt(get(KEY_SNOOZE), 10);
    return !!t && (Date.now() - t) < SNOOZE_MS;
  }

  function initPopup(pop) {
    if (suppressed()) return;

    var content = document.querySelector('.page__content');
    var inline = document.querySelector('.nlbox');
    if (!content) return;

    var shown = false;
    var lastFocus = null;

    function open() {
      if (shown) return;
      /* 하단 폼이 이미 화면에 있으면 같은 걸 두 번 보여주는 셈이라 띄우지 않는다 */
      if (inline) {
        var r = inline.getBoundingClientRect();
        if (r.top < window.innerHeight && r.bottom > 0) return;
      }
      shown = true;
      lastFocus = document.activeElement;
      pop.hidden = false;
      var input = pop.querySelector('input[name=email]');
      if (input) input.focus();
      window.removeEventListener('scroll', onScroll);
    }

    function close(done) {
      pop.hidden = true;
      set(done ? KEY_DONE : KEY_SNOOZE, done ? '1' : String(Date.now()));
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    function onScroll() {
      var box = content.getBoundingClientRect();
      var readTo = window.innerHeight - box.top;       /* 본문에서 읽어 내려온 높이 */
      if (readTo > box.height * 0.55) open();
    }

    var closers = pop.querySelectorAll('[data-nlpop-close]');
    for (var i = 0; i < closers.length; i++) {
      closers[i].addEventListener('click', function () { close(false); });
    }
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && !pop.hidden) close(false);
    });
    pop.addEventListener('nl:success', function () {
      setTimeout(function () { close(true); }, 1600);
    });

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();   /* 짧은 글이라 이미 55% 를 넘겼을 수 있다 */
  }


  document.addEventListener('DOMContentLoaded', function () {
    var forms = document.querySelectorAll('.nlbox__form[data-nl-endpoint]');
    for (var i = 0; i < forms.length; i++) init(forms[i]);

    var pop = document.getElementById('nlpop');
    if (pop) initPopup(pop);
  });
})();
