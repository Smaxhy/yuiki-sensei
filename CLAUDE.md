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
- **Conversation courses (N5 + N4)**: `COURSE` = 36 units: 24 N5 + 12 N4 (unit field `lv`, default "n5"). v30 added 10 N5
  units before "Real conversations" (money & big numbers c15, konbini c16, restaurant c17, past tense c18, adjectives c19,
  health c20, plans & phone c21, home c22, seasons c23, explaining c24; kana bites ナニヌネノ…パピプペポ) and the N4 course
  c31–c42 (requests/permission/rules, -ている, casual plain forms, opinions & comparing, experiences, work & school,
  giving & receiving, feelings & ～そう, trains & directions, weather & ～たら/～ば, keigo, Real N4 conversations = FINAL;
  N4 units have `kana:""` so no kana node). Words may carry a 4th field of kanji spellings ("一万|万") that feed
  `KANJI_ALT` for mic detection. Level helpers: `isN5Path()` = level n5 or n4, `courseLv()`, `unitLv(u)`, `levelUnits(lv)`;
  the path shows only the current level's units (titles "Unit k" / "N4 · Unit k"), recaps every 3rd unit by position,
  finals `cq:final` (N5) / `cq:final4` (N4), tests and the final conversation use that level's words. v30 migration moves
  Real conversations' progress 13 → 23 (after v26's 11 → 13). Original units: `COURSE` 14 topic units (greetings, introductions,
  numbers, food, time, hobbies, family, shopping, directions, weather & feelings, travel, small talk (c13*),
  making friends (c14*), real conversations). State v26 inserted the two new units before "Real conversations"
  (migrate remaps cr:11/cq:11:m/cq:11:t → index 13; ck:11 stays since unit 11 still teaches カキクケコ). Each unit
  has a can-do goal `cd`. Each unit: 3 lessons of max 5 words `[jp, romaji, en]`, a 5-kana bite
  (`kana`), and a roleplay (`rp`; "FINAL" = end-of-course conversation). Path order per unit:
  lesson, lesson, kana, lesson, roleplay. Node keys `cl:<id>`, `ck:<unit>`, `cr:<unit>`.
  Lesson player (`UI.lp`, `vLesson`): Learn (one word per card, recorded audio) → Practise
  (offline tap quiz incl. 2 review questions from older due words) → Talk. Talk = `S.course`
  ({key, kind, title, goal, scen, targets, used, review}); `coursePrompt()` tells Yuki to make
  the student use every target word and to bring back older words; words tick off via
  `detectUsed()` on what the student types (kana, kanji spellings via `KANJI_ALT`, digits turned back into Japanese via `jaDigits()` — the Japanese mic also converts digits — romaji, or English voice-typing look-alikes like "Ohio" via `soundsLike()`; everyday English words in `EN_COMMON` never count) and the `used` MEM field; all used
  AND at least `TALK_MIN` (6) messages from the student in that talk (`talkTurns(c)` counts the student's messages in the whole thread, opening excluded; `courseTurn()`, `talkDone()`;
  `courseResync()` in `vChat` re-ticks target words from everything already said; chip
  "💬 n/6"; `coursePrompt` asks for a real back-and-forth with follow-up questions, not word drilling)
  → node done and a "Lesson complete" card (`courseDoneCard`) with ✓ Finish lesson / Keep practising
  appears in chat and on the call (hands-free stops auto-listening until "keep practising"). Course words are flashcards `w:<jp>` ("My words" deck) and share spaced
  repetition in `S.cards` (`bumpWord`, `reviewWords`).
