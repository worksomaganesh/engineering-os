# Authentication and Authorization

Authentication and authorization are two essential security concepts in websites, REST APIs, mobile applications, databases, cloud services, and AI applications.

They are related, but they solve different problems:

- **Authentication asks: "Who are you?"**
- **Authorization asks: "What are you allowed to do?"**

Authentication verifies an identity or credential. Authorization determines which resources and actions that identity is permitted to access.

## 1. A Real-World Analogy: Entering a College Campus

Imagine entering a college campus.

At the entrance, a security guard checks your student ID. The guard verifies that the ID is valid and belongs to you.

This is an example of **authentication**: verifying identity.

Now imagine that you want to enter a restricted examination office. Even though the guard has confirmed that you are a student, you may not have permission to enter that office.

This is an example of **authorization**: checking what you are permitted to access.

The key lesson is:

> You can be successfully authenticated but still not be authorized to perform a particular action.

Software systems apply the same idea. Knowing who a user is does not automatically mean that the user should have unrestricted access to every resource.

## 2. What Is Authentication?

**Authentication is the process of verifying the identity of a user, application, device, or other entity.**

A person or system presents some form of evidence, and the receiving system checks that evidence according to its authentication rules.

Common authentication methods include:

### Passwords

The user supplies a password associated with an account. A properly designed service verifies it against a securely stored password hash rather than storing the password as plain text.

### One-time codes

The user enters a temporary code, for example from an authenticator app or another supported channel. The actual security depends on how the code is generated, delivered, and verified.

### Multi-factor authentication (MFA)

MFA asks the user to prove identity using two or more different factor types, such as something they know, something they possess, or something they are.

Using two passwords is not the same as using two different factor types.

### Passkeys

Passkeys use public-key cryptography. The user typically approves authentication on a device using a screen lock, PIN, or biometric gesture. The biometric data generally remains on the device rather than being sent to the website as the password.

### API credentials and tokens

Applications may present credentials or tokens that a service validates. The exact mechanism may be an API key, a bearer access token, a signed token, a client certificate, or another supported credential.

A token is not automatically safe or sufficient for every operation. The service must validate it correctly and apply the appropriate access checks.

## 3. Example: Logging In to GitHub

Imagine you open GitHub and authenticate using a supported method, such as a passkey or password plus any required verification.

A simplified flow is:

```text
You provide authentication evidence
              |
              v
The service validates the evidence
              |
              v
Identity or account session is established
              |
              v
You are authenticated
```

The exact process depends on the authentication method and service.

Authentication establishes or verifies an identity. It does **not** automatically grant permission to every repository, organization, setting, or action.

## 4. What Is Authorization?

**Authorization is the process of deciding what an authenticated identity is allowed to access or do.**

An application can use authorization rules to decide whether a user may:

- View a particular file.
- Read or modify a GitHub repository.
- Delete a database record.
- Access another user's account information.
- Create, update, or delete resources through an API.
- Perform administrative operations.
- Use a particular feature or service.

Authorization decisions may depend on the user's role, assigned permissions, resource ownership, the requested action, the resource's attributes, or the context of the request.

## 5. Example: Different GitHub Repository Permissions

Imagine three people have successfully authenticated on GitHub.

| Person | Example access level | Typical capabilities |
|---|---|---|
| Person A | Read | View repository content and history |
| Person B | Write | View content and make permitted changes |
| Person C | Admin | Manage additional repository settings and administrative capabilities |

All three people may be authenticated, but their authorization differs.

The precise permissions depend on the repository, organization policy, role, branch rules, and the action being attempted. A role name alone does not guarantee that every operation is allowed.

## 6. Authentication vs. Authorization

| Feature | Authentication | Authorization |
|---|---|---|
| Main question | Who are you? | What are you allowed to do? |
| Purpose | Verify identity or credentials | Determine permitted access and actions |
| Common example | Checking a passkey or password | Checking whether a user may edit a repository |
| Common mechanisms | Passwords, passkeys, MFA, validated credentials | Roles, permissions, policies, resource ownership |
| Typical outcome | Identity verified or authentication rejected | Action allowed or denied |
| Relationship | Often happens before a protected operation is authorized | Uses an identity or other trusted context to make an access decision |

### A memory trick

- **Authentication = Identity**
- **Authorization = Permissions**

Do not confuse these two processes. A successful login does not mean that the user has access to every resource.

## 7. How Do Authentication and Authorization Work Together?

Imagine you use an online shopping application and request an order.

You send a request such as "Show me order 105." The application needs to establish who is making the request and whether that identity can view that particular order.

A typical process is:

1. **The client makes a request.** It asks to access a protected resource.
2. **Authentication is checked.** The service validates the supplied credential, token, or session.
3. **The identity is associated with the request.** The service determines which user or application is making the request.
4. **Authorization is checked.** The service determines whether the identity is allowed to access the requested order.
5. **The operation is allowed or denied.** If permitted, the server returns the allowed data. Otherwise, it rejects the request.

