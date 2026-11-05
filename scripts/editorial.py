"""Landing page chapters and small, self-contained browser demonstrations."""

CHAPTERS = (
    ('01', 'Explore'),
    ('02', 'Make it yours'),
    ('03', 'Studio'),
    ('04', 'Field guide'),
)


def chapter_header(index, title, accent, links):
    number, name = CHAPTERS[index]
    shortcuts = ''.join(f'<a href="#{anchor}">{label}</a>' for anchor, label in links)
    return f'''<div class="chapter-heading wrap" data-chapter-reveal>
      <div><span class="chapter-eyebrow">{number} / {name.upper()}</span>
      <h2 id="chapter-{number}-title">{title} <em>{accent}</em></h2></div>
      <nav aria-label="{name} sections">{shortcuts}</nav>
    </div>'''


def creator_studio(g):
    icon = g['icon']
    lyrics = (
        'The sky goes quiet.',
        'Leave a light on for the night.',
        'We have a world of our own.',
        'Keep this moment a little longer.',
    )
    first_line = '<li class="is-current" aria-current="true">' + lyrics[0] + '</li>'
    lines = first_line + ''.join(f'<li>{line}</li>' for line in lyrics[1:])
    return f'''<section class="section studio-section" id="studio"><div class="wrap">
      <div class="studio-layout" data-lyric-studio>
        <div class="studio-scene" data-studio-layout="stack" data-studio-font="inter">
          <img src="/assets/img/screenshots/night-800.webp" width="800" height="421" loading="lazy" alt="">
          <div class="studio-scene-top"><span>LYRIC PLACEMENT</span><span>WEB DEMO</span></div>
          <ol class="studio-lines" aria-label="Original sample lyrics">{lines}</ol>
          <div class="studio-track"><span class="studio-track-icon">{icon('music')}</span><div><b>World of our own</b><small>Original sample · lyric timeline</small></div></div>
        </div>
        <div class="studio-control">
          <span class="section-label">LYRIC STUDIO <span class="new-badge">NEW</span></span>
          <h3>Give the words a place.</h3>
          <p>Scrub through the sample, then try a compact line or a full stack over the world.</p>
          <label class="studio-control-row" for="studio-seek">Timeline <output data-studio-time>00:00 / 00:24</output></label>
          <input id="studio-seek" type="range" min="0" max="24" value="0" aria-valuetext="0 of 24 seconds">
          <label class="studio-control-row">Placement <select data-studio-layout-select><option value="stack">Stacked</option><option value="compact">Compact</option></select></label>
          <label class="studio-control-row">Typeface <select data-studio-font-select><option value="inter">Inter</option><option value="serif">Editorial Serif</option><option value="mono">Mono</option></select></label>
          <label class="studio-control-row">Accent <input type="color" data-studio-accent value="#c9dcda"></label>
          <a class="detail-link" href="/docs/lyrics">Set up lyrics in Minecraft {icon('arrow')}</a>
        </div>
      </div>
      <div class="studio-tools">
        <a href="#product" data-open-preview="t-music"><span>{icon('music')}</span><div><b>Now playing</b><small>See the music card and lyrics in the client preview.</small></div>{icon('arrow')}</a>
        <a href="#product" data-open-preview="t-captures"><span>{icon('camera')}</span><div><b>Instant Replay</b><small>Try the recordings gallery and its 30-second clip flow.</small></div>{icon('arrow')}</a>
        <a href="/docs/captures"><span>{icon('play')}</span><div><b>Capture guide</b><small>Set up desktop audio, recordings and screenshots.</small></div>{icon('arrow')}</a>
      </div>
    </div></section>'''


def performance_room(g):
    icon = g['icon']
    return f'''<section class="section performance-room" id="performance-room"><div class="wrap">
      <div class="room-layout" data-frame-room>
        <div class="room-copy"><span class="section-label">PERFORMANCE ROOM <span class="new-badge">NEW</span></span>
          <h3>See the frame behind the FPS.</h3>
          <p>A few slow frames can stand out in an otherwise steady session. Compare two sample traces, then use Performance Monitor to measure the same scene in Minecraft.</p>
          <div class="room-choices" role="group" aria-label="Frame time sample">
            <button type="button" data-frame-sample="steady" aria-pressed="true">Steady scene</button>
            <button type="button" data-frame-sample="busy" aria-pressed="false">Busy scene</button>
          </div>
          <a class="detail-link" href="/docs/performance">Read the performance guide {icon('arrow')}</a>
        </div>
        <figure class="room-monitor">
          <figcaption><span>{icon('performance')} Frame times</span><small>ILLUSTRATIVE DATA</small></figcaption>
          <div class="room-metrics" aria-live="polite">
            <div><small>Median</small><b data-frame-median>8.0 ms</b></div>
            <div><small>95th percentile</small><b data-frame-p95>9.0 ms</b></div>
            <div><small>Slowest frame</small><b data-frame-max>10.0 ms</b></div>
          </div>
          <svg class="room-chart" viewBox="0 0 440 166" role="img" aria-labelledby="frame-chart-title frame-chart-description">
            <title id="frame-chart-title">Frame time by frame</title>
            <desc id="frame-chart-description" data-frame-description>A steady sample with frame times from 7 to 10 milliseconds.</desc>
            <path class="room-grid" d="M34 14H424 M34 57H424 M34 100H424 M34 143H424"/>
            <g class="room-axis"><text x="0" y="18">30</text><text x="0" y="61">20</text><text x="0" y="104">10</text><text x="0" y="147">0</text><text x="34" y="163">Frame 1</text><text x="381" y="163">Frame 24</text></g>
            <path class="room-area" data-frame-area d="M34 143L34 108L424 108L424 143Z"/>
            <polyline class="room-line" data-frame-line points="34,108 424,108"/>
          </svg>
          <p class="room-note" data-frame-note>Steady frames stay close together in this sample.</p>
        </figure>
      </div>
    </div></section>'''
