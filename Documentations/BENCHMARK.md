# Benchmark
 *We evaluated the most popular technologies for frontend, backend, and mobile development. Our criteria included, but weren’t limited to, learning curve, ecosystem size, performance, team familiarity, and suitability for our project features.*

---

# Frontend

## React.js

| PROS                          | DESCRIPTION                            |
|:------------------------------|:---------------------------------------|
| **Perfect for dashboard UIs** | Component-based architecture available |
| **Huge ecosystem**            | Plenty of libraries                    |
| **Flexibility**               | Choose your own state management       |

| CONS          | DESCRIPTION                                  |
|:--------------|:---------------------------------------------|
| **Decisions** | Too many choices (state management, router…) |


## Vue.js

| PROS                        | DESCRIPTION                                  |
|:----------------------------|:---------------------------------------------|
| **Learning curve**          | Easy to learn                                |
| **Excellent documentation** | Docs and guides                              |
| **Flexible**                | More structure than React, less than Angular |
| **Great performance**       | Lightweight and fast                         |
| **Composition API**         | Powerful                                     |

| CONS                     | DESCRIPTION                                  |
|:-------------------------|:---------------------------------------------|
| **Fewer mobile options** | No direct mobile framework like React Native |

## Angular

| PROS                    | DESCRIPTION                                            |
|:------------------------|:-------------------------------------------------------|
| **Decisions**           | Routing, HTTP client, forms, state management built-in |
| **Type safety**         | Fewer runtime errors                                   |
| **Powerful CLI**        | Generates components, services, modules                |

| CONS                         | DESCRIPTION                                            |
|:-----------------------------|:-------------------------------------------------------|
| **Learning curve**           | Routing, HTTP client, forms, state management built-in |
| **Heavier**                  | Larger bundle size, more concepts to understand        |
| **Less flexible**            |                                                        |
| **Overkill for simple apps** |                                                        |

---

# Backend

## Node.js
| PROS                  | DESCRIPTION                                             |
|:----------------------|:--------------------------------------------------------|
| **Non-blocking I/O**  | Perfect for hook system calling external APIs           |
| **Single Language**   | JavaScript across backend, web, and React Native mobile |
| **Background Jobs**   | Bull queue excellent for hook processing                |
| **Huge Ecosystem**    | NPM has libraries for every service you need            |

| CONS                | DESCRIPTION                   |
|:--------------------|:------------------------------|
| **CPU limitations** | Slower for heavy computations |
| **Type safety**     | Though TypeScript helps       |

## Python
| PROS                     | DESCRIPTION                                                        |
|:-------------------------|:-------------------------------------------------------------------|
| **Rapid Development**    | Clean syntax, extensive libraries                                  |
| **Excellent OAuth2**     | Authlib, python-social-auth libraries                              |
| **Great API Frameworks** | FastAPI with auto-generated docs, Django Admin for user management |
| **Team Familiarity**     | Python is commonly taught and widely known                         |

| CONS                      | DESCRIPTION                                                        |
|:--------------------------|:-------------------------------------------------------------------|
| **Performance**           | Slower than Go/Node for some tasks                                 |
| **Async Complexity**      | Asyncio can be tricky compared to Node.js                          |
| **Hook System**           | Requires Celery/Redis for background processing (added complexity) |

## Go

| PROS                        | DESCRIPTION                                       |
|:----------------------------|:--------------------------------------------------|
| **Blazing Performance**     | Compiled, native execution                        |
| **Built-in Concurrency**    | Goroutines perfect for running thousands of hooks |
| **Simple Deployment**       | Single binary, no runtime dependencies            |
| **Strong Typing**           | Compile-time safety, fewer runtime errors         |
| **Excellent for Hooks**     | Native background processing without queues       |

| CONS                  | DESCRIPTION                                               |
|:----------------------|:----------------------------------------------------------|
| **Learning Curve**    | Different paradigms (no classes, explicit error handling) |
| **Younger Ecosystem** | Fewer high-level libraries                                |
| **More Verbose**      | More code for the same functionality                      |

---

# Mobile

## Kotlin

| PROS                    | DESCRIPTION                                                                    |
|:------------------------|:-------------------------------------------------------------------------------|
| **Higher performances** | Access directly Android APIs                                                   |
| **Maturity**            | Years of experience ensure bug-free features and a reliable level of security  |
| **Long-term stability** | Recommended by Google in developing Android apps                               |
| **Learning curve**      | Simple syntax quick to understand and learn, fairly similar to the one of Java |

| CONS                   | DESCRIPTION                                   |
|:-----------------------|:----------------------------------------------|
| **Android only**       | Cannot reuse code for iOS if needed later     |
| **Development time**   | Might be slower than cross-platform solutions |