The exact architecture can vary. For example, some authentication checks happen at an API gateway while resource-specific authorization happens in the backend service.

**Important:** The server must not assume that being logged in is enough to view any order. It needs to check access to the particular resource, such as whether the order belongs to the user or has otherwise been shared with them.

## 8. How Does This Apply to REST APIs?

Consider a web API endpoint:

```http
GET /orders/105
```

A client wants to retrieve order `105`. A protected endpoint may require a token in the HTTP Authorization header.

Example request:

```http
GET /orders/105 HTTP/1.1
Host: api.example.com
Authorization: Bearer YOUR_ACCESS_TOKEN
```

This is an illustrative request. The hostname and token are placeholders, not a real endpoint or credential.

Here is what the header means:

- `Authorization` is the HTTP header used to carry credentials for the request.
- `Bearer` indicates a bearer-token authentication scheme.
- `YOUR_ACCESS_TOKEN` is a placeholder for a real access token. Never publish a real token in a learning document or public repository.

### Authentication check

The service validates the token according to its design. It may check whether the token is valid, unexpired, intended for this service, and associated with an identity or permitted client.

If authentication fails, a server commonly returns an HTTP status such as:

```http
HTTP/1.1 401 Unauthorized
```

### Authorization check

If authentication succeeds, the server checks whether the identified user is allowed to view order `105`.

If the user is authenticated but is not allowed to access that order, a common response is:

```http
HTTP/1.1 403 Forbidden
```

These are common HTTP conventions, not an absolute description of every API. Some systems intentionally use a `404 Not Found` response when revealing the existence of a protected resource would expose sensitive information.

A valid token is not necessarily sufficient for every operation. The backend may also need to check the token's scopes, role, resource ownership, and other permission rules.

## 9. Authentication Tokens, Sessions, and Permissions

These terms are related, but they have different purposes.

### Session

A session is a way for a service to maintain or recognize an authenticated interaction across requests. For example, a server may issue a session identifier in a cookie after login and use it to look up session state.

### Access token

An access token is a credential presented to a service to access protected functionality or data. Tokens may be opaque or have a structured, signed format. Their meaning, lifetime, intended audience, and permissions depend on the system.

### API key

An API key commonly identifies an application or caller and may be used to control access, quotas, or billing. It should not automatically be treated as proof of a human user's identity or as permission to access every resource.

### Role and permission

A **role** groups a set of capabilities, while a **permission** represents an allowed action or access right. Authorization logic uses these and other relevant facts to decide whether an operation is allowed.

### How they fit together

A token or session can help authenticate a request. The service still needs to make an authorization decision for the requested operation.

For instance, a token may identify a user but not grant access to another customer's private order.

## 10. How Do Developers Implement Authorization?

Authorization can use several approaches. Systems often combine more than one.

### 10.1 Role-Based Access Control (RBAC)

Role-Based Access Control assigns permissions to roles such as `admin`, `editor`, and `viewer`. Users receive capabilities through their roles.

Example:

| Role | Example permission |
|---|---|
| Viewer | Read permitted records |
| Editor | Read and update permitted records |
| Admin | Manage additional settings and access, subject to policy |

RBAC works well when access can be described through stable roles, but applications still need to check which resources each role can access.

### 10.2 Attribute-Based Access Control (ABAC)

Attribute-Based Access Control evaluates attributes of the user, resource, action, and sometimes the surrounding context.

For example, a policy might allow an employee to view a document only if the employee belongs to the required department and the document is classified for that department.

This approach can express more detailed conditions than a simple role check.

### 10.3 Resource Ownership Checks

An application can check whether the authenticated user owns or has been granted access to a specific resource.

For example, a customer may be allowed to view orders associated with their account, but not orders belonging to other customers.

Ownership checks are important because permission to use an endpoint does not automatically imply permission to access every record that endpoint can identify.

### Never rely only on the frontend

Hiding a button in a website is not sufficient authorization. A user could still attempt to send the corresponding API request directly.

Protected operations must be checked by a trusted server-side component or another enforcement point that cannot be bypassed by modifying the client.

## 11. Authentication and Authorization: Common Scenarios

| Scenario | Authentication | Authorization |
|---|---|---|
| Valid login, but no access to an admin page | Succeeds | Denies access |
| Invalid or expired credential | Fails | The protected action should not proceed |
| User can read a file but cannot edit it | Succeeds | Allows reading, denies editing |
| Application token is valid but lacks a required scope | May succeed | Denies the operation due to insufficient permission |
| User tries to read another customer's order | Succeeds | Denies access unless the user has permission |

These examples show why applications must check identity and access separately.

## 12. Security Best Practices

### For authentication

- Use established authentication protocols and well-maintained libraries instead of designing your own cryptographic scheme.
- Store passwords using a suitable password-hashing algorithm with appropriate parameters; never store plain-text passwords.
- Encourage phishing-resistant authentication methods where feasible.
- Apply multi-factor authentication to sensitive accounts and administrative access.
- Protect session identifiers and access tokens as credentials.
- Expire, revoke, and rotate credentials according to the system's security requirements.

