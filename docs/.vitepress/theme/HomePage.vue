<script setup>
</script>

<template>
  <div class="home-page">
    <!-- Hero: two-column like Vitest -->
    <section class="wrapper wrapper--ticks hero-grid">
      <div class="hero-text">
        <div class="hero-text-inner">
          <h1>
            <span class="hero-brand">Slidev MCP</span><br />
            AI-Powered Presentations
          </h1>
          <p class="hero-tagline">
            Connect your AI assistant, describe your slides, get a shareable link. Built on <a href="https://sli.dev" target="_blank">Slidev</a> and the <a href="https://modelcontextprotocol.io" target="_blank">Model Context Protocol</a>.
          </p>
          <div class="hero-actions">
            <a href="/guide/getting-started" class="button button--primary">Get Started</a>
            <a href="https://github.com/joelbarmettlerUZH/slidev-mcp" target="_blank" class="button">View on GitHub</a>
          </div>
        </div>
      </div>
      <div class="hero-visual">
        <div class="hero-visual-inner">
          <video
            autoplay
            loop
            muted
            playsinline
            poster="/demo-readme.webp"
            class="hero-video"
          >
            <source src="/demo-fast.mp4" type="video/mp4" />
          </video>
        </div>
      </div>
    </section>

    <!-- Intro: "Why" section like Vitest -->
    <section class="wrapper wrapper--ticks intro-section">
      <div class="intro-inner">
        <div class="intro-left">
          <div class="intro-badge">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            <span>How it works</span>
          </div>
          <h3>Three Steps to a Presentation</h3>
          <a href="/guide/getting-started" class="button intro-button-desktop">Learn more</a>
        </div>
        <div class="intro-right">
          <div class="intro-steps">
            <div class="intro-step">
              <span class="step-num">1</span>
              <div>
                <strong>Connect</strong> &mdash; Add one line to your MCP client. No API keys, no sign-up.
                <div class="step-code"><code>claude mcp add slidev-mcp https://slidev-mcp.org/mcp</code></div>
              </div>
            </div>
            <div class="intro-step">
              <span class="step-num">2</span>
              <div>
                <strong>Describe</strong> &mdash; Tell your AI what you need. It reads the theme gallery, picks a style, and writes Slidev markdown.
              </div>
            </div>
            <div class="intro-step">
              <span class="step-num">3</span>
              <div>
                <strong>Share</strong> &mdash; Get a URL that works in any browser. Keep iterating &mdash; the link stays the same.
              </div>
            </div>
          </div>
          <a href="/guide/getting-started" class="button intro-button-mobile">Learn more</a>
        </div>
      </div>
    </section>

    <!-- Heading section like Vitest "Fast. Lightweight. Integrated." -->
    <section class="wrapper heading-section">
      <h2>Everything you need. Nothing to install.</h2>
    </section>

    <!-- Feature grid: 2x2 like Vitest -->
    <section class="wrapper wrapper--ticks feature-grid">
      <div class="feature-cell">
        <div class="feature-content">
          <h5>Works Everywhere</h5>
          <p>Claude Code, Claude Desktop, claude.ai, Cursor, Windsurf, VS Code, JetBrains, Zed, ChatGPT &mdash; if it speaks MCP, it works.</p>
        </div>
        <div class="client-tags">
          <span class="tag">Claude Code</span>
          <span class="tag">Claude Desktop</span>
          <span class="tag">Cursor</span>
          <span class="tag">Windsurf</span>
          <span class="tag">VS Code</span>
          <span class="tag">JetBrains</span>
          <span class="tag">Zed</span>
          <span class="tag">ChatGPT</span>
        </div>
      </div>
      <div class="feature-cell">
        <div class="feature-content">
          <h5>24 Curated Themes</h5>
          <p>From minimalist to cinematic. Describe a style and let the AI pick, or <a href="/reference/themes">browse the gallery</a> yourself. Every theme is tested and production-ready.</p>
        </div>
      </div>
      <div class="feature-cell">
        <div class="feature-content">
          <h5>Iterative Updates</h5>
          <p>Keep refining in the same conversation. The URL stays the same, the content updates instantly. Version history is preserved.</p>
        </div>
      </div>
      <div class="feature-cell">
        <div class="feature-content">
          <h5>Secure by Design</h5>
          <p>Builds run in isolated containers with no inbound network. Your markdown goes in, static HTML comes out. No data leaves the server.</p>
        </div>
      </div>
    </section>

    <!-- "See all features" link -->
    <section class="wrapper features-link-section">
      <a href="/reference/tools" class="button">See all tools &amp; resources</a>
    </section>

    <!-- CTA Footer like Vitest -->
    <footer class="cta-footer" data-theme="dark">
      <section class="wrapper">
        <div class="cta-bg">
          <div class="cta-inner">
            <h2>Start creating presentations</h2>
            <p>Connect your AI assistant and build your first deck in under a minute</p>
            <a href="/guide/getting-started" class="button button--white">Get started</a>
          </div>
        </div>
      </section>
      <nav class="footer-nav">
        <div class="footer-nav-inner">
          <div class="footer-col">
            <h6>Slidev MCP</h6>
            <ul>
              <li><a href="/guide/what-is-slidev-mcp">What is Slidev MCP?</a></li>
              <li><a href="/guide/getting-started">Getting Started</a></li>
              <li><a href="/reference/tools">Tools</a></li>
              <li><a href="/reference/resources">Resources</a></li>
            </ul>
          </div>
          <div class="footer-col">
            <h6>Clients</h6>
            <ul>
              <li><a href="/clients/claude-code">Claude Code</a></li>
              <li><a href="/clients/claude-desktop">Claude Desktop</a></li>
              <li><a href="/clients/cursor">Cursor</a></li>
              <li><a href="/clients/windsurf">Windsurf</a></li>
              <li><a href="/clients/">All clients</a></li>
            </ul>
          </div>
          <div class="footer-col">
            <h6>Reference</h6>
            <ul>
              <li><a href="/reference/themes">Themes</a></li>
              <li><a href="/reference/limitations">Limitations</a></li>
              <li><a href="/guide/deployment">Self-hosting</a></li>
              <li><a href="/contributing">Contributing</a></li>
            </ul>
          </div>
          <div class="footer-col">
            <h6>Social</h6>
            <ul>
              <li>
                <a href="https://github.com/joelbarmettlerUZH/slidev-mcp" target="_blank">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" class="footer-icon"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                  GitHub
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <span>Built with <a href="https://sli.dev" target="_blank">Slidev</a> and the <a href="https://modelcontextprotocol.io" target="_blank">Model Context Protocol</a>.</span>
        </div>
      </nav>
    </footer>
  </div>