- **Tutor structure** (owner: "make it professional, like a real tutor giving assignments"): every path step has an
  objective `nodeGoal(n)`, a kind `nodeKind`, minutes `nodeMin`, a plan `nodePlan` (numbered steps + what counts as
  passing) and `nodeBuilds` (the last finished lesson goal before it). Tapping a node (or the Home "📋 Your next
  assignment" card, `nextCard()`) opens the lesson brief `vBrief` (`UI.brief` = node key, full screen) → "Start lesson"
  (`ACT.briefGo` → `startNode`). Unit banners show the unit goal; the path folds finished units into slim bars and shows
  only banners for units after the next one (no auto-scroll; tap a banner → `unitSheet`, which lists each step with its
  objective and opens its brief). Lesson-player done screens and `courseDoneCard` show the objective; finishing a
  roleplay toasts "🏅 Unit goal reached". Progress → "🎯 What you can do now" (`canDoList`/`canDoHTML`: finished lesson
  goals + reached unit goals, next objective). `coursePrompt` asks Yuki to open with today's objective in one line.
- **Lessons build on each other** (owner: "each path progressive, based off the last lesson, with quizzes and random
  things"): `prevLessonOf(n)` = the lesson before in `CLESSONS` (a roleplay's = its unit's last lesson). A CL lesson starts
  with "🔁 Recap" (`recapQs(n)`: 3 questions on last lesson's learned words: meaning, how-do-you-say, 👂 listening;
  `UI.lp.recap`/`hadRecap`, then Learn). Practise adds 2 👂 listening questions (`dir:"listen"`) and one ⌨️ typed answer
  (`dir:"type"`, `ACT.lpType`: romaji or kana, 1 typo allowed) to the usual questions. `startTalk` puts up to 2 of last
  lesson's words first in `S.course.review` and stores `S.course.prev` (last lesson's goal); `coursePrompt` tells Yuki to
  link back to it and to drop in 1–2 surprise mini-tasks (quiz, fill-the-gap, [[listening]]). The objective (`.tgoal`)
  shows above the target words in the chat lesson bar and on the call screen. (`.tbar .tgoal` takes the full row; on the call
  screen `.vgoal` must stay `flex:0 0 auto`, an unscoped flex-basis:100% once pushed the chips and captions off screen).
  Target-word chips show the English meaning under each word; tapping one (`ACT.chipWord`) plays it and toasts the
  meaning. `KANJI_ALT` also covers the small-talk/making-friends words and the polite phrases the mic writes in kanji
  (初めて, 凄い, 私も, 最近, 今度, 連絡します, お願いします…; Latin "line" for ライン); `detectUsed` looks it up by the
  hiragana key or the original spelling.
- **Roleplay warm-up**: a roleplay / the final conversation (CR node) first runs the lesson player on its 5
  target words (`rpTargets(n)`, `UI.lp.pre`: "Warm-up" → Practise, free), then `startTalk(n, lp.targets)` uses
  the same words. `coursePrompt` tells Yuki to use only Japanese the student has learned (anything else with
  its English in brackets).
- **Path tests & recaps** (free, offline; state v23; made harder on the owner's request): N5 units get ⚡ Mini test
  after lesson b (`cq:<u>:m`, 10 Qs, pass 70%), 📝 Unit test after the roleplay (`cq:<u>:t`, 16 Qs incl. the unit's
  kana, 80%), 🔁 Big recap every 3 units (`cq:<u>:r`, 20 Qs over the last 3 units, 80%) and 🏅 N5 final test
  (`cq:final`, 30 Qs, 80%). Other levels get a 🔁 Card recap after each unit review (`<lv>:<u>:c`, 15 Qs, 70%).
  Test questions (`makeQ(id,true,pool)`) take wrong options from the same test first (similar words) and mix in
  TYPED answers: `typeRo` (English shown → type the Japanese in romaji or kana), `listenRo` (hear it → type it),
  `typeSound` (kana → type its sound); `q.typeIn="ro"`, checked in `ACT.qzType` with `normR`/`normJ`/1 typo allowed. Node type "CQ";
  `testSpec(n)` → `startTest()` → `UI.qz.test` with a recap page first (`intro`, tap to hear), questions from
  `makeQ(id,true)` (adds 👂 listening questions), full screen like a lesson, passing marks the node done,
  failing offers Try again. v23 marks tests in already-finished units as done so the path doesn't jump back.
- **More recaps** (state v31, owner: "more big recaps, recaps of all past lessons, last 6 lessons, 2…"): every N5/N4 unit gets
  ⚡ Quick recap `cq:<u>:q` after lesson c, before the roleplay (lessons b+c, 8 Qs, 75%). Unit-end recaps by position in the
  level (`endRecap(pos)`): every 6th unit 🌏 Everything so far `cq:<u>:a` (all units of the level so far + kana, 25 Qs, 75%),
  else every 3rd 🔁 Big recap `:r`, else every 2nd 🔁 Recap · last 6 lessons `:s` (last 2 units, 14 Qs, 75%). v31 migrate
  marks q (lesson c or roleplay done) and the unit-end recap (unit finished) as done, and an old `:r` where `:a` now sits
  carries over. Practice → "🔁 Recaps of past lessons" (`RECAPS`, `doneLessons()`, `recapSpec(v)`, `ACT.recap`): free
  tests on the last 1 / 2 / 6 / 12 finished lessons or everything; they're `test.free` (no path node, +10 XP, retry keeps
  the spec, closing returns to Practice). `nodeSub` for tests now reads counts from `testSpec`.
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
  "⭐ Add a lesson" sheet or Yuki's `path` MEM field (accepted only when the student's last message asks to add
  a lesson / mentions the path; Yuki used to add repeats by herself, so v28 cleared all old ⭐ lessons). Progress in
  `S.plan.done`. Locking: `nodeLocked(n)` = not done and after the first unfinished step; tapping it (path, unit sheet,
  brief) only toasts `lockedToast()`; locked bubbles show a 🔒 badge. Finished steps can always be redone; "skip the
  unit" in the unit sheet still marks a whole unit done.
- **Tabs**: Path, Yuki (chat), Translate (`UI.tab="translate"`), Practice, Cards, Me (labels 10.5px). Progress (`UI.tab="progress"`) is opened from the top row of Me → You (and the Home goal ring / streak pill); it has a "‹ Me" back button and lights up the Me tab. Cards (`vCards`) lists only learned cards
  (`S.cards`), weakest first, filter chips (`UI.cardsF`), and practises them with the "mine" decks
  (`MINE`: mine / mine-words / mine-kana / mine-kanji = due first, then weakest, never new cards). Home's
  "to review" and Practice's "Review due cards" open it. "All lessons" (`UI.tab="learn"`) opens from the
  path, the level sheet, or Practice.
- **Progress system** (state v21): every study day has a record `S.days["YYYY-MM-DD"]` = {xp, sec, cards,
  words, msgs, calls, les[], goal?, frozen?}. `addXP(n, kind, label)` is the single entry point (flashcard
  1–2, lesson practice 1–2, word used in a talk 5, message 2 / spoken 3, path node 15 (kana 10), CUR lesson
  15, level check 10). Study time = gaps between taps under 2 min (`track()`, on every click).
  `S.daily` = {goal (20/50/100/150, from onboarding minutes via `goalForMinutes`), freeze (0–2, +1 every
  7 streak days), best, exam/examName (countdown, 🎌 on the calendar), remind ("HH:MM"), badges [[id,date]],
  init}. `streakInfo()` counts consecutive active/frozen days ending today or yesterday; `checkFreeze()`
  (on open and on return) spends a freeze when exactly yesterday was missed. The old `stats.streak` was
  turned into study days in the v21 migration. Progress tab (`vProgress`): today ring + goal picker,
  `calendarHTML()` month grid (tap a day → `daySheet`), `weekHTML()` 7-day bars, countdown, daily reminder
  (in-app "Study time!" on Home after `remind`, plus `addReminder()` = a repeating .ics event with an alert
  for the iPhone Calendar), all-time stats, `BADGES` (16, `checkBadges`), word bank (`wordBankSheet`).
  Home shows `todayStrip()` (goal ring, streak, cards due). Practice shows the word of the day
  (`wordOfDay()`, from VOCAB, same all day; add to flashcards / use it with Yuki).
- **Me tab**: a profile header plus rows that open sub-pages (`UI.me` = profile, talk, voice, ai, memory,
  app; `ME_SECS`, `ACT.meSec`). The chat error bubble opens AI setup directly.
- **Yuki the AI tutor**: 26, from Kyoto, warm and playful, corrects mistakes clearly.
  Calls the Anthropic Messages API directly from the browser (`apiRequest()`) using the
  owner's API key, which is saved only in localStorage (never in the repo).
  Default model: `claude-haiku-4-5-20251001`. Calls always use Haiku (`FAST_MODEL`, `apiRequest(body,cheap)`), at
  most 6 recent messages, max_tokens 400, and a shorter system prompt (no chat-only rules). Note: Haiku 4.5
  only caches prompts of 4096+ tokens, so Yuki's prompt isn't cached on Haiku; savings come from sending less. Optional "Smart" model: `claude-sonnet-5-5`
  (sent with `output_config.effort:"low"` and server-side fallbacks; Haiku 4.5 rejects effort).
  The system prompt is two blocks: a stable one (persona, learner card, style rules; marked
  `cache_control`) and `memoryPrompt()` (memory, stats, current lesson) which changes per turn.
