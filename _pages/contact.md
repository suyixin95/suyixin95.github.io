---
title: "Contact (联系方式)"
permalink: /contact/
redirect_from:
  - /portfolio/
  - /portfolio/portfolio-1/
---

Feel free to connect with me! 欢迎与我联系交流！

Email / 邮箱：[{{ site.data.profile.email }}](mailto:{{ site.data.profile.email }})

{% for link in site.data.profile.links %}
- [{{ link.label }}]({{ link.url }})
{% endfor %}

{% if site.data.profile.wechat_image %}
## WeChat / 微信

<img class="wechat" src="{{ site.data.profile.wechat_image | relative_url }}" alt="{{ site.data.profile.name | escape }} 的微信二维码 / WeChat QR code" width="280" loading="lazy">

Feel free to scan the QR code to connect with me. 欢迎扫描二维码与我联系。
{% endif %}
