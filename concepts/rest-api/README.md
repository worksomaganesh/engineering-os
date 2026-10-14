# REST API: A Beginner-Friendly Guide

A REST API is a common way for applications to communicate over the web using HTTP methods and a resource-oriented design.

Imagine you are building an online store. The website needs to retrieve products, create orders, update inventory, and retrieve order details. A REST API defines a consistent way for a frontend, mobile application, or another service to request those operations from the backend.

This guide builds on the concepts in [API](../api/README.md) and [HTTP and HTTPS](../http-and-https/README.md).

## 1. What Does REST API Stand For?

- **REST:** Representational State Transfer
- **API:** Application Programming Interface

REST is an architectural style: a set of constraints for designing networked software systems. A REST API is an API designed according to REST principles.

In everyday software development, people often use the term *REST API* to describe an HTTP API that organizes functionality around resources, identifies resources with URLs, and uses HTTP methods such as GET, POST, PUT, PATCH, and DELETE.

**Important:** Not every HTTP API is a REST API. Using HTTP alone does not automatically make an API RESTful.

## 2. A Real-World Example: An Online Store

Imagine opening a shopping application and wanting to view all available products.

1. You click **View Products** in the frontend.
2. The frontend sends a request to the API.
3. The backend processes the request and may retrieve product information from a database.
4. The API returns a response, often containing JSON.
5. The frontend displays the products.

A simplified flow looks like this:

```text
Frontend — Shopping App
          |
          | HTTP request
          v
REST API endpoint
          |
          v
Backend processes the request
          |
          v
Database may provide stored product data
          |
          v
HTTP response, often containing JSON
          |
          v
Frontend displays the products
```

The API defines the interface for requesting information. The backend implements the application logic, and a database may store the products.

## 3. What Makes an API a REST API?

Start with three important ideas: resources, HTTP methods, and representations.

### 3.1 Resources

A **resource** is something an application can identify and work with.

In an online store, resources may include products, customers, orders, and shopping carts.

A REST-style API commonly identifies resources using URLs called **endpoints**.

| Example endpoint | Resource |
|---|---|
| `/products` | The collection of products |
| `/products/42` | Product with ID `42` |
| `/customers/15` | Customer with ID `15` |
| `/orders/105` | Order with ID `105` |

These are illustrative paths, not real API endpoints.

Notice that the paths use nouns such as `products` and `orders` to identify resources. This is a common resource-oriented design convention.

### 3.2 HTTP Methods

The URL identifies the resource, while the HTTP method indicates the intended operation.

For example, `/products/42` identifies a particular product. A client might use GET to retrieve it, PATCH to update some of its fields, or DELETE to request its deletion—if the API supports those operations and the caller is authorized.

### 3.3 Representations

A **representation** is information that describes or expresses the state of a resource.

An API might return product `42` as JSON:

```json
{
  "id": 42,
  "name": "Wireless Headphones",
  "price": 1999,
  "inStock": true
}
```

The client can read this representation and display it in the application.

JSON is common, but REST does not require every representation to use JSON. Other formats are possible.

## 4. CRUD: Create, Read, Update, Delete

In software development, you will frequently hear the term **CRUD**. It stands for:

- **C — Create**
- **R — Read**
- **U — Update**
- **D — Delete**

These are four basic operations commonly performed on data.

A REST-style product API might support the following:

| Purpose | HTTP method | Example endpoint |
|---|---|---|
| Retrieve all products | `GET` | `/products` |
| Retrieve product 42 | `GET` | `/products/42` |
| Create a product | `POST` | `/products` |
| Replace product 42 | `PUT` | `/products/42` |
| Partially update product 42 | `PATCH` | `/products/42` |
| Delete product 42 | `DELETE` | `/products/42` |

This is a common mapping, not a guarantee. Each API's documentation specifies which endpoints and methods are supported and what permissions they require.

The important idea is that the same resource can support different operations when different HTTP methods are used.

## 5. How Does a REST API Work? A Step-by-Step Example

Suppose a shopping website needs to display product number `42`.

### Step 1: The client sends a request

The frontend sends a request to retrieve the product:

```http
GET /products/42 HTTP/1.1
Host: api.example.com
Accept: application/json
```

This is an illustrative request. `api.example.com` is not a real product service.

What the lines mean:

- **`GET`** is the HTTP method. It generally requests data.
- **`/products/42`** is the resource path.
- **`Host`** identifies the hostname in HTTP/1.1.
- **`Accept`** tells the server which response media type the client prefers. Here, the client prefers JSON.

### Step 2: The server processes the request

The backend may validate the request, check access permissions, and retrieve the product from a database or another service. Not every request needs a database; a server may calculate a result or retrieve cached data.

### Step 3: The server sends a response

