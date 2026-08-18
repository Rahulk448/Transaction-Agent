# Discussion Record

## Discussion 1 — Transaction Threshold

**Platform:** Reddit  
**Community:** r/learnmachinelearning

### My Question

> transaction agent thinking
>
> I am building an AI agent for transactions which performs actions like approve / hold or question / stop, so I want feedback on:
>
> **If your bank/payment system flags a payment as suspicious, which would you prefer?**
>
> A) Block it immediately  
> B) Let me confirm/verify it before blocking  
> C) Something else — explain

### Their Response

> I wouldn't use one fixed threshold. In transaction systems, the score is far less important than the cost of wrong transactions themselves. A $10 purchase and a $100k transfer shouldn't be treated the same. I'd start with a risk score + dynamic thresholds, then tune them based on real false positive/false negative data. you cannot afford any wrong transactions etc here.

### What I Understood

I understood that the agent should not necessarily use one fixed threshold for every transaction. The amount and the cost of making the wrong decision could affect how strict the agent should be.

---

## Discussion 2 — Software Design Perspective

**Platform:** Reddit  
**Community:** r/AskProgramming

### My Question

> transaction agent thinking
>
> I am building an AI agent for transactions which performs actions like approve / hold or question / stop, so I want feedback on:
>
> **From a software-design perspective, would you let an automated transaction system make a final decision when its confidence is low, or would you design a separate human-review state?**

### Their Response

> I'd absolutely design a separate human-review state.
>
> Low confidence should be a first-class state, not something you collapse into approve/deny. For transactions, I'd rather have:
>
> **APPROVE → HOLD_FOR_REVIEW → STOP**
>
> with the transition into review triggered by uncertainty, policy conflicts, or missing evidence.
>
> The important part is not just the confidence score, but why confidence is low and whether the decision is reversible.
>
> I'm building something adjacent with MARGINAL: [GitHub link from the original Reddit response]
>
> Different domain, but the principle is similar: observe first, collect evidence, and only earn stronger enforcement when the system has enough proof. Weak evidence should fail open or escalate, not silently become an irreversible decision.
>
> If you want, fork MARGINAL and adapt the evidence / decision-gating model to transaction actions. I'd be interested to see how that maps to financial approval flows.

### What I Understood

I understood that `HOLD_FOR_REVIEW` should be an actual state of the agent, rather than simply treating low confidence as approve or stop. If the evidence is weak, missing, or conflicting, the agent can hold the transaction and ask for human review instead of making an irreversible decision.

---

## Other Reddit Posts

I also posted the transaction-agent question in other relevant communities, but these posts did not receive a response at the time of recording.

I will add the actual thread links here as they become available.
