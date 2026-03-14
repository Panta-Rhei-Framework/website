---
layout: default
title: Updates
description: Public updates for the Panta Rhei site and series.
theme: spectrum
---

<section class="page-hero">
  <div class="content">
    <div class="page-hero__panel hero-card reveal">
      <div>
        <div class="eyebrow">Updates</div>
        <h1 class="page-hero__title">Public notes &amp; release updates</h1>
        <p class="page-hero__copy">Release notes, launch announcements, and milestones for the series and the website.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="content">
    <div class="post-grid reveal">
      {% for post in site.posts %}
        <article class="card">
          <div class="eyebrow">{{ post.date | date: "%B %-d, %Y" }}</div>
          <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
          <p>{{ post.excerpt | strip_html | truncate: 180 }}</p>
        </article>
      {% endfor %}
    </div>
  </div>
</section>
