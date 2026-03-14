---
layout: default
title: Books
description: Browse all seven volumes of the Panta Rhei series — from mathematical foundations through physics, life, and metaphysics.
theme: spectrum
---

{% assign sorted_books = site.books | sort: 'order' %}

<section class="page-hero">
  <div class="content">
    <div class="page-hero__panel hero-card reveal">
      <div class="page-hero__grid">
        <div>
          <div class="eyebrow">Books index</div>
          <h1 class="page-hero__title">Explore the seven-volume arc</h1>
          <p class="page-hero__copy">Seven volumes, three reading paths, and a shared structural vocabulary that connects mathematics to lived reality.</p>
          <div class="hero__actions">
            <a class="button button--primary" href="{{ '/books/categorical-foundations/' | relative_url }}">Open Book I</a>
            <a class="button button--secondary" href="#paths">View reading paths</a>
          </div>
        </div>

        <div class="stat-grid">
          <div class="stat"><strong>Volumes</strong><span>{{ sorted_books | size }} published books</span></div>
          <div class="stat"><strong>Reader paths</strong><span>Foundational · bridge · expansive</span></div>
          <div class="stat"><strong>Formats</strong><span>Print · Kindle · DOI resources</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="content">
    <div class="section__intro reveal">
      <div>
        <div class="eyebrow">Filter</div>
        <h2>Browse by pathway</h2>
      </div>
      <p>Select a reading path to highlight the volumes most relevant to your entry point.</p>
    </div>

    <div class="chip-row reveal mb-20">
      <button class="filter-chip is-active" data-filter="all" aria-pressed="true">All books</button>
      <button class="filter-chip" data-filter="foundational" aria-pressed="false">Foundational</button>
      <button class="filter-chip" data-filter="bridge" aria-pressed="false">Bridge / method</button>
      <button class="filter-chip" data-filter="expansive" aria-pressed="false">Expansive</button>
    </div>

    <div class="book-grid reveal">
      {% for book in sorted_books %}
        {% include book-card.html book=book %}
      {% endfor %}
    </div>
  </div>
</section>

<section class="section" id="paths">
  <div class="content">
    <div class="section__intro reveal">
      <div>
        <div class="eyebrow">Reader guidance</div>
        <h2>Three reading paths</h2>
      </div>
      <p>Choose the entry that matches your background. Each path leads into the full series from a different angle.</p>
    </div>

    <div class="path-grid reveal">
      <article class="card">
        <h3>Foundational</h3>
        <p>Move through Books I and II first to build the conceptual and methodological basis before branching outward.</p>
      </article>
      <article class="card">
        <h3>Bridge / method</h3>
        <p>Enter through the middle of the series to understand the structural bridge between abstract method and physical application.</p>
      </article>
      <article class="card">
        <h3>Expansive</h3>
        <p>Begin with the cosmological, biological, or metaphysical volumes and later descend into their foundations.</p>
      </article>
    </div>
  </div>
</section>
