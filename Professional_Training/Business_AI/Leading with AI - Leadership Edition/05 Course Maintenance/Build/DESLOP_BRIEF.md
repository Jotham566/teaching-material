# De-slop brief (12 November 2026): remove machine-sounding wording and templated design

The lecturer's request (verbatim): "Review and remove ai-like slop woridings and designs".

Both editions were drafted with AI help and it shows. A scan of the 400 Leadership and 414 Executive slides found:
- about 60% of titles in the "X: Y" pattern, and the same titles in every deck ("From Session N to today: ...", "Take-away: five things to remember", "... in six industries, with one named example in each", "Questions to ask your team and your vendor before ...");
- 50+ notes opening "Here is"/"Here are", stock closers ("Now, what you ...", "Tell me your ...", "Three stories follow."), a quarter of notes ending on a question;
- filler and tells: "simply/just/really/actually/clearly/exactly", "Think of/Imagine/Picture", "the catch", "in plain words", "That is why/the point", "Notice", "key";
- design templates repeated without thought: the same four-box case card (problem, what the AI does, result, catch) 35 times in the Leadership Edition; a five-card numbered take-away with an icon on each card at the end of every deck; icons on every table row; gold boxes on everything; a lead line that repeats the title and points that repeat the figure.

## What good looks like
Write the way an experienced lecturer who knows the room talks and writes a handout: specific, plain, varied, with no performance. Every sentence carries information; nothing announces itself.

### Wording
1. **Titles** state the point of the slide as a plain sentence, specific to its content. At most about a third may use a colon, and only where it genuinely helps. No title may begin "From Session N to today", "Take-away:", "Everyday first"; none may contain "five things to remember" or "one named example"; tour, questions, people and close slides get titles about their own content (for example "Banks, telcos and farms already score customers this way" rather than "Prediction at work in six industries, with one named example in each").
2. **Notes** sound like a person speaking, varied in rhythm. At most two notes per deck open with "Here is", "Let me", "Let us" or "Now let". Do not end every note with a question: at most 30%, and only real questions you will wait for. Cut stock signposts ("Three stories follow", "Now we turn to", "With that in mind"), filler adverbs, and mottos that repeat what was just said ("Fluent is not true." after explaining it). Use "Think of/Imagine/Picture" at most twice per deck. Avoid tidy triads in every sentence ("X, Y and Z"); use the number of items the content has. No "the catch" as a label: say what went wrong. Do not narrate the teaching ("in plain words", "the point is", "the key is").
3. **Slide text**: the lead line adds something the title does not; points do not repeat the figure's words; captions give the source or one useful fact, not a slogan. Fewer, better words.
4. **Keep** every fact, number, source line, name, the learning order, the explain-before-use standard, the no-maths rule (Leadership) and every lint rule. Do not shorten notes below 45 words or lose the explanations; rewrite them better.

### Design
1. **Case slides**: the four-box card may appear at most once per deck. Give each other case the layout its story needs: a headline number with one line of context and the source; a short timeline; a before and after; a quote-free two-column "what happened / what it means for you"; or a small chart of its real figures. Red only for a real failure or warning; gold only for the one thing to look at.
2. **Closing take-away**: replace the five numbered icon cards with something specific to the session: the session's own key figure or picture with three or four plain lines, or a short list. No icon per item.
3. **Icons** only where they help someone find or recognise something. Remove decorative icons from tables, word lists and option boxes where they add nothing (the `icons`/`word_icons` fields can be dropped or reduced).
4. **One highlight per figure.** Remove gold fills that mark nothing in particular, extra borders and rounded boxes around single lines of text.
5. Text in figures at least 14 pt, no overlaps or clipping; look at every changed slide image.

## Workflow
Edit only your sessions' `content/sNN.py` and figure modules (Leadership: `kit/diagrams_lNN.py`; Executive: `kit/diagrams_tNN.py`). Shared figures used by other sessions keep their names and signatures; make a local variant if you need a different look. Lint (`python kit/lint_content.py N`) now enforces the style rules above and must reach 0 problems. Render (`$S/render_lead.sh N` for Leadership, `$S/render_one.sh N` for Executive), look at every changed slide, fix, repeat. Read the notes aloud in order: they must still bridge and still teach.

Report (under 200 words per session group): what you rewrote and redesigned, any fact you touched (should be none), lint result.