A simplified response might be:

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "id": 42,
  "name": "Wireless Headphones",
  "price": 1999
}
```

Here:

- **`200 OK`** is an HTTP status code indicating success.
- **`Content-Type`** identifies the media type of the response body.
- The JSON body contains the example product information.

### Step 4: The client uses the response

The frontend reads the response and displays the product name and price.

The frontend does not need to know exactly how the backend stores its products. It only needs to understand the API's documented request and response format.

## 6. How Do You Call a REST API?

You can make requests to an API using a browser, an API testing tool, or code.

### Example A: Retrieve a product

An API might accept a request like this:

```http
GET https://api.example.com/products/42
Accept: application/json
```

A successful response could contain the product representation shown above. The example hostname is a placeholder, so this request is not guaranteed to work.

### Example B: Create a product

A client might send a POST request with a JSON body:

```http
POST /products HTTP/1.1
Host: api.example.com
Content-Type: application/json
```

```json
{
  "name": "USB-C Cable",
  "price": 299
}
```

If the server accepts the request and creates the product, it might return a `201 Created` status and information about the new product.

Creating a resource may require authentication, authorization, validation, and other checks.

### Example C: Call an API with JavaScript

This example shows a common way to retrieve product details from a web API:

```javascript
async function getProduct() {
  try {
    const response = await fetch(
      "https://api.example.com/products/42"
    );

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const product = await response.json();

    console.log(product.name);
    console.log(product.price);
  } catch (error) {
    console.error("Could not load product:", error);
  }
}

