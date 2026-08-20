---
permalink: /ax/foundation/
title: "AX Insight · 파운데이션"
layout: single
author_profile: true
domain: foundation
---

{% assign d = "" %}{% for x in site.data.domains.ax %}{% if x.slug == page.domain %}{% assign d = x %}{% endif %}{% endfor %}
{% include domain-archive.html domain=d %}

---

[← AX Insight 전체 도메인](/ax/){: .btn .btn--inverse}
