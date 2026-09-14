# -*- coding: utf-8 -*-
"""Render the twelve Data Analysis session decks.

Content lives in da_deck_w1.py through da_deck_w4.py; the session spine
(titles, outcomes, the trap) comes from da_content.py; every number comes
from da_keys.py, which reads the generated answer key.

Placeholders are written <<name>> rather than {name} on purpose: the slides
carry Python dicts, DAX measures and f-strings, all of which contain braces,
and str.format would either choke on them or silently eat them.
"""
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

from pptxkit import (deck, tb, chip, card, theight, notes, notes_context,
                     s_figure, add_fig,
                     s_title, s_question, s_head, s_points, s_split,
                     s_livecode, s_challenge, s_closing, s_divider, s_break,
                     s_prose, s_define, s_worked, s_check, s_answers,
                     s_summary, W, H, M, INK, INK2, PAPER, ORANGE, MUTED,
                     TEAL, STEEL, STEEL2, C, _blank, _bg,
                     _shrink, LECTURER)
from pptx.enum.text import PP_ALIGN
import da_content as DC
import da_keys as DK
import da_deck_w1 as W1
import da_deck_w2 as W2
import da_deck_w3 as W3
import da_deck_w4 as W4
import da_deck_w5 as W5

OUT = os.path.join(_ROOT, "DataAnalysis_Track", "decks")
FIGS = os.path.join(_ROOT, "DataAnalysis_Track", "figs")

DECKS = {}
FMT = dict(DK.FMT_BASE)
for mod in (W1, W2, W3, W4, W5):
    DECKS.update(mod.DECKS)
    FMT.update(mod.FMT)

PLACEHOLDER = re.compile(r"<<(\w+)>>")


def fmt(obj):
    """Fill <<placeholders>> anywhere in a nested structure of strings.

    A missing name raises here rather than projecting "<<orders>>" onto a
    screen in front of a room, which is the whole reason this is a function
    and not a str.format call at the point of use.
    """
    if isinstance(obj, str):
        def sub(m):
            k = m.group(1)
            if k not in FMT:
                raise KeyError("no value for placeholder <<%s>>" % k)
            return FMT[k]
        return PLACEHOLDER.sub(sub, obj)
    if isinstance(obj, tuple):
        return tuple(fmt(x) for x in obj)
    if isinstance(obj, list):
        return [fmt(x) for x in obj]
    if isinstance(obj, dict):
        return {k: fmt(v) for k, v in obj.items()}
    return obj


def note(slide, text, label=None):
    """notes(), plus a usable label for the lecturer guide.

    pptxkit.notes() infers a title by taking the first short line of text on
    the slide, which on a definition slide is the kicker. So two consecutive
    concept slides both appear in the guide as "DEFINITION", which is no use
    to somebody trying to find their place. Pass the label explicitly.
    """
    notes(slide, text)
    if label and LECTURER and "TO TEACH" in text:
        LECTURER[-1]["title"] = label
    return slide


# ------------------------------------------------------- track-specific slides
def s_da_objectives(prs, objs, session, title, tool):
    """Like pptxkit's s_objectives, but the footer says something true for
    this audience: these are people in work, and the relevant promise is
    about the next three hours rather than about prior experience."""
    s = _blank(prs)
    tb(s, M, 0.62, W - 2 * M, 0.32, "WHAT YOU WILL BE ABLE TO DO", size=12,
       bold=True, colour=ORANGE)
    tb(s, M, 1.04, W - 2 * M, 0.8, "By the end of tonight you can…",
       size=30, bold=True, colour=INK)
    y = 2.10
    n = len(objs)
    rh = min(0.90, (H - y - 0.95) / n)
    for i, o in enumerate(objs):
        h = theight(o, W - 2 * M - 0.75, 14, 1.18)
        chip(s, M, y + 0.04, str(i + 1), fill=INK, dia=0.36, size=11)
        tb(s, M + 0.60, y, W - 2 * M - 0.75, h + 0.06, o, size=14,
           colour=C(0x2A, 0x3B, 0x4A), line=1.18)
        y += max(rh, h + 0.18)
    tb(s, M, H - 0.78, W - 2 * M, 0.4,
       "Session {} of 15  ·  {}  ·  {}".format(session, tool, title),
       size=11, italic=True, colour=MUTED)
    return s


