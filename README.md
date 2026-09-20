<div align="center">

# Shaik Asad Ahmed

**I don't build demos. I build things that stay up after the hackathon ends.**

Final-year AI engineer · Kurnool, India · 28+ shipped projects · Solo hackathon builder

[Email](mailto:shaikasadahmed22@gmail.com) · [LinkedIn](https://www.linkedin.com/in/shaik-asad-ahmed-224b9b2a8/) · [GitHub](https://github.com/shaikasadahmed2k23) · [LeetCode](https://leetcode.com/Shaik_Asad)

</div>

<br/>

```
$ whoami
> B.Tech CSE (AI), GPCET Kurnool — GPA 8.5/10, Class of 2026
> AI Application Developer @ HandiCrafts — shipping a RAG healthcare chatbot
> Trained under Innovexa Catalyst Industrial Program, Batch 2026
> Weekends: hackathons. Solo. No team to hide behind, no excuses either.
```

## Why I build this way

Most people ship a chatbot and call it "AI." I care about the boring parts that make
a system trustworthy in production: latency under load, graceful failure, cost per
request, and whether it still works at 2am when nobody's watching it. If a project
of mine is live, it's because I stress-tested it — not because a demo video looked good.

<br/>

## Selected builds

Not a link dump. Here's what each one actually had to solve.

<table>
<tr>
<td width="50%" valign="top">

**🐾 Dr. Paws**
*Real-time veterinary voice agent*

Sub-2s speech-to-response over LiveKit + Groq Llama 3.3-70B. Handles
mid-conversation context switches between emergency triage and appointment
scheduling — validated across 6 clinical scenarios spanning cats, dogs,
birds, and street animals. Async tool-calling books real slots in Supabase.

`LiveKit` `Groq` `ElevenLabs` `Supabase` `n8n`

</td>
<td width="50%" valign="top">

**🕌 Islamic Guidance RAG**
*Live at [islamic-rag-one.vercel.app](https://islamic-rag-one.vercel.app)*

101,502 chunks indexed in ChromaDB with HuggingFace embeddings, serving
grounded answers with source attribution instead of confident hallucination.
Built because most "Islamic AI" projects skip the part where wrong answers
about religion actually matter.

`ChromaDB` `HuggingFace` `RAG`

</td>
</tr>
<tr>
<td width="50%" valign="top">

**🤖 DevCrew**
*6-agent pipeline that ships full projects from a sentence*

Goal Analyst → Tech Advisor → Planner → Coder → Tester → QA, fully
sequential. The Tech Advisor agent will talk you *out* of using CrewAI
(its own stack) when something simpler fits — because a recommendation
engine that never disagrees with itself isn't one you can trust. Solved
Groq's 6,000 TPM rate limit across 6 concurrent agents via per-agent
crew isolation.

`CrewAI` `FastAPI` `Next.js` `Groq`

</td>
<td width="50%" valign="top">

**📧 Smart Email Agent**
*Autonomous inbox triage, zero human in the loop*

5-node swarm: polls Gmail → classifies → routes by priority → detects
calendar intent → logs to Sheets for memory. Cuts ~70% of inbox noise
without the user lifting a finger, including auto-triggering unsubscribe
flows when it spots spam patterns.

`n8n` `Groq` `Gmail API` `Google Sheets`

</td>
</tr>
</table>

<br/>

## Hackathon track record

I compete solo — no split credit, no hiding behind a teammate's code.

| Event | Result |
|---|---|
| HackerRank RecNet Orchestrate | **211 / 1,700** |
| HiDevs Black Protocol Challenge | **4th place** |
| Gridlock Hackathon (traffic ML) | 6-model ensemble, best score **78.05** |
| Unisys Innovation Challenge 2025 | Pre-finalist |
| Agentathon 2025 (GDG Hyderabad) | Participant — Guinness World Record–holding largest agentic AI hackathon |

Currently mid-flight on **MethaneGuard AI**, **magicpin's Vera AI Challenge**, and an
**Outbox Labs / ReachInbox.ai** production scheduler assignment — dataset, backend, and
API work don't stop just because there's a README to write.

<br/>

## Stack I actually reach for

**AI/LLM** — LangChain · CrewAI · Groq · OpenAI · Claude API · Gemini · RAG (ChromaDB/Qdrant/Pinecone)
**Backend** — FastAPI · Flask · Node.js/Express · PostgreSQL · Supabase · MongoDB
**Automation** — n8n · LiveKit
**Frontend** — React · Next.js · Tailwind CSS
**Tooling** — Docker · Git · JWT

<br/>

## What's next

Wrapping final year with a published paper on real-time wildfire detection
(96.3% accuracy, 0.8s inference) and looking for AI engineering / agentic
systems roles where "it works on my machine" isn't the bar.

<div align="center">

<br/>

*If it's not deployed, it's not done.*

</div>
