---
layout: default
title: Home
description: Panta Rhei is a seven-volume research book series spanning mathematics, holomorphy, spectrum, quantum structure, cosmology, life, and metaphysics.
theme: metaphysics
---

{% assign sorted_books = site.books | sort: 'order' %}

<section class="hero">
  <div class="hero__orb" aria-hidden="true"></div>
  <div class="container hero__grid">
    <div class="reveal">
      <div class="eyebrow">{{ site.data.site.series.eyebrow }}</div>
      <h1 class="hero__title">{{ site.data.site.series.hero_title }}</h1>
      <p class="hero__copy">{{ site.data.site.series.hero_copy }}</p>
      <div class="hero__actions">
        <a class="button button--primary" href="{{ '/books/' | relative_url }}">Explore the books</a>
        <a class="button button--secondary" href="{{ '/series/panta-rhei/' | relative_url }}">Read the series overview</a>
      </div>
    </div>

    <aside class="hero-card reveal">
      <div class="eyebrow">Series thesis</div>
      <h2 class="hero-card__tagline">{{ site.data.site.brand.tagline }}</h2>
      <p class="lead">Seven volumes develop a single categorical vocabulary and follow it from the foundations of mathematics through analysis, physics, biology, and into the hardest questions of mind, value, and meaning.</p>
      <div class="spectrum-bar"></div>
    </aside>
  </div>
</section>

<section class="section" id="series">
  <div class="content">
    <div class="section__intro reveal">
      <div>
        <div class="eyebrow">A coherent progression</div>
        <h2>From foundations to metaphysics</h2>
      </div>
      <p>Each volume inherits the vocabulary of the one before it and extends it into a new domain, so that the whole series reads as a single sustained argument.</p>
    </div>

    <div class="section-grid section-grid--2">
      <article class="paper-block reveal">
        <h3>One scaffold, seven domains</h3>
        <p>The series begins with a small axiomatic foundation, builds an analysis and spectral theory on top of it, then uses that scaffold to engage quantum structure, cosmology, living systems, and finally philosophy. The ambition is structural unity across traditionally separate fields.</p>
      </article>

      <article class="card reveal">
        <h3>Start exploring</h3>
        <div class="chip-row">
          <a class="chip chip--solid" href="{{ '/series/panta-rhei/' | relative_url }}">Series</a>
          <a class="chip" href="{{ '/books/' | relative_url }}">Books</a>
          <a class="chip" href="{{ '/resources/' | relative_url }}">Resources</a>
          <a class="chip" href="{{ '/press-kit/' | relative_url }}">Press Kit</a>
          <a class="chip" href="{{ '/updates/' | relative_url }}">Updates</a>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="content">
    <div class="section__intro reveal">
      <div>
        <div class="eyebrow">Seven volumes</div>
        <h2>The series at a glance</h2>
      </div>
      <p>From foundational category theory through quantum physics and cosmology to life and metaphysics.</p>
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
        <div class="eyebrow">Reader pathways</div>
        <h2>How to enter the series</h2>
      </div>
      <p>There is no single right way to begin. Choose the path that matches your background and curiosity.</p>
    </div>

    <div class="path-grid reveal">
      <article class="card">
        <h3>Foundational path</h3>
        <p>Begin with Book I and move through the series in conceptual order for the clearest cumulative progression.</p>
      </article>
      <article class="card">
        <h3>Thematic path</h3>
        <p>Jump into the volume closest to your current interest, then use the cross-links to connect outward into related parts of the arc.</p>
      </article>
      <article class="card">
        <h3>Expansive path</h3>
        <p>Enter through the larger horizon books — cosmology, life, or metaphysics — and then descend back into the foundations.</p>
      </article>
    </div>
  </div>
</section>

<section class="section" id="practical">
  <div class="content">
    <div class="section__intro reveal">
      <div>
        <div class="eyebrow">Supporting materials</div>
        <h2>Resources, press, and updates</h2>
      </div>
      <p>Every volume is backed by DOI registration, downloadable reader materials, and a curated press kit.</p>
    </div>

    <div class="section-grid section-grid--3 reveal">
      <article class="card">
        <h3><a href="{{ '/resources/' | relative_url }}">Reader resources</a></h3>
        <p>Tables of contents, Q&amp;A appendices, and edition-linked download bundles for every volume.</p>
      </article>
      <article class="card">
        <h3><a href="{{ '/press-kit/' | relative_url }}">Press kit</a></h3>
        <p>Author bios, cover assets, citation sheets, and review-ready materials in one place.</p>
      </article>
      <article class="card">
        <h3><a href="{{ '/updates/' | relative_url }}">Latest updates</a></h3>
        <p>Release notes, launch announcements, and project milestones.</p>
      </article>
    </div>
  </div>
</section>