</template>

<style scoped>
/* ═══════════════════════════════════
   Base: mirrors Vitest's wrapper system
   ═══════════════════════════════════ */
.home-page {
  --brand: #c78704;
  --brand-light: #daa520;
  --brand-dim: #a87000;
  --brand-glow: rgba(199, 135, 4, 0.35);
  --nickel: rgba(255, 255, 255, 0.08);
  --grey: #b0a89b;
  --bg: #262624;
  --bg-soft: #30302e;
  font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.wrapper {
  max-width: 1280px;
  margin: 0 auto;
  border-left: 1px solid var(--nickel);
  border-right: 1px solid var(--nickel);
}

/* Tick marks on wrapper edges like Vitest */
.wrapper--ticks {
  position: relative;
}
.wrapper--ticks::before,
.wrapper--ticks::after {
  content: '';
  position: absolute;
  top: -4px;
  width: 1px;
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  z-index: 1;
}
.wrapper--ticks::before { left: -1px; }
.wrapper--ticks::after { right: -1px; }

/* ═══════════════════════════════════
   Buttons: match Vitest's button system
   ═══════════════════════════════════ */
.button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  border: 1px solid var(--nickel);
  color: var(--vp-c-text-1);
  background: transparent;
  transition: all 0.25s;
  cursor: pointer;
}
.button:hover {
  border-color: rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.04);
}

.button--primary {
  background: var(--brand);
  border-color: transparent;
  color: #fff;
}
.button--primary:hover {
  background: var(--brand-light);
  box-shadow: 0 4px 20px var(--brand-glow);
}

.button--white {
  background: #fff;
  border-color: transparent;
  color: #1a1a2e;
  font-weight: 600;
}
.button--white:hover {
  background: #f0f0f0;
}

/* ═══════════════════════════════════
   Hero: two-column grid like Vitest
   ═══════════════════════════════════ */
