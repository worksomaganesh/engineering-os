# API: Application Programming Interface

## 1. What Is an API?

**API stands for Application Programming Interface.**

An API is a defined interface that lets one piece of software request data or functionality from another piece of software according to agreed rules. For example, a weather application may use a weather service's API to request the current conditions for a city. The service returns data, and the application displays it to the user.

An API describes how software can interact. It does not necessarily describe the internal implementation of the software being accessed.

## 2. A Real-World Analogy: Ordering at a Restaurant

Imagine ordering a meal at a restaurant:

1. You tell the waiter what you want.
2. The waiter communicates the order to the kitchen.
3. The kitchen prepares the meal.
4. The waiter brings the meal to you.

This is a useful analogy for a common client-server API interaction:

| Restaurant analogy | Software example |
|---|---|
| Customer | Client application |
| Menu and ordering rules | API's available operations and rules |
| Order | Request |
| Kitchen | Server-side application or service |
| Meal delivered | Response |

The analogy is not exact: an API is not always a separate program or a person-like intermediary. It is the defined interface and rules through which software interacts.

## 3. A Practical Example: A Weather App

Suppose a weather app needs the current weather in Hyderabad.

1. The app sends a request to a weather service.
2. The service processes the request and obtains the relevant weather data.
3. The service sends a response.
4. The app reads the response and displays the result.

A simplified response might look like this:

```json
{
  "city": "Hyderabad",
  "temperature": 29,
  "condition": "Cloudy"
}
```

The app could display: **Hyderabad — 29°C, Cloudy**. This JSON is illustrative data, not a live weather report. JSON is a common format for representing data, but APIs can use other formats too.

## 4. Request and Response

In a typical web API interaction:

- **Request:** The message asking the service to perform an operation or provide information.
- **Response:** The message returned by the service.
- **Endpoint:** A particular address at which an API operation can be accessed, commonly a URL for a web API.
- **HTTP method:** Indicates the kind of operation being requested.
- **Parameters:** Values that help specify the request, such as a city name or an item ID.
- **Headers:** Additional request or response information, such as the content type or authentication details.
- **Request body:** Data sent with a request, commonly with methods such as POST, PUT, or PATCH.
- **Status code:** An HTTP code indicating the result of the request.

Example request:

```http
GET https://api.example.com/weather?city=Hyderabad
```

This is an illustrative URL, not a real weather API endpoint. `GET` generally requests data. The part after `?` is a query parameter specifying the city.

## 5. Common HTTP Methods

| Method | Typical purpose |
|---|---|
| `GET` | Retrieve a resource or data |
| `POST` | Submit data or ask the server to process an operation; often used to create a resource |
| `PUT` | Create or replace a resource at a specified address, depending on the API's rules |
| `PATCH` | Partially update a resource |
| `DELETE` | Delete a resource |

These are common conventions. The exact behavior also depends on the API's documentation and implementation.

## 6. What Happens Behind the Scenes?

```text
User clicks "Show My Profile"
            |
            v
Frontend sends an API request
            |
            v
Backend receives and validates the request
            |
            v
Backend may read data from a database
            |
            v
Backend sends an API response
            |
            v
Frontend displays the profile
```

Not every API request needs a database. A service might calculate a result, call another service, return cached information, or perform another operation.

## 7. API vs. Frontend vs. Backend vs. Database

- **Frontend:** The part of an application that users interact with, such as a website's screens.
- **API:** The defined interface and rules through which software components communicate.
- **Backend:** The server-side application logic that processes requests and coordinates work.
- **Server:** The computer or runtime environment that runs a service and handles requests.
- **Database:** A system used to store and retrieve data.

An API is not the same thing as a server or database. An API may provide a way to access functionality implemented by a backend, which may use a database.

## 8. Where Are APIs Used?

- **AI applications:** An application can send a prompt to an AI provider's API and receive a model response.
- **Payments:** A store may use a payment provider's API to initiate and check payments.
- **Maps:** An application can request map tiles, routes, or place information from a maps service.
- **E-commerce:** A frontend can request product details, submit orders, and check delivery status through backend APIs.
- **Developer tools:** Programs can use APIs to create issues, retrieve repository information, or automate workflows on supported platforms.

An API does not automatically grant unrestricted access. The provider may require authentication, authorization, rate limits, or payment.

## 9. Does Every API Use the Internet?

No. A web API is accessed over a network, often using HTTP or HTTPS, but APIs also exist within a single program or on a local computer. A programming language's standard library exposes functions that other code can call. Those functions form part of a programming API even when no internet connection is involved.

## 10. API Keys and Security

Some services require an API key or another authentication method to identify a caller or control access.

- Treat secret API keys like passwords.
- Do not commit private keys or tokens to a public GitHub repository.
- Use environment variables or an appropriate secrets manager for server-side secrets.
- Do not assume an API key alone proves that a user is authorized to access every resource.
- Follow the service's documentation, permissions, and usage limits.

A public API is not necessarily an API that can be used without authentication.

## 11. Common Misconceptions

- **An API is a database.** No. An API is an interface; it may provide access to data stored in a database.
- **An API is always a website.** No. A web API may use URLs, but APIs also exist inside programs and libraries.
- **An API always returns JSON.** No. JSON is common, but other formats are possible.
- **An API does all the backend work.** Not necessarily. It defines how functionality is accessed; the implementation performs the work.
- **Every API is public and free.** No. Access may be private, restricted, paid, or rate-limited.

## 12. Key Takeaway

> An API is a defined interface that allows software components to communicate and request data or functionality from one another.

For web APIs, a useful starting mental model is:

**Client → Request → API endpoint → Server-side processing → Response → Client**

## 13. Questions for Revision

Try answering these without looking at the document:

1. What does API stand for?
2. What problem does an API solve?
3. In the restaurant analogy, what do the request and response represent?
4. What is the difference between an API and a backend?
5. What are an endpoint, an HTTP method, and a status code?
6. What is JSON, and why might an API return it?
7. Does every API need the internet or a database?
8. Why should secret API keys never be committed to a public repository?

## 14. What to Learn Next

A useful learning order is:

1. HTTP and HTTPS
2. URLs, endpoints, headers, and query parameters
3. JSON
4. HTTP status codes
5. REST APIs and CRUD operations
6. Authentication, authorization, and API keys
7. Calling an API from a small program
8. Building a simple API and testing it

As you explore these topics, add short study-session summaries to `notes/`, runnable experiments to `builds/`, quick references to `cheat-sheets/`, and follow-up questions to `questions/`.