- **Reply style** (`S.settings.style`): length (tiny/short/normal/detailed, default tiny; v27 set everyone to tiny because
  the owner's credits went too fast; tiny = under 20 words, calls = under 15 words, max_tokens 300 for both), English vs Japanese, reading help, simple
  English. Turned into prompt lines by `styleRules()`.
- **Credit saver** (`S.settings.history`): 6/12/24 recent messages sent per request, default 6 (v22 set
  everyone to 6). Messages older than the last two are cut to 300 characters in `buildMessages`. The system
  prompt is deliberately compact (~600 tokens) and `memoryPrompt` sends short lists (6 lessons, 12 facts,
  8 weak, 5 strong, 12 learned); max_tokens tiny 350 / short 500 / normal 800 / detailed 1300 (calls 350).
  A typical chat request is ~1,100–1,300 input tokens. Keep new prompt text short: it's paid on every message.
- **Spending meter** (`S.usage`, `noteUsage()` from the API's `usage`, `PRICE` per model, `spendCard()` in
  Me → AI setup & spending): this month, replies, cost per reply, "$20 ≈ N replies", last reply's tokens.
- **Corrections**: when the student's message is their own sentence with Japanese, Yuki adds a hidden
  `<<FIX>>{"ja","en","ok","why"}` line before `<<MEM>>` (rule in `systemPrompt`). `takeFix()` strips it (before
  `takeSay`), it's stored as `msg.fix` on the user message and shown under it (`fixHTML`: correct Japanese
  with 🔊, punctuated English translation, 💡 reason) and on the call screen (`.vfix`). Skipped for app
  commands (messages with `api` text, except voice). On calls the live transcript is shown tidied
  (`tidySpeech`), Yuki is told to always add FIX, and the call card shows "You said" (struck through) above
  the correction; the orb shrinks while a correction is shown. English sentences get one too ("✏️ Better English" =
  their English fixed, plus "🇯🇵 In Japanese"), so spoken English is corrected as well.
  Yuki sometimes writes markers slightly wrong ("FIX>>"): `normMarkers()` restores `<<FIX>>`/`<<MEM>>`/
  `<<SAY>>` before parsing, and `stripHidden()` removes any leftover hidden line from what is shown
  (`md`), captioned (`captionText`) or spoken (`cleanSpeech`). `md()` also renders *italics*.
- **Tidy voice typing**: `tidySpeech()` (free, on the phone) gives mic transcripts punctuation and capitals:
  spaces between Japanese words removed (。 after です/ます…, 、 after greetings/yes/no via `JA_PAUSE`),
  ending 。/？ or ./?, capital first letters and "I". Course-word detection still uses the untidied words
  (`UI.spoken`).
- **Memory**: every AI reply ends with a hidden line `<<MEM>>{json}` containing facts,
  weak, strong, learned, right, wrong, lessonDone, used, path. The app strips it (`parseMem`), saves it
  to the profile (`applyMem`), and feeds the profile back into `systemPrompt()`. No repeats (owner: "a lot of it is
  repetitive"): `addMem` drops near-duplicates before adding (`memSame` = word/kana-pair overlap after removing filler like
  "the student", "lives in japan now" = "Lives in Japan"; learned items match by the Japanese word via `learnKey`); new
  "strong" removes it from "weak" and vice versa; caps facts 30 / weak 20 / strong 20 / learned 300. The prompt asks for
  only things not already in YOU REMEMBER. v29 runs `cleanMemory()` once on old saves. Me → What Yuki remembers: tap ✕
  (`ACT.memDel`) to make her forget an item.
  Self-improvement (owner: "the AI constantly learns from its mistakes"): `S.profile.teach` = Yuki's teaching notes about
  this student (MEM field "teach", 1 short rule when she notices confusion / too hard / too long; and the 👍/👎 under her
  latest reply: 👎 → `FB_REASONS` sheet → a rule like "Keep replies shorter"); max 10, deduped by `addMem`, sent as
  "YOUR TEACHING NOTES … always follow" in `memoryPrompt`, removable in Me → What Yuki remembers.
  Brain-like memory (v2026.10.14-12, owner: "remember things better, improve more and more, work like a brain"; all local,
  no extra API calls): `S.profile.str` = {memK(text): [strength, lastSeen]}; `addMem` adds +1 strength when a memory comes
  up again and, when a list is full, forgets the lowest `memScore` (strength vs. age; memories without an entry count as
  strength 2, a week old) instead of the oldest (learned items still drop oldest). `recall(list,n)` picks what's sent:
  overlap with `recallCtx()` (last student message, current lesson/convo) ×3 + memScore — used for facts (12), weak (8),
  strong (5). `S.miss` = {cardId: [wrong, right, lastWrong]} from `noteMiss` in `bumpWord`, `grade`, `qzGrade`;
  `keepsMissing(n)` → prompt line "Keeps getting wrong in quizzes (bring these back)". `episode(text)` writes Yuki's diary
  `S.profile.eps` (max 30, "MM/DD …"): lesson talk finished, every test result with missed words, conversation practice
  (at 6 turns); the last 3 go in the prompt as "Recent sessions", plus a rule to use memory like a friend. Me → What Yuki
  remembers shows ★ strength, "❌ Words you keep missing" and "📓 Yuki's diary".
  Don't break this format.
- **Lessons**: 100+ lessons in the `CUR` object, grouped by level (n5–n1) → unit →
  [id, title, description]. Tapping one starts a step-by-step lesson in chat, and
  "✓ Done" marks it complete.
