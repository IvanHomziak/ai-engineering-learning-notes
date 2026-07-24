# Udemy AI Transition Audit

_Audit date: 2026-07-24. Target roles: AI Platform Engineer / LLM Infrastructure Engineer._

## 1. Executive Summary

The audit found **106 unique courses** across all 9 pages of Udemy **All courses**. Udemy reports **11 completed**, **51 in progress**, **44 not started**, and **0 archived** courses. **0 certificates were independently confirmed**: the library exposes completion percentages, while the Certifications tab shows third-party badges rather than per-course completion certificates. Therefore every 100% entry is explicitly treated as **“Udemy says completed; certificate not confirmed; actual mastery cannot be confirmed.”**

There are **13 highly relevant AI courses** by verified syllabus and **29 courses recommended to skip**. Decisions are distributed as: A. Complete now: 13; B. Use selectively: 26; C. Reference only: 28; D. Skip: 29; E. Already provides sufficient foundation: 10.

The strongest conclusion is that the transition is **technically credible but not yet complete**. The existing Java/Spring/Kafka/microservices/testing/CI/CD base maps unusually well to AI platform work: service boundaries, gateways, resilience, event processing, deployment and operational debugging all transfer. The missing layer is not generic software engineering; it is production LLM specialization—evaluation, guarded tool use, model routing, AI observability semantics, token/cost governance, secure RAG and lifecycle operations.

Current readiness assessment:

- **AI Platform Engineer:** strongest long-term fit; roughly medium readiness because the platform foundation is strong but AI-specific control planes remain incomplete.
- **AI Application Engineer:** fastest near-term entry; several practical LangChain, FastAPI and Spring AI courses can close the gap quickly.
- **LLM Infrastructure Engineer:** credible next step after completing RAG/evaluation/observability/routing work.
- **MLOps Engineer:** weaker fit today because the library lacks model registries, experiment tracking, serving and data/feature lifecycle depth.
- **ML Engineer:** weakest fit today; mathematical ML/DL/transformer foundations are incomplete.

## 2. Data Collection Limitations

- Work was performed read-only in the authorized Chrome Udemy session. No course, lecture, rating, review, archive state, list, cart or account setting was changed.
- All nine pagination pages were inspected. The Udemy result counter reported 106 courses and 106 unique course IDs were captured; no duplicate IDs were found.
- Archived and My Lists were empty. The Certifications tab reported 0 uploaded badges; it is not a per-course certificate inventory.
- Course progress is a platform fact, not proof of retention, hands-on completion or current mastery.
- Certificate links were not exposed in the library. Player/dashboard pages were not opened solely to hunt for certificates because doing so could start content or affect learning state. Consequently certificate status is **Unknown**, not false.
- 104 public landing pages exposed structured metadata and syllabus. Two courses—**Learn Redis And Use Jedis With Spring Data Redis** and **Python Basics**—redirected to unavailable draft pages; their assessments are Low confidence.
- Dates, durations, captions and syllabi reflect what Udemy displayed on 2026-07-24 and may change later.
- Scores are independent syllabus-based assessments. Udemy popularity and star ratings were not used as substitutes for technical depth.
- “Completed” always means “Udemy says 100%”; actual mastery cannot be confirmed.

## 3. Course Inventory

Score order: **Content quality / Technical depth / Practical value / AI Platform relevance / LLM Infrastructure relevance / AI Application relevance / Java-backend transferability / Currency in 2026**.

