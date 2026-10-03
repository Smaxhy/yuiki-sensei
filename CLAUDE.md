# Yuki Sensei — project brief

## What this is
A personal Japanese tutor web app for an iPhone 15. One self-contained file, `index.html`
(HTML + CSS + vanilla JS, no build step, no frameworks). Hosted free on GitHub Pages from
the `main` branch root of the `yuki-sensei` repo, and installed on the home screen via
Safari → Add to Home Screen.

## Features (all in index.html)
- **Onboarding**: name, level (N5–N2), and learning goal on first launch.
- **Tabs**: Home, Yuki (chat), Learn, Practice, Me.
- **Yuki the AI tutor**: 26, from Kyoto, warm and playful, corrects mistakes clearly.
  Calls the Anthropic Messages API directly from the browser (`apiRequest()`) using the
  owner's API key, which is saved only in localStorage (never in the repo).
  Default model: `claude-haiku-4-5-20251001`. Optional "Smart" model: `claude-sonnet-5-5`.
- **Memory**: every AI reply ends with a hidden line `<<MEM>>{json}` containing facts,
  weak, strong, learned, right, wrong, lessonDone. The app strips it (`parseMem`), saves it
  to the profile (`applyMem`), and feeds the profile back into `systemPrompt()`.
  Don't break this format.
- **Lessons**: 100+ lessons in the `CUR` object, grouped by level (n5–n1) → unit →
  [id, title, description]. Tapping one starts a step-by-step lesson in chat, and
  "✓ Done" marks it complete.
- **Voice call mode**: full-screen orb, Web Speech API speech recognition (ja-JP or en-US)
  and speechSynthesis that splits Japanese and English into separate voices.
  Has Repeat and Slower buttons. If the mic is blocked, it shows iPhone fix-it steps.
- **Listening**: Japanese wrapped in [[double brackets]] in AI replies shows as a hidden,
  tap-to-play audio clip.
- **Flashcards**: decks for hiragana, katakana, 80 core words, and 50 kanji, using
  Leitner spaced repetition stored in `S.cards`. Works offline with no AI.
- **Kana charts**: tap any character to hear it; ones missed get a red border.
- **Quizzes**: mixed, weak spots, vocab, grammar, kanji, listening, translation, and
  roleplay, all run by Yuki in chat one question at a time.
- **Me tab**: profile, API key and model picker with a "Test Yuki" button, voice
  settings, what Yuki remembers, and backup/restore as JSON (key excluded).

## Technical notes
- State object `S` saved to localStorage key `yuki-sensei-v3`. Keep it backward
  compatible. Saved data (and restored backups) go through `migrate()`; if the shape
  changes, bump `DEFAULT.v` and add a step there instead of wiping progress.
- Clicks route through `data-act` attributes to the `ACT` object.
- Must stay iPhone-friendly: 16px inputs (stops zoom), safe-area padding,
  visualViewport resize handling, and tap targets of at least 44px.
- No secrets in the code, ever. The repo is public.

## How changes should be made
- Keep it one `index.html` file unless there's a strong reason to split it.
- Test that the JS has no syntax errors before committing, e.g.
  `sed -n '/<script>/,/<\/script>/p' index.html | sed '1d;$d' > /tmp/app.js && node --check /tmp/app.js`
- Commit with a clear message and push to `main` so GitHub Pages updates
  (or to the session's assigned branch, then merge to `main`).
- Explain changes to the owner in plain language. They're learning, not a developer.

## Ideas for next versions
- Kanji stroke-order practice
- More vocab and kanji decks for N4 and up
- Daily study reminders or goals
- Streak rewards
