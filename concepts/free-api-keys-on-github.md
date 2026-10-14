# Why Are Some API Keys Shared Publicly on GitHub?

This concept explains an apparent contradiction:

- We learn that private API keys should **not** be committed to GitHub.
- Yet some GitHub repositories advertise free APIs, free LLM access, or even shared API keys.

There is no contradiction once we distinguish **an API directory**, **a free key you obtain for yourself**, **an intentionally shared credential**, and **an accidentally exposed secret**. These are different things.

## 1. First, distinguish free APIs from free API keys

### A. A directory that lists APIs

A repository such as [public-apis/public-apis](https://github.com/public-apis/public-apis) is primarily a catalogue of APIs. Its entries describe services and link to their websites or documentation. Its authentication column may say that an API requires a key.

That does **not** mean the repository publishes a working key belonging to the maintainer.

For example, a directory might list:

| API entry | Authentication field | What the listing tells you |
|---|---|---|
| Example weather service | apiKey | Visit the provider's site and follow its signup process. |
| Example public-data service | None | The service may allow requests without a key. |
| Example account service | OAuth | Use the provider's authorised sign-in or consent flow. |

These are illustrative examples, not current claims about particular providers.

If a listing says that authentication is required, it usually means **you must obtain a key** according to the provider's instructions. The directory is not necessarily giving you someone else's key.

### B. A directory of free-tier API providers

A GitHub topic such as [free-llm-api](https://github.com/topics/free-llm-api) groups projects related to free or low-cost language-model APIs. It is a topic page, not one single service. Repositories under it can have different purposes and trust levels.

Many projects list providers, available models, official signup links, free-tier terms, rate limits, and SDK instructions. In those cases, “free API keys” often means **the providers allow users to obtain their own keys under a free plan or trial**.

Other projects under similar topics may offer shared credentials or shared gateways. Inspect the specific project to understand which kind of access it provides.

### C. A project that actually publishes shared access

Some projects explicitly offer shared credentials or an intermediary endpoint so multiple users can try an API without each setting up a separate provider account.

That is different from listing providers. It may be an intentional community service, an authorised programme, a limited giveaway, or an implementation whose authorisation is unclear. Public visibility alone does not tell you which one it is.

**Key lesson:** “Free API,” “free API key,” and “shared API key” are not interchangeable.

## 2. Why would someone share a working API key?

The motivation depends on the project; do not assume the same explanation applies to every repository.

### Reason 1 — Community support

A developer may deliberately allocate some resources to help students, hobbyists, or open-source developers experiment.

For example, someone might receive an authorised promotional allocation and choose to share a limited portion with a community. They are offering limited access, not necessarily unlimited use of their whole account.

### Reason 2 — Limited budget or temporary access

A shared-access project may set limits on how much can be used or how long access remains available. Where supported, the provider or operator might configure:
- A spending or credit budget.
- Request-rate limits.
- Token or usage quotas.
- An expiration time.
- Revocation when the offer ends.

For illustration only, imagine a shared service with a $20 budget, five requests per minute, and a 24-hour lifetime. These are made-up numbers, not real credentials or limits from any provider.

Once the allowance is consumed or expires, requests may fail until a reset or until the operator provides valid new access.

### Reason 3 — Promotion or business goals

A free-access project may help its creator attract users, collect feedback, demonstrate a tool, build reputation, find contributors, or promote another product.

“Free” does not necessarily mean the provider or maintainer has no other objective. A legitimate service may offer free usage to encourage adoption and may also have paid plans.

### Reason 4 — A shared API gateway or proxy

A project may provide a gateway rather than revealing the upstream provider's raw key.

```text
Many users
    |
    v
Shared gateway operated by a project
    |
    | Checks access, quotas, and usage
    v
Upstream provider API
    |
    v
Gateway returns the result
```

In this model, the operator keeps upstream credentials on its server. Users send requests to the gateway, which forwards permitted requests using the operator's credentials.

A gateway can implement user authentication, rate limiting, spending controls, model routing, logging, and failover. The quality of these protections depends on how it is built.

There is also a trust trade-off: depending on the design, the operator may be able to inspect or log prompts, responses, metadata, and other request details. Do not send confidential information unless the gateway's privacy and security practices are appropriate for it.

### Reason 5 — The key is leaked or shared without permission

Not every repository exposing a working key is a legitimate giveaway. A credential could be:
- Accidentally committed by its owner.
- Copied from another source without permission.
- Published by someone who does not control the account.
- Expired, revoked, or already exhausted.
- A placeholder or fake value that does not work.
- Advertised in a way that exaggerates what the project provides.

**A key being publicly visible does not establish that its use or distribution is authorised.**

## 3. Doesn't the shared key's quota get exhausted?

**Yes. A shared allowance can be consumed by the combined usage of everyone using it.** This is one of the main trade-offs of shared access.

Imagine a hypothetical shared credential that permits 1,000 requests per day:
- You send 100 requests.
- Ten other users send 100 requests each.
- Another user sends 200 requests.

Combined usage:

```text
100 + (10 × 100) + 200 = 1,300 requests
```

That is 300 more requests than the hypothetical daily allowance. Some requests may be rejected once the applicable quota is exhausted.

These are made-up numbers. Real quota rules depend on the provider and account.

### Different kinds of limits

| Limit | Meaning |
|---|---|
| Requests per minute (RPM) | Limits how quickly requests can be made over a minute. |
| Requests per day (RPD) | Limits the number of requests in a day. |
| Tokens per minute (TPM) | Limits input/output token use over a period, where the provider measures it this way. |
| Usage budget | Limits spending or credit, if the provider or gateway supports it. |
| Expiration time | The credential or temporary grant stops being valid after a specified time. |
| Concurrency limit | Limits how many requests or operations may run simultaneously. |

The provider may enforce limits at different levels, such as a key, user, project, account, model, or shared quota pool. Check the provider's current documentation.

When a limit is reached, requests may be rate-limited, rejected due to exhausted quota, blocked by budget controls, or fail because the key has expired or been revoked. The repository may remain public even when the shared service no longer works.

## 4. How can a project provide new keys repeatedly?

Some projects may rotate credentials, replenish a budget, add a newly authorised allocation, or aggregate multiple providers behind a gateway. A gateway might route to another permitted model when one provider's allowance runs out.

But **creating another API key does not necessarily create another independent allowance**.

For example:
- Ten keys associated with the same project may share one quota pool.
- A key may have an individual limit and also be subject to an account-level limit.
- A free-tier allocation may reset according to the provider's rules.
- A new key may not help if the account or model quota is exhausted.

The number of published keys alone does not tell you how much usable capacity exists.

Creating keys or accounts to bypass usage limits may violate provider policies. Legitimate shared services should follow provider terms and have appropriate authorisation.

## 5. Why doesn't this contradict our API-key security rule?

The practical rule remains:

> **Do not commit private API keys to GitHub.**

This advice applies to credentials that must remain secret, especially personal credentials linked to an account, billing, private data, or usage limits.

There are legitimate cases where a service intentionally exposes a restricted public key or an owner authorises a sharing arrangement. Those exceptions do not make every secret key safe to publish.

| Situation | How to think about it |
|---|---|
| Your own private paid API key | Keep it secret; someone else could use your quota or create charges, depending on the provider. |
| Your own free-tier key linked to your account | Usually keep it secret; quota can still be exhausted or access misused. |
| A placeholder such as YOUR_API_KEY in sample code | Usually safe because it is not a real credential. |
| A directory linking to an official free-tier signup page | Usually fine; users obtain their own credentials. |
| A deliberately public, restricted key documented by the provider for public use | May be appropriate within the provider's intended restrictions. |
| An explicitly authorised shared gateway | May be appropriate, depending on security, privacy, limits, and terms. |
| A leaked or stolen secret | Public availability does not make its use authorised. |

The important questions are: **Who owns this credential? What permissions does it grant? Has the owner or provider authorised this use?**

## 6. Why do shared keys stop working?

A key copied from a public repository may fail for several reasons:

1. **Quota exhausted:** Other users consumed the available allowance.
2. **Rate limit reached:** Too many requests were sent during the relevant interval.
3. **Expired or revoked:** The owner or provider disabled it, or its temporary validity ended.
4. **Account-level restriction:** A limit on the underlying project or account affects several keys.
5. **Provider policy changed:** Free-tier terms, supported models, endpoints, or eligibility changed.
6. **Gateway unavailable:** The intermediary service is offline, overloaded, or no longer funded.
7. **The key was never valid:** It was a placeholder or an inaccurate claim.

A repository being maintained does not guarantee that every external key or service listed there works at this exact moment.

## 7. Risks of using random shared keys

### Reliability

Many unrelated users may consume the same allowance. Your test may work once and fail later.

### Privacy

A proxy operator may log prompts and responses. Avoid confidential data unless you trust the service and its handling practices.

### Ownership and authorisation

A published key may have been leaked or shared without permission. Public visibility is not proof of consent.

### Security

A key may have broader permissions than necessary. The impact of misuse depends on what it can access.

### Accountability

You may not know who operates the service, how it is monitored, or how problems will be handled.

For a harmless experiment, an authorised and trustworthy shared service with clear limits may be acceptable. For serious projects, prefer credentials you control or a reputable, well-documented gateway.

## 8. A safer way to get free API access

For a personal project:

1. Find a provider in a directory or curated list.
2. Open the provider's official website and documentation.
3. Check its current free-tier limits, supported models, and signup requirements.
4. Create your own account and credential if required.
5. Restrict the key's permissions, project, origin, or IP address where supported.
6. Keep private credentials out of committed files.
7. Monitor usage and rotate or revoke a credential if exposed.
8. Check provider terms before deploying the project or sharing access.

Example local `.env` file:

```dotenv
# Local .env file — do not commit the real secret
OPENAI_API_KEY=your_own_key_goes_here
```

Example `.gitignore` rules:

```gitignore
.env
.env.*
!.env.example
```

A committed `.env.example` should contain placeholders rather than working credentials.

Environment variables are not automatically secret in a frontend application: a frontend build may embed values in code delivered to the browser.

If a real secret is committed, revoke or rotate it promptly. Removing it from the latest file or rewriting Git history does not invalidate a credential that someone has already copied.

## 9. How to assess a repository claiming to share keys

Before relying on a project, inspect it critically:

- Does it link to official signup pages, or paste credentials directly?
- Does it explain how access is authorised and funded?
- Does it state limits and what happens when they are exhausted?
- Does it use an operator-controlled gateway?
- Does it explain whether prompts, responses, or metadata may be logged?
- Do the provider's terms permit the intended use and sharing arrangement?
- Is it maintained, and are its limitations stated honestly?
- Does it ask you to run an unknown script or send a local credential to a third party?

No individual signal proves that a project is trustworthy. A large number of stars or forks is not proof of authorisation, security, or ongoing availability.

## 10. Common misconceptions

### “Every repository in a free-API topic gives away working keys.”

No. GitHub topics group many kinds of projects. Many list providers, free-tier details, signup links, or client libraries. Others may offer shared credentials or gateway access.

### “A free key has no risk.”

No. Free quotas can be exhausted, and the credential may still connect to an account with permissions or billing implications.

### “If a shared key works today, it will work tomorrow.”

Not necessarily. It may reach a quota, expire, be revoked, or depend on a gateway that stops operating.

### “Creating more keys always increases the quota.”

No. Multiple keys may share one account- or project-level allowance.

### “A key visible on GitHub is authorised for public use.”

No. It may have been exposed accidentally or published by someone without permission.

### “A gateway is the same as receiving a provider key.”

No. With a gateway, the operator manages the upstream connection and may process your requests. You rely on its controls, availability, and privacy practices.

### “If a key is free, there's no reason to get my own.”

Your own key gives you direct control over permissions, usage, monitoring, and revocation. Shared access may suit a limited experiment, but it is not automatically a suitable foundation for a production project.

## 11. Questions for revision

Try answering these before checking the key.

1. What is the difference between a free API directory and a shared-key repository?
2. If a catalogue says an API requires a key, does it mean the catalogue provides a working key?
3. Why might someone intentionally share limited API access?
4. What is an API gateway, and how does it differ from distributing an upstream key?
5. Why can a shared key's quota be exhausted?
6. What is the difference between a request-rate limit and a usage budget?
7. Why don't multiple keys necessarily mean multiple independent quotas?
8. Why is public visibility not proof of authorisation?
9. Name two risks of sending prompts through an unknown shared gateway.
10. What is the safer way to obtain a key for your own project?
11. What should you do if your private key is exposed?
12. Why must you check the provider's terms before using a shared-access service?

### Answer key

1. A directory points users to APIs and information; a shared-key repository offers credentials or an intermediary service shared among users.
2. No. It normally indicates that a key is required; users usually obtain their own from the provider.
3. Community support, a promotional allocation, a funded limited grant, or another authorised purpose.
4. A gateway accepts requests and forwards them to upstream services. It can keep upstream credentials on its server but requires users to trust the operator.
5. All users draw from a limited allowance and collectively reach a rate, request, token, or spending limit.
6. A rate limit restricts usage over time; a budget restricts consumption of allocated money or credit, where supported.
7. Several keys may belong to one project or account and share its quota.
8. A secret may have been exposed accidentally or shared without permission.
9. The operator may log prompts and outputs; the service may also be unreliable or poorly secured.
10. Use the provider's official site, create your own authorised credential, configure it securely, and monitor its use.
11. Revoke or rotate it promptly, review usage, remove it from current code, and clean up history as appropriate.
12. Providers can restrict how their services and credentials are used or shared; a public repository does not override those terms.

## 12. Key takeaway

> **A GitHub repository listing free APIs is not necessarily publishing working API keys. Some repositories point you to a provider so you can obtain your own free key; others offer shared credentials or a gateway. Shared access can work, but its quotas may be exhausted, keys may expire, and authorisation and privacy must be checked.**

The security rule has not changed:

**Keep private credentials out of your repository. Use your own authorised key or a trustworthy, authorised service with clearly documented limits.**

## Further reading

- [Public APIs directory](https://github.com/public-apis/public-apis)
- [GitHub's free-llm-api topic](https://github.com/topics/free-llm-api)
- [Google Cloud: Best practices for managing API keys](https://docs.cloud.google.com/docs/authentication/api-keys-best-practices)
- [Google API Console: Best practices for securely using API keys](https://support.google.com/googleapi/answer/6310037)
- [Engineering OS: API Keys and Secrets](api-keys-and-secrets.md)
