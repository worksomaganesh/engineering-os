# Firebase: A Beginner-Friendly Guide with Examples

Firebase is Google's app-development platform. It provides ready-made services that help you build web and mobile apps without having to create every backend feature from scratch.

For example, a notes app may need user sign-in, a database to save notes, file storage for attachments, and hosting for its website. Firebase offers services for many of these needs, so you can focus more on the application itself.

Firebase is closely integrated with Google Cloud. A Firebase project is backed by a Google Cloud project, and some Firebase products use Google Cloud infrastructure or billing. Firebase is not a replacement for every backend: you can combine it with your own API or other cloud services when your application needs them.

Official entry point: [Firebase documentation](https://firebase.google.com/docs).

## 1. What Can Firebase Do?

Think of building a small app without a backend platform. You might need to write:
- A sign-up and sign-in system.
- A database API to save and retrieve information.
- An upload service for images and documents.
- A hosting and deployment setup.
- Notifications and crash reporting.
- Server-side code for trusted operations.

Firebase offers managed products for several of these jobs. You choose only the ones your app needs.

## 2. The Main Firebase Services

| Service | What it does | Beginner example |
|---|---|---|
| [Firebase Authentication](https://firebase.google.com/docs/auth) | Helps users sign in using supported methods | A student signs into a study app with email/password or Google |
| [Cloud Firestore](https://firebase.google.com/docs/firestore) | A cloud NoSQL document database | Save a user's notes, tasks, or app preferences |
| [Realtime Database](https://firebase.google.com/docs/database) | A cloud-hosted JSON database with realtime synchronization | Show a live status that updates immediately |
| [Cloud Storage for Firebase](https://firebase.google.com/docs/storage) | Stores user-uploaded files | Store profile pictures, photos, or documents |
| [Firebase Hosting](https://firebase.google.com/docs/hosting) | Hosts web content | Publish a static website or frontend |
| [Firebase App Hosting](https://firebase.google.com/docs/app-hosting) | Builds and deploys supported full-stack web apps | Deploy a supported modern web application |
| [Cloud Functions for Firebase](https://firebase.google.com/docs/functions) | Runs backend code in response to events or requests | Send a notification after an order is created |
| [Firebase Cloud Messaging (FCM)](https://firebase.google.com/docs/cloud-messaging) | Sends push notifications | Notify a user when a new message arrives |
| [Firebase Analytics](https://firebase.google.com/docs/analytics) | Measures app usage and events | Understand which features people use |
| [Crashlytics](https://firebase.google.com/docs/crashlytics) | Reports app crashes and errors | Investigate why an Android or iOS app crashed |
| [Remote Config](https://firebase.google.com/docs/remote-config) | Changes selected app behavior without a normal app release | Enable a feature for a test group |
| [App Check](https://firebase.google.com/docs/app-check) | Helps protect backend resources from unauthorized clients | Reduce abuse of supported Firebase services |
| [Local Emulator Suite](https://firebase.google.com/docs/emulator-suite) | Runs supported Firebase services locally for development and testing | Test authentication and Firestore without writing test data to production |

You do not need all these products for every project. Start with one or two, understand them, and add others when they solve a real problem.

## 3. Example: A Student To-Do App

Imagine a to-do application where each student signs in and saves their own tasks.

A simple design is:
- **Frontend:** the web page or mobile app the student interacts with.
- **Firebase Authentication:** identifies the signed-in student.
- **Cloud Firestore:** saves task documents.
- **Firestore Security Rules:** control which tasks the student may read or change.
- **Firebase Hosting:** can host a web frontend.
- **Cloud Functions:** can be added later for trusted backend operations.

Example flow:
1. The student signs in.
2. The app identifies the signed-in user.
3. The app saves a task to the database.
4. Security Rules check whether the user is allowed to perform the operation.
5. The UI can retrieve updated data or listen for realtime updates.

Firebase can handle much of the underlying infrastructure, but **you are still responsible for data modeling, access rules, application logic, and cost awareness**.

## 4. Get Started with Firebase

The exact setup steps depend on whether you build for the web, Android, iOS, Flutter, or Unity. This example uses a web app with modern JavaScript.

1. Open the [Firebase Console](https://console.firebase.google.com/).
2. Create a Firebase project.
3. Register a web app inside that project.
4. Follow the console's setup instructions to get its Firebase configuration.
5. Enable the products you need, such as Authentication and Cloud Firestore.
6. Read the relevant pricing and security instructions before using real user data.

The official [web setup guide](https://firebase.google.com/docs/web/setup) is the source of truth for the current installation steps.

For a JavaScript app that already uses npm, install the Firebase SDK:

```bash
npm install firebase
```

The modular JavaScript SDK lets you import the functions you need rather than importing the whole older namespaced API.

## 5. Basic Example 1 — Initialize Firebase

Create a file such as `src/firebase.js`:

```javascript
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "YOUR_FIREBASE_WEB_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  appId: "YOUR_WEB_APP_ID"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app);
```

Replace the placeholders with the configuration for your own registered web app. Copy the complete configuration from your Firebase Console rather than guessing its values.

**Security note:** the Firebase web configuration and its API key are identifiers used by the client SDK; they are not a substitute for database security. Protect client-accessible data with Authentication, Security Rules, applicable API restrictions, and App Check where supported. Never put service-account private keys, Admin SDK credentials, or other server secrets in frontend code.

This example assumes a modern JavaScript project with a build tool that supports ES module imports.

## 6. Basic Example 2 — Sign Up and Sign In

After enabling an email/password provider in Firebase Authentication, you can create a user account like this:

```javascript
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut
} from "firebase/auth";
import { auth } from "./firebase.js";

export async function signUp(email, password) {
  const result = await createUserWithEmailAndPassword(
    auth,
    email,
    password
  );

  return result.user;
}

export async function signIn(email, password) {
  const result = await signInWithEmailAndPassword(
    auth,
    email,
    password
  );

  return result.user;
}

export async function logOut() {
  await signOut(auth);
}
```

How to understand this:
- `createUserWithEmailAndPassword` creates an account and signs that user in.
- `signInWithEmailAndPassword` signs in an existing account.
- `signOut` signs out the current user.
- These calls are asynchronous, so real UI code should handle loading, validation, and errors.

This example assumes the email/password sign-in provider has been enabled in the Firebase Console. Never store plain-text passwords in your own database.

Official reference: [Firebase Authentication for web](https://firebase.google.com/docs/auth/web/start).

## 7. Basic Example 3 — Save a Task in Cloud Firestore

Firestore stores data as **documents** grouped into **collections**. A collection might be called `tasks`, while each task is a document with fields such as `title`, `done`, and `ownerId`.

Example data model:

```text
tasks (collection)
├── task_document_A
│   ├── title: "Finish assignment"
│   ├── done: false
│   └── ownerId: "user_uid_123"
└── task_document_B
    ├── title: "Revise JavaScript"
    ├── done: true
    └── ownerId: "user_uid_456"
```

To add a task from a signed-in client:

```javascript
import {
  addDoc,
  collection,
  serverTimestamp
} from "firebase/firestore";
import { auth, db } from "./firebase.js";

export async function addTask(title) {
  const user = auth.currentUser;

  if (!user) {
    throw new Error("Sign in before adding a task.");
  }

  const cleanTitle = title.trim();

  if (!cleanTitle) {
    throw new Error("Task title cannot be empty.");
  }

  const docRef = await addDoc(collection(db, "tasks"), {
    title: cleanTitle,
    done: false,
    ownerId: user.uid,
    createdAt: serverTimestamp()
  });

  return docRef.id;
}
```

What this does:
1. Checks that a user is signed in.
2. Trims and validates the task title.
3. Creates a new document in the `tasks` collection.
4. Saves the user's UID to associate the record with its owner.
5. Stores a server-generated timestamp.

This function alone does **not** make the data private. Firestore Security Rules must enforce who can read or modify each task. Client-side checks improve user experience but cannot replace authorization enforced by the database.

Official reference: [Add data to Cloud Firestore](https://firebase.google.com/docs/firestore/manage-data/add-data).

## 8. Security Rules — Keep Users' Data Separate

For a beginner prototype using the `tasks` collection from the previous example, Firestore Rules could restrict access so only the authenticated owner can read or write a task:

```text
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    match /tasks/{taskId} {
      allow read, delete:
        if request.auth != null
        && request.auth.uid == resource.data.ownerId;

      allow create:
        if request.auth != null
        && request.resource.data.ownerId == request.auth.uid
        && request.resource.data.title is string;

      allow update:
        if request.auth != null
        && request.auth.uid == resource.data.ownerId
        && request.resource.data.ownerId == resource.data.ownerId;
    }
  }
}
```

This illustrates an ownership check and basic title validation. **It is a learning starting point, not a complete production ruleset.** Production rules should validate all allowed fields and types, constrain values and updates, and be tested with the Firebase Emulator Suite. The example assumes each task has an `ownerId` field; existing or malformed documents need to be handled carefully.

Firestore evaluates client requests against Security Rules. Never use an open rule such as `allow read, write: if true;` for real user data.

Trusted server code using Firebase Admin or server libraries uses server credentials and IAM rather than relying on client Security Rules in the same way. Protect the server credentials and validate authorization in the backend.

Official references:
- [Get started with Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started)
- [Writing Security Rules conditions](https://firebase.google.com/docs/firestore/security/rules-conditions)
- [Firebase Local Emulator Suite](https://firebase.google.com/docs/emulator-suite)

## 9. Firebase Hosting — Publish a Simple Website

Firebase Hosting can publish static web assets such as HTML, CSS, JavaScript, and images.

Install the Firebase CLI and sign in:

```bash
npm install -g firebase-tools
firebase login
```

From your project's directory, initialize Hosting:

```bash
firebase init hosting
```

Follow the prompts to choose the Firebase project and specify your public/build output directory. Then build the site if your framework requires it and deploy:

```bash
firebase deploy --only hosting
```

Do not assume the public folder is always named `public`: the correct output directory depends on your app and build tool. Review the generated configuration before deploying, and check the current plan and pricing limits.

Official guide: [Firebase Hosting](https://firebase.google.com/docs/hosting).

## 10. Firebase CLI and the Local Emulator Suite

The Firebase CLI helps configure a project, run local emulators, and deploy supported resources. Useful commands include:

```bash
firebase --version
firebase login
firebase projects:list
firebase init
firebase emulators:start
firebase deploy
```

Run `firebase init` from your application's directory and select only the products you need. `firebase emulators:start` runs configured emulated services locally; it does not automatically emulate every Firebase product.

The Emulator Suite is useful for testing sign-in flows and database rules without depending on production data. Learn more in the [official documentation](https://firebase.google.com/docs/emulator-suite).

Deployment can affect live resources and may incur costs. Check what each command does and which project is selected before running it.

## 11. Spark vs Blaze — Understand the Pricing

Firebase has two commonly discussed pricing plans:

- **Spark:** the no-cost plan, with product-specific limits and restrictions. Many features can be explored without adding billing details.
- **Blaze:** the pay-as-you-go plan, which links a Cloud Billing account and charges for eligible usage beyond applicable no-cost quotas. Some capabilities require Blaze.

There is no single blanket rule that "Firebase is free." Different products have different quotas, prerequisites, and pricing. For example, the current pricing documentation states that Cloud Functions access requires the Blaze plan, and some Google Cloud integrations or features are unavailable on Spark. Storage, hosting, databases, authentication methods, and other services each have their own conditions.

Before choosing a service:
1. Check the current [Firebase pricing plans](https://firebase.google.com/docs/projects/billing/firebase-pricing-plans).
2. Read that specific product's quota and pricing page.
3. Understand whether billing is required.
4. Set up billing budgets and alerts when a billing account is linked. Alerts notify you; they do not guarantee a hard spending cap.
5. Remove unused resources and avoid deploying services you do not understand.

Pricing, quotas, eligibility, and service requirements can change. The official pricing documentation is the final authority.

## 12. Firebase vs Google Cloud vs Google AI Studio

These products overlap but solve different jobs.

| Product | Main role | Example |
|---|---|---|
| Firebase | Managed app-development services | Sign-in, app database, file uploads, web hosting, crash reports |
| Google Cloud | Broader cloud platform and infrastructure | Cloud Run backend, virtual machines, BigQuery, networking, IAM |
| Google AI Studio | Experimenting with Gemini prompts and the Gemini API | Prototype an AI assistant's system prompt and test model responses |

You can use Firebase on its own for a suitable application, connect it with other Google Cloud services, or have a Firebase-based frontend call your own backend API. If a Firebase feature needs Google Cloud billing or a Google Cloud service, check its specific setup and pricing requirements.

Related guide: [Google Cloud Platform](../google-cloud/README.md).

## 13. What Should You Build First?

A good beginner exercise is a **personal notes app**:

1. Build a basic page with a text input and a save button.
2. Set up a Firebase project and register your web app.
3. Add Firebase Authentication.
4. Use Cloud Firestore to save notes associated with the signed-in user's UID.
5. Write Security Rules so one user cannot read or edit another user's notes.
6. Use the Emulator Suite to test signed-in and signed-out behavior.
7. Deploy the frontend with Firebase Hosting if appropriate.
8. Check the plan, quotas, and pricing; clean up anything you no longer use.

Start with the smallest working version. Add file uploads, realtime listeners, notifications, or server-side functions only when you can explain why the app needs them.

## 14. Common Beginner Mistakes

- **Treating the web configuration as access control.** The config connects the SDK to a project; Security Rules and appropriate restrictions protect data.
- **Leaving database rules open.** Never use unrestricted read/write rules with real data.
- **Assuming hidden UI is security.** A button hidden in the frontend does not prevent someone from calling the backend directly.
- **Putting Admin SDK credentials in the browser.** Server credentials must remain on a trusted backend.
- **Assuming all services are free.** Check exact product limits and required billing plans.
- **Using Firestore as if it were a relational database.** Learn its collections, documents, queries, indexes, and data-modeling trade-offs.
- **Adding every Firebase service immediately.** Begin with the services that solve your current problem.
- **Skipping tests.** Test authorization and access rules, preferably with the Emulator Suite, before trusting user data.

## 15. Quick Self-Test

1. What problem does Firebase solve for app developers?
2. What is the difference between Firebase Authentication and Firestore?
3. What is the difference between a collection and a document?
4. Why is saving a user's UID not enough to secure a database?
5. What do Firestore Security Rules do?
6. Why should a service-account private key never be placed in frontend JavaScript?
7. What is Firebase Hosting useful for?
8. How does the Local Emulator Suite help during development?
9. What is the difference between Spark and Blaze?
10. How is Firebase different from Google Cloud and Google AI Studio?

### Answer key

1. It provides managed app-development services so you do not have to build every common backend capability yourself.
2. Authentication manages user identity and sign-in; Firestore stores app data in collections and documents.
3. A collection groups documents; a document stores fields and values.
4. Client code can be changed or bypassed, so Security Rules must check ownership and permissions.
5. They authorize and validate client requests to supported Firebase data services.
6. Anyone who can access frontend code could extract the private key and misuse its privileges.
7. It publishes web assets and supported web application content.
8. It lets you test supported Firebase services locally, including access-control scenarios, without relying solely on production resources.
9. Spark is the no-cost plan with product-specific limits; Blaze is pay-as-you-go and requires a linked billing account for applicable usage.
10. Firebase focuses on app-development services, Google Cloud is the broader cloud platform, and AI Studio is for Gemini prompt/model experimentation.

---

**Guiding principle:** Firebase can speed up development, but authentication, authorization, data modeling, testing, and cost control are still engineering responsibilities.