- **Voice call mode**: full-screen orb, Web Speech API speech recognition (ja-JP or en-US)
  and speechSynthesis that splits Japanese and English into separate voices. Voices are
  ranked by `voiceScore()` (Premium/Enhanced/Siri first, detected from name or `voiceURI` via `isHQ()`, novelty voices excluded) and can be
  chosen in Me (`S.settings.voiceEn` / `voiceJa`).
  Removed engines (owner's request, v27): ElevenLabs, Microsoft Azure and the "Own server" VOICEVOX Space are gone;
  migrate drops their settings/keys and moves those users to Ryusei everywhere; the ElevenLabs clip cache is deleted on
  open. The only engines are "quest" (Ryusei everywhere) and "device" (⚡ Fast).
  Recordings v2 (v2026.10.14-9, owner's log: tapping えん ten times, "voice breaking and delayed in lessons"): all clips in
  audio/ryusei and audio/himari were re-processed by `tools/fix_audio.sh` (≥0.25 s silent lead-in, because iPhone/AirPods
  swallow the first moment of short words; louder: peak about -1.5 dB, +9 dB max). Run it on any new clips
  (`ls audio/*/*.mp3 | xargs -P8 -n1 tools/fix_audio.sh`; it skips clips that are already done). Clip URLs carry `AUD_V`
  ("?v=2", bump it when the recordings change); sw.js uses the cache "yuki-audio-2" and deletes the old "yuki-audio".
  Free recorded Japanese audio: every `CARDS[*].say` (incl. course words) is pre-recorded with VOICEVOX in
  `audio/himari/` and `audio/ryusei/` (file name = `recId(text)`), chosen with
  `S.settings.jaRec`; `speak()` plays these first for exact matches, and in the default
  engine `speakWithRecordings()` also uses them for any matching Japanese segment inside Yuki's
  replies (rest = iPhone voice). New decks: re-run
  `tools/gen_audio.py`. Credits "VOICEVOX:冥鳴ひまり" / "VOICEVOX:青山龍星" must stay (Me + README).
  Ryusei = Japanese only (v2026.10.14-6, owner: "I need Ryusei to only speak Japanese, not English, that's what bugs it"):
  `enRyusei()` and `sayWanted()` always return false, migrate forces `enVoice="iphone"` and the "English parts" picker is
  gone; English always goes to the English voice (online/iPhone). The enVoice="ryusei" notes below are history.
  Default engine "Ryusei everywhere" (`S.settings.tts="quest"`, default voice `jaRec="ryusei"`):
  Japanese segments play from the recordings when they match, otherwise live from the free public
  VOICEVOX service tts.quest (`questUrl` → mp3StreamingUrl, played on one shared <audio> element
  unlocked on first tap; speaker id from `REC_VOICES`); English parts use Ryusei or the iPhone voice; any
  failure falls back to the iPhone voice. `questUrl` keeps retrying "retryAfter" answers (up to
  ~25 s, like tts.quest's own browser example) and records `questLastErr`; with Ryusei for English
  the whole reply is ONE request. Optional free tts.quest key `S.settings.questKey` (never in
  backups); Me → Voice → "Test Ryusei's live voice" shows the exact error. With
  `enVoice="ryusei"` (optional; default is now "iphone" — owner: "doesn't have to be Ryusei, just a better voice") English is sent to VOICEVOX too, lower-cased with contractions
  expanded (`englishForVV`), neighbouring live segments merged into one request.
  tts.quest goes silent on English letters, so with Ryusei for English Yuki adds a hidden
  `<<SAY>>` line before `<<MEM>>` (the whole reply with English in katakana; requested only when
  `sayWanted()`); `takeSay()` strips it, it's stored as `msg.say` and spoken instead of the text.
  Without it, `toSpeakable()` keeps Japanese, turns common English words into katakana and drops
  the rest, so no Latin letters are ever sent.
  All recordings and tts.quest clips play through one shared <audio> element (`questPlayer`,
  `playUrl`, unlocked on first touch/pointer) rather than Web Audio, which iOS silently suspends
  after calls/mic use/app switches; the first clip starts synchronously inside the tap.
  A clip counts as played once it has started (`playUrl`, `playId`): an error after it started, or 3 s
  without progress, ends it instead of retrying, so Ryusei never repeats a sentence. Retries (stream,
  then a few tries of the finished file) only happen if no sound came out at all.
  No gaps when switching voices: `speakQuest` prepares every Ryusei clip up front (`prepClip`: wait for
  tts.quest `questReady`, then download into memory with `toBlobUrl`, cached) while the iPhone voice is
  still talking, so each clip starts the moment the English ends. The 120 ms gap before the iPhone voice
  only applies right after a clip (`clipEndAt`).
  All or nothing (v2026.10.14-2, owner: "the voice keeps breaking and glitching in lessons"): `speakQuest` first waits for
  EVERY Ryusei clip of the reply (`Promise.all` of `prepClip`s, 5 s, 3.5 s when `questSlow()`), then plays them in one go;
  if any isn't ready in time (or fails), the whole reply is read by the iPhone voice (`speakPlainDevice`) — no switching
  voices mid-reply. The older mid-reply cut-off below now only matters for play-time failures.
  No pre-wait (v2026.10.14-10, owner: "it works but it's very delayed"): the all-or-nothing wait below is GONE. `speakQuest`
  starts speaking at once (English in the English voice); a Japanese part waits briefly for its clip (first one up to
  2.5 s from the start, 1.5 s when `questSlow()`; later ones 1.2 s / 0.8 s), else the iPhone Japanese voice says it and the
  rest of the reply (`stay`). Before a clip: `synthIdle(600)` and a 200 ms duck gap. `stopMic` waits only 450 ms for
  iPhone's "end" (was 1.5 s). English parts are always spoken by the English voice on calls when "Read English parts" is on.
  Mic + Ryusei lead-in (v2026.10.14-13, owner: "it fails to pick up my voice while calling and Ryusei still breaks often"):
  `stopMic` waits up to 1.2 s (words already in) / 2.5 s (nothing yet) for iPhone's late results, and a result arriving
  after Send closes the mic 350 ms later (`MIC.closeIt`, `MIC.lateT`); the 0.45 s cut-off lost the words. Live Ryusei clips
  get 0.25 s of silence in front (`padClip`: `mp3Fmt` reads the sample rate/channels, `LEAD_MP3` = silent MP3s without a
  Xing header for 22.05/24/44.1/48 kHz mono/stereo) in `ryGet`/`ryPut`; later Japanese parts wait up to 2.5 s (1.8 s when
  slow) before the iPhone voice takes over, the first one up to 3 s.
  Lesson audio (v2026.10.14-4, owner: "playing audios still isn't working during lessons"): `preloadRec(list)` downloads
  the recordings a lesson (`lpSay`: items + quiz) or quiz/test (`qzSayListen`, also on `startTest`) needs into memory
  (`recBlobs`, blob URLs), so `playRecorded` plays them from the phone; if a clip fails it tries once the other way
  (internet ↔ memory) before the iPhone voice. sw.js never fails an audio response just because saving it to the cache
  failed (full storage). The Ryusei sentence cache is capped at 300 and halves itself if storage is full.
  Saved Ryusei (v2026.10.14-3, owner: "make Ryusei's servers work better so he doesn't crash or pause"): live
  sentences go through `ryuseiClip(text)` = phone cache first (Cache Storage "yuki-ryusei", key `ryKey` = speaker+text,
  `ryGet`/`ryPut`, max 300, blob URLs in `ryMem` max 60), else `prepClip(questUrl(text), null)`. `my = null` means the
  request keeps going after the reply's deadline (background) and is saved, so a sentence said once plays instantly
  forever (Say it again, repeats, offline). The slow-server pause is 5 min, and while paused `questProbe()` (from
  `speakAI`, max once a minute) quietly asks tts.quest for the reply's first Japanese part; under 4 s → unpause,
  toast "🎌 Ryusei's voice is back".
  Ryusei never holds Yuki up: if a clip isn't ready 3 s after its turn (5 s for the first one; 2 s / 3 s when
  `questSlow()`), the iPhone voice says the rest of that reply. tts.quest requests go one at a time (`questQ`; bursts trigger "wait").
  An iPhone line that hasn't started after 1.8 s is cancelled and tried once more (`sayChunk`).
  "🔁 Say it again" (call screen, under the captions; also Repeat and the chat 🔊) runs `sayAgain()`:
  `resetAudio()` fully resets the speech engine and makes a fresh audio player inside the tap.
  Stopping is final: `stopSpeak()` bumps `spGen`, and `sayDevice`/`sayChunk`/`speakPlainDevice` check it
  before every sentence, so a cut-off reply can't carry on. The voice stops on End call, switching chat
  or tab, Finish lesson and when the app is hidden; a reply that arrives after you left isn't read out.
  Volume: Ryusei waits 300 ms after the iPhone voice (`synthEndAt`; iOS "ducks" other sound right after
  its own speech), and a mic that doesn't end after Send is aborted (an open mic keeps iPhone in quiet
  call sound).
  iPhone audio session: left on "auto" (forcing "playback" could silence speechSynthesis);
  "play-and-record" only while the mic is actually listening, then back to "auto" (keeping
  "play-and-record" for a whole call makes voices sound muffled/telephone-like).
  tts.quest playback (`playQuestAudio`): `questUrl` returns {stream, mp3, wav, status}; poll the
  status URL until `isAudioReady`, then play the finished MP3 (iOS is unreliable with streams);
  if status can't be read, try the stream, then retry the finished files. The "Test Ryusei"
  sheet shows which of the 3 steps fails (`questFail`) and has an iPhone-voice test.
  Particles は/へ before a space or punctuation (or standing alone) are sent as わ/え so Ryusei says "wa"/"e".
  Once Ryusei falls behind in a reply (clip not ready 4 s after its turn, 8 s for the first, or an error),
  the rest of that reply stays with the iPhone voice (`stay` in `speakQuest`) instead of switching back and
  forth. `resetAudio()` reuses the one shared player (a new player per repeat made iOS lower the volume),
  and the silent unlock sound never plays on a mic tap or while listening (it could block the mic).
  A clip that hasn't started within 3.5 s (local/blob) or 9 s (remote) is given up (`t2` in `playUrl`; iPhone
  sometimes accepts play() and stays silent); a failed recording is then said by the iPhone Japanese voice.
  Before a clip, Ryusei waits at most 1.2 s for the iPhone voice (`synthIdle(1200)`; iOS can report
  "speaking" for seconds after a line ended). `noteLat()` records live clip times; when the free service is
  slow (`questSlow()`, median of the last 3 > 4.5 s) the cut-off is shorter (3.5 s first, 2.5 s later) and a
  one-time tip suggests the free tts.quest key.
  Two late/failed Ryusei replies (`questLate()`) pause live Ryusei for 5 min (`questPaused()`, `useQuest()` false,
  toast once); recordings still play. The call-screen button then reads "⚡ Fast · tap for 🎌" and tapping it resumes.
  Call screen has a "🎌 Ryusei / ⚡ Fast voice" switch (`ACT.vFast`): Fast = `tts="device"` (recordings for
  learned words, the iPhone's own Japanese/English voices for everything else, no waiting).
  A mic with no sign of life retries once by itself (`MIC.retried`) before pausing.
  Pronunciation fixes: `vvText` also turns the particle は/へ into わ/え after known nouns in unspaced Japanese
  (`partRe()`: course nouns + pronouns, "わたしはゆき" → "わたしわゆき") and before question words (はなん/はどこ…);
  `romaToKana()` (in `speakAI`) swaps romaji of course/phrase words inside English ("say konnichiwa") for kana so the
  Japanese voice says them (≥4 letters, English look-alikes like zero/demo/made excluded); at N5/N4 Yuki is told to space
  Japanese words. No repeats: `saidBefore()` (in `memoryPrompt`) lists up to 8 of Yuki's replies older than the history
  window ("don't repeat these"), plus a vary-your-wording rule.
  Text for Ryusei goes through `vvText()`: spaces between Japanese characters removed (spaced
  beginner kana makes VOICEVOX pause after every word and stress oddly), Japanese punctuation.
  `cleanSpeech()` speaks the reading for 漢字(かな) instead of the kanji. Ryusei never starts while
  the iPhone voice is still talking (`synthIdle()`), and an iPhone line that never started is
  cancelled so it can't start late over Ryusei.
  iPhone speech (`sayDevice`/`sayChunk`): short sentence chunks (≤180 chars), resume if paused,
  120 ms gap after an audio clip, safety timer if "end" never fires, voice assignment guarded.
  🌐 Online English voices (`WEB_EN`, `voiceEn="web:<id>"`, default "web:google" since v25): free text-to-speech with
  no key or AI credits: Google Translate's `translate_tts` (client=tw-ob, US/UK). The StreamElements (Polly) voices
  were removed in v27: on the owner's iPhone they always failed with "play() refused: NotSupportedError". `sayDevice` sends English to `sayWebEn` (≤170-char sentence chunks on the shared player
  via `playUrl`, without bumping `natSeq`); offline, a failure, or 3 failures in a row → the iPhone voice. `speakDevice`
  routes through `sayDevice` when one is chosen (5 s to start; after one failure, the iPhone voice for the rest of
  the session). Reason: the owner's iPhone only gives web apps the basic voices (Samantha), even after downloading Premium.
  `voiceEn=""` = Automatic: the best-ranked iPhone voice (Premium > Enhanced > rest).
  v24 moved everyone off the old "system" value: Safari can't see the voice picked in iPhone Settings and web apps
  can't use Siri voices, so "system" just gave the basic voice. Better voices come from downloading a Premium/
  Enhanced voice in Settings → Accessibility → Spoken Content → Voices (then reopen the app); Automatic picks it up.
  🩺 Voice check (`voiceCheck()`, big button at the top of Me → Voice): plays a recording, Ryusei live (tts.quest),
  the online English voice and the iPhone voice one after another, plus a 🎤 Test mic, with ✅/❌ and the reason
  for each; then switches to what works (online voice failed → iPhone voice; live Ryusei failed → ⚡ Fast voice) and
  "📋 Copy the results for Claude" (results + voice log).
  Me → Voice shows the English voice in use (★ = Premium/Enhanced) with a 🔊 Test button.
  Below it, `enVoiceList()` lists every English voice Safari reports (★ count) with "🔄 Refresh voice list"
  (`ACT.refreshVoices`). Settings path on newer iOS: Accessibility → Read & Speak (was Spoken Content) → Voices.
  Voice log (`VLOG`, `vlog()`, Me → Voice → "🧾 Voice log", or tap the title on the call screen):
  every speak attempt, tts.quest request/answer, audio play/refusal/error and iPhone voice that
  didn't start, for diagnosing problems on the owner's phone. "📋 Copy log" copies it (with app version, engine and
  English voice) so the owner can paste it to Claude. Recordings inside a mixed reply are
  no longer played as fragments (only when the whole thing is one recorded word).
  `cleanSpeech()` drops romaji in brackets right after Japanese (「こんにちは」(konnichiwa)) so the
  English voice doesn't mangle it.
  `applyMem` coerces MEM fields with `asList()` and is wrapped in try/catch so an odd memory
  line can never break a reply.
  Japanese-mic transcripts go through `jaDigits()` and `kanaize()` (course words via `KANJI_ALT` +
  common beginner words in `KANA_EXTRA` back to kana; 今日は/今晩は only as standalone greetings);
  if kanji is left, the API text gets a note that voice typing added it.
  Mic engine (`MIC`, `startMic`/`micRun`/`resumeMic`/`stopMic`): iPhone only reliably starts
  recognition directly inside a tap, so `rec.start()` runs synchronously in the tap handler (no
  delays, no audio-session switching; the shared player is released first). Continuous listening
  until ➤ Send; if iPhone ends it, one immediate restart is tried, and if there's no sign of life
  (3.5 s, 5.5 s on the first start: iOS can be slow to start dictation right after opening) the mic PAUSES keeping the words ("tap 🎤 Continue or ➤ Send").
  Tapping the other language (or the same one while paused) resumes inside the tap. Hands-free
  (`S.settings.handsFree`) is off by default since iPhone may refuse a mic start without a tap.
  Pauses → commas: `onresult` notes the text so far when ~1 s passes before more words arrive (`MIC.marks`), and
  `withPauses()` puts "、" (ja) or "," (en) there; a mic restart between `MIC.base` and the new session counts as a pause
  too (`micText`). Numbers: `jaDigits()` reads digits with counter sound changes (`CNT_SPECIAL`/`CNT_READ`/`jaCount`:
  ひとつ, ふたり, よじ, いっぷん, さんじゅっぷん, はたち, ついたち, さんぼん…), drops thousands commas (1,000円 → せんえん) and
  reads phone numbers (0… with dashes) digit by digit.
  Results are joined with `joinResults`/`mergeHeard` (also base+session in `micText`): iPhone sends cumulative or
  repeated pieces ("hello", "hello how"…), and plain concatenation had doubled/scrambled what the owner said.
  Mic events are written to the voice log. Chat mic fills the text box (no auto-send).
  Default `micLang="ja-JP"`.
  Yuki is told English via the Japanese mic arrives as katakana and English-mode Japanese as
  look-alikes ("Ohio"). Captions toggle sits top-right on the call screen.
  Has "🔁 Say it again" (under the captions) and Slower buttons. If the mic is blocked, it shows iPhone fix-it steps.
  Mic permission is iPhone's decision (a web app can't grant itself permanent access): `micAllowSheet()` (Me → Voice →
  "🎤 Allow the mic for good") explains Settings → Apps → Safari → Settings for Websites → Microphone → Allow (or per site
  via aA → Website Settings). `micPermTip()` runs on each mic start: if `navigator.permissions` says "prompt", a toast
  points there (at most once per 3 days, localStorage `yuki-mictip`).
