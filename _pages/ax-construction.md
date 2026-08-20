---
permalink: /ax/construction/
title: "AX Insight · 건설"
layout: single
author_profile: true
domain: construction
---

{% assign d = "" %}{% for x in site.data.domains.ax %}{% if x.slug == page.domain %}{% assign d = x %}{% endif %}{% endfor %}
{% include domain-archive.html domain=d %}

---

[← AX Insight 전체 도메인](/ax/){: .btn .btn--inverse}
