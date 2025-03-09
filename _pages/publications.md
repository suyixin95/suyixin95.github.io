---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

---
title: "Nonlinear dynamic simulation and parametric analysis of a rotor-AMB-TDB system experiencing strong base shock excitations"
collection: publications
permalink: /publication/2021-paper-title-number-1
excerpt: 'This paper is about the number 1. The number 2 is left for future work.'
date: 2021
venue: 'Journal 1'
paperurl: 'https://www.sciencedirect.com/science/article/abs/pii/S0094114X20302913'
citation: 'Y Su, Y Gu, PS Keogh, S Yu, G Ren - Mechanism and Machine Theory, 2021'
---

[Download paper here](https://www.sciencedirect.com/science/article/abs/pii/S0094114X20302913)

Recommended citation: Y Su, Y Gu, PS Keogh, S Yu, G Ren - Mechanism and Machine Theory, 2021.

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