- **Listening**: Japanese wrapped in [[double brackets]] in AI replies shows as a hidden,
  tap-to-play audio clip.
- **Flashcards**: decks for hiragana, katakana, 80 core words, and 50 kanji, using
  Leitner spaced repetition stored in `S.cards`. Works offline with no AI. Rounds only use cards already
  learned (due first, then weakest); new kana come only from "＋ 5 new" (`learnNew`: 5 characters in chart
  order, shown with answer and sound, `UI.fc.learn`) or path lessons. Practice shows kana first, other decks
  folded under "More decks"; the Cards tab defaults to Kana. A card speaks only when flipped
  (audio before flipping gave the answer away; "🔊 Hear it (a hint)" plays it on purpose).
- **No look-alike answers**: every multiple-choice question (lesson practice/recap via `wrongOpts()`, tests and quizzes via
  `makeQ`) skips wrong options whose meaning overlaps the answer or each other (`meanClash`: compares English meanings
  without brackets, per "/" or "," variant, word containment) and words with the same reading. Owner hit はじめまして with
  "nice to meet you (please be kind to me)" as a "wrong" option.
- **Multiple-choice quiz** (`buildQz`/`startQz`/`vQuiz`, `UI.qz`): 10 questions from learned cards only (due
  first), 4 options from the same kind (kana: sound↔character; words: meaning↔Japanese; kanji: meaning or
  reading). No audio and no reading until you answer; then the answer, reading and audio show. Updates
  spaced repetition and XP. Started from the Cards tab (all/words/kana/kanji) or Practice.
