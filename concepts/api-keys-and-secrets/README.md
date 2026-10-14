# API Keys and Secrets: Why They Must Stay Out of GitHub

API keys and other credentials allow software to identify itself or access a service. Depending on how a credential is configured, it may allow requests to be made using your account, consume your quota, access data, or perform operations.

**A secret API key should not be committed to a GitHub repository alongside your project code.** If someone obtains a usable key, they may be able to use it without your permission.

The safest general practice is to keep project code in version control and keep secret credentials in environment variables, a secrets manager, or your hosting provider's secret configuration.

## 1. What Is an API Key?

An **API key** is a string a service uses to identify a caller or application and, depending on the service, control access, usage quotas, or billing.

Imagine building an AI application that calls an AI provider's API. Your application may need a credential to send requests. The provider can use that credential to associate requests with a project or account and apply the rules configured for it.

A fake example might look like this:

```python
api_key = "sk-example123456"
```

This is a made-up example, not a real credential.

API keys do not all grant the same access. Some identify an application, some have limited permissions, and some are designed to be public. Unless a provider explicitly documents a key as safe to expose, treat it as a secret.

## 2. Why Shouldn't a Secret API Key Be Uploaded to GitHub?

A public GitHub repository can be viewed, cloned, or copied by other people. If a real secret key is committed to source code, other people may obtain and misuse it.

### Risk 1: Unexpected usage or charges

Suppose your API provider charges according to requests or usage. If someone copies an exposed key, they may use it to make requests that consume your quota or create charges associated with your project, depending on the provider's billing arrangement.

### Risk 2: Unauthorized access to services or data

The impact depends on what the credential permits. A key may provide access to specific API operations, data, or resources. If it has broader permissions than necessary, the potential damage can be greater.

This is why credentials should have the minimum permissions required for their task. This principle is called **least privilege**.

### Risk 3: Automated discovery

Public repositories can be scanned by automated tools that look for exposed credentials. You should not assume that a secret is safe simply because your repository is new, has few visitors, or is unlikely to attract attention.

GitHub provides secret-scanning and push-protection features for supported secrets and repositories. These features can help detect or prevent some leaks, but they are not a substitute for keeping credentials out of source code.

### Risk 4: Removing the key later may not be enough

Git records changes over time. If a secret was committed, it may remain in prior commits even after the file is edited. Someone may also have copied the key before it was removed.

**Removing a leaked key from the latest file does not invalidate the credential.** You must revoke or rotate it with the provider.

### Risk 5: Misuse of your account or project

Depending on its permissions, an exposed credential may be used to access restricted resources, modify data, consume quotas, or perform other unauthorized operations. The exact risk depends on the service and the credential's scope.

## 3. Does This Apply to Private Repositories?

Yes. A private repository limits who can view the repository, but it is not a secure secret store.

Secrets may still be exposed through accidental sharing, compromised accounts, logs, copied files, or other incidents. Keep private credentials out of committed source code in both public and private repositories.

A deliberate exception is a credential that the service explicitly designs for public use, such as certain browser-restricted public keys. Follow the provider's documentation, apply the intended restrictions, and do not confuse a publishable identifier with a secret server-side credential.

## 4. The Safer Pattern: Keep Code and Secrets Separate

A project should obtain private credentials from its runtime environment or an appropriate secret-management system rather than embedding them in the source code.

### Unsafe: hardcoding a secret

```python
api_key = "sk-your-real-secret-key"
```

This places the key directly in the source file. If that file is committed, the secret can be exposed.

### Safer: read the key from an environment variable

```python
import os

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not configured")
```

The code refers to the variable by name, while the actual credential is supplied separately when the program runs.

This pattern helps separate the application code from environment-specific configuration. The environment variable itself must still be set securely and should not be printed in logs or error messages.

## 5. Using a .env File for Local Development

For local development, many projects use a file named `.env` to keep environment variables in one place.

Example local `.env` file:

```dotenv
OPENAI_API_KEY=your_real_key_goes_here
```

Replace the placeholder locally with your actual credential. Do not commit this file to GitHub.

A library such as a dotenv loader may be needed for your programming language to load the file into the process environment. Follow the setup instructions for the library used in your project.

### Add .env to .gitignore

At the root of your repository, add rules like these to `.gitignore`:

```gitignore
.env
.env.*
!.env.example
```

These rules ignore `.env` and similarly named environment files while allowing `.env.example` to be committed. Adjust the rules if your project deliberately uses other environment-file conventions, and verify which files are staged before committing.

**Important:** `.gitignore` prevents untracked matching files from being added normally; it does not automatically remove a file that Git is already tracking. If a secret file has already been committed, remove it from tracking as appropriate and revoke the exposed credential.

## 6. Commit an .env.example File Instead

Other developers need to know which environment variables the project requires. You can document the expected variables without publishing their real values.

Example `.env.example`:

```dotenv
OPENAI_API_KEY=replace_with_your_own_key
```

This placeholder is not a working API key. A developer who clones the repository can copy the example to a local `.env` file and supply their own credential.

For projects that use multiple settings, the example file can document each variable with safe placeholders. Never include working credentials in the example.

## 7. Configure Secrets in the Deployment Environment

When you deploy an application, configure its credentials using your hosting platform's secret settings or a suitable secrets manager.

A common deployment pattern is:

```text
Project code is stored in GitHub
             |
             v
Application is deployed
             |
             v
Hosting environment supplies the secret securely
             |
             v
Backend reads the credential at runtime
             |
             v
Backend calls the external API
```

For production systems, a managed secrets service may provide better access controls, auditing, and rotation support than a manually maintained file.

