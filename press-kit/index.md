---
layout: default
title: Press Kit
description: Press materials, author bios, cover assets, and citation access for the Panta Rhei series.
theme: metaphysics
---

<section class="page-hero">
  <div class="content">
    <div class="page-hero__panel hero-card reveal">
      <div>
        <div class="eyebrow">Press kit</div>
        <h1 class="page-hero__title">Press &amp; review materials</h1>
        <p class="page-hero__copy">Cover assets, author biographies, citation references, and review-ready materials — everything needed for coverage of the series.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="content">
    <div class="related-grid reveal mb-20">
      <article class="resource-item">
        <h4>Website</h4>
        <p><a href="{{ site.data.site.links.website }}">{{ site.data.site.links.website }}</a></p>
      </article>
      <article class="resource-item">
        <h4>Amazon series</h4>
        <p><a href="{{ site.data.site.links.amazon_series }}">Print + Kindle series page</a></p>
      </article>
      <article class="resource-item">
        <h4>Downloads release</h4>
        <p><a href="{{ site.data.site.links.downloads_release }}">Reader materials release</a></p>
      </article>
    </div>

    <div class="section__intro reveal">
      <div>
        <div class="eyebrow">Official assets</div>
        <h2>Press downloads</h2>
      </div>
      <p>All links below point to the official press release assets for the 1st edition.</p>
    </div>

    <div class="section-grid section-grid--2 reveal">
      {% for item in site.data.press_assets.series %}
        <article class="resource-item">
          <h4>{{ item[1].label }}</h4>
          <p><a href="{{ item[1].url }}">Open asset</a></p>
        </article>
      {% endfor %}
    </div>
  </div>
</section>

<section class="section">
  <div class="content">
    <article class="paper-block reveal">
      <h3>About the series</h3>
      <p><em>Panta Rhei</em> is a seven-volume research program developing categorical foundations across mathematics, physics, life, and metaphysics. The series builds a unified structural vocabulary—starting from axioms and holomorphy, moving through spectral organization and micro/macro dynamics, and culminating in questions of emergence, mind, and lived reality.</p>
      <p>The work is presented as an open program: rigorous, testable, and intended for critical engagement.</p>
    </article>
  </div>
</section>