- **Numbers**: deck "num" (`NUMS`: 0–10, 11, tens, 100, 300/600/800, 1000/3000/8000, 10000; cards `n:<n>`,
  learned 5 at a time with ＋ 5 new, in the Cards tab as "Numbers"). `jaNum(n)` reads any number to 99,999
  (さんびゃく, ろっぴゃく, はっせん…), `kanjiNum`, `numRomaji`. Free exercises (`numQuiz(mode)`, `NUM_MODES`: mixed,
  number→Japanese, Japanese→number, listen, hear & type, kanji numbers, prices in yen) generate new numbers up to
  `numMax()` (grows with the number cards learned); typed answers via `qzType`. `NUM_REC` (0–100, hundreds,
  thousands, 10000) are recorded in Ryusei/Himari like the cards; `jaDigits` uses `jaNum`.
- **Travel translator** (`UI.tab="translate"`, from the 🗣️ pill on Path and Practice; free, offline): English
  (typed, or the 🎤 in English) → Japanese without AI. `translateEn()` = `composeEn()` (sentence builder) first,
  then `translateOld()` (word patterns `TR_PAT` + `TR_FIX` phrasebook) as alternatives.
  Sentence builder: `trxClean` (contractions, "try it on"), splits sentences, strips "excuse me/hello" (→ すみません、)
  and "thank you"; an exact `TR_FIX` phrase wins; else `trxSentence` matches ~40 English frames (where is / where
  can I V / how much / what time does X open / when / what is / how long / how do I get to / do you have / is
  there X near here / is there X in this / can I have / can I V (potential for go/buy/pay/walk…, else てもいいですか)
  / can you V (てもらえますか) / is it ADJ (too → すぎます) / does this train go to / don't V (ないでください) / let's /
  I'm hungry… (`TRX_STATE`) / I'm from / nationality (`TRX_NAT`) / age / I'm here for N days / I want (to) / I
  don't need (いりません) / I like / I can't V (が + potential) / I V / I V-ed / I'm V-ing (ています) / X hurts /
  I have a headache / I have a reservation… / there is no X / my name is / which platform / do you take cards /
  a little spicy / commands (てください) / bare things (を ください, places → どこですか)); `trxSplit` tries
  run-on sentences as two. Pieces: `trxNP` (nouns `TRX_NOUNS`+`TR_WORDS`, adjectives `TRX_ADJ` i/na/の/v,
  this/that, next/other/same, counts with counters つ/人/枚/泊/本 (`trCnt`, kanji `trCntJ`), "another"/"more",
  "and/or", noun+noun → の, "train/ticket to X" → 行きの/までの, exit A3, platform 3), `trxVP` (verbs
  `TRX_VERBS` with groups 5/1/s/k, conjugated in kana and kanji by `vForm`), `trxMods` (time words `TRX_ADV`,
  "at 7 pm", "for 2 nights/people", to/from/at/in/by/with/near → particles), `trxBuild`. Result chunks
  `{k,j,e}` → `ja` (kana with spaces, matches recordings), `say` (kanji, for voices and the staff sheet),
  word-by-word breakdown chips. Unknown names (capitalised, e.g. "the Park Hyatt") stay in English letters
  (`guess`, note shown); guesses rank below the old patterns unless they're capitalised names.
  Recorded: every sentence from `trRecList()` (TR_FIX + patterns + `TR_EXTRA` = common built sentences, ~940)
  in Ryusei, louder (volumeScale 1.6, `tools/gen_translator.py`, file = `recId(kana)`). `trSay(ja,say)`: recording
  → else Ryusei live via `speakQuest` when online (not in ⚡ Fast mode, no English letters) → else the iPhone
  Japanese voice. "Save the voice for offline" (`trSaveOffline`) puts all clips and the page in the cache.
  New common sentences: add them to `TR_EXTRA` and re-run the generator.