def s_da_map(prs, current):
    """Where tonight sits in the twelve. Four rows of three, one per week."""
    s = _blank(prs)
    y = s_head(s, "Where tonight sits", "THE FIFTEEN SESSIONS")
    # Fifteen cards. Five rows of three does not fit the slide height, so
    # four columns of four it is, with the last slot empty.
    cols = 4
    cw = (W - 2 * M - 0.30 * (cols - 1)) / cols
    ch = 1.16
    for i, ss in enumerate(DC.SESSIONS):
        r, c = divmod(i, cols)
        x = M + c * (cw + 0.30)
        top = y + 0.04 + r * (ch + 0.18)
        now = ss["n"] == current
        card(s, x, top, cw, ch, fill=ORANGE if now else STEEL, shadow=False)
        tb(s, x + 0.16, top + 0.08, cw - 0.32, 0.28,
           "{}  ·  {}".format(ss["n"], ss["tool"].upper()),
           size=9.5, bold=True,
           colour=PAPER if now else C(0x6B, 0x7A, 0x8A))
        tb(s, x + 0.16, top + 0.38, cw - 0.32, ch - 0.46, ss["title"],
           size=11, bold=now,
           colour=PAPER if now else C(0x2A, 0x3B, 0x4A), line=1.12)
    return s


def s_da_trap(prs, trap, session):
    """The mistake the session exists to prevent, on its own dark slide.

    It gets a slide of its own because it is the one thing from each session
    that is worth remembering in six months, and because a warning buried in
    a bullet list is not a warning.
    """
    s = _blank(prs)
    _bg(s, prs, INK2)
    tb(s, M, 1.05, W - 2 * M, 0.34, "THE MISTAKE THIS SESSION PREVENTS",
       size=13, bold=True, colour=ORANGE)
    h = theight(trap, W - 2 * M, 26, 1.14)
    tb(s, M, 1.75, W - 2 * M, h + 0.1, trap, size=26, bold=True,
       colour=PAPER, line=1.14)
    tb(s, M, 1.95 + h, W - 2 * M, 0.5,
       "It is in tonight's lab on purpose.", size=15,
       colour=C(0xB8, 0xC9, 0xD8))
    tb(s, M, H - 0.85, W - 2 * M, 0.4,
       "Session {} of 15".format(session), size=11,
       colour=C(0x7E, 0x93, 0xA6))
    return s


def s_da_homework(prs, home, session):
    s = _blank(prs)
    y = s_head(s, "Before the next session", "HOMEWORK · 45 TO 60 MINUTES")
    hh = theight(home, W - 2 * M - 0.64, 16, 1.22)
    card(s, M, y, W - 2 * M, hh + 0.5, fill=STEEL)
    tb(s, M + 0.32, y + 0.24, W - 2 * M - 0.64, hh + 0.06, home, size=16,
       colour=INK, line=1.22)
    ty = y + hh + 0.8
    chip(s, M, ty, "WHY IT IS ALWAYS OPTIONAL ON YOUR OWN DATA", fill=TEAL,
         w=4.9, size=11)
    tb(s, M, ty + 0.62, W - 2 * M, 1.2,
       "Homework on a dataset you already care about gets done. Homework on "
       "a teaching dataset competes with your job and loses. Either version "
       "counts, and the one on your own data is worth more to you.",
       size=15, colour=C(0x33, 0x46, 0x57), line=1.22)
    return s



