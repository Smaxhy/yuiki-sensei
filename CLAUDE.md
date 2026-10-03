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
- **Conversation course (N5 path)**: `COURSE` = 12 topic units (greetings, introductions,
  numbers, food, time, hobbies, family, shopping, directions, weather & feelings, travel, real
  conversations). Each unit: 3 lessons of max 5 words `[jp, romaji, en]`, a 5-kana bite
  (`kana`), and a roleplay (`rp`; "FINAL" = end-of-course conversation). Path order per unit:
  lesson, lesson, kana, lesson, roleplay. Node keys `cl:<id>`, `ck:<unit>`, `cr:<unit>`.
  Lesson player (`UI.lp`, `vLesson`): Learn (one word per card, recorded audio) → Practise
  (offline tap quiz incl. 2 review questions from older due words) → Talk. Talk = `S.course`
  ({key, kind, title, goal, scen, targets, used, review}); `coursePrompt()` tells Yuki to make
  the student use every target word and to bring back older words; words tick off via
  `detectUsed()` on what the student types (kana, romaji, or English voice-typing look-alikes like "Ohio" via `soundsLike()`; everyday English words in `EN_COMMON` never count) and the `used` MEM field; all used
  → node done. Course words are flashcards `w:<jp>` ("My words" deck) and share spaced
  repetition in `S.cards` (`bumpWord`, `reviewWords`).
- **Auto-update**: on open, on returning to the app, and every 15 min, `checkUpdate` fetches
  the live page and compares its `<script>`/`<style>` with the running ones. If different it
  reloads right away when idle (`canReloadNow`), otherwise when the app is next hidden. Loop
  guard: at most one auto-reload per 2 min (`yuki-upd-at`). Still bump `APP_VERSION` (shown in Me).
- **Speaking vs chat lessons**: `isSpeakingKey(key)` — in each unit lesson b and the roleplay are
  🎙️ speaking (the call screen opens automatically when the talk starts, target words shown on
  the call screen), lessons a and c are 💬 chat. Shown as tags on path nodes and in the lesson
  player.
- **Separate chats**: `S.threads` = {id: {title, kind, msgs, at}}, `S.chatId` = open thread,
  `S.chat` is only a pointer to the open thread's msgs (`linkChat()`; not saved twice). "main" =
  free chat with Yuki; each course talk/lesson/quiz/custom lesson opens its own thread
  (`openThread`, 30 most recent kept). Chat header title opens the chats list. Course state only
  applies in its own thread (`activeCourse()`); replies go to the thread they were sent from.
- **Path (home tab)**: winding path of nodes with coloured unit banners and a sticky unit card
  that appears once you scroll past a banner (`pathScroll`). N5 = the conversation course;
  other levels are built from `CUR[level]` (lessons + a 🏆 unit review). `pathNodes()` /
  `pathUnits()`; custom ⭐ lessons in `S.plan.custom` ({id,title,before,level}) from the
  "⭐ Add a lesson" sheet or Yuki's `path` MEM field. Progress in `S.plan.done`.
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
  weak, strong, learned, right, wrong, lessonDone, used, path. The app strips it (`parseMem`), saves it
  to the profile (`applyMem`), and feeds the profile back into `systemPrompt()`.
  Don't break this format.
- **Lessons**: 100+ lessons in the `CUR` object, grouped by level (n5–n1) → unit →
  [id, title, description]. Tapping one starts a step-by-step lesson in chat, and
  "✓ Done" marks it complete.