.hero-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-top: 1px solid var(--nickel);
}

.hero-text {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px;
  border-right: 1px solid var(--nickel);
}

.hero-text-inner {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 480px;
  text-align: left;
}

.hero-text h1 {
  font-family: "APK Protocol", sans-serif;
  font-size: 44px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.03em;
  color: var(--vp-c-text-1);
}

.hero-brand {
  background: linear-gradient(135deg, var(--brand), var(--brand-light));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-tagline {
  font-size: 17px;
  line-height: 1.6;
  color: var(--grey);
  max-width: 400px;
}
.hero-tagline a {
  color: var(--brand-light);
  text-decoration: none;
  border-bottom: 1px solid rgba(199, 135, 4, 0.3);
}
.hero-tagline a:hover {
  border-color: var(--brand-light);
}

.hero-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.hero-visual {
  display: flex;
  flex-direction: column;
  min-height: 360px;
  position: relative;
  overflow: hidden;
  background: radial-gradient(ellipse at 70% 50%, rgba(199, 135, 4, 0.08), transparent 70%);
}

.hero-visual-inner {
  position: relative;
  padding: 24px 24px 24px 40px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-video {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
  display: block;
}

/* ═══════════════════════════════════
   Intro: "Why" section like Vitest
   ═══════════════════════════════════ */
.intro-section {
  border-top: 1px solid var(--nickel);
  padding: 56px 20px;
}

@media (min-width: 1024px) {
  .intro-section {
    padding: 80px 48px;
  }
}

.intro-inner {
  display: flex;
  flex-direction: column;
  gap: 32px;
  text-align: left;
}

@media (min-width: 1024px) {
  .intro-inner {
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-start;
    gap: 48px;
  }
}

.intro-left {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 400px;
}

.intro-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  font-family: ui-monospace, monospace;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--grey);
}
.intro-badge svg {
  color: var(--brand-light);
}

.intro-left h3 {
  font-family: "APK Protocol", sans-serif;
  font-size: 32px;
  font-weight: 700;
  line-height: 1.15;
  color: var(--vp-c-text-1);
  text-wrap: balance;
}

@media (min-width: 1024px) {
  .intro-left h3 {
    font-size: 36px;
  }
}

.intro-button-desktop {
  display: none;
  margin-top: 32px;
  width: fit-content;
}
.intro-button-mobile {
  display: block;
  margin-top: 24px;
  width: fit-content;
}

@media (min-width: 1024px) {
  .intro-button-desktop { display: block; }
  .intro-button-mobile { display: none; }
}

.intro-right {
  max-width: 560px;
}

.intro-steps {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.intro-step {
  display: flex;
  gap: 16px;
  font-size: 15px;
  line-height: 1.6;
  color: var(--grey);
}
.intro-step strong {
  color: var(--vp-c-text-1);
}

.step-num {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: var(--brand);
  color: #fff;
  font-weight: 700;
  font-size: 13px;
  margin-top: 2px;
}

.step-code {
  margin-top: 8px;
  padding: 8px 12px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--nickel);
  overflow-x: auto;
}
.step-code code {
  font-size: 12px;
  color: var(--brand-light);
  font-family: ui-monospace, 'JetBrains Mono', 'Fira Code', monospace;
  white-space: nowrap;
}

/* ═══════════════════════════════════
   Heading section
   ═══════════════════════════════════ */
.heading-section {
  border-top: 1px solid var(--nickel);
  padding: 56px 20px;
  display: flex;
  justify-content: center;
  text-align: center;
}

@media (min-width: 640px) {
  .heading-section {
    padding: 80px 40px;
  }
}

.heading-section h2 {
  font-family: "APK Protocol", sans-serif;
  font-size: 36px;
  font-weight: 700;
  line-height: 1.15;
  color: var(--vp-c-text-1);
  text-wrap: balance;
  max-width: 640px;
}

@media (min-width: 640px) {
  .heading-section h2 {
    font-size: 44px;
  }
}

/* ═══════════════════════════════════
   Feature grid: 2x2 like Vitest
   ═══════════════════════════════════ */
.feature-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-top: 1px solid var(--nickel);
}