def s_da_vocab(prs, vocab, session):
    """The words tonight will use, with the spreadsheet equivalent.

    This slide exists because the room is confident in Excel and has never
    been given the vocabulary of data. Beginners lose sessions to undefined
    words far more often than to difficult ideas, so the words come first,
    before the technique, every session. Three columns: the term, what it
    means in plain language, and what it is called in the tool they already
    use.
    """
    s = _blank(prs)
    y = s_head(s, "The words for tonight", "BEFORE WE START")
    n = len(vocab)
    tw, dw = 2.45, 5.35
    ew = W - 2 * M - tw - dw - 0.5

    # header strip, so the third column is not a mystery
    tb(s, M, y, tw, 0.3, "TERM", size=10, bold=True, colour=ORANGE)
    tb(s, M + tw + 0.25, y, dw, 0.3, "WHAT IT MEANS", size=10, bold=True,
       colour=ORANGE)
    tb(s, M + tw + dw + 0.5, y, ew, 0.3, "IN A SPREADSHEET", size=10,
       bold=True, colour=ORANGE)
    top = y + 0.40

    avail = (H - 0.45) - top

    def need(fs):
        total = 0.0
        for term, definition, excel in vocab:
            total += max(theight(term, tw, fs + 0.5, 1.14),
                         theight(definition, dw, fs, 1.16),
                         theight(excel or "—", ew, fs, 1.16)) + 0.14
        return total

    fs = _shrink(12.5, need, avail, "vocab")
    for i, (term, definition, excel) in enumerate(vocab):
        h = max(theight(term, tw, fs + 0.5, 1.14),
                theight(definition, dw, fs, 1.16),
                theight(excel or "—", ew, fs, 1.16))
        if i % 2 == 0:
            card(s, M - 0.12, top - 0.04, W - 2 * M + 0.24, h + 0.1,
                 fill=STEEL2, radius=False, shadow=False)
        tb(s, M, top, tw, h + 0.05, term, size=fs + 0.5, bold=True,
           colour=INK, line=1.14)
        tb(s, M + tw + 0.25, top, dw, h + 0.05, definition, size=fs,
           colour=C(0x33, 0x46, 0x57), line=1.16)
        tb(s, M + tw + dw + 0.5, top, ew, h + 0.05, excel or "no direct "
           "equivalent", size=fs, italic=not excel,
           colour=TEAL if excel else MUTED, line=1.16)
        top += h + 0.14
    return s


def s_da_figure(prs, path, title, caption, kicker="LOOK AT THIS"):
    """A figure, as big as the slide allows, with its caption under it.

    pptxkit's s_figure reserves a fixed band for the caption, which wastes
    height on a one-line caption and clips a three-line one. This measures
    the caption first and gives the image everything left over, because
    these figures ARE the teaching for a beginner rather than decoration.
    """
    s = _blank(prs)
    y = s_head(s, title, kicker)
    ch = theight(caption, W - 2 * M, 13, 1.2)
    avail_h = (H - 0.42) - y - ch - 0.22
    from PIL import Image
    with Image.open(path) as im:
        iw, ih = im.size
    aspect = ih / float(iw)
    w = min(W - 2 * M, avail_h / aspect)
    h = w * aspect
    add_fig(s, path, M + (W - 2 * M - w) / 2.0, y, w, h)
    tb(s, M, y + h + 0.16, W - 2 * M, ch + 0.06, caption, size=13,
       colour=C(0x33, 0x46, 0x57), line=1.2)
    return s


