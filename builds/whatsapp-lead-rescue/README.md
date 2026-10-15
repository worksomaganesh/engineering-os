# WhatsApp Lead Rescue — Never Let a Sales Conversation Go Cold

> **One-line promise:** We stop WhatsApp leads from being forgotten.

**Status:** Researched project concept and implementation blueprint. This documentation describes a proposed product; it does not imply that a working application or official WhatsApp integration already exists.

## 1. The Problem

A coaching institute, real-estate broker, manufacturer, clinic, or agency receives leads through WhatsApp. One person asks for pricing, a salesperson promises to send details, many other messages arrive, and that promise gets buried. Nobody sees that the lead has been waiting, so the quote or follow-up is delayed and a potential customer goes elsewhere.

The central problem is not necessarily "we need a huge CRM." It is:

**"Which conversations need action right now, who owns them, and what exactly did we promise?"**

WhatsApp Lead Rescue is an action layer around conversations: detect possible next actions, show evidence for why they matter, assign an owner, and remind the right person.

## 2. Research Signal — Not Proof of Product-Market Fit

A May 2026 report by HelloGrowthCRM says it analyzed activity and survey data from 527 Indian SMBs. It reports that 67% of surveyed businesses used WhatsApp as their primary initial sales channel and that businesses replying within five minutes closed 3.7 times as many deals as those responding after 60 minutes. The report discloses that it is vendor research rather than an independent academic study, so treat the figures as directional and do not interpret them as a guaranteed causal effect. [Report and methodology](https://hellogrowthcrm.com/resources/original-research).

This is a useful hypothesis generator, not proof that this product will succeed. Interview sellers and observe their workflow before making market-size or revenue claims. Social and Reddit anecdotes can reveal pain points but are qualitative signals, not reliable statistical validation.

WhatsApp has both a Business app and a Business Platform/API. Meta's official developer hub documents API access, webhooks, test resources, opt-in guidance, and pricing. [WhatsApp Business Developer Hub](https://whatsappbusiness.com/developers/developer-hub/) · [WhatsApp Business product overview](https://faq.whatsapp.com/general/whatsapp-business-api/about-whatsapp-business-products?lang=en).

**Pricing timing:** researched on 15 October 2026. Recent published coverage reports WhatsApp Business Platform pricing changes effective 1 October 2026. Exact rates, allowances, provider fees, and eligibility can vary or change. Verify the current Meta pricing page and the business account's own billing settings before calculating costs; never hard-code rates from a third-party blog. [Official pricing entry point](https://whatsappbusiness.com/developers/developer-hub/) · [Recent change coverage](https://www.moneycontrol.com/technology/whatsapp-business-platform-pricing-changes-from-october-1-here-s-what-businesses-need-to-know-article-14042527.html).

## 3. Product Philosophy

Do not replace WhatsApp in the first release. Build a narrow action queue that answers:
1. Which conversation deserves attention first?
2. Why is it on this list?
3. What action is expected, and by whom?
4. When should that action happen?

The product should improve follow-up discipline, ownership, and visibility—not bombard leads with automatic messages.

## 4. Core Lifecycle

~~~text
NEW
 ↓
QUALIFIED
 ↓
QUOTE SENT
 ↓
WAITING FOR CUSTOMER
 ↓
FOLLOW-UP DUE
 ↓
WON / LOST
~~~

Real workflows branch and loop. A lead may be disqualified early, a quote may be revised, or the customer may ask a new question. Store lead stage, who is expected to respond next, and internal task status separately. AI must not mark a deal WON or LOST from a vague phrase alone.

## 5. MVP: Chat Export → Action Dashboard

1. The user exports a conversation from WhatsApp/WhatsApp Business.
2. The user uploads the exported text to a private workspace.
3. The app parses messages, timestamps, and sender labels.
4. It detects candidate inbound questions, unanswered latest messages, promises, quote/proposal/demo mentions, and suggested actions.
5. The user reviews the evidence and corrects mistakes.
6. A dashboard shows "Follow-ups due now", owner, reason, age, next action, and due time.
7. The app creates in-app reminders or another explicitly configured reminder channel.

WhatsApp's Help Center explains exporting a chat through **More → Export chat**, with media optionally included. The export is a text file and cannot be re-imported as a WhatsApp backup. [Official export-chat guidance](https://faq.whatsapp.com/1180414079177245/?cms_platform=android&locale=en).

The MVP does not scrape the inbox, sync live messages, or send WhatsApp messages. A deliberate user-initiated export keeps scope small and validates whether the action dashboard solves the pain.

## 6. What the Killer Screen Looks Like

> **FOLLOW-UPS DUE NOW**
>
> - **Rahul** — asked for the ₹80k package — no company reply detected for 19 hours
> - **Priya** — quote discussed yesterday — confirm whether it was actually sent
> - **ABC Industries** — requested a technical proposal — a promised action appears overdue
> - **Karthik** — asked for a demo — no next action recorded

These are illustrative examples, not real customers. Every row must show why it was detected and allow a user to correct the system.

## 7. Documentation Pack

- [Product requirements and user journey](product-requirements.md)
- [Technical architecture and event pipeline](technical-architecture.md)
- [Data model and conversation evidence](data-model.md)
- [Dashboard UX and prioritization](ux-and-workflows.md)
- [Evaluation and test plan](evaluation-plan.md)
- [Security, privacy, and WhatsApp policy controls](security-and-compliance.md)
- [Roadmap, validation, and business model](roadmap.md)

## 8. Initial Target Segment

Do not build an all-industry CRM on day one. Interview coaching/training institutes, real-estate businesses, agencies/B2B services, manufacturers, and distributors. Choose a segment based on repeated pain and actual message patterns.

Clinics may have this problem too, but health-related data raises extra privacy and WhatsApp-policy concerns. Treat healthcare as a separately reviewed later segment, rather than casually processing sensitive health conversations in a general-purpose AI system.

## 9. Success Metrics

- Conversation import and parse success by format.
- Precision/recall for actionable leads and unanswered messages.
- Percentage of extracted commitments accepted or corrected.
- On-time completion rate for due tasks.
- Median inbound-to-first-human-response time.
- Follow-ups rescued that users say would otherwise have been missed.
- Time spent correcting imported data.
- Weekly active usage, repeat usage, and willingness to pay.
- Processing cost per conversation.
- Message delivery/template approval/cost only after official integration exists.

Measure against each pilot business's own baseline. Don't promise a fixed percentage improvement based on a vendor benchmark.

## 10. Research Sources

- [WhatsApp Business Developer Hub](https://whatsappbusiness.com/developers/developer-hub/)
- [Meta's official WhatsApp Cloud API Postman collection](https://www.postman.com/meta/whatsapp-business-platform/overview?sideView=agentMode)
- [WhatsApp Business Messaging Policy](https://business.whatsapp.com/policy/preview?lang=en)
- [WhatsApp Help Center: export chat](https://faq.whatsapp.com/1180414079177245/?cms_platform=android&locale=en)
- [WhatsApp Business product overview](https://faq.whatsapp.com/general/whatsapp-business-api/about-whatsapp-business-products?lang=en)
- [HelloGrowthCRM Indian SMB CRM Benchmark Report, May 2026](https://hellogrowthcrm.com/resources/original-research) — vendor research, directional rather than independent validation
- [Moneycontrol: October 2026 pricing-change coverage](https://www.moneycontrol.com/technology/whatsapp-business-platform-pricing-changes-from-october-1-here-s-what-businesses-need-to-know-article-14042527.html)
- [MeitY: Digital Personal Data Protection Rules, 2025](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa?pageTitle=Digital-Personal-Data-Protection-Rules-2025)

**Boundary:** this is a proposed decision-support product. A live messaging integration must follow current Meta/WhatsApp terms, opt-in and opt-out requirements, approved-template rules where applicable, security practices, and relevant law.