## React Native

| PROS                  | DESCRIPTION                               |
|:----------------------|:------------------------------------------|
| **Code Reusability**  | Single codebase for iOS and Android       |
| **Fast Development**  | Hot reload, large component library       |
| **Community**         | Huge ecosystem, many pre-built components |

| CONS                     | DESCRIPTION                              |
|:-------------------------|:-----------------------------------------|
| **Performance Overhead** | JavaScript bridge can cause lag          |
| **Native Dependencies**  | Some features may require native modules |
| **Debugging Complexity** | JavaScript + Native debugging            |


## Flutter

| PROS                      | DESCRIPTION                                  |
|:--------------------------|:---------------------------------------------|
| **Excellent Performance** | Compiled to native code, no bridge           |
| **Beautiful UI**          | Highly customizable, pixel-perfect designs   |
| **Hot Reload**            | Excellent developer experience               |
| **Single Codebase**       | True cross-platform with consistent behavior |


| CONS                  | DESCRIPTION                            |
|:----------------------|:---------------------------------------|
| **Dart Language**     | Additional learning curve for the team |
| **Larger App Size**   | Includes Flutter engine                |
| **Younger Ecosystem** | Still growing, though rapidly          |

---

## What did we choose those languages

### **1. Why we chose React over Vue or Angular**

- **Component-Based Architecture :** We can build reusable ActionConfig and ReactionConfig components, making the UI modular and maintainable
- **Rich Ecosystem for Dashboard UIs:** React has a vast selection of UI librarties (like Material-UI or Ant Design) that will help us build a professional-looking, accessible dashboard very quickly
- **Team Familiarity:** Our team is already comfortable with Python, reducing the initial
  learning curve and allowing us to focus on the project's features rather than the language's intricacies

### **2. Why we chose Python over Node.js or Go**

- **Rapid Development & Clean Syntax:** Python allows us to build the  logic of the AREA platform (user management, service integrations…) quickly and with code that is easy for the entire team to read and debug
- **Powerful Ecosystem for Integrations:** Libraries like authlib provide excellent, well-documented tools for implementing the OAuth2
- **Data Handling:** Python is excellent for processing and transforming the data that flows between Actions and Reactions (parsing email subjects, extracting file information...)
- **Team Familiarity:** Our team is already comfortable with Python, reducing the initial learning curve and allowing us to focus on the project's features rather than the language's intricacies

### **3. Why we chose Kotlin over React Native or Flutter**

- **Best Performance and Native Feel:** Since the project scope specifically requires an Android file, using Kotlin guarantees the best possible performance and a true native user experience
- **Direct Access to Android APIs:** We can easily integrate with native Android features without dealing with the potential complexity of "bridge" layers in cross-platform frameworks
- **Reliability and Stability:** Kotlin is a modern, mature language officially supported by Google for Android development. This means excellent documentation, strong community support, and fewer unexpected bugs
- **Team Familiarity:** Our team is already comfortable with Python, reducing the initial
  learning curve and allowing us to focus on the project's features rather than the language's intricacies

## Combination

| COMPONENT         | TECHNOLOGY | DESCRIPTION                                                                           |
|:------------------|:-----------|:--------------------------------------------------------------------------------------|
| **Backend**       | **Python** | Rapid development, great API docs, rich ecosystem for OAuth2 and service integrations |
| **Web Client**    | **React**  | Reusable components, huge ecosystem, excellent for dashboard-style apps               |
| **Mobile Client** | **Kotlin** | Best Android performance, native look/feel, reliable for project scope                |

<br>

*The combination of React-Python-Kotlin in our tech stack blends React's flexibility for the frontend, Python's robustness for the backend, and Kotlin's native performance for mobile. This layer specialization allows us to use the best technology for each component. Additionally, our expertise with these technologies would help accelerate development.*

<br>

⣧⢮⢭⠛⢲⣦⣀⠀⠀⠀⠀⡀⠀⠀⠀
⠈⠻⣶⡛⠲⣄⠀⠙⠢⣀⠀⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢻⣿⣥⡬⠽⠶⠤⣌⣣⣼⡔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⣿⣧⣤⡴⢤⡴⣶⣿⣟⢯⡙⠒⠤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠘⣗⣞⣢⡟⢋⢜⣿⠛⡿⡄⢻⡮⣄⠈⠳⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠻⠮⠴⠵⢋⣇⡇⣷⢳⡀⢱⡈⢋⠛⣄⣹⣲⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣱⡇⣦⢾⣾⠿⠟⠿⠷⠷⣻⠧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⠽⠞⠊⠀⠀  _<sub>By ✧˖°. Winx magic .°˖✧</sub>_