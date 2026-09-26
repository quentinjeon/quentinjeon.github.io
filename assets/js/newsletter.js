/* 뉴스레터 구독 제출.
   Apps Script 웹앱은 CORS 헤더를 주지 않으므로 no-cors 로 보낸다.
   응답 본문을 읽을 수 없으므로 전송 성공 여부만 낙관적으로 표시하고,
   실제 수신 확인은 Apps Script 가 보내는 메일 알림으로 한다. */
(function () {
  function init(form) {
    var endpoint = form.getAttribute('data-nl-endpoint');
    var msg = form.querySelector('.nlbox__msg');
    var btn = form.querySelector('.nlbox__submit');

    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var email = form.email.value.trim();
      var consent = form.consent.checked;

      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
        return say('이메일 주소를 확인해 주세요.', 'is-err');
      }
      if (!consent) {
        return say('개인정보 수집·이용 동의가 필요합니다.', 'is-err');
      }

      btn.disabled = true;
      say('전송 중…', '');

      fetch(endpoint, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'text/plain;charset=utf-8' },
        body: JSON.stringify({
          email: email,
          phone: form.phone.value.trim(),
          consent: true,
          website: form.website.value,
          source: location.pathname
        })
      }).then(function () {
        form.reset();
        say('구독 신청이 접수됐습니다. 감사합니다.', 'is-ok');
      }).catch(function () {
        say('전송에 실패했습니다. 잠시 후 다시 시도해 주세요.', 'is-err');
      }).then(function () {
        btn.disabled = false;
      });
    });

    function say(text, cls) { msg.textContent = text; msg.className = 'nlbox__msg ' + cls; }
  }

  document.addEventListener('DOMContentLoaded', function () {
    var forms = document.querySelectorAll('.nlbox__form[data-nl-endpoint]');
    for (var i = 0; i < forms.length; i++) init(forms[i]);
  });
})();
