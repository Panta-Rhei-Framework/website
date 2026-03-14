---
layout: default
title: Citation
description: DOI and citation references for the Panta Rhei series.
theme: foundations
---

{% assign sorted_books = site.books | sort: 'order' %}

<section class="page-hero">
  <div class="content">
    <div class="page-hero__panel hero-card reveal">
      <div>
        <div class="eyebrow">Citation</div>
        <h1 class="page-hero__title">DOI &amp; citation guide</h1>
        <p class="page-hero__copy">Each volume in the series is citable via DOI. This page centralizes the reference layer and gives readers, reviewers, and cataloguers one stable scholarly surface.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="content">
    <div class="section-grid section-grid--2 reveal">
      {% for book in sorted_books %}
        {% assign resource = site.data.resources.books[book.slug] %}
        <article class="paper-block">
          <h3>{{ book.volume_label }} — {{ book.title }}</h3>
          <p><strong>DOI:</strong> <a href="{{ resource.doi }}">{{ resource.doi }}</a></p>
          <p><strong>Suggested citation:</strong> Fuchs, Thorsten; Fuchs, Anna-Sophie. <em>{{ book.title }}</em>. 1st ed., 2025. Zenodo.</p>
        </article>
      {% endfor %}
    </div>
  </div>
</section>
