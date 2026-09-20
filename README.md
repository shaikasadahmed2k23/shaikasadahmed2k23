<div align="center">

<h1>Hi, I'm Asad.</h1>
<h3>I build AI agents that run on their own — and I keep pushing them to production.</h3>

</div>

<br/>

Most of what's below isn't a plan or a portfolio piece — it's stuff that's live right now, doing its job without me watching it. A veterinary voice agent answering real calls. An inbox that classifies itself. A prayer reminder that checks in on you and actually knows what to say if you missed one. I like the part of AI engineering where the system stops needing you.

I'm a final-year CS (AI) student from Kurnool, India — currently building an AI healthcare chatbot as an intern, and shipping one weekend project after another because that's genuinely how I learn fastest.

<br/>

<!--LIVE-STATUS-START-->
### 🟢 Right now

> *Loading latest activity...*
<!--LIVE-STATUS-END-->

*(This block updates itself daily via GitHub Actions — see [`.github/workflows/live-status.yml`](.github/workflows/live-status.yml))*

<br/>

## What I actually work on

I connect three things most people keep separate: **LLM reasoning**, **real-time systems** (voice, webhooks, live data), and **backend infra** that doesn't fall over. The projects below are picked because each one solves a real, specific problem — not because they demo well.

<br/>

---

### 🐾 Dr. Paws — a vet clinic's after-hours triage problem

**Problem:** Emergency vet calls at 2 AM were going unanswered, or triaged by whoever picked up — no consistency, no urgency detection.

**What I built:** A real-time voice agent (LiveKit + Groq LLaMA 3.3-70B + ElevenLabs) that listens, reasons about symptom severity, and can switch mid-conversation between "this is an emergency" and "let's just book a slot" — then books it live via n8n + Supabase.

**Result:** Sub-2-second speech-to-response latency, validated across 6 real clinical scenarios spanning cats, dogs, birds, and street animals.

---

### 📧 Smart Email Agent — inbox triage nobody wants to do manually

**Problem:** Unsubscribing, sorting, and flagging calendar-relevant emails eats time every single day, and rules-based filters miss context.

**What I built:** A 5-node autonomous pipeline — Gmail polling → LLM classification → priority routing → calendar detection → Sheets memory. It even detects spam unsubscribe links and triggers browser automation on its own.

**Result:** ~70% reduction in inbox noise, zero manual action required after setup.

---

### 🕌 Salah Reminder Agent — where reminders actually help instead of nagging

**Problem:** Most prayer reminder apps are just alarms. They don't know *you* missed one, and they definitely don't respond to it.

**What I built:** A Telegram-based agent that reminds 15 minutes before each Salah, and if one's missed, pulls a relevant hadith from Supabase and generates a context-aware, non-preachy nudge via Claude API — running an A/B setup against Groq to compare tone.

**Result:** Full-stack, self-serve onboarding (React + Tailwind), live and in daily use.

---

### 🍽️ Spice Garden — replacing a restaurant's broken paper-menu workflow

**Problem:** A real restaurant was losing orders to messy paper menus and dead-end static QR codes — ten distinct failure modes, all preventable.

**What I built:** A 4-tier ordering system — CDN frontend, Postgres, n8n automation, dual LLM inference for dish Q&A with neural voice descriptions.

**Result:** Live in production at a real restaurant, running at ~$65/month.

---

### 🤖 DevCrew — six agents that build projects from a plain-English idea

**Problem:** Turning "I have an idea" into a working scaffolded project takes hours of boilerplate most people never get past.

**What I built:** A 6-agent CrewAI pipeline — Goal Analyst → Tech Advisor → Planner → Coder → Tester → QA — that ships a ready-to-run ZIP with README and `.env.example`. The Tech Advisor agent will honestly tell you *not* to use CrewAI if a simpler stack fits better.

**Result:** Built in a weekend, runs at zero cost (solved Groq's 6,000 TPM rate-limit wall via per-agent isolation).

<br/>

---

<br/>

## How I build

`Python · FastAPI · LangChain / CrewAI · Groq / Claude / Gemini APIs · Supabase / ChromaDB · React / Next.js · n8n · LiveKit`

Core languages: Java, Python, JavaScript, SQL — and enough DSA to know exactly where I still need to get faster.

<br/>

## Talk to me about

Agentic systems · RAG pipelines that actually reduce hallucination · Real-time voice agents · Backend architecture for AI products

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-connect-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shaik-asad-ahmed-224b9b2a8/)
[![GitHub](https://img.shields.io/badge/GitHub-explore-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/shaikasadahmed2k23)
[![Email](https://img.shields.io/badge/Email-say_hi-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:shaikasadahmed22@gmail.com)

*Open to AI Engineering · Agentic Systems · Backend roles*

</div>
