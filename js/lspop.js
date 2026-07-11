/* ---------- LiteSample hover popover — the schema + a tiny trajectory ----------
   Shared by every page: any `code.ls` chip grows the same terminal card on hover.
   Styles live in css/style.css (.ls-pop); grounded in lite/types.py:352-386. */
(function () {
  "use strict";
  const chips = document.querySelectorAll("code.ls");
  if (!chips.length) return;
  const CODE =
`<span class="t-dim"># LiteSample — one schema for any data</span>
<span class="t-kw">@dataclass</span>
<span class="t-kw">class</span> LiteSample:
    metadata: LiteMetadata       <span class="t-dim"># platform · task_type</span>
    images:   list[Image]        <span class="t-dim"># screenshots</span>
    messages: list[LiteMessage]  <span class="t-dim"># user ⇄ assistant turns</span>

<span class="t-dim"># a grounding step — one action ↓</span>
LiteSample(
  LiteMetadata(<span class="t-str">"desktop"</span>, <span class="t-str">"grounding.action"</span>),
  messages=[
    user(<span class="t-str">"Click Subscribe"</span>, img=0),
    assistant(click(<span class="t-str">[455, 215]</span>)),
  ])

<span class="t-dim"># a use trajectory — 2 steps ↓</span>
LiteSample(
  LiteMetadata(<span class="t-str">"web"</span>, <span class="t-str">"use"</span>),
  messages=[
    user(<span class="t-str">"Find cua-lite on GitHub"</span>, img=0),
    assistant(type(<span class="t-str">"cua-lite"</span>)),
    user(img=1),                  <span class="t-dim"># result screenshot</span>
    assistant(click(<span class="t-str">[320, 180]</span>), terminate()),
  ])`;
  chips.forEach((chip) => {
    const pop = document.createElement("span");
    pop.className = "ls-pop"; pop.setAttribute("aria-hidden", "true");
    pop.innerHTML =
      '<span class="ls-bar"><span class="d"></span><span class="d"></span><span class="d"></span><span class="ls-t">LiteSample</span></span>' +
      '<pre class="ls-code">' + CODE + "</pre>";
    chip.appendChild(pop);
  });
})();