| # | Course | Status | Progress | Updated | Duration | CQ/TD/PV/AP/LI/AA/JB/CY | Decision | Confidence |
|---:|---|---|---:|---|---:|---|---|---|
| 1 | [Claude Code Bootcamp: Hooks, MCP & Agentic AI Workflows](https://www.udemy.com/course/claude-code-bootcamp) | in progress | 38% | 2026-07 | 10h 44m | 9/8/8/8/8/7/5/10 | A. Complete now | High |
| 2 | [Production AI Agents with LangChain + LangGraph \[2026\]](https://www.udemy.com/course/production-ai-agents) | in progress | 13% | 2026-05 | 17h 6m | 9/9/9/10/10/10/5/10 | A. Complete now | High |
| 3 | [AI Engineer Core Track: LLM Engineering, RAG, QLoRA, Agents](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models) | in progress | 5% | 2026-06 | 33h 27m | 9/8/9/8/9/10/4/10 | A. Complete now | High |
| 4 | [LangChain- Agentic AI Engineering with LangChain & LangGraph](https://www.udemy.com/course/langchain) | in progress | 63% | 2026-07 | 19h 43m | 9/9/9/8/9/10/4/10 | A. Complete now | High |
| 5 | [100 Days of Code™: The Complete Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code) | in progress | 36% | 2026-06 | 56h 48m | 9/7/9/5/4/5/5/10 | B. Use selectively | High |
| 6 | [Java Interview Questions Boot Camp - 1000+ Q& A Master Class](https://www.udemy.com/course/java-interview-questions-bootcamp-master-class-1000-java-questions) | in progress | 1% | 2025-07 | 24h 50m | 3/3/3/3/1/2/9/8 | D. Skip | High |
| 7 | [FastAPI - The Complete Course 2026 (Beginner + Advanced)](https://www.udemy.com/course/fastapi-the-complete-course) | in progress | 90% | 2026-05 | 21h 28m | 8/8/9/7/7/8/5/10 | A. Complete now | High |
| 8 | [Python - Полный Курс по Python, Django, Data Science и ML](https://www.udemy.com/course/python-ru) | in progress | 53% | 2026-03 | 45h 28m | 7/6/7/5/4/5/4/9 | B. Use selectively | High |
| 9 | [Искусственный интеллект и Машинное обучение + Основы Python](https://www.udemy.com/course/ai-machinelearning-ru) | completed | 100% | 2024-10 | 3h 19m | 5/3/5/3/2/4/2/6 | E. Already provides sufficient foundation | High |
| 10 | [\[NEW\] Master Microservices with SpringBoot,Docker,Kubernetes](https://www.udemy.com/course/master-microservices-with-spring-docker-kubernetes) | in progress | 71% | 2026-02 | 40h 24m | 9/8/9/8/6/4/10/9 | A. Complete now | High |
| 11 | [From Java Dev to AI Engineer: Spring AI Fast Track](https://www.udemy.com/course/java-spring-ai) | in progress | 8% | 2026-07 | 17h 49m | 9/8/9/10/9/9/10/10 | A. Complete now | High |
| 12 | [The Complete Oracle SQL Bootcamp (2026)](https://www.udemy.com/course/oracle-sql-12c-become-an-sql-developer-with-subtitle) | not started | 0% | 2026-02 | 37h 57m | 9/7/7/3/1/2/7/9 | C. Reference only | High |
| 13 | [Spring Security with ReactJS, OAuth2, JWT, MFA \| Spring Boot](https://www.udemy.com/course/spring-security-6-with-reactjs-oauth2-jwt-multifactor-authentication) | completed | 100% | 2026-03 | 34h 51m | 9/8/8/5/4/2/9/9 | E. Already provides sufficient foundation | High |
| 14 | [Kafka MicroServices with Spring Boot, Docker, Kubernetes, AI](https://www.udemy.com/course/apache-kafka-for-developers-using-springboot) | in progress | 36% | 2026-06 | 27h 10m | 8/8/9/7/5/4/10/10 | B. Use selectively | High |
| 15 | [The AI Engineer Course 2026: Complete AI Engineer Bootcamp](https://www.udemy.com/course/the-ai-engineer-course-complete-ai-engineer-bootcamp) | not started | 0% | 2026-05 | 29h 42m | 8/7/8/6/7/8/4/10 | B. Use selectively | High |
| 16 | [Master statistics & machine learning: intuition, math, code](https://www.udemy.com/course/statsml_x) | not started | 0% | 2026-06 | 38h 20m | 9/9/8/6/5/5/4/10 | A. Complete now | High |
| 17 | [Apache Kafka for Event-Driven Spring Boot Microservices](https://www.udemy.com/course/apache-kafka-for-spring-boot-microservices) | completed | 100% | 2026-06 | 14h 15m | 9/5/7/5/4/2/9/10 | E. Already provides sufficient foundation | High |
| 18 | [Spring Boot Microservices and Spring Cloud. Build & Deploy.](https://www.udemy.com/course/spring-boot-microservices-and-spring-cloud) | in progress | 77% | 2026-06 | 25h 47m | 9/8/8/5/4/2/9/9 | B. Use selectively | High |
| 19 | [Selenium WebDriver with Java -Basics to Advanced+Frameworks](https://www.udemy.com/course/selenium-real-time-examplesinterview-questions) | in progress | 46% | 2026-07 | 56h 4m | 9/8/8/5/4/2/9/10 | C. Reference only | High |
| 20 | [Playwright JS/TS Automation Testing from Scratch & Framework](https://www.udemy.com/course/playwright-tutorials-automation-testing) | in progress | 88% | 2026-05 | 25h 9m | 9/7/7/8/6/8/9/9 | B. Use selectively | High |
| 21 | [Cypress -Modern Automation Testing from Scratch + Frameworks](https://www.udemy.com/course/cypress-tutorial) | in progress | 15% | 2026-03 | 20h 18m | 9/7/8/8/5/7/9/9 | D. Skip | High |
| 22 | [Automated Software Testing with Cypress](https://www.udemy.com/course/automated-testing-with-cypress) | in progress | 24% | 2026-06 | 11h 58m | 8/5/8/5/4/2/9/10 | D. Skip | High |
| 23 | [Spring AI - GenAI with Telusko](https://www.udemy.com/course/spring-ai-genai) | not started | 0% | 2025-11 | 5h 5m | 7/6/8/8/7/9/10/8 | B. Use selectively | High |
| 24 | [Spring Boot Unit Testing with JUnit, Mockito and MockMvc](https://www.udemy.com/course/spring-boot-unit-testing) | completed | 100% | 2026-01 | 9h 51m | 9/5/6/3/1/2/9/9 | E. Already provides sufficient foundation | High |
| 25 | [Testing Java: JUnit 5, Mockito, Testcontainers, REST Assured](https://www.udemy.com/course/testing-java-code-with-junit-5-and-mockito) | completed | 100% | 2026-06 | 10h 40m | 9/6/7/6/4/6/9/10 | E. Already provides sufficient foundation | High |
| 26 | [Hibernate](https://www.udemy.com/course/hibernate-dmdev) | in progress | 1% | 2021-11 | 13h 45m | 4/5/5/5/4/2/9/2 | D. Skip | High |
| 27 | [Computer Science 101: Master the Theory Behind Programming](https://www.udemy.com/course/computer-science-101-master-the-theory-behind-programming) | not started | 0% | 2026-05 | 11h 52m | 7/5/4/1/1/2/3/9 | C. Reference only | High |
| 28 | [Software Architecture & Design of Modern Large Scale Systems](https://www.udemy.com/course/software-architecture-design-of-modern-large-scale-systems) | completed | 100% | 2025-12 | 7h 54m | 8/4/6/6/4/6/7/8 | E. Already provides sufficient foundation | High |
| 29 | [OpenTelemetry Observability For Java Spring Boot Developers](https://www.udemy.com/course/opentelemetry-metrics-tracing-guide) | in progress | 8% | 2026-06 | 11h 24m | 9/9/9/9/8/5/10/10 | A. Complete now | High |
| 30 | [React - The Complete Guide (incl. Next.js, Redux)](https://www.udemy.com/course/react-the-complete-guide-incl-redux) | not started | 0% | 2026-01 | 71h 21m | 9/8/7/5/4/2/9/9 | D. Skip | High |
| 31 | [The Ultimate React Course 2025: React, Next.js, Redux & More](https://www.udemy.com/course/the-ultimate-react-course) | not started | 0% | 2025-05 | 83h 52m | 9/8/8/5/4/2/9/8 | D. Skip | High |
| 32 | [Docker & Kubernetes: The Complete Practical Guide](https://www.udemy.com/course/docker-complete) | not started | 0% | 2026-03 | 21h 24m | 9/6/7/5/4/2/9/9 | D. Skip | High |
| 33 | [Spring Boot 4, Spring 7 & Hibernate for Beginners](https://www.udemy.com/course/spring-hibernate-tutorial) | completed | 100% | 2026-05 | 35h 28m | 8/7/6/5/4/2/9/9 | E. Already provides sufficient foundation | High |
| 34 | [Reactive Applications with Spring WebFlux Framework](https://www.udemy.com/course/reactive-applications-with-spring-webflux-framework) | in progress | 46% | 2026-06 | 11h 27m | 9/6/7/5/4/2/9/10 | B. Use selectively | High |
| 35 | [Let's Learn Terraform in GCP](https://www.udemy.com/course/lets-learn-terraform-in-gcp) | in progress | 28% | 2024-10 | 17h 33m | 7/5/7/5/4/2/7/6 | B. Use selectively | High |
| 36 | [Understanding TypeScript](https://www.udemy.com/course/understanding-typescript) | in progress | 71% | 2026-04 | 22h 32m | 9/7/7/6/4/6/9/9 | C. Reference only | High |
| 37 | [Java Data Structures & Algorithms + LEETCODE Exercises](https://www.udemy.com/course/data-structures-and-algorithms-java) | in progress | 50% | 2026-04 | 11h 7m | 9/6/6/3/1/2/9/9 | C. Reference only | High |
| 38 | [Docker & Kubernetes: The Practical Guide](https://www.udemy.com/course/docker-kubernetes-the-practical-guide) | in progress | 6% | 2026-04 | 23h 39m | 9/5/7/5/4/2/7/9 | D. Skip | High |
| 39 | [Hibernate and Spring Data JPA: Beginner to Guru](https://www.udemy.com/course/hibernate-and-spring-data-jpa-beginner-to-guru) | not started | 0% | 2025-11 | 30h 18m | 9/7/7/3/1/2/9/8 | D. Skip | High |
| 40 | [Spring Security Zero to Master along with JWT,OAUTH2](https://www.udemy.com/course/spring-security-zero-to-master) | not started | 0% | 2026-01 | 24h 37m | 9/6/6/5/4/2/9/9 | C. Reference only | High |
| 41 | [Java Masterclass 2025: 130+ Hours of Expert Lessons](https://www.udemy.com/course/java-the-complete-java-developer-course) | in progress | 1% | 2026-05 | 135h 42m | 9/8/8/3/1/2/9/9 | D. Skip | High |
| 42 | [GCP for Beginners - Become a Google Cloud Digital Leader](https://www.udemy.com/course/google-cloud-digital-leader-certification) | in progress | 4% | 2026-06 | 15h 59m | 9/7/8/8/5/7/7/10 | B. Use selectively | High |
| 43 | [Terraform for the Absolute Beginners with Labs](https://www.udemy.com/course/terraform-for-the-absolute-beginners) | not started | 0% | 2024-11 | 4h 36m | 8/7/9/8/6/3/7/9 | A. Complete now | High |
| 44 | [Build Reactive MicroServices using Spring WebFlux/SpringBoot](https://www.udemy.com/course/build-reactive-restful-apis-using-spring-boot-webflux) | completed | 100% | 2026-02 | 8h 26m | 9/5/7/5/4/2/9/9 | E. Already provides sufficient foundation | High |
| 45 | [Java Debugging With IntelliJ IDEA](https://www.udemy.com/course/java-debugging-with-intellij-idea) | in progress | 8% | 2025-11 | 4h 40m | 8/4/6/5/4/2/9/8 | C. Reference only | High |
| 46 | [Full Stack: Angular and Java Spring Boot E-Commerce Website](https://www.udemy.com/course/full-stack-angular-spring-boot-tutorial) | in progress | 64% | 2026-01 | 25h 53m | 9/8/7/5/4/2/9/9 | D. Skip | High |
| 47 | [\[NEW\] Spring Boot 4, Spring Framework 7: Beginner to Guru](https://www.udemy.com/course/spring-framework-6-beginner-to-guru) | in progress | 47% | 2025-12 | 48h 2m | 9/8/7/8/3/5/9/8 | C. Reference only | High |
| 48 | [FULL STACK JAVA DEV: JAVA + JSP + SPRING + BOOT + JS + REACT](https://www.udemy.com/course/full-stack-java-developer-java) | completed | 100% | 2026-07 | 84h 31m | 9/8/7/3/1/2/9/10 | E. Already provides sufficient foundation | High |
| 49 | [Spring WebFlux: Microservices Patterns & Advanced Resilience](https://www.udemy.com/course/spring-webflux-patterns) | not started | 0% | 2026-06 | 8h 36m | 8/5/6/5/4/2/9/10 | B. Use selectively | High |
| 50 | [Spring WebFlux Masterclass: High-Performance Reactive APIs](https://www.udemy.com/course/spring-webflux) | not started | 0% | 2026-06 | 13h 18m | 9/5/8/8/4/6/9/10 | B. Use selectively | High |
| 51 | [Java Design Patterns & SOLID Design Principles](https://www.udemy.com/course/design-patterns-in-java-concepts-hands-on-projects) | in progress | 19% | 2025-01 | 17h 1m | 9/6/8/3/1/2/9/8 | C. Reference only | High |
| 52 | [600+ Spring Interview Questions Practice Test](https://www.udemy.com/course/spring-interview-questions) | in progress | 17% | 2026-04 | Unknown | 3/3/3/3/1/2/9/9 | D. Skip | High |
| 53 | [Java Interview Masterclass: Top 350 Questions (PDF)(2026)](https://www.udemy.com/course/top-250-java-interview-questions) | completed | 100% | 2025-12 | 13h 8m | 3/3/3/3/1/2/9/8 | D. Skip | High |
| 54 | [Angular - The Complete Guide](https://www.udemy.com/course/the-complete-guide-to-angular-2) | in progress | 15% | 2026-04 | 55h 49m | 9/8/8/3/1/2/9/9 | D. Skip | High |
| 55 | [The Git & Github Bootcamp](https://www.udemy.com/course/git-and-github-bootcamp) | not started | 0% | 2026-01 | 17h 3m | 9/5/7/1/1/2/3/9 | C. Reference only | High |
| 56 | [Spring](https://www.udemy.com/course/spring-dmdev) | in progress | 24% | 2022-08 | 21h 9m | 5/6/4/5/4/2/9/4 | D. Skip | High |
| 57 | [Spring - Полный курс. Boot, Hibernate, Security, REST.](https://www.udemy.com/course/spring-alishev) | in progress | 91% | 2022-10 | 25h 5m | 5/7/4/5/4/2/9/4 | C. Reference only | High |
| 58 | [Integration Testing with Testcontainers: Java & Spring Boot](https://www.udemy.com/course/testcontainers-integration-testing-java-spring-boot) | completed | 100% | 2025-11 | 5h 7m | 8/5/7/5/4/2/9/8 | E. Already provides sufficient foundation | High |
| 59 | [\[NEW\] Master Spring Boot Microservice & Angular K8s CICD AWS](https://www.udemy.com/course/master-spring-boot-microservice-angular-with-k8s-cicd-aws) | in progress | 98% | 2026-05 | 12h 48m | 7/8/9/8/5/3/10/9 | A. Complete now | High |
| 60 | [Design Patterns in Java](https://www.udemy.com/course/design-patterns-java) | in progress | 1% | 2020-04 | 10h 30m | 6/6/6/3/1/2/9/2 | C. Reference only | High |
| 61 | [Java Full Stack(Spring Boot, Spring AI, React, Stripe, AWS )](https://www.udemy.com/course/java-full-stack-mastery-spring-boot-react-stripe-aws) | in progress | 14% | 2025-09 | 47h 46m | 9/8/7/8/5/7/9/8 | B. Use selectively | High |
| 62 | [The Complete Full-Stack Web Development Bootcamp](https://www.udemy.com/course/the-complete-web-development-bootcamp) | in progress | 39% | 2025-11 | 61h 53m | 9/8/7/8/4/6/9/8 | D. Skip | High |
| 63 | [Master the Coding Interview: Data Structures + Algorithms](https://www.udemy.com/course/master-the-coding-interview-data-structures-algorithms) | in progress | 13% | 2026-03 | 20h 4m | 9/5/6/3/1/2/9/9 | C. Reference only | High |
| 64 | [OAuth 2.0 in Spring Boot Applications](https://www.udemy.com/course/oauth2-in-spring-boot-applications) | in progress | 2% | 2026-06 | 11h 4m | 8/6/4/8/5/7/9/10 | C. Reference only | High |
| 65 | [Event-Driven Microservices, CQRS, SAGA, Axon 4, Spring Boot](https://www.udemy.com/course/spring-boot-microservices-cqrs-saga-axon-framework) | not started | 0% | 2026-06 | 9h 31m | 9/6/5/5/4/2/9/10 | B. Use selectively | High |
| 66 | [Spring Boot Microservices with Spring Cloud Beginner to Guru](https://www.udemy.com/course/spring-boot-microservices-with-spring-cloud-beginner-to-guru) | in progress | 34% | 2025-11 | 42h 31m | 9/8/7/5/4/2/9/8 | C. Reference only | High |
| 67 | [Event-Driven Microservices: Spring Boot, Kafka and Elastic](https://www.udemy.com/course/event-driven-microservices-spring-boot-kafka-and-elasticsearch) | not started | 0% | 2026-01 | 16h 12m | 9/6/7/8/4/6/9/9 | B. Use selectively | High |
| 68 | [Deploy Java Spring Apps Online to Amazon Cloud (AWS)](https://www.udemy.com/course/deploy-java-spring-apps-online) | in progress | 44% | 2026-01 | 1h 51m | 8/3/6/5/4/2/9/9 | B. Use selectively | High |
| 69 | [Java Spring Boot Full Stack: eCommerce Project Masterclass](https://www.udemy.com/course/spring-boot-using-intellij-build-a-real-world-project) | in progress | 3% | 2026-05 | 92h 54m | 9/8/8/8/4/6/9/9 | D. Skip | High |
| 70 | [Java Multithreading, Concurrency & Performance Optimization](https://www.udemy.com/course/java-multithreading-concurrency-performance-optimization) | in progress | 13% | 2026-07 | 5h 26m | 8/5/5/3/1/2/9/10 | B. Use selectively | High |
| 71 | [Learn Redis And Use Jedis With Spring Data Redis](https://www.udemy.com/course/1701332/) | in progress | 2% | Unknown | Unknown | 2/2/3/4/3/2/7/1 | C. Reference only | Low |
| 72 | [Reactive Redis Masterclass For Java Spring Boot Developers](https://www.udemy.com/course/spring-webflux-redis) | not started | 0% | 2026-06 | 12h 21m | 8/5/7/8/4/6/9/10 | C. Reference only | High |
| 73 | [Redis: The Complete Developer's Guide](https://www.udemy.com/course/redis-the-complete-developers-guide-p) | in progress | 2% | 2026-02 | 15h 34m | 9/6/8/5/4/2/9/9 | B. Use selectively | High |
| 74 | [Apache Kafka Series - Learn Apache Kafka for Beginners v3](https://www.udemy.com/course/apache-kafka) | in progress | 17% | 2026-07 | 8h 20m | 9/5/7/5/4/2/9/10 | B. Use selectively | High |
| 75 | [Devops Fundamentals - CI/CD with AWS +Docker+Ansible+Jenkins](https://www.udemy.com/course/devops-fundamentals-aws) | in progress | 3% | 2024-12 | 8h 51m | 7/4/7/5/4/2/9/6 | D. Skip | High |
| 76 | [Docker Mastery: with Kubernetes +Swarm from a Docker Captain](https://www.udemy.com/course/docker-mastery) | not started | 0% | 2025-09 | 22h 59m | 9/7/8/8/4/6/7/8 | C. Reference only | High |
| 77 | [Appium -Mobile Testing (Android/IOS) from Scratch+Frameworks](https://www.udemy.com/course/mobile-automation-using-appiumselenium-3) | not started | 0% | 2026-03 | 26h 5m | 9/8/7/5/4/2/9/9 | D. Skip | High |
| 78 | [Learn Cucumber BDD with Java -MasterClass Selenium Framework](https://www.udemy.com/course/cucumber-tutorial) | not started | 0% | 2026-03 | 12h 10m | 9/5/8/5/4/2/9/9 | D. Skip | High |
| 79 | [Complete Linux Training Course to Get Your Dream IT Job 2026](https://www.udemy.com/course/complete-linux-training-course-to-get-your-dream-it-job) | in progress | 51% | 2026-05 | 42h 34m | 8/8/8/8/5/2/8/10 | A. Complete now | High |
| 80 | [Understanding NPM - Node.js Package Manager](https://www.udemy.com/course/understanding-npm) | in progress | 12% | 2026-03 | 2h 19m | 8/3/6/1/1/2/3/9 | D. Skip | High |
| 81 | [Full Stack: React and Java Spring Boot - The Developer Guide](https://www.udemy.com/course/full-stack-react-and-java-spring-boot-the-developer-guide) | not started | 0% | 2026-02 | 26h 39m | 9/8/7/5/4/2/9/9 | D. Skip | High |
| 82 | [Business Model Innovation: Differentiate & Grow Your Company](https://www.udemy.com/course/disruptive-innovation-business-model-startup) | not started | 0% | 2026-02 | 5h 33m | 7/3/3/6/3/5/4/9 | D. Skip | High |
| 83 | [The Project Management Course: Beginner to PROject Manager](https://www.udemy.com/course/the-project-management-course-beginner-to-project-manager) | not started | 0% | 2026-04 | 7h 47m | 9/4/6/6/4/6/4/9 | C. Reference only | High |
| 84 | [Business Analysis Fundamentals - IIBA endorsed](https://www.udemy.com/course/business-analysis-ba) | not started | 0% | 2025-09 | 8h 14m | 9/4/6/6/3/5/4/8 | C. Reference only | High |
| 85 | [Rest API Testing (Automation) from Scratch-Rest Assured Java](https://www.udemy.com/course/rest-api-automation-testing-rest-assured) | in progress | 50% | 2026-04 | 24h 35m | 9/5/8/3/1/2/9/9 | C. Reference only | High |
| 86 | [Bash Scripting and Shell Programming (Linux Command Line)](https://www.udemy.com/course/bash-scripting) | not started | 0% | 2026-07 | 2h 33m | 7/5/4/5/4/2/7/10 | B. Use selectively | High |
| 87 | [WebDriverIO + Node.js -JavaScript UI Automation from Scratch](https://www.udemy.com/course/webdriverio-tutorial-nodejs-javascript) | in progress | 13% | 2025-03 | 10h 59m | 8/5/8/3/1/2/9/8 | D. Skip | High |
| 88 | [Python Basics](https://www.udemy.com/course/2435072/) | not started | 0% | Unknown | Unknown | 2/1/2/2/2/2/2/1 | D. Skip | Low |
| 89 | [Business Analysis: Functional & Non-Functional Requirements](https://www.udemy.com/course/identify-functional-and-non-functional-requirements) | not started | 0% | 2026-03 | 1h 35m | 8/4/6/6/4/6/7/9 | C. Reference only | High |
| 90 | [Learn JMETER from Scratch on Live Apps -Performance Testing](https://www.udemy.com/course/learn-jmeter-from-scratch-performance-load-testing-tool) | not started | 0% | 2025-07 | 8h 19m | 9/5/7/5/4/2/7/8 | B. Use selectively | High |
| 91 | [Hibernate: Advanced Development Techniques](https://www.udemy.com/course/hibernate-tutorial-advanced) | not started | 0% | 2026-01 | 3h 28m | 8/5/5/1/1/2/9/9 | D. Skip | High |
| 92 | [Design Patterns in JavaScript](https://www.udemy.com/course/design-patterns-javascript) | not started | 0% | 2021-08 | 10h 3m | 6/6/6/3/1/2/9/2 | D. Skip | High |
| 93 | [Postman: The Complete Guide - REST API Testing](https://www.udemy.com/course/postman-the-complete-guide) | not started | 0% | 2025-11 | 19h 47m | 9/6/8/3/1/2/9/7 | C. Reference only | High |
| 94 | [Advanced Java Topics: Java Reflection - Master Class](https://www.udemy.com/course/java-reflection-master-class) | not started | 0% | 2025-09 | 4h 51m | 8/4/5/3/1/2/9/8 | C. Reference only | High |
| 95 | [Event Driven Microservices with CQRS, Saga, Event Sourcing](https://www.udemy.com/course/event-driven-microservices-with-cqrs-saga-event-sourcing) | not started | 0% | 2025-12 | 10h 54m | 8/4/6/5/4/2/9/8 | B. Use selectively | High |
| 96 | [Microservices: Clean Architecture, DDD, SAGA, Outbox & Kafka](https://www.udemy.com/course/microservices-clean-architecture-ddd-saga-outbox-kafka-kubernetes) | not started | 0% | 2026-06 | 22h 22m | 9/6/7/8/3/5/9/10 | B. Use selectively | High |
| 97 | [Mastering Java Reactive Programming \[ From Scratch \]](https://www.udemy.com/course/complete-java-reactive-programming) | not started | 0% | 2026-06 | 17h 5m | 9/6/8/3/1/2/9/10 | C. Reference only | High |
| 98 | [Master Generative AI for Developer Productivity With Pieces](https://www.udemy.com/course/mastering-generative-ai-for-developer-productivity) | not started | 0% | 2026-06 | 1h 5m | 4/3/5/2/2/3/3/9 | D. Skip | High |
| 99 | [Java Spring Boot Microservices eCommerce Project Masterclass](https://www.udemy.com/course/java-spring-boot-microservices-with-spring-cloud-k8s-docker) | not started | 0% | 2026-05 | 77h 16m | 9/8/8/5/4/2/9/9 | D. Skip | High |
| 100 | [Master Microservices with Spring Boot and Spring Cloud](https://www.udemy.com/course/microservices-with-spring-boot-and-spring-cloud) | not started | 0% | 2026-05 | 22h 44m | 9/6/7/5/4/2/9/9 | C. Reference only | High |
| 101 | [Apache Maven](https://www.udemy.com/course/maven-dmdev) | not started | 0% | 2022-03 | 4h 35m | 3/3/3/1/1/2/9/4 | C. Reference only | High |
| 102 | [Gradle](https://www.udemy.com/course/gradle-dmdev) | not started | 0% | 2021-10 | 4h 47m | 5/4/6/1/1/2/9/2 | C. Reference only | High |
| 103 | [AWS Serverless REST APIs for Java Developers. CI/CD included](https://www.udemy.com/course/aws-serverless-rest-apis-for-java-developers) | not started | 0% | 2025-12 | 14h 56m | 9/6/7/5/4/2/9/8 | B. Use selectively | High |
| 104 | [gRPC Java: High-Performance Spring Boot Microservices](https://www.udemy.com/course/grpc-the-complete-guide-for-java-developers) | not started | 0% | 2026-06 | 15h 58m | 9/6/7/8/4/6/9/10 | B. Use selectively | High |
| 105 | [AI Builder: Create Agents, Voice Agents & Automations in n8n](https://www.udemy.com/course/ai-builder-with-n8n-create-agents-voice-agents) | not started | 0% | 2026-06 | 14h 20m | 7/6/8/5/6/8/3/10 | B. Use selectively | High |
| 106 | [AI Engineer Agentic Track: The Complete Agent & MCP Course](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course) | not started | 0% | 2026-06 | 21h 33m | 9/8/9/9/10/10/4/10 | A. Complete now | High |

## 4. Completed Courses

| Course | Udemy evidence | Certificate | Audit interpretation |
|---|---|---|---|
| [Искусственный интеллект и Машинное обучение + Основы Python](https://www.udemy.com/course/ai-machinelearning-ru) | Udemy says 100% complete | Unknown / not independently confirmed | Actual mastery cannot be confirmed; E. Already provides sufficient foundation |
| [Spring Security with ReactJS, OAuth2, JWT, MFA \| Spring Boot](https://www.udemy.com/course/spring-security-6-with-reactjs-oauth2-jwt-multifactor-authentication) | Udemy says 100% complete | Unknown / not independently confirmed | Actual mastery cannot be confirmed; E. Already provides sufficient foundation |
| [Apache Kafka for Event-Driven Spring Boot Microservices](https://www.udemy.com/course/apache-kafka-for-spring-boot-microservices) | Udemy says 100% complete | Unknown / not independently confirmed | Actual mastery cannot be confirmed; E. Already provides sufficient foundation |
| [Spring Boot Unit Testing with JUnit, Mockito and MockMvc](https://www.udemy.com/course/spring-boot-unit-testing) | Udemy says 100% complete | Unknown / not independently confirmed | Actual mastery cannot be confirmed; E. Already provides sufficient foundation |
| [Testing Java: JUnit 5, Mockito, Testcontainers, REST Assured](https://www.udemy.com/course/testing-java-code-with-junit-5-and-mockito) | Udemy says 100% complete | Unknown / not independently confirmed | Actual mastery cannot be confirmed; E. Already provides sufficient foundation |
| [Software Architecture & Design of Modern Large Scale Systems](https://www.udemy.com/course/software-architecture-design-of-modern-large-scale-systems) | Udemy says 100% complete | Unknown / not independently confirmed | Actual mastery cannot be confirmed; E. Already provides sufficient foundation |
| [Spring Boot 4, Spring 7 & Hibernate for Beginners](https://www.udemy.com/course/spring-hibernate-tutorial) | Udemy says 100% complete | Unknown / not independently confirmed | Actual mastery cannot be confirmed; E. Already provides sufficient foundation |
| [Build Reactive MicroServices using Spring WebFlux/SpringBoot](https://www.udemy.com/course/build-reactive-restful-apis-using-spring-boot-webflux) | Udemy says 100% complete | Unknown / not independently confirmed | Actual mastery cannot be confirmed; E. Already provides sufficient foundation |
| [FULL STACK JAVA DEV: JAVA + JSP + SPRING + BOOT + JS + REACT](https://www.udemy.com/course/full-stack-java-developer-java) | Udemy says 100% complete | Unknown / not independently confirmed | Actual mastery cannot be confirmed; E. Already provides sufficient foundation |
| [Java Interview Masterclass: Top 350 Questions (PDF)(2026)](https://www.udemy.com/course/top-250-java-interview-questions) | Udemy says 100% complete | Unknown / not independently confirmed | Actual mastery cannot be confirmed; D. Skip |
| [Integration Testing with Testcontainers: Java & Spring Boot](https://www.udemy.com/course/testcontainers-integration-testing-java-spring-boot) | Udemy says 100% complete | Unknown / not independently confirmed | Actual mastery cannot be confirmed; E. Already provides sufficient foundation |

The completed set strongly supports Java testing, Spring, event-driven Kafka, reactive services, software architecture and security. Only the short 3h19m AI/ML introduction is AI-specific, so it should be treated as orientation rather than an ML foundation. The completed Java interview PDF course is low-value evidence for the target transition despite its 100% status.

## 5. Courses in Progress

| Course | Progress | Decision | Recommended focus |
|---|---:|---|---|
| [Claude Code Bootcamp: Hooks, MCP & Agentic AI Workflows](https://www.udemy.com/course/claude-code-bootcamp) | 38% | A. Complete now | Complete full course; prioritize: Never Lose Your Work - Mastering Context, Sessions & Checkpoints \| Mastering MCP - Connect, Automate, and Supercharge Claude Code with Real Tools \| Sub Agents & Agent Teams - Claude Code's Multi-Agent Universe \| Mastering Claude Code - Setup, Modes, Permissions & Customization \| Claude Code + GitHub - Automating Real Developer Workflows \| From Chaos to Control - Mastering Claude Code Rules, Memory & Skills |
| [Production AI Agents with LangChain + LangGraph \[2026\]](https://www.udemy.com/course/production-ai-agents) | 13% | A. Complete now | Complete full course; prioritize: Document Loading, Chunking & Embeddings - Loaders, Splitters, Vector Stores \| RAG and Memory - A Comprehensive Dive \| LangGraph - A Full Deep Dive \| Multi-Agent Systems with LangGraph and LangChain \| Production Deployment - Deploying AI Agents \| LangChain Foundations - A Deep Dive |
| [AI Engineer Core Track: LLM Engineering, RAG, QLoRA, Agents](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models) | 5% | A. Complete now | Complete full course; prioritize: Week 1 - Build Your First LLM Product: Exploring Top Models \| Week 2 - Build a Multi-Modal Chatbot: LLMs, Gradio UI, and Agents \| Week 4 - LLM Showdown: Evaluating Models for Code Gen & Business Tasks \| Week 5 - Mastering RAG: Build Advanced Solutions with Vector Embeddings \| Week 8 - Build Autonomous multi agent system \| Week 3 - Open-Source Gen AI: Automated Solutions with HuggingFace |
| [LangChain- Agentic AI Engineering with LangChain & LangGraph](https://www.udemy.com/course/langchain) | 63% | A. Complete now | Complete full course; prioritize: THE GIST Of AI Agents \| Agents Under The Hood (1/4) \| The GIST of RAG- Embeddings, Vector Databases and, & Retrieval \| Building a documentation assistant (Embeddings, VectorDBs, Retrieval, Memory) \| Let's Talk About LLM Applications In Production \| Reflection Agent |
| [100 Days of Code™: The Complete Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code) | 36% | B. Use selectively | Day 1 - Beginner - Working with Variables in Python to Manage Data \| Day 2 - Beginner - Understanding Data Types and How to Manipulate Strings \| Day 3 - Beginner - Control Flow and Logical Operators \| Day 4 - Beginner - Randomisation and Python Lists \| Day 5 - Beginner - Python Loops \| Day 6 - Beginner - Python Functions & Karel |
| [Java Interview Questions Boot Camp - 1000+ Q& A Master Class](https://www.udemy.com/course/java-interview-questions-bootcamp-master-class-1000-java-questions) | 1% | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [FastAPI - The Complete Course 2026 (Beginner + Advanced)](https://www.udemy.com/course/fastapi-the-complete-course) | 90% | A. Complete now | Complete full course; prioritize: FastAPI Overview \| FastAPI Setup & Installation \| Project 1 - FastAPI Request Method Logic \| Project 2 - Move Fast with FastAPI \| Project 4 - Unit & Integration Testing \| Deploying FastAPI Applications |
| [Python - Полный Курс по Python, Django, Data Science и ML](https://www.udemy.com/course/python-ru) | 53% | B. Use selectively | Введение в Python \| Установка и настройка редактора Visual Studio Code \| Установка PyCharm \| Основные концепции в Python \| Встроенные функции в Python \| Форматирование кода и PEP8 |
| [\[NEW\] Master Microservices with SpringBoot,Docker,Kubernetes](https://www.udemy.com/course/master-microservices-with-spring-docker-kubernetes) | 71% | A. Complete now | Complete full course; prioritize: Handle deployment, portability & scalability of microservices using Docker \| Deep Dive on Cloud Native Apps & 15-Factor methodology \| Gateway, Routing & Cross cutting concerns in Microservices \| Making Microservices Resilient \| Observability and monitoring of microservices \| Microservices Security |
| [From Java Dev to AI Engineer: Spring AI Fast Track](https://www.udemy.com/course/java-spring-ai) | 8% | A. Complete now | Complete full course; prioritize: Spring AI Essentials - Prompts, Advisors, and Structured Responses \| Foundations of Generative AI and LLMs \| Teaching LLMs to Remember - The Power of Chat Memory in Spring AI \| The Art of Talking to Documents – RAG Unleashed \| Tool Calling in Action - Giving LLMs the Power to Do Things \| Mastering Model Context Protocol (MCP) |
| [Kafka MicroServices with Spring Boot, Docker, Kubernetes, AI](https://www.udemy.com/course/apache-kafka-for-developers-using-springboot) | 36% | B. Use selectively | Getting Started with Kafka \| Docker Installation \| Understanding Kafka Components and its Internals - (Theory + Hands On) \| AI Driven Development - Vibe Coding , Agentic Engineering \| Build LibraryEvents Kafka Producer MicroService \| Unit and Integration Testing - Library Events producer API - AI Assisted |
| [Spring Boot Microservices and Spring Cloud. Build & Deploy.](https://www.udemy.com/course/spring-boot-microservices-and-spring-cloud) | 77% | B. Use selectively | Spring Cloud Gateway - Spring Cloud Routing. \| Spring Cloud Gateway as a Load Balancer \| [Deprecated] Enable Spring Security in Zuul API Gateway \| Spring Cloud API Gateway - Creating a Custom Filter. \| Spring Cloud API Gateway Global Pre and Post Filters \| Spring Cloud Config Server (Git backend) - Centralized Configuration. |
| [Selenium WebDriver with Java -Basics to Advanced+Frameworks](https://www.udemy.com/course/selenium-real-time-examplesinterview-questions) | 46% | C. Reference only | Reference on demand: Deep Dive into Functional testing with Selenium \| Framework Part 6 - Test Execution from Maven & Integration with Jenkins CI/CD \| CI/CD Integration of Selenium Framework with Jenkins & GitHub \| Cross Browser Testing with Selenium Grid |
| [Playwright JS/TS Automation Testing from Scratch & Framework](https://www.udemy.com/course/playwright-tutorials-automation-testing) | 88% | B. Use selectively | Playwright Basic methods for Web Automation testing with examples \| Playwright Unique GetBy Locators for Smart Testing & Test Runner usage \| API Testing with Playwright and Build mix of Web & API tests \| Session storage & Intercepting Network request/responses with Playwright \| Assignment on API Testing & Mocking with Playwright \| Perform Visual Testing with Playwright Algorithms |
| [Cypress -Modern Automation Testing from Scratch + Frameworks](https://www.udemy.com/course/cypress-tutorial) | 15% | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Automated Software Testing with Cypress](https://www.udemy.com/course/automated-testing-with-cypress) | 24% | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Hibernate](https://www.udemy.com/course/hibernate-dmdev) | 1% | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [OpenTelemetry Observability For Java Spring Boot Developers](https://www.udemy.com/course/opentelemetry-metrics-tracing-guide) | 8% | A. Complete now | Complete full course; prioritize: The Need for Application Observability \| Observability & OpenTelemetry Basics \| Distributed Tracing \| OpenTelemetry - Manual Instrumentation \| Role Play: Debugging a Latency Spike using OpenTelemetry \| OpenTelemetry Spring Boot Starter |
| [Reactive Applications with Spring WebFlux Framework](https://www.udemy.com/course/reactive-applications-with-spring-webflux-framework) | 46% | B. Use selectively | Unprotected API endpoints - Security Security in Reactive WebFlux. \| Encrypting User's Password - Spring Security in Reactive Spring WebFlux. \| Implement User Authentication(Login). Spring Security in Reactive Spring WebFlux \| Generating JSON Web Token(JWT) \| Validating JSON Web Token(JWT) in Reactive Spring WebFlux applications \| Method-level Security in Reactive Spring WebFlux applications |
| [Let's Learn Terraform in GCP](https://www.udemy.com/course/lets-learn-terraform-in-gcp) | 28% | B. Use selectively | Getting started with Terraform \| Basics of Terraform \| Creating and managing GCP resources using Terraform \| Working with Managed Instance Groups in GCP using Terraform \| Load balancing and network services in GCP using Terraform \| Optimizing Terraform Configuration Logic and Workflow |
| [Understanding TypeScript](https://www.udemy.com/course/understanding-typescript) | 71% | C. Reference only | Reference on demand: Practice Time! Let's build a Drag & Drop Project \| Getting Started \| TypeScript Basics & Basic Types \| The TypeScript Compiler (and its Configuration) |
| [Java Data Structures & Algorithms + LEETCODE Exercises](https://www.udemy.com/course/data-structures-and-algorithms-java) | 50% | C. Reference only | Reference on demand: Big O \| Classes & References \| Linked Lists \| <> LL: Coding Exercises |
| [Docker & Kubernetes: The Practical Guide](https://www.udemy.com/course/docker-kubernetes-the-practical-guide) | 6% | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Java Masterclass 2025: 130+ Hours of Expert Lessons](https://www.udemy.com/course/java-the-complete-java-developer-course) | 1% | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [GCP for Beginners - Become a Google Cloud Digital Leader](https://www.udemy.com/course/google-cloud-digital-leader-certification) | 4% | B. Use selectively | Getting Started - Google Cloud - Cloud Digital Leader Certification \| Getting Started with Cloud and Google Cloud \| Regions and Zones in GCP - Google Cloud Platform \| Google Cloud - Managing VMs with Compute Engine \| Google Cloud - Managing VM Groups with Instance Groups \| Getting Started with Cloud Load Balancing |
| [Java Debugging With IntelliJ IDEA](https://www.udemy.com/course/java-debugging-with-intellij-idea) | 8% | C. Reference only | Reference on demand: GCP Cloud Function Local Debugging with Intellij IDEA \| Environment Setup \| Basic Debugging Features \| Advanced Debugging Features |
| [Full Stack: Angular and Java Spring Boot E-Commerce Website](https://www.udemy.com/course/full-stack-angular-spring-boot-tutorial) | 64% | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [\[NEW\] Spring Boot 4, Spring Framework 7: Beginner to Guru](https://www.udemy.com/course/spring-framework-6-beginner-to-guru) | 47% | C. Reference only | Reference on demand: Testing Spring RestTemplate \| Spring Security HTTP Basic Auth \| Spring Cloud Gateway \| Docker with Spring Boot |
| [Java Design Patterns & SOLID Design Principles](https://www.udemy.com/course/design-patterns-in-java-concepts-hands-on-projects) | 19% | C. Reference only | Reference on demand: SOLID Design Principles \| Creational Design Patterns \| Builder \| Simple Factory |
| [600+ Spring Interview Questions Practice Test](https://www.udemy.com/course/spring-interview-questions) | 17% | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Angular - The Complete Guide](https://www.udemy.com/course/the-complete-guide-to-angular-2) | 15% | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Spring](https://www.udemy.com/course/spring-dmdev) | 24% | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Spring - Полный курс. Boot, Hibernate, Security, REST.](https://www.udemy.com/course/spring-alishev) | 91% | C. Reference only | Reference on demand: Spring Security \| Перед началом \| Spring Core \| Spring MVC |
| [\[NEW\] Master Spring Boot Microservice & Angular K8s CICD AWS](https://www.udemy.com/course/master-spring-boot-microservice-angular-with-k8s-cicd-aws) | 98% | A. Complete now | Complete full course; prioritize: All about Docker and Dockerization of food delivery application (FE + BE) \| Cloud Databases \| Kubernetes \| Continuous Integration Continuous deployment CI/CD \| Building Backend Microservice Application \| All about Angular for quick start with Food delivery application |
| [Design Patterns in Java](https://www.udemy.com/course/design-patterns-java) | 1% | C. Reference only | Reference on demand: SOLID Design Principles \| Builder \| Factories \| Prototype |
| [Java Full Stack(Spring Boot, Spring AI, React, Stripe, AWS )](https://www.udemy.com/course/java-full-stack-mastery-spring-boot-react-stripe-aws) | 14% | B. Use selectively | Final project BE - Spring Security and Jwt Integration \| Deploying to AWS \| Working with LLM - The Backend \| Working with the Spring AI Chroma Vector Store \| Spring Boot Crash Course \| React Crash Course |
| [The Complete Full-Stack Web Development Bootcamp](https://www.udemy.com/course/the-complete-web-development-bootcamp) | 39% | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Master the Coding Interview: Data Structures + Algorithms](https://www.udemy.com/course/master-the-coding-interview-data-structures-algorithms) | 13% | C. Reference only | Reference on demand: Getting More Interviews \| Big O \| How To Solve Coding Problems \| Data Structures: Introduction |
| [OAuth 2.0 in Spring Boot Applications](https://www.udemy.com/course/oauth2-in-spring-boot-applications) | 2% | C. Reference only | Reference on demand: Refreshing Access Token \| Resource Server: Method Level Security \| Keycloak Remote User Authentication. User Storage SPI. \| OAuth 2 Grant Types and Authorization Flows |
| [Spring Boot Microservices with Spring Cloud Beginner to Guru](https://www.udemy.com/course/spring-boot-microservices-with-spring-cloud-beginner-to-guru) | 34% | C. Reference only | Reference on demand: Using Sagas with Spring \| Integration Testing of Sagas \| Compensating Transactions with Sagas \| Spring Cloud Gateway |
| [Deploy Java Spring Apps Online to Amazon Cloud (AWS)](https://www.udemy.com/course/deploy-java-spring-apps-online) | 44% | B. Use selectively | Deploy Java Spring Apps to Amazon Cloud \| Deploy MySQL Database in AWS with RDS \| Deploy Real-Time CRUD Spring App to Amazon Cloud \| Course Introduction \| Getting Started with Amazon Web Services \| Creating a Custom Domain Name with AWS Route 53 |
| [Java Spring Boot Full Stack: eCommerce Project Masterclass](https://www.udemy.com/course/spring-boot-using-intellij-build-a-real-world-project) | 3% | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Java Multithreading, Concurrency & Performance Optimization](https://www.udemy.com/course/java-multithreading-concurrency-performance-optimization) | 13% | B. Use selectively | Threading fundamentals - Thread Creation \| Threading fundamentals - Thread Coordination \| Performance Optimization \| Data Sharing between Threads \| The Concurrency Challenges & Solutions \| Advanced Locking |
| [Learn Redis And Use Jedis With Spring Data Redis](https://www.udemy.com/course/1701332/) | 2% | C. Reference only | Reference on demand: relevant module only |
| [Redis: The Complete Developer's Guide](https://www.udemy.com/course/redis-the-complete-developers-guide-p) | 2% | B. Use selectively | Get Started Here! \| Commands for Adding and Querying Data \| E-Commerce App Setup \| Local Redis Setup \| Hash Data Structures \| Redis Has Gotcha's! |
| [Apache Kafka Series - Learn Apache Kafka for Beginners v3](https://www.udemy.com/course/apache-kafka) | 17% | B. Use selectively | Kafka Introduction \| ====== Kafka Fundamentals ====== \| Kafka Theory \| Starting Kafka \| [Archive] Starting Kafka with Zookeeper + Windows non WSL-2 \| Kafka UI - Conduktor Demo |
| [Devops Fundamentals - CI/CD with AWS +Docker+Ansible+Jenkins](https://www.udemy.com/course/devops-fundamentals-aws) | 3% | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Complete Linux Training Course to Get Your Dream IT Job 2026](https://www.udemy.com/course/complete-linux-training-course-to-get-your-dream-it-job) | 51% | A. Complete now | Complete full course; prioritize: Module 1 - Introduction to Linux \| Module 2 - Download, Install and Configure \| Module 3 - System Access and File System \| Module 4 - Linux Fundamentals \| Module 5 - System Administration \| Module 6 - Shell Scripting |
| [Understanding NPM - Node.js Package Manager](https://www.udemy.com/course/understanding-npm) | 12% | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Rest API Testing (Automation) from Scratch-Rest Assured Java](https://www.udemy.com/course/rest-api-automation-testing-rest-assured) | 50% | C. Reference only | Reference on demand: Getting started with API Testing using Postman \| Rest Assured setup for API Automation Testing \| Learn GraphQL from Scratch and Testing with Rest Assured \| REST API Basics and Terminology |
| [WebDriverIO + Node.js -JavaScript UI Automation from Scratch](https://www.udemy.com/course/webdriverio-tutorial-nodejs-javascript) | 13% | D. Skip | None; lower priority because of duplication, weak fit, or staleness |

Highest-ROI near-complete items are **FastAPI (90%)**, **AWS/K8s/CI/CD microservices (98%)**, **LangChain/LangGraph (63%)**, and the **Spring/Docker/Kubernetes microservices course (71%)**. Progress alone does not show which modules were completed, so recommendations name the modules with the strongest target-role value.

## 6. Not Started Courses

| Course | Decision | Recommended focus |
|---|---|---|
| [The Complete Oracle SQL Bootcamp (2026)](https://www.udemy.com/course/oracle-sql-12c-become-an-sql-developer-with-subtitle) | C. Reference only | Reference on demand: Database Concepts \| Software Download & Installation \| Retrieving Data \| Restricting Data |
| [The AI Engineer Course 2026: Complete AI Engineer Bootcamp](https://www.udemy.com/course/the-ai-engineer-course-complete-ai-engineer-bootcamp) | B. Use selectively | NLP Module: Vectorizing Text \| LLMs Module: Introduction to Large Language Models \| LLMs Module: The Transformer Architecture \| LLMs Module: Getting Started With GPT Models \| LLMs Module: Hugging Face Transformers \| LLMs Module: Question and Answer Models With BERT |
| [Master statistics & machine learning: intuition, math, code](https://www.udemy.com/course/statsml_x) | A. Complete now | Complete full course; prioritize: Hypothesis testing \| Math prerequisites \| IMPORTANT: Download course materials \| What are (is?) data? \| Visualizing data \| Descriptive statistics |
| [Spring AI - GenAI with Telusko](https://www.udemy.com/course/spring-ai-genai) | B. Use selectively | AI Model Integration (Cloud-Based), ChatClient API, and ChatModel \| Vector Embeddings \| Vector Databases \| Retrieval-Augmented Generation (RAG) \| AI Model Integration (Open Source) \| Prompt Templates |
| [Computer Science 101: Master the Theory Behind Programming](https://www.udemy.com/course/computer-science-101-master-the-theory-behind-programming) | C. Reference only | Reference on demand: Analyzing Algorithms \| Arrays \| Linked Lists \| Stacks and Queues |
| [React - The Complete Guide (incl. Next.js, Redux)](https://www.udemy.com/course/react-the-complete-guide-incl-redux) | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [The Ultimate React Course 2025: React, Next.js, Redux & More](https://www.udemy.com/course/the-ultimate-react-course) | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Docker & Kubernetes: The Complete Practical Guide](https://www.udemy.com/course/docker-complete) | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Hibernate and Spring Data JPA: Beginner to Guru](https://www.udemy.com/course/hibernate-and-spring-data-jpa-beginner-to-guru) | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Spring Security Zero to Master along with JWT,OAUTH2](https://www.udemy.com/course/spring-security-zero-to-master) | C. Reference only | Reference on demand: Changing the default security configurations \| Spring Security customizations for most common use cases \| Custom Filters in Spring Security \| Token based Authentication using JSON Web Token (JWT) |
| [Terraform for the Absolute Beginners with Labs](https://www.udemy.com/course/terraform-for-the-absolute-beginners) | A. Complete now | Complete full course; prioritize: Getting Started with Terraform \| Terraform Basics \| Terraform State \| Working with Terraform \| Terraform with AWS \| Terraform Provisioners |
| [Spring WebFlux: Microservices Patterns & Advanced Resilience](https://www.udemy.com/course/spring-webflux-patterns) | B. Use selectively | Orchestrator Saga: Distributed Transactions & Parallel Workflow \| Orchestrator Saga: Distributed Transactions & Sequential Workflow \| Splitter Pattern: Routing Messages to Multiple Services \| Reactive Resilience: Timeout Pattern \| Reactive Resilience: Retry Pattern for Fault Tolerance \| Reactive Resilience: Circuit Breaker Pattern |
| [Spring WebFlux Masterclass: High-Performance Reactive APIs](https://www.udemy.com/course/spring-webflux) | B. Use selectively | Welcome: Why Master Spring WebFlux? \| Architectural Shift: Blocking I/O vs Reactive Web \| Reactive Data Access: Spring Data R2DBC \| R2DBC vs JDBC: Performance, Efficiency, and Resource Usage \| Implementing Reactive APIs: CRUD \| Input Validation and Reactive Error Handling |
| [The Git & Github Bootcamp](https://www.udemy.com/course/git-and-github-bootcamp) | C. Reference only | Reference on demand: Course Orientation \| Introducing...Git! \| Installation & Setup \| The Very Basics Of Git: Adding & Committing |
| [Event-Driven Microservices, CQRS, SAGA, Axon 4, Spring Boot](https://www.udemy.com/course/spring-boot-microservices-cqrs-saga-axon-framework) | B. Use selectively | Spring Cloud API Gateway & Load Balancing \| Orchestration-based Saga. Part 1. Reserve Product in Stock. \| Saga. Part 2. Fetch Payment Details. \| Saga. Part 3. Process User Payment. \| Saga. Part 3. Approve Order. \| Saga. Compensating Transactions. |
| [Event-Driven Microservices: Spring Boot, Kafka and Elastic](https://www.udemy.com/course/event-driven-microservices-spring-boot-kafka-and-elasticsearch) | B. Use selectively | First service: ai-generated-tweet-to-kafka-service \| Externalizing configuration with Spring Cloud Config Server \| kafka-to-elastic-service: How to use Kafka consumers and Elastic Index API \| Securing the services: Spring security OAuth2, OpenID connect, Keycloak and JWT \| Kafka streams with a new microservice: How to use Kafka streams state store \| Implement service discovery with Netflix Eureka and Spring Cloud: Spring Eureka |
| [Reactive Redis Masterclass For Java Spring Boot Developers](https://www.udemy.com/course/spring-webflux-redis) | C. Reference only | Reference on demand: Resource \| Redis - Crash Course \| Redisson - Crash Course \| Spring WebFlux Caching |
| [Docker Mastery: with Kubernetes +Swarm from a Docker Captain](https://www.udemy.com/course/docker-mastery) | C. Reference only | Reference on demand: The Best Way to Setup Docker for Your OS \| Dockerfile ENTRYPOINT \| Making It Easier with Docker Compose: The Multi-Container Tool \| Container Registries: Image Storage and Distribution |
| [Appium -Mobile Testing (Android/IOS) from Scratch+Frameworks](https://www.udemy.com/course/mobile-automation-using-appiumselenium-3) | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Learn Cucumber BDD with Java -MasterClass Selenium Framework](https://www.udemy.com/course/cucumber-tutorial) | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Full Stack: React and Java Spring Boot - The Developer Guide](https://www.udemy.com/course/full-stack-react-and-java-spring-boot-the-developer-guide) | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Business Model Innovation: Differentiate & Grow Your Company](https://www.udemy.com/course/disruptive-innovation-business-model-startup) | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [The Project Management Course: Beginner to PROject Manager](https://www.udemy.com/course/the-project-management-course-beginner-to-project-manager) | C. Reference only | Reference on demand: The planning phase - cost \| The monitoring and control phase \| Welcome to the course! Introduction to projects and Project Management \| The project phases |
| [Business Analysis Fundamentals - IIBA endorsed](https://www.udemy.com/course/business-analysis-ba) | C. Reference only | Reference on demand: Welcome to the Course! \| The Basics: From Business Analysis to Business Analyst \| Business Analysis Skills and You \| Approaching Change |
| [Bash Scripting and Shell Programming (Linux Command Line)](https://www.udemy.com/course/bash-scripting) | B. Use selectively | Bash Programming Course Overview and Downloads \| Shell Scripting in a Nutshell \| Return Codes and Exit Statuses \| Shell Functions \| Shell Script Checklist and Template \| Wildcards |
| [Python Basics](https://www.udemy.com/course/2435072/) | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Business Analysis: Functional & Non-Functional Requirements](https://www.udemy.com/course/identify-functional-and-non-functional-requirements) | C. Reference only | Reference on demand: Setting the Stage \| Discovering Functional and Informational Requirements \| Capturing Non-Functional Solution Requirements \| Unlock the Power of AI: Requirements Decomposition with Generative AI Tools |
| [Learn JMETER from Scratch on Live Apps -Performance Testing](https://www.udemy.com/course/learn-jmeter-from-scratch-performance-load-testing-tool) | B. Use selectively | Data Driven testing with Jmeter \| Monitoring Server performance \| Recording the Jmeter Scripts \| How to put load and analyse performance metrics \| Advanced Thread Group Methods for Real time load with Jmeter \| Http Cookie Manager to capture sessions |
| [Hibernate: Advanced Development Techniques](https://www.udemy.com/course/hibernate-tutorial-advanced) | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Design Patterns in JavaScript](https://www.udemy.com/course/design-patterns-javascript) | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Postman: The Complete Guide - REST API Testing](https://www.udemy.com/course/postman-the-complete-guide) | C. Reference only | Reference on demand: File uploads (testing, automatic uploads, uploading multiple files) \| Creating REST API requests with Postman \| Practice section - Building REST API requests \| Writing basic API tests |
| [Advanced Java Topics: Java Reflection - Master Class](https://www.udemy.com/course/java-reflection-master-class) | C. Reference only | Reference on demand: Object Creation and Constructors \| Inspection of Fields & Arrays \| Field Modification & Arrays Creation \| Methods Discovery & Invocation |
| [Event Driven Microservices with CQRS, Saga, Event Sourcing](https://www.udemy.com/course/event-driven-microservices-with-cqrs-saga-event-sourcing) | B. Use selectively | Choreography Saga pattern \| Orchestration Saga pattern \| Database-per-service pattern \| Understanding CQRS and Event Sourcing patterns- Theory \| Implementing CQRS and Event Sourcing patterns \| Materialized View Pattern |
| [Microservices: Clean Architecture, DDD, SAGA, Outbox & Kafka](https://www.udemy.com/course/microservices-clean-architecture-ddd-saga-outbox-kafka-kubernetes) | B. Use selectively | Apache Kafka \| SAGA Architecture Pattern \| Outbox Architecture Pattern \| Kubernetes(K8s) \| K8s & Google Kubernetes Engine(GKE) \| NEW: Outbox pattern with Change Data Capture(CDC) and Debezium |
| [Mastering Java Reactive Programming \[ From Scratch \]](https://www.udemy.com/course/complete-java-reactive-programming) | C. Reference only | Reference on demand: [OPTIONAL] - Context \| Unit Testing With Step Verifier \| Mono \| Flux |
| [Master Generative AI for Developer Productivity With Pieces](https://www.udemy.com/course/mastering-generative-ai-for-developer-productivity) | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Java Spring Boot Microservices eCommerce Project Masterclass](https://www.udemy.com/course/java-spring-boot-microservices-with-spring-cloud-k8s-docker) | D. Skip | None; lower priority because of duplication, weak fit, or staleness |
| [Master Microservices with Spring Boot and Spring Cloud](https://www.udemy.com/course/microservices-with-spring-boot-and-spring-cloud) | C. Reference only | Reference on demand: Master Microservices with Spring Boot and Spring Cloud - Getting Started \| Microservices with Spring Cloud \| Docker with Microservices using Spring Boot and Spring Cloud - V3 \| Kubernetes with Microservices using Docker, Spring Boot and Spring Cloud - V3 |
| [Apache Maven](https://www.udemy.com/course/maven-dmdev) | C. Reference only | Reference on demand: Введение |
| [Gradle](https://www.udemy.com/course/gradle-dmdev) | C. Reference only | Reference on demand: Введение \| Gradle Lifecycle \| Task graph \| Properties |
| [AWS Serverless REST APIs for Java Developers. CI/CD included](https://www.udemy.com/course/aws-serverless-rest-apis-for-java-developers) | B. Use selectively | AWS SAM - Tools to create & deploy Lambda functions \| Canary Release Deployment \| Cognito Authorizer. Using JWT Access Tokens. \| JUnit Testing AWS Lambda \| Developer Tools. AWS CI/CD - AWS CodeCommit \| Developer Tools. AWS CI/CD - AWS CodeBuild |
| [gRPC Java: High-Performance Spring Boot Microservices](https://www.udemy.com/course/grpc-the-complete-guide-for-java-developers) | B. Use selectively | Why gRPC?: The Performance Advantage \| Protocol Buffers \| Unary API: Standard Request-Response \| Server Streaming: Sending Multiple Responses \| Client Streaming: Sending a Stream of Requests \| BiDirectional Streaming: Two-Way Data Flow |
| [AI Builder: Create Agents, Voice Agents & Automations in n8n](https://www.udemy.com/course/ai-builder-with-n8n-create-agents-voice-agents) | B. Use selectively | Week 1 - Automate with Workflows in n8n Cloud. \| Week 2: Accelerate With Voice Agents And RAG \| Week 3: Amplify With Multi-Agent Systems And MCP |
| [AI Engineer Agentic Track: The Complete Agent & MCP Course](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course) | A. Complete now | Complete full course; prioritize: Week 6 - MCP \| Week 1 \| Week 2 \| Week 3 \| Week 4 \| Week 5 |

The most valuable not-started courses are **Master statistics & machine learning**, **Terraform for Absolute Beginners with Labs**, and **AI Engineer Agentic Track: Agent & MCP**. Starting all three concurrently would fragment progress; they should be sequenced after the near-complete courses.

## 7. Archived Courses

No archived courses were present. The Archived tab displayed an empty state.

## 8. Highest-Value Courses

| Course | Progress | AI Platform | LLM Infra | Why it matters now |
|---|---:|---:|---:|---|
| [Production AI Agents with LangChain + LangGraph \[2026\]](https://www.udemy.com/course/production-ai-agents) | 13% | 10 | 10 | LLM APIs, Structured outputs, Embeddings, Vector databases, RAG, LLM evaluation, Agent engineering; strong practical syllabus |
| [From Java Dev to AI Engineer: Spring AI Fast Track](https://www.udemy.com/course/java-spring-ai) | 8% | 10 | 9 | LLM APIs, Structured outputs, Embeddings, RAG, LLM evaluation, Agent engineering, MCP; strong practical syllabus |
| [AI Engineer Agentic Track: The Complete Agent & MCP Course](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course) | 0% | 9 | 10 | LLM APIs, Agent engineering, LangGraph, MCP, Docker; strong practical syllabus |
| [AI Engineer Core Track: LLM Engineering, RAG, QLoRA, Agents](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models) | 5% | 8 | 9 | LLM APIs, Embeddings, RAG, Agent engineering, Token/cost management, Python engineering, MLOps/LLMOps; strong practical syllabus |
| [LangChain- Agentic AI Engineering with LangChain & LangGraph](https://www.udemy.com/course/langchain) | 63% | 8 | 9 | LLM APIs, Embeddings, Vector databases, RAG, Agent engineering, LangGraph, LangChain; strong practical syllabus |
| [OpenTelemetry Observability For Java Spring Boot Developers](https://www.udemy.com/course/opentelemetry-metrics-tracing-guide) | 8% | 9 | 8 | OpenTelemetry, Java/Spring, Microservices/distributed systems, Docker, CI/CD, Observability; strong practical syllabus |
| [Claude Code Bootcamp: Hooks, MCP & Agentic AI Workflows](https://www.udemy.com/course/claude-code-bootcamp) | 38% | 8 | 8 | Agent engineering, MCP, Context engineering, Databases/data; strong practical syllabus |
| [FastAPI - The Complete Course 2026 (Beginner + Advanced)](https://www.udemy.com/course/fastapi-the-complete-course) | 90% | 7 | 7 | Token/cost management, Python engineering, FastAPI, Security, Testing, Databases/data; strong practical syllabus |
| [\[NEW\] Master Microservices with SpringBoot,Docker,Kubernetes](https://www.udemy.com/course/master-microservices-with-spring-docker-kubernetes) | 71% | 8 | 6 | Model routing/fallbacks, Java/Spring, Kafka/event-driven, Microservices/distributed systems, Docker, Kubernetes/Helm, Observability; strong practical syllabus |
| [Terraform for the Absolute Beginners with Labs](https://www.udemy.com/course/terraform-for-the-absolute-beginners) | 0% | 8 | 6 | Terraform/IaC, Cloud infrastructure; strong practical syllabus |
| [\[NEW\] Master Spring Boot Microservice & Angular K8s CICD AWS](https://www.udemy.com/course/master-spring-boot-microservice-angular-with-k8s-cicd-aws) | 98% | 8 | 5 | Java/Spring, Microservices/distributed systems, Docker, Kubernetes/Helm, Cloud infrastructure, CI/CD, Testing; strong practical syllabus |
| [Complete Linux Training Course to Get Your Dream IT Job 2026](https://www.udemy.com/course/complete-linux-training-course-to-get-your-dream-it-job) | 51% | 8 | 5 | Linux/Bash; strong practical syllabus |
| [Master statistics & machine learning: intuition, math, code](https://www.udemy.com/course/statsml_x) | 0% | 6 | 5 | Python engineering, Machine learning, Testing; strong practical syllabus |

Recommended order is not identical to the A category. Use three waves:

1. **Quick closures:** FastAPI 90% and AWS/K8s/CI/CD microservices 98%.
2. **AI application core:** LangChain/LangGraph 63% → Spring AI Fast Track 8% → Production AI Agents 13% → AI Engineer Core Track 5%.
3. **Platform specialization:** OpenTelemetry 8% → Docker/Kubernetes microservices 71% → Terraform labs 0% → Linux 51% → Agent & MCP Track 0%.

The statistics/ML course should run as a slower parallel foundation only if weekly capacity remains; it should not displace production LLM work.

## 9. Low-Value and Duplicate Courses

### Major overlap clusters

- **Agent/LLM stack:** Production AI Agents, AI Engineer Core Track, LangChain/LangGraph, AI Engineer Bootcamp and Agent & MCP Track overlap on agents/RAG. Use LangChain as the immediate implementation course, AI Core for breadth/fine-tuning, Production Agents for production hardening, and Agent & MCP for orchestration. Do not complete every introductory module in every course.
- **Spring AI:** Spring AI Fast Track is the primary Java path. Telusko is useful selectively for embeddings/vector/RAG; the 47-hour Java full-stack e-commerce course should be used only for its Spring AI/Chroma/AWS modules.
- **Docker/Kubernetes:** the 71% Spring microservices course plus the 98% AWS/K8s course already cover much of the target. The two generic Docker/Kubernetes guides and Docker Swarm course are duplicates or references.
- **Spring/microservices:** many courses repeat service discovery, gateways, Spring Cloud, CRUD and e-commerce. These are existing strengths, not the highest-value next learning frontier.
- **Testing automation:** Selenium, two Cypress courses, Appium, Cucumber, WebDriverIO, Postman and Rest Assured overlap heavily. Keep Playwright selectively for API testing, CI/CD, MCP and agent tooling; skip additional UI-testing frameworks.
- **Frontend/full-stack:** React, Angular and repeated e-commerce bootcamps add little to AI platform/LLM infrastructure goals.
- **Java basics/interview:** Java Masterclass, interview Q&A/PDF, Hibernate basics and duplicate Spring basics mostly repeat established experience.
- **Terraform:** use KodeKloud labs as the primary course and the GCP-specific Terraform course selectively.
- **Redis:** use Stephen Grider’s Redis course selectively; the Jedis course is an unavailable draft and Reactive Redis is reference-only.

### Courses that can create an illusion of transition progress

- **Искусственный интеллект и Машинное обучение + Основы Python (100%)** — only 3h19m and introductory; useful orientation, not ML/DL mastery.
- **Java Interview Masterclass PDF (100%)** — completion does not improve AI platform capability.
- **100 Days of Code (36%)** — excellent Python practice, but large portions are games, GUI and general web topics; select production-relevant days.
- **Python/Django/Data Science/ML (53%)** — broad 45-hour survey; progress mixes unrelated domains and should not be read as production Python depth.
- **Angular/Spring e-commerce (64%)** and repeated full-stack courses — substantial time spent, low incremental value for the target.
- **Playwright (88%)** — valuable engineering skill, but only the API, CI/CD, MCP and AI-agent modules materially help this transition.

### Stale or unavailable items

- [Hibernate](https://www.udemy.com/course/hibernate-dmdev) — currency 2/10, 2021-11; version-sensitive material should be verified before use.
- [Spring](https://www.udemy.com/course/spring-dmdev) — currency 4/10, 2022-08; version-sensitive material should be verified before use.
- [Spring - Полный курс. Boot, Hibernate, Security, REST.](https://www.udemy.com/course/spring-alishev) — currency 4/10, 2022-10; version-sensitive material should be verified before use.
- [Design Patterns in Java](https://www.udemy.com/course/design-patterns-java) — currency 2/10, 2020-04; version-sensitive material should be verified before use.
- [Learn Redis And Use Jedis With Spring Data Redis](https://www.udemy.com/course/1701332/) — currency 1/10, Unknown; landing page unavailable/draft.
- [Python Basics](https://www.udemy.com/course/2435072/) — currency 1/10, Unknown; landing page unavailable/draft.
- [Design Patterns in JavaScript](https://www.udemy.com/course/design-patterns-javascript) — currency 2/10, 2021-08; version-sensitive material should be verified before use.
- [Apache Maven](https://www.udemy.com/course/maven-dmdev) — currency 4/10, 2022-03; version-sensitive material should be verified before use.
- [Gradle](https://www.udemy.com/course/gradle-dmdev) — currency 2/10, 2021-10; version-sensitive material should be verified before use.

## 10. Skills Coverage Matrix

Statuses measure evidence from the Udemy library plus the professional context supplied in the request; they do not certify mastery.

| Напрям | Покриття | Докази |
|---|---|---|
| Python engineering | Partial | 100 Days of Code (36%); Python/Django/Data Science/ML (53%); Python Basics is an inaccessible draft. Broad exposure exists, but production packaging, typing, dependency management and testing are not confirmed. |
| Async Python | Weak | FastAPI course is 90%, but the public syllabus does not expose a dedicated async-Python engineering track; no focused asyncio/concurrency course found. |
| FastAPI production engineering | Adequate | FastAPI Complete Course (90%) covers REST APIs, auth, SQLAlchemy, Alembic, tests and deployment; Production AI Agents (13%) adds rate limiting, caching, logging, metrics and Docker. |
| Machine learning fundamentals | Partial | Intro AI/ML course is 100% but only 3h19m; Master Statistics & ML is not started; AI Engineer Bootcamp is not started. |
| Deep learning fundamentals | Partial | Completed intro course includes a shallow neural-network section; AI Engineer Core Track (5%) and AI Engineer Bootcamp (0%) contain deeper DL material not yet evidenced as learned. |
| Transformer architecture | Weak | The AI Engineer Bootcamp includes Transformer/BERT/XLNet sections but is not started; AI Engineer Core Track is 5%. |
| LLM APIs | Partial | LangChain course 63%; Claude Code 38%; Spring AI Fast Track 8%; multiple provider-integration courses exist, but completed module-level mastery cannot be inferred. |
| Structured outputs | Partial | Production AI Agents syllabus includes structured output; Spring AI Fast Track includes structured responses; Spring AI Telusko has output converters. All remain incomplete/not started. |
| Embeddings | Partial | LangChain (63%), Spring AI Fast Track (8%), Spring AI Telusko (0%) and AI Core Track (5%) explicitly cover embeddings. |
| Vector databases | Partial | LangChain covers Pinecone/FAISS; Spring AI courses cover vector stores/Chroma; AI Core Track has vector embeddings. Progress is fragmented. |
| RAG | Partial | LangChain 63% is the strongest signal; Production AI Agents 13%, AI Core 5%, Spring AI Fast Track 8% and Telusko 0% add several RAG implementations. |
| RAG evaluation | Weak | Evaluation is present mainly in Production AI Agents and Spring AI Fast Track, both early in progress; no completed dedicated RAG-evaluation course. |
| LLM evaluation | Weak | AI Core includes a model showdown; Production AI Agents includes semantic evaluation; Spring AI Fast Track includes evaluators. None is complete. |
| Agent engineering | Partial | LangChain 63% and Claude Code 38% provide partial exposure; Production Agents 13% and Agent & MCP Track 0% contain the strongest production and multi-agent projects. |
| LangGraph | Partial | LangChain 63% and Production AI Agents 13% explicitly cover LangGraph; Agent & MCP Track is not started. |
| MCP | Partial | Claude Code 38% and LangChain 63% include MCP sections; Spring AI Fast Track 8% and Agent & MCP Track 0% provide additional but uncompleted depth. |
| Context engineering | Partial | LangChain explicitly claims context engineering; Claude Code covers context windows, memory, checkpoints and worktrees. Progress does not prove those later sections were completed. |
| Tool calling | Partial | LangChain covers raw function calling/ReAct; Spring AI Fast Track has Java tool calling; Agent & MCP Track adds tool-rich projects. No completed targeted course. |
| AI security | Weak | Production AI Agents includes prompt injection/PII defense; LangChain includes agent-security modules; Spring AI Fast Track includes safer answers. These courses are incomplete. |
| Prompt injection protection | Weak | Explicit only in Production AI Agents and agent-security portions of LangChain; no completed evidence. |
| AI observability | Weak | Spring AI Fast Track includes AI metrics/tracing; Production AI Agents includes LangSmith/metrics/logging. Both are at 8–13%. |
| OpenTelemetry | Partial | Dedicated OpenTelemetry for Java/Spring course is 8%; existing observability experience transfers, but course mastery is unconfirmed. |
| Token and cost management | Weak | Tokens/prices/context costs appear in LangChain and Claude Code, but no dedicated budgeting, quotas, attribution or FinOps syllabus was found. |
| Model routing and fallbacks | Weak | Production AI Agents mentions provider switching; Spring AI integrates multiple providers; resilience courses cover generic fallbacks. No complete AI-routing implementation is evidenced. |
| MLOps | Weak | AI Core includes fine-tuning/QLoRA but little verified platform lifecycle; no dedicated model registry, feature store, experiment tracking or serving course. |
| LLMOps | Weak | Deployment, evaluation and observability appear across incomplete courses, but no unified LLMOps lifecycle course is complete. |
| Docker | Strong | Professional context already includes Docker; multiple courses reinforce containers. Completed/advanced microservice and Testcontainers work is strongly transferable. |
| Kubernetes | Partial | Master Microservices with Docker/Kubernetes is 71%; AWS/K8s/CI/CD course is 98%; several duplicate Kubernetes courses are untouched. Practical mastery cannot be confirmed from progress. |
| Terraform | Weak | Terraform in GCP is 28%; KodeKloud Terraform labs are not started. |
| Cloud infrastructure | Partial | GCP beginner course 4%, Terraform/GCP 28%, AWS deployment 44%, AWS serverless 0%, and K8s/AWS 98% provide fragmented coverage. |
| CI/CD for AI systems | Weak | Strong general CI/CD background transfers; AI-specific delivery appears in Claude Code, Production Agents and AWS/K8s courses but is not complete. |
| Data engineering | Partial | SQL, Kafka and Redis courses provide storage/event foundations; no focused lakehouse, batch/stream processing, lineage or AI data pipeline course was found. |
| Distributed systems | Strong | Existing microservices/Kafka experience plus completed large-scale architecture, Kafka and reactive-microservice courses provide the strongest transferable foundation. |

## 11. Transferable Engineering Skills

- **Java and Spring Boot:** provider adapters, AI gateways, policy filters, structured Java outputs, Spring AI services, MCP servers/clients and internal platform APIs.
- **REST API engineering:** model-provider abstraction, streaming/non-streaming endpoints, idempotency, rate limits, quotas, auth and audit-friendly request contracts.
- **Microservices:** isolation of ingestion, retrieval, orchestration, evaluation and policy services; resilience and failure-domain design transfer directly.
- **Kafka:** asynchronous document ingestion, evaluation jobs, human-approval events, audit streams, retry/DLT patterns and decoupled agent workflows.
- **Testing:** deterministic unit tests for tools and adapters, integration tests with provider stubs/Testcontainers, contract tests, regression datasets and evaluation gates.
- **Docker/CI/CD/GitHub Actions:** reproducible agent/RAG services, evaluation in pull requests, prompt/config versioning, image scanning and progressive delivery.
- **SQL/NoSQL:** metadata stores, chat/session state, RAG document metadata, vector-store integration and cost/usage ledgers.
- **System analysis/debugging:** tracing multi-step agent execution, finding retrieval vs generation failures, replaying tool calls and correlating latency/cost/errors.
- **Observability:** metrics/logs/traces are already familiar; the remaining step is adding LLM semantics such as model, tokens, prompt version, retrieval quality, tool span and evaluation score.

## 12. Critical Knowledge Gaps

The five largest gaps are:

1. **Evaluation engineering:** golden datasets, RAG retrieval metrics, LLM-as-judge limitations, offline/online evaluation, regression gates and human calibration.
2. **AI security and governance:** prompt injection, indirect injection, tool authorization, data exfiltration, PII controls, tenant isolation, approval workflows and auditability.
3. **LLM reliability/control plane:** model routing, fallbacks, timeouts, circuit breakers, provider quotas, structured-output validation, retry semantics and graceful degradation.
4. **Token/cost operations:** budgets, attribution, caching, context compression, per-tenant quotas, forecasting and cost-aware routing.
5. **MLOps/LLMOps lifecycle:** experiment/model/prompt registries, reproducible serving, evaluation promotion gates, drift/quality monitoring and rollback.

Additional weak areas are async Python, transformer internals, cloud IAM/networking, Terraform and production data pipelines.

## 13. Recommended Learning Priorities

### 90-day focus

1. Finish **FastAPI** and only the remaining high-value modules of the **98% AWS/K8s/CI/CD** course.
2. Finish **LangChain/LangGraph**, then build one small evaluated RAG service rather than starting another overview course.
3. Complete **Spring AI Fast Track** to translate LLM/RAG/MCP/tool-calling/evaluation concepts into the strongest existing language stack.
4. Continue **Production AI Agents** for security, tests, FastAPI deployment, tracing and human approval.
5. Complete **OpenTelemetry** and instrument the same AI service end-to-end.
6. Add Terraform/Kubernetes/Linux work after the application path is operational.
7. Take the Agent & MCP track only after one production-style single-agent service exists; otherwise the multi-agent projects risk becoming orchestration demos without reliability fundamentals.

### Decisions for every course

### A. Complete now

- [Claude Code Bootcamp: Hooks, MCP & Agentic AI Workflows](https://www.udemy.com/course/claude-code-bootcamp) — 38%; Complete full course; prioritize: Never Lose Your Work - Mastering Context, Sessions & Checkpoints \| Mastering MCP - Connect, Automate, and Supercharge Claude Code with Real Tools \| Sub Agents & Agent Teams - Claude Code's Multi-Agent Universe \| Mastering Claude Code - Setup, Modes, Permissions & Customization \| Claude Code + GitHub - Automating Real Developer Workflows \| From Chaos to Control - Mastering Claude Code Rules, Memory & Skills
- [Production AI Agents with LangChain + LangGraph \[2026\]](https://www.udemy.com/course/production-ai-agents) — 13%; Complete full course; prioritize: Document Loading, Chunking & Embeddings - Loaders, Splitters, Vector Stores \| RAG and Memory - A Comprehensive Dive \| LangGraph - A Full Deep Dive \| Multi-Agent Systems with LangGraph and LangChain \| Production Deployment - Deploying AI Agents \| LangChain Foundations - A Deep Dive
- [AI Engineer Core Track: LLM Engineering, RAG, QLoRA, Agents](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models) — 5%; Complete full course; prioritize: Week 1 - Build Your First LLM Product: Exploring Top Models \| Week 2 - Build a Multi-Modal Chatbot: LLMs, Gradio UI, and Agents \| Week 4 - LLM Showdown: Evaluating Models for Code Gen & Business Tasks \| Week 5 - Mastering RAG: Build Advanced Solutions with Vector Embeddings \| Week 8 - Build Autonomous multi agent system \| Week 3 - Open-Source Gen AI: Automated Solutions with HuggingFace
- [LangChain- Agentic AI Engineering with LangChain & LangGraph](https://www.udemy.com/course/langchain) — 63%; Complete full course; prioritize: THE GIST Of AI Agents \| Agents Under The Hood (1/4) \| The GIST of RAG- Embeddings, Vector Databases and, & Retrieval \| Building a documentation assistant (Embeddings, VectorDBs, Retrieval, Memory) \| Let's Talk About LLM Applications In Production \| Reflection Agent
- [FastAPI - The Complete Course 2026 (Beginner + Advanced)](https://www.udemy.com/course/fastapi-the-complete-course) — 90%; Complete full course; prioritize: FastAPI Overview \| FastAPI Setup & Installation \| Project 1 - FastAPI Request Method Logic \| Project 2 - Move Fast with FastAPI \| Project 4 - Unit & Integration Testing \| Deploying FastAPI Applications
- [\[NEW\] Master Microservices with SpringBoot,Docker,Kubernetes](https://www.udemy.com/course/master-microservices-with-spring-docker-kubernetes) — 71%; Complete full course; prioritize: Handle deployment, portability & scalability of microservices using Docker \| Deep Dive on Cloud Native Apps & 15-Factor methodology \| Gateway, Routing & Cross cutting concerns in Microservices \| Making Microservices Resilient \| Observability and monitoring of microservices \| Microservices Security
- [From Java Dev to AI Engineer: Spring AI Fast Track](https://www.udemy.com/course/java-spring-ai) — 8%; Complete full course; prioritize: Spring AI Essentials - Prompts, Advisors, and Structured Responses \| Foundations of Generative AI and LLMs \| Teaching LLMs to Remember - The Power of Chat Memory in Spring AI \| The Art of Talking to Documents – RAG Unleashed \| Tool Calling in Action - Giving LLMs the Power to Do Things \| Mastering Model Context Protocol (MCP)
- [Master statistics & machine learning: intuition, math, code](https://www.udemy.com/course/statsml_x) — 0%; Complete full course; prioritize: Hypothesis testing \| Math prerequisites \| IMPORTANT: Download course materials \| What are (is?) data? \| Visualizing data \| Descriptive statistics
- [OpenTelemetry Observability For Java Spring Boot Developers](https://www.udemy.com/course/opentelemetry-metrics-tracing-guide) — 8%; Complete full course; prioritize: The Need for Application Observability \| Observability & OpenTelemetry Basics \| Distributed Tracing \| OpenTelemetry - Manual Instrumentation \| Role Play: Debugging a Latency Spike using OpenTelemetry \| OpenTelemetry Spring Boot Starter
- [Terraform for the Absolute Beginners with Labs](https://www.udemy.com/course/terraform-for-the-absolute-beginners) — 0%; Complete full course; prioritize: Getting Started with Terraform \| Terraform Basics \| Terraform State \| Working with Terraform \| Terraform with AWS \| Terraform Provisioners
- [\[NEW\] Master Spring Boot Microservice & Angular K8s CICD AWS](https://www.udemy.com/course/master-spring-boot-microservice-angular-with-k8s-cicd-aws) — 98%; Complete full course; prioritize: All about Docker and Dockerization of food delivery application (FE + BE) \| Cloud Databases \| Kubernetes \| Continuous Integration Continuous deployment CI/CD \| Building Backend Microservice Application \| All about Angular for quick start with Food delivery application
- [Complete Linux Training Course to Get Your Dream IT Job 2026](https://www.udemy.com/course/complete-linux-training-course-to-get-your-dream-it-job) — 51%; Complete full course; prioritize: Module 1 - Introduction to Linux \| Module 2 - Download, Install and Configure \| Module 3 - System Access and File System \| Module 4 - Linux Fundamentals \| Module 5 - System Administration \| Module 6 - Shell Scripting
- [AI Engineer Agentic Track: The Complete Agent & MCP Course](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course) — 0%; Complete full course; prioritize: Week 6 - MCP \| Week 1 \| Week 2 \| Week 3 \| Week 4 \| Week 5

### B. Use selectively

- [100 Days of Code™: The Complete Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code) — 36%; Day 1 - Beginner - Working with Variables in Python to Manage Data \| Day 2 - Beginner - Understanding Data Types and How to Manipulate Strings \| Day 3 - Beginner - Control Flow and Logical Operators \| Day 4 - Beginner - Randomisation and Python Lists \| Day 5 - Beginner - Python Loops \| Day 6 - Beginner - Python Functions & Karel
- [Python - Полный Курс по Python, Django, Data Science и ML](https://www.udemy.com/course/python-ru) — 53%; Введение в Python \| Установка и настройка редактора Visual Studio Code \| Установка PyCharm \| Основные концепции в Python \| Встроенные функции в Python \| Форматирование кода и PEP8
- [Kafka MicroServices with Spring Boot, Docker, Kubernetes, AI](https://www.udemy.com/course/apache-kafka-for-developers-using-springboot) — 36%; Getting Started with Kafka \| Docker Installation \| Understanding Kafka Components and its Internals - (Theory + Hands On) \| AI Driven Development - Vibe Coding , Agentic Engineering \| Build LibraryEvents Kafka Producer MicroService \| Unit and Integration Testing - Library Events producer API - AI Assisted
- [The AI Engineer Course 2026: Complete AI Engineer Bootcamp](https://www.udemy.com/course/the-ai-engineer-course-complete-ai-engineer-bootcamp) — 0%; NLP Module: Vectorizing Text \| LLMs Module: Introduction to Large Language Models \| LLMs Module: The Transformer Architecture \| LLMs Module: Getting Started With GPT Models \| LLMs Module: Hugging Face Transformers \| LLMs Module: Question and Answer Models With BERT
- [Spring Boot Microservices and Spring Cloud. Build & Deploy.](https://www.udemy.com/course/spring-boot-microservices-and-spring-cloud) — 77%; Spring Cloud Gateway - Spring Cloud Routing. \| Spring Cloud Gateway as a Load Balancer \| [Deprecated] Enable Spring Security in Zuul API Gateway \| Spring Cloud API Gateway - Creating a Custom Filter. \| Spring Cloud API Gateway Global Pre and Post Filters \| Spring Cloud Config Server (Git backend) - Centralized Configuration.
- [Playwright JS/TS Automation Testing from Scratch & Framework](https://www.udemy.com/course/playwright-tutorials-automation-testing) — 88%; Playwright Basic methods for Web Automation testing with examples \| Playwright Unique GetBy Locators for Smart Testing & Test Runner usage \| API Testing with Playwright and Build mix of Web & API tests \| Session storage & Intercepting Network request/responses with Playwright \| Assignment on API Testing & Mocking with Playwright \| Perform Visual Testing with Playwright Algorithms
- [Spring AI - GenAI with Telusko](https://www.udemy.com/course/spring-ai-genai) — 0%; AI Model Integration (Cloud-Based), ChatClient API, and ChatModel \| Vector Embeddings \| Vector Databases \| Retrieval-Augmented Generation (RAG) \| AI Model Integration (Open Source) \| Prompt Templates
- [Reactive Applications with Spring WebFlux Framework](https://www.udemy.com/course/reactive-applications-with-spring-webflux-framework) — 46%; Unprotected API endpoints - Security Security in Reactive WebFlux. \| Encrypting User's Password - Spring Security in Reactive Spring WebFlux. \| Implement User Authentication(Login). Spring Security in Reactive Spring WebFlux \| Generating JSON Web Token(JWT) \| Validating JSON Web Token(JWT) in Reactive Spring WebFlux applications \| Method-level Security in Reactive Spring WebFlux applications
- [Let's Learn Terraform in GCP](https://www.udemy.com/course/lets-learn-terraform-in-gcp) — 28%; Getting started with Terraform \| Basics of Terraform \| Creating and managing GCP resources using Terraform \| Working with Managed Instance Groups in GCP using Terraform \| Load balancing and network services in GCP using Terraform \| Optimizing Terraform Configuration Logic and Workflow
- [GCP for Beginners - Become a Google Cloud Digital Leader](https://www.udemy.com/course/google-cloud-digital-leader-certification) — 4%; Getting Started - Google Cloud - Cloud Digital Leader Certification \| Getting Started with Cloud and Google Cloud \| Regions and Zones in GCP - Google Cloud Platform \| Google Cloud - Managing VMs with Compute Engine \| Google Cloud - Managing VM Groups with Instance Groups \| Getting Started with Cloud Load Balancing
- [Spring WebFlux: Microservices Patterns & Advanced Resilience](https://www.udemy.com/course/spring-webflux-patterns) — 0%; Orchestrator Saga: Distributed Transactions & Parallel Workflow \| Orchestrator Saga: Distributed Transactions & Sequential Workflow \| Splitter Pattern: Routing Messages to Multiple Services \| Reactive Resilience: Timeout Pattern \| Reactive Resilience: Retry Pattern for Fault Tolerance \| Reactive Resilience: Circuit Breaker Pattern
- [Spring WebFlux Masterclass: High-Performance Reactive APIs](https://www.udemy.com/course/spring-webflux) — 0%; Welcome: Why Master Spring WebFlux? \| Architectural Shift: Blocking I/O vs Reactive Web \| Reactive Data Access: Spring Data R2DBC \| R2DBC vs JDBC: Performance, Efficiency, and Resource Usage \| Implementing Reactive APIs: CRUD \| Input Validation and Reactive Error Handling
- [Java Full Stack(Spring Boot, Spring AI, React, Stripe, AWS )](https://www.udemy.com/course/java-full-stack-mastery-spring-boot-react-stripe-aws) — 14%; Final project BE - Spring Security and Jwt Integration \| Deploying to AWS \| Working with LLM - The Backend \| Working with the Spring AI Chroma Vector Store \| Spring Boot Crash Course \| React Crash Course
- [Event-Driven Microservices, CQRS, SAGA, Axon 4, Spring Boot](https://www.udemy.com/course/spring-boot-microservices-cqrs-saga-axon-framework) — 0%; Spring Cloud API Gateway & Load Balancing \| Orchestration-based Saga. Part 1. Reserve Product in Stock. \| Saga. Part 2. Fetch Payment Details. \| Saga. Part 3. Process User Payment. \| Saga. Part 3. Approve Order. \| Saga. Compensating Transactions.
- [Event-Driven Microservices: Spring Boot, Kafka and Elastic](https://www.udemy.com/course/event-driven-microservices-spring-boot-kafka-and-elasticsearch) — 0%; First service: ai-generated-tweet-to-kafka-service \| Externalizing configuration with Spring Cloud Config Server \| kafka-to-elastic-service: How to use Kafka consumers and Elastic Index API \| Securing the services: Spring security OAuth2, OpenID connect, Keycloak and JWT \| Kafka streams with a new microservice: How to use Kafka streams state store \| Implement service discovery with Netflix Eureka and Spring Cloud: Spring Eureka
- [Deploy Java Spring Apps Online to Amazon Cloud (AWS)](https://www.udemy.com/course/deploy-java-spring-apps-online) — 44%; Deploy Java Spring Apps to Amazon Cloud \| Deploy MySQL Database in AWS with RDS \| Deploy Real-Time CRUD Spring App to Amazon Cloud \| Course Introduction \| Getting Started with Amazon Web Services \| Creating a Custom Domain Name with AWS Route 53
- [Java Multithreading, Concurrency & Performance Optimization](https://www.udemy.com/course/java-multithreading-concurrency-performance-optimization) — 13%; Threading fundamentals - Thread Creation \| Threading fundamentals - Thread Coordination \| Performance Optimization \| Data Sharing between Threads \| The Concurrency Challenges & Solutions \| Advanced Locking
- [Redis: The Complete Developer's Guide](https://www.udemy.com/course/redis-the-complete-developers-guide-p) — 2%; Get Started Here! \| Commands for Adding and Querying Data \| E-Commerce App Setup \| Local Redis Setup \| Hash Data Structures \| Redis Has Gotcha's!
- [Apache Kafka Series - Learn Apache Kafka for Beginners v3](https://www.udemy.com/course/apache-kafka) — 17%; Kafka Introduction \| ====== Kafka Fundamentals ====== \| Kafka Theory \| Starting Kafka \| [Archive] Starting Kafka with Zookeeper + Windows non WSL-2 \| Kafka UI - Conduktor Demo
- [Bash Scripting and Shell Programming (Linux Command Line)](https://www.udemy.com/course/bash-scripting) — 0%; Bash Programming Course Overview and Downloads \| Shell Scripting in a Nutshell \| Return Codes and Exit Statuses \| Shell Functions \| Shell Script Checklist and Template \| Wildcards
- [Learn JMETER from Scratch on Live Apps -Performance Testing](https://www.udemy.com/course/learn-jmeter-from-scratch-performance-load-testing-tool) — 0%; Data Driven testing with Jmeter \| Monitoring Server performance \| Recording the Jmeter Scripts \| How to put load and analyse performance metrics \| Advanced Thread Group Methods for Real time load with Jmeter \| Http Cookie Manager to capture sessions
- [Event Driven Microservices with CQRS, Saga, Event Sourcing](https://www.udemy.com/course/event-driven-microservices-with-cqrs-saga-event-sourcing) — 0%; Choreography Saga pattern \| Orchestration Saga pattern \| Database-per-service pattern \| Understanding CQRS and Event Sourcing patterns- Theory \| Implementing CQRS and Event Sourcing patterns \| Materialized View Pattern
- [Microservices: Clean Architecture, DDD, SAGA, Outbox & Kafka](https://www.udemy.com/course/microservices-clean-architecture-ddd-saga-outbox-kafka-kubernetes) — 0%; Apache Kafka \| SAGA Architecture Pattern \| Outbox Architecture Pattern \| Kubernetes(K8s) \| K8s & Google Kubernetes Engine(GKE) \| NEW: Outbox pattern with Change Data Capture(CDC) and Debezium
- [AWS Serverless REST APIs for Java Developers. CI/CD included](https://www.udemy.com/course/aws-serverless-rest-apis-for-java-developers) — 0%; AWS SAM - Tools to create & deploy Lambda functions \| Canary Release Deployment \| Cognito Authorizer. Using JWT Access Tokens. \| JUnit Testing AWS Lambda \| Developer Tools. AWS CI/CD - AWS CodeCommit \| Developer Tools. AWS CI/CD - AWS CodeBuild
- [gRPC Java: High-Performance Spring Boot Microservices](https://www.udemy.com/course/grpc-the-complete-guide-for-java-developers) — 0%; Why gRPC?: The Performance Advantage \| Protocol Buffers \| Unary API: Standard Request-Response \| Server Streaming: Sending Multiple Responses \| Client Streaming: Sending a Stream of Requests \| BiDirectional Streaming: Two-Way Data Flow
- [AI Builder: Create Agents, Voice Agents & Automations in n8n](https://www.udemy.com/course/ai-builder-with-n8n-create-agents-voice-agents) — 0%; Week 1 - Automate with Workflows in n8n Cloud. \| Week 2: Accelerate With Voice Agents And RAG \| Week 3: Amplify With Multi-Agent Systems And MCP

### C. Reference only

- [The Complete Oracle SQL Bootcamp (2026)](https://www.udemy.com/course/oracle-sql-12c-become-an-sql-developer-with-subtitle) — 0%; Reference on demand: Database Concepts \| Software Download & Installation \| Retrieving Data \| Restricting Data
- [Selenium WebDriver with Java -Basics to Advanced+Frameworks](https://www.udemy.com/course/selenium-real-time-examplesinterview-questions) — 46%; Reference on demand: Deep Dive into Functional testing with Selenium \| Framework Part 6 - Test Execution from Maven & Integration with Jenkins CI/CD \| CI/CD Integration of Selenium Framework with Jenkins & GitHub \| Cross Browser Testing with Selenium Grid
- [Computer Science 101: Master the Theory Behind Programming](https://www.udemy.com/course/computer-science-101-master-the-theory-behind-programming) — 0%; Reference on demand: Analyzing Algorithms \| Arrays \| Linked Lists \| Stacks and Queues
- [Understanding TypeScript](https://www.udemy.com/course/understanding-typescript) — 71%; Reference on demand: Practice Time! Let's build a Drag & Drop Project \| Getting Started \| TypeScript Basics & Basic Types \| The TypeScript Compiler (and its Configuration)
- [Java Data Structures & Algorithms + LEETCODE Exercises](https://www.udemy.com/course/data-structures-and-algorithms-java) — 50%; Reference on demand: Big O \| Classes & References \| Linked Lists \| <> LL: Coding Exercises
- [Spring Security Zero to Master along with JWT,OAUTH2](https://www.udemy.com/course/spring-security-zero-to-master) — 0%; Reference on demand: Changing the default security configurations \| Spring Security customizations for most common use cases \| Custom Filters in Spring Security \| Token based Authentication using JSON Web Token (JWT)
- [Java Debugging With IntelliJ IDEA](https://www.udemy.com/course/java-debugging-with-intellij-idea) — 8%; Reference on demand: GCP Cloud Function Local Debugging with Intellij IDEA \| Environment Setup \| Basic Debugging Features \| Advanced Debugging Features
- [\[NEW\] Spring Boot 4, Spring Framework 7: Beginner to Guru](https://www.udemy.com/course/spring-framework-6-beginner-to-guru) — 47%; Reference on demand: Testing Spring RestTemplate \| Spring Security HTTP Basic Auth \| Spring Cloud Gateway \| Docker with Spring Boot
- [Java Design Patterns & SOLID Design Principles](https://www.udemy.com/course/design-patterns-in-java-concepts-hands-on-projects) — 19%; Reference on demand: SOLID Design Principles \| Creational Design Patterns \| Builder \| Simple Factory
- [The Git & Github Bootcamp](https://www.udemy.com/course/git-and-github-bootcamp) — 0%; Reference on demand: Course Orientation \| Introducing...Git! \| Installation & Setup \| The Very Basics Of Git: Adding & Committing
- [Spring - Полный курс. Boot, Hibernate, Security, REST.](https://www.udemy.com/course/spring-alishev) — 91%; Reference on demand: Spring Security \| Перед началом \| Spring Core \| Spring MVC
- [Design Patterns in Java](https://www.udemy.com/course/design-patterns-java) — 1%; Reference on demand: SOLID Design Principles \| Builder \| Factories \| Prototype
- [Master the Coding Interview: Data Structures + Algorithms](https://www.udemy.com/course/master-the-coding-interview-data-structures-algorithms) — 13%; Reference on demand: Getting More Interviews \| Big O \| How To Solve Coding Problems \| Data Structures: Introduction
- [OAuth 2.0 in Spring Boot Applications](https://www.udemy.com/course/oauth2-in-spring-boot-applications) — 2%; Reference on demand: Refreshing Access Token \| Resource Server: Method Level Security \| Keycloak Remote User Authentication. User Storage SPI. \| OAuth 2 Grant Types and Authorization Flows
- [Spring Boot Microservices with Spring Cloud Beginner to Guru](https://www.udemy.com/course/spring-boot-microservices-with-spring-cloud-beginner-to-guru) — 34%; Reference on demand: Using Sagas with Spring \| Integration Testing of Sagas \| Compensating Transactions with Sagas \| Spring Cloud Gateway
- [Learn Redis And Use Jedis With Spring Data Redis](https://www.udemy.com/course/1701332/) — 2%; Reference on demand: relevant module only
- [Reactive Redis Masterclass For Java Spring Boot Developers](https://www.udemy.com/course/spring-webflux-redis) — 0%; Reference on demand: Resource \| Redis - Crash Course \| Redisson - Crash Course \| Spring WebFlux Caching
- [Docker Mastery: with Kubernetes +Swarm from a Docker Captain](https://www.udemy.com/course/docker-mastery) — 0%; Reference on demand: The Best Way to Setup Docker for Your OS \| Dockerfile ENTRYPOINT \| Making It Easier with Docker Compose: The Multi-Container Tool \| Container Registries: Image Storage and Distribution
- [The Project Management Course: Beginner to PROject Manager](https://www.udemy.com/course/the-project-management-course-beginner-to-project-manager) — 0%; Reference on demand: The planning phase - cost \| The monitoring and control phase \| Welcome to the course! Introduction to projects and Project Management \| The project phases
- [Business Analysis Fundamentals - IIBA endorsed](https://www.udemy.com/course/business-analysis-ba) — 0%; Reference on demand: Welcome to the Course! \| The Basics: From Business Analysis to Business Analyst \| Business Analysis Skills and You \| Approaching Change
- [Rest API Testing (Automation) from Scratch-Rest Assured Java](https://www.udemy.com/course/rest-api-automation-testing-rest-assured) — 50%; Reference on demand: Getting started with API Testing using Postman \| Rest Assured setup for API Automation Testing \| Learn GraphQL from Scratch and Testing with Rest Assured \| REST API Basics and Terminology
- [Business Analysis: Functional & Non-Functional Requirements](https://www.udemy.com/course/identify-functional-and-non-functional-requirements) — 0%; Reference on demand: Setting the Stage \| Discovering Functional and Informational Requirements \| Capturing Non-Functional Solution Requirements \| Unlock the Power of AI: Requirements Decomposition with Generative AI Tools
- [Postman: The Complete Guide - REST API Testing](https://www.udemy.com/course/postman-the-complete-guide) — 0%; Reference on demand: File uploads (testing, automatic uploads, uploading multiple files) \| Creating REST API requests with Postman \| Practice section - Building REST API requests \| Writing basic API tests
- [Advanced Java Topics: Java Reflection - Master Class](https://www.udemy.com/course/java-reflection-master-class) — 0%; Reference on demand: Object Creation and Constructors \| Inspection of Fields & Arrays \| Field Modification & Arrays Creation \| Methods Discovery & Invocation
- [Mastering Java Reactive Programming \[ From Scratch \]](https://www.udemy.com/course/complete-java-reactive-programming) — 0%; Reference on demand: [OPTIONAL] - Context \| Unit Testing With Step Verifier \| Mono \| Flux
- [Master Microservices with Spring Boot and Spring Cloud](https://www.udemy.com/course/microservices-with-spring-boot-and-spring-cloud) — 0%; Reference on demand: Master Microservices with Spring Boot and Spring Cloud - Getting Started \| Microservices with Spring Cloud \| Docker with Microservices using Spring Boot and Spring Cloud - V3 \| Kubernetes with Microservices using Docker, Spring Boot and Spring Cloud - V3
- [Apache Maven](https://www.udemy.com/course/maven-dmdev) — 0%; Reference on demand: Введение
- [Gradle](https://www.udemy.com/course/gradle-dmdev) — 0%; Reference on demand: Введение \| Gradle Lifecycle \| Task graph \| Properties

### D. Skip

- [Java Interview Questions Boot Camp - 1000+ Q& A Master Class](https://www.udemy.com/course/java-interview-questions-bootcamp-master-class-1000-java-questions) — 1%; None; lower priority because of duplication, weak fit, or staleness
- [Cypress -Modern Automation Testing from Scratch + Frameworks](https://www.udemy.com/course/cypress-tutorial) — 15%; None; lower priority because of duplication, weak fit, or staleness
- [Automated Software Testing with Cypress](https://www.udemy.com/course/automated-testing-with-cypress) — 24%; None; lower priority because of duplication, weak fit, or staleness
- [Hibernate](https://www.udemy.com/course/hibernate-dmdev) — 1%; None; lower priority because of duplication, weak fit, or staleness
- [React - The Complete Guide (incl. Next.js, Redux)](https://www.udemy.com/course/react-the-complete-guide-incl-redux) — 0%; None; lower priority because of duplication, weak fit, or staleness
- [The Ultimate React Course 2025: React, Next.js, Redux & More](https://www.udemy.com/course/the-ultimate-react-course) — 0%; None; lower priority because of duplication, weak fit, or staleness
- [Docker & Kubernetes: The Complete Practical Guide](https://www.udemy.com/course/docker-complete) — 0%; None; lower priority because of duplication, weak fit, or staleness
- [Docker & Kubernetes: The Practical Guide](https://www.udemy.com/course/docker-kubernetes-the-practical-guide) — 6%; None; lower priority because of duplication, weak fit, or staleness
- [Hibernate and Spring Data JPA: Beginner to Guru](https://www.udemy.com/course/hibernate-and-spring-data-jpa-beginner-to-guru) — 0%; None; lower priority because of duplication, weak fit, or staleness
- [Java Masterclass 2025: 130+ Hours of Expert Lessons](https://www.udemy.com/course/java-the-complete-java-developer-course) — 1%; None; lower priority because of duplication, weak fit, or staleness
- [Full Stack: Angular and Java Spring Boot E-Commerce Website](https://www.udemy.com/course/full-stack-angular-spring-boot-tutorial) — 64%; None; lower priority because of duplication, weak fit, or staleness
- [600+ Spring Interview Questions Practice Test](https://www.udemy.com/course/spring-interview-questions) — 17%; None; lower priority because of duplication, weak fit, or staleness
- [Java Interview Masterclass: Top 350 Questions (PDF)(2026)](https://www.udemy.com/course/top-250-java-interview-questions) — 100%; None; lower priority because of duplication, weak fit, or staleness
- [Angular - The Complete Guide](https://www.udemy.com/course/the-complete-guide-to-angular-2) — 15%; None; lower priority because of duplication, weak fit, or staleness
- [Spring](https://www.udemy.com/course/spring-dmdev) — 24%; None; lower priority because of duplication, weak fit, or staleness
- [The Complete Full-Stack Web Development Bootcamp](https://www.udemy.com/course/the-complete-web-development-bootcamp) — 39%; None; lower priority because of duplication, weak fit, or staleness
- [Java Spring Boot Full Stack: eCommerce Project Masterclass](https://www.udemy.com/course/spring-boot-using-intellij-build-a-real-world-project) — 3%; None; lower priority because of duplication, weak fit, or staleness
- [Devops Fundamentals - CI/CD with AWS +Docker+Ansible+Jenkins](https://www.udemy.com/course/devops-fundamentals-aws) — 3%; None; lower priority because of duplication, weak fit, or staleness
- [Appium -Mobile Testing (Android/IOS) from Scratch+Frameworks](https://www.udemy.com/course/mobile-automation-using-appiumselenium-3) — 0%; None; lower priority because of duplication, weak fit, or staleness
- [Learn Cucumber BDD with Java -MasterClass Selenium Framework](https://www.udemy.com/course/cucumber-tutorial) — 0%; None; lower priority because of duplication, weak fit, or staleness
- [Understanding NPM - Node.js Package Manager](https://www.udemy.com/course/understanding-npm) — 12%; None; lower priority because of duplication, weak fit, or staleness
- [Full Stack: React and Java Spring Boot - The Developer Guide](https://www.udemy.com/course/full-stack-react-and-java-spring-boot-the-developer-guide) — 0%; None; lower priority because of duplication, weak fit, or staleness
- [Business Model Innovation: Differentiate & Grow Your Company](https://www.udemy.com/course/disruptive-innovation-business-model-startup) — 0%; None; lower priority because of duplication, weak fit, or staleness
- [WebDriverIO + Node.js -JavaScript UI Automation from Scratch](https://www.udemy.com/course/webdriverio-tutorial-nodejs-javascript) — 13%; None; lower priority because of duplication, weak fit, or staleness
- [Python Basics](https://www.udemy.com/course/2435072/) — 0%; None; lower priority because of duplication, weak fit, or staleness
- [Hibernate: Advanced Development Techniques](https://www.udemy.com/course/hibernate-tutorial-advanced) — 0%; None; lower priority because of duplication, weak fit, or staleness
- [Design Patterns in JavaScript](https://www.udemy.com/course/design-patterns-javascript) — 0%; None; lower priority because of duplication, weak fit, or staleness
- [Master Generative AI for Developer Productivity With Pieces](https://www.udemy.com/course/mastering-generative-ai-for-developer-productivity) — 0%; None; lower priority because of duplication, weak fit, or staleness
- [Java Spring Boot Microservices eCommerce Project Masterclass](https://www.udemy.com/course/java-spring-boot-microservices-with-spring-cloud-k8s-docker) — 0%; None; lower priority because of duplication, weak fit, or staleness

### E. Already provides sufficient foundation

- [Искусственный интеллект и Машинное обучение + Основы Python](https://www.udemy.com/course/ai-machinelearning-ru) — 100%; No further modules required; review only when a concrete gap appears
- [Spring Security with ReactJS, OAuth2, JWT, MFA \| Spring Boot](https://www.udemy.com/course/spring-security-6-with-reactjs-oauth2-jwt-multifactor-authentication) — 100%; No further modules required; review only when a concrete gap appears
- [Apache Kafka for Event-Driven Spring Boot Microservices](https://www.udemy.com/course/apache-kafka-for-spring-boot-microservices) — 100%; No further modules required; review only when a concrete gap appears
- [Spring Boot Unit Testing with JUnit, Mockito and MockMvc](https://www.udemy.com/course/spring-boot-unit-testing) — 100%; No further modules required; review only when a concrete gap appears
- [Testing Java: JUnit 5, Mockito, Testcontainers, REST Assured](https://www.udemy.com/course/testing-java-code-with-junit-5-and-mockito) — 100%; No further modules required; review only when a concrete gap appears
- [Software Architecture & Design of Modern Large Scale Systems](https://www.udemy.com/course/software-architecture-design-of-modern-large-scale-systems) — 100%; No further modules required; review only when a concrete gap appears
- [Spring Boot 4, Spring 7 & Hibernate for Beginners](https://www.udemy.com/course/spring-hibernate-tutorial) — 100%; No further modules required; review only when a concrete gap appears
- [Build Reactive MicroServices using Spring WebFlux/SpringBoot](https://www.udemy.com/course/build-reactive-restful-apis-using-spring-boot-webflux) — 100%; No further modules required; review only when a concrete gap appears
- [FULL STACK JAVA DEV: JAVA + JSP + SPRING + BOOT + JS + REACT](https://www.udemy.com/course/full-stack-java-developer-java) — 100%; No further modules required; review only when a concrete gap appears
- [Integration Testing with Testcontainers: Java & Spring Boot](https://www.udemy.com/course/testcontainers-integration-testing-java-spring-boot) — 100%; No further modules required; review only when a concrete gap appears

## 14. Recommended Production Projects

### Project 1 — Governed multi-provider AI gateway

Build a Spring Boot/Spring AI gateway for OpenAI-compatible, Ollama and AWS Bedrock providers. Include typed/structured responses, streaming, per-tenant auth/quotas, token and cost accounting, cache, rate limiting, model routing/fallback, circuit breakers, prompt/version registry, OpenTelemetry traces and Grafana dashboards. Add contract tests and a GitHub Actions evaluation gate.

### Project 2 — Evaluated multi-tenant RAG platform

Use FastAPI for ingestion/evaluation workers and Java/Spring for the platform API. Add object storage, PostgreSQL/pgvector or Qdrant, chunking/versioning, hybrid retrieval, reranking, citation enforcement, tenant isolation, prompt-injection tests, golden datasets, retrieval/generation metrics and a human feedback loop. Deploy with Docker, Kubernetes and Terraform.

### Project 3 — MCP agent runtime with approval and audit

Create an agent runtime that consumes multiple MCP servers but enforces an allowlist, schema validation, least-privilege credentials, timeouts, sandboxed execution and human approval for risky tools. Persist every decision/tool call to an immutable Kafka audit stream. Add replay, failure recovery, budget limits, OpenTelemetry spans and end-to-end security/evaluation tests.

## 15. Final Career-Fit Assessment

1. **Readiness for AI:** medium. The software/platform base is strong, but AI-specific production controls are only Partial/Weak.
2. **Strongest transferable foundation:** production Java backend engineering—Spring Boot, microservices, Kafka, testing, CI/CD, Docker, system debugging and distributed-systems thinking.
3. **Five biggest gaps:** evaluation, AI security/governance, model routing/reliability, token/cost operations, and MLOps/LLMOps lifecycle.
4. **Courses that create an illusion of progress:** the 3h19m completed AI introduction, Java interview/PDF content, broad Python/Django surveys, repeated full-stack e-commerce courses, and UI-test frameworks outside their MCP/API/CI modules.
5. **Highest-ROI unfinished courses:** FastAPI (90%), AWS/K8s/CI/CD (98%), LangChain/LangGraph (63%), Spring/Docker/Kubernetes (71%), Spring AI Fast Track (8%), Production AI Agents (13%) and OpenTelemetry (8%).
6. **Safe skips:** the 29 D-category courses, especially duplicate frontend/e-commerce, Cypress/Appium/WebDriverIO/Cucumber, Java beginner/interview and duplicate Docker/Kubernetes courses.
7. **Closest direction:** long-term **AI Platform Engineer**; fastest first role may be **AI Application Engineer using Java/Spring AI**. LLM Infrastructure becomes realistic after evaluation, RAG hardening, observability and routing work. MLOps/ML Engineer are currently less supported.
8. **Transferable knowledge:** Java/Spring for gateways/adapters/policies; Kafka for ingestion and approval/audit flows; testing for eval gates and deterministic tool tests; microservices for isolation/resilience; CI/CD for prompt/model/config promotion.
9. **Outside Udemy:** official provider and Spring AI docs, OpenAI Evals-style methodology, RAG evaluation frameworks, OWASP guidance for LLM applications, OpenTelemetry GenAI semantic conventions, Kubernetes/IAM/security labs, and hands-on cost/routing experiments. Version-sensitive claims should be verified against official documentation at implementation time.
10. **Best portfolio proof:** the governed AI gateway, evaluated multi-tenant RAG platform and approval-aware MCP runtime described above.

## Appendix A. Evidence and URLs

1. [Claude Code Bootcamp: Hooks, MCP & Agentic AI Workflows](https://www.udemy.com/course/claude-code-bootcamp) — Udemy course ID 7151685; confidence High; 2026-07.
2. [Production AI Agents with LangChain + LangGraph \[2026\]](https://www.udemy.com/course/production-ai-agents) — Udemy course ID 7031331; confidence High; 2026-05.
3. [AI Engineer Core Track: LLM Engineering, RAG, QLoRA, Agents](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models) — Udemy course ID 6100015; confidence High; 2026-06.
4. [LangChain- Agentic AI Engineering with LangChain & LangGraph](https://www.udemy.com/course/langchain) — Udemy course ID 5281528; confidence High; 2026-07.
5. [100 Days of Code™: The Complete Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code) — Udemy course ID 2776760; confidence High; 2026-06.
6. [Java Interview Questions Boot Camp - 1000+ Q& A Master Class](https://www.udemy.com/course/java-interview-questions-bootcamp-master-class-1000-java-questions) — Udemy course ID 2456220; confidence High; 2025-07.
7. [FastAPI - The Complete Course 2026 (Beginner + Advanced)](https://www.udemy.com/course/fastapi-the-complete-course) — Udemy course ID 4355412; confidence High; 2026-05.
8. [Python - Полный Курс по Python, Django, Data Science и ML](https://www.udemy.com/course/python-ru) — Udemy course ID 5031680; confidence High; 2026-03.
9. [Искусственный интеллект и Машинное обучение + Основы Python](https://www.udemy.com/course/ai-machinelearning-ru) — Udemy course ID 2374124; confidence High; 2024-10.
10. [\[NEW\] Master Microservices with SpringBoot,Docker,Kubernetes](https://www.udemy.com/course/master-microservices-with-spring-docker-kubernetes) — Udemy course ID 3984552; confidence High; 2026-02.
11. [From Java Dev to AI Engineer: Spring AI Fast Track](https://www.udemy.com/course/java-spring-ai) — Udemy course ID 6745851; confidence High; 2026-07.
12. [The Complete Oracle SQL Bootcamp (2026)](https://www.udemy.com/course/oracle-sql-12c-become-an-sql-developer-with-subtitle) — Udemy course ID 549998; confidence High; 2026-02.
13. [Spring Security with ReactJS, OAuth2, JWT, MFA \| Spring Boot](https://www.udemy.com/course/spring-security-6-with-reactjs-oauth2-jwt-multifactor-authentication) — Udemy course ID 6109339; confidence High; 2026-03.
14. [Kafka MicroServices with Spring Boot, Docker, Kubernetes, AI](https://www.udemy.com/course/apache-kafka-for-developers-using-springboot) — Udemy course ID 1862914; confidence High; 2026-06.
15. [The AI Engineer Course 2026: Complete AI Engineer Bootcamp](https://www.udemy.com/course/the-ai-engineer-course-complete-ai-engineer-bootcamp) — Udemy course ID 6112535; confidence High; 2026-05.
16. [Master statistics & machine learning: intuition, math, code](https://www.udemy.com/course/statsml_x) — Udemy course ID 3160664; confidence High; 2026-06.
17. [Apache Kafka for Event-Driven Spring Boot Microservices](https://www.udemy.com/course/apache-kafka-for-spring-boot-microservices) — Udemy course ID 5552882; confidence High; 2026-06.
18. [Spring Boot Microservices and Spring Cloud. Build & Deploy.](https://www.udemy.com/course/spring-boot-microservices-and-spring-cloud) — Udemy course ID 2144744; confidence High; 2026-06.
19. [Selenium WebDriver with Java -Basics to Advanced+Frameworks](https://www.udemy.com/course/selenium-real-time-examplesinterview-questions) — Udemy course ID 354176; confidence High; 2026-07.
20. [Playwright JS/TS Automation Testing from Scratch & Framework](https://www.udemy.com/course/playwright-tutorials-automation-testing) — Udemy course ID 4574326; confidence High; 2026-05.
21. [Cypress -Modern Automation Testing from Scratch + Frameworks](https://www.udemy.com/course/cypress-tutorial) — Udemy course ID 2470214; confidence High; 2026-03.
22. [Automated Software Testing with Cypress](https://www.udemy.com/course/automated-testing-with-cypress) — Udemy course ID 2299970; confidence High; 2026-06.
23. [Spring AI - GenAI with Telusko](https://www.udemy.com/course/spring-ai-genai) — Udemy course ID 6664991; confidence High; 2025-11.
24. [Spring Boot Unit Testing with JUnit, Mockito and MockMvc](https://www.udemy.com/course/spring-boot-unit-testing) — Udemy course ID 4425116; confidence High; 2026-01.
25. [Testing Java: JUnit 5, Mockito, Testcontainers, REST Assured](https://www.udemy.com/course/testing-java-code-with-junit-5-and-mockito) — Udemy course ID 4602786; confidence High; 2026-06.
26. [Hibernate](https://www.udemy.com/course/hibernate-dmdev) — Udemy course ID 4230386; confidence High; 2021-11.
27. [Computer Science 101: Master the Theory Behind Programming](https://www.udemy.com/course/computer-science-101-master-the-theory-behind-programming) — Udemy course ID 1395136; confidence High; 2026-05.
28. [Software Architecture & Design of Modern Large Scale Systems](https://www.udemy.com/course/software-architecture-design-of-modern-large-scale-systems) — Udemy course ID 3997622; confidence High; 2025-12.
29. [OpenTelemetry Observability For Java Spring Boot Developers](https://www.udemy.com/course/opentelemetry-metrics-tracing-guide) — Udemy course ID 6867677; confidence High; 2026-06.
30. [React - The Complete Guide (incl. Next.js, Redux)](https://www.udemy.com/course/react-the-complete-guide-incl-redux) — Udemy course ID 1362070; confidence High; 2026-01.
31. [The Ultimate React Course 2025: React, Next.js, Redux & More](https://www.udemy.com/course/the-ultimate-react-course) — Udemy course ID 4471614; confidence High; 2025-05.
32. [Docker & Kubernetes: The Complete Practical Guide](https://www.udemy.com/course/docker-complete) — Udemy course ID 3096964; confidence High; 2026-03.
33. [Spring Boot 4, Spring 7 & Hibernate for Beginners](https://www.udemy.com/course/spring-hibernate-tutorial) — Udemy course ID 647428; confidence High; 2026-05.
34. [Reactive Applications with Spring WebFlux Framework](https://www.udemy.com/course/reactive-applications-with-spring-webflux-framework) — Udemy course ID 6168117; confidence High; 2026-06.
35. [Let's Learn Terraform in GCP](https://www.udemy.com/course/lets-learn-terraform-in-gcp) — Udemy course ID 5774134; confidence High; 2024-10.
36. [Understanding TypeScript](https://www.udemy.com/course/understanding-typescript) — Udemy course ID 947098; confidence High; 2026-04.
37. [Java Data Structures & Algorithms + LEETCODE Exercises](https://www.udemy.com/course/data-structures-and-algorithms-java) — Udemy course ID 4218796; confidence High; 2026-04.
38. [Docker & Kubernetes: The Practical Guide](https://www.udemy.com/course/docker-kubernetes-the-practical-guide) — Udemy course ID 3490000; confidence High; 2026-04.
39. [Hibernate and Spring Data JPA: Beginner to Guru](https://www.udemy.com/course/hibernate-and-spring-data-jpa-beginner-to-guru) — Udemy course ID 4022034; confidence High; 2025-11.
40. [Spring Security Zero to Master along with JWT,OAUTH2](https://www.udemy.com/course/spring-security-zero-to-master) — Udemy course ID 3485044; confidence High; 2026-01.
41. [Java Masterclass 2025: 130+ Hours of Expert Lessons](https://www.udemy.com/course/java-the-complete-java-developer-course) — Udemy course ID 533682; confidence High; 2026-05.
42. [GCP for Beginners - Become a Google Cloud Digital Leader](https://www.udemy.com/course/google-cloud-digital-leader-certification) — Udemy course ID 4008228; confidence High; 2026-06.
43. [Terraform for the Absolute Beginners with Labs](https://www.udemy.com/course/terraform-for-the-absolute-beginners) — Udemy course ID 4226208; confidence High; 2024-11.
44. [Build Reactive MicroServices using Spring WebFlux/SpringBoot](https://www.udemy.com/course/build-reactive-restful-apis-using-spring-boot-webflux) — Udemy course ID 1565240; confidence High; 2026-02.
45. [Java Debugging With IntelliJ IDEA](https://www.udemy.com/course/java-debugging-with-intellij-idea) — Udemy course ID 2608314; confidence High; 2025-11.
46. [Full Stack: Angular and Java Spring Boot E-Commerce Website](https://www.udemy.com/course/full-stack-angular-spring-boot-tutorial) — Udemy course ID 1856950; confidence High; 2026-01.
47. [\[NEW\] Spring Boot 4, Spring Framework 7: Beginner to Guru](https://www.udemy.com/course/spring-framework-6-beginner-to-guru) — Udemy course ID 4522192; confidence High; 2025-12.
48. [FULL STACK JAVA DEV: JAVA + JSP + SPRING + BOOT + JS + REACT](https://www.udemy.com/course/full-stack-java-developer-java) — Udemy course ID 1993718; confidence High; 2026-07.
49. [Spring WebFlux: Microservices Patterns & Advanced Resilience](https://www.udemy.com/course/spring-webflux-patterns) — Udemy course ID 4651564; confidence High; 2026-06.
50. [Spring WebFlux Masterclass: High-Performance Reactive APIs](https://www.udemy.com/course/spring-webflux) — Udemy course ID 3868548; confidence High; 2026-06.
51. [Java Design Patterns & SOLID Design Principles](https://www.udemy.com/course/design-patterns-in-java-concepts-hands-on-projects) — Udemy course ID 1568344; confidence High; 2025-01.
52. [600+ Spring Interview Questions Practice Test](https://www.udemy.com/course/spring-interview-questions) — Udemy course ID 5742462; confidence High; 2026-04.
53. [Java Interview Masterclass: Top 350 Questions (PDF)(2026)](https://www.udemy.com/course/top-250-java-interview-questions) — Udemy course ID 6065245; confidence High; 2025-12.
54. [Angular - The Complete Guide](https://www.udemy.com/course/the-complete-guide-to-angular-2) — Udemy course ID 756150; confidence High; 2026-04.
55. [The Git & Github Bootcamp](https://www.udemy.com/course/git-and-github-bootcamp) — Udemy course ID 3792262; confidence High; 2026-01.
56. [Spring](https://www.udemy.com/course/spring-dmdev) — Udemy course ID 4384840; confidence High; 2022-08.
57. [Spring - Полный курс. Boot, Hibernate, Security, REST.](https://www.udemy.com/course/spring-alishev) — Udemy course ID 4345538; confidence High; 2022-10.
58. [Integration Testing with Testcontainers: Java & Spring Boot](https://www.udemy.com/course/testcontainers-integration-testing-java-spring-boot) — Udemy course ID 6525217; confidence High; 2025-11.
59. [\[NEW\] Master Spring Boot Microservice & Angular K8s CICD AWS](https://www.udemy.com/course/master-spring-boot-microservice-angular-with-k8s-cicd-aws) — Udemy course ID 5441346; confidence High; 2026-05.
60. [Design Patterns in Java](https://www.udemy.com/course/design-patterns-java) — Udemy course ID 1358570; confidence High; 2020-04.
61. [Java Full Stack(Spring Boot, Spring AI, React, Stripe, AWS )](https://www.udemy.com/course/java-full-stack-mastery-spring-boot-react-stripe-aws) — Udemy course ID 6189983; confidence High; 2025-09.
62. [The Complete Full-Stack Web Development Bootcamp](https://www.udemy.com/course/the-complete-web-development-bootcamp) — Udemy course ID 1565838; confidence High; 2025-11.
63. [Master the Coding Interview: Data Structures + Algorithms](https://www.udemy.com/course/master-the-coding-interview-data-structures-algorithms) — Udemy course ID 1917546; confidence High; 2026-03.
64. [OAuth 2.0 in Spring Boot Applications](https://www.udemy.com/course/oauth2-in-spring-boot-applications) — Udemy course ID 3219295; confidence High; 2026-06.
65. [Event-Driven Microservices, CQRS, SAGA, Axon 4, Spring Boot](https://www.udemy.com/course/spring-boot-microservices-cqrs-saga-axon-framework) — Udemy course ID 3698214; confidence High; 2026-06.
66. [Spring Boot Microservices with Spring Cloud Beginner to Guru](https://www.udemy.com/course/spring-boot-microservices-with-spring-cloud-beginner-to-guru) — Udemy course ID 2313280; confidence High; 2025-11.
67. [Event-Driven Microservices: Spring Boot, Kafka and Elastic](https://www.udemy.com/course/event-driven-microservices-spring-boot-kafka-and-elasticsearch) — Udemy course ID 3599404; confidence High; 2026-01.
68. [Deploy Java Spring Apps Online to Amazon Cloud (AWS)](https://www.udemy.com/course/deploy-java-spring-apps-online) — Udemy course ID 1599662; confidence High; 2026-01.
69. [Java Spring Boot Full Stack: eCommerce Project Masterclass](https://www.udemy.com/course/spring-boot-using-intellij-build-a-real-world-project) — Udemy course ID 4298517; confidence High; 2026-05.
70. [Java Multithreading, Concurrency & Performance Optimization](https://www.udemy.com/course/java-multithreading-concurrency-performance-optimization) — Udemy course ID 1656228; confidence High; 2026-07.
71. [Learn Redis And Use Jedis With Spring Data Redis](https://www.udemy.com/course/1701332/) — Udemy course ID 1701332; confidence Low; Unknown.
72. [Reactive Redis Masterclass For Java Spring Boot Developers](https://www.udemy.com/course/spring-webflux-redis) — Udemy course ID 4176592; confidence High; 2026-06.
73. [Redis: The Complete Developer's Guide](https://www.udemy.com/course/redis-the-complete-developers-guide-p) — Udemy course ID 4672206; confidence High; 2026-02.
74. [Apache Kafka Series - Learn Apache Kafka for Beginners v3](https://www.udemy.com/course/apache-kafka) — Udemy course ID 1075642; confidence High; 2026-07.
75. [Devops Fundamentals - CI/CD with AWS +Docker+Ansible+Jenkins](https://www.udemy.com/course/devops-fundamentals-aws) — Udemy course ID 3236235; confidence High; 2024-12.
76. [Docker Mastery: with Kubernetes +Swarm from a Docker Captain](https://www.udemy.com/course/docker-mastery) — Udemy course ID 1035000; confidence High; 2025-09.
77. [Appium -Mobile Testing (Android/IOS) from Scratch+Frameworks](https://www.udemy.com/course/mobile-automation-using-appiumselenium-3) — Udemy course ID 246314; confidence High; 2026-03.
78. [Learn Cucumber BDD with Java -MasterClass Selenium Framework](https://www.udemy.com/course/cucumber-tutorial) — Udemy course ID 1560542; confidence High; 2026-03.
79. [Complete Linux Training Course to Get Your Dream IT Job 2026](https://www.udemy.com/course/complete-linux-training-course-to-get-your-dream-it-job) — Udemy course ID 1523066; confidence High; 2026-05.
80. [Understanding NPM - Node.js Package Manager](https://www.udemy.com/course/understanding-npm) — Udemy course ID 1869566; confidence High; 2026-03.
81. [Full Stack: React and Java Spring Boot - The Developer Guide](https://www.udemy.com/course/full-stack-react-and-java-spring-boot-the-developer-guide) — Udemy course ID 4659752; confidence High; 2026-02.
82. [Business Model Innovation: Differentiate & Grow Your Company](https://www.udemy.com/course/disruptive-innovation-business-model-startup) — Udemy course ID 1030316; confidence High; 2026-02.
83. [The Project Management Course: Beginner to PROject Manager](https://www.udemy.com/course/the-project-management-course-beginner-to-project-manager) — Udemy course ID 1978132; confidence High; 2026-04.
84. [Business Analysis Fundamentals - IIBA endorsed](https://www.udemy.com/course/business-analysis-ba) — Udemy course ID 751792; confidence High; 2025-09.
85. [Rest API Testing (Automation) from Scratch-Rest Assured Java](https://www.udemy.com/course/rest-api-automation-testing-rest-assured) — Udemy course ID 694982; confidence High; 2026-04.
86. [Bash Scripting and Shell Programming (Linux Command Line)](https://www.udemy.com/course/bash-scripting) — Udemy course ID 958532; confidence High; 2026-07.
87. [WebDriverIO + Node.js -JavaScript UI Automation from Scratch](https://www.udemy.com/course/webdriverio-tutorial-nodejs-javascript) — Udemy course ID 3943902; confidence High; 2025-03.
88. [Python Basics](https://www.udemy.com/course/2435072/) — Udemy course ID 2435072; confidence Low; Unknown.
89. [Business Analysis: Functional & Non-Functional Requirements](https://www.udemy.com/course/identify-functional-and-non-functional-requirements) — Udemy course ID 288590; confidence High; 2026-03.
90. [Learn JMETER from Scratch on Live Apps -Performance Testing](https://www.udemy.com/course/learn-jmeter-from-scratch-performance-load-testing-tool) — Udemy course ID 380872; confidence High; 2025-07.
91. [Hibernate: Advanced Development Techniques](https://www.udemy.com/course/hibernate-tutorial-advanced) — Udemy course ID 1848328; confidence High; 2026-01.
92. [Design Patterns in JavaScript](https://www.udemy.com/course/design-patterns-javascript) — Udemy course ID 2251868; confidence High; 2021-08.
93. [Postman: The Complete Guide - REST API Testing](https://www.udemy.com/course/postman-the-complete-guide) — Udemy course ID 1265410; confidence High; 2025-11.
94. [Advanced Java Topics: Java Reflection - Master Class](https://www.udemy.com/course/java-reflection-master-class) — Udemy course ID 2916558; confidence High; 2025-09.
95. [Event Driven Microservices with CQRS, Saga, Event Sourcing](https://www.udemy.com/course/event-driven-microservices-with-cqrs-saga-event-sourcing) — Udemy course ID 6194627; confidence High; 2025-12.
96. [Microservices: Clean Architecture, DDD, SAGA, Outbox & Kafka](https://www.udemy.com/course/microservices-clean-architecture-ddd-saga-outbox-kafka-kubernetes) — Udemy course ID 4517270; confidence High; 2026-06.
97. [Mastering Java Reactive Programming \[ From Scratch \]](https://www.udemy.com/course/complete-java-reactive-programming) — Udemy course ID 3788696; confidence High; 2026-06.
98. [Master Generative AI for Developer Productivity With Pieces](https://www.udemy.com/course/mastering-generative-ai-for-developer-productivity) — Udemy course ID 6072251; confidence High; 2026-06.
99. [Java Spring Boot Microservices eCommerce Project Masterclass](https://www.udemy.com/course/java-spring-boot-microservices-with-spring-cloud-k8s-docker) — Udemy course ID 6072261; confidence High; 2026-05.
100. [Master Microservices with Spring Boot and Spring Cloud](https://www.udemy.com/course/microservices-with-spring-boot-and-spring-cloud) — Udemy course ID 1352468; confidence High; 2026-05.
101. [Apache Maven](https://www.udemy.com/course/maven-dmdev) — Udemy course ID 4176008; confidence High; 2022-03.
102. [Gradle](https://www.udemy.com/course/gradle-dmdev) — Udemy course ID 4216004; confidence High; 2021-10.
103. [AWS Serverless REST APIs for Java Developers. CI/CD included](https://www.udemy.com/course/aws-serverless-rest-apis-for-java-developers) — Udemy course ID 2569122; confidence High; 2025-12.
104. [gRPC Java: High-Performance Spring Boot Microservices](https://www.udemy.com/course/grpc-the-complete-guide-for-java-developers) — Udemy course ID 3576019; confidence High; 2026-06.
105. [AI Builder: Create Agents, Voice Agents & Automations in n8n](https://www.udemy.com/course/ai-builder-with-n8n-create-agents-voice-agents) — Udemy course ID 6973513; confidence High; 2026-06.
106. [AI Engineer Agentic Track: The Complete Agent & MCP Course](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course) — Udemy course ID 6566789; confidence High; 2026-06.
