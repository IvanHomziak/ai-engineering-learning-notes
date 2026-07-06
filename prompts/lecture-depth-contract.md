# Lecture Depth Contract

This contract defines the minimum educational depth required for every generated
technical lecture. It complements `prompts/master-learning-prompt.md`.

## 1. Core outcome

A lecture must be self-contained for its declared scope.

After reading it, a Senior Java Engineer who is new to the specific technology
must be able to:

- explain the central concepts in their own words;
- describe the internal execution flow;
- understand the important data types and component boundaries;
- implement or adapt the worked example;
- identify limitations, alternatives, failure modes, and production risks;
- answer the interview questions without searching for foundational explanations.

External documentation may still be needed for exact version-specific API
signatures, but not for understanding the core topic.

## 2. Atomic scope gate

A lecture must have one central topic and normally no more than three primary
concepts that each require independent internal-mechanics explanations.

Split the lecture when:

- several technologies have independent lifecycles or runtimes;
- each major component could support its own execution-flow diagram;
- the title contains multiple independent products joined by commas or `and`;
- explaining one component requires skipping the mechanics of another;
- the result would become an ecosystem glossary rather than a teachable module.

An overview lecture may mention many components, but it must clearly distinguish:

- primary concepts explained deeply;
- secondary concepts introduced only as navigation context;
- concepts deferred to later lectures.

Do not claim full coverage for a concept that is only introduced.

## 3. Concept explanation contract

For every primary concept, include all applicable elements:

1. precise definition;
2. problem it solves;
3. why simpler alternatives may be insufficient;
4. internal mechanics;
5. lifecycle or execution sequence;
6. important inputs and outputs;
7. concrete worked example;
8. limitations and invalid assumptions;
9. alternatives and trade-offs;
10. production failure modes;
11. testing and observability implications.

A one-row table entry is never sufficient for a primary concept. Tables may
summarize the explanation after the narrative section.

## 4. Execution-flow contract

The lecture must trace the important operation end to end.

Include, where relevant:

- initiating actor;
- application entry point;
- concrete input type and representative value;
- transformations between components;
- provider or framework boundary;
- validation points;
- side effects;
- output type;
- error propagation;
- retry, recovery, or compensation behavior.

Use concrete flows such as:

```text
input dict
-> prompt value
-> message list
-> provider request
-> provider response
-> framework message
-> parser
-> application result
```

Do not replace an execution flow with generic statements such as “the model is
called” or “the framework handles it”.

## 5. Code explanation contract

When code is assigned or added:

- explain the responsibility of every important class, function, or module;
- explain important imports and framework abstractions when they are not obvious;
- state input and output types;
- explain the order of calls;
- explain framework-generated or overloaded behavior;
- explain sync, async, stream, and batch implications when relevant;
- explain error paths and resource cleanup;
- show how to test the code;
- distinguish demo simplifications from production requirements.

For a central code example, provide a line-group walkthrough rather than only a
single paragraph after the code.

When no lecturer code is assigned, create a coherent supplementary example that
is large enough to demonstrate the lecture topic, and label it as additional
material.

## 6. Depth heuristics

Word count is a warning signal, not the quality goal.

Recommended ranges:

- focused conceptual lecture: 3,000–5,000 words;
- code-heavy lecture: 4,000–7,000 words;
- architecture-heavy lecture: 4,000–8,000 words.

A lecture below 2,500 words must explain in `generation-report.md` why its scope
is still complete. A lecture with twenty or more required sections and fewer
than 2,000 words normally fails the depth check.

Recommended narrative depth:

- each primary concept: usually 300–800 words;
- end-to-end execution flow: usually at least 300 words plus a diagram when useful;
- central code walkthrough: usually at least 600 words when code exists;
- failure modes: each important failure includes cause, symptom, impact,
  detection, mitigation, and recovery;
- security, observability, and testing sections include concrete mechanisms, not
  only lists of terms.

Do not add filler to satisfy these ranges. Split or narrow the scope when depth
would require excessive length.

## 7. Self-containment test

Before review, answer these questions:

- Are all terms required to understand the central topic defined?
- Is the internal mechanism explained rather than named?
- Can the reader follow data from input to output?
- Can the reader understand the example without consulting another tutorial?
- Are important constraints and alternatives explained?
- Are production recommendations connected to concrete failure modes?
- Are deferred concepts explicitly identified?

Any `no` answer must be corrected or documented as a blocking limitation.

## 8. Production-depth test

Production sections must explain mechanisms.

Examples:

- Security: trust boundaries, authorization point, secret handling, data
  redaction, tenant isolation, injection or tool-call controls.
- Observability: instrumentation location, metric meaning, useful attributes,
  cardinality risks, trace correlation, alerts, and debugging workflow.
- Testing: test level, system under test, dependency strategy, assertions,
  failure paths, and flakiness control.
- Reliability: timeout budget, retry conditions, idempotency, fallback,
  degradation, and recovery.

A checklist without these explanations is insufficient.

## 9. Source and verification contract

- Cover every assigned transcript range or explain the omission.
- Use assigned code and configuration where relevant.
- Correct transcript errors explicitly.
- Verify version-sensitive claims with official sources when access exists.
- Do not invent citations or imply verification that did not occur.
- Clearly mark supplementary explanations not present in the source material.

## 10. Quality thresholds

A lecture may pass only when:

- technical correctness is at least 16/20;
- explanation depth is at least 16/20;
- self-containment is at least 12/15;
- source coverage is at least 12/15;
- code explanation is at least 8/10 when code is applicable;
- production value is at least 8/10;
- structure and readability are at least 4/5;
- traceability and verification are at least 4/5;
- total score is at least 85/100;
- no critical factual, security, or source-coverage defect remains.

A structurally complete but shallow lecture must receive `QUALITY_FAILED`.
