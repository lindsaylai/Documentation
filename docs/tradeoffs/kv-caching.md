# KV caching

During generation, a transformer stores **key** and **value** tensors for
tokens it has already processed so it does not recompute them on every new
token. **KV caching** reuses that state. In serving systems, the same idea
extends across requests: shared prompt prefixes can keep a warm cache so later
calls skip redundant prefill work.

For tutors, the useful form of caching is usually **prefix reuse**—system
instructions, shared tutoring rules, and common course context—not storing a
finished answer for each exact student question.

## The pieces, as blocks

Each prompt token owns a paired **key** and **value**. Visually, treat every
token as one column: the top half is the key, the bottom half is the value.
Caching keeps those columns for tokens that already appeared, so later
generation only fills columns for new tokens.

<div class="piece-map" markdown>

<p class="piece-map__title">One prompt, token by token</p>
<p class="piece-map__lede">
Shared tutor preamble stays warm. Retrieved course text and the student
question still arrive as ordinary tokens; only the shared prefix is reused.
</p>

<ul class="piece-map__strip">
<li class="piece-map__token piece-map__token--cached">
<p class="piece-map__token-label">Sys</p>
<div class="piece-map__kv">
<p class="piece-map__half piece-map__half--key">K</p>
<p class="piece-map__half piece-map__half--value">V</p>
</div>
</li>
<li class="piece-map__token piece-map__token--cached">
<p class="piece-map__token-label">Rules</p>
<div class="piece-map__kv">
<p class="piece-map__half piece-map__half--key">K</p>
<p class="piece-map__half piece-map__half--value">V</p>
</div>
</li>
<li class="piece-map__token piece-map__token--cached">
<p class="piece-map__token-label">Style</p>
<div class="piece-map__kv">
<p class="piece-map__half piece-map__half--key">K</p>
<p class="piece-map__half piece-map__half--value">V</p>
</div>
</li>
<li class="piece-map__token">
<p class="piece-map__token-label">Ctx</p>
<div class="piece-map__kv">
<p class="piece-map__half piece-map__half--key">K</p>
<p class="piece-map__half piece-map__half--value">V</p>
</div>
</li>
<li class="piece-map__token piece-map__token--fresh">
<p class="piece-map__token-label">Ask</p>
<div class="piece-map__kv">
<p class="piece-map__half piece-map__half--key">K</p>
<p class="piece-map__half piece-map__half--value">V</p>
</div>
</li>
</ul>

<ul class="piece-map__caption">
<li><span class="piece-map__swatch piece-map__swatch--key" aria-hidden="true"></span> Key half</li>
<li><span class="piece-map__swatch piece-map__swatch--value" aria-hidden="true"></span> Value half</li>
<li><span class="piece-map__swatch piece-map__swatch--cached" aria-hidden="true"></span> Cached prefix</li>
<li><span class="piece-map__swatch piece-map__swatch--fresh" aria-hidden="true"></span> New tokens</li>
</ul>

<dl class="piece-map__defs">
<div>
<dt>Key</dt>
<dd>
The address side of the token: how later attention finds this position when
deciding what to look at.
</dd>
</div>
<div>
<dt>Value</dt>
<dd>
The content side of the token: what information is carried forward once
attention selects that position.
</dd>
</div>
</dl>

</div>

## Why it comes up

Student questions vary, but large parts of the prompt often do not: the
tutoring system prompt, safety rules, and sometimes a stable block of course
or syllabus context. If those prefixes repeat, KV reuse can cut latency and
cost. Whether that matters depends on how similar real student traffic is, and
on whether the serving stack exposes prefix or automatic prefix caching.

## Advantages

- Speeds up turns that share a long common prefix
- Reduces repeated prefill cost for system prompts and shared context
- Helps multi-turn chats where earlier tokens can be reused within a session
- Complements RAG when the retrieved block changes but the tutor preamble does
  not

## Limitations

- Helps little if every request has a unique, long, unshared prefix
- Caching **specific answers** to specific-sounding questions is brittle:
  wording changes, course updates, and near-duplicates all miss
- Correctness still depends on retrieval and the model; a fast wrong answer is
  still wrong
- Behavior differs by provider and engine; not every API offers the same reuse
- Measuring benefit requires realistic question mixes, not synthetic repeats

## Prefer general context over memorized answers

For this project, caching is more promising when it targets **stable, shared
information**—tutor instructions, course-wide framing, or frequently retrieved
general passages—than when it tries to memorize replies to narrow questions.

Memorizing specific Q&A pairs:

- Breaks when students rephrase
- Risks serving stale or over-specific guidance
- Fights the goal of grounded, retrieval-based tutoring

Reusing KV state for shared prefixes:

- Stays compatible with RAG (retrieval can still vary per question)
- Scales with traffic that shares the same tutor configuration
- Is a serving optimization, not a substitute for a better corpus

## When it is likely to help

KV caching is worth pursuing after looking at what students actually ask:

- If many turns share the same system prompt and similar context length,
  prefix caching is a good candidate
- If questions are highly unique and retrieval dominates the prompt, gains may
  be modest
- Run small A/B or load tests with representative queries before committing
  infrastructure to cache tuning

## Project stance

Treat KV caching as a **performance optimization** on top of the tutoring
pipeline, not as a knowledge store. Prefer caching or reusing general shared
prompt and database-backed context over answer memorization. Use traffic and
benchmark measurements to decide whether the latency and cost gains justify
provider- or vLLM-specific cache configuration.
