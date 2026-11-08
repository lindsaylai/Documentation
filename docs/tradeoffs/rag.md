# RAG

Retrieval-augmented generation (RAG) answers a question by first searching a
knowledge base, then asking the language model to respond using the retrieved
passages. In this project, the knowledge base is the course corpus; retrieval
selects relevant chunks; the configured model generates the tutoring reply.

The Data 8 tutor already follows this pattern. See
[GPT Corpus](../model-options/data8/corpus-options.md) for how the local BM25
index and optional embeddings work today.

## The pieces, as blocks

RAG is a handoff across four blocks: the student question, the searchable
corpus, the retrieved passages that enter the prompt, and the model that writes
the reply. Nothing here is a key/value cache; these are content blocks the
pipeline moves.

<div class="piece-map" markdown>

<p class="piece-map__title">Retrieve, then generate</p>
<p class="piece-map__lede">
The corpus stays outside the model. Only the selected passages join the prompt
for that turn.
</p>

<ul class="piece-flow">
<li class="piece-flow__node piece-flow__node--origin">
<p class="piece-flow__role">Input</p>
<p class="piece-flow__name">Student question</p>
<p class="piece-flow__note">Wording students actually use</p>
</li>
<li class="piece-flow__node">
<p class="piece-flow__role">Store</p>
<p class="piece-flow__name">Course corpus</p>
<p class="piece-flow__note">Lectures, worksheets, text</p>
</li>
<li class="piece-flow__node piece-flow__node--accent">
<p class="piece-flow__role">Select</p>
<p class="piece-flow__name">Retrieved chunks</p>
<p class="piece-flow__note">BM25 or embeddings hit list</p>
</li>
<li class="piece-flow__node">
<p class="piece-flow__role">Generate</p>
<p class="piece-flow__name">Tutor reply</p>
<p class="piece-flow__note">Grounded in those passages</p>
</li>
</ul>

</div>

## Why it comes up

A tutor that only uses pretrained model knowledge can invent course details,
mix terms from other curricula, or miss the wording students see in lecture.
RAG ties answers to identifiable course files. The open question for this
project is whether the available corpus is large and varied enough for
retrieval to pay off consistently, or whether many questions will still miss
useful passages.

## Advantages

- Grounds responses in course material instead of model memory alone
- Makes sources inspectable when retrieval results are logged or shown
- Lets the corpus and the model change independently
- Avoids fine-tuning the model every time course content is updated
- Works with a free local BM25 index by default in the current setup

## Limitations

- A small or sparse corpus returns weak context; the model then fills gaps
- Retrieval can miss the right passage when student wording differs from the
  source text
- Extra latency and (with embeddings) extra API cost on each question
- Poor chunking or incomplete conversion of source files hurts quality more
  than the choice of model
- Does not by itself prevent answer leakage if solution text is retrievable

## When it is likely to help

RAG is most useful when the corpus covers the topics students actually ask
about, and when those topics appear in searchable form (lectures, worksheets,
textbook excerpts). If the corpus is thin, retrieval often returns near-misses
or empty results, and the pipeline behaves like a prompt-only tutor with extra
overhead.

Practical checks before expanding RAG investment:

- Sample real or representative student questions and measure hit rate
- Prefer improving corpus coverage and chunk quality over adding complexity
- Keep solution material out of student-mode retrieval

## Project stance

RAG remains the default tutoring pattern for Data 8 because it matches the
goal of course-grounded help. Its value still depends on corpus depth. If
benchmarks show frequent retrieval misses, the next improvements should focus
on indexing and content coverage before assuming a different architecture is
required.
