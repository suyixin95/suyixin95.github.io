---
title: "Publications (论文)"
permalink: /publications/
---

论文按年份倒序排列；详细摘要请点击标题。更多信息见侧栏中的 Google Scholar。

{% assign papers = site.publications | sort: "year" | reverse %}
{% assign journals = papers | where: "category", "manuscripts" %}
{% assign conferences = papers | where: "category", "conferences" %}

{% if journals.size > 0 %}
<h2>Journal Articles / 期刊论文</h2>
<ul class="publication-list">
{% for paper in journals %}{% include publication-card.html paper=paper %}{% endfor %}
</ul>
{% endif %}

{% if conferences.size > 0 %}
<h2>Conference Papers / 会议论文</h2>
<ul class="publication-list">
{% for paper in conferences %}{% include publication-card.html paper=paper %}{% endfor %}
</ul>
{% endif %}
