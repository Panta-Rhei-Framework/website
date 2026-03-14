---
layout: default
title: Resources
description: Reader downloads and supplementary resources for the Panta Rhei series.
theme: spectrum
---

{% assign sorted_books = site.books | sort: 'order' %}

<section class="page-hero">
  <div class="content">
    <div class="page-hero__panel hero-card reveal">
      <div>
        <div class="eyebrow">Reader resources</div>
        <h1 class="page-hero__title">Downloads &amp; supplementary material</h1>
        <p class="page-hero__copy">This area brings together the practical reader-facing materials of the series: contents, appendices, bundles, and future supplementary documents.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="content">
    <div class="section__intro reveal">
      <div>
        <div class="eyebrow">Series bundles</div>
        <h2>Quick series downloads</h2>
      </div>
      <p>Use the release bundles to download all reader materials at once or browse by volume below.</p>
    </div>

    <div class="related-grid reveal">
      {% for item in site.data.resources.series %}
        <article class="resource-item">
          <h4>{{ item[1].label }}</h4>
          <p><a href="{{ item[1].url }}">Open download</a></p>
        </article>
      {% endfor %}
    </div>
  </div>
</section>

<section class="section">
  <div class="content">
    <div class="section__intro reveal">
      <div>
        <div class="eyebrow">By volume</div>
        <h2>Reader packs by book</h2>
      </div>
      <p>Each volume offers a table of contents PDF, a Q&amp;A appendix PDF, and a combined reader pack.</p>
    </div>

    <div class="section-grid section-grid--2 reveal">
      {% for book in sorted_books %}
        {% assign resource = site.data.resources.books[book.slug] %}
        <article class="card">
          <h3>{{ book.title }}</h3>
          <div class="chip-row">
            <a class="chip" href="{{ resource.toc_url }}">TOC</a>
            <a class="chip" href="{{ resource.qa_url }}">Q&amp;A</a>
            <a class="chip" href="{{ resource.bundle_url }}">Reader pack</a>
            <a class="chip" href="{{ resource.doi }}">DOI</a>
          </div>
        </article>
      {% endfor %}
    </div>
  </div>
</section>