.feature-cell {
  padding: 24px;
  border-bottom: 1px solid var(--nickel);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Vertical dividers between columns */
.feature-cell:nth-child(odd) {
  border-right: 1px solid var(--nickel);
}

@media (min-width: 640px) {
  .feature-cell {
    padding: 40px;
  }
}

.feature-content h5 {
  font-family: "APK Protocol", sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--vp-c-text-1);
  margin-bottom: 8px;
}

.feature-content p {
  font-size: 15px;
  line-height: 1.6;
  color: var(--grey);
  max-width: 420px;
  text-wrap: pretty;
}
.feature-content a {
  color: var(--brand-light);
  text-decoration: none;
  border-bottom: 1px solid rgba(199, 135, 4, 0.3);
}
.feature-content a:hover {
  border-color: var(--brand-light);
}

.client-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  color: var(--grey);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--nickel);
}

/* ═══════════════════════════════════
   Features link
   ═══════════════════════════════════ */
.features-link-section {
  border-top: 1px solid var(--nickel);
  padding: 32px 0;
  display: flex;
  justify-content: center;
}

/* ═══════════════════════════════════
   CTA Footer like Vitest
   ═══════════════════════════════════ */
.cta-footer {
  margin-top: 48px;
}

.cta-footer .wrapper {
  border: none;
}

.cta-bg {
  position: relative;
  overflow: hidden;
  background: linear-gradient(160deg, #c78704 0%, #a87000 30%, #8a5c00 60%, #c78704 100%);
}
.cta-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 50% -20%, rgba(255, 220, 100, 0.5), transparent 50%),
    radial-gradient(ellipse at 20% 80%, rgba(140, 90, 0, 0.6), transparent 50%),
    radial-gradient(ellipse at 80% 30%, rgba(255, 200, 50, 0.3), transparent 40%);
  pointer-events: none;
}

.cta-inner {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 48px 24px;
  text-align: center;
}

@media (min-width: 768px) {
  .cta-inner {
    padding: 96px 24px;
  }
}

.cta-inner h2 {
  font-family: "APK Protocol", sans-serif;
  font-size: 36px;
  font-weight: 700;
  color: #fff;
  text-wrap: balance;
  text-shadow: 0 2px 8px rgba(0,0,0,0.15);
  border: none;
  margin: 0;
  padding: 0;
}

@media (min-width: 640px) {
  .cta-inner h2 {
    font-size: 44px;
  }
}

.cta-inner p {
  font-size: 17px;
  color: rgba(255, 255, 255, 0.85);
  max-width: 420px;
  text-wrap: balance;
  text-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

.cta-inner .button--white {
  margin-top: 12px;
}

/* ═══════════════════════════════════
   Footer navigation like Vitest
   ═══════════════════════════════════ */
.footer-nav {
  border-top: 1px solid var(--nickel);
  padding: 48px 24px 32px;
  max-width: 1280px;
  margin: 0 auto;
}

.footer-nav-inner {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 32px;
  margin-bottom: 32px;
}

@media (min-width: 768px) {
  .footer-nav-inner {
    grid-template-columns: repeat(4, 1fr);
    gap: 40px;
  }
}

.footer-col h6 {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--vp-c-text-1);
  margin-bottom: 14px;
  font-family: ui-monospace, monospace;
}

.footer-col ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.footer-col a {
  font-size: 14px;
  color: var(--grey);
  text-decoration: none;
  transition: color 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.footer-col a:hover {
  color: var(--vp-c-text-1);
}

.footer-icon {
  vertical-align: -2px;
}

.footer-bottom {
  border-top: 1px solid var(--nickel);
  padding-top: 20px;
  text-align: center;
  font-size: 13px;
  color: var(--grey);
}
.footer-bottom a {
  color: var(--grey);
  text-decoration: none;
}
.footer-bottom a:hover {
  color: var(--vp-c-text-1);
}

/* ═══════════════════════════════════
   Responsive
   ═══════════════════════════════════ */
@media (max-width: 768px) {
  .hero-grid {
    grid-template-columns: 1fr;
  }
  .hero-text {
    border-right: none;
    border-bottom: 1px solid var(--nickel);
    padding: 32px 24px;
    align-items: flex-start;
  }
  .hero-text h1 {
    font-size: 36px;
  }
  .hero-visual-inner {
    padding: 24px;
  }
  .feature-grid {
    grid-template-columns: 1fr;
  }
  .feature-cell:nth-child(odd) {
    border-right: none;
  }
}
</style>
