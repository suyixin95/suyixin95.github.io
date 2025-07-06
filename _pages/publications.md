# _pages/publications.md
---
title: "Publications"
layout: archive
permalink: /publications/
---

{% for pub in site.publications reversed %}
  <div class="publication-item">
    <h3>{{ pub.title }}</h3>
    <p>{{ pub.authors }}</p>
    <p><em>{{ pub.venue }}</em>, {{ pub.year }}</p>
    {% if pub.doi %}
      <p>DOI: <a href="https://doi.org/{{ pub.doi }}">{{ pub.doi }}</a></p>
    {% endif %}
  </div>
{% endfor %}