- **Free translation + sentence bank** (no AI, no credits): the translator has two directions (`UI.tr.dir` "en"/"ja",
  🎤 in en-US or ja-JP). `trRun`: a sure offline hit (exact sentence-bank match, or a recorded built sentence) plays
  at once; otherwise, when online, `freeMT(text,sl,tl)` = Google Translate's public `client=gtx` endpoint (romaji
  via `dt=rm`), falling back to MyMemory, with a 6 s timeout; offline it uses the sentence builder/patterns/bank.
  The phrasebook chips were removed from the screen (owner: "I don't need preset texts"; `TR_FIX` still powers
  exact matches). Sentence bank `TRB` (localStorage `yuki-trbank`, max 3000, not in backups): every free
  translation, every `<<FIX>>` pair, and every Japanese sentence in Yuki's replies (`trHarvest(shown, fix)` in
  `send`, pairs like 「日本語 (English)」/「日本語 – English」, romaji brackets skipped via `trRomaji`).
  Sentences without English get it filled in for free in the background when online (`trFill`, ≤80 per session).
  `trBankFind` (exact, then shared words / character pairs); "📚 Browse saved sentences" sheet (`trBankSheet`).
  Screen (`vTranslate`, `.tx-*` CSS): big "Translate" layout like Google Translate — English ⇄ 日本語 bar (swap = `trDir`),
  a large textarea `#trIn` (Enter translates, Shift+Enter new line) with ✕ clear / big 🎤 / → translate, a large result
  card (🔊 Play, 📱 Show staff, 📋 Copy `trCopy`, "Word by word" folded), alternatives, and one small footer row:
  🧠 N saved (bank) · ⬇️ Save voice offline · ⓘ (`trInfo` explains offline/bank). The box shrinks once there's a result.
- **Offline helper** `sw.js` (service worker, registered on https): navigations are network-first with the
  page cached for offline (auto-update unaffected); `/audio/` is served from the cache when saved (Range
  requests answered with 206 for Safari), otherwise fetched and cached.
- **Study time vs XP**: XP goals no longer claim minutes (tests give XP fast); real minutes (`sec`, gaps
  between taps under 90 s) show next to XP on Home and Progress.
