# Yuki Sensei — project brief

## What this is
A personal Japanese tutor web app for an iPhone 15. One self-contained file, `index.html`
(HTML + CSS + vanilla JS, no build step, no frameworks). Hosted free on GitHub Pages from
the `main` branch root of the `yuki-sensei` repo, and installed on the home screen via
Safari → Add to Home Screen.

## Features (all in index.html)
- **Onboarding**: name, level (N5–N2), goal, focus areas, where they are now (kana/kanji,
  location, first language, daily minutes), reply style, and free-text notes. Existing users
  get a Home card ("Help Yuki get to know you") and can edit answers in Me (`UI.obEdit`).
- **Level check**: 16 offline multiple-choice questions in `PLACE` (bands kana/n5/n4/n3/n2).
  No AI, no credits. Result saved to `S.placement` and can set `S.level`.
- **Learner card**: `learnerCard()` turns `S.about` + `S.placement` into one compact line
  sent with every request so Yuki always knows who the student is.
- **Guided plan**: 12 weeks / 84 days in `PLAN` (flattened to `PDAYS`), aimed at kana +
  basic conversation. Task codes: `L:` lesson, `C:` flashcard deck (`due` = review),
  `K:` kana chart, `Q:` quiz, `T:` talk prompt in `TALK`. Progress in `S.plan` (`start`,
  `done["day:task"]`). Tasks tick themselves (`planAuto`, lesson completion, 4 Yuki replies
  via `UI.planCtx`) or via ✓ Done in chat. Shown as the Path (see below).
- **Auto-update**: on open, on returning to the app, and every 15 min, `checkUpdate` fetches
  the live page and compares its `<script>`/`<style>` with the running ones. If different it
  reloads right away when idle (`canReloadNow`), otherwise when the app is next hidden. Loop
  guard: at most one auto-reload per 2 min (`yuki-upd-at`). Still bump `APP_VERSION` (shown in Me).
- **Path (home tab)**: Duolingo-style winding path of nodes. N5 uses the 12-week `PLAN`;
  other levels get one built from `CUR[level]` (lessons + a 🏆 unit review per unit). Built by
  `pathNodes()` / `pathUnits()`; node keys: `day:task` (N5), `L:id` (lessons), `lv:unit:q`,
  `c:id` (custom ⭐). Sticky unit header (`pathScroll`), unit sheet with "skip unit",
  level sheet. Custom lessons in `S.plan.custom` ({id,title,before,level}) are added from the
  "⭐ Add a lesson" sheet or by Yuki via the `path` MEM field.
- **Tabs**: Path, Yuki (chat), Practice, Me. "All lessons" (`UI.tab="learn"`) opens from the
  path, the level sheet, or Practice.
- **Yuki the AI tutor**: 26, from Kyoto, warm and playful, corrects mistakes clearly.
  Calls the Anthropic Messages API directly from the browser (`apiRequest()`) using the
  owner's API key, which is saved only in localStorage (never in the repo).
  Default model: `claude-haiku-4-5-20251001`. Optional "Smart" model: `claude-sonnet-5-5`
  (sent with `output_config.effort:"low"` and server-side fallbacks; Haiku 4.5 rejects effort).
  The system prompt is two blocks: a stable one (persona, learner card, style rules; marked
  `cache_control`) and `memoryPrompt()` (memory, stats, current lesson) which changes per turn.
- **Reply style** (`S.settings.style`): length, English vs Japanese, reading help, simple
  English. Turned into prompt lines by `styleRules()`.
- **Credit saver** (`S.settings.history`): 6/12/24 recent messages sent per request.
- **Memory**: every AI reply ends with a hidden line `<<MEM>>{json}` containing facts,
  weak, strong, learned, right, wrong, lessonDone, path. The app strips it (`parseMem`), saves it
  to the profile (`applyMem`), and feeds the profile back into `systemPrompt()`.
  Don't break this format.
- **Lessons**: 100+ lessons in the `CUR` object, grouped by level (n5–n1) → unit →
  [id, title, description]. Tapping one starts a step-by-step lesson in chat, and
  "✓ Done" marks it complete.
- **Voice call mode**: full-screen orb, Web Speech API speech recognition (ja-JP or en-US)
  and speechSynthesis that splits Japanese and English into separate voices. Voices are
  ranked by `voiceScore()` (Premium/Enhanced/Siri first, novelty voices excluded) and can be
  chosen in Me (`S.settings.voiceEn` / `voiceJa`).
  Optional "Natural voices" engine (`S.settings.tts="azure"`): Microsoft Azure neural TTS
  (same voices as Edge Read Aloud; Edge TTS itself can't be called from iPhone Safari) via
  REST with the owner's own key (`azKey`, `azRegion`, never in backups). One SSML request per
  reply switching between `azEn`/`azJa` voices (`AZ_VOICES`), played with Web Audio, cached
  (`natCache`), monthly characters counted (`ttsChars`, free tier 500k). Falls back to iPhone
  voices on any error. `isSpeaking()` / `stopSpeak()` cover both engines.
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
- State object `S` (currently `v:7`) saved to localStorage key `yuki-sensei-v3`. Keep it backward
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
