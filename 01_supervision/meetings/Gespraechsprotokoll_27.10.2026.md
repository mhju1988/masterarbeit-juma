# Supervision meeting — 27 October 2026

**Participants:** Prof. Dr. Katja Zeume (supervisor, first examiner), Mohamad Juma
**Format:** Zoom, ca. 30 minutes
**Purpose (hers):** *"talk a bit about the topic and an up-to-date focus again"*
**Record:** reconstructed from a transcript of the call. The student's audio was not captured for
roughly the first ten minutes, during which the presentation was given, so the opening is recorded
from the slides and the prepared script rather than from the transcript.

**Basis of the discussion:** `2026-10-27_PROGRESS_REPORT.md` and the 12-slide deck covering the BIRD
Mini-Dev structural pass, the Spider pilot and the counterexample tests.

---

## 1. Overall assessment

Positive, and the topic is not at risk.

> *"The pre-research sounds very good, sounds interesting."*

> *"I'm fairly satisfied with the status of the work."*

> *"In the exposé we have still a lot of questions that you can work on when you start. So that's
> also fine."*

No change of direction was requested. The work remains as approved in August.

---

## 2. Answers to the six questions

The questions were answered briefly in the call. She offered to answer them more fully in writing:

> *"You can also send me the questions if you want an answer. I mean, I only briefly answered them."*

### Q1 — Does a flat, SQL-92-shaped baseline change what we should expect to find?

**Answered: yes.**

> *"If it doesn't change what it shows, then it's a strange baseline. I think so. I think the answer
> to one is yes."*

### Q2 — Is splitting the two variants sound? (SQLite for operators, PostgreSQL for execution)

**Approved.**

> *"I think two is fair enough, because of like availability for systems. So that's also fine."*

Her reasoning was system availability — the split is justified by what each system supports, not
treated as a compromise.

### Q3 — Is schema-driven non-sargability a result in its own right, or a confound?

**A result in its own right, and worth researching.**

> *"I think that you could research. I mean, that's a research question. Three is a research
> question."*

### Q4 — Does the porting result make the working-SQL corpora more urgent?

**Not answered.** The phrasing did not carry:

> *"Which porting result? Which one here? … I'm a little bit confused of this question here."*

She asked for clearer formulation of such questions in future. This one is **still open** and should
be re-asked in writing, naming the finding explicitly rather than calling it "the porting result".

### Q5 and Q6 — The extension paths, and new literature

> *"For four to six, that's also what I had in mind."*

**The extensions stay open — confirmed for the third time.**

> *"We did not officially start it yet. I think for this kind of topic, actually, a lot changes in
> very little time. So I think it's good that we have still some open extension possibilities."*

> *"The other ones are also still, I think, valid enough."*

---

## 3. New: a fourth extension path — SQL that calls an LLM

Raised by Prof. Zeume, unprompted. This is the only genuinely new item from the meeting.

> *"I also read about, because you mentioned Snowflake, that they also have published some AI
> operators, which I think is interesting maybe also for this work, because then it's like SQL can
> also use an LLM call. So, is this used by an LLM or by a human or differently? So I think that
> would also be a nice extension."*

The question she poses: when SQL itself gains operators that invoke a language model, **do models
and people reach for them differently?**

This sits naturally inside the existing focus rather than beside it — it is the evolution of the
query language, observed as it happens. It joins the list of open extensions; it does not replace
any of them, and nothing was committed.

**To do:** verify what these operators actually are before building anything on the idea. Nothing
about them has been checked yet.

---

## 4. Keeping up with the literature is the student's job

A clear instruction, repeated.

> *"Now that you've started your research, you should also keep track whether there is something
> that has appeared since August. I don't have a news feed for exactly this kind of question."*

> *"You are now much more focused on this topic than I am."*

And on what to do if something relevant appears late:

> *"Of course it's not optimal if some study is published two weeks before you hand in your master's
> thesis which would exactly solve all the problems you have. But honestly, if this happens, then I
> think you should react to this, because it shows that you work on a very active topic, which is
> very relevant."*

Using AI tooling to do that monitoring was proposed by the student and endorsed:

> *"Yeah, of course. You should do this."*

### What the thesis is for

Stated explicitly, and worth recording because it sets the standard for the Kolloquium:

> *"After your master's thesis you should have the competency to start working on a problem and then
> after six months you are an expert on the current status of this problem."*

> *"We also always said: not producing a piece of paper any more, but being an expert in your topic
> and being able to defend it after the six months."*

---

## 5. Registration and the signature

**Resolved.** The August signature does not need renewing.

> *"If you send this and you put me in CC and you say that you have spoken to me and it's still
> fine, then I think it's fine. … It's transparent because I'm in CC, so I could say no."*

**Procedure agreed:** submit the application to the Prüfungsamt, **with Prof. Zeume in CC**, stating
that the matter was discussed with her and that her signature stands.

She is comfortable with the official start following the credit points:

> *"I'm really comfortable when you start this officially after you have the [credits]."*

### Second examiner — still open

Prof. Gleim was mentioned, and there was an exchange about an earlier confusion over the name. The
transcript does not attribute the speakers reliably at that point, and **no confirmation that Prof.
Gleim will act as second examiner was recorded.** Treat this as unresolved and settle it in writing.

---

## 6. Agreed next steps

| # | Action | Owner |
|---|---|---|
| 1 | Send this protocol to Prof. Zeume; she will return comments if anything needs correcting | Student |
| 2 | Re-send the six questions in writing, Q4 reformulated, for fuller answers | Student |
| 3 | Submit the Antrag to the Prüfungsamt with Prof. Zeume in CC, noting the signature was discussed | Student |
| 4 | Settle the second examiner in writing | Student |
| 5 | Set up the repository of protocols and correspondence, and send her the link with instructions | Student |
| 6 | Monitor the literature continuously; react to anything relevant, however late it appears | Student |
| 7 | Check what Snowflake's AI operators are, as a candidate extension | Student |

Her side:

> *"You can also send some kind of protocol. Maybe that's easier. And if there's something I need to
> correct, then I would return some comments."*

---

## 7. Future meetings

In-person meetings at her office are welcome, but must be arranged beforehand:

> *"We only have to talk about it, because sometimes I only make these meetings and then I see I'm
> not there."*

Agreed: send a message before any in-person meeting to confirm she will be there.

---

## 8. What did not come up

- The BIRD-versus-Spider decision for the paired experiment was **not** discussed. The student's
  question 4b did not get through in the form it was asked. Still open.
- No preference was expressed among the extension paths — consistent with August.
- No deadline, milestone or interim deliverable was set.

---

## Note on this record

Speaker attribution in the underlying transcript is unreliable in places, particularly around the
second-examiner exchange. Quotations above are from Prof. Zeume where the attribution is clear from
context. Anything uncertain is marked as such rather than resolved by guesswork.

---

## Addendum — 21.11.2026

Two points recorded above as open have since been resolved, and this protocol is left otherwise
unchanged as the record of what was said on the day.

- **Second examiner: Prof. Dr. Gleim, confirmed.** He agreed and signed the Antrag. Section 5 above
  records this as unresolved because the transcript's speaker attribution was unreliable at that
  point; the attribution was the problem, not the fact.
- **Registration is complete.** The module exam of 05.10.2026 was passed, completing the 78 CP, and
  the application was accepted in November 2026 — submitted with both examiners in copy and with the
  August signature accepted without renewal, exactly as agreed in §5.

Still outstanding from §6: the protocol itself has not yet been sent to her, the six questions have
not been re-sent in writing, and she has not been given the repository link.