- **Voice call mode**: full-screen orb, Web Speech API speech recognition (ja-JP or en-US)
  and speechSynthesis that splits Japanese and English into separate voices. Voices are
  ranked by `voiceScore()` (Premium/Enhanced/Siri first, detected from name or `voiceURI` via `isHQ()`, novelty voices excluded) and can be
  chosen in Me (`S.settings.voiceEn` / `voiceJa`).
  Optional "Natural voices" engine (`S.settings.tts="azure"`): Microsoft Azure neural TTS
  (same voices as Edge Read Aloud; Edge TTS itself can't be called from iPhone Safari) via
  REST with the owner's own key (`azKey`, `azRegion`, never in backups). One SSML request per
  reply switching between `azEn`/`azJa` voices (`AZ_VOICES`), played with Web Audio, cached
  (`natCache`), monthly characters counted (`ttsChars`, free tier 500k). Falls back to iPhone
  voices on any error. `isSpeaking()` / `stopSpeak()` cover both engines.
  Free recorded Japanese audio: every `CARDS[*].say` (incl. course words) is pre-recorded with VOICEVOX in
  `audio/himari/` and `audio/ryusei/` (file name = `recId(text)`), chosen with
  `S.settings.jaRec`; `speak()` plays these first for exact matches, and in the default
  engine `speakWithRecordings()` also uses them for any matching Japanese segment inside Yuki's
  replies (rest = iPhone voice). New decks: re-run
  `tools/gen_audio.py`. Credits "VOICEVOX:冥鳴ひまり" / "VOICEVOX:青山龍星" must stay (Me + README).
  Live "Himari & Ryusei" engine (`S.settings.tts="voicevox"`, `vvUrl`): the owner's own free
  VOICEVOX server (Hugging Face Space built from `voice-server/Dockerfile`, CORS open). `speakVV`
  synthesises Japanese segments on the server (`fetchVV`, speaker from `jaRec`, cached) and
  speaks English segments with the best iPhone voice, in order; falls back to iPhone voices if
  the server is asleep/unreachable. `pingVV()` wakes the server on open. `vvBase()` accepts
  "user/space" or a full URL. Shown as "Own server (advanced)" (HF Docker Spaces may need billing).
  Default engine "Ryusei everywhere" (`S.settings.tts="quest"`, default voice `jaRec="ryusei"`):
  Japanese segments play from the recordings when they match, otherwise live from the free public
  VOICEVOX service tts.quest (`questUrl` → mp3StreamingUrl, played on one shared <audio> element
  unlocked on first tap; speaker id from `REC_VOICES`); English parts use Ryusei or the iPhone voice; any
  failure (busy/unreachable) falls back to the iPhone voice for that segment; a "retryAfter ≤ 4 s" answer is retried once. With
  `enVoice="ryusei"` (default again at the owner's request; "iphone" optional) English is sent to VOICEVOX too, lower-cased with contractions
  expanded (`englishForVV`), neighbouring live segments merged into one request.
  All recordings and tts.quest clips play through one shared <audio> element (`questPlayer`,
  `playUrl`, unlocked on first touch/pointer) rather than Web Audio, which iOS silently suspends
  after calls/mic use/app switches; the first clip starts synchronously inside the tap.
  iPhone audio session: `setAudioMode("playback")` normally, "play-and-record" only while the
  mic is actually listening ("playback" alone blocks the microphone; keeping "play-and-record"
  for a whole call makes voices sound muffled/telephone-like).
  `cleanSpeech()` drops romaji in brackets right after Japanese (「こんにちは」(konnichiwa)) so the
  English voice doesn't mangle it.
  `applyMem` coerces MEM fields with `asList()` and is wrapped in try/catch so an odd memory
  line can never break a reply.
  Two mic buttons everywhere (chat input bar and call screen): 🎤 日本語 and 🎤 English, each
  starting recognition in that language for one utterance (`startMic(…, lang)`, `UI.micLang`),
  because iPhone recognition handles one language at a time. Default `micLang="ja-JP"`.
  Yuki is told English via the Japanese mic arrives as katakana and English-mode Japanese as
  look-alikes ("Ohio"). Captions toggle sits top-right on the call screen.
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
- State object `S` (currently `v:15`) saved to localStorage key `yuki-sensei-v3`. Keep it backward
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