### For authorization

- Apply the **principle of least privilege**: give each user or service only the access it needs.
- Check permissions on the server for every protected operation.
- Check access to individual resources, not just the endpoint.
- Deny access by default when a clear permission decision cannot be made.
- Review administrative privileges and service-account permissions regularly.
- Log important security decisions without recording passwords, tokens, or other secrets.

### For APIs

- Use HTTPS to protect credentials and data in transit.
- Validate inputs and enforce authentication and authorization checks on the server.
- Do not place access tokens or passwords in public URLs.
- Return appropriate errors without revealing sensitive information.
- Keep secrets out of source control, public repositories, and logs.

No single security mechanism makes an application secure by itself. Authentication, authorization, secure credential handling, input validation, and careful system design work together.

## 13. Common Misconceptions

### "Authentication and authorization mean the same thing."

No. Authentication verifies identity; authorization determines what that identity may access or do.

### "If a user has logged in, they can access everything."

No. Authenticated users still need permission for protected resources and operations.

### "An API key always identifies a specific human user."

No. API keys commonly identify an application or caller. Their identity and authorization meaning depends on how the service defines and validates them.

### "The frontend can enforce all permissions."

No. Client-side checks can improve the user experience, but a user may bypass them. Sensitive access decisions need trusted enforcement on the server or another protected layer.

### "A valid token means every request is authorized."

No. The token may be expired, intended for another service, missing a required scope, or associated with an identity that cannot access the requested resource. The service must perform the appropriate checks.

### "A 401 and a 403 always mean exactly the same thing."

No. Commonly, `401 Unauthorized` indicates that valid authentication credentials are missing or unacceptable, while `403 Forbidden` indicates that the server refuses the operation. Implementations may vary and may conceal the existence of protected resources.

## 14. Questions for Revision

Try answering the following questions without looking at the answer key.

1. What is authentication?
2. What is authorization?
3. What is the simplest way to remember the difference?
4. Can a user be authenticated but not authorized to access a resource?
5. What are three examples of authentication methods?
6. What is multi-factor authentication?
7. What is the difference between a session, an access token, and an API key?
8. What does a REST API's Authorization header commonly carry?
9. What does HTTP status code 401 commonly indicate?
10. What does HTTP status code 403 commonly indicate?
11. Why does a valid token not automatically permit every operation?
12. What is Role-Based Access Control (RBAC)?
13. What is Attribute-Based Access Control (ABAC)?
14. Why are resource ownership checks important?
15. Why is hiding a button in the frontend not sufficient authorization?
16. What does the principle of least privilege mean?
17. How are authentication and authorization related to API security?

### Answer Key

1. Authentication is the process of verifying an identity or credential.
2. Authorization is the process of determining which actions or resources an identity is permitted to access.
3. Authentication asks, "Who are you?" Authorization asks, "What are you allowed to do?"
4. Yes. Identity may be verified while permission for a particular operation is denied.
5. Examples include passwords, passkeys, and multi-factor authentication. Services can also validate tokens, certificates, or other credentials.
6. MFA requires evidence from at least two different authentication factor types.
7. A session maintains or recognizes an authenticated interaction; an access token is a credential presented to access protected functionality; an API key commonly identifies a caller or application and may control access or quotas.
8. It commonly carries credentials, such as a bearer access token, that the server validates.
9. A 401 response commonly indicates that valid authentication credentials are missing or unacceptable.
10. A 403 response commonly indicates that the server refuses to allow the operation.
11. The token may not grant the required scope or permission, or the identity may lack access to that resource.
12. RBAC assigns permissions to roles and grants capabilities through those roles.
13. ABAC makes access decisions using attributes of the user, resource, action, and possibly context.
14. An endpoint may identify many records, but the user should only access the records they are permitted to view or change.
15. A user can bypass client-side interface restrictions and send requests directly. The server must enforce permissions.
16. Give a user or service only the permissions necessary for its task.
17. Authentication establishes or verifies who is making a request, while authorization checks whether that identity can perform the requested action.

## 15. What to Learn Next

A useful learning sequence after authentication and authorization is:

1. **Sessions and cookies** — learn how websites recognize users across requests.
2. **Access tokens and OAuth 2.0** — understand how applications obtain and use delegated access.
3. **JWT (JSON Web Token)** — learn one common token format and its validation requirements.
4. **RBAC and ABAC** — explore permission models.
5. **API security** — study resource-level authorization, rate limiting, input validation, and safe error handling.
6. **Practical implementation** — build a small API with login, protected endpoints, and resource ownership checks.

## Key Takeaway

> **Authentication verifies identity. Authorization decides what that identity is permitted to access or do.**

For a protected API, remember this flow:

**Request → Validate credentials → Establish identity → Check permissions → Allow or deny the operation**

These checks are separate but complementary. Correct authentication without correct authorization can still expose private data or allow actions that a user should not be able to perform.
