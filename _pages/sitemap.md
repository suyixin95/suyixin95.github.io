---
title: "Sitemap (站点地图)"
permalink: /sitemap/
---

{% for item in site.data.navigation.main %}
- [{{ item.title }}]({{ item.url | relative_url }})
{% endfor %}

## Publications / 论文

{% assign papers = site.publications | sort: "year" | reverse %}
{% for paper in papers %}
- [{{ paper.title }}]({{ paper.url | relative_url }})
{% endfor %}

[XML Sitemap]({{ '/sitemap.xml' | relative_url }})