- **Kana charts**: tap any character to hear it; ones missed get a red border.
- **Real conversations** (Practice → 🗣️ Real conversations, uses credits): `CONVOS` (café, meeting someone new, izakaya,
  lost in Tokyo, clothes shop, hotel check-in, "how was your day?", free talk). `ACT.convo` sheet → 🎙️ call or 💬 chat
  → `startConvo(id,voice)`: own thread `cv:<id>`, `S.convo` = {id,title,scene,turns}; `convoPrompt()` (in `memoryPrompt`,
  only in that thread via `activeConvo()`) keeps Yuki in character, chatting naturally, and after ~10 exchanges wrapping
  up with what went well, 2 things to improve and a score /10. Turns counted in `send`.
- **Making friends & small talk** (Practice → 🤝, top of the page): `TALK` = 6 groups (start a chat, react, keep it going,
  topics, make friends, rescue phrases), 40 phrases `[jp spaced, romaji, en]`; cards `t:<jp without spaces>` (deck "talk",
  `talkSay`, `cardKind` "talk", Cards filter "Phrases", `mine-talk`, ＋ 5 new phrases). Recorded in Ryusei/Himari (particle
  は synthesised as わ). `CONVOS` entries with a 6th field "st" (stranger 🎲 / mkfriend 🤝 / roulette 🎡) get a fresh random
  scene from `convoScene()` (`ST_PEOPLE`, `ST_PLACES`, `ST_TOPICS`, all adults) and small-talk coaching in `convoPrompt`
  (`S.convo.st`: tip to react/ask back, wrap-up rates reactions, asking back, keeping it going). 💡 Phrase helper in any
  convo thread: chips `PH_QUICK` + "💡 Phrases" (`phraseSheet`, `ACT.phIns` inserts into `#inp`; on a call it speaks it),
  also a 💡 button on the call screen. `buildQz("words")` now maps to "word" (the Words quiz button was finding nothing).
- **Conversation steering + speaking test**: `systemPrompt` CONVERSATION rule: chat naturally (react + one follow-up) but
  move every reply toward the current objective, bridge back when they drift, never re-ask answered questions. 🎓
  "Speaking test: everything I've learned" (`CONVOS` id "exam", 6th field "exam", row at the top of Practice → Real
  conversations): `examTopics()` = units with finished lessons (title + goal) + up to 24 learned words; `convoPrompt`
  runs it as a smooth examiner chat, ~2 exchanges per topic with transitions, then a score /10 per topic, overall, 2
  strengths, 2 things to practise. The course's final conversation also gets the topic list.
- **Quizzes**: mixed, weak spots, vocab, grammar, kanji, listening, translation, and
  roleplay, all run by Yuki in chat one question at a time.
- **No answering old messages** (v2026.10.14-5, owner: "it translates things from previous questions and repeats itself"):
  `buildMessages` sends only the newest of two student messages in a row (an earlier one left unanswered by a failed
  reply used to be glued on, so Yuki answered/translated it again); the prompt says to reply only to the latest message;
  `saidBefore` lines are quoted "only so you don't say them again"; `fixForOlder()` (`fixSim` bigram overlap) drops a
  `<<FIX>>` that clearly belongs to an older student message.
- **No stutter, no crashes on calls** (v2026.10.14-7, owner: "don't need him to stutter or bug, the AI to work better when
  speaking and not crash"): `sayChunkOnce` counts a line as started when `synth.speaking` is true (iOS fires "start"
  late; cancelling and re-saying it stuttered); `warmWebEn(segs)` (from `speakQuest`) pre-fetches the online English
  clips (`webEnChunks`, no-cors cache warm-up); `apiRequest` retries twice by itself on a dropped connection or
  429/5xx/529; a call that still fails shows "🔁 Try again" (`UI.vretry`, `ACT.vRetry` removes the failed attempt and
  resends the same words).
- **No "server is slow" pop-ups** (v2026.10.14-8, owner: "I always get Ryusei free server is slow, fix it"): the slow/paused/
  failed Ryusei toasts are gone (voice log only). Instead `questSlowSeen` shows a "🔑 Make Ryusei faster (free)" button on
  the call screen (only without a key), also in Me → Voice; it opens `questKeySheet()` (steps + link to su-shiki.com/api +
  paste box, `ACT.saveQuestKey2` saves the key, clears the pause; it's in the click router's keep-sheet-open list).
- **Reliability**: `apiRequest` gives up after 60 s (AbortController) so Yuki can't hang on "thinking";
  auto-update never reloads during a lesson, flashcards or an open sheet (`canReloadNow`); call captions use
  `captionText()` (markdown removed, bullets kept); spoken answers with kanji still tick course words.

## Look (v3, 2026.10.09) — Duolingo-style
- Theme `S.settings.theme` = "light" (default, "washi": warm paper white #faf7f2, sakura #ec5f87, indigo-blue #3487dc,
  matcha #4fae42, yuzu #e9a120) / "dark" / "auto" (follows the iPhone), picked in Me → App & data → 🎨 Look (`ACT.setTheme`).
  `applyTheme()` toggles `html.light`; a tiny `<script id="themeBoot">` in `<head>` sets it before first paint. The update
  check compares `script:not([id])`, so keep the main `<script>` without an id. In light mode a sakura band sits behind the
  status bar (the status-bar style is black-translucent = white clock). The call screen (`#voice`) stays dark in both themes.
- Font: Nunito from Google Fonts (falls back to the system font offline); headings weight 900, body 600.
- CSS blocks at the end of `<style>`: "Look v2" (grouped lists), then "Look v3" (both themes: chunky buttons with a pressable
  bottom "lip", 2px outlines with a 4px bottom edge on lists/tiles/options/cards, thick shiny progress bars, round 3D path
  bubbles coloured by unit, solid unit banners, flat bottom bar with the open tab outlined in blue), then "Light theme".
  Unit colours go through `ucol()` (`UCOL_L`, deeper versions so white text reads). `.sec` = bold sentence-case headings.
- Pages use `.sec` category headings: Practice (Today / Quick practice / decks…), Me (You / Yuki / App).

## Technical notes
- State object `S` (currently `v:31`) saved to localStorage key `yuki-sensei-v3`. Keep it backward
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
- Explain changes to the owner in plain language, in 1–2 short sentences max (owner: "I don't read long messages; just tell me what to do and how, super short and simple"). They're learning, not a developer.

## Ideas for next versions
- Kanji stroke-order practice
- More vocab and kanji decks for N4 and up
- Daily study reminders or goals
- Streak rewards