Only the component that actually needs a credential should receive it. Avoid copying secrets into build logs, client-side bundles, error messages, or unrelated services.

## 8. A Critical Warning About Frontend Applications

**Environment variables do not automatically make a secret safe in frontend code.**

In a browser-based application, values embedded into JavaScript or delivered to the browser can usually be inspected by users. Some frontend build tools intentionally replace environment-variable references during the build, placing the values into the public bundle.

For example, do not place a private AI provider key in code that runs in the browser.

A safer architecture is:

```text
Browser frontend
       |
       | Request to your application
       v
Your backend
       |
       | Uses private API key stored server-side
       v
External API provider
       |
       v
Your backend returns the allowed result
       |
       v
Browser frontend
```

The backend keeps the private credential on the server and calls the provider. The frontend should receive only the information it needs, not the secret key.

Some services provide intentionally public keys for use in a browser. Use those only as documented, with the applicable domain restrictions and permissions; do not expose a private secret key just because a framework supports environment variables.

## 9. What If You Accidentally Push an API Key?

Treat an exposed, usable secret as compromised. Take these steps promptly.

1. **Revoke or rotate the key.** Use the provider's dashboard or credential-management process. Do not wait to see whether someone has used it.
2. **Review usage and billing.** Look for requests or activity you do not recognize and follow the provider's incident guidance.
3. **Remove the secret from the current code.** Replace it with an environment variable or a suitable secret-management method.
4. **Check Git history and copies.** The secret may remain in older commits, branches, tags, releases, logs, or other copies. Clean history where needed, using a careful repository-specific process.
5. **Check for reuse.** If the same credential was used anywhere else, rotate it there too.
6. **Add preventive controls.** Review `.gitignore`, consider secret scanning and push protection, and check staged changes before future commits.

Changing Git history does not revoke a credential that someone has already copied. **Rotation or revocation is the essential first step.**

## 10. Useful Git Habits

Before committing a project, check what Git is about to include:

```bash
git status
git diff --cached
```

These commands help you review the repository state and the staged changes. They are useful checks, but they are not a complete secret scanner.

Also:
- Keep private configuration out of tracked files.
- Do not paste credentials into public issues, pull requests, screenshots, or logs.
- Use a secret scanner where appropriate.
- Restrict API keys by scope, project, origin, or IP address where the provider supports such restrictions.
- Rotate credentials when people, systems, or environments no longer need them.

## 11. Common Misconceptions

### "Deleting the key from the latest version fixes the leak."

No. The credential may still exist in Git history or in copies made by others. Revoke or rotate it.

### "A private repository is a safe place for secrets."

No. Private repositories restrict access but are not dedicated secret stores.

### "Putting a key in an environment variable always makes it secret."

No. Environment variables help separate configuration from source code, but a value can still leak if it is embedded into a frontend bundle, printed in logs, exposed to an untrusted process, or configured insecurely.

### "Every API key is equally powerful."

No. Permissions and capabilities vary. Limit a key to the minimum required access, and understand what its provider allows it to do.

### "A key that looks random is safe to publish."

No. A secret remains sensitive regardless of whether it is easy to guess. The risk is that someone can copy and use it.

### "GitHub will always catch leaked keys."

No. Detection and prevention depend on the secret type, repository settings, and available features. Do not rely on automated scanning as the only protection.

## 12. Questions for Revision

Try answering these without looking at the answer key.

1. What is an API key?
2. Why can exposing a secret API key cause unexpected charges?
3. Can someone misuse a key even if the project code is harmless?
4. Why is a private GitHub repository not a secret manager?
5. What is an environment variable?
6. What is the purpose of a local `.env` file?
7. Why should `.env` be listed in `.gitignore`?
8. What is `.env.example` used for?
9. Why does deleting a key from the latest commit not guarantee safety?
10. What should you do first after exposing a real secret key?
11. Why are frontend environment variables not automatically secret?
12. What is the principle of least privilege?
13. Where should production API credentials be configured?
14. What can GitHub secret scanning and push protection do, and why should you not rely on them exclusively?
15. Why should you review staged changes before committing?

### Answer Key

1. An API key is a credential that a service uses to identify a caller or control access, usage, or billing, depending on the service.
2. Someone may use the key to generate API requests that consume quotas or create charges associated with the account.
3. Yes. The key may permit requests or operations that consume resources or access protected services.
4. A private repository still allows access by authorized collaborators and can be exposed through other incidents. It is not designed for secret storage.
5. An environment variable is a named value made available to a running process through its environment.
6. It holds local development configuration such as API keys and is normally kept out of version control.
7. It helps prevent the local secret-containing file from being committed.
8. It documents the required variable names and safe placeholders for other developers without including real credentials.
9. The secret may remain in prior commits or copies that other people already made.
10. Revoke or rotate the exposed credential promptly.
11. Frontend build processes can embed values into browser-visible code, which users can inspect.
12. Give each user, application, or service only the permissions needed for its task.
13. In a secure deployment environment, such as a hosting provider's secret settings or a managed secrets service.
14. They can detect or block some credential leaks, but coverage depends on the secret type and configuration. They are an additional defense, not a replacement for safe practices.
15. It helps catch accidental inclusion of secrets or other unintended files before they enter the repository.

## 13. Key Takeaway

> **Keep project code in GitHub, but keep secret API keys outside your committed code. Supply credentials securely at runtime, restrict their permissions, and revoke any secret that has been exposed.**

A practical pattern to remember is:

**Code in GitHub → Secret configured securely → Backend reads it at runtime → Backend calls the API**

This practice is important for personal projects, team repositories, AI applications, and production systems alike.