getProduct();
```

What the code does:

1. `fetch()` sends an HTTP request.
2. `response.ok` checks whether the HTTP status indicates success.
3. `response.json()` parses the response body as JSON.
4. The program reads the product's `name` and `price` fields.
5. The `catch` block handles errors.

The endpoint is a placeholder, so you must replace it with a real, accessible API URL. Also remember that `fetch()` does not automatically throw an error for every HTTP error status, which is why the example checks `response.ok`.

## 7. What Does RESTful Mean?

You may see both terms:

- **REST API**
- **RESTful API**

People often use them interchangeably. More precisely, a RESTful system follows the constraints of the REST architectural style. Those constraints go beyond simply using URLs, HTTP methods, and JSON.

REST is commonly described by the following constraints.

### 7.1 Client-Server Separation

The client handles the user interface and client-side interaction, while the server handles data and application functionality. They can evolve independently as long as their interface remains compatible.

### 7.2 Stateless Communication

Each request must contain the information needed to understand and process it. The server must not rely on stored client-session context from an earlier request to interpret the current request.

**Stateless does not mean that the server cannot store data.** The server can still store product records, user accounts, orders, and other application data. The constraint concerns the state of the client-server interaction.

### 7.3 Cacheability

Responses should indicate whether they can be cached. Appropriate caching can reduce repeated requests and improve performance.

### 7.4 Uniform Interface

Clients and servers interact through a consistent interface for identifying and manipulating resources. This is a defining REST constraint. It includes concepts such as resource identification, manipulating resources through representations, self-descriptive messages, and hypermedia as the engine of application state (HATEOAS).

Many APIs described as REST APIs use resource-oriented URLs and HTTP methods but do not implement every aspect of a uniform interface.

### 7.5 Layered System

The architecture can include intermediaries such as proxies, gateways, and load balancers. A client does not necessarily need to know which internal layers handle its request.

### 7.6 Code on Demand (Optional)

A server may optionally extend a client's functionality by transferring executable code. This constraint is optional in REST.

These are architectural constraints, not a checklist that can be reduced to “use JSON with HTTP methods.” For the original description of REST, see [Roy Fielding's dissertation on the REST architectural style](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm).

## 8. Why Do Developers Use REST APIs?

REST-style APIs are popular because they provide familiar ways to organize communication between applications.

- **Separation:** Frontend and backend teams can work independently.
- **Reusability:** A website and a mobile application can use the same API when they need the same functionality.
- **Consistency:** Resource-oriented URLs and common HTTP methods provide predictable conventions.
- **Scalability:** Stateless interactions, caching, and layered architecture can help systems scale when designed appropriately.
- **Interoperability:** Different programming languages and platforms can communicate when they support the API's protocol, format, and authentication requirements.

REST does not automatically make an application fast, scalable, or secure. Those properties depend on the overall design, infrastructure, and implementation.

## 9. Where Are REST APIs Used?

REST-style APIs are used in many kinds of web applications, mobile applications, cloud services, and integrations.

| Area | Example use |
|---|---|
| E-commerce | Retrieve products, create orders, update inventory |
| Social applications | Retrieve posts, create comments, manage profiles |
| AI applications | Send requests to an AI service and receive results |
| Banking and payments | Retrieve permitted account information or initiate payment operations |
| Developer platforms | Retrieve repository information or manage issues |
| Travel applications | Retrieve available flights, hotels, or reservation details |

These are common use cases; not every service uses REST.

## 10. REST API vs. API vs. HTTP vs. HTTPS vs. MCP

Because these concepts are connected, it is important to keep their roles separate.

| Term | What it means |
|---|---|
| **API** | An interface through which software functionality or data can be accessed |
| **HTTP** | A protocol for exchanging web requests and responses |
| **REST** | An architectural style for designing networked systems |
| **REST API** | An API designed around REST principles, commonly using HTTP |
| **HTTPS** | HTTP communication protected by TLS |
| **MCP** | A protocol that standardizes how compatible AI applications communicate with MCP servers and use the capabilities those servers expose |

A REST API commonly uses HTTP or HTTPS. An MCP server may call a REST API to retrieve data or perform an operation.

For example, an AI assistant might communicate with a GitHub MCP server using MCP, while that server communicates with GitHub's API over HTTPS.

## 11. Security and Common Mistakes

REST does not automatically provide authentication or authorization.

When developing or using an API:

- **Use HTTPS in production** to protect data in transit.
- **Authenticate callers where required** to establish who is making a request.
- **Authorize each operation** to check whether the caller can access the requested resource or perform the action.
- **Validate input** before processing it.
- **Protect secrets** and never commit private API keys or tokens to public repositories.
- **Handle error responses** instead of assuming every request succeeds.
- **Avoid putting confidential information in URLs**, where it may appear in logs, browser history, or monitoring systems.
- **Apply rate limits and other controls** where appropriate to reduce abuse.

A well-designed API needs both a consistent interface and appropriate security controls.

## 12. Questions for Revision

Try answering these questions without looking at the answer key.

1. What does REST stand for?
2. What is the difference between an API and a REST API?
3. What is a resource, and how might it be identified?
4. What is an endpoint?
5. What does CRUD stand for?
6. What is the typical difference between GET, POST, PUT, PATCH, and DELETE?
7. Why might `GET /products/42` and `PATCH /products/42` have different results?
8. What is a representation, and why might an API return JSON?
9. What is the difference between a REST API and an API that merely uses HTTP?
10. What does stateless communication mean in REST?
11. Does statelessness prevent a server from storing data in a database?
12. What is cacheability, and why can it be useful?
13. What does the uniform interface constraint mean?
14. Does REST guarantee that an API is fast or secure?
15. How can a frontend and a backend use the same API?
16. What is the relationship between REST APIs and MCP?
17. Why should production APIs use HTTPS?
18. Why must API input be validated?

### Answer Key

1. **Representational State Transfer.**
2. An API is a general interface for accessing functionality or data. A REST API is designed around REST's architectural principles.
3. A resource is something identifiable, such as a product, customer, or order. It is commonly identified by a URL.
4. An endpoint is an address at which an API exposes a resource or operation.
5. **Create, Read, Update, Delete.**
6. GET retrieves; POST submits data or asks the server to process an operation; PUT creates or replaces a resource at a specified address according to the API's rules; PATCH partially updates; DELETE requests deletion.
7. The URL identifies the same resource, but the HTTP method expresses a different intended operation.
8. A representation is information describing a resource. JSON is a common structured format that clients can parse.
9. REST includes architectural constraints beyond the use of HTTP. An HTTP API is not automatically fully RESTful.
10. Each request contains the information needed to understand and process it without depending on stored client-session context from earlier requests.
11. No. A server can store application data such as products and orders.
12. Cacheability indicates whether a response can be reused for a period or under certain conditions, potentially reducing repeated work and improving performance.
13. It means clients and servers use a consistent interface for identifying resources and interacting with their representations; in REST it includes additional requirements such as self-descriptive messages and hypermedia.
14. No. Performance and security depend on the implementation and overall system design.
15. Both can send requests to the API and process its responses, provided they follow the API's contract and have the necessary permissions.
16. An MCP server can use a REST API behind the scenes and expose selected operations through MCP to a compatible AI application.
17. HTTPS helps protect data in transit and helps the client verify the server's identity.
18. Validation helps reject malformed or unsafe input before it causes errors, invalid data, or security problems.

## 13. What to Learn Next

A useful learning order is:

1. **JSON** — understand structured data returned by APIs.
2. **HTTP headers and request bodies** — learn what accompanies requests and responses.
3. **HTTP status codes** — understand success, redirects, and errors.
4. **Authentication and authorization** — learn how services verify users and permissions.
5. **API testing** — use an API client to make requests and inspect responses.
6. **Call a real public API** — write a small program that handles responses and errors.
7. **Build a small REST API** — implement endpoints, validate input, and return suitable status codes.
8. **Deployment and security** — expose an API safely in a production environment.

For further reading:

- [Roy Fielding's dissertation on REST](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
- [MDN: HTTP request methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)

## Key Takeaway

> **A REST API is an interface that exposes resources through a consistent set of conventions, commonly using URLs, HTTP methods, and representations such as JSON, while following REST's architectural constraints.**

Remember this mental model:

**Resource + URL + HTTP method → Request → Backend processing → Response**

For your Engineering OS learning journey, the next useful step is to practice JSON and HTTP status codes, then consume a real public API. After that, build a small REST API of your own so these concepts become practical skills rather than just definitions.