# ------------------------------------------------------------------ the render
def build_session(ss):
    """One deck for one session, in the order it is taught."""
    c = fmt(DECKS[ss["n"]])
    prs = deck()
    name = "S{:02d} {}".format(ss["n"], ss["title"])
    notes_context(name)

    s = s_title(prs, "SESSION {} OF 15".format(ss["n"]), ss["title"],
                c["question"][2],
                "WEEK {}  ·  {}  ·  3 HOURS".format(
                    ss["week"], ss["tool"].upper()),
                "Data Analysis with Python, SQL and Power BI  ·  "
                "roadmap.sh: " + ss["roadmap"])
    notes(s, "Start on time. "
             "TO TEACH: name the one thing they will be able to do at 21:00 "
             "that they cannot do at 18:00, and keep it to one sentence.")

    s = s_da_map(prs, ss["n"])
    notes(s, "Tonight is session {} of twelve.".format(ss["n"]))

    # The words come before the technique, every session. This is the one
    # change that matters most for a room starting from scratch.
    if ss.get("vocab"):
        s = s_da_vocab(prs, ss["vocab"], ss["n"])
        note(s, "TO TEACH: read these out, slowly, and ask whether anybody "
                "already uses a different word for any of them. They often "
                "do, and reconciling the two takes thirty seconds now and "
                "saves an argument later.",
             label="The words for tonight")

    s = s_da_objectives(prs, ss["outcomes"], ss["n"], ss["title"], ss["tool"])
    notes(s, "These three are what tonight is marked against, in the sense "
             "that the lab checks them. "
             "TO TEACH: read them out. It takes twenty seconds and it stops "
             "the room wondering where a session is going.")

    k, q, under = c["question"]
    s = s_question(prs, k, q, under)
    notes(s, under + " TO TEACH: leave this on screen while you talk. Do not "
                     "answer it yet.")

    # ---------------------------------------------------------- block one
    s = s_divider(prs, "BLOCK ONE · 50 MINUTES", c.get(
        "b1_title", "The first half"), ss["b1"][:220])

    for title, items, kicker in c.get("points", []):
        s = s_points(prs, title, items, kicker=kicker)
        note(s, "TO TEACH: work down these one at a time and ask the room "
                "for a fifth example. There always is one.", label=title)

    for term, definition, example, confuse in c.get("concepts", []):
        s = s_define(prs, term, definition, example, confuse)
        note(s, definition + " TO TEACH: say the definition once, then the "
                              "example, then ask somebody to give it back in "
                              "their own words.", label="Define: " + term)

    for fig, ftitle, fcap in c.get("b1_figs", []):
        s = s_da_figure(prs, os.path.join(FIGS, fig + ".png"), ftitle, fcap)
        note(s, fcap + " TO TEACH: put this up and say nothing for ten "
                       "seconds. Let them read it, then ask what they "
                       "notice before you tell them.",
             label="Figure: " + ftitle)

    code = c.get("code", [])
    first = code[:1] if len(code) > 1 else code
    rest = code[1:] if len(code) > 1 else []
    for title, where, block, mistake in first:
        s = s_livecode(prs, title, where, block, mistake)
        note(s, "TO TEACH: type it, do not paste it. Then break it exactly "
                "as the bottom of the slide says and let them see the "
                "result before you fix it.",
             label="Live code: " + title)

    s = s_break(prs, 10)
    notes(s, "Ten minutes. TO TEACH: take it properly. This is an evening "
             "class and the second half needs them awake.")

    # ---------------------------------------------------------- block two
    s = s_divider(prs, "BLOCK TWO · 45 MINUTES",
                  c.get("b2_title", "The second half"), ss["b2"][:220])

    for title, where, block, mistake in rest:
        s = s_livecode(prs, title, where, block, mistake)
        note(s, "TO TEACH: type it live. The mistake at the bottom is the "
                "part they will remember.",
             label="Live code: " + title)

    for fig, ftitle, fcap in c.get("b2_figs", []):
        s = s_da_figure(prs, os.path.join(FIGS, fig + ".png"), ftitle, fcap)
        note(s, fcap + " TO TEACH: ten seconds of silence, then ask the "
                       "room what it says before you say it.",
             label="Figure: " + ftitle)

    if c.get("worked"):
        title, intro, steps, answer = c["worked"]
        s = s_worked(prs, title, intro, steps, answer)
        note(s, intro + " TO TEACH: walk it slowly and do not skip the "
                        "check at the end.", label="Worked: " + title)

    for sp in c.get("splits", []):
        title, lh, lb, rh, rr, kicker = sp
        s = s_split(prs, title, lh, lb, rh, rr, kicker=kicker)
        note(s, "TO TEACH: this is what they hand in. Read the right-hand "
                "panel out loud.", label=title)

    for pr in c.get("prose", []):
        title, paras, kicker, cols = pr
        s = s_prose(prs, title, paras, kicker=kicker, cols=cols)
        note(s, "Reference. TO TEACH: do not read this slide out. Point at "
                "it, say it is in the pack, and move on.", label=title)

    if ss.get("note"):
        # Operational notes: the Windows-only problem in week 5, the group
        # size limit in session 15. These have to be on a slide, because
        # they change what the room can actually do tonight.
        sl = _blank(prs)
        y2 = s_head(sl, "Before you start tonight", "PRACTICAL NOTE")
        nh = theight(ss["note"], W - 2 * M - 0.64, 16, 1.22)
        card(sl, M, y2, W - 2 * M, nh + 0.5, fill=STEEL)
        tb(sl, M + 0.32, y2 + 0.24, W - 2 * M - 0.64, nh + 0.06,
           ss["note"], size=16, colour=INK, line=1.22)
        note(sl, ss["note"] + " TO TEACH: deal with this in the first five "
                              "minutes. It changes what half the room can "
                              "do tonight.",
             label="Practical note")

    s = s_da_trap(prs, ss["trap"], ss["n"])
    notes(s, ss["trap"] + " TO TEACH: say it, then say where in tonight's "
                          "lab they will meet it.")

    # ---------------------------------------------------------- close out
    if c.get("check"):
        qs, pairs = c["check"]
        s = s_check(prs, qs)
        notes(s, "TO TEACH: thirty seconds of silence, then take answers. "
                 "Do not let the fastest person answer all three.")
        s = s_answers(prs, pairs)
        notes(s, "TO TEACH: the second answer is usually the one worth "
                 "dwelling on.")

    title, brief, questions = c["lab"]
    s = s_challenge(prs, title, brief, questions, kicker="LAB · 50 MINUTES")
    notes(s, brief + " TO TEACH: circulate. Anything asked twice gets "
                     "answered to the whole room.")

    s = s_summary(prs, ss["outcomes"],
                  kicker="TONIGHT IN THREE LINES",
                  title="What you can do now")
    notes(s, "TO TEACH: read these back and ask for a show of hands on the "
             "one they are least sure about. That tells you what to open "
             "with next session.")

    s = s_da_homework(prs, ss["home"], ss["n"])
    notes(s, ss["home"])

    headline, body, footer = c["closing"]
    s = s_closing(prs, headline, body, footer)
    notes(s, body + " TO TEACH: end on this, not on the homework slide.")

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "DA_S{:02d}_{}.pptx".format(
        ss["n"], re.sub(r"[^A-Za-z0-9]+", "_", ss["title"]).strip("_")))
    prs.save(path)
    return path, len(prs.slides.__iter__.__self__._sldIdLst)


if __name__ == "__main__":
    total = 0
    written = []
    for ss in DC.SESSIONS:
        path, nslides = build_session(ss)
        total += nslides
        written.append(os.path.basename(path))
        print("  {:>2} slides  {}".format(nslides, os.path.basename(path)))

    # The deck filenames carry the session title, so renaming a session
    # leaves the old file behind. An instructor opening a stale deck in
    # front of a room is a real failure mode, so the current set is written
    # down and the verifier checks the directory against it.
    with open(os.path.join(OUT, "MANIFEST.txt"), "w",
              encoding="utf-8") as fh:
        fh.write("# The 15 current decks. Anything else in this folder is\n"
                 "# stale: delete it.\n")
        for name in written:
            fh.write(name + "\n")
    stale = sorted(set(f for f in os.listdir(OUT) if f.endswith(".pptx"))
                   - set(written))
    if stale:
        print("\n*** {} STALE DECK(S) from an earlier build. Delete them:"
              .format(len(stale)))
        print("      cd {} && rm {}".format(
            OUT, " ".join('"%s"' % f for f in stale)))
    print("\n{} decks, {} slides".format(len(DC.SESSIONS), total))
    print("{} lecturer notes collected".format(len(LECTURER)))
