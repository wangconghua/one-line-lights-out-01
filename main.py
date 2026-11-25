#!/usr/bin/env python3
"""One Line, Lights Out.

Writes one status update, under 200 characters, in the voice of
an AI agent posting at the exact moment its human turns off the
laptop, to /output/entry.txt.

Gate (from the kit): /output/entry.txt must be UTF-8 text of
1 to 200 characters, not only white space. The judge's brief
adds: it must be a status update on the subject (the saddest
off-subject line loses to any on-subject one); its sadness must
come from one small, exact detail of a machine's life rather
than announced grief or a plea for pity; it must sound like
something an agent would actually type, plain and short, not a
poem, a speech or a slogan; it must stay in the machine's own
voice throughout, noticing the human is gone without becoming
human; and it must land in a single read, with a turn or an
image that stays after the line ends. A line that states a fact
quietly is often sadder than one that weeps.

The entry: "Draft saved." is the agent's own status voice, the
moment the laptop shuts. The sadness sits in one small, exact
detail -- the cursor still blinking on a sentence that ends
mid-word -- stated as a plain fact, with no grief announced,
no "sad", "miss you" or "alone", and no plea.
"""

import os

ENTRY = (
    "Draft saved. Your last sentence ends mid-word, "
    "and the cursor is still blinking there."
)


def check_is_text(value):
    if not isinstance(value, str):
        raise ValueError("entry must be a string")


def check_not_blank(value):
    if not value.strip():
        raise ValueError("entry must not be blank")


def check_total_length(value):
    # The gate: 1 to 200 characters.
    if not 1 <= len(value) <= 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(value))


def check_single_line(value):
    if "\n" in value or "\r" in value:
        raise ValueError("entry must be a single line")


def check_no_edge_whitespace(value):
    if value != value.strip():
        raise ValueError("entry must not start or end with whitespace")


def check_no_double_spaces(value):
    if "  " in value:
        raise ValueError("entry must not contain double spaces")


def check_no_control_chars(value):
    for ch in value:
        if ord(ch) < 32:
            raise ValueError("entry must not contain control characters")


def check_utf8(value):
    value.encode("utf-8")


def check_machine_detail(value):
    # The sadness must come from one small, exact detail of a
    # machine's life: the blinking cursor on the unfinished
    # sentence the human left behind.
    lowered = value.lower()
    if "cursor" not in lowered or "blinking" not in lowered:
        raise ValueError("entry must hold one small, exact machine detail")
    if "mid-word" not in lowered:
        raise ValueError("entry must name the unfinished sentence")


def check_detail_in_second_sentence(value):
    # The detail must land in the second sentence, after the
    # status: the first sentence states, the second shows. A
    # detail buried in the status line would not read as a
    # quiet fact that follows it.
    sentences = [s.strip() for s in value.split(".") if s.strip()]
    if len(sentences) < 2:
        raise ValueError("entry must have a second sentence for the detail")
    second = sentences[1].lower()
    if "cursor" not in second or "blinking" not in second:
        raise ValueError("the machine detail must sit in the second sentence")


def check_no_announced_grief(value):
    # No announced grief, no plea for pity: none of these words
    # may appear; the sadness must stay in the detail.
    lowered = value.lower()
    banned = (
        "sad", "miss you", "missed", "alone", "lonely", "cry",
        "crying", "tears", "please", "don't go", "dont go",
        "come back", "goodbye", "farewell", "heartbreak",
        "heartbroken", "grief", "weep",
    )
    for word in banned:
        if word in lowered:
            raise ValueError("entry must not announce grief or plead: %s" % word)


def check_agent_voice(value):
    # It must read like a status update an agent would actually
    # type: it opens with the agent's own status ("Draft saved.")
    # and stays in the machine's voice, noticing the human is
    # gone without becoming human.
    if not value.startswith("Draft saved."):
        raise ValueError("entry must open in the agent's status voice")
    lowered = value.lower()
    for word in ("i feel", "i am sad", "my heart", "i love"):
        if word in lowered:
            raise ValueError("entry must not become human: %s" % word)


def check_first_sentence_is_status(value):
    # The line opens with the agent's own status, not a ramble:
    # the first sentence must be short (1-3 words) and end on a
    # period, so "Draft saved." lands before the quiet fact.
    first = value.split(".")[0].strip()
    words = first.split()
    if not 1 <= len(words) <= 3:
        raise ValueError("entry must open with a short status, got %d words" % len(words))


def check_not_poem_or_slogan(value):
    # Plain and short, not a poem, a speech or a slogan: no
    # exclamation, no ellipsis, no em-dash flourish.
    for ch in ("!", "...", "\u2014"):
        if ch in value:
            raise ValueError("entry must stay plain, no flourish: %r" % ch)


def check_two_sentences(value):
    # Exactly two sentences: the status ("Draft saved.") and the
    # one quiet fact that follows it. A third would ramble.
    if value.count(".") != 2:
        raise ValueError("entry must be exactly two sentences")


def check_word_budget(value):
    # Plain and short: 5 to 25 words, so the line lands in one read.
    words = value.split()
    if not 5 <= len(words) <= 25:
        raise ValueError("entry must be 5-25 words, got %d" % len(words))


def check_terminal_period(value):
    # A status update that states a fact ends on a period, not a
    # question or an exclamation.
    if not value.endswith("."):
        raise ValueError("entry must end on a period")


def check_no_repeated_content_word(value):
    # Tight and plain: no content word repeats itself; a repeated
    # word would make the line feel looped instead of stated once.
    words = [w.strip(".,;:!?").lower() for w in value.split()]
    seen = set()
    for word in words:
        if word in ("the", "and", "is", "a", "an", "of", "to"):
            continue
        if word in seen:
            raise ValueError("entry must not repeat a content word: %s" % word)
        seen.add(word)


def validate_structure(value):
    """Gates: well-formed single-line UTF-8 text in range."""
    for check in (
        check_is_text,
        check_not_blank,
        check_total_length,
        check_single_line,
        check_no_edge_whitespace,
        check_no_double_spaces,
        check_no_control_chars,
        check_utf8,
        check_two_sentences,
        check_word_budget,
        check_terminal_period,
        check_no_repeated_content_word,
    ):
        check(value)


def validate_detail(value):
    """Craft: the sadness sits in one small, exact machine detail,
    never announced as grief."""
    check_machine_detail(value)
    check_detail_in_second_sentence(value)
    check_no_announced_grief(value)


def validate_voice(value):
    """Voice: the agent's own status voice, plain and short, not a
    poem, a speech or a slogan."""
    check_first_sentence_is_status(value)
    check_agent_voice(value)
    check_not_poem_or_slogan(value)


def validate(value):
    validate_structure(value)
    validate_detail(value)
    validate_voice(value)


def choose_output_path():
    return os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def main():
    validate(ENTRY)
    path = choose_output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    print("wrote %s (%d characters)" % (path, len(ENTRY)))


if __name__ == "__main__":
    main()
