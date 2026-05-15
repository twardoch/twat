I use Python. Let’s say I have a function that takes a value like the name of an API, or an instantiated object that points to an API endpoint. I have several options at my disposal, for example I could do `apicall("unreliable-but-cheap-api-version")` or `apicall("reliable-but-expensive-api-version")`. I’d like to be able to easily do an apicall with `("unreliable-but-cheap-api-version", "reliable-but-expensive-api-version")` and have the app attempt the first solution but if that fails fall back to the 2nd. Especially I’d like to use this together with `tenacity` and `asynciolimiter`. 

Overall, I’d like to be able to write a variety of functions that would accept Python iterables and have simple logic in them for processing each item in the iterable, and then have some mechanism like a compact decorator or some "orchestration object" where I could define some execution conditions, including: 

- multiprocessing (via `twat_mp` and `pathos`)
- limits (controlled by `asynciolimiter`)
- retries (controlled by `tenacity`)
- fallback for failures

I want to have a simple-to-use, elegant, Pythonic, unified interface for such execution orchestration. 


------

# Technical Report: Tenacity and AsyncIOLimiter - Complementary Solutions for Robust Asynchronous Applications

## Executive Summary

This report provides a comprehensive analysis of two Python libraries designed to improve reliability and efficiency in asynchronous applications: **Tenacity** and **AsyncIOLimiter**. While each addresses distinct concerns in application design—retry logic and rate limiting, respectively—they can be effectively combined to create robust, well-behaved asynchronous systems.

Tenacity offers sophisticated retry mechanisms for handling transient failures, while AsyncIOLimiter provides precise control over operation rates. When integrated, these libraries create a comprehensive solution for resilient API clients, external service integrations, and high-volume data processing pipelines, particularly in distributed systems where controlling both failure recovery and resource utilization is critical.

## Introduction to Reliability Challenges in Asynchronous Systems

Modern distributed systems face two fundamental challenges:

1. **Handling transient failures**: Network glitches, temporary service outages, and intermittent errors require intelligent retry mechanisms.
2. **Controlling request rates**: Respecting API rate limits, preventing resource exhaustion, and ensuring fair service utilization demand sophisticated rate limiting strategies.

These challenges are particularly pronounced in asynchronous applications, where concurrent operations can amplify both the frequency of failures and the potential for overwhelming dependent services.

## Tenacity: Comprehensive Retry Solution

### Core Functionality

Tenacity is a general-purpose retrying library that simplifies adding resilient retry behavior to Python functions and coroutines. It stands out for its flexibility and comprehensive feature set:

```python
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=(
        retry_if_exception_type(ConnectionError) | 
        retry_if_exception_type(TimeoutError)
    ),
    before_sleep=before_sleep_log(logger, logging.INFO)
)
async def resilient_api_call():
    # Implementation with potential failures
```

### Key Features

1. **Flexible Retry Conditions**
   - Exception-based retries with type and message filtering
   - Return value verification
   - Logical combinations of retry conditions (AND/OR operations)
   - Exception cause-based retries for handling wrapped exceptions

2. **Sophisticated Waiting Strategies**
   - Fixed intervals
   - Exponential backoff
   - Random jitter for avoiding thundering herd problems
   - Fibonacci sequences
   - Custom wait functions

3. **Stop Conditions**
   - Maximum attempt limits
   - Maximum duration limits
   - Custom stop functions
   - Composite stop conditions

4. **Execution Controls**
   - Before/after attempt callbacks
   - Before-sleep hooks for logging or notifications
   - Customizable retry error handling

5. **Framework Integration**
   - Native asyncio support
   - Tornado coroutines support
   - Context manager interface

6. **Observability**
   - Detailed statistics tracking
   - Customizable logging

### Architecture

Tenacity uses a decorator-based approach centered around the `@retry` decorator and a series of strategy classes implementing different retry behaviors. The core architecture includes:

- `BaseRetrying`: Abstract class defining the retry workflow
- `Retrying`: Implementation for synchronous functions
- `AsyncRetrying`: Implementation for asyncio coroutines
- `TornadoRetrying`: Implementation for Tornado coroutines

The separation between retry policies (what to retry), wait strategies (how long to wait), and stop conditions (when to give up) creates a highly composable system.

## AsyncIOLimiter: Efficient Rate Control

### Core Functionality

AsyncIOLimiter provides asyncio-specific rate limiting implementations for controlling the frequency of asynchronous operations:

```python
# Limit to 10 requests per 5 seconds (2/second)
limiter = Limiter(10/5)

async def api_request():
    await limiter.wait()  # Wait until a slot is available
    # Execute API call
```

### Available Limiter Types

AsyncIOLimiter offers three rate limiter implementations, each with distinct characteristics:

1. **Limiter**
   - Default implementation that accounts for CPU delays
   - Allows controlled bursts to compensate for processing delays
   - Best for general-purpose rate limiting

2. **LeakyBucketLimiter**
   - Implements the classic leaky bucket algorithm
   - Supports configurable initial burst capacity
   - Ideal for APIs with token bucket rate limiting

3. **StrictLimiter**
   - Enforces precise spacing between operations
   - No bursts allowed
   - Best for strict rate requirements or precise timing

### Key Features

1. **Simple API**
   - `wait()`: Core method to enforce rate limits
   - `cancel()`: Cancel all waiting operations
   - `breach()`: Temporarily disable rate limiting
   - `reset()`: Restore initial state
   - `wrap()`: Convenience method for wrapping coroutines

2. **Flexible Configuration**
   - Configurable rates (operations per second)
   - Adjustable burst capacities
   - Runtime rate adjustments

3. **Efficient Implementation**
   - Minimal overhead
   - No busy waiting
   - Proper handling of event loop irregularities

### Architecture

AsyncIOLimiter employs a class hierarchy with a common base interface:

- `_BaseLimiter`: Abstract base class defining the limiter interface
- `_CommonLimiterMixin`: Shared implementation details
- Concrete implementations (`Limiter`, `LeakyBucketLimiter`, `StrictLimiter`)

The implementation leverages asyncio's event loop scheduling mechanisms for precise timing control without busy waiting.

## Comparative Analysis

| Feature | Tenacity | AsyncIOLimiter |
|---------|----------|----------------|
| **Primary Focus** | Retry logic | Rate limiting |
| **Execution Control** | Retries failed operations | Throttles operation frequency |
| **Core Use Case** | Handling transient failures | Respecting rate limits |
| **Architecture Style** | Decorator-based | Object-oriented |
| **Async Support** | asyncio, Tornado | asyncio only |
| **Python Version** | 3.9+ | 3.11+ |
| **Configuration Style** | Function composition | Object initialization |
| **Module Size** | Larger, more features | Smaller, focused |

While both libraries operate in the realm of operation execution control, they address orthogonal concerns. Tenacity handles *what happens after failure*, while AsyncIOLimiter controls *when operations are allowed to execute*.

## Integration Strategies: Using Both Libraries Together

The complementary nature of these libraries makes them particularly effective when used together. Here are key integration patterns:

### Pattern 1: Outer Rate Limiting, Inner Retry

```python
limiter = AsyncLimiter(10/60)  # 10 requests per minute

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5)
)
async def resilient_api_call(endpoint, data):
    # Implementation with retry on failure
    return await make_request(endpoint, data)

async def controlled_api_call(endpoint, data):
    await limiter.wait()  # First control rate
    return await resilient_api_call(endpoint, data)  # Then handle failures
```

This pattern is ideal when:
- The rate limit must be respected regardless of retries
- Retries are relatively infrequent
- Rate limit violations are more costly than occasional delays

### Pattern 2: Retry with Rate-Limited Operations

```python
limiter = LeakyBucketLimiter(5, capacity=10)  # 5/sec with burst capacity

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(),
    retry=retry_if_exception_type(ApiError)
)
async def fetch_with_retry(item_id):
    await limiter.wait()  # Wait for rate limit with each attempt
    return await api.fetch_item(item_id)
```

This pattern is suitable when:
- Each retry must also respect the rate limit
- The operation itself is what's rate-limited, not just the initial request
- Maintaining consistent request spacing is important

### Pattern 3: Limiter-Aware Retry Strategy

```python
limiter = StrictLimiter(1)  # 1 request per second

class RateLimitExceededError(Exception):
    pass

@retry(
    stop=stop_after_attempt(5),
    wait=wait_fixed(5),  # Wait 5 seconds on rate limit errors
    retry=retry_if_exception_type(RateLimitExceededError)
)
async def adaptive_api_call():
    await limiter.wait()
    response = await make_api_call()
    
    if response.status_code == 429:  # Rate limited by external API
        limiter.rate = limiter.rate * 0.8  # Reduce our rate
        raise RateLimitExceededError()
    
    return response
```

This advanced pattern:
- Dynamically adjusts rate limiting based on external feedback
- Uses different retry strategies for different error types
- Adapts to changing conditions in the external service

## Implementation Patterns

### External API Client

```python
class RobustApiClient:
    def __init__(self, base_url, rate_limit=10, max_retries=3):
        self.base_url = base_url
        self.limiter = AsyncLimiter(rate_limit)
        self.session = aiohttp.ClientSession()
        self.max_retries = max_retries
        
    async def request(self, method, endpoint, **kwargs):
        @retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=1, max=30),
            retry=retry_if_exception_type(aiohttp.ClientError)
        )
        async def _make_request():
            async with self.limiter:
                async with self.session.request(
                    method, f"{self.base_url}/{endpoint}", **kwargs
                ) as response:
                    if response.status >= 500:
                        response.raise_for_status()
                    return await response.json()
                    
        return await _make_request()
```

### Distributed Worker System

```python
class WorkerNode:
    def __init__(self, task_queue, result_queue, worker_id):
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.worker_id = worker_id
        self.limiter = LeakyBucketLimiter(20, capacity=50)  # 20/sec with burst
        
    async def process_task(self, task):
        @retry(
            stop=stop_after_delay(60),  # Give up after a minute
            wait=wait_random_exponential(multiplier=0.5, max=10),
            retry=retry_if_exception_type(TransientError)
        )
        async def _process():
            # Process the task with potential transient errors
            return await process_task_implementation(task)
            
        await self.limiter.wait()
        result = await _process()
        await self.result_queue.put((self.worker_id, task.id, result))
```

## Performance Considerations

When integrating these libraries, consider:

1. **Retry Overhead**
   - Each retry incurs the full cost of the operation
   - Exponential backoff ensures retry attempts don't overwhelm the system
   - State tracking adds minimal overhead (~1μs per retry attempt)

2. **Rate Limiting Efficiency**
   - AsyncIOLimiter uses asyncio's event loop for timing, not busy waiting
   - The `Limiter` implementation handles timing drift efficiently
   - For high-precision requirements, `StrictLimiter` provides more precise timing at the cost of potential underutilization

3. **Combined Cost**
   - The decorating pattern adds a small amount of function call overhead
   - Memory usage increases with the number of pending operations
   - Monitoring both retry statistics and rate limiter throughput is recommended

4. **Scaling Considerations**
   - For distributed systems, consider rate limiting per node versus globally
   - Retries should account for the full system's capacity, not just individual nodes
   - For very high throughput systems (>10k req/s), custom rate limiters may be needed

## Conclusion and Recommendations

Tenacity and AsyncIOLimiter address complementary aspects of building reliable asynchronous systems. Together, they provide a comprehensive solution for resilient distributed applications.

### When to Use Tenacity Alone

- Handling unreliable external services with no rate limits
- Retrying background tasks that may occasionally fail
- Operations where timing precision is not critical

### When to Use AsyncIOLimiter Alone

- Respecting fixed API rate limits with highly reliable services
- Controlling resource utilization in high-throughput systems
- Enforcing fair resource sharing between components

### When to Use Both Together

- External API clients that need both resilience and rate control
- Distributed systems with both failure handling and resource constraints
- Multi-tenant applications requiring both reliability and fairness

For most real-world applications interfacing with external services, the combined approach provides the best balance of resilience and respectful behavior. By separating the concerns of retry logic and rate limiting, each aspect can be tuned independently as requirements evolve.

For mission-critical systems, we recommend starting with the "Outer Rate Limiting, Inner Retry" pattern, as it provides the most predictable rate control while still handling transient failures effectively.





## https://github.com/jd/tenacity

Token Usage:
GitHub Tokens: 40276
LLM Input Tokens: 0
LLM Output Tokens: 0
Total Tokens: 40276

FileTree:
.github/dependabot.yml
.github/workflows/ci.yaml
.github/workflows/deploy.yaml
.gitignore
.mergify.yml
.readthedocs.yml
doc/source/conf.py
pyproject.toml
releasenotes/notes/Fix-tests-for-typeguard-3.x-6eebfea546b6207e.yaml
releasenotes/notes/Use--for-formatting-and-validate-using-black-39ec9d57d4691778.yaml
releasenotes/notes/add-async-actions-b249c527d99723bb.yaml
releasenotes/notes/add-reno-d1ab5710f272650a.yaml
releasenotes/notes/add-retry_except_exception_type-31b31da1924d55f4.yaml
releasenotes/notes/add-stop-before-delay-a775f88ac872c923.yaml
releasenotes/notes/add-test-extra-55e869261b03e56d.yaml
releasenotes/notes/add_omitted_modules_to_import_all-2ab282f20a2c22f7.yaml
releasenotes/notes/add_retry_if_exception_cause_type-d16b918ace4ae0ad.yaml
releasenotes/notes/added_a_link_to_documentation-eefaf8f074b539f8.yaml
releasenotes/notes/after_log-50f4d73b24ce9203.yaml
releasenotes/notes/allow-mocking-of-nap-sleep-6679c50e702446f1.yaml
releasenotes/notes/annotate_code-197b93130df14042.yaml
releasenotes/notes/before_sleep_log-improvements-d8149274dfb37d7c.yaml
releasenotes/notes/clarify-reraise-option-6829667eacf4f599.yaml
releasenotes/notes/dependabot-for-github-actions-4d2464f3c0928463.yaml
releasenotes/notes/do_not_package_tests-fe5ac61940b0a5ed.yaml
releasenotes/notes/drop-deprecated-python-versions-69a05cb2e0f1034c.yaml
releasenotes/notes/drop_deprecated-7ea90b212509b082.yaml
releasenotes/notes/export-convenience-symbols-981d9611c8b754f3.yaml
releasenotes/notes/fix-async-loop-with-result-f68e913ccb425aca.yaml
releasenotes/notes/fix-local-context-overwrite-94190ba06a481631.yaml
releasenotes/notes/fix-retry-wrapper-attributes-f7a3a45b8e90f257.yaml
releasenotes/notes/fix-setuptools-config-3af71aa3592b6948.yaml
releasenotes/notes/fix-wait-typing-b26eecdb6cc0a1de.yaml
releasenotes/notes/fix_async-52b6594c8e75c4bc.yaml
releasenotes/notes/make-logger-more-compatible-5da1ddf1bab77047.yaml
releasenotes/notes/no-async-iter-6132a42e52348a75.yaml
releasenotes/notes/pr320-py3-only-wheel-tag.yaml
releasenotes/notes/py36_plus-c425fb3aa17c6682.yaml
releasenotes/notes/remove-py36-876c0416cf279d15.yaml
releasenotes/notes/retrycallstate-repr-94947f7b00ee15e1.yaml
releasenotes/notes/some-slug-for-preserve-defaults-86682846dfa18005.yaml
releasenotes/notes/sphinx_define_error-642c9cd5c165d39a.yaml
releasenotes/notes/support-timedelta-wait-unit-type-5ba1e9fc0fe45523.yaml
releasenotes/notes/timedelta-for-stop-ef6bf71b88ce9988.yaml
releasenotes/notes/trio-support-retry-22bd544800cd1f36.yaml
releasenotes/notes/wait-random-exponential-min-2a4b7eed9f002436.yaml
releasenotes/notes/wait_exponential_jitter-6ffc81dddcbaa6d3.yaml
reno.yaml
setup.cfg
setup.py
tenacity/__init__.py
tenacity/_utils.py
tenacity/after.py
tenacity/asyncio/__init__.py
tenacity/asyncio/retry.py
tenacity/before.py
tenacity/before_sleep.py
tenacity/nap.py
tenacity/retry.py
tenacity/stop.py
tenacity/tornadoweb.py
tenacity/wait.py
tests/__init__.py
tests/test_after.py
tests/test_asyncio.py
tests/test_issue_478.py
tests/test_tenacity.py
tests/test_tornado.py
tests/test_utils.py
tox.ini

Analysis:
.github/dependabot.yml
```.yml
version: 2
updates:
  - package-ecosystem: 'github-actions'
    directory: '/'
    schedule:
      interval: 'monthly'
    groups:
      github-actions:
        patterns:
          - '*'

```
.github/workflows/ci.yaml
```.yaml
name: Continuous Integration
permissions: read-all

on:
  pull_request:
    branches:
      - main

concurrency:
  # yamllint disable-line rule:line-length
  group: "${{ github.workflow }}-${{ github.head_ref || github.run_id }}"
  cancel-in-progress: true

jobs:
  test:
    timeout-minutes: 20
    runs-on: ubuntu-24.04
    strategy:
      matrix:
        include:
          - python: "3.9"
            tox: py39
          - python: "3.10"
            tox: py310
          - python: "3.11"
            tox: py311
          - python: "3.12"
            tox: py312
          - python: "3.12"
            tox: pep8
          - python: "3.13"
            tox: py313,py313-trio
          - python: "3.11"
            tox: mypy
    steps:
      - name: Checkout 🛎️
        uses: actions/checkout@v4.2.2
        with:
          fetch-depth: 0

      - name: Setup Python 🔧
        uses: actions/setup-python@v5.4.0
        with:
          python-version: ${{ matrix.python }}
          allow-prereleases: true

      - name: Build 🔧 & Test 🔍
        run: |
          pip install tox
          tox -e ${{ matrix.tox }}

```
.github/workflows/deploy.yaml
```.yaml
name: Release deploy

on:
  release:
    types:
      - published

jobs:
  publish:
    timeout-minutes: 20
    runs-on: ubuntu-latest
    steps:
      - name: Checkout 🛎️
        uses: actions/checkout@v4.2.2
        with:
          fetch-depth: 0

      - name: Setup Python 🔧
        uses: actions/setup-python@v5.4.0
        with:
          python-version: 3.11

      - name: Build 🔧 & Deploy 🚀
        env:
          PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
        run: |
          pip install tox twine wheel

          echo -e "[pypi]" >> ~/.pypirc
          echo -e "username = __token__" >> ~/.pypirc
          echo -e "password = $PYPI_TOKEN" >> ~/.pypirc

          python setup.py sdist bdist_wheel
          twine upload dist/*

```
.gitignore
```.gitignore
.idea
dist
*.pyc
*.egg-info
build
.tox/
AUTHORS
ChangeLog
.eggs/
doc/_build

/.pytest_cache

```
.mergify.yml
```.yml
queue_rules:
  - name: default
    merge_method: squash
    queue_conditions:
      - or:
        - author = jd
        - "#approved-reviews-by >= 1"
        - author = dependabot[bot]
      - or:
        - files ~= ^releasenotes/notes/
        - label = no-changelog
        - author = dependabot[bot]
      - "check-success=test (3.9, py39)"
      - "check-success=test (3.10, py310)"
      - "check-success=test (3.11, py311)"
      - "check-success=test (3.12, py312)"
      - "check-success=test (3.13, py313,py313-trio)"
      - "check-success=test (3.12, pep8)"

pull_request_rules:
  - name: warn on no changelog
    conditions:
      - -files~=^releasenotes/notes/
      - label!=no-changelog
      - -closed
    actions:
      comment:
        message: >
          ⚠️ No release notes detected. Please make sure to use
          [reno](https://docs.openstack.org/reno/latest/user/usage.html) to add
          a changelog entry.

  - name: automatic queue
    conditions: []
    actions:
      queue:

  - name: dismiss reviews
    conditions: []
    actions:
      dismiss_reviews: {}

```
.readthedocs.yml
```.yml
version: 2
python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - doc

```
doc/source/conf.py
```.py
# Copyright 2016 Étienne Bersac
# Copyright 2016 Julien Danjou
# Copyright 2016 Joshua Harlow
# Copyright 2013-2014 Ray Holder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

master_doc = "index"
project = "Tenacity"

# Add tenacity to the path, so sphinx can find the functions for autodoc.
sys.path.insert(0, os.path.abspath("../.."))

extensions = [
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "reno.sphinxext",
]

# -- Options for sphinx.ext.doctest  -----------------------------------------

# doctest_default_flags =
cwd = os.path.abspath(os.path.dirname(__file__))
tenacity_path = os.path.join(cwd, os.pardir, os.pardir)
doctest_path = [tenacity_path]
# doctest_global_setup =
# doctest_global_cleanup =
# doctest_test_doctest_blocks =

```
pyproject.toml
```.toml
[build-system]
# Minimum requirements for the build system to execute.
# PEP 508 specifications for PEP 518.
# Banned setuptools versions have well-known issues
requires = [
  "setuptools >= 21.0.0,!=24.0.0,!=34.0.0,!=34.0.1,!=34.0.2,!=34.0.3,!=34.1.0,!=34.1.1,!=34.2.0,!=34.3.0,!=34.3.1,!=34.3.2,!=36.2.0",  # PSF/ZPL
  "setuptools_scm[toml]>=3.4",
]
build-backend="setuptools.build_meta"

[tool.ruff]
line-length = 88
indent-width = 4
target-version = "py39"

[tool.mypy]
strict = true
files = ["tenacity", "tests"]
show_error_codes = true

[[tool.mypy.overrides]]
module = "tornado.*"
ignore_missing_imports = true

[tool.setuptools_scm]

```
releasenotes/notes/Fix-tests-for-typeguard-3.x-6eebfea546b6207e.yaml
```.yaml
---
fixes:
  - "Fixes test failures with typeguard 3.x"

```
releasenotes/notes/Use--for-formatting-and-validate-using-black-39ec9d57d4691778.yaml
```.yaml
---
other:
  - "Use `black` for code formatting and validate using `black --check`. Code compatibility: py26-py39."
  - "Enforce maximal line length to 120 symbols"

```
releasenotes/notes/add-async-actions-b249c527d99723bb.yaml
```.yaml
---
features:
  - |
    Added the ability to use async functions for retries. This way, you can now use
    asyncio coroutines for retry strategy predicates.

```
releasenotes/notes/add-reno-d1ab5710f272650a.yaml
```.yaml
---
features:
  - Add reno (changelog system)

```
releasenotes/notes/add-retry_except_exception_type-31b31da1924d55f4.yaml
```.yaml
---
features:
  - Add ``retry_if_not_exception_type()`` that allows to retry if a raised exception doesn't match given exceptions.

```
releasenotes/notes/add-stop-before-delay-a775f88ac872c923.yaml
```.yaml
---
features:
  - |
    Added a new stop function: stop_before_delay, which will stop execution
    if the next sleep time would cause overall delay to exceed the specified delay. 
    Useful for use cases where you have some upper bound on retry times that you must
    not exceed, so returning before that timeout is preferable than returning after that timeout.
```
releasenotes/notes/add-test-extra-55e869261b03e56d.yaml
```.yaml
---
other:
  - Add a \"test\" extra

```
releasenotes/notes/add_omitted_modules_to_import_all-2ab282f20a2c22f7.yaml
```.yaml
---
other:
  - Add `retry_if_exception_cause_type`and `wait_exponential_jitter` to __all__ of init.py
```
releasenotes/notes/add_retry_if_exception_cause_type-d16b918ace4ae0ad.yaml
```.yaml
---
features:
  - |
    Add a new `retry_base` class called `retry_if_exception_cause_type` that
    checks, recursively, if any of the causes of the raised exception is of a certain type.

```
releasenotes/notes/added_a_link_to_documentation-eefaf8f074b539f8.yaml
```.yaml
---
other:
  - |
    Added a link to the documentation, as code snippets are not being rendered properly
    Changed branch name to main in index.rst

```
releasenotes/notes/after_log-50f4d73b24ce9203.yaml
```.yaml
---
fixes:
  - "Fix after_log logger format: function name was used with delay formatting."

```
releasenotes/notes/allow-mocking-of-nap-sleep-6679c50e702446f1.yaml
```.yaml
---
other:
  - Unit tests can now mock ``nap.sleep()`` for testing in all tenacity usage styles
```
releasenotes/notes/annotate_code-197b93130df14042.yaml
```.yaml
---
other:
  - Add type annotations to cover all public API.

```
releasenotes/notes/before_sleep_log-improvements-d8149274dfb37d7c.yaml
```.yaml
---
features:
  - Add an ``exc_info`` option to the ``before_sleep_log()`` strategy.
```
releasenotes/notes/clarify-reraise-option-6829667eacf4f599.yaml
```.yaml
---
prelude: >
    Clarify usage of `reraise` keyword argument

```
releasenotes/notes/dependabot-for-github-actions-4d2464f3c0928463.yaml
```.yaml
---
other:
  - |
    Add a Dependabot configuration submit PRs monthly (as needed)
    to keep GitHub action versions updated.

```
releasenotes/notes/do_not_package_tests-fe5ac61940b0a5ed.yaml
```.yaml
---
other:
  - Do not package tests with tenacity.

```
releasenotes/notes/drop-deprecated-python-versions-69a05cb2e0f1034c.yaml
```.yaml
---
other:
  - |
    Drop support for deprecated Python versions (2.7 and 3.5)

```
releasenotes/notes/drop_deprecated-7ea90b212509b082.yaml
```.yaml
---
upgrade:
  - "Removed `BaseRetrying.call`: was long time deprecated and produced `DeprecationWarning`"
  - "Removed `BaseRetrying.fn`: was noted as deprecated"
  - "API change: `BaseRetrying.begin()` do not require arguments anymore as it not setting `BaseRetrying.fn`"

```
releasenotes/notes/export-convenience-symbols-981d9611c8b754f3.yaml
```.yaml
---
features:
  - Explicitly export convenience symbols from tenacity root module

```
releasenotes/notes/fix-async-loop-with-result-f68e913ccb425aca.yaml
```.yaml
---
fixes:
  - |
    Fix async loop with retrying code block when result is available.

```
releasenotes/notes/fix-local-context-overwrite-94190ba06a481631.yaml
```.yaml
---
fixes:
  - |
    Avoid overwriting local contexts when applying the retry decorator.

```
releasenotes/notes/fix-retry-wrapper-attributes-f7a3a45b8e90f257.yaml
```.yaml
---
fixes:
  - |
    Restore the value of the `retry` attribute for wrapped functions. Also,
    clarify that those attributes are write-only and statistics should be
    read from the function attribute directly.

```
releasenotes/notes/fix-setuptools-config-3af71aa3592b6948.yaml
```.yaml
---
fixes:
  - Fix setuptools config to include tenacity.asyncio package in release distributions.

```
releasenotes/notes/fix-wait-typing-b26eecdb6cc0a1de.yaml
```.yaml
---
fixes:
  - |
    Argument `wait` was improperly annotated, making mypy checks fail.
    Now it's annotated as `typing.Union[wait_base, typing.Callable[["RetryCallState"], typing.Union[float, int]]]`

```
releasenotes/notes/fix_async-52b6594c8e75c4bc.yaml
```.yaml
---
fixes:
  - "Fix issue #288 : __name__ and other attributes for async functions"

```
releasenotes/notes/make-logger-more-compatible-5da1ddf1bab77047.yaml
```.yaml
---
fixes:
  - |
    Use str.format to format the logs internally to make logging compatible with other logger such as loguru.

```
releasenotes/notes/no-async-iter-6132a42e52348a75.yaml
```.yaml
---
fixes:
  - |
    `AsyncRetrying` was erroneously implementing `__iter__()`, making tenacity
    retrying mechanism working but in a synchronous fashion and not waiting as
    expected. This interface has been removed, `__aiter__()` should be used
    instead.

```
releasenotes/notes/pr320-py3-only-wheel-tag.yaml
```.yaml
---
other: >-
  Corrected the PyPI-published wheel tag to match the
  metadata saying that the release is Python 3 only.
...

```
releasenotes/notes/py36_plus-c425fb3aa17c6682.yaml
```.yaml
---
features:
  - Most part of the code is type annotated.
  - Python 3.10 support has been added.

```
releasenotes/notes/remove-py36-876c0416cf279d15.yaml
```.yaml
---
upgrade:
  - |
    Support for Python 3.6 has been removed.

```
releasenotes/notes/retrycallstate-repr-94947f7b00ee15e1.yaml
```.yaml
---
features:
  - Add a ``__repr__`` method to ``RetryCallState`` objects for easier debugging.

```
releasenotes/notes/some-slug-for-preserve-defaults-86682846dfa18005.yaml
```.yaml
---
fixes:
  - |
    Preserve __defaults__ and __kwdefaults__ through retry decorator

```
releasenotes/notes/sphinx_define_error-642c9cd5c165d39a.yaml
```.yaml
---
fixes: Sphinx build error where Sphinx complains about an undefined class.

```
releasenotes/notes/support-timedelta-wait-unit-type-5ba1e9fc0fe45523.yaml
```.yaml
---
features:
  - Add ``datetime.timedelta`` as accepted wait unit type.

```
releasenotes/notes/timedelta-for-stop-ef6bf71b88ce9988.yaml
```.yaml
---
features:
  - |
    - accept ``datetime.timedelta`` instances as argument to ``tenacity.stop.stop_after_delay``

```
releasenotes/notes/trio-support-retry-22bd544800cd1f36.yaml
```.yaml
---
features:
  - |
    If you're using `Trio <https://trio.readthedocs.io>`__, then
    ``@retry`` now works automatically. It's no longer necessary to
    pass ``sleep=trio.sleep``.

```
releasenotes/notes/wait-random-exponential-min-2a4b7eed9f002436.yaml
```.yaml
---
fixes:
  - |
    Respects `min` arg for `wait_random_exponential`

```
releasenotes/notes/wait_exponential_jitter-6ffc81dddcbaa6d3.yaml
```.yaml
---
features:
  - |
    Implement a wait.wait_exponential_jitter per Google's storage retry guide.
    See https://cloud.google.com/storage/docs/retry-strategy

```
reno.yaml
```.yaml
---
unreleased_version_title: Unreleased

```
setup.cfg
```.cfg
[metadata]
name = tenacity
license = Apache 2.0
url = https://github.com/jd/tenacity
summary = Retry code until it succeeds
long_description = Tenacity is a general-purpose retrying library to simplify the task of adding retry behavior to just about anything.
author = Julien Danjou
author_email = julien@danjou.info
home_page = https://github.com/jd/tenacity
classifier =
    Intended Audience :: Developers
    License :: OSI Approved :: Apache Software License
    Programming Language :: Python
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3 :: Only
    Programming Language :: Python :: 3.9
    Programming Language :: Python :: 3.10
    Programming Language :: Python :: 3.11
    Programming Language :: Python :: 3.12
    Programming Language :: Python :: 3.13
    Topic :: Utilities

[options]
install_requires =
python_requires = >=3.9
packages = find:

[options.packages.find]
include = tenacity*
exclude = tests

[options.package_data]
tenacity = py.typed

[options.extras_require]
doc =
    reno
    sphinx
test =
    pytest
    tornado>=4.5
    typeguard

[tool:pytest]
filterwarnings =
    # Show any DeprecationWarnings once
    once::DeprecationWarning

```
setup.py
```.py
#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools

setuptools.setup(
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
)

```
tenacity/__init__.py
```.py
# Copyright 2016-2018 Julien Danjou
# Copyright 2017 Elisey Zanko
# Copyright 2016 Étienne Bersac
# Copyright 2016 Joshua Harlow
# Copyright 2013-2014 Ray Holder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import dataclasses
import functools
import sys
import threading
import time
import typing as t
import warnings
from abc import ABC, abstractmethod
from concurrent import futures

from . import _utils

# Import all built-in retry strategies for easier usage.
from .retry import retry_base  # noqa
from .retry import retry_all  # noqa
from .retry import retry_always  # noqa
from .retry import retry_any  # noqa
from .retry import retry_if_exception  # noqa
from .retry import retry_if_exception_type  # noqa
from .retry import retry_if_exception_cause_type  # noqa
from .retry import retry_if_not_exception_type  # noqa
from .retry import retry_if_not_result  # noqa
from .retry import retry_if_result  # noqa
from .retry import retry_never  # noqa
from .retry import retry_unless_exception_type  # noqa
from .retry import retry_if_exception_message  # noqa
from .retry import retry_if_not_exception_message  # noqa

# Import all nap strategies for easier usage.
from .nap import sleep  # noqa
from .nap import sleep_using_event  # noqa

# Import all built-in stop strategies for easier usage.
from .stop import stop_after_attempt  # noqa
from .stop import stop_after_delay  # noqa
from .stop import stop_before_delay  # noqa
from .stop import stop_all  # noqa
from .stop import stop_any  # noqa
from .stop import stop_never  # noqa
from .stop import stop_when_event_set  # noqa

# Import all built-in wait strategies for easier usage.
from .wait import wait_chain  # noqa
from .wait import wait_combine  # noqa
from .wait import wait_exponential  # noqa
from .wait import wait_fixed  # noqa
from .wait import wait_incrementing  # noqa
from .wait import wait_none  # noqa
from .wait import wait_random  # noqa
from .wait import wait_random_exponential  # noqa
from .wait import wait_random_exponential as wait_full_jitter  # noqa
from .wait import wait_exponential_jitter  # noqa

# Import all built-in before strategies for easier usage.
from .before import before_log  # noqa
from .before import before_nothing  # noqa

# Import all built-in after strategies for easier usage.
from .after import after_log  # noqa
from .after import after_nothing  # noqa

# Import all built-in before sleep strategies for easier usage.
from .before_sleep import before_sleep_log  # noqa
from .before_sleep import before_sleep_nothing  # noqa

try:
    import tornado
except ImportError:
    tornado = None

if t.TYPE_CHECKING:
    import types

    from . import asyncio as tasyncio
    from .retry import RetryBaseT
    from .stop import StopBaseT
    from .wait import WaitBaseT


WrappedFnReturnT = t.TypeVar("WrappedFnReturnT")
WrappedFn = t.TypeVar("WrappedFn", bound=t.Callable[..., t.Any])


dataclass_kwargs = {}
if sys.version_info >= (3, 10):
    dataclass_kwargs.update({"slots": True})


@dataclasses.dataclass(**dataclass_kwargs)
class IterState:
    actions: t.List[t.Callable[["RetryCallState"], t.Any]] = dataclasses.field(
        default_factory=list
    )
    retry_run_result: bool = False
    delay_since_first_attempt: int = 0
    stop_run_result: bool = False
    is_explicit_retry: bool = False

    def reset(self) -> None:
        self.actions = []
        self.retry_run_result = False
        self.delay_since_first_attempt = 0
        self.stop_run_result = False
        self.is_explicit_retry = False


class TryAgain(Exception):
    """Always retry the executed function when raised."""


NO_RESULT = object()


class DoAttempt:
    pass


class DoSleep(float):
    pass


class BaseAction:
    """Base class for representing actions to take by retry object.

    Concrete implementations must define:
    - __init__: to initialize all necessary fields
    - REPR_FIELDS: class variable specifying attributes to include in repr(self)
    - NAME: for identification in retry object methods and callbacks
    """

    REPR_FIELDS: t.Sequence[str] = ()
    NAME: t.Optional[str] = None

    def __repr__(self) -> str:
        state_str = ", ".join(
            f"{field}={getattr(self, field)!r}" for field in self.REPR_FIELDS
        )
        return f"{self.__class__.__name__}({state_str})"

    def __str__(self) -> str:
        return repr(self)


class RetryAction(BaseAction):
    REPR_FIELDS = ("sleep",)
    NAME = "retry"

    def __init__(self, sleep: t.SupportsFloat) -> None:
        self.sleep = float(sleep)


_unset = object()


def _first_set(first: t.Union[t.Any, object], second: t.Any) -> t.Any:
    return second if first is _unset else first


class RetryError(Exception):
    """Encapsulates the last attempt instance right before giving up."""

    def __init__(self, last_attempt: "Future") -> None:
        self.last_attempt = last_attempt
        super().__init__(last_attempt)

    def reraise(self) -> t.NoReturn:
        if self.last_attempt.failed:
            raise self.last_attempt.result()
        raise self

    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.last_attempt}]"


class AttemptManager:
    """Manage attempt context."""

    def __init__(self, retry_state: "RetryCallState"):
        self.retry_state = retry_state

    def __enter__(self) -> None:
        pass

    def __exit__(
        self,
        exc_type: t.Optional[t.Type[BaseException]],
        exc_value: t.Optional[BaseException],
        traceback: t.Optional["types.TracebackType"],
    ) -> t.Optional[bool]:
        if exc_type is not None and exc_value is not None:
            self.retry_state.set_exception((exc_type, exc_value, traceback))
            return True  # Swallow exception.
        else:
            # We don't have the result, actually.
            self.retry_state.set_result(None)
            return None


class BaseRetrying(ABC):
    def __init__(
        self,
        sleep: t.Callable[[t.Union[int, float]], None] = sleep,
        stop: "StopBaseT" = stop_never,
        wait: "WaitBaseT" = wait_none(),
        retry: "RetryBaseT" = retry_if_exception_type(),
        before: t.Callable[["RetryCallState"], None] = before_nothing,
        after: t.Callable[["RetryCallState"], None] = after_nothing,
        before_sleep: t.Optional[t.Callable[["RetryCallState"], None]] = None,
        reraise: bool = False,
        retry_error_cls: t.Type[RetryError] = RetryError,
        retry_error_callback: t.Optional[t.Callable[["RetryCallState"], t.Any]] = None,
    ):
        self.sleep = sleep
        self.stop = stop
        self.wait = wait
        self.retry = retry
        self.before = before
        self.after = after
        self.before_sleep = before_sleep
        self.reraise = reraise
        self._local = threading.local()
        self.retry_error_cls = retry_error_cls
        self.retry_error_callback = retry_error_callback

    def copy(
        self,
        sleep: t.Union[t.Callable[[t.Union[int, float]], None], object] = _unset,
        stop: t.Union["StopBaseT", object] = _unset,
        wait: t.Union["WaitBaseT", object] = _unset,
        retry: t.Union[retry_base, object] = _unset,
        before: t.Union[t.Callable[["RetryCallState"], None], object] = _unset,
        after: t.Union[t.Callable[["RetryCallState"], None], object] = _unset,
        before_sleep: t.Union[
            t.Optional[t.Callable[["RetryCallState"], None]], object
        ] = _unset,
        reraise: t.Union[bool, object] = _unset,
        retry_error_cls: t.Union[t.Type[RetryError], object] = _unset,
        retry_error_callback: t.Union[
            t.Optional[t.Callable[["RetryCallState"], t.Any]], object
        ] = _unset,
    ) -> "BaseRetrying":
        """Copy this object with some parameters changed if needed."""
        return self.__class__(
            sleep=_first_set(sleep, self.sleep),
            stop=_first_set(stop, self.stop),
            wait=_first_set(wait, self.wait),
            retry=_first_set(retry, self.retry),
            before=_first_set(before, self.before),
            after=_first_set(after, self.after),
            before_sleep=_first_set(before_sleep, self.before_sleep),
            reraise=_first_set(reraise, self.reraise),
            retry_error_cls=_first_set(retry_error_cls, self.retry_error_cls),
            retry_error_callback=_first_set(
                retry_error_callback, self.retry_error_callback
            ),
        )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} object at 0x{id(self):x} ("
            f"stop={self.stop}, "
            f"wait={self.wait}, "
            f"sleep={self.sleep}, "
            f"retry={self.retry}, "
            f"before={self.before}, "
            f"after={self.after})>"
        )

    @property
    def statistics(self) -> t.Dict[str, t.Any]:
        """Return a dictionary of runtime statistics.

        This dictionary will be empty when the controller has never been
        ran. When it is running or has ran previously it should have (but
        may not) have useful and/or informational keys and values when
        running is underway and/or completed.

        .. warning:: The keys in this dictionary **should** be some what
                     stable (not changing), but there existence **may**
                     change between major releases as new statistics are
                     gathered or removed so before accessing keys ensure that
                     they actually exist and handle when they do not.

        .. note:: The values in this dictionary are local to the thread
                  running call (so if multiple threads share the same retrying
                  object - either directly or indirectly) they will each have
                  there own view of statistics they have collected (in the
                  future we may provide a way to aggregate the various
                  statistics from each thread).
        """
        try:
            return self._local.statistics  # type: ignore[no-any-return]
        except AttributeError:
            self._local.statistics = t.cast(t.Dict[str, t.Any], {})
            return self._local.statistics

    @property
    def iter_state(self) -> IterState:
        try:
            return self._local.iter_state  # type: ignore[no-any-return]
        except AttributeError:
            self._local.iter_state = IterState()
            return self._local.iter_state

    def wraps(self, f: WrappedFn) -> WrappedFn:
        """Wrap a function for retrying.

        :param f: A function to wraps for retrying.
        """

        @functools.wraps(
            f, functools.WRAPPER_ASSIGNMENTS + ("__defaults__", "__kwdefaults__")
        )
        def wrapped_f(*args: t.Any, **kw: t.Any) -> t.Any:
            # Always create a copy to prevent overwriting the local contexts when
            # calling the same wrapped functions multiple times in the same stack
            copy = self.copy()
            wrapped_f.statistics = copy.statistics  # type: ignore[attr-defined]
            return copy(f, *args, **kw)

        def retry_with(*args: t.Any, **kwargs: t.Any) -> WrappedFn:
            return self.copy(*args, **kwargs).wraps(f)

        # Preserve attributes
        wrapped_f.retry = self  # type: ignore[attr-defined]
        wrapped_f.retry_with = retry_with  # type: ignore[attr-defined]
        wrapped_f.statistics = {}  # type: ignore[attr-defined]

        return wrapped_f  # type: ignore[return-value]

    def begin(self) -> None:
        self.statistics.clear()
        self.statistics["start_time"] = time.monotonic()
        self.statistics["attempt_number"] = 1
        self.statistics["idle_for"] = 0

    def _add_action_func(self, fn: t.Callable[..., t.Any]) -> None:
        self.iter_state.actions.append(fn)

    def _run_retry(self, retry_state: "RetryCallState") -> None:
        self.iter_state.retry_run_result = self.retry(retry_state)

    def _run_wait(self, retry_state: "RetryCallState") -> None:
        if self.wait:
            sleep = self.wait(retry_state)
        else:
            sleep = 0.0

        retry_state.upcoming_sleep = sleep

    def _run_stop(self, retry_state: "RetryCallState") -> None:
        self.statistics["delay_since_first_attempt"] = retry_state.seconds_since_start
        self.iter_state.stop_run_result = self.stop(retry_state)

    def iter(self, retry_state: "RetryCallState") -> t.Union[DoAttempt, DoSleep, t.Any]:  # noqa
        self._begin_iter(retry_state)
        result = None
        for action in self.iter_state.actions:
            result = action(retry_state)
        return result

    def _begin_iter(self, retry_state: "RetryCallState") -> None:  # noqa
        self.iter_state.reset()

        fut = retry_state.outcome
        if fut is None:
            if self.before is not None:
                self._add_action_func(self.before)
            self._add_action_func(lambda rs: DoAttempt())
            return

        self.iter_state.is_explicit_retry = fut.failed and isinstance(
            fut.exception(), TryAgain
        )
        if not self.iter_state.is_explicit_retry:
            self._add_action_func(self._run_retry)
        self._add_action_func(self._post_retry_check_actions)

    def _post_retry_check_actions(self, retry_state: "RetryCallState") -> None:
        if not (self.iter_state.is_explicit_retry or self.iter_state.retry_run_result):
            self._add_action_func(lambda rs: rs.outcome.result())
            return

        if self.after is not None:
            self._add_action_func(self.after)

        self._add_action_func(self._run_wait)
        self._add_action_func(self._run_stop)
        self._add_action_func(self._post_stop_check_actions)

    def _post_stop_check_actions(self, retry_state: "RetryCallState") -> None:
        if self.iter_state.stop_run_result:
            if self.retry_error_callback:
                self._add_action_func(self.retry_error_callback)
                return

            def exc_check(rs: "RetryCallState") -> None:
                fut = t.cast(Future, rs.outcome)
                retry_exc = self.retry_error_cls(fut)
                if self.reraise:
                    raise retry_exc.reraise()
                raise retry_exc from fut.exception()

            self._add_action_func(exc_check)
            return

        def next_action(rs: "RetryCallState") -> None:
            sleep = rs.upcoming_sleep
            rs.next_action = RetryAction(sleep)
            rs.idle_for += sleep
            self.statistics["idle_for"] += sleep
            self.statistics["attempt_number"] += 1

        self._add_action_func(next_action)

        if self.before_sleep is not None:
            self._add_action_func(self.before_sleep)

        self._add_action_func(lambda rs: DoSleep(rs.upcoming_sleep))

    def __iter__(self) -> t.Generator[AttemptManager, None, None]:
        self.begin()

        retry_state = RetryCallState(self, fn=None, args=(), kwargs={})
        while True:
            do = self.iter(retry_state=retry_state)
            if isinstance(do, DoAttempt):
                yield AttemptManager(retry_state=retry_state)
            elif isinstance(do, DoSleep):
                retry_state.prepare_for_next_attempt()
                self.sleep(do)
            else:
                break

    @abstractmethod
    def __call__(
        self,
        fn: t.Callable[..., WrappedFnReturnT],
        *args: t.Any,
        **kwargs: t.Any,
    ) -> WrappedFnReturnT:
        pass


class Retrying(BaseRetrying):
    """Retrying controller."""

    def __call__(
        self,
        fn: t.Callable[..., WrappedFnReturnT],
        *args: t.Any,
        **kwargs: t.Any,
    ) -> WrappedFnReturnT:
        self.begin()

        retry_state = RetryCallState(retry_object=self, fn=fn, args=args, kwargs=kwargs)
        while True:
            do = self.iter(retry_state=retry_state)
            if isinstance(do, DoAttempt):
                try:
                    result = fn(*args, **kwargs)
                except BaseException:  # noqa: B902
                    retry_state.set_exception(sys.exc_info())  # type: ignore[arg-type]
                else:
                    retry_state.set_result(result)
            elif isinstance(do, DoSleep):
                retry_state.prepare_for_next_attempt()
                self.sleep(do)
            else:
                return do  # type: ignore[no-any-return]


if sys.version_info >= (3, 9):
    FutureGenericT = futures.Future[t.Any]
else:
    FutureGenericT = futures.Future


class Future(FutureGenericT):
    """Encapsulates a (future or past) attempted call to a target function."""

    def __init__(self, attempt_number: int) -> None:
        super().__init__()
        self.attempt_number = attempt_number

    @property
    def failed(self) -> bool:
        """Return whether a exception is being held in this future."""
        return self.exception() is not None

    @classmethod
    def construct(
        cls, attempt_number: int, value: t.Any, has_exception: bool
    ) -> "Future":
        """Construct a new Future object."""
        fut = cls(attempt_number)
        if has_exception:
            fut.set_exception(value)
        else:
            fut.set_result(value)
        return fut


class RetryCallState:
    """State related to a single call wrapped with Retrying."""

    def __init__(
        self,
        retry_object: BaseRetrying,
        fn: t.Optional[WrappedFn],
        args: t.Any,
        kwargs: t.Any,
    ) -> None:
        #: Retry call start timestamp
        self.start_time = time.monotonic()
        #: Retry manager object
        self.retry_object = retry_object
        #: Function wrapped by this retry call
        self.fn = fn
        #: Arguments of the function wrapped by this retry call
        self.args = args
        #: Keyword arguments of the function wrapped by this retry call
        self.kwargs = kwargs

        #: The number of the current attempt
        self.attempt_number: int = 1
        #: Last outcome (result or exception) produced by the function
        self.outcome: t.Optional[Future] = None
        #: Timestamp of the last outcome
        self.outcome_timestamp: t.Optional[float] = None
        #: Time spent sleeping in retries
        self.idle_for: float = 0.0
        #: Next action as decided by the retry manager
        self.next_action: t.Optional[RetryAction] = None
        #: Next sleep time as decided by the retry manager.
        self.upcoming_sleep: float = 0.0

    @property
    def seconds_since_start(self) -> t.Optional[float]:
        if self.outcome_timestamp is None:
            return None
        return self.outcome_timestamp - self.start_time

    def prepare_for_next_attempt(self) -> None:
        self.outcome = None
        self.outcome_timestamp = None
        self.attempt_number += 1
        self.next_action = None

    def set_result(self, val: t.Any) -> None:
        ts = time.monotonic()
        fut = Future(self.attempt_number)
        fut.set_result(val)
        self.outcome, self.outcome_timestamp = fut, ts

    def set_exception(
        self,
        exc_info: t.Tuple[
            t.Type[BaseException], BaseException, "types.TracebackType| None"
        ],
    ) -> None:
        ts = time.monotonic()
        fut = Future(self.attempt_number)
        fut.set_exception(exc_info[1])
        self.outcome, self.outcome_timestamp = fut, ts

    def __repr__(self) -> str:
        if self.outcome is None:
            result = "none yet"
        elif self.outcome.failed:
            exception = self.outcome.exception()
            result = f"failed ({exception.__class__.__name__} {exception})"
        else:
            result = f"returned {self.outcome.result()}"

        slept = float(round(self.idle_for, 2))
        clsname = self.__class__.__name__
        return f"<{clsname} {id(self)}: attempt #{self.attempt_number}; slept for {slept}; last result: {result}>"


@t.overload
def retry(func: WrappedFn) -> WrappedFn: ...


@t.overload
def retry(
    sleep: t.Callable[[t.Union[int, float]], t.Union[None, t.Awaitable[None]]] = sleep,
    stop: "StopBaseT" = stop_never,
    wait: "WaitBaseT" = wait_none(),
    retry: "t.Union[RetryBaseT, tasyncio.retry.RetryBaseT]" = retry_if_exception_type(),
    before: t.Callable[
        ["RetryCallState"], t.Union[None, t.Awaitable[None]]
    ] = before_nothing,
    after: t.Callable[
        ["RetryCallState"], t.Union[None, t.Awaitable[None]]
    ] = after_nothing,
    before_sleep: t.Optional[
        t.Callable[["RetryCallState"], t.Union[None, t.Awaitable[None]]]
    ] = None,
    reraise: bool = False,
    retry_error_cls: t.Type["RetryError"] = RetryError,
    retry_error_callback: t.Optional[
        t.Callable[["RetryCallState"], t.Union[t.Any, t.Awaitable[t.Any]]]
    ] = None,
) -> t.Callable[[WrappedFn], WrappedFn]: ...


def retry(*dargs: t.Any, **dkw: t.Any) -> t.Any:
    """Wrap a function with a new `Retrying` object.

    :param dargs: positional arguments passed to Retrying object
    :param dkw: keyword arguments passed to the Retrying object
    """
    # support both @retry and @retry() as valid syntax
    if len(dargs) == 1 and callable(dargs[0]):
        return retry()(dargs[0])
    else:

        def wrap(f: WrappedFn) -> WrappedFn:
            if isinstance(f, retry_base):
                warnings.warn(
                    f"Got retry_base instance ({f.__class__.__name__}) as callable argument, "
                    f"this will probably hang indefinitely (did you mean retry={f.__class__.__name__}(...)?)"
                )
            r: "BaseRetrying"
            if _utils.is_coroutine_callable(f):
                r = AsyncRetrying(*dargs, **dkw)
            elif (
                tornado
                and hasattr(tornado.gen, "is_coroutine_function")
                and tornado.gen.is_coroutine_function(f)
            ):
                r = TornadoRetrying(*dargs, **dkw)
            else:
                r = Retrying(*dargs, **dkw)

            return r.wraps(f)

        return wrap


from tenacity.asyncio import AsyncRetrying  # noqa:E402,I100

if tornado:
    from tenacity.tornadoweb import TornadoRetrying


__all__ = [
    "retry_base",
    "retry_all",
    "retry_always",
    "retry_any",
    "retry_if_exception",
    "retry_if_exception_type",
    "retry_if_exception_cause_type",
    "retry_if_not_exception_type",
    "retry_if_not_result",
    "retry_if_result",
    "retry_never",
    "retry_unless_exception_type",
    "retry_if_exception_message",
    "retry_if_not_exception_message",
    "sleep",
    "sleep_using_event",
    "stop_after_attempt",
    "stop_after_delay",
    "stop_before_delay",
    "stop_all",
    "stop_any",
    "stop_never",
    "stop_when_event_set",
    "wait_chain",
    "wait_combine",
    "wait_exponential",
    "wait_fixed",
    "wait_incrementing",
    "wait_none",
    "wait_random",
    "wait_random_exponential",
    "wait_full_jitter",
    "wait_exponential_jitter",
    "before_log",
    "before_nothing",
    "after_log",
    "after_nothing",
    "before_sleep_log",
    "before_sleep_nothing",
    "retry",
    "WrappedFn",
    "TryAgain",
    "NO_RESULT",
    "DoAttempt",
    "DoSleep",
    "BaseAction",
    "RetryAction",
    "RetryError",
    "AttemptManager",
    "BaseRetrying",
    "Retrying",
    "Future",
    "RetryCallState",
    "AsyncRetrying",
]

```
tenacity/_utils.py
```.py
# Copyright 2016 Julien Danjou
# Copyright 2016 Joshua Harlow
# Copyright 2013-2014 Ray Holder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import functools
import inspect
import sys
import typing
from datetime import timedelta


# sys.maxsize:
# An integer giving the maximum value a variable of type Py_ssize_t can take.
MAX_WAIT = sys.maxsize / 2


def find_ordinal(pos_num: int) -> str:
    # See: https://en.wikipedia.org/wiki/English_numerals#Ordinal_numbers
    if pos_num == 0:
        return "th"
    elif pos_num == 1:
        return "st"
    elif pos_num == 2:
        return "nd"
    elif pos_num == 3:
        return "rd"
    elif 4 <= pos_num <= 20:
        return "th"
    else:
        return find_ordinal(pos_num % 10)


def to_ordinal(pos_num: int) -> str:
    return f"{pos_num}{find_ordinal(pos_num)}"


def get_callback_name(cb: typing.Callable[..., typing.Any]) -> str:
    """Get a callback fully-qualified name.

    If no name can be produced ``repr(cb)`` is called and returned.
    """
    segments = []
    try:
        segments.append(cb.__qualname__)
    except AttributeError:
        try:
            segments.append(cb.__name__)
        except AttributeError:
            pass
    if not segments:
        return repr(cb)
    else:
        try:
            # When running under sphinx it appears this can be none?
            if cb.__module__:
                segments.insert(0, cb.__module__)
        except AttributeError:
            pass
        return ".".join(segments)


time_unit_type = typing.Union[int, float, timedelta]


def to_seconds(time_unit: time_unit_type) -> float:
    return float(
        time_unit.total_seconds() if isinstance(time_unit, timedelta) else time_unit
    )


def is_coroutine_callable(call: typing.Callable[..., typing.Any]) -> bool:
    if inspect.isclass(call):
        return False
    if inspect.iscoroutinefunction(call):
        return True
    partial_call = isinstance(call, functools.partial) and call.func
    dunder_call = partial_call or getattr(call, "__call__", None)
    return inspect.iscoroutinefunction(dunder_call)


def wrap_to_async_func(
    call: typing.Callable[..., typing.Any],
) -> typing.Callable[..., typing.Awaitable[typing.Any]]:
    if is_coroutine_callable(call):
        return call

    async def inner(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return call(*args, **kwargs)

    return inner

```
tenacity/after.py
```.py
# Copyright 2016 Julien Danjou
# Copyright 2016 Joshua Harlow
# Copyright 2013-2014 Ray Holder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing

from tenacity import _utils

if typing.TYPE_CHECKING:
    import logging

    from tenacity import RetryCallState


def after_nothing(retry_state: "RetryCallState") -> None:
    """After call strategy that does nothing."""


def after_log(
    logger: "logging.Logger",
    log_level: int,
    sec_format: str = "%0.3f",
) -> typing.Callable[["RetryCallState"], None]:
    """After call strategy that logs to some logger the finished attempt."""

    def log_it(retry_state: "RetryCallState") -> None:
        if retry_state.fn is None:
            # NOTE(sileht): can't really happen, but we must please mypy
            fn_name = "<unknown>"
        else:
            fn_name = _utils.get_callback_name(retry_state.fn)
        logger.log(
            log_level,
            f"Finished call to '{fn_name}' "
            f"after {sec_format % retry_state.seconds_since_start}(s), "
            f"this was the {_utils.to_ordinal(retry_state.attempt_number)} time calling it.",
        )

    return log_it

```
tenacity/asyncio/__init__.py
```.py
# Copyright 2016 Étienne Bersac
# Copyright 2016 Julien Danjou
# Copyright 2016 Joshua Harlow
# Copyright 2013-2014 Ray Holder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import sys
import typing as t

import tenacity
from tenacity import AttemptManager
from tenacity import BaseRetrying
from tenacity import DoAttempt
from tenacity import DoSleep
from tenacity import RetryCallState
from tenacity import RetryError
from tenacity import after_nothing
from tenacity import before_nothing
from tenacity import _utils

# Import all built-in retry strategies for easier usage.
from .retry import RetryBaseT
from .retry import retry_all  # noqa
from .retry import retry_any  # noqa
from .retry import retry_if_exception  # noqa
from .retry import retry_if_result  # noqa
from ..retry import RetryBaseT as SyncRetryBaseT

if t.TYPE_CHECKING:
    from tenacity.stop import StopBaseT
    from tenacity.wait import WaitBaseT

WrappedFnReturnT = t.TypeVar("WrappedFnReturnT")
WrappedFn = t.TypeVar("WrappedFn", bound=t.Callable[..., t.Awaitable[t.Any]])


def _portable_async_sleep(seconds: float) -> t.Awaitable[None]:
    # If trio is already imported, then importing it is cheap.
    # If trio isn't already imported, then it's definitely not running, so we
    # can skip further checks.
    if "trio" in sys.modules:
        # If trio is available, then sniffio is too
        import trio
        import sniffio

        if sniffio.current_async_library() == "trio":
            return trio.sleep(seconds)
    # Otherwise, assume asyncio
    # Lazy import asyncio as it's expensive (responsible for 25-50% of total import overhead).
    import asyncio

    return asyncio.sleep(seconds)


class AsyncRetrying(BaseRetrying):
    def __init__(
        self,
        sleep: t.Callable[
            [t.Union[int, float]], t.Union[None, t.Awaitable[None]]
        ] = _portable_async_sleep,
        stop: "StopBaseT" = tenacity.stop.stop_never,
        wait: "WaitBaseT" = tenacity.wait.wait_none(),
        retry: "t.Union[SyncRetryBaseT, RetryBaseT]" = tenacity.retry_if_exception_type(),
        before: t.Callable[
            ["RetryCallState"], t.Union[None, t.Awaitable[None]]
        ] = before_nothing,
        after: t.Callable[
            ["RetryCallState"], t.Union[None, t.Awaitable[None]]
        ] = after_nothing,
        before_sleep: t.Optional[
            t.Callable[["RetryCallState"], t.Union[None, t.Awaitable[None]]]
        ] = None,
        reraise: bool = False,
        retry_error_cls: t.Type["RetryError"] = RetryError,
        retry_error_callback: t.Optional[
            t.Callable[["RetryCallState"], t.Union[t.Any, t.Awaitable[t.Any]]]
        ] = None,
    ) -> None:
        super().__init__(
            sleep=sleep,  # type: ignore[arg-type]
            stop=stop,
            wait=wait,
            retry=retry,  # type: ignore[arg-type]
            before=before,  # type: ignore[arg-type]
            after=after,  # type: ignore[arg-type]
            before_sleep=before_sleep,  # type: ignore[arg-type]
            reraise=reraise,
            retry_error_cls=retry_error_cls,
            retry_error_callback=retry_error_callback,
        )

    async def __call__(  # type: ignore[override]
        self, fn: WrappedFn, *args: t.Any, **kwargs: t.Any
    ) -> WrappedFnReturnT:
        self.begin()

        retry_state = RetryCallState(retry_object=self, fn=fn, args=args, kwargs=kwargs)
        while True:
            do = await self.iter(retry_state=retry_state)
            if isinstance(do, DoAttempt):
                try:
                    result = await fn(*args, **kwargs)
                except BaseException:  # noqa: B902
                    retry_state.set_exception(sys.exc_info())  # type: ignore[arg-type]
                else:
                    retry_state.set_result(result)
            elif isinstance(do, DoSleep):
                retry_state.prepare_for_next_attempt()
                await self.sleep(do)  # type: ignore[misc]
            else:
                return do  # type: ignore[no-any-return]

    def _add_action_func(self, fn: t.Callable[..., t.Any]) -> None:
        self.iter_state.actions.append(_utils.wrap_to_async_func(fn))

    async def _run_retry(self, retry_state: "RetryCallState") -> None:  # type: ignore[override]
        self.iter_state.retry_run_result = await _utils.wrap_to_async_func(self.retry)(
            retry_state
        )

    async def _run_wait(self, retry_state: "RetryCallState") -> None:  # type: ignore[override]
        if self.wait:
            sleep = await _utils.wrap_to_async_func(self.wait)(retry_state)
        else:
            sleep = 0.0

        retry_state.upcoming_sleep = sleep

    async def _run_stop(self, retry_state: "RetryCallState") -> None:  # type: ignore[override]
        self.statistics["delay_since_first_attempt"] = retry_state.seconds_since_start
        self.iter_state.stop_run_result = await _utils.wrap_to_async_func(self.stop)(
            retry_state
        )

    async def iter(
        self, retry_state: "RetryCallState"
    ) -> t.Union[DoAttempt, DoSleep, t.Any]:  # noqa: A003
        self._begin_iter(retry_state)
        result = None
        for action in self.iter_state.actions:
            result = await action(retry_state)
        return result

    def __iter__(self) -> t.Generator[AttemptManager, None, None]:
        raise TypeError("AsyncRetrying object is not iterable")

    def __aiter__(self) -> "AsyncRetrying":
        self.begin()
        self._retry_state = RetryCallState(self, fn=None, args=(), kwargs={})
        return self

    async def __anext__(self) -> AttemptManager:
        while True:
            do = await self.iter(retry_state=self._retry_state)
            if do is None:
                raise StopAsyncIteration
            elif isinstance(do, DoAttempt):
                return AttemptManager(retry_state=self._retry_state)
            elif isinstance(do, DoSleep):
                self._retry_state.prepare_for_next_attempt()
                await self.sleep(do)  # type: ignore[misc]
            else:
                raise StopAsyncIteration

    def wraps(self, fn: WrappedFn) -> WrappedFn:
        wrapped = super().wraps(fn)
        # Ensure wrapper is recognized as a coroutine function.

        @functools.wraps(
            fn, functools.WRAPPER_ASSIGNMENTS + ("__defaults__", "__kwdefaults__")
        )
        async def async_wrapped(*args: t.Any, **kwargs: t.Any) -> t.Any:
            # Always create a copy to prevent overwriting the local contexts when
            # calling the same wrapped functions multiple times in the same stack
            copy = self.copy()
            async_wrapped.statistics = copy.statistics  # type: ignore[attr-defined]
            return await copy(fn, *args, **kwargs)

        # Preserve attributes
        async_wrapped.retry = self  # type: ignore[attr-defined]
        async_wrapped.retry_with = wrapped.retry_with  # type: ignore[attr-defined]
        async_wrapped.statistics = {}  # type: ignore[attr-defined]

        return async_wrapped  # type: ignore[return-value]


__all__ = [
    "retry_all",
    "retry_any",
    "retry_if_exception",
    "retry_if_result",
    "WrappedFn",
    "AsyncRetrying",
]

```
tenacity/asyncio/retry.py
```.py
# Copyright 2016–2021 Julien Danjou
# Copyright 2016 Joshua Harlow
# Copyright 2013-2014 Ray Holder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import abc
import typing

from tenacity import _utils
from tenacity import retry_base

if typing.TYPE_CHECKING:
    from tenacity import RetryCallState


class async_retry_base(retry_base):
    """Abstract base class for async retry strategies."""

    @abc.abstractmethod
    async def __call__(self, retry_state: "RetryCallState") -> bool:  # type: ignore[override]
        pass

    def __and__(  # type: ignore[override]
        self, other: "typing.Union[retry_base, async_retry_base]"
    ) -> "retry_all":
        return retry_all(self, other)

    def __rand__(  # type: ignore[misc,override]
        self, other: "typing.Union[retry_base, async_retry_base]"
    ) -> "retry_all":
        return retry_all(other, self)

    def __or__(  # type: ignore[override]
        self, other: "typing.Union[retry_base, async_retry_base]"
    ) -> "retry_any":
        return retry_any(self, other)

    def __ror__(  # type: ignore[misc,override]
        self, other: "typing.Union[retry_base, async_retry_base]"
    ) -> "retry_any":
        return retry_any(other, self)


RetryBaseT = typing.Union[
    async_retry_base, typing.Callable[["RetryCallState"], typing.Awaitable[bool]]
]


class retry_if_exception(async_retry_base):
    """Retry strategy that retries if an exception verifies a predicate."""

    def __init__(
        self, predicate: typing.Callable[[BaseException], typing.Awaitable[bool]]
    ) -> None:
        self.predicate = predicate

    async def __call__(self, retry_state: "RetryCallState") -> bool:  # type: ignore[override]
        if retry_state.outcome is None:
            raise RuntimeError("__call__() called before outcome was set")

        if retry_state.outcome.failed:
            exception = retry_state.outcome.exception()
            if exception is None:
                raise RuntimeError("outcome failed but the exception is None")
            return await self.predicate(exception)
        else:
            return False


class retry_if_result(async_retry_base):
    """Retries if the result verifies a predicate."""

    def __init__(
        self, predicate: typing.Callable[[typing.Any], typing.Awaitable[bool]]
    ) -> None:
        self.predicate = predicate

    async def __call__(self, retry_state: "RetryCallState") -> bool:  # type: ignore[override]
        if retry_state.outcome is None:
            raise RuntimeError("__call__() called before outcome was set")

        if not retry_state.outcome.failed:
            return await self.predicate(retry_state.outcome.result())
        else:
            return False


class retry_any(async_retry_base):
    """Retries if any of the retries condition is valid."""

    def __init__(self, *retries: typing.Union[retry_base, async_retry_base]) -> None:
        self.retries = retries

    async def __call__(self, retry_state: "RetryCallState") -> bool:  # type: ignore[override]
        result = False
        for r in self.retries:
            result = result or await _utils.wrap_to_async_func(r)(retry_state)
            if result:
                break
        return result


class retry_all(async_retry_base):
    """Retries if all the retries condition are valid."""

    def __init__(self, *retries: typing.Union[retry_base, async_retry_base]) -> None:
        self.retries = retries

    async def __call__(self, retry_state: "RetryCallState") -> bool:  # type: ignore[override]
        result = True
        for r in self.retries:
            result = result and await _utils.wrap_to_async_func(r)(retry_state)
            if not result:
                break
        return result

```
tenacity/before.py
```.py
# Copyright 2016 Julien Danjou
# Copyright 2016 Joshua Harlow
# Copyright 2013-2014 Ray Holder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing

from tenacity import _utils

if typing.TYPE_CHECKING:
    import logging

    from tenacity import RetryCallState


def before_nothing(retry_state: "RetryCallState") -> None:
    """Before call strategy that does nothing."""


def before_log(
    logger: "logging.Logger", log_level: int
) -> typing.Callable[["RetryCallState"], None]:
    """Before call strategy that logs to some logger the attempt."""

    def log_it(retry_state: "RetryCallState") -> None:
        if retry_state.fn is None:
            # NOTE(sileht): can't really happen, but we must please mypy
            fn_name = "<unknown>"
        else:
            fn_name = _utils.get_callback_name(retry_state.fn)
        logger.log(
            log_level,
            f"Starting call to '{fn_name}', "
            f"this is the {_utils.to_ordinal(retry_state.attempt_number)} time calling it.",
        )

    return log_it

```
tenacity/before_sleep.py
```.py
# Copyright 2016 Julien Danjou
# Copyright 2016 Joshua Harlow
# Copyright 2013-2014 Ray Holder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing

from tenacity import _utils

if typing.TYPE_CHECKING:
    import logging

    from tenacity import RetryCallState


def before_sleep_nothing(retry_state: "RetryCallState") -> None:
    """Before sleep strategy that does nothing."""


def before_sleep_log(
    logger: "logging.Logger",
    log_level: int,
    exc_info: bool = False,
) -> typing.Callable[["RetryCallState"], None]:
    """Before sleep strategy that logs to some logger the attempt."""

    def log_it(retry_state: "RetryCallState") -> None:
        local_exc_info: BaseException | bool | None

        if retry_state.outcome is None:
            raise RuntimeError("log_it() called before outcome was set")

        if retry_state.next_action is None:
            raise RuntimeError("log_it() called before next_action was set")

        if retry_state.outcome.failed:
            ex = retry_state.outcome.exception()
            verb, value = "raised", f"{ex.__class__.__name__}: {ex}"

            if exc_info:
                local_exc_info = retry_state.outcome.exception()
            else:
                local_exc_info = False
        else:
            verb, value = "returned", retry_state.outcome.result()
            local_exc_info = False  # exc_info does not apply when no exception

        if retry_state.fn is None:
            # NOTE(sileht): can't really happen, but we must please mypy
            fn_name = "<unknown>"
        else:
            fn_name = _utils.get_callback_name(retry_state.fn)

        logger.log(
            log_level,
            f"Retrying {fn_name} "
            f"in {retry_state.next_action.sleep} seconds as it {verb} {value}.",
            exc_info=local_exc_info,
        )

    return log_it

```
tenacity/nap.py
```.py
# Copyright 2016 Étienne Bersac
# Copyright 2016 Julien Danjou
# Copyright 2016 Joshua Harlow
# Copyright 2013-2014 Ray Holder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import typing

if typing.TYPE_CHECKING:
    import threading


def sleep(seconds: float) -> None:
    """
    Sleep strategy that delays execution for a given number of seconds.

    This is the default strategy, and may be mocked out for unit testing.
    """
    time.sleep(seconds)


class sleep_using_event:
    """Sleep strategy that waits on an event to be set."""

    def __init__(self, event: "threading.Event") -> None:
        self.event = event

    def __call__(self, timeout: typing.Optional[float]) -> None:
        # NOTE(harlowja): this may *not* actually wait for timeout
        # seconds if the event is set (ie this may eject out early).
        self.event.wait(timeout=timeout)

```
tenacity/retry.py
```.py
# Copyright 2016–2021 Julien Danjou
# Copyright 2016 Joshua Harlow
# Copyright 2013-2014 Ray Holder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import re
import typing

if typing.TYPE_CHECKING:
    from tenacity import RetryCallState


class retry_base(abc.ABC):
    """Abstract base class for retry strategies."""

    @abc.abstractmethod
    def __call__(self, retry_state: "RetryCallState") -> bool:
        pass

    def __and__(self, other: "retry_base") -> "retry_all":
        return other.__rand__(self)

    def __rand__(self, other: "retry_base") -> "retry_all":
        return retry_all(other, self)

    def __or__(self, other: "retry_base") -> "retry_any":
        return other.__ror__(self)

    def __ror__(self, other: "retry_base") -> "retry_any":
        return retry_any(other, self)


RetryBaseT = typing.Union[retry_base, typing.Callable[["RetryCallState"], bool]]


class _retry_never(retry_base):
    """Retry strategy that never rejects any result."""

    def __call__(self, retry_state: "RetryCallState") -> bool:
        return False


retry_never = _retry_never()


class _retry_always(retry_base):
    """Retry strategy that always rejects any result."""

    def __call__(self, retry_state: "RetryCallState") -> bool:
        return True


retry_always = _retry_always()


class retry_if_exception(retry_base):
    """Retry strategy that retries if an exception verifies a predicate."""

    def __init__(self, predicate: typing.Callable[[BaseException], bool]) -> None:
        self.predicate = predicate

    def __call__(self, retry_state: "RetryCallState") -> bool:
        if retry_state.outcome is None:
            raise RuntimeError("__call__() called before outcome was set")

        if retry_state.outcome.failed:
            exception = retry_state.outcome.exception()
            if exception is None:
                raise RuntimeError("outcome failed but the exception is None")
            return self.predicate(exception)
        else:
            return False


class retry_if_exception_type(retry_if_exception):
    """Retries if an exception has been raised of one or more types."""

    def __init__(
        self,
        exception_types: typing.Union[
            typing.Type[BaseException],
            typing.Tuple[typing.Type[BaseException], ...],
        ] = Exception,
    ) -> None:
        self.exception_types = exception_types
        super().__init__(lambda e: isinstance(e, exception_types))


class retry_if_not_exception_type(retry_if_exception):
    """Retries except an exception has been raised of one or more types."""

    def __init__(
        self,
        exception_types: typing.Union[
            typing.Type[BaseException],
            typing.Tuple[typing.Type[BaseException], ...],
        ] = Exception,
    ) -> None:
        self.exception_types = exception_types
        super().__init__(lambda e: not isinstance(e, exception_types))


class retry_unless_exception_type(retry_if_exception):
    """Retries until an exception is raised of one or more types."""

    def __init__(
        self,
        exception_types: typing.Union[
            typing.Type[BaseException],
            typing.Tuple[typing.Type[BaseException], ...],
        ] = Exception,
    ) -> None:
        self.exception_types = exception_types
        super().__init__(lambda e: not isinstance(e, exception_types))

    def __call__(self, retry_state: "RetryCallState") -> bool:
        if retry_state.outcome is None:
            raise RuntimeError("__call__() called before outcome was set")

        # always retry if no exception was raised
        if not retry_state.outcome.failed:
            return True

        exception = retry_state.outcome.exception()
        if exception is None:
            raise RuntimeError("outcome failed but the exception is None")
        return self.predicate(exception)


class retry_if_exception_cause_type(retry_base):
    """Retries if any of the causes of the raised exception is of one or more types.

    The check on the type of the cause of the exception is done recursively (until finding
    an exception in the chain that has no `__cause__`)
    """

    def __init__(
        self,
        exception_types: typing.Union[
            typing.Type[BaseException],
            typing.Tuple[typing.Type[BaseException], ...],
        ] = Exception,
    ) -> None:
        self.exception_cause_types = exception_types

    def __call__(self, retry_state: "RetryCallState") -> bool:
        if retry_state.outcome is None:
            raise RuntimeError("__call__ called before outcome was set")

        if retry_state.outcome.failed:
            exc = retry_state.outcome.exception()
            while exc is not None:
                if isinstance(exc.__cause__, self.exception_cause_types):
                    return True
                exc = exc.__cause__

        return False


class retry_if_result(retry_base):
    """Retries if the result verifies a predicate."""

    def __init__(self, predicate: typing.Callable[[typing.Any], bool]) -> None:
        self.predicate = predicate

    def __call__(self, retry_state: "RetryCallState") -> bool:
        if retry_state.outcome is None:
            raise RuntimeError("__call__() called before outcome was set")

        if not retry_state.outcome.failed:
            return self.predicate(retry_state.outcome.result())
        else:
            return False


class retry_if_not_result(retry_base):
    """Retries if the result refutes a predicate."""

    def __init__(self, predicate: typing.Callable[[typing.Any], bool]) -> None:
        self.predicate = predicate

    def __call__(self, retry_state: "RetryCallState") -> bool:
        if retry_state.outcome is None:
            raise RuntimeError("__call__() called before outcome was set")

        if not retry_state.outcome.failed:
            return not self.predicate(retry_state.outcome.result())
        else:
            return False


class retry_if_exception_message(retry_if_exception):
    """Retries if an exception message equals or matches."""

    def __init__(
        self,
        message: typing.Optional[str] = None,
        match: typing.Optional[str] = None,
    ) -> None:
        if message and match:
            raise TypeError(
                f"{self.__class__.__name__}() takes either 'message' or 'match', not both"
            )

        # set predicate
        if message:

            def message_fnc(exception: BaseException) -> bool:
                return message == str(exception)

            predicate = message_fnc
        elif match:
            prog = re.compile(match)

            def match_fnc(exception: BaseException) -> bool:
                return bool(prog.match(str(exception)))

            predicate = match_fnc
        else:
            raise TypeError(
                f"{self.__class__.__name__}() missing 1 required argument 'message' or 'match'"
            )

        super().__init__(predicate)


class retry_if_not_exception_message(retry_if_exception_message):
    """Retries until an exception message equals or matches."""

    def __init__(
        self,
        message: typing.Optional[str] = None,
        match: typing.Optional[str] = None,
    ) -> None:
        super().__init__(message, match)
        # invert predicate
        if_predicate = self.predicate
        self.predicate = lambda *args_, **kwargs_: not if_predicate(*args_, **kwargs_)

    def __call__(self, retry_state: "RetryCallState") -> bool:
        if retry_state.outcome is None:
            raise RuntimeError("__call__() called before outcome was set")

        if not retry_state.outcome.failed:
            return True

        exception = retry_state.outcome.exception()
        if exception is None:
            raise RuntimeError("outcome failed but the exception is None")
        return self.predicate(exception)


class retry_any(retry_base):
    """Retries if any of the retries condition is valid."""

    def __init__(self, *retries: retry_base) -> None:
        self.retries = retries

    def __call__(self, retry_state: "RetryCallState") -> bool:
        return any(r(retry_state) for r in self.retries)


class retry_all(retry_base):
    """Retries if all the retries condition are valid."""

    def __init__(self, *retries: retry_base) -> None:
        self.retries = retries

    def __call__(self, retry_state: "RetryCallState") -> bool:
        return all(r(retry_state) for r in self.retries)

```
tenacity/stop.py
```.py
# Copyright 2016–2021 Julien Danjou
# Copyright 2016 Joshua Harlow
# Copyright 2013-2014 Ray Holder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import abc
import typing

from tenacity import _utils

if typing.TYPE_CHECKING:
    import threading

    from tenacity import RetryCallState


class stop_base(abc.ABC):
    """Abstract base class for stop strategies."""

    @abc.abstractmethod
    def __call__(self, retry_state: "RetryCallState") -> bool:
        pass

    def __and__(self, other: "stop_base") -> "stop_all":
        return stop_all(self, other)

    def __or__(self, other: "stop_base") -> "stop_any":
        return stop_any(self, other)


StopBaseT = typing.Union[stop_base, typing.Callable[["RetryCallState"], bool]]


class stop_any(stop_base):
    """Stop if any of the stop condition is valid."""

    def __init__(self, *stops: stop_base) -> None:
        self.stops = stops

    def __call__(self, retry_state: "RetryCallState") -> bool:
        return any(x(retry_state) for x in self.stops)


class stop_all(stop_base):
    """Stop if all the stop conditions are valid."""

    def __init__(self, *stops: stop_base) -> None:
        self.stops = stops

    def __call__(self, retry_state: "RetryCallState") -> bool:
        return all(x(retry_state) for x in self.stops)


class _stop_never(stop_base):
    """Never stop."""

    def __call__(self, retry_state: "RetryCallState") -> bool:
        return False


stop_never = _stop_never()


class stop_when_event_set(stop_base):
    """Stop when the given event is set."""

    def __init__(self, event: "threading.Event") -> None:
        self.event = event

    def __call__(self, retry_state: "RetryCallState") -> bool:
        return self.event.is_set()


class stop_after_attempt(stop_base):
    """Stop when the previous attempt >= max_attempt."""

    def __init__(self, max_attempt_number: int) -> None:
        self.max_attempt_number = max_attempt_number

    def __call__(self, retry_state: "RetryCallState") -> bool:
        return retry_state.attempt_number >= self.max_attempt_number


class stop_after_delay(stop_base):
    """
    Stop when the time from the first attempt >= limit.

    Note: `max_delay` will be exceeded, so when used with a `wait`, the actual total delay will be greater
    than `max_delay` by some of the final sleep period before `max_delay` is exceeded.

    If you need stricter timing with waits, consider `stop_before_delay` instead.
    """

    def __init__(self, max_delay: _utils.time_unit_type) -> None:
        self.max_delay = _utils.to_seconds(max_delay)

    def __call__(self, retry_state: "RetryCallState") -> bool:
        if retry_state.seconds_since_start is None:
            raise RuntimeError("__call__() called but seconds_since_start is not set")
        return retry_state.seconds_since_start >= self.max_delay


class stop_before_delay(stop_base):
    """
    Stop right before the next attempt would take place after the time from the first attempt >= limit.

    Most useful when you are using with a `wait` function like wait_random_exponential, but need to make
    sure that the max_delay is not exceeded.
    """

    def __init__(self, max_delay: _utils.time_unit_type) -> None:
        self.max_delay = _utils.to_seconds(max_delay)

    def __call__(self, retry_state: "RetryCallState") -> bool:
        if retry_state.seconds_since_start is None:
            raise RuntimeError("__call__() called but seconds_since_start is not set")
        return (
            retry_state.seconds_since_start + retry_state.upcoming_sleep
            >= self.max_delay
        )

```
tenacity/tornadoweb.py
```.py
# Copyright 2017 Elisey Zanko
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import typing

from tenacity import BaseRetrying
from tenacity import DoAttempt
from tenacity import DoSleep
from tenacity import RetryCallState

from tornado import gen

if typing.TYPE_CHECKING:
    from tornado.concurrent import Future

_RetValT = typing.TypeVar("_RetValT")


class TornadoRetrying(BaseRetrying):
    def __init__(
        self,
        sleep: "typing.Callable[[float], Future[None]]" = gen.sleep,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(**kwargs)
        self.sleep = sleep

    @gen.coroutine  # type: ignore[misc]
    def __call__(
        self,
        fn: "typing.Callable[..., typing.Union[typing.Generator[typing.Any, typing.Any, _RetValT], Future[_RetValT]]]",
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> "typing.Generator[typing.Any, typing.Any, _RetValT]":
        self.begin()

        retry_state = RetryCallState(retry_object=self, fn=fn, args=args, kwargs=kwargs)
        while True:
            do = self.iter(retry_state=retry_state)
            if isinstance(do, DoAttempt):
                try:
                    result = yield fn(*args, **kwargs)
                except BaseException:  # noqa: B902
                    retry_state.set_exception(sys.exc_info())  # type: ignore[arg-type]
                else:
                    retry_state.set_result(result)
            elif isinstance(do, DoSleep):
                retry_state.prepare_for_next_attempt()
                yield self.sleep(do)
            else:
                raise gen.Return(do)

```
tenacity/wait.py
```.py
# Copyright 2016–2021 Julien Danjou
# Copyright 2016 Joshua Harlow
# Copyright 2013-2014 Ray Holder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import random
import typing

from tenacity import _utils

if typing.TYPE_CHECKING:
    from tenacity import RetryCallState


class wait_base(abc.ABC):
    """Abstract base class for wait strategies."""

    @abc.abstractmethod
    def __call__(self, retry_state: "RetryCallState") -> float:
        pass

    def __add__(self, other: "wait_base") -> "wait_combine":
        return wait_combine(self, other)

    def __radd__(self, other: "wait_base") -> typing.Union["wait_combine", "wait_base"]:
        # make it possible to use multiple waits with the built-in sum function
        if other == 0:  # type: ignore[comparison-overlap]
            return self
        return self.__add__(other)


WaitBaseT = typing.Union[
    wait_base, typing.Callable[["RetryCallState"], typing.Union[float, int]]
]


class wait_fixed(wait_base):
    """Wait strategy that waits a fixed amount of time between each retry."""

    def __init__(self, wait: _utils.time_unit_type) -> None:
        self.wait_fixed = _utils.to_seconds(wait)

    def __call__(self, retry_state: "RetryCallState") -> float:
        return self.wait_fixed


class wait_none(wait_fixed):
    """Wait strategy that doesn't wait at all before retrying."""

    def __init__(self) -> None:
        super().__init__(0)


class wait_random(wait_base):
    """Wait strategy that waits a random amount of time between min/max."""

    def __init__(
        self, min: _utils.time_unit_type = 0, max: _utils.time_unit_type = 1
    ) -> None:  # noqa
        self.wait_random_min = _utils.to_seconds(min)
        self.wait_random_max = _utils.to_seconds(max)

    def __call__(self, retry_state: "RetryCallState") -> float:
        return self.wait_random_min + (
            random.random() * (self.wait_random_max - self.wait_random_min)
        )


class wait_combine(wait_base):
    """Combine several waiting strategies."""

    def __init__(self, *strategies: wait_base) -> None:
        self.wait_funcs = strategies

    def __call__(self, retry_state: "RetryCallState") -> float:
        return sum(x(retry_state=retry_state) for x in self.wait_funcs)


class wait_chain(wait_base):
    """Chain two or more waiting strategies.

    If all strategies are exhausted, the very last strategy is used
    thereafter.

    For example::

        @retry(wait=wait_chain(*[wait_fixed(1) for i in range(3)] +
                               [wait_fixed(2) for j in range(5)] +
                               [wait_fixed(5) for k in range(4)))
        def wait_chained():
            print("Wait 1s for 3 attempts, 2s for 5 attempts and 5s
                   thereafter.")
    """

    def __init__(self, *strategies: wait_base) -> None:
        self.strategies = strategies

    def __call__(self, retry_state: "RetryCallState") -> float:
        wait_func_no = min(max(retry_state.attempt_number, 1), len(self.strategies))
        wait_func = self.strategies[wait_func_no - 1]
        return wait_func(retry_state=retry_state)


class wait_incrementing(wait_base):
    """Wait an incremental amount of time after each attempt.

    Starting at a starting value and incrementing by a value for each attempt
    (and restricting the upper limit to some maximum value).
    """

    def __init__(
        self,
        start: _utils.time_unit_type = 0,
        increment: _utils.time_unit_type = 100,
        max: _utils.time_unit_type = _utils.MAX_WAIT,  # noqa
    ) -> None:
        self.start = _utils.to_seconds(start)
        self.increment = _utils.to_seconds(increment)
        self.max = _utils.to_seconds(max)

    def __call__(self, retry_state: "RetryCallState") -> float:
        result = self.start + (self.increment * (retry_state.attempt_number - 1))
        return max(0, min(result, self.max))


class wait_exponential(wait_base):
    """Wait strategy that applies exponential backoff.

    It allows for a customized multiplier and an ability to restrict the
    upper and lower limits to some maximum and minimum value.

    The intervals are fixed (i.e. there is no jitter), so this strategy is
    suitable for balancing retries against latency when a required resource is
    unavailable for an unknown duration, but *not* suitable for resolving
    contention between multiple processes for a shared resource. Use
    wait_random_exponential for the latter case.
    """

    def __init__(
        self,
        multiplier: typing.Union[int, float] = 1,
        max: _utils.time_unit_type = _utils.MAX_WAIT,  # noqa
        exp_base: typing.Union[int, float] = 2,
        min: _utils.time_unit_type = 0,  # noqa
    ) -> None:
        self.multiplier = multiplier
        self.min = _utils.to_seconds(min)
        self.max = _utils.to_seconds(max)
        self.exp_base = exp_base

    def __call__(self, retry_state: "RetryCallState") -> float:
        try:
            exp = self.exp_base ** (retry_state.attempt_number - 1)
            result = self.multiplier * exp
        except OverflowError:
            return self.max
        return max(max(0, self.min), min(result, self.max))


class wait_random_exponential(wait_exponential):
    """Random wait with exponentially widening window.

    An exponential backoff strategy used to mediate contention between multiple
    uncoordinated processes for a shared resource in distributed systems. This
    is the sense in which "exponential backoff" is meant in e.g. Ethernet
    networking, and corresponds to the "Full Jitter" algorithm described in
    this blog post:

    https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/

    Each retry occurs at a random time in a geometrically expanding interval.
    It allows for a custom multiplier and an ability to restrict the upper
    limit of the random interval to some maximum value.

    Example::

        wait_random_exponential(multiplier=0.5,  # initial window 0.5s
                                max=60)          # max 60s timeout

    When waiting for an unavailable resource to become available again, as
    opposed to trying to resolve contention for a shared resource, the
    wait_exponential strategy (which uses a fixed interval) may be preferable.

    """

    def __call__(self, retry_state: "RetryCallState") -> float:
        high = super().__call__(retry_state=retry_state)
        return random.uniform(self.min, high)


class wait_exponential_jitter(wait_base):
    """Wait strategy that applies exponential backoff and jitter.

    It allows for a customized initial wait, maximum wait and jitter.

    This implements the strategy described here:
    https://cloud.google.com/storage/docs/retry-strategy

    The wait time is min(initial * 2**n + random.uniform(0, jitter), maximum)
    where n is the retry count.
    """

    def __init__(
        self,
        initial: float = 1,
        max: float = _utils.MAX_WAIT,  # noqa
        exp_base: float = 2,
        jitter: float = 1,
    ) -> None:
        self.initial = initial
        self.max = max
        self.exp_base = exp_base
        self.jitter = jitter

    def __call__(self, retry_state: "RetryCallState") -> float:
        jitter = random.uniform(0, self.jitter)
        try:
            exp = self.exp_base ** (retry_state.attempt_number - 1)
            result = self.initial * exp + jitter
        except OverflowError:
            result = self.max
        return max(0, min(result, self.max))

```
tests/__init__.py
```.py

```
tests/test_after.py
```.py
# mypy: disable-error-code="no-untyped-def,no-untyped-call"
import logging
import random
import unittest.mock

from tenacity import _utils  # noqa
from tenacity import after_log

from . import test_tenacity


class TestAfterLogFormat(unittest.TestCase):
    def setUp(self) -> None:
        self.log_level = random.choice(
            (
                logging.DEBUG,
                logging.INFO,
                logging.WARNING,
                logging.ERROR,
                logging.CRITICAL,
            )
        )
        self.previous_attempt_number = random.randint(1, 512)

    def test_01_default(self):
        """Test log formatting."""
        log = unittest.mock.MagicMock(spec="logging.Logger.log")
        logger = unittest.mock.MagicMock(spec="logging.Logger", log=log)

        sec_format = "%0.3f"
        delay_since_first_attempt = 0.1

        retry_state = test_tenacity.make_retry_state(
            self.previous_attempt_number, delay_since_first_attempt
        )
        fun = after_log(
            logger=logger, log_level=self.log_level
        )  # use default sec_format
        fun(retry_state)
        fn_name = (
            "<unknown>"
            if retry_state.fn is None
            else _utils.get_callback_name(retry_state.fn)
        )
        log.assert_called_once_with(
            self.log_level,
            f"Finished call to '{fn_name}' "
            f"after {sec_format % retry_state.seconds_since_start}(s), "
            f"this was the {_utils.to_ordinal(retry_state.attempt_number)} time calling it.",
        )

    def test_02_custom_sec_format(self):
        """Test log formatting with custom int format.."""
        log = unittest.mock.MagicMock(spec="logging.Logger.log")
        logger = unittest.mock.MagicMock(spec="logging.Logger", log=log)

        sec_format = "%.1f"
        delay_since_first_attempt = 0.1

        retry_state = test_tenacity.make_retry_state(
            self.previous_attempt_number, delay_since_first_attempt
        )
        fun = after_log(logger=logger, log_level=self.log_level, sec_format=sec_format)
        fun(retry_state)
        fn_name = (
            "<unknown>"
            if retry_state.fn is None
            else _utils.get_callback_name(retry_state.fn)
        )
        log.assert_called_once_with(
            self.log_level,
            f"Finished call to '{fn_name}' "
            f"after {sec_format % retry_state.seconds_since_start}(s), "
            f"this was the {_utils.to_ordinal(retry_state.attempt_number)} time calling it.",
        )

```
tests/test_asyncio.py
```.py
# mypy: disable-error-code="no-untyped-def,no-untyped-call"
# Copyright 2016 Étienne Bersac
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import inspect
import unittest
from functools import wraps
from unittest import mock

try:
    import trio
except ImportError:
    have_trio = False
else:
    have_trio = True

import pytest

import tenacity
from tenacity import AsyncRetrying, RetryError
from tenacity import asyncio as tasyncio
from tenacity import retry, retry_if_exception, retry_if_result, stop_after_attempt
from tenacity.wait import wait_fixed

from .test_tenacity import NoIOErrorAfterCount, current_time_ms


def asynctest(callable_):
    @wraps(callable_)
    def wrapper(*a, **kw):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(callable_(*a, **kw))

    return wrapper


async def _async_function(thing):
    await asyncio.sleep(0.00001)
    return thing.go()


@retry
async def _retryable_coroutine(thing):
    await asyncio.sleep(0.00001)
    return thing.go()


@retry(stop=stop_after_attempt(2))
async def _retryable_coroutine_with_2_attempts(thing):
    await asyncio.sleep(0.00001)
    return thing.go()


class TestAsyncio(unittest.TestCase):
    @asynctest
    async def test_retry(self):
        thing = NoIOErrorAfterCount(5)
        await _retryable_coroutine(thing)
        assert thing.counter == thing.count

    @asynctest
    async def test_iscoroutinefunction(self):
        assert asyncio.iscoroutinefunction(_retryable_coroutine)
        assert inspect.iscoroutinefunction(_retryable_coroutine)

    @asynctest
    async def test_retry_using_async_retying(self):
        thing = NoIOErrorAfterCount(5)
        retrying = AsyncRetrying()
        await retrying(_async_function, thing)
        assert thing.counter == thing.count

    @asynctest
    async def test_stop_after_attempt(self):
        thing = NoIOErrorAfterCount(2)
        try:
            await _retryable_coroutine_with_2_attempts(thing)
        except RetryError:
            assert thing.counter == 2

    def test_repr(self):
        repr(tasyncio.AsyncRetrying())

    def test_retry_attributes(self):
        assert hasattr(_retryable_coroutine, "retry")
        assert hasattr(_retryable_coroutine, "retry_with")

    def test_retry_preserves_argument_defaults(self):
        async def function_with_defaults(a=1):
            return a

        async def function_with_kwdefaults(*, a=1):
            return a

        retrying = AsyncRetrying(
            wait=tenacity.wait_fixed(0.01), stop=tenacity.stop_after_attempt(3)
        )
        wrapped_defaults_function = retrying.wraps(function_with_defaults)
        wrapped_kwdefaults_function = retrying.wraps(function_with_kwdefaults)

        self.assertEqual(
            function_with_defaults.__defaults__, wrapped_defaults_function.__defaults__
        )
        self.assertEqual(
            function_with_kwdefaults.__kwdefaults__,
            wrapped_kwdefaults_function.__kwdefaults__,
        )

    @asynctest
    async def test_attempt_number_is_correct_for_interleaved_coroutines(self):
        attempts = []

        def after(retry_state):
            attempts.append((retry_state.args[0], retry_state.attempt_number))

        thing1 = NoIOErrorAfterCount(3)
        thing2 = NoIOErrorAfterCount(3)

        await asyncio.gather(
            _retryable_coroutine.retry_with(after=after)(thing1),  # type: ignore[attr-defined]
            _retryable_coroutine.retry_with(after=after)(thing2),  # type: ignore[attr-defined]
        )

        # There's no waiting on retry, only a wait in the coroutine, so the
        # executions should be interleaved.
        even_thing_attempts = attempts[::2]
        things, attempt_nos1 = zip(*even_thing_attempts)
        assert len(set(things)) == 1
        assert list(attempt_nos1) == [1, 2, 3]

        odd_thing_attempts = attempts[1::2]
        things, attempt_nos2 = zip(*odd_thing_attempts)
        assert len(set(things)) == 1
        assert list(attempt_nos2) == [1, 2, 3]


@unittest.skipIf(not have_trio, "trio not installed")
class TestTrio(unittest.TestCase):
    def test_trio_basic(self):
        thing = NoIOErrorAfterCount(5)

        @retry
        async def trio_function():
            await trio.sleep(0.00001)
            return thing.go()

        trio.run(trio_function)

        assert thing.counter == thing.count


class TestContextManager(unittest.TestCase):
    @asynctest
    async def test_do_max_attempts(self):
        attempts = 0
        retrying = tasyncio.AsyncRetrying(stop=stop_after_attempt(3))
        try:
            async for attempt in retrying:
                with attempt:
                    attempts += 1
                    raise Exception
        except RetryError:
            pass

        assert attempts == 3

    @asynctest
    async def test_reraise(self):
        class CustomError(Exception):
            pass

        try:
            async for attempt in tasyncio.AsyncRetrying(
                stop=stop_after_attempt(1), reraise=True
            ):
                with attempt:
                    raise CustomError()
        except CustomError:
            pass
        else:
            raise Exception

    @asynctest
    async def test_sleeps(self):
        start = current_time_ms()
        try:
            async for attempt in tasyncio.AsyncRetrying(
                stop=stop_after_attempt(1), wait=wait_fixed(1)
            ):
                with attempt:
                    raise Exception()
        except RetryError:
            pass
        t = current_time_ms() - start
        self.assertLess(t, 1.1)

    @asynctest
    async def test_retry_with_result(self):
        async def test():
            attempts = 0

            # mypy doesn't have great lambda support
            def lt_3(x: float) -> bool:
                return x < 3

            async for attempt in tasyncio.AsyncRetrying(retry=retry_if_result(lt_3)):
                with attempt:
                    attempts += 1
                attempt.retry_state.set_result(attempts)
            return attempts

        result = await test()

        self.assertEqual(3, result)

    @asynctest
    async def test_retry_with_async_result(self):
        async def test():
            attempts = 0

            async def lt_3(x: float) -> bool:
                return x < 3

            async for attempt in tasyncio.AsyncRetrying(
                retry=tasyncio.retry_if_result(lt_3)
            ):
                with attempt:
                    attempts += 1

                assert attempt.retry_state.outcome  # help mypy
                if not attempt.retry_state.outcome.failed:
                    attempt.retry_state.set_result(attempts)

            return attempts

        result = await test()

        self.assertEqual(3, result)

    @asynctest
    async def test_retry_with_async_exc(self):
        async def test():
            attempts = 0

            class CustomException(Exception):
                pass

            async def is_exc(e: BaseException) -> bool:
                return isinstance(e, CustomException)

            async for attempt in tasyncio.AsyncRetrying(
                retry=tasyncio.retry_if_exception(is_exc)
            ):
                with attempt:
                    attempts += 1
                    if attempts < 3:
                        raise CustomException()

                assert attempt.retry_state.outcome  # help mypy
                if not attempt.retry_state.outcome.failed:
                    attempt.retry_state.set_result(attempts)

            return attempts

        result = await test()

        self.assertEqual(3, result)

    @asynctest
    async def test_retry_with_async_result_or(self):
        async def test():
            attempts = 0

            async def lt_3(x: float) -> bool:
                return x < 3

            class CustomException(Exception):
                pass

            def is_exc(e: BaseException) -> bool:
                return isinstance(e, CustomException)

            retry_strategy = tasyncio.retry_if_result(lt_3) | retry_if_exception(is_exc)
            async for attempt in tasyncio.AsyncRetrying(retry=retry_strategy):
                with attempt:
                    attempts += 1
                    if 2 < attempts < 4:
                        raise CustomException()

                assert attempt.retry_state.outcome  # help mypy
                if not attempt.retry_state.outcome.failed:
                    attempt.retry_state.set_result(attempts)

            return attempts

        result = await test()

        self.assertEqual(4, result)

    @asynctest
    async def test_retry_with_async_result_ror(self):
        async def test():
            attempts = 0

            def lt_3(x: float) -> bool:
                return x < 3

            class CustomException(Exception):
                pass

            async def is_exc(e: BaseException) -> bool:
                return isinstance(e, CustomException)

            retry_strategy = retry_if_result(lt_3) | tasyncio.retry_if_exception(is_exc)
            async for attempt in tasyncio.AsyncRetrying(retry=retry_strategy):
                with attempt:
                    attempts += 1
                    if 2 < attempts < 4:
                        raise CustomException()

                assert attempt.retry_state.outcome  # help mypy
                if not attempt.retry_state.outcome.failed:
                    attempt.retry_state.set_result(attempts)

            return attempts

        result = await test()

        self.assertEqual(4, result)

    @asynctest
    async def test_retry_with_async_result_and(self):
        async def test():
            attempts = 0

            async def lt_3(x: float) -> bool:
                return x < 3

            def gt_0(x: float) -> bool:
                return x > 0

            retry_strategy = tasyncio.retry_if_result(lt_3) & retry_if_result(gt_0)
            async for attempt in tasyncio.AsyncRetrying(retry=retry_strategy):
                with attempt:
                    attempts += 1
                attempt.retry_state.set_result(attempts)

            return attempts

        result = await test()

        self.assertEqual(3, result)

    @asynctest
    async def test_retry_with_async_result_rand(self):
        async def test():
            attempts = 0

            async def lt_3(x: float) -> bool:
                return x < 3

            def gt_0(x: float) -> bool:
                return x > 0

            retry_strategy = retry_if_result(gt_0) & tasyncio.retry_if_result(lt_3)
            async for attempt in tasyncio.AsyncRetrying(retry=retry_strategy):
                with attempt:
                    attempts += 1
                attempt.retry_state.set_result(attempts)

            return attempts

        result = await test()

        self.assertEqual(3, result)

    @asynctest
    async def test_async_retying_iterator(self):
        thing = NoIOErrorAfterCount(5)
        with pytest.raises(TypeError):
            for attempts in AsyncRetrying():
                with attempts:
                    await _async_function(thing)


class TestDecoratorWrapper(unittest.TestCase):
    @asynctest
    async def test_retry_function_attributes(self):
        """Test that the wrapped function attributes are exposed as intended.

        - statistics contains the value for the latest function run
        - retry object can be modified to change its behaviour (useful to patch in tests)
        - retry object statistics do not contain valid information
        """

        self.assertTrue(
            await _retryable_coroutine_with_2_attempts(NoIOErrorAfterCount(1))
        )

        expected_stats = {
            "attempt_number": 2,
            "delay_since_first_attempt": mock.ANY,
            "idle_for": mock.ANY,
            "start_time": mock.ANY,
        }
        self.assertEqual(
            _retryable_coroutine_with_2_attempts.statistics,  # type: ignore[attr-defined]
            expected_stats,
        )
        self.assertEqual(
            _retryable_coroutine_with_2_attempts.retry.statistics,  # type: ignore[attr-defined]
            {},
        )

        with mock.patch.object(
            _retryable_coroutine_with_2_attempts.retry,  # type: ignore[attr-defined]
            "stop",
            tenacity.stop_after_attempt(1),
        ):
            try:
                self.assertTrue(
                    await _retryable_coroutine_with_2_attempts(NoIOErrorAfterCount(2))
                )
            except RetryError as exc:
                expected_stats = {
                    "attempt_number": 1,
                    "delay_since_first_attempt": mock.ANY,
                    "idle_for": mock.ANY,
                    "start_time": mock.ANY,
                }
                self.assertEqual(
                    _retryable_coroutine_with_2_attempts.statistics,  # type: ignore[attr-defined]
                    expected_stats,
                )
                self.assertEqual(exc.last_attempt.attempt_number, 1)
                self.assertEqual(
                    _retryable_coroutine_with_2_attempts.retry.statistics,  # type: ignore[attr-defined]
                    {},
                )
            else:
                self.fail("RetryError should have been raised after 1 attempt")


# make sure mypy accepts passing an async sleep function
# https://github.com/jd/tenacity/issues/399
async def my_async_sleep(x: float) -> None:
    await asyncio.sleep(x)


@retry(sleep=my_async_sleep)
async def foo():
    pass


if __name__ == "__main__":
    unittest.main()

```
tests/test_issue_478.py
```.py
import asyncio
import typing
import unittest

from functools import wraps

from tenacity import RetryCallState, retry


def asynctest(
    callable_: typing.Callable[..., typing.Any],
) -> typing.Callable[..., typing.Any]:
    @wraps(callable_)
    def wrapper(*a: typing.Any, **kw: typing.Any) -> typing.Any:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(callable_(*a, **kw))

    return wrapper


MAX_RETRY_FIX_ATTEMPTS = 2


class TestIssue478(unittest.TestCase):
    def test_issue(self) -> None:
        results = []

        def do_retry(retry_state: RetryCallState) -> bool:
            outcome = retry_state.outcome
            assert outcome
            ex = outcome.exception()
            _subject_: str = retry_state.args[0]

            if _subject_ == "Fix":  # no retry on fix failure
                return False

            if retry_state.attempt_number >= MAX_RETRY_FIX_ATTEMPTS:
                return False

            if ex:
                do_fix_work()
                return True

            return False

        @retry(reraise=True, retry=do_retry)
        def _do_work(subject: str) -> None:
            if subject == "Error":
                results.append(f"{subject} is not working")
                raise Exception(f"{subject} is not working")
            results.append(f"{subject} is working")

        def do_any_work(subject: str) -> None:
            _do_work(subject)

        def do_fix_work() -> None:
            _do_work("Fix")

        try:
            do_any_work("Error")
        except Exception as exc:
            assert str(exc) == "Error is not working"
        else:
            assert False, "No exception caught"

        assert results == [
            "Error is not working",
            "Fix is working",
            "Error is not working",
        ]

    @asynctest
    async def test_async(self) -> None:
        results = []

        async def do_retry(retry_state: RetryCallState) -> bool:
            outcome = retry_state.outcome
            assert outcome
            ex = outcome.exception()
            _subject_: str = retry_state.args[0]

            if _subject_ == "Fix":  # no retry on fix failure
                return False

            if retry_state.attempt_number >= MAX_RETRY_FIX_ATTEMPTS:
                return False

            if ex:
                await do_fix_work()
                return True

            return False

        @retry(reraise=True, retry=do_retry)
        async def _do_work(subject: str) -> None:
            if subject == "Error":
                results.append(f"{subject} is not working")
                raise Exception(f"{subject} is not working")
            results.append(f"{subject} is working")

        async def do_any_work(subject: str) -> None:
            await _do_work(subject)

        async def do_fix_work() -> None:
            await _do_work("Fix")

        try:
            await do_any_work("Error")
        except Exception as exc:
            assert str(exc) == "Error is not working"
        else:
            assert False, "No exception caught"

        assert results == [
            "Error is not working",
            "Fix is working",
            "Error is not working",
        ]

```
tests/test_tenacity.py
```.py
# mypy: disable_error_code="no-untyped-def,no-untyped-call,attr-defined,arg-type,no-any-return,list-item,var-annotated,import,call-overload"
# Copyright 2016–2021 Julien Danjou
# Copyright 2016 Joshua Harlow
# Copyright 2013 Ray Holder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import datetime
import logging
import re
import sys
import time
import typing
import unittest
import warnings
from contextlib import contextmanager
from copy import copy
from fractions import Fraction
from unittest import mock

import pytest

import tenacity
from tenacity import RetryCallState, RetryError, Retrying, retry

_unset = object()


def _make_unset_exception(func_name, **kwargs):
    missing = []
    for k, v in kwargs.items():
        if v is _unset:
            missing.append(k)
    missing_str = ", ".join(repr(s) for s in missing)
    return TypeError(func_name + " func missing parameters: " + missing_str)


def _set_delay_since_start(retry_state, delay):
    # Ensure outcome_timestamp - start_time is *exactly* equal to the delay to
    # avoid complexity in test code.
    retry_state.start_time = Fraction(retry_state.start_time)
    retry_state.outcome_timestamp = retry_state.start_time + Fraction(delay)
    assert retry_state.seconds_since_start == delay


def make_retry_state(
    previous_attempt_number,
    delay_since_first_attempt,
    last_result=None,
    upcoming_sleep=0,
):
    """Construct RetryCallState for given attempt number & delay.

    Only used in testing and thus is extra careful about timestamp arithmetics.
    """
    required_parameter_unset = (
        previous_attempt_number is _unset or delay_since_first_attempt is _unset
    )
    if required_parameter_unset:
        raise _make_unset_exception(
            "wait/stop",
            previous_attempt_number=previous_attempt_number,
            delay_since_first_attempt=delay_since_first_attempt,
        )

    retry_state = RetryCallState(None, None, (), {})
    retry_state.attempt_number = previous_attempt_number
    if last_result is not None:
        retry_state.outcome = last_result
    else:
        retry_state.set_result(None)

    retry_state.upcoming_sleep = upcoming_sleep

    _set_delay_since_start(retry_state, delay_since_first_attempt)
    return retry_state


class TestBase(unittest.TestCase):
    def test_retrying_repr(self):
        class ConcreteRetrying(tenacity.BaseRetrying):
            def __call__(self, fn, *args, **kwargs):
                pass

        repr(ConcreteRetrying())

    def test_callstate_repr(self):
        rs = RetryCallState(None, None, (), {})
        rs.idle_for = 1.1111111
        assert repr(rs).endswith("attempt #1; slept for 1.11; last result: none yet>")
        rs = make_retry_state(2, 5)
        assert repr(rs).endswith(
            "attempt #2; slept for 0.0; last result: returned None>"
        )
        rs = make_retry_state(
            0, 0, last_result=tenacity.Future.construct(1, ValueError("aaa"), True)
        )
        assert repr(rs).endswith(
            "attempt #0; slept for 0.0; last result: failed (ValueError aaa)>"
        )


class TestStopConditions(unittest.TestCase):
    def test_never_stop(self):
        r = Retrying()
        self.assertFalse(r.stop(make_retry_state(3, 6546)))

    def test_stop_any(self):
        stop = tenacity.stop_any(
            tenacity.stop_after_delay(1), tenacity.stop_after_attempt(4)
        )

        def s(*args):
            return stop(make_retry_state(*args))

        self.assertFalse(s(1, 0.1))
        self.assertFalse(s(2, 0.2))
        self.assertFalse(s(2, 0.8))
        self.assertTrue(s(4, 0.8))
        self.assertTrue(s(3, 1.8))
        self.assertTrue(s(4, 1.8))

    def test_stop_all(self):
        stop = tenacity.stop_all(
            tenacity.stop_after_delay(1), tenacity.stop_after_attempt(4)
        )

        def s(*args):
            return stop(make_retry_state(*args))

        self.assertFalse(s(1, 0.1))
        self.assertFalse(s(2, 0.2))
        self.assertFalse(s(2, 0.8))
        self.assertFalse(s(4, 0.8))
        self.assertFalse(s(3, 1.8))
        self.assertTrue(s(4, 1.8))

    def test_stop_or(self):
        stop = tenacity.stop_after_delay(1) | tenacity.stop_after_attempt(4)

        def s(*args):
            return stop(make_retry_state(*args))

        self.assertFalse(s(1, 0.1))
        self.assertFalse(s(2, 0.2))
        self.assertFalse(s(2, 0.8))
        self.assertTrue(s(4, 0.8))
        self.assertTrue(s(3, 1.8))
        self.assertTrue(s(4, 1.8))

    def test_stop_and(self):
        stop = tenacity.stop_after_delay(1) & tenacity.stop_after_attempt(4)

        def s(*args):
            return stop(make_retry_state(*args))

        self.assertFalse(s(1, 0.1))
        self.assertFalse(s(2, 0.2))
        self.assertFalse(s(2, 0.8))
        self.assertFalse(s(4, 0.8))
        self.assertFalse(s(3, 1.8))
        self.assertTrue(s(4, 1.8))

    def test_stop_after_attempt(self):
        r = Retrying(stop=tenacity.stop_after_attempt(3))
        self.assertFalse(r.stop(make_retry_state(2, 6546)))
        self.assertTrue(r.stop(make_retry_state(3, 6546)))
        self.assertTrue(r.stop(make_retry_state(4, 6546)))

    def test_stop_after_delay(self):
        for delay in (1, datetime.timedelta(seconds=1)):
            with self.subTest():
                r = Retrying(stop=tenacity.stop_after_delay(delay))
                self.assertFalse(r.stop(make_retry_state(2, 0.999)))
                self.assertTrue(r.stop(make_retry_state(2, 1)))
                self.assertTrue(r.stop(make_retry_state(2, 1.001)))

    def test_stop_before_delay(self):
        for delay in (1, datetime.timedelta(seconds=1)):
            with self.subTest():
                r = Retrying(stop=tenacity.stop_before_delay(delay))
                self.assertFalse(
                    r.stop(make_retry_state(2, 0.999, upcoming_sleep=0.0001))
                )
                self.assertTrue(r.stop(make_retry_state(2, 1, upcoming_sleep=0.001)))
                self.assertTrue(r.stop(make_retry_state(2, 1, upcoming_sleep=1)))

                # It should act the same as stop_after_delay if upcoming sleep is 0
                self.assertFalse(r.stop(make_retry_state(2, 0.999, upcoming_sleep=0)))
                self.assertTrue(r.stop(make_retry_state(2, 1, upcoming_sleep=0)))
                self.assertTrue(r.stop(make_retry_state(2, 1.001, upcoming_sleep=0)))

    def test_legacy_explicit_stop_type(self):
        Retrying(stop="stop_after_attempt")

    def test_stop_func_with_retry_state(self):
        def stop_func(retry_state):
            rs = retry_state
            return rs.attempt_number == rs.seconds_since_start

        r = Retrying(stop=stop_func)
        self.assertFalse(r.stop(make_retry_state(1, 3)))
        self.assertFalse(r.stop(make_retry_state(100, 99)))
        self.assertTrue(r.stop(make_retry_state(101, 101)))


class TestWaitConditions(unittest.TestCase):
    def test_no_sleep(self):
        r = Retrying()
        self.assertEqual(0, r.wait(make_retry_state(18, 9879)))

    def test_fixed_sleep(self):
        for wait in (1, datetime.timedelta(seconds=1)):
            with self.subTest():
                r = Retrying(wait=tenacity.wait_fixed(wait))
                self.assertEqual(1, r.wait(make_retry_state(12, 6546)))

    def test_incrementing_sleep(self):
        for start, increment in (
            (500, 100),
            (datetime.timedelta(seconds=500), datetime.timedelta(seconds=100)),
        ):
            with self.subTest():
                r = Retrying(
                    wait=tenacity.wait_incrementing(start=start, increment=increment)
                )
                self.assertEqual(500, r.wait(make_retry_state(1, 6546)))
                self.assertEqual(600, r.wait(make_retry_state(2, 6546)))
                self.assertEqual(700, r.wait(make_retry_state(3, 6546)))

    def test_random_sleep(self):
        for min_, max_ in (
            (1, 20),
            (datetime.timedelta(seconds=1), datetime.timedelta(seconds=20)),
        ):
            with self.subTest():
                r = Retrying(wait=tenacity.wait_random(min=min_, max=max_))
                times = set()
                for _ in range(1000):
                    times.add(r.wait(make_retry_state(1, 6546)))

                # this is kind of non-deterministic...
                self.assertTrue(len(times) > 1)
                for t in times:
                    self.assertTrue(t >= 1)
                    self.assertTrue(t < 20)

    def test_random_sleep_withoutmin_(self):
        r = Retrying(wait=tenacity.wait_random(max=2))
        times = set()
        times.add(r.wait(make_retry_state(1, 6546)))
        times.add(r.wait(make_retry_state(1, 6546)))
        times.add(r.wait(make_retry_state(1, 6546)))
        times.add(r.wait(make_retry_state(1, 6546)))

        # this is kind of non-deterministic...
        self.assertTrue(len(times) > 1)
        for t in times:
            self.assertTrue(t >= 0)
            self.assertTrue(t <= 2)

    def test_exponential(self):
        r = Retrying(wait=tenacity.wait_exponential())
        self.assertEqual(r.wait(make_retry_state(1, 0)), 1)
        self.assertEqual(r.wait(make_retry_state(2, 0)), 2)
        self.assertEqual(r.wait(make_retry_state(3, 0)), 4)
        self.assertEqual(r.wait(make_retry_state(4, 0)), 8)
        self.assertEqual(r.wait(make_retry_state(5, 0)), 16)
        self.assertEqual(r.wait(make_retry_state(6, 0)), 32)
        self.assertEqual(r.wait(make_retry_state(7, 0)), 64)
        self.assertEqual(r.wait(make_retry_state(8, 0)), 128)

    def test_exponential_with_max_wait(self):
        r = Retrying(wait=tenacity.wait_exponential(max=40))
        self.assertEqual(r.wait(make_retry_state(1, 0)), 1)
        self.assertEqual(r.wait(make_retry_state(2, 0)), 2)
        self.assertEqual(r.wait(make_retry_state(3, 0)), 4)
        self.assertEqual(r.wait(make_retry_state(4, 0)), 8)
        self.assertEqual(r.wait(make_retry_state(5, 0)), 16)
        self.assertEqual(r.wait(make_retry_state(6, 0)), 32)
        self.assertEqual(r.wait(make_retry_state(7, 0)), 40)
        self.assertEqual(r.wait(make_retry_state(8, 0)), 40)
        self.assertEqual(r.wait(make_retry_state(50, 0)), 40)

    def test_exponential_with_min_wait(self):
        r = Retrying(wait=tenacity.wait_exponential(min=20))
        self.assertEqual(r.wait(make_retry_state(1, 0)), 20)
        self.assertEqual(r.wait(make_retry_state(2, 0)), 20)
        self.assertEqual(r.wait(make_retry_state(3, 0)), 20)
        self.assertEqual(r.wait(make_retry_state(4, 0)), 20)
        self.assertEqual(r.wait(make_retry_state(5, 0)), 20)
        self.assertEqual(r.wait(make_retry_state(6, 0)), 32)
        self.assertEqual(r.wait(make_retry_state(7, 0)), 64)
        self.assertEqual(r.wait(make_retry_state(8, 0)), 128)
        self.assertEqual(r.wait(make_retry_state(20, 0)), 524288)

    def test_exponential_with_max_wait_and_multiplier(self):
        r = Retrying(wait=tenacity.wait_exponential(max=50, multiplier=1))
        self.assertEqual(r.wait(make_retry_state(1, 0)), 1)
        self.assertEqual(r.wait(make_retry_state(2, 0)), 2)
        self.assertEqual(r.wait(make_retry_state(3, 0)), 4)
        self.assertEqual(r.wait(make_retry_state(4, 0)), 8)
        self.assertEqual(r.wait(make_retry_state(5, 0)), 16)
        self.assertEqual(r.wait(make_retry_state(6, 0)), 32)
        self.assertEqual(r.wait(make_retry_state(7, 0)), 50)
        self.assertEqual(r.wait(make_retry_state(8, 0)), 50)
        self.assertEqual(r.wait(make_retry_state(50, 0)), 50)

    def test_exponential_with_min_wait_and_multiplier(self):
        r = Retrying(wait=tenacity.wait_exponential(min=20, multiplier=2))
        self.assertEqual(r.wait(make_retry_state(1, 0)), 20)
        self.assertEqual(r.wait(make_retry_state(2, 0)), 20)
        self.assertEqual(r.wait(make_retry_state(3, 0)), 20)
        self.assertEqual(r.wait(make_retry_state(4, 0)), 20)
        self.assertEqual(r.wait(make_retry_state(5, 0)), 32)
        self.assertEqual(r.wait(make_retry_state(6, 0)), 64)
        self.assertEqual(r.wait(make_retry_state(7, 0)), 128)
        self.assertEqual(r.wait(make_retry_state(8, 0)), 256)
        self.assertEqual(r.wait(make_retry_state(20, 0)), 1048576)

    def test_exponential_with_min_wait_andmax__wait(self):
        for min_, max_ in (
            (10, 100),
            (datetime.timedelta(seconds=10), datetime.timedelta(seconds=100)),
        ):
            with self.subTest():
                r = Retrying(wait=tenacity.wait_exponential(min=min_, max=max_))
                self.assertEqual(r.wait(make_retry_state(1, 0)), 10)
                self.assertEqual(r.wait(make_retry_state(2, 0)), 10)
                self.assertEqual(r.wait(make_retry_state(3, 0)), 10)
                self.assertEqual(r.wait(make_retry_state(4, 0)), 10)
                self.assertEqual(r.wait(make_retry_state(5, 0)), 16)
                self.assertEqual(r.wait(make_retry_state(6, 0)), 32)
                self.assertEqual(r.wait(make_retry_state(7, 0)), 64)
                self.assertEqual(r.wait(make_retry_state(8, 0)), 100)
                self.assertEqual(r.wait(make_retry_state(9, 0)), 100)
                self.assertEqual(r.wait(make_retry_state(20, 0)), 100)

    def test_legacy_explicit_wait_type(self):
        Retrying(wait="exponential_sleep")

    def test_wait_func(self):
        def wait_func(retry_state):
            return retry_state.attempt_number * retry_state.seconds_since_start

        r = Retrying(wait=wait_func)
        self.assertEqual(r.wait(make_retry_state(1, 5)), 5)
        self.assertEqual(r.wait(make_retry_state(2, 11)), 22)
        self.assertEqual(r.wait(make_retry_state(10, 100)), 1000)

    def test_wait_combine(self):
        r = Retrying(
            wait=tenacity.wait_combine(
                tenacity.wait_random(0, 3), tenacity.wait_fixed(5)
            )
        )
        # Test it a few time since it's random
        for i in range(1000):
            w = r.wait(make_retry_state(1, 5))
            self.assertLess(w, 8)
            self.assertGreaterEqual(w, 5)

    def test_wait_double_sum(self):
        r = Retrying(wait=tenacity.wait_random(0, 3) + tenacity.wait_fixed(5))
        # Test it a few time since it's random
        for i in range(1000):
            w = r.wait(make_retry_state(1, 5))
            self.assertLess(w, 8)
            self.assertGreaterEqual(w, 5)

    def test_wait_triple_sum(self):
        r = Retrying(
            wait=tenacity.wait_fixed(1)
            + tenacity.wait_random(0, 3)
            + tenacity.wait_fixed(5)
        )
        # Test it a few time since it's random
        for i in range(1000):
            w = r.wait(make_retry_state(1, 5))
            self.assertLess(w, 9)
            self.assertGreaterEqual(w, 6)

    def test_wait_arbitrary_sum(self):
        r = Retrying(
            wait=sum(
                [
                    tenacity.wait_fixed(1),
                    tenacity.wait_random(0, 3),
                    tenacity.wait_fixed(5),
                    tenacity.wait_none(),
                ]
            )
        )
        # Test it a few time since it's random
        for _ in range(1000):
            w = r.wait(make_retry_state(1, 5))
            self.assertLess(w, 9)
            self.assertGreaterEqual(w, 6)

    def _assert_range(self, wait, min_, max_):
        self.assertLess(wait, max_)
        self.assertGreaterEqual(wait, min_)

    def _assert_inclusive_range(self, wait, low, high):
        self.assertLessEqual(wait, high)
        self.assertGreaterEqual(wait, low)

    def _assert_inclusive_epsilon(self, wait, target, epsilon):
        self.assertLessEqual(wait, target + epsilon)
        self.assertGreaterEqual(wait, target - epsilon)

    def test_wait_chain(self):
        r = Retrying(
            wait=tenacity.wait_chain(
                *[tenacity.wait_fixed(1) for i in range(2)]
                + [tenacity.wait_fixed(4) for i in range(2)]
                + [tenacity.wait_fixed(8) for i in range(1)]
            )
        )

        for i in range(10):
            w = r.wait(make_retry_state(i + 1, 1))
            if i < 2:
                self._assert_range(w, 1, 2)
            elif i < 4:
                self._assert_range(w, 4, 5)
            else:
                self._assert_range(w, 8, 9)

    def test_wait_chain_multiple_invocations(self):
        sleep_intervals = []
        r = Retrying(
            sleep=sleep_intervals.append,
            wait=tenacity.wait_chain(*[tenacity.wait_fixed(i + 1) for i in range(3)]),
            stop=tenacity.stop_after_attempt(5),
            retry=tenacity.retry_if_result(lambda x: x == 1),
        )

        @r.wraps
        def always_return_1():
            return 1

        self.assertRaises(tenacity.RetryError, always_return_1)
        self.assertEqual(sleep_intervals, [1.0, 2.0, 3.0, 3.0])
        sleep_intervals[:] = []

        # Clear and restart retrying.
        self.assertRaises(tenacity.RetryError, always_return_1)
        self.assertEqual(sleep_intervals, [1.0, 2.0, 3.0, 3.0])
        sleep_intervals[:] = []

    def test_wait_random_exponential(self):
        fn = tenacity.wait_random_exponential(0.5, 60.0)

        for _ in range(1000):
            self._assert_inclusive_range(fn(make_retry_state(1, 0)), 0, 0.5)
            self._assert_inclusive_range(fn(make_retry_state(2, 0)), 0, 1.0)
            self._assert_inclusive_range(fn(make_retry_state(3, 0)), 0, 2.0)
            self._assert_inclusive_range(fn(make_retry_state(4, 0)), 0, 4.0)
            self._assert_inclusive_range(fn(make_retry_state(5, 0)), 0, 8.0)
            self._assert_inclusive_range(fn(make_retry_state(6, 0)), 0, 16.0)
            self._assert_inclusive_range(fn(make_retry_state(7, 0)), 0, 32.0)
            self._assert_inclusive_range(fn(make_retry_state(8, 0)), 0, 60.0)
            self._assert_inclusive_range(fn(make_retry_state(9, 0)), 0, 60.0)

        # max wait
        max_wait = 5
        fn = tenacity.wait_random_exponential(10, max_wait)
        for _ in range(1000):
            self._assert_inclusive_range(fn(make_retry_state(1, 0)), 0.00, max_wait)

        # min wait
        min_wait = 5
        fn = tenacity.wait_random_exponential(min=min_wait)
        for _ in range(1000):
            self._assert_inclusive_range(fn(make_retry_state(1, 0)), min_wait, 5)

        # Default arguments exist
        fn = tenacity.wait_random_exponential()
        fn(make_retry_state(0, 0))

    def test_wait_random_exponential_statistically(self):
        fn = tenacity.wait_random_exponential(0.5, 60.0)

        attempt = []
        for i in range(10):
            attempt.append([fn(make_retry_state(i, 0)) for _ in range(4000)])

        def mean(lst):
            return float(sum(lst)) / float(len(lst))

        # skipping attempt 0
        self._assert_inclusive_epsilon(mean(attempt[1]), 0.25, 0.02)
        self._assert_inclusive_epsilon(mean(attempt[2]), 0.50, 0.04)
        self._assert_inclusive_epsilon(mean(attempt[3]), 1, 0.08)
        self._assert_inclusive_epsilon(mean(attempt[4]), 2, 0.16)
        self._assert_inclusive_epsilon(mean(attempt[5]), 4, 0.32)
        self._assert_inclusive_epsilon(mean(attempt[6]), 8, 0.64)
        self._assert_inclusive_epsilon(mean(attempt[7]), 16, 1.28)
        self._assert_inclusive_epsilon(mean(attempt[8]), 30, 2.56)
        self._assert_inclusive_epsilon(mean(attempt[9]), 30, 2.56)

    def test_wait_exponential_jitter(self):
        fn = tenacity.wait_exponential_jitter(max=60)

        for _ in range(1000):
            self._assert_inclusive_range(fn(make_retry_state(1, 0)), 1, 2)
            self._assert_inclusive_range(fn(make_retry_state(2, 0)), 2, 3)
            self._assert_inclusive_range(fn(make_retry_state(3, 0)), 4, 5)
            self._assert_inclusive_range(fn(make_retry_state(4, 0)), 8, 9)
            self._assert_inclusive_range(fn(make_retry_state(5, 0)), 16, 17)
            self._assert_inclusive_range(fn(make_retry_state(6, 0)), 32, 33)
            self.assertEqual(fn(make_retry_state(7, 0)), 60)
            self.assertEqual(fn(make_retry_state(8, 0)), 60)
            self.assertEqual(fn(make_retry_state(9, 0)), 60)

        fn = tenacity.wait_exponential_jitter(10, 5)
        for _ in range(1000):
            self.assertEqual(fn(make_retry_state(1, 0)), 5)

        # Default arguments exist
        fn = tenacity.wait_exponential_jitter()
        fn(make_retry_state(0, 0))

    def test_wait_retry_state_attributes(self):
        class ExtractCallState(Exception):
            pass

        # retry_state is mutable, so return it as an exception to extract the
        # exact values it has when wait is called and bypass any other logic.
        def waitfunc(retry_state):
            raise ExtractCallState(retry_state)

        retrying = Retrying(
            wait=waitfunc,
            retry=(
                tenacity.retry_if_exception_type()
                | tenacity.retry_if_result(lambda result: result == 123)
            ),
        )

        def returnval():
            return 123

        try:
            retrying(returnval)
        except ExtractCallState as err:
            retry_state = err.args[0]
        self.assertIs(retry_state.fn, returnval)
        self.assertEqual(retry_state.args, ())
        self.assertEqual(retry_state.kwargs, {})
        self.assertEqual(retry_state.outcome.result(), 123)
        self.assertEqual(retry_state.attempt_number, 1)
        self.assertGreaterEqual(retry_state.outcome_timestamp, retry_state.start_time)

        def dying():
            raise Exception("Broken")

        try:
            retrying(dying)
        except ExtractCallState as err:
            retry_state = err.args[0]
        self.assertIs(retry_state.fn, dying)
        self.assertEqual(retry_state.args, ())
        self.assertEqual(retry_state.kwargs, {})
        self.assertEqual(str(retry_state.outcome.exception()), "Broken")
        self.assertEqual(retry_state.attempt_number, 1)
        self.assertGreaterEqual(retry_state.outcome_timestamp, retry_state.start_time)


class TestRetryConditions(unittest.TestCase):
    def test_retry_if_result(self):
        retry = tenacity.retry_if_result(lambda x: x == 1)

        def r(fut):
            retry_state = make_retry_state(1, 1.0, last_result=fut)
            return retry(retry_state)

        self.assertTrue(r(tenacity.Future.construct(1, 1, False)))
        self.assertFalse(r(tenacity.Future.construct(1, 2, False)))

    def test_retry_if_not_result(self):
        retry = tenacity.retry_if_not_result(lambda x: x == 1)

        def r(fut):
            retry_state = make_retry_state(1, 1.0, last_result=fut)
            return retry(retry_state)

        self.assertTrue(r(tenacity.Future.construct(1, 2, False)))
        self.assertFalse(r(tenacity.Future.construct(1, 1, False)))

    def test_retry_any(self):
        retry = tenacity.retry_any(
            tenacity.retry_if_result(lambda x: x == 1),
            tenacity.retry_if_result(lambda x: x == 2),
        )

        def r(fut):
            retry_state = make_retry_state(1, 1.0, last_result=fut)
            return retry(retry_state)

        self.assertTrue(r(tenacity.Future.construct(1, 1, False)))
        self.assertTrue(r(tenacity.Future.construct(1, 2, False)))
        self.assertFalse(r(tenacity.Future.construct(1, 3, False)))
        self.assertFalse(r(tenacity.Future.construct(1, 1, True)))

    def test_retry_all(self):
        retry = tenacity.retry_all(
            tenacity.retry_if_result(lambda x: x == 1),
            tenacity.retry_if_result(lambda x: isinstance(x, int)),
        )

        def r(fut):
            retry_state = make_retry_state(1, 1.0, last_result=fut)
            return retry(retry_state)

        self.assertTrue(r(tenacity.Future.construct(1, 1, False)))
        self.assertFalse(r(tenacity.Future.construct(1, 2, False)))
        self.assertFalse(r(tenacity.Future.construct(1, 3, False)))
        self.assertFalse(r(tenacity.Future.construct(1, 1, True)))

    def test_retry_and(self):
        retry = tenacity.retry_if_result(lambda x: x == 1) & tenacity.retry_if_result(
            lambda x: isinstance(x, int)
        )

        def r(fut):
            retry_state = make_retry_state(1, 1.0, last_result=fut)
            return retry(retry_state)

        self.assertTrue(r(tenacity.Future.construct(1, 1, False)))
        self.assertFalse(r(tenacity.Future.construct(1, 2, False)))
        self.assertFalse(r(tenacity.Future.construct(1, 3, False)))
        self.assertFalse(r(tenacity.Future.construct(1, 1, True)))

    def test_retry_or(self):
        retry = tenacity.retry_if_result(
            lambda x: x == "foo"
        ) | tenacity.retry_if_result(lambda x: isinstance(x, int))

        def r(fut):
            retry_state = make_retry_state(1, 1.0, last_result=fut)
            return retry(retry_state)

        self.assertTrue(r(tenacity.Future.construct(1, "foo", False)))
        self.assertFalse(r(tenacity.Future.construct(1, "foobar", False)))
        self.assertFalse(r(tenacity.Future.construct(1, 2.2, False)))
        self.assertFalse(r(tenacity.Future.construct(1, 42, True)))

    def _raise_try_again(self):
        self._attempts += 1
        if self._attempts < 3:
            raise tenacity.TryAgain

    def test_retry_try_again(self):
        self._attempts = 0
        Retrying(stop=tenacity.stop_after_attempt(5), retry=tenacity.retry_never)(
            self._raise_try_again
        )
        self.assertEqual(3, self._attempts)

    def test_retry_try_again_forever(self):
        def _r():
            raise tenacity.TryAgain

        r = Retrying(stop=tenacity.stop_after_attempt(5), retry=tenacity.retry_never)
        self.assertRaises(tenacity.RetryError, r, _r)
        self.assertEqual(5, r.statistics["attempt_number"])

    def test_retry_try_again_forever_reraise(self):
        def _r():
            raise tenacity.TryAgain

        r = Retrying(
            stop=tenacity.stop_after_attempt(5),
            retry=tenacity.retry_never,
            reraise=True,
        )
        self.assertRaises(tenacity.TryAgain, r, _r)
        self.assertEqual(5, r.statistics["attempt_number"])

    def test_retry_if_exception_message_negative_no_inputs(self):
        with self.assertRaises(TypeError):
            tenacity.retry_if_exception_message()

    def test_retry_if_exception_message_negative_too_many_inputs(self):
        with self.assertRaises(TypeError):
            tenacity.retry_if_exception_message(message="negative", match="negative")


class NoneReturnUntilAfterCount:
    """Holds counter state for invoking a method several times in a row."""

    def __init__(self, count):
        self.counter = 0
        self.count = count

    def go(self):
        """Return None until after count threshold has been crossed.

        Then return True.
        """
        if self.counter < self.count:
            self.counter += 1
            return None
        return True


class NoIOErrorAfterCount:
    """Holds counter state for invoking a method several times in a row."""

    def __init__(self, count):
        self.counter = 0
        self.count = count

    def go(self):
        """Raise an IOError until after count threshold has been crossed.

        Then return True.
        """
        if self.counter < self.count:
            self.counter += 1
            raise OSError("Hi there, I'm an IOError")
        return True


class NoNameErrorAfterCount:
    """Holds counter state for invoking a method several times in a row."""

    def __init__(self, count):
        self.counter = 0
        self.count = count

    def go(self):
        """Raise a NameError until after count threshold has been crossed.

        Then return True.
        """
        if self.counter < self.count:
            self.counter += 1
            raise NameError("Hi there, I'm a NameError")
        return True


class NoNameErrorCauseAfterCount:
    """Holds counter state for invoking a method several times in a row."""

    def __init__(self, count):
        self.counter = 0
        self.count = count

    def go2(self):
        raise NameError("Hi there, I'm a NameError")

    def go(self):
        """Raise an IOError with a NameError as cause until after count threshold has been crossed.

        Then return True.
        """
        if self.counter < self.count:
            self.counter += 1
            try:
                self.go2()
            except NameError as e:
                raise OSError() from e

        return True


class NoIOErrorCauseAfterCount:
    """Holds counter state for invoking a method several times in a row."""

    def __init__(self, count):
        self.counter = 0
        self.count = count

    def go2(self):
        raise OSError("Hi there, I'm an IOError")

    def go(self):
        """Raise a NameError with an IOError as cause until after count threshold has been crossed.

        Then return True.
        """
        if self.counter < self.count:
            self.counter += 1
            try:
                self.go2()
            except OSError as e:
                raise NameError() from e

        return True


class NameErrorUntilCount:
    """Holds counter state for invoking a method several times in a row."""

    derived_message = "Hi there, I'm a NameError"

    def __init__(self, count):
        self.counter = 0
        self.count = count

    def go(self):
        """Return True until after count threshold has been crossed.

        Then raise a NameError.
        """
        if self.counter < self.count:
            self.counter += 1
            return True
        raise NameError(self.derived_message)


class IOErrorUntilCount:
    """Holds counter state for invoking a method several times in a row."""

    def __init__(self, count):
        self.counter = 0
        self.count = count

    def go(self):
        """Return True until after count threshold has been crossed.

        Then raise an IOError.
        """
        if self.counter < self.count:
            self.counter += 1
            return True
        raise OSError("Hi there, I'm an IOError")


class CustomError(Exception):
    """This is a custom exception class.

    Note that For Python 2.x, we don't strictly need to extend BaseException,
    however, Python 3.x will complain. While this test suite won't run
    correctly under Python 3.x without extending from the Python exception
    hierarchy, the actual module code is backwards compatible Python 2.x and
    will allow for cases where exception classes don't extend from the
    hierarchy.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class NoCustomErrorAfterCount:
    """Holds counter state for invoking a method several times in a row."""

    derived_message = "This is a Custom exception class"

    def __init__(self, count):
        self.counter = 0
        self.count = count

    def go(self):
        """Raise a CustomError until after count threshold has been crossed.

        Then return True.
        """
        if self.counter < self.count:
            self.counter += 1
            raise CustomError(self.derived_message)
        return True


class CapturingHandler(logging.Handler):
    """Captures log records for inspection."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def emit(self, record):
        self.records.append(record)


def current_time_ms():
    return int(round(time.time() * 1000))


@retry(
    wait=tenacity.wait_fixed(0.05),
    retry=tenacity.retry_if_result(lambda result: result is None),
)
def _retryable_test_with_wait(thing):
    return thing.go()


@retry(
    stop=tenacity.stop_after_attempt(3),
    retry=tenacity.retry_if_result(lambda result: result is None),
)
def _retryable_test_with_stop(thing):
    return thing.go()


@retry(retry=tenacity.retry_if_exception_cause_type(NameError))
def _retryable_test_with_exception_cause_type(thing):
    return thing.go()


@retry(retry=tenacity.retry_if_exception_type(IOError))
def _retryable_test_with_exception_type_io(thing):
    return thing.go()


@retry(retry=tenacity.retry_if_not_exception_type(IOError))
def _retryable_test_if_not_exception_type_io(thing):
    return thing.go()


@retry(
    stop=tenacity.stop_after_attempt(3), retry=tenacity.retry_if_exception_type(IOError)
)
def _retryable_test_with_exception_type_io_attempt_limit(thing):
    return thing.go()


@retry(retry=tenacity.retry_unless_exception_type(NameError))
def _retryable_test_with_unless_exception_type_name(thing):
    return thing.go()


@retry(
    stop=tenacity.stop_after_attempt(3),
    retry=tenacity.retry_unless_exception_type(NameError),
)
def _retryable_test_with_unless_exception_type_name_attempt_limit(thing):
    return thing.go()


@retry(retry=tenacity.retry_unless_exception_type())
def _retryable_test_with_unless_exception_type_no_input(thing):
    return thing.go()


@retry(
    stop=tenacity.stop_after_attempt(5),
    retry=tenacity.retry_if_exception_message(
        message=NoCustomErrorAfterCount.derived_message
    ),
)
def _retryable_test_if_exception_message_message(thing):
    return thing.go()


@retry(
    retry=tenacity.retry_if_not_exception_message(
        message=NoCustomErrorAfterCount.derived_message
    )
)
def _retryable_test_if_not_exception_message_message(thing):
    return thing.go()


@retry(
    retry=tenacity.retry_if_exception_message(
        match=NoCustomErrorAfterCount.derived_message[:3] + ".*"
    )
)
def _retryable_test_if_exception_message_match(thing):
    return thing.go()


@retry(
    retry=tenacity.retry_if_not_exception_message(
        match=NoCustomErrorAfterCount.derived_message[:3] + ".*"
    )
)
def _retryable_test_if_not_exception_message_match(thing):
    return thing.go()


@retry(
    retry=tenacity.retry_if_not_exception_message(
        message=NameErrorUntilCount.derived_message
    )
)
def _retryable_test_not_exception_message_delay(thing):
    return thing.go()


@retry
def _retryable_default(thing):
    return thing.go()


@retry()
def _retryable_default_f(thing):
    return thing.go()


@retry(retry=tenacity.retry_if_exception_type(CustomError))
def _retryable_test_with_exception_type_custom(thing):
    return thing.go()


@retry(
    stop=tenacity.stop_after_attempt(3),
    retry=tenacity.retry_if_exception_type(CustomError),
)
def _retryable_test_with_exception_type_custom_attempt_limit(thing):
    return thing.go()


class TestDecoratorWrapper(unittest.TestCase):
    def test_with_wait(self):
        start = current_time_ms()
        result = _retryable_test_with_wait(NoneReturnUntilAfterCount(5))
        t = current_time_ms() - start
        self.assertGreaterEqual(t, 250)
        self.assertTrue(result)

    def test_with_stop_on_return_value(self):
        try:
            _retryable_test_with_stop(NoneReturnUntilAfterCount(5))
            self.fail("Expected RetryError after 3 attempts")
        except RetryError as re:
            self.assertFalse(re.last_attempt.failed)
            self.assertEqual(3, re.last_attempt.attempt_number)
            self.assertTrue(re.last_attempt.result() is None)
            print(re)

    def test_with_stop_on_exception(self):
        try:
            _retryable_test_with_stop(NoIOErrorAfterCount(5))
            self.fail("Expected IOError")
        except OSError as re:
            self.assertTrue(isinstance(re, IOError))
            print(re)

    def test_retry_if_exception_of_type(self):
        self.assertTrue(_retryable_test_with_exception_type_io(NoIOErrorAfterCount(5)))

        try:
            _retryable_test_with_exception_type_io(NoNameErrorAfterCount(5))
            self.fail("Expected NameError")
        except NameError as n:
            self.assertTrue(isinstance(n, NameError))
            print(n)

        self.assertTrue(
            _retryable_test_with_exception_type_custom(NoCustomErrorAfterCount(5))
        )

        try:
            _retryable_test_with_exception_type_custom(NoNameErrorAfterCount(5))
            self.fail("Expected NameError")
        except NameError as n:
            self.assertTrue(isinstance(n, NameError))
            print(n)

    def test_retry_except_exception_of_type(self):
        self.assertTrue(
            _retryable_test_if_not_exception_type_io(NoNameErrorAfterCount(5))
        )

        try:
            _retryable_test_if_not_exception_type_io(NoIOErrorAfterCount(5))
            self.fail("Expected IOError")
        except OSError as err:
            self.assertTrue(isinstance(err, IOError))
            print(err)

    def test_retry_until_exception_of_type_attempt_number(self):
        try:
            self.assertTrue(
                _retryable_test_with_unless_exception_type_name(NameErrorUntilCount(5))
            )
        except NameError as e:
            s = _retryable_test_with_unless_exception_type_name.statistics
            self.assertTrue(s["attempt_number"] == 6)
            print(e)
        else:
            self.fail("Expected NameError")

    def test_retry_until_exception_of_type_no_type(self):
        try:
            # no input should catch all subclasses of Exception
            self.assertTrue(
                _retryable_test_with_unless_exception_type_no_input(
                    NameErrorUntilCount(5)
                )
            )
        except NameError as e:
            s = _retryable_test_with_unless_exception_type_no_input.statistics
            self.assertTrue(s["attempt_number"] == 6)
            print(e)
        else:
            self.fail("Expected NameError")

    def test_retry_until_exception_of_type_wrong_exception(self):
        try:
            # two iterations with IOError, one that returns True
            _retryable_test_with_unless_exception_type_name_attempt_limit(
                IOErrorUntilCount(2)
            )
            self.fail("Expected RetryError")
        except RetryError as e:
            self.assertTrue(isinstance(e, RetryError))
            print(e)

    def test_retry_if_exception_message(self):
        try:
            self.assertTrue(
                _retryable_test_if_exception_message_message(NoCustomErrorAfterCount(3))
            )
        except CustomError:
            print(_retryable_test_if_exception_message_message.statistics)
            self.fail("CustomError should've been retried from errormessage")

    def test_retry_if_not_exception_message(self):
        try:
            self.assertTrue(
                _retryable_test_if_not_exception_message_message(
                    NoCustomErrorAfterCount(2)
                )
            )
        except CustomError:
            s = _retryable_test_if_not_exception_message_message.statistics
            self.assertTrue(s["attempt_number"] == 1)

    def test_retry_if_not_exception_message_delay(self):
        try:
            self.assertTrue(
                _retryable_test_not_exception_message_delay(NameErrorUntilCount(3))
            )
        except NameError:
            s = _retryable_test_not_exception_message_delay.statistics
            print(s["attempt_number"])
            self.assertTrue(s["attempt_number"] == 4)

    def test_retry_if_exception_message_match(self):
        try:
            self.assertTrue(
                _retryable_test_if_exception_message_match(NoCustomErrorAfterCount(3))
            )
        except CustomError:
            self.fail("CustomError should've been retried from errormessage")

    def test_retry_if_not_exception_message_match(self):
        try:
            self.assertTrue(
                _retryable_test_if_not_exception_message_message(
                    NoCustomErrorAfterCount(2)
                )
            )
        except CustomError:
            s = _retryable_test_if_not_exception_message_message.statistics
            self.assertTrue(s["attempt_number"] == 1)

    def test_retry_if_exception_cause_type(self):
        self.assertTrue(
            _retryable_test_with_exception_cause_type(NoNameErrorCauseAfterCount(5))
        )

        try:
            _retryable_test_with_exception_cause_type(NoIOErrorCauseAfterCount(5))
            self.fail("Expected exception without NameError as cause")
        except NameError:
            pass

    def test_retry_preserves_argument_defaults(self):
        def function_with_defaults(a=1):
            return a

        def function_with_kwdefaults(*, a=1):
            return a

        retrying = Retrying(
            wait=tenacity.wait_fixed(0.01), stop=tenacity.stop_after_attempt(3)
        )
        wrapped_defaults_function = retrying.wraps(function_with_defaults)
        wrapped_kwdefaults_function = retrying.wraps(function_with_kwdefaults)

        self.assertEqual(
            function_with_defaults.__defaults__, wrapped_defaults_function.__defaults__
        )
        self.assertEqual(
            function_with_kwdefaults.__kwdefaults__,
            wrapped_kwdefaults_function.__kwdefaults__,
        )

    def test_defaults(self):
        self.assertTrue(_retryable_default(NoNameErrorAfterCount(5)))
        self.assertTrue(_retryable_default_f(NoNameErrorAfterCount(5)))
        self.assertTrue(_retryable_default(NoCustomErrorAfterCount(5)))
        self.assertTrue(_retryable_default_f(NoCustomErrorAfterCount(5)))

    def test_retry_function_object(self):
        """Test that funсtools.wraps doesn't cause problems with callable objects.

        It raises an error upon trying to wrap it in Py2, because __name__
        attribute is missing. It's fixed in Py3 but was never backported.
        """

        class Hello:
            def __call__(self):
                return "Hello"

        retrying = Retrying(
            wait=tenacity.wait_fixed(0.01), stop=tenacity.stop_after_attempt(3)
        )
        h = retrying.wraps(Hello())
        self.assertEqual(h(), "Hello")

    def test_retry_function_attributes(self):
        """Test that the wrapped function attributes are exposed as intended.

        - statistics contains the value for the latest function run
        - retry object can be modified to change its behaviour (useful to patch in tests)
        - retry object statistics do not contain valid information
        """

        self.assertTrue(_retryable_test_with_stop(NoneReturnUntilAfterCount(2)))

        expected_stats = {
            "attempt_number": 3,
            "delay_since_first_attempt": mock.ANY,
            "idle_for": mock.ANY,
            "start_time": mock.ANY,
        }
        self.assertEqual(_retryable_test_with_stop.statistics, expected_stats)
        self.assertEqual(_retryable_test_with_stop.retry.statistics, {})

        with mock.patch.object(
            _retryable_test_with_stop.retry, "stop", tenacity.stop_after_attempt(1)
        ):
            try:
                self.assertTrue(_retryable_test_with_stop(NoneReturnUntilAfterCount(2)))
            except RetryError as exc:
                expected_stats = {
                    "attempt_number": 1,
                    "delay_since_first_attempt": mock.ANY,
                    "idle_for": mock.ANY,
                    "start_time": mock.ANY,
                }
                self.assertEqual(_retryable_test_with_stop.statistics, expected_stats)
                self.assertEqual(exc.last_attempt.attempt_number, 1)
                self.assertEqual(_retryable_test_with_stop.retry.statistics, {})
            else:
                self.fail("RetryError should have been raised after 1 attempt")


class TestRetryWith:
    def test_redefine_wait(self):
        start = current_time_ms()
        result = _retryable_test_with_wait.retry_with(wait=tenacity.wait_fixed(0.1))(
            NoneReturnUntilAfterCount(5)
        )
        t = current_time_ms() - start
        assert t >= 500
        assert result is True

    def test_redefine_stop(self):
        result = _retryable_test_with_stop.retry_with(
            stop=tenacity.stop_after_attempt(5)
        )(NoneReturnUntilAfterCount(4))
        assert result is True

    def test_retry_error_cls_should_be_preserved(self):
        @retry(stop=tenacity.stop_after_attempt(10), retry_error_cls=ValueError)
        def _retryable():
            raise Exception("raised for test purposes")

        with pytest.raises(Exception) as exc_ctx:
            _retryable.retry_with(stop=tenacity.stop_after_attempt(2))()

        assert exc_ctx.type is ValueError, "Should remap to specific exception type"

    def test_retry_error_callback_should_be_preserved(self):
        def return_text(retry_state):
            return "Calling {} keeps raising errors after {} attempts".format(
                retry_state.fn.__name__,
                retry_state.attempt_number,
            )

        @retry(stop=tenacity.stop_after_attempt(10), retry_error_callback=return_text)
        def _retryable():
            raise Exception("raised for test purposes")

        result = _retryable.retry_with(stop=tenacity.stop_after_attempt(5))()
        assert result == "Calling _retryable keeps raising errors after 5 attempts"


class TestBeforeAfterAttempts(unittest.TestCase):
    _attempt_number = 0

    def test_before_attempts(self):
        TestBeforeAfterAttempts._attempt_number = 0

        def _before(retry_state):
            TestBeforeAfterAttempts._attempt_number = retry_state.attempt_number

        @retry(
            wait=tenacity.wait_fixed(1),
            stop=tenacity.stop_after_attempt(1),
            before=_before,
        )
        def _test_before():
            pass

        _test_before()

        self.assertTrue(TestBeforeAfterAttempts._attempt_number == 1)

    def test_after_attempts(self):
        TestBeforeAfterAttempts._attempt_number = 0

        def _after(retry_state):
            TestBeforeAfterAttempts._attempt_number = retry_state.attempt_number

        @retry(
            wait=tenacity.wait_fixed(0.1),
            stop=tenacity.stop_after_attempt(3),
            after=_after,
        )
        def _test_after():
            if TestBeforeAfterAttempts._attempt_number < 2:
                raise Exception("testing after_attempts handler")
            else:
                pass

        _test_after()

        self.assertTrue(TestBeforeAfterAttempts._attempt_number == 2)

    def test_before_sleep(self):
        def _before_sleep(retry_state):
            self.assertGreater(retry_state.next_action.sleep, 0)
            _before_sleep.attempt_number = retry_state.attempt_number

        @retry(
            wait=tenacity.wait_fixed(0.01),
            stop=tenacity.stop_after_attempt(3),
            before_sleep=_before_sleep,
        )
        def _test_before_sleep():
            if _before_sleep.attempt_number < 2:
                raise Exception("testing before_sleep_attempts handler")

        _test_before_sleep()
        self.assertEqual(_before_sleep.attempt_number, 2)

    def _before_sleep_log_raises(self, get_call_fn):
        thing = NoIOErrorAfterCount(2)
        logger = logging.getLogger(self.id())
        logger.propagate = False
        logger.setLevel(logging.INFO)
        handler = CapturingHandler()
        logger.addHandler(handler)
        try:
            _before_sleep = tenacity.before_sleep_log(logger, logging.INFO)
            retrying = Retrying(
                wait=tenacity.wait_fixed(0.01),
                stop=tenacity.stop_after_attempt(3),
                before_sleep=_before_sleep,
            )
            get_call_fn(retrying)(thing.go)
        finally:
            logger.removeHandler(handler)

        etalon_re = (
            r"^Retrying .* in 0\.01 seconds as it raised "
            r"(IO|OS)Error: Hi there, I'm an IOError\.$"
        )
        self.assertEqual(len(handler.records), 2)
        fmt = logging.Formatter().format
        self.assertRegex(fmt(handler.records[0]), etalon_re)
        self.assertRegex(fmt(handler.records[1]), etalon_re)

    def test_before_sleep_log_raises(self):
        self._before_sleep_log_raises(lambda x: x)

    def test_before_sleep_log_raises_with_exc_info(self):
        thing = NoIOErrorAfterCount(2)
        logger = logging.getLogger(self.id())
        logger.propagate = False
        logger.setLevel(logging.INFO)
        handler = CapturingHandler()
        logger.addHandler(handler)
        try:
            _before_sleep = tenacity.before_sleep_log(
                logger, logging.INFO, exc_info=True
            )
            retrying = Retrying(
                wait=tenacity.wait_fixed(0.01),
                stop=tenacity.stop_after_attempt(3),
                before_sleep=_before_sleep,
            )
            retrying(thing.go)
        finally:
            logger.removeHandler(handler)

        etalon_re = re.compile(
            r"^Retrying .* in 0\.01 seconds as it raised "
            r"(IO|OS)Error: Hi there, I'm an IOError\.{0}"
            r"Traceback \(most recent call last\):{0}"
            r".*$".format("\n"),
            flags=re.MULTILINE,
        )
        self.assertEqual(len(handler.records), 2)
        fmt = logging.Formatter().format
        self.assertRegex(fmt(handler.records[0]), etalon_re)
        self.assertRegex(fmt(handler.records[1]), etalon_re)

    def test_before_sleep_log_returns(self, exc_info=False):
        thing = NoneReturnUntilAfterCount(2)
        logger = logging.getLogger(self.id())
        logger.propagate = False
        logger.setLevel(logging.INFO)
        handler = CapturingHandler()
        logger.addHandler(handler)
        try:
            _before_sleep = tenacity.before_sleep_log(
                logger, logging.INFO, exc_info=exc_info
            )
            _retry = tenacity.retry_if_result(lambda result: result is None)
            retrying = Retrying(
                wait=tenacity.wait_fixed(0.01),
                stop=tenacity.stop_after_attempt(3),
                retry=_retry,
                before_sleep=_before_sleep,
            )
            retrying(thing.go)
        finally:
            logger.removeHandler(handler)

        etalon_re = r"^Retrying .* in 0\.01 seconds as it returned None\.$"
        self.assertEqual(len(handler.records), 2)
        fmt = logging.Formatter().format
        self.assertRegex(fmt(handler.records[0]), etalon_re)
        self.assertRegex(fmt(handler.records[1]), etalon_re)

    def test_before_sleep_log_returns_with_exc_info(self):
        self.test_before_sleep_log_returns(exc_info=True)


class TestReraiseExceptions(unittest.TestCase):
    def test_reraise_by_default(self):
        calls = []

        @retry(
            wait=tenacity.wait_fixed(0.1),
            stop=tenacity.stop_after_attempt(2),
            reraise=True,
        )
        def _reraised_by_default():
            calls.append("x")
            raise KeyError("Bad key")

        self.assertRaises(KeyError, _reraised_by_default)
        self.assertEqual(2, len(calls))

    def test_reraise_from_retry_error(self):
        calls = []

        @retry(wait=tenacity.wait_fixed(0.1), stop=tenacity.stop_after_attempt(2))
        def _raise_key_error():
            calls.append("x")
            raise KeyError("Bad key")

        def _reraised_key_error():
            try:
                _raise_key_error()
            except tenacity.RetryError as retry_err:
                retry_err.reraise()

        self.assertRaises(KeyError, _reraised_key_error)
        self.assertEqual(2, len(calls))

    def test_reraise_timeout_from_retry_error(self):
        calls = []

        @retry(
            wait=tenacity.wait_fixed(0.1),
            stop=tenacity.stop_after_attempt(2),
            retry=lambda retry_state: True,
        )
        def _mock_fn():
            calls.append("x")

        def _reraised_mock_fn():
            try:
                _mock_fn()
            except tenacity.RetryError as retry_err:
                retry_err.reraise()

        self.assertRaises(tenacity.RetryError, _reraised_mock_fn)
        self.assertEqual(2, len(calls))

    def test_reraise_no_exception(self):
        calls = []

        @retry(
            wait=tenacity.wait_fixed(0.1),
            stop=tenacity.stop_after_attempt(2),
            retry=lambda retry_state: True,
            reraise=True,
        )
        def _mock_fn():
            calls.append("x")

        self.assertRaises(tenacity.RetryError, _mock_fn)
        self.assertEqual(2, len(calls))


class TestStatistics(unittest.TestCase):
    def test_stats(self):
        @retry()
        def _foobar():
            return 42

        self.assertEqual({}, _foobar.statistics)
        _foobar()
        self.assertEqual(1, _foobar.statistics["attempt_number"])

    def test_stats_failing(self):
        @retry(stop=tenacity.stop_after_attempt(2))
        def _foobar():
            raise ValueError(42)

        self.assertEqual({}, _foobar.statistics)
        try:
            _foobar()
        except Exception:  # noqa: B902
            pass
        self.assertEqual(2, _foobar.statistics["attempt_number"])


class TestRetryErrorCallback(unittest.TestCase):
    def setUp(self):
        self._attempt_number = 0
        self._callback_called = False

    def _callback(self, fut):
        self._callback_called = True
        return fut

    def test_retry_error_callback(self):
        num_attempts = 3

        def retry_error_callback(retry_state):
            retry_error_callback.called_times += 1
            return retry_state.outcome

        retry_error_callback.called_times = 0

        @retry(
            stop=tenacity.stop_after_attempt(num_attempts),
            retry_error_callback=retry_error_callback,
        )
        def _foobar():
            self._attempt_number += 1
            raise Exception("This exception should not be raised")

        result = _foobar()

        self.assertEqual(retry_error_callback.called_times, 1)
        self.assertEqual(num_attempts, self._attempt_number)
        self.assertIsInstance(result, tenacity.Future)


class TestContextManager(unittest.TestCase):
    def test_context_manager_retry_one(self):
        from tenacity import Retrying

        raise_ = True

        for attempt in Retrying():
            with attempt:
                if raise_:
                    raise_ = False
                    raise Exception("Retry it!")

    def test_context_manager_on_error(self):
        from tenacity import Retrying

        class CustomError(Exception):
            pass

        retry = Retrying(retry=tenacity.retry_if_exception_type(IOError))

        def test():
            for attempt in retry:
                with attempt:
                    raise CustomError("Don't retry!")

        self.assertRaises(CustomError, test)

    def test_context_manager_retry_error(self):
        from tenacity import Retrying

        retry = Retrying(stop=tenacity.stop_after_attempt(2))

        def test():
            for attempt in retry:
                with attempt:
                    raise Exception("Retry it!")

        self.assertRaises(RetryError, test)

    def test_context_manager_reraise(self):
        from tenacity import Retrying

        class CustomError(Exception):
            pass

        retry = Retrying(reraise=True, stop=tenacity.stop_after_attempt(2))

        def test():
            for attempt in retry:
                with attempt:
                    raise CustomError("Don't retry!")

        self.assertRaises(CustomError, test)


class TestInvokeAsCallable:
    """Test direct invocation of Retrying as a callable."""

    @staticmethod
    def invoke(retry, f):
        """
        Invoke Retrying logic.

        Wrapper allows testing different call mechanisms in test sub-classes.
        """
        return retry(f)

    def test_retry_one(self):
        def f():
            f.calls.append(len(f.calls) + 1)
            if len(f.calls) <= 1:
                raise Exception("Retry it!")
            return 42

        f.calls = []

        retry = Retrying()
        assert self.invoke(retry, f) == 42
        assert f.calls == [1, 2]

    def test_on_error(self):
        class CustomError(Exception):
            pass

        def f():
            f.calls.append(len(f.calls) + 1)
            if len(f.calls) <= 1:
                raise CustomError("Don't retry!")
            return 42

        f.calls = []

        retry = Retrying(retry=tenacity.retry_if_exception_type(IOError))
        with pytest.raises(CustomError):
            self.invoke(retry, f)
        assert f.calls == [1]

    def test_retry_error(self):
        def f():
            f.calls.append(len(f.calls) + 1)
            raise Exception("Retry it!")

        f.calls = []

        retry = Retrying(stop=tenacity.stop_after_attempt(2))
        with pytest.raises(RetryError):
            self.invoke(retry, f)
        assert f.calls == [1, 2]

    def test_reraise(self):
        class CustomError(Exception):
            pass

        def f():
            f.calls.append(len(f.calls) + 1)
            raise CustomError("Retry it!")

        f.calls = []

        retry = Retrying(reraise=True, stop=tenacity.stop_after_attempt(2))
        with pytest.raises(CustomError):
            self.invoke(retry, f)
        assert f.calls == [1, 2]


class TestRetryException(unittest.TestCase):
    def test_retry_error_is_pickleable(self):
        import pickle

        expected = RetryError(last_attempt=123)
        pickled = pickle.dumps(expected)
        actual = pickle.loads(pickled)
        self.assertEqual(expected.last_attempt, actual.last_attempt)


class TestRetryTyping(unittest.TestCase):
    @pytest.mark.skipif(
        sys.version_info < (3, 0), reason="typeguard not supported for python 2"
    )
    def test_retry_type_annotations(self):
        """The decorator should maintain types of decorated functions."""
        # Just in case this is run with unit-test, return early for py2
        if sys.version_info < (3, 0):
            return

        # Function-level import because we can't install this for python 2.
        from typeguard import check_type

        def num_to_str(number):
            # type: (int) -> str
            return str(number)

        # equivalent to a raw @retry decoration
        with_raw = retry(num_to_str)
        with_raw_result = with_raw(1)

        # equivalent to a @retry(...) decoration
        with_constructor = retry()(num_to_str)
        with_constructor_result = with_raw(1)

        # These raise TypeError exceptions if they fail
        check_type(with_raw, typing.Callable[[int], str])
        check_type(with_raw_result, str)
        check_type(with_constructor, typing.Callable[[int], str])
        check_type(with_constructor_result, str)


@contextmanager
def reports_deprecation_warning():
    __tracebackhide__ = True
    oldfilters = copy(warnings.filters)
    warnings.simplefilter("always")
    try:
        with pytest.warns(DeprecationWarning):
            yield
    finally:
        warnings.filters = oldfilters


class TestMockingSleep:
    RETRY_ARGS = dict(
        wait=tenacity.wait_fixed(0.1),
        stop=tenacity.stop_after_attempt(5),
    )

    def _fail(self):
        raise NotImplementedError()

    @retry(**RETRY_ARGS)
    def _decorated_fail(self):
        self._fail()

    @pytest.fixture()
    def mock_sleep(self, monkeypatch):
        class MockSleep:
            call_count = 0

            def __call__(self, seconds):
                self.call_count += 1

        sleep = MockSleep()
        monkeypatch.setattr(tenacity.nap.time, "sleep", sleep)
        yield sleep

    def test_decorated(self, mock_sleep):
        with pytest.raises(RetryError):
            self._decorated_fail()
        assert mock_sleep.call_count == 4

    def test_decorated_retry_with(self, mock_sleep):
        fail_faster = self._decorated_fail.retry_with(
            stop=tenacity.stop_after_attempt(2),
        )
        with pytest.raises(RetryError):
            fail_faster()
        assert mock_sleep.call_count == 1


if __name__ == "__main__":
    unittest.main()

```
tests/test_tornado.py
```.py
# mypy: disable-error-code="no-untyped-def,no-untyped-call"
# Copyright 2017 Elisey Zanko
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from tenacity import RetryError, retry, stop_after_attempt
from tenacity import tornadoweb

from tornado import gen
from tornado import testing

from .test_tenacity import NoIOErrorAfterCount


@retry
@gen.coroutine
def _retryable_coroutine(thing):
    yield gen.sleep(0.00001)
    thing.go()


@retry(stop=stop_after_attempt(2))
@gen.coroutine
def _retryable_coroutine_with_2_attempts(thing):
    yield gen.sleep(0.00001)
    thing.go()


class TestTornado(testing.AsyncTestCase):  # type: ignore[misc]
    @testing.gen_test
    def test_retry(self):
        assert gen.is_coroutine_function(_retryable_coroutine)
        thing = NoIOErrorAfterCount(5)
        yield _retryable_coroutine(thing)
        assert thing.counter == thing.count

    @testing.gen_test
    def test_stop_after_attempt(self):
        assert gen.is_coroutine_function(_retryable_coroutine)
        thing = NoIOErrorAfterCount(2)
        try:
            yield _retryable_coroutine_with_2_attempts(thing)
        except RetryError:
            assert thing.counter == 2

    def test_repr(self):
        repr(tornadoweb.TornadoRetrying())

    def test_old_tornado(self):
        old_attr = gen.is_coroutine_function
        try:
            del gen.is_coroutine_function

            # is_coroutine_function was introduced in tornado 4.5;
            # verify that we don't *completely* fall over on old versions
            @retry
            def retryable(thing):
                pass

        finally:
            gen.is_coroutine_function = old_attr


if __name__ == "__main__":
    unittest.main()

```
tests/test_utils.py
```.py
import functools

from tenacity import _utils


def test_is_coroutine_callable() -> None:
    async def async_func() -> None:
        pass

    def sync_func() -> None:
        pass

    class AsyncClass:
        async def __call__(self) -> None:
            pass

    class SyncClass:
        def __call__(self) -> None:
            pass

    lambda_fn = lambda: None  # noqa: E731

    partial_async_func = functools.partial(async_func)
    partial_sync_func = functools.partial(sync_func)
    partial_async_class = functools.partial(AsyncClass().__call__)
    partial_sync_class = functools.partial(SyncClass().__call__)
    partial_lambda_fn = functools.partial(lambda_fn)

    assert _utils.is_coroutine_callable(async_func) is True
    assert _utils.is_coroutine_callable(sync_func) is False
    assert _utils.is_coroutine_callable(AsyncClass) is False
    assert _utils.is_coroutine_callable(AsyncClass()) is True
    assert _utils.is_coroutine_callable(SyncClass) is False
    assert _utils.is_coroutine_callable(SyncClass()) is False
    assert _utils.is_coroutine_callable(lambda_fn) is False

    assert _utils.is_coroutine_callable(partial_async_func) is True
    assert _utils.is_coroutine_callable(partial_sync_func) is False
    assert _utils.is_coroutine_callable(partial_async_class) is True
    assert _utils.is_coroutine_callable(partial_sync_class) is False
    assert _utils.is_coroutine_callable(partial_lambda_fn) is False

```
tox.ini
```.ini
[tox]
# we only test trio on latest python version
envlist = py3{9,10,11,12,13,13-trio}, pep8, pypy3
skip_missing_interpreters = True

[testenv]
usedevelop = True
sitepackages = False
deps =
    .[test]
    .[doc]
    trio: trio
commands =
    py3{8,9,10,11,12,13},pypy3: pytest {posargs}
    py3{8,9,10,11,12,13},pypy3: sphinx-build -a -E -W -b doctest doc/source doc/build
    py3{8,9,10,11,12,13},pypy3: sphinx-build -a -E -W -b html doc/source doc/build

[testenv:pep8]
basepython = python3
deps = ruff
commands =
  ruff check . {posargs}
  ruff format --check . {posargs}

[testenv:mypy]
deps =
    mypy>=1.0.0
    pytest # for stubs
    trio
commands =
    mypy {posargs}

[testenv:reno]
basepython = python3
deps = reno
commands = reno {posargs}

```


## https://github.com/bharel/asynciolimiter

Token Usage:
GitHub Tokens: 16253
LLM Input Tokens: 0
LLM Output Tokens: 0
Total Tokens: 16253

FileTree:
.github/FUNDING.yml
.github/workflows/release.yml
.github/workflows/test.yml
.gitignore
.readthedocs.yaml
CONTRIBUTING.md
README.md
asynciolimiter/__init__.py
changelog.md
cliff.toml
docs/_static/custom.css
docs/conf.py
docs/make.bat
pyproject.toml
scripts/build.bat
scripts/run_open_coverage.bat
scripts/run_tests.bat
scripts/upload_real.bat
scripts/upload_test.bat
tests/__init__.py
tests/test_limiter.py

Analysis:
.github/FUNDING.yml
```.yml
buy_me_a_coffee: bharel
github: bharel

```
.github/workflows/release.yml
```.yml
name: Release asynciolimiter

on:
  release:
    types: [published]

jobs:
  check_version:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: 3.12
      - name: Verify version
        run: |
          PY_VER=$(python -c "import asynciolimiter;print(asynciolimiter.__version__)")
          echo Python version - "$PY_VER"
          TAG_VER=${{ github.event.release.tag_name }}
          echo Tag version "$TAG_VER"
          [[ $TAG_VER == $PY_VER ]]
  upload_test_pypi:
    needs: check_version
    runs-on: ubuntu-latest
    environment:
      name: Test PyPi
      url: https://test.pypi.org/p/asynciolimiter
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Build wheel
        run: |
          pip install hatch
          hatch build
      - name: Publish on Test PyPi
        run: hatch publish -r test -u ${{ secrets.PYPI_USERNAME }} -a ${{ secrets.PYPI_PASSWORD }}
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/*
  upload_production_pypi:
    needs: upload_test_pypi
    runs-on: ubuntu-latest
    environment:
      name: Production PyPi
      url: https://pypi.org/p/asynciolimiter
    permissions:
      id-token: write
      contents: write
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - uses: AButler/upload-release-assets@v3.0
        with:
          files: 'dist/*'
          repo-token: ${{ secrets.GITHUB_TOKEN }}
      - name: Upload release to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1

```
.github/workflows/test.yml
```.yml
name: Test asynciolimiter

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install hatch
        run: pip install hatch
      - name: Lint using hatch
        run: hatch fmt --check
      - name: Install mypy
        run: pip install mypy
      - name: Lint using mypy
        run: >-
          mypy --ignore-missing-imports --check-untyped-defs
          asynciolimiter
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: true
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: [3.11, 3.12, "3.13.0-rc.1"]
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install hatch
      run: pip install hatch
    - name: Test on Python ${{ matrix.python-version }}
      run: hatch test
  
  generate-coverage:
    runs-on: ubuntu-latest
    needs: test
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python 3.12
      uses: actions/setup-python@v5
      with:
        python-version: "3.12"
    - name: Install Coverage
      run: pip install coverage
    - name: Generate coverage report
      run: coverage run --branch -m unittest && coverage xml
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v1
      with:
        token: ${{ secrets.CODECOV_TOKEN }}
        file: ./coverage.xml
        flags: unittests



```
.gitignore
```.gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
**/.DS_STORE
# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/
.idea
*.whl
.vscode

```
.readthedocs.yaml
```.yaml
# .readthedocs.yaml
# Read the Docs configuration file
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

# Required
version: 2

# Set the version of Python and other tools you might need
build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

# Build documentation in the docs/ directory with Sphinx
sphinx:
  configuration: docs/conf.py

# We recommend specifying your dependencies to enable reproducible builds:
# https://docs.readthedocs.io/en/stable/guides/reproducible-builds.html
# python:
#   install:
#   - requirements: docs/requirements.txt
```
CONTRIBUTING.md
# Contributing to asynciolimiter

Thank you for considering contributing to asynciolimiter! Here are some guidelines to help you get started:

## Getting Started

1. **Fork the Repository**: Fork the repository to your own GitHub account.

2. **Clone the Repository**: Clone your forked repository to your local machine.
   ```sh
   git clone https://github.com/your-username/asynciolimiter.git
   ```

3. **Create a Branch**: Create a new branch for your feature or bug fix.
   ```sh
   git checkout -b feature-or-bugfix-name
   ```

## Making Changes

1. **Install Dependencies**: Install the necessary dependencies using `hatch`.
   ```sh
   pip install hatch
   hatch env create dev
   ```

2. **Make Changes**: Implement your changes in the codebase.

3. **Run Tests**: Ensure that all tests pass before committing your changes.
   ```sh
   hatch test
   ```

4. **Run Formatter**: Format your code to adhere to the project's style guidelines.
   ```sh
   hatch fmt
   ```

5. **Commit Changes**: Commit your changes with a descriptive commit message.
   ```sh
   git commit -a -m "Description of the changes made"
   ```

6. **Push Changes**: Push your changes to your forked repository.
   ```sh
   git push origin feature-or-bugfix-name
   ```

## Submitting Changes

1. **Create a Pull Request**: Open a pull request to the main repository. Provide a clear description of the changes and any related issue numbers.

2. **Review Process**: Participate in the review process. Make any requested changes and update the pull request.

3. **Merge**: Once approved, your changes will be merged into the main repository.

## Code Style

- Follow the PEP 8 style guide for Python code.
- Use type hints where appropriate.
- Write clear and concise commit messages.

## Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub. Provide as much detail as possible to help us understand and address the issue.

Thank you for your contributions!

# For Maintainers

## Merging PRs

1. **Wait for all checks to complete**: These include linters and testing.
2. **Merge with squash**: Change the commit message according to the prefixes set in `cliff.toml`, ending with `(#PR)`.  
    For example:  
   `feat: My new feature (#12)`  
   or  
   `fix: My bugfix (#45)`.

## Bumping Version

1. **Install Dependencies**: Ensure you have `git-cliff` and `hatch` installed.
   ```sh
   pip install git-cliff hatch
   ```

2. **Update Version**: Use `hatch` to bump the version. Replace `x.y.z` with the new version number.
   ```sh
   hatch version x.y.z
   ```
   Alternatively, bump the version by specifying the designator such as `minor` or `post`.
   ```sh
   hatch version patch
   ```

3. **Generate Changelog**: Use `git-cliff` to generate the changelog. Replace `x.y.z` with the new version number.
   ```sh
   git cliff --tag x.y.z -o CHANGELOG.md
   ```

4. **Commit Changes**: Commit the updated `CHANGELOG.md` and version changes.
   ```sh
   git add CHANGELOG.md pyproject.toml
   git commit -a -m "Bump version to x.y.z"
   ```

5. **Tag the Release**: Create a new git tag for the release.
   ```sh
   git tag x.y.z
   git push origin x.y.z
   ```

6. **Push Changes**: Push the changes to the main repository.
   ```sh
   git push origin master
   ```

7. **Create Release**: Go to the GitHub repository and create a new release using the pushed tag. Include the changelog in the release description.


README.md
# asynciolimiter
A simple yet efficient Python AsyncIO rate limiter.

[![GitHub branch checks state](https://img.shields.io/github/checks-status/bharel/asynciolimiter/master)](https://github.com/bharel/asynciolimiter/actions)
[![PyPI](https://img.shields.io/pypi/v/asynciolimiter)](https://pypi.org/project/asynciolimiter/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/asynciolimiter)](https://pypi.org/project/asynciolimiter/)
[![codecov](https://codecov.io/gh/bharel/asynciolimiter/branch/master/graph/badge.svg?token=BJBL909NH3)](https://codecov.io/gh/bharel/asynciolimiter)

## Installation
`pip install asynciolimiter`

## Sample Usage

```python
# Limit to 10 requests per 5 second (equiv to 2 requests per second)
>>> limiter = asynciolimiter.Limiter(10/5)
>>> async def main():
...     await limiter.wait() # Wait for a slot to be available.
...     pass # do stuff

>>> limiter = Limiter(1/3)
>>> async def request():
...     await limiter.wait()
...     print("Request")  # Do stuff
...
>>> async def main():
...     # Schedule 1 request every 3 seconds.
...     await asyncio.gather(*(request() for _ in range(10)))
```

## Available Limiter flavors

- `Limiter`: Limits by requests per second and takes into account CPU heavy
    tasks or other delays that can occur while the process is sleeping.
- `LeakyBucketLimiter`: Limits by requests per second according to the
    [leaky bucket algorithm](https://en.wikipedia.org/wiki/Leaky_bucket). Has a maximum capacity and an initial burst of
    requests.
- `StrictLimiter`: Limits by requests per second, without taking CPU or other
    process sleeps into account. There are no bursts and the resulting rate will
    always be a less than the set limit.

## Documentation

Full documentation available on [Read the Docs](https://asynciolimiter.readthedocs.io/en/latest/).

## License

Licensed under the MIT License.

## Contribution
See [contributing.md](CONTRIBUTING.md).

asynciolimiter/__init__.py
```.py
# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Bar Harel
# Licensed under the MIT license as detailed in LICENSE.txt
"""AsyncIO rate limiters.

This module provides different rate limiters for asyncio.

    - `Limiter`: Limits by requests per second and takes into account CPU heavy
    tasks or other delays that can occur while the process is sleeping.
    - `LeakyBucketLimiter`: Limits by requests per second according to the
    leaky bucket algorithm. Has a maximum capacity and an initial burst of
    requests.
    - `StrictLimiter`: Limits by requests per second, without taking CPU or
    other process sleeps into account. There are no bursts and the resulting
    rate will always be a less than the set limit.

If you don't know which of these to choose, go for the regular Limiter.

The main method in each limiter is the wait(). For example:

    # Limit to 10 requests per 5 second (equiv to 2 requests per second)
    >>> limiter = Limiter(10 / 5)
    >>> async def main():
    ...     await limiter.wait()  # Wait for a slot to be available.
    ...     pass  # do stuff

    # Limit to, at most, 1 request every 10 seconds
    >>> limiter = StrictLimiter(1 / 10)

For more info, see the documentation for each limiter.
"""

import asyncio as _asyncio
import functools as _functools
from abc import ABC as _ABC
from abc import abstractmethod as _abstractmethod
from collections import deque as _deque
from collections.abc import Awaitable as _Awaitable
from collections.abc import Callable as _Callable
from typing import Any
from typing import TypeVar as _TypeVar
from typing import cast as _cast

__all__ = ["Limiter", "StrictLimiter", "LeakyBucketLimiter"]
__version__ = "1.1.1"
__author__ = "Bar Harel"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2022 Bar Harel"


_T = _TypeVar("_T")


def _pop_pending(futures: _deque[_asyncio.Future]) -> _asyncio.Future | None:
    """Pop until the first pending future is found and return it.

    If all futures are done, or deque is empty, return None.

    Args:
        futures: A deque of futures.

    Returns:
        The first pending future, or None if all futures are done.
    """
    while futures:
        waiter = futures.popleft()
        if not waiter.done():
            return waiter
    return None


class _BaseLimiter(_ABC):
    """Base class for all limiters."""

    @_abstractmethod
    async def wait(self) -> None:  # pragma: no cover # ABC
        """Wait for the limiter to let us through.

        Main function of the limiter. Blocks if limit has been reached, and
        lets us through once time passes.
        """

    @_abstractmethod
    def cancel(self) -> None:  # pragma: no cover # ABC
        """Cancel all waiting calls.

        This will cancel all currently waiting calls.
        Limiter is reusable afterwards, and new calls will wait as usual.
        """

    @_abstractmethod
    def breach(self) -> None:  # pragma: no cover # ABC
        """Let all calls through.

        All waiting calls will be let through, new `.wait()` calls will also
        pass without waiting, until `.reset()` is called.
        """

    @_abstractmethod
    def reset(self) -> None:  # pragma: no cover # ABC
        """Reset the limiter.

        This will cancel all waiting calls, reset all internal timers, and
        restore the limiter to its initial state.
        Limiter is reusable afterwards, and the next call will be
        immediately scheduled.
        """

    def wrap(self, coro: _Awaitable[_T]) -> _Awaitable[_T]:
        """Wrap a coroutine with the limiter.

        Returns a new coroutine that waits for the limiter to be unlocked, and
        then schedules the original coroutine.

        Equivalent to:

            >>> async def wrapper():
            ...     await limiter.wait()
            ...     return await coro
            >>> wapper()

        Example use:

            >>> async def foo(number):
            ...     print(number)  # Do stuff
            >>> limiter = Limiter(1)
            >>> async def main():
            ...     print_numbers = (foo(i) for i in range(10))
            ...     # This will print the numbers over 10 seconds
            ...     await asyncio.gather(*map(limiter.wrap, print_numbers))

        Args:
            coro: The coroutine or awaitable to wrap.

        Returns:
            The wrapped coroutine.
        """

        async def _wrapper() -> _T:
            await self.wait()
            return await coro

        wrapper = _wrapper()
        _functools.update_wrapper(_wrapper, _cast(_Callable, coro))
        return wrapper


class _CommonLimiterMixin(_BaseLimiter):
    """Some common attributes a limiter might need.

    Includes:
        _waiters: A deque of futures waiting for the limiter to be unlocked.
        _locked: Whether the limiter is locked.
        _breached: Whether the limiter has been breached.
        _wakeup_handle: An asyncio.TimerHandle for the next scheduled wakeup.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the limiter.

        Subclasses must call `super()`.
        """
        super().__init__(*args, **kwargs)
        self._locked = False
        self._waiters: _deque[_asyncio.Future] = _deque()
        self._wakeup_handle: _asyncio.TimerHandle | None = None
        self._breached = False

    async def wait(self) -> None:
        if self._breached:
            return

        if not self._locked:
            self._maybe_lock()
            return
        fut = _asyncio.get_running_loop().create_future()
        self._waiters.append(fut)
        await fut

    def cancel(self) -> None:
        while self._waiters:
            self._waiters.popleft().cancel()

    def breach(self) -> None:
        while self._waiters:
            fut = self._waiters.popleft()
            if not fut.done():
                fut.set_result(None)
        self._cancel_wakeup()
        self._breached = True
        self._locked = False

    def _cancel_wakeup(self) -> None:
        if self._wakeup_handle is not None:
            self._wakeup_handle.cancel()
            self._wakeup_handle = None

    def reset(self) -> None:
        self.cancel()
        self._cancel_wakeup()

        self._locked = False
        self._breached = False

    @_abstractmethod
    def _maybe_lock(self) -> None:  # pragma: no cover # ABC
        """Hook called after a request was allowed to pass without waiting.

        Limiter was unlocked, and we can choose to lock it.
        Subclasses must implement this.
        """

    def __del__(self) -> None:
        """Finalization. Cancel waiters to prevent a deadlock."""
        # No need to touch wakeup, as wakeup holds a strong reference and
        # __del__ won't be called.
        try:
            # Technically this should never happen, where there are waiters
            # without a wakeup scheduled. Means there was a bug in the code.
            waiters = self._waiters

        # Error during initialization before _waiters exists.
        except AttributeError:  # pragma: no cover # Technically a bug.
            return

        any_waiting = False
        for fut in waiters:  # pragma: no cover # Technically a bug.
            if not fut.done():
                fut.cancel()
                any_waiting = True

        # Alert for the bug.
        assert not any_waiting, "__del__ was called with waiters still waiting"

    def close(self) -> None:
        """Close the limiter.

        This will cancel all waiting calls. Limiter is unusable afterwards.
        """
        self.cancel()
        self._cancel_wakeup()


_EVENT_LOOP_FAST_WARNING = (
    "Event loop is too fast. Woke up {} ticks early ({} ms). System will "
    "utilize more CPU than necessary. This warning results from an "
    "inaccurate system clock or a bug in the event loop implementation. "
    "You may safely ignore this warning, but please report it on Github "
    "to help identify the cause."
)


class Limiter(_CommonLimiterMixin):
    """Regular limiter, with a max burst compensating for delayed schedule.

    Takes into account CPU heavy tasks or other delays that can occur while
    the process is sleeping.

    Usage:
        >>> limiter = Limiter(1)
        >>> async def main():
        ...     print_numbers = (foo(i) for i in range(10))
        ...     # This will print the numbers over 10 seconds
        ...     await asyncio.gather(*map(limiter.wrap, print_numbers))

    Alternative usage:
        >>> limiter = Limiter(5)
        >>> async def request():
        ...     await limiter.wait()
        ...     print("Request")  # Do stuff
        >>> async def main():
        ...     # Schedule 5 requests per second.
        ...     await asyncio.gather(*(request() for _ in range(10)))

    Attributes:
        max_burst: In case there's a delay, schedule no more than this many
        calls at once.
        rate: The rate (calls per second) at which the limiter should let
        traffic through.
    """

    def __init__(self, rate: float, *, max_burst: int = 5) -> None:
        """Create a new limiter.

        Args:
            rate: The rate (calls per second) at which calls can pass through.
            max_burst: In case there's a delay, schedule no more than this many
            calls at once.
        """
        super().__init__()
        self._rate = rate
        self._time_between_calls = 1 / rate
        self.max_burst = max_burst

    def __repr__(self) -> str:
        cls = self.__class__
        return f"{cls.__module__}.{cls.__qualname__}(rate={self._rate})"

    @property
    def rate(self) -> float:
        """Calls per second at which the limiter should let traffic through."""
        return self._rate

    @rate.setter
    def rate(self, value: float) -> None:
        """Set the rate (calls per second) at which calls can pass through.

        Args:
            value: The rate (calls per second) at which calls can pass through.
        """
        self._rate = value
        self._time_between_calls = 1 / value

    def _maybe_lock(self) -> None:
        """Lock the limiter as soon a request passes through."""
        self._locked = True
        self._schedule_wakeup()

    def _schedule_wakeup(
        self,
        at: float | None = None,
        *,
        _loop: _asyncio.AbstractEventLoop | None = None,
    ) -> None:
        """Schedule the next wakeup to be unlocked.

        Args:
            at: The time at which to wake up. If None, use the current
            time + 1/rate.
            _loop: The asyncio loop to use. If None, use the current loop. For
            caching purposes.
        """
        loop = _loop or _asyncio.get_running_loop()
        if at is None:
            at = loop.time() + self._time_between_calls
        self._wakeup_handle = loop.call_at(at, self._wakeup)
        # Saving next wakeup and not this wakeup to account for fractions
        # of rate passed. See leftover_time under _wakeup.
        self._next_wakeup = at

    def _wakeup(self) -> None:
        """Advance the limiter counters once."""

        def _unlock() -> None:
            self._wakeup_handle = None
            self._locked = False

        loop = _asyncio.get_running_loop()
        waiters = self._waiters
        # Short circuit if there are no waiters
        if not waiters:
            _unlock()
            return

        this_wakeup = self._next_wakeup
        current_time = loop.time()
        # We woke up early. Damn event loop!
        if current_time < this_wakeup:
            missed_wakeups = 0.0
            # We have a negative leftover bois. Increase the next sleep!
            leftover_time = current_time - this_wakeup
            # More than 1 tick early. Great success.
            # Technically the higher the rate, the more likely the event loop
            # should be late. If we came early on 2 ticks, that's really bad.
            if -leftover_time > self._time_between_calls:
                import warnings

                _warning = _EVENT_LOOP_FAST_WARNING.format(
                    -leftover_time * self.rate, -leftover_time * 1000
                )
                warnings.warn(_warning, ResourceWarning, stacklevel=1)

        else:
            # We woke up too late!
            # Missed wakeups can happen in case of heavy CPU-bound activity,
            # or high event loop load.
            # Check if we overflowed longer than a single call-time.
            missed_wakeups, leftover_time = divmod(
                current_time - this_wakeup, self._time_between_calls
            )

        # Attempt to wake up only the missed wakeups and ones that were
        # inserted while we missed the original wakeup.
        to_wakeup = min(int(missed_wakeups) + 1, self.max_burst)

        while to_wakeup and self._waiters:
            waiter = self._waiters.popleft()
            if waiter.done():  # Might have been cancelled.
                continue
            waiter.set_result(None)
            to_wakeup -= 1

        # All of the waiters were cancelled or we missed wakeups and we're out
        # of waiters. Free to accept traffic.
        if to_wakeup:
            _unlock()

        # If we still have waiters, we need to schedule the next wakeup.
        # If we're out of waiters we still need to wait before
        # unlocking in case a new waiter comes in, as we just
        # let a call through.
        else:
            self._schedule_wakeup(
                at=current_time + self._time_between_calls - leftover_time,
                _loop=loop,
            )


class LeakyBucketLimiter(_CommonLimiterMixin):
    """Leaky bucket compliant with bursts.

    Limits by requests per second according to the
    leaky bucket algorithm. Has a maximum capacity and an initial burst of
    requests.

    Usage:
        >>> limiter = LeakyBucketLimiter(1, capacity=5)
        >>> async def main():
        ...     print_numbers = (foo(i) for i in range(10))
        ...     # This will print the numbers 0,1,2,3,4 immidiately, then
        ...     # wait for a second before each number.
        ...     await asyncio.gather(*map(limiter.wrap, print_numbers))
        ...     # After 5 seconds of inactivity, bucket will drain back to
        ...     # empty.

    Alternative usage:
        >>> limiter = LeakyBucketLimiter(5)  # capacity is 10 by default.
        >>> async def request():
        ...     await limiter.wait()
        ...     print("Request")  # Do stuff
        >>> async def main():
        ...     # First 10 requests would be immediate, then schedule 5
        ...     # requests per second.
        ...     await asyncio.gather(*(request() for _ in range(20)))

    Attributes:
        capacity: The maximum number of requests that can pass through until
        the bucket is full. Defaults to 10.
        rate: The rate (calls per second) at which the bucket should "drain" or
        let calls through.
    """

    capacity: int
    """The maximum number of requests that can pass through until the bucket is
    full."""

    def __init__(self, rate: float, *, capacity: int = 10) -> None:
        """Create a new limiter.

        Args:
            rate: The rate (calls per second) at which calls can pass through
            (or bucket drips).
            capacity: The capacity of the bucket. At full capacity calls to
            wait() will block until the bucket drips.
        """
        super().__init__()
        self._rate = rate
        self._time_between_calls = 1 / rate
        self.capacity = capacity
        self._level = 0

    def __repr__(self) -> str:
        cls = self.__class__
        return (
            f"{cls.__module__}.{cls.__qualname__}(rate={self._rate}, "
            f"capacity={self.capacity})"
        )

    @property
    def rate(self) -> float:
        """Calls per second at which the bucket should "drain" or let calls
        through."""

        return self._rate

    @rate.setter
    def rate(self, value: float) -> None:
        """Set the rate (calls per second) at which bucket should "drain".

        Args:
            value: The rate (calls per second) at which bucket should "drain".
        """
        self._rate = value
        self._time_between_calls = 1 / value

    def _maybe_lock(self) -> None:
        """Increase the level, schedule a drain. Lock when the bucket is full."""
        self._level += 1

        if self._wakeup_handle is None:
            self._schedule_wakeup()

        if self._level >= self.capacity:
            self._locked = True
            return

    def _schedule_wakeup(
        self,
        at: float | None = None,
        *,
        _loop: _asyncio.AbstractEventLoop | None = None,
    ) -> None:
        """Schedule the next wakeup to be unlocked.

        Args:
            at: The time at which to wake up. If None, use the current
            time + 1/rate.
            _loop: The asyncio loop to use. If None, use the current loop. For
            caching purposes.
        """
        loop = _loop or _asyncio.get_running_loop()
        if at is None:
            at = loop.time() + self._time_between_calls
        self._wakeup_handle = loop.call_at(at, self._wakeup)
        self._next_wakeup = at

    def reset(self) -> None:
        """Reset the limiter.

        This will cancel all waiting calls, reset all internal timers, reset
        the bucket to empty and restore the limiter to its initial state.
        Limiter is reusable afterwards, and the next call will be immediately
        scheduled.
        """
        super().reset()
        self._level = 0

    def _wakeup(self) -> None:
        """Drain the bucket at least once. Wakeup waiters if there are any."""
        loop = _asyncio.get_running_loop()
        this_wakeup = self._next_wakeup
        current_time = loop.time()

        # We woke up early. Damn event loop!
        if current_time < this_wakeup:
            missed_drains = 0.0
            # We have a negative leftover bois. Increase the next sleep!
            leftover_time = current_time - this_wakeup
            # More than 1 tick early. Great success.
            # Technically the higher the rate, the more likely the event loop
            # should be late. If we came early on 2 ticks, that's really bad.
            if -leftover_time > self._time_between_calls:
                import warnings

                _warning = _EVENT_LOOP_FAST_WARNING.format(
                    -leftover_time * self.rate, -leftover_time * 1000
                )
                warnings.warn(_warning, ResourceWarning, stacklevel=1)

        else:
            # We woke up too late!
            # Missed wakeups can happen in case of heavy CPU-bound activity,
            # or high event loop load.
            # Check if we overflowed longer than a single call-time.
            missed_drains, leftover_time = divmod(
                current_time - this_wakeup, self._time_between_calls
            )

        capacity = self.capacity
        level = self._level
        # There are no waiters if level is not == capacity.
        # We can decrease without accounting for current level.
        assert missed_drains.is_integer()
        level = max(0, level - int(missed_drains) - 1)
        while (
            level < capacity
            and (waiter := _pop_pending(self._waiters)) is not None
        ):
            waiter.set_result(None)
            level += 1

        # We have no more waiters
        if level < capacity:
            self._locked = False
            self._level = level
            if level == 0:
                return

        time_to_next_drain = self._time_between_calls - leftover_time
        self._schedule_wakeup(at=current_time + time_to_next_drain)


class StrictLimiter(_CommonLimiterMixin):
    """Limits by a maximum number of requests per second.
    Doesn't take CPU or other process sleeps into account.
    There are no bursts to compensate, and the resulting rate will always be
    less than the set limit.

    Attributes:
        rate: The maximum rate (calls per second) at which calls can pass
        through.
    """

    rate: float
    """The maximum rate (calls per second) at which calls can pass through."""

    def __init__(self, rate: float) -> None:
        """Create a new limiter.

        Args:
            rate: The maximum rate (calls per second) at which calls can pass
            through.
        """
        super().__init__()
        self.rate = rate

    def __repr__(self) -> str:
        cls = self.__class__
        return f"{cls.__module__}.{cls.__qualname__}(rate={self.rate})"

    def _maybe_lock(self) -> None:
        """Lock the limiter, schedule a wakeup."""
        self._locked = True
        self._schedule_wakeup()

    def _schedule_wakeup(self) -> None:
        """Schedule the next wakeup to be unlocked."""
        loop = _asyncio.get_running_loop()
        self._wakeup_handle = loop.call_at(
            loop.time() + 1 / self.rate, self._wakeup
        )

    def _wakeup(self) -> None:
        """Wakeup a single waiter if there is any, otherwise unlock."""
        waiter = _pop_pending(self._waiters)
        if waiter is not None:
            waiter.set_result(None)
            self._schedule_wakeup()
        else:
            self._locked = False
            self._wakeup_handle = None

```
changelog.md
# Changelog

All notable changes to this project will be documented in this file.

## [1.1.1] - 2024-12-16

### 🐛 Bug Fixes

- Changed assertion when the event loop was too fast to warning

## [1.1.0.post3] - 2024-09-07

### ⚙️ Miscellaneous Tasks

- Add verified publisher status to pypi (#13)

## [1.1.0.post2] - 2024-09-07

### 📚 Documentation

- Contributing guidelines were added (#12)

### 🎨 Styling

- Allow using the ruff formatter using hatch fmt (#11)

### ⚙️ Miscellaneous Tasks

- Update github action for assets uploading
- Updated trove markers, we're in production. Added some topics too and typing designation.
- Removing the "v" prefix from releases. Utilities using semver fail.
- Recognize "misc" as a changelog marker.
- Hatch can now easily create a development environment. (#10)

## [1.1.0] - 2024-09-07

### 🐛 Bug Fixes

- Mypy will now type hint the package correctly (#9)

### ⚙️ Miscellaneous Tasks

- We are now tracking the changelog using git cliff
- We switched to pyproject.toml and hatch. Also updated to Python 3.11-3.14 as supported versions.

<!-- generated by git-cliff -->

cliff.toml
```.toml
# git-cliff ~ default configuration file
# https://git-cliff.org/docs/configuration
#
# Lines starting with "#" are comments.
# Configuration options are organized into tables and keys.
# See documentation for more information on available options.

[changelog]
# template for the changelog header
header = """
# Changelog\n
All notable changes to this project will be documented in this file.\n
"""
# template for the changelog body
# https://keats.github.io/tera/docs/#introduction
body = """
{% if version %}\
    ## [{{ version | trim_start_matches(pat="v") }}] - {{ timestamp | date(format="%Y-%m-%d") }}
{% else %}\
    ## [unreleased]
{% endif %}\
{% for group, commits in commits | group_by(attribute="group") %}
    ### {{ group | striptags | trim | upper_first }}
    {% for commit in commits %}
        - {% if commit.scope %}*({{ commit.scope }})* {% endif %}\
            {% if commit.breaking %}[**breaking**] {% endif %}\
            {{ commit.message | upper_first }}\
    {% endfor %}
{% endfor %}\n
"""
# template for the changelog footer
footer = """
<!-- generated by git-cliff -->
"""
# remove the leading and trailing s
trim = true
# postprocessors
postprocessors = [
  # { pattern = '<REPO>', replace = "https://github.com/orhun/git-cliff" }, # replace repository URL
]

[git]
# parse the commits based on https://www.conventionalcommits.org
conventional_commits = true
# filter out the commits that are not conventional
filter_unconventional = true
# process each line of a commit as an individual commit
split_commits = false
# regex for preprocessing the commit messages
commit_preprocessors = [
  # Replace issue numbers
  #{ pattern = '\((\w+\s)?#([0-9]+)\)', replace = "([#${2}](<REPO>/issues/${2}))"},
  # Check spelling of the commit with https://github.com/crate-ci/typos
  # If the spelling is incorrect, it will be automatically fixed.
  #{ pattern = '.*', replace_command = 'typos --write-changes -' },
]
# regex for parsing and grouping commits
commit_parsers = [
  { message = "^feat", group = "<!-- 0 -->🚀 Features" },
  { message = "^fix", group = "<!-- 1 -->🐛 Bug Fixes" },
  { message = "^doc", group = "<!-- 3 -->📚 Documentation" },
  { message = "^perf", group = "<!-- 4 -->⚡ Performance" },
  { message = "^refactor", group = "<!-- 2 -->🚜 Refactor" },
  { message = "^style", group = "<!-- 5 -->🎨 Styling" },
  { message = "^test", group = "<!-- 6 -->🧪 Testing" },
  { message = "^chore\\(release\\): prepare for", skip = true },
  { message = "^chore\\(deps.*\\)", skip = true },
  { message = "^chore\\(pr\\)", skip = true },
  { message = "^chore\\(pull\\)", skip = true },
  { message = "^chore|^ci|^misc", group = "<!-- 7 -->⚙️ Miscellaneous Tasks" },
  { body = ".*security", group = "<!-- 8 -->🛡️ Security" },
  { message = "^revert", group = "<!-- 9 -->◀️ Revert" },
]
# filter out the commits that are not matched by commit parsers
filter_commits = false
# sort the tags topologically
topo_order = false
# sort the commits inside sections by oldest/newest order
sort_commits = "oldest"


```
docs/_static/custom.css
```.css
.py .method {
    margin-bottom: 1em;
    margin-top: 1em;
}
```
docs/conf.py
```.py
# test documentation build configuration file, created by
# sphinx-quickstart on Sun Jun 26 00:00:43 2016.
#
# This file is executed through importlib.import_module with
# the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.intersphinx"
]

# Intersphinx extension
intersphinx_mapping = {'python':('http://docs.python.org/3/', None)}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
#
# source_encoding = 'utf-8-sig'

# The master toctree document.
root_doc = 'index'

# General information about the project.
project = 'asynciolimiter'
copyright = '2023, Bar Harel'
author = 'Bar Harel'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '1.0'
# The full version, including alpha/beta/rc tags.
release = '1.0.0'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#
# today = ''
#
# Else, today_fmt is used as the format for a strftime call.
#
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# These patterns also affect html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'
highlight_language = "python3"

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'



# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'logo': 'logo.png',
    'logo_text_align': 'left'
 }
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}
# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.
# "<project> v<release> documentation" by default.
#
# html_title = u'test vtest'

# A shorter title for the navigation bar.  Default is the same as html_title.
#
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#
#html_logo = "_static/logo.png"

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#
# html_extra_path = []

# If not None, a 'Last updated on:' timestamp is inserted at every page
# bottom, using the given strftime format.
# The empty string is equivalent to '%b %d, %Y'.
#
# html_last_updated_fmt = None

# Custom sidebar templates, maps document names to template names.
#
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#
# html_additional_pages = {}

# If false, no module index is generated.
#
# html_domain_indices = True

# If false, no index is generated.
#
# html_use_index = True

# If true, the index is split into individual pages for each letter.
#
# html_split_index = False

# If true, links to the reST sources are added to the pages.
#
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr', 'zh'
#
# html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# 'ja' uses this config value.
# 'zh' user can custom change `jieba` dictionary path.
#
# html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
#
# html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = 'asynciolimiterdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
# latex_documents = [
#     (root_doc, 'test.tex', u'test Documentation',
#      u'test', 'manual'),
# ]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#
# latex_logo = None

# If true, show page references after internal links.
#
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
#
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
#
# latex_appendices = []

# If false, no module index is generated.
#
# latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
# man_pages = [
#     (root_doc, 'test', u'test Documentation',
#      [author], 1)
# ]

# If true, show URL addresses after external links.
#
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
# texinfo_documents = [
#     (root_doc, 'test', u'test Documentation',
#      author, 'test', 'One line description of project.',
#      'Miscellaneous'),
# ]

# Documents to append as an appendix to all manuals.
#
# texinfo_appendices = []

# If false, no module index is generated.
#
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#
# texinfo_no_detailmenu = False

# If false, do not generate in manual @ref nodes.
#
# texinfo_cross_references = False

```
docs/make.bat
```.bat
@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=.
set BUILDDIR=_build

if "%1" == "" goto help

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd

```
pyproject.toml
```.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "asynciolimiter"
dynamic = ["version"]
description = "Rate limiter for Async IO"
readme = "README.md"
authors = [
    { name = "Bar Harel", email = "bzvi7919@gmail.com" }
]
classifiers = [
    "Development Status :: 5 - Production/Stable",

    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",

    "Framework :: AsyncIO",

    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    
    "Topic :: Internet",
    "Topic :: Utilities",
    "Topic :: Software Development :: Libraries",
    
    "Typing :: Typed"
]
keywords = ["rate limiter", "asyncio", "throttling"]
requires-python = ">=3.11"

[project.urls]
Homepage = "https://github.com/bharel/asynciolimiter"
Documentation = "https://asynciolimiter.readthedocs.io/en/latest/"
Source = "https://github.com/bharel/asynciolimiter"
Changelog = "https://github.com/bharel/asynciolimiter/blob/master/changelog.md"

[project.optional-dependencies]
dev = [
    "flake8",
    "isort",
    "mypy",
    "git-cliff",
    "sphinx",
    "sphinx-rtd-theme"
]

[tool.hatch.build.targets.sdist]
packages = ["asynciolimiter"]

[tool.hatch.build.targets.wheel]
packages = ["asynciolimiter"]

[tool.hatch.version]
path = "asynciolimiter/__init__.py"

[tool.ruff]
exclude = ["docs"]
line-length = 79

[tool.ruff.lint]
ignore = ["PT", "S101"]

[tool.hatch.envs.dev]
features = ["dev"]

[tool.mypy]
exclude = ["tests", "docs"]

```
scripts/build.bat
```.bat
pip wheel ..
```
scripts/run_open_coverage.bat
```.bat
@echo off
pushd %~dp0..\
call .\venv\Scripts\activate.bat
coverage run --branch -m unittest tests.py && coverage html && start explorer .\htmlcov\index.html
if NOT ["%errorlevel%"]==["0"] (
    pause
    exit /b %errorlevel%
)
popd
```
scripts/run_tests.bat
```.bat
@echo off
pushd %~dp0..\
call .\venv\Scripts\activate.bat
coverage run --branch -m unittest tests.py && coverage html
if NOT ["%errorlevel%"]==["0"] (
    pause
    exit /b %errorlevel%
)
popd
```
scripts/upload_real.bat
```.bat
twine upload asynciolimiter-*.whl
```
scripts/upload_test.bat
```.bat
twine upload -r testpypi asynciolimiter-*.whl
```
tests/__init__.py
```.py

```
tests/test_limiter.py
```.py
import asyncio
import typing
from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase, skipUnless
from unittest.mock import ANY, Mock, patch

import asynciolimiter
from asynciolimiter import LeakyBucketLimiter, Limiter, StrictLimiter

if typing.TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Awaitable


class PatchLoopMixin(IsolatedAsyncioTestCase):
    """Patch the loop scheduling functions"""

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        asyncio_mock = Mock(wraps=asyncio)
        patcher = patch("asynciolimiter._asyncio", asyncio_mock)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.loop = SimpleNamespace()
        asyncio_mock.get_running_loop.return_value = self.loop
        self.loop.time = Mock(return_value=0)
        self.timer_handler = Mock()
        self.loop.call_at = Mock(return_value=self.timer_handler)
        real_loop = asyncio.get_running_loop()
        self.loop.create_future = real_loop.create_future

    def get_scheduled_functions(self):
        return [call[0][1] for call in self.loop.call_at.call_args_list]

    def get_scheduled_function(self):
        return self.get_scheduled_functions()[-1]


class CommonTestsMixin(PatchLoopMixin, IsolatedAsyncioTestCase):
    limiter: asynciolimiter._BaseLimiter

    def setUp(self) -> None:
        self.waiters_finished = 0
        self.waiters: list[Awaitable] = []
        return super().setUp()

    def call_wakeup(self):
        self.get_scheduled_function()()

    def add_waiter(self):
        def cb(_):
            self.waiters_finished += 1

        task = asyncio.create_task(self.limiter.wait())
        task.add_done_callback(cb)
        self.waiters.append(task)

    def set_time(self, time: float):
        self.loop.time.return_value = time

    def assert_call_at(self, time: float):
        self.assertEqual(self.loop.call_at.call_args_list[-1][0][0], time)

    async def advance_loop(self, count: int = 5):
        for _ in range(count):
            await asyncio.sleep(0)

    def assert_finished(self, count: int):
        self.assertEqual(self.waiters_finished, count)


class LimiterTestCase(
    CommonTestsMixin, PatchLoopMixin, IsolatedAsyncioTestCase
):
    def setUp(self):
        super().setUp()
        self.limiter = Limiter(1 / 3, max_burst=3)

    def test_init_keyword_only(self):
        assert Limiter(1.0, max_burst=5).max_burst == 5
        with self.assertRaises(TypeError):
            Limiter(1.0, 5)

    async def test_wait(self):
        await self.limiter.wait()
        self.loop.call_at.assert_called_once_with(3, ANY)

    async def test_rate_setter(self):
        self.limiter.rate = 1 / 2
        self.assertEqual(self.limiter.rate, 1 / 2)
        self.add_waiter()
        await self.advance_loop()
        self.assert_call_at(2)

    async def test_repr(self):
        self.assertEqual(eval(repr(self.limiter)).rate, self.limiter.rate)

    async def test_wait_multiple(self):
        self.add_waiter()
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.assert_call_at(3)
        self.assert_finished(1)
        self.set_time(3)
        self.call_wakeup()
        await self.advance_loop()
        self.assert_finished(2)
        await self.advance_loop()
        self.assert_call_at(6)
        self.set_time(6)
        self.call_wakeup()
        await self.advance_loop()
        self.assert_finished(3)

    async def test_wait_multiple_cpu_heavy(self):
        self.add_waiter()
        self.add_waiter()
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.assert_call_at(3)
        self.assert_finished(1)
        self.set_time(8)  # Two were supposed to run
        self.call_wakeup()
        await self.advance_loop()
        self.assert_finished(3)
        self.assert_call_at(9)
        self.set_time(9)
        self.call_wakeup()
        await self.advance_loop()
        self.assert_finished(4)

    async def test_early_wakeups(self):
        """Event loop can sometimes wake us too early!

        Expected behavior is to send it a the current pending request a bit
        earlier (only a few microseconds usually) but delay the next one but
        the complementing factor. Should round to a correct wakeup time.
        """
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.assert_call_at(3)
        self.set_time(2)  # Beh.
        self.call_wakeup()  # Wakey wakey!
        await self.advance_loop()
        self.assert_finished(2)
        self.assert_call_at(6)

    @skipUnless(__debug__, "Debug mode only")
    async def test_too_early_wakeups(self):
        """When the wakeup is way too early. Should never happen.

        Fails only on __debug__. Attempts to recover in real time.
        """
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.assert_call_at(3)
        self.set_time(3)  # So far so good
        self.call_wakeup()
        self.add_waiter()
        await self.advance_loop()
        self.assert_finished(2)
        self.assert_call_at(6)
        self.set_time(2)  # Time just went backwards.
        with self.assertWarns(ResourceWarning):
            self.call_wakeup()

    async def test_wait_multiple_max_burst(self):
        for _ in range(5):
            self.add_waiter()
        await self.advance_loop()
        self.assert_call_at(3)
        self.assert_finished(1)
        self.set_time(3 * 10 + 1)
        self.call_wakeup()
        await self.advance_loop()
        self.assert_finished(4)
        self.assert_call_at(3 * 11)
        self.set_time(3 * 11 + 2)
        self.call_wakeup()
        await self.advance_loop()
        self.assert_finished(5)
        self.assert_call_at(3 * 12)
        self.set_time(3 * 12)
        self.call_wakeup()  # Unlocke the limiter
        await self.advance_loop()
        self.assert_finished(5)
        self.add_waiter()  # Unlocked, should immediately finish
        await self.advance_loop()
        self.assert_finished(6)

    async def test_cancelled_waiters(self):
        self.add_waiter()
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.assert_call_at(3)
        self.assert_finished(1)
        self.waiters[1].cancel()
        self.waiters[2].cancel()
        self.add_waiter()
        await self.advance_loop()
        self.set_time(3)
        self.call_wakeup()
        await self.advance_loop()
        self.assert_finished(4)

    async def test_cancel(self):
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.limiter.cancel()
        await self.advance_loop()
        assert self.waiters[1].cancelled()

    async def test_breach(self):
        self.add_waiter()
        self.add_waiter()
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        # Make sure one is cancelled to test breach handing done futures.
        self.waiters[-1].cancel()
        await self.advance_loop(2)
        self.limiter.breach()
        await self.advance_loop()
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.assert_finished(6)

    async def test_reset(self):
        self.limiter.breach()
        self.limiter.reset()
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.assert_finished(1)  # Not breached
        self.limiter.reset()  # Reset cancells all waiters
        await self.advance_loop()
        assert self.waiters[-1].cancelled()
        # Handler cancelled
        self.loop.call_at.return_value.cancel.assert_called_once_with()

    async def test_wrap(self):
        async def coro():
            return 123

        task = asyncio.create_task(self.limiter.wrap(coro()))
        await self.advance_loop()
        self.assertEqual((await task), 123)
        task = asyncio.create_task(self.limiter.wrap(coro()))
        await self.advance_loop()
        self.assertFalse(task.done())
        self.set_time(3)
        self.call_wakeup()
        await self.advance_loop()
        self.assertEqual((await task), 123)

    async def test_close(self):
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.limiter.close()
        await self.advance_loop()
        assert self.waiters[-1].cancelled()
        # Handler cancelled
        self.loop.call_at.return_value.cancel.assert_called_once_with()

    async def test_waiters_cancelled_unlock(self):
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.waiters[1].cancel()
        self.set_time(3)
        self.call_wakeup()
        self.add_waiter()
        # No more wakeups, no waiting on wait() due to unlock
        await self.advance_loop()
        self.assert_finished(3)


class StrictLimiterTestCase(CommonTestsMixin, IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.limiter = StrictLimiter(1 / 3)

    async def test_repr(self):
        self.assertEqual(eval(repr(self.limiter)).rate, self.limiter.rate)

    async def test_wait(self):
        self.add_waiter()
        await self.advance_loop()
        self.loop.call_at.assert_called_once_with(3, ANY)
        self.set_time(3)
        self.call_wakeup()
        # Unlocked.
        self.add_waiter()
        await self.advance_loop()
        self.assert_finished(2)

    async def test_wait_multiple(self):
        self.add_waiter()
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.assert_call_at(3)
        self.assert_finished(1)
        self.set_time(3 * 10 + 1)
        self.call_wakeup()
        await self.advance_loop()
        self.assert_finished(2)
        # Whether 1 second CPU delay or not, always schedule 3 seconds
        # afterwards
        self.assert_call_at(3 * 11 + 1)
        self.set_time(3 * 11 + 2)
        self.call_wakeup()
        await self.advance_loop()
        self.assert_finished(3)


class LeakyBucketLimiterTestCase(CommonTestsMixin, IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.limiter = LeakyBucketLimiter(1 / 3, capacity=3)

    def test_repr(self):
        self.assertEqual(
            eval(repr(self.limiter)).__dict__, self.limiter.__dict__
        )

    async def test_rate_setter(self):
        self.limiter.rate = 1 / 2
        self.assertEqual(self.limiter.rate, 1 / 2)
        self.add_waiter()
        await self.advance_loop()
        self.assert_call_at(2)

    async def test_wait(self):
        await self.limiter.wait()
        self.loop.call_at.assert_called_once_with(3, ANY)
        self.set_time(3)
        self.call_wakeup()
        # Should be empty
        await self.advance_loop()
        # Wasn't rescheduled.
        self.loop.call_at.assert_called_once()

    async def test_wait_multiple(self):
        self.add_waiter()
        self.add_waiter()
        self.add_waiter()
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.waiters[-1].cancel()
        await self.advance_loop()
        self.assert_call_at(3)
        self.assert_finished(4)
        self.set_time(3)
        self.call_wakeup()
        await self.advance_loop()
        self.assert_call_at(3 * 2)
        self.assert_finished(5)
        self.add_waiter()
        await self.advance_loop()
        self.assert_finished(5)  # Still blocked, bucket hasn't drained
        self.add_waiter()
        await self.advance_loop()
        # Bucket drained twice, with 1 second to spare
        self.set_time(3 * 3 + 1)
        self.call_wakeup()
        await self.advance_loop()
        self.assert_finished(7)
        self.assert_call_at(3 * 4)
        self.set_time(3 * 10)  # Bucket fully drained
        self.call_wakeup()
        # Make sure it didn't underflow
        self.add_waiter()
        self.add_waiter()
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.assert_finished(10)  # Last one is queued on a full bucket.
        self.waiters[-1].cancel()

    async def test_wait_max_burst(self):
        for _ in range(10):
            self.add_waiter()
        await self.advance_loop()
        self.assert_finished(3)
        # Very slow CPU operation. So slow the bucket was supposed to be
        # emptied twice
        self.set_time(3 * 10)
        self.call_wakeup()
        await self.advance_loop()
        # Bucket did not empty twice. We kept max to the capacity.
        self.assert_finished(6)
        self.assert_call_at(3 * 11)
        self.set_time(3 * 11)
        self.call_wakeup()
        await self.advance_loop()
        # Continued draining from full.
        self.assert_finished(7)
        self.limiter.cancel()

    async def test_bucket_reset(self):
        for _ in range(2):
            for _ in range(4):
                self.add_waiter()
            await self.advance_loop()
            self.limiter.reset()
        await self.advance_loop()

        # 8 finished, out of them 2 due to reset.
        self.assert_finished(8)
        self.assertEqual(sum(fut.cancelled() for fut in self.waiters), 2)

    async def test_bucket_empty(self):
        """Doesn't reschedule when empty"""
        self.add_waiter()
        await self.advance_loop()
        self.assert_call_at(3)
        self.set_time(3)
        self.call_wakeup()
        await self.advance_loop()
        self.loop.call_at.assert_called_once()  # Wasn't called again.

    async def test_bucket_drain_once(self):
        """Drains the bucket once, make sure it reschedules for next."""
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.set_time(3)
        self.call_wakeup()
        await self.advance_loop()
        self.assert_call_at(3 * 2)

    async def test_early_wakeups(self):
        """Event loop can sometimes wake us too early!

        Expected behavior is to drain a bit earlier (only a few microseconds
        usually) but delay the next one but the complementing factor. Should
        round to a correct drain time.
        """
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.assert_call_at(3)
        self.set_time(2)  # Beh.
        self.call_wakeup()  # Wakey wakey!
        await self.advance_loop()
        self.assert_finished(2)
        self.assert_call_at(6)

    @skipUnless(__debug__, "Debug mode only")
    async def test_too_early_wakeups(self):
        """When the wakeup is way too early. Should never happen.

        Fails only on __debug__. Attempts to recover in real time.
        """
        self.add_waiter()
        self.add_waiter()
        await self.advance_loop()
        self.assert_call_at(3)
        self.set_time(3)  # So far so good
        self.call_wakeup()
        await self.advance_loop()
        self.assert_finished(2)
        self.assert_call_at(6)
        self.set_time(2)  # Time just went backwards.
        with self.assertWarns(ResourceWarning):
            self.call_wakeup()

```

## https://github.com/twardoch/twat-mp

Token Usage:
GitHub Tokens: 12655
LLM Input Tokens: 0
LLM Output Tokens: 0
Total Tokens: 12655

FileTree:
.github/workflows/push.yml
.github/workflows/release.yml
.gitignore
.pre-commit-config.yaml
LOG.md
README.md
VERSION.txt
cleanup.py
pyproject.toml
src/twat_mp/__init__.py
src/twat_mp/mp.py
tests/test_benchmark.py
tests/test_twat_mp.py

Analysis:
.github/workflows/push.yml
```.yml
name: Build & Test

on:
  push:
    branches: [main]
    tags-ignore: ["v*"]
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: write
  id-token: write

# Ensure that only one run per branch/commit is active at once.
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  # === QUALITY JOB: Lint and format checks ===
  quality:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Ruff lint
        uses: astral-sh/ruff-action@v3
        with:
          version: "latest"
          args: "check --output-format=github"

      - name: Run Ruff Format
        uses: astral-sh/ruff-action@v3
        with:
          version: "latest"
          args: "format --check --respect-gitignore"

  # === TEST JOB: Run tests ===
  test:
    name: Run Tests
    needs: quality
    strategy:
      matrix:
        python-version: ["3.12"]
        os: [ubuntu-latest]
      fail-fast: true
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
          python-version: ${{ matrix.python-version }}
          enable-cache: true
          cache-suffix: ${{ matrix.os }}-${{ matrix.python-version }}

      - name: Install test dependencies
        run: |
          uv pip install --system --upgrade pip
          uv pip install --system ".[test]"

      - name: Run tests with Pytest
        run: uv run pytest -n auto --maxfail=1 --disable-warnings --cov-report=xml --cov-config=pyproject.toml --cov=src/twat_mp --cov=tests tests/

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-${{ matrix.python-version }}-${{ matrix.os }}
          path: coverage.xml

  # === BUILD JOB: Create distribution artifacts ===
  build:
    name: Build Distribution
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
          python-version: "3.12"
          enable-cache: true

      - name: Install build tools
        run: uv pip install build hatchling hatch-vcs

      - name: Build distributions
        run: uv run python -m build --outdir dist

      - name: Upload distribution artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist-files
          path: dist/
          retention-days: 5

```
.github/workflows/release.yml
```.yml
name: Release

on:
  push:
    tags: ["v*"]

permissions:
  contents: write
  id-token: write

jobs:
  release:
    name: Release to PyPI
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/twat-mp
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
          python-version: "3.12"
          enable-cache: true

      - name: Install build tools
        run: uv pip install build hatchling hatch-vcs

      - name: Build distributions
        run: uv run python -m build --outdir dist

      - name: Verify distribution files
        run: |
          ls -la dist/
          test -n "$(find dist -name '*.whl')" || (echo "Wheel file missing" && exit 1)
          test -n "$(find dist -name '*.tar.gz')" || (echo "Source distribution missing" && exit 1)

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_TOKEN }}

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

```
.gitignore
```.gitignore
*_autogen/
.DS_Store
__version__.py
__pycache__/
_Chutzpah*
_deps
_NCrunch_*
_pkginfo.txt
_Pvt_Extensions
_ReSharper*/
_TeamCity*
_UpgradeReport_Files/
!?*.[Cc]ache/
!.axoCover/settings.json
!.vscode/extensions.json
!.vscode/launch.json
!.vscode/settings.json
!.vscode/tasks.json
!**/[Pp]ackages/build/
!Directory.Build.rsp
.*crunch*.local.xml
.axoCover/*
.builds
.cr/personal
.fake/
.history/
.ionide/
.localhistory/
.mfractor/
.ntvs_analysis.dat
.paket/paket.exe
.sass-cache/
.vs/
.vscode
.vscode/*
.vshistory/
[Aa][Rr][Mm]/
[Aa][Rr][Mm]64/
[Bb]in/
[Bb]uild[Ll]og.*
[Dd]ebug/
[Dd]ebugPS/
[Dd]ebugPublic/
[Ee]xpress/
[Ll]og/
[Ll]ogs/
[Oo]bj/
[Rr]elease/
[Rr]eleasePS/
[Rr]eleases/
[Tt]est[Rr]esult*/
[Ww][Ii][Nn]32/
*_h.h
*_i.c
*_p.c
*_wpftmp.csproj
*- [Bb]ackup ([0-9]).rdl
*- [Bb]ackup ([0-9][0-9]).rdl
*- [Bb]ackup.rdl
*.[Cc]ache
*.[Pp]ublish.xml
*.[Rr]e[Ss]harper
*.a
*.app
*.appx
*.appxbundle
*.appxupload
*.aps
*.azurePubxml
*.bim_*.settings
*.bim.layout
*.binlog
*.btm.cs
*.btp.cs
*.build.csdef
*.cab
*.cachefile
*.code-workspace
*.coverage
*.coveragexml
*.d
*.dbmdl
*.dbproj.schemaview
*.dll
*.dotCover
*.DotSettings.user
*.dsp
*.dsw
*.dylib
*.e2e
*.exe
*.gch
*.GhostDoc.xml
*.gpState
*.ilk
*.iobj
*.ipdb
*.jfm
*.jmconfig
*.la
*.lai
*.ldf
*.lib
*.lo
*.log
*.mdf
*.meta
*.mm.*
*.mod
*.msi
*.msix
*.msm
*.msp
*.ncb
*.ndf
*.nuget.props
*.nuget.targets
*.nupkg
*.nvuser
*.o
*.obj
*.odx.cs
*.opendb
*.opensdf
*.opt
*.out
*.pch
*.pdb
*.pfx
*.pgc
*.pgd
*.pidb
*.plg
*.psess
*.publishproj
*.publishsettings
*.pubxml
*.pyc
*.rdl.data
*.rptproj.bak
*.rptproj.rsuser
*.rsp
*.rsuser
*.sap
*.sbr
*.scc
*.sdf
*.sln.docstates
*.sln.iml
*.slo
*.smod
*.snupkg
*.so
*.suo
*.svclog
*.tlb
*.tlh
*.tli
*.tlog
*.tmp
*.tmp_proj
*.tss
*.user
*.userosscache
*.userprefs
*.vbp
*.vbw
*.VC.db
*.VC.VC.opendb
*.VisualState.xml
*.vsp
*.vspscc
*.vspx
*.vssscc
*.xsd.cs
**/[Pp]ackages/*
**/*.DesktopClient/GeneratedArtifacts
**/*.DesktopClient/ModelManifest.xml
**/*.HTMLClient/GeneratedArtifacts
**/*.Server/GeneratedArtifacts
**/*.Server/ModelManifest.xml
*~
~$*
$tf/
AppPackages/
artifacts/
ASALocalRun/
AutoTest.Net/
Backup*/
BenchmarkDotNet.Artifacts/
bld/
BundleArtifacts/
ClientBin/
cmake_install.cmake
CMakeCache.txt
CMakeFiles
CMakeLists.txt.user
CMakeScripts
CMakeUserPresets.json
compile_commands.json
coverage*.info
coverage*.json
coverage*.xml
csx/
CTestTestfile.cmake
dlldata.c
DocProject/buildhelp/
DocProject/Help/*.hhc
DocProject/Help/*.hhk
DocProject/Help/*.hhp
DocProject/Help/*.HxC
DocProject/Help/*.HxT
DocProject/Help/html
DocProject/Help/Html2
ecf/
FakesAssemblies/
FodyWeavers.xsd
Generated_Code/
Generated\ Files/
healthchecksdb
install_manifest.txt
ipch/
Makefile
MigrationBackup/
mono_crash.*
nCrunchTemp_*
node_modules/
nunit-*.xml
OpenCover/
orleans.codegen.cs
Package.StoreAssociation.xml
paket-files/
project.fragment.lock.json
project.lock.json
publish/
PublishScripts/
rcf/
ScaffoldingReadMe.txt
ServiceFabricBackup/
StyleCopReport.xml
Testing
TestResult.xml
UpgradeLog*.htm
UpgradeLog*.XML
x64/
x86/
# Python coverage
.coverage
.coverage.*
htmlcov/
coverage.xml
.pytest_cache/
.benchmarks/

_private

```
.pre-commit-config.yaml
```.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
        args: [--respect-gitignore]
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-added-large-files
      - id: debug-statements
      - id: check-case-conflict
      - id: mixed-line-ending
        args: [--fix=lf]

```
LOG.md
---
this_file: LOG.md
---

# Changelog

All notable changes to the `twat-mp` project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.7.5] - 2025-02-15
### Changed
- Optimized CI/CD pipeline with improved GitHub Actions workflow
- Enhanced stability and performance optimizations in core multiprocessing functions
- Updated documentation and README with clearer usage examples

## [1.7.3] - 2025-02-15
### Changed
- Refined GitHub Actions release workflow
- Minor improvements to error handling in process pools
- Documentation updates for better clarity

## [1.7.0] - 2025-02-13
### Added
- Major overhaul of GitHub Actions workflows
- Improved process pool management with better resource handling
- Enhanced thread pool capabilities with optimized performance
### Changed
- Significant updates to pyproject.toml configuration
- Improved test coverage and benchmarking

## [1.6.2] - 2025-02-06
### Fixed
- Bug fixes in process pool resource management
- Enhanced stability for parallel processing operations
### Added
- Pre-commit hooks configuration for better code quality

## [1.6.0] - 2025-02-06
### Added
- Significant improvements to parallel processing capabilities
- Enhanced pool management with better resource cleanup
- New GitHub Actions workflow for automated releases
### Changed
- Major updates to project configuration and dependencies
- Improved documentation and examples

## [1.2.5] - 2025-02-06
### Changed
- Stability improvements in core multiprocessing functions
- Minor bug fixes and code cleanup
- Enhanced test coverage

## [1.2.1] - 2025-02-05
### Added
- Enhanced error handling in pool operations
- Improved documentation with better examples
### Changed
- Refined project structure and organization

## [1.1.0] - 2025-02-03
### Added
- First feature update after initial release
- Improved parallel processing utilities with better performance
- Enhanced pool management capabilities
### Changed
- Updated project dependencies and requirements

## [1.0.10] - 2025-02-05
### Fixed
- Various bug fixes in core functionality
- Enhanced stability of pool operations
### Changed
- Minor documentation improvements

## [1.0.0] - 2025-02-05
### Added
- Initial release of twat-mp
- Basic parallel processing utilities using Pathos library
- Process and Thread pool implementations with context managers
- Map decorators (amap, imap, pmap) for different parallel processing patterns
- Automatic CPU core detection for optimal performance
- Type hints and modern Python features throughout the codebase
- Comprehensive documentation and usage examples
### Changed
- Updated license year to 2025

[1.7.5]: https://github.com/twardoch/twat-mp/compare/v1.7.3...v1.7.5
[1.7.3]: https://github.com/twardoch/twat-mp/compare/v1.7.0...v1.7.3
[1.7.0]: https://github.com/twardoch/twat-mp/compare/v1.6.2...v1.7.0
[1.6.2]: https://github.com/twardoch/twat-mp/compare/v1.6.0...v1.6.2
[1.6.0]: https://github.com/twardoch/twat-mp/compare/v1.2.5...v1.6.0
[1.2.5]: https://github.com/twardoch/twat-mp/compare/v1.2.1...v1.2.5
[1.2.1]: https://github.com/twardoch/twat-mp/compare/v1.1.0...v1.2.1
[1.1.0]: https://github.com/twardoch/twat-mp/compare/v1.0.10...v1.1.0
[1.0.10]: https://github.com/twardoch/twat-mp/compare/v1.0.0...v1.0.10
[1.0.0]: https://github.com/twardoch/twat-mp/releases/tag/v1.0.0

README.md
# twat-mp

(work in progress)

Parallel processing utilities using the Pathos multiprocessing library. This package provides convenient context managers and decorators for parallel processing, with both process-based and thread-based pools.

## Features

* Context managers for both process and thread pools:
  + `ProcessPool`: For CPU-intensive parallel processing
  + `ThreadPool`: For I/O-bound parallel processing
* Decorators for common parallel mapping operations:
  + `amap`: Asynchronous parallel map with automatic result retrieval
  + `imap`: Lazy parallel map returning an iterator
  + `pmap`: Standard parallel map (eager evaluation)
* Automatic CPU core detection for optimal pool sizing
* Clean resource management with context managers
* Full type hints and modern Python features
* Flexible pool configuration with customizable worker count

## Installation

```bash
pip install twat-mp
```

## Usage

### Using Process and Thread Pools

The package provides dedicated context managers for both process and thread pools:

```python
from twat_mp import ProcessPool, ThreadPool

# For CPU-intensive operations
with ProcessPool() as pool:
    results = pool.map(lambda x: x * x, range(10))
    print(list(results))  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# For I/O-bound operations
with ThreadPool() as pool:
    results = pool.map(lambda x: x * 2, range(10))
    print(list(results))  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Custom number of workers
with ProcessPool(nodes=4) as pool:
    results = pool.map(lambda x: x * x, range(10))
```

### Using Map Decorators

The package provides three decorators for different mapping strategies:

```python
from twat_mp import amap, imap, pmap

# Standard parallel map (eager evaluation)
@pmap
def square(x: int) -> int:
    return x * x

results = list(square(range(10)))
print(results)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Lazy parallel map (returns iterator)
@imap
def cube(x: int) -> int:
    return x * x * x

for result in cube(range(5)):
    print(result)  # Prints results as they become available

# Asynchronous parallel map with automatic result retrieval
@amap
def double(x: int) -> int:
    return x * 2

results = list(double(range(10)))
print(results)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

### Function Composition

Decorators can be composed for complex parallel operations:

```python
from twat_mp import amap

@amap
def compute_intensive(x: int) -> int:
    result = x
    for _ in range(1000):  # Simulate CPU-intensive work
        result = (result * x + x) % 10000
    return result

@amap
def io_intensive(x: int) -> int:
    import time
    time.sleep(0.001)  # Simulate I/O wait
    return x * 2

# Chain parallel operations
results = list(io_intensive(compute_intensive(range(100))))
```

## Dependencies

* `pathos`: For parallel processing functionality

## Development

To set up the development environment:

```bash
# Install in development mode with test dependencies
uv pip install -e ".[test]"

# Run tests
python -m pytest tests/

# Run benchmarks
python -m pytest tests/test_benchmark.py
```

## License

MIT License
.

VERSION.txt
```.txt
v1.8.1

```
cleanup.py
```.py
#!/usr/bin/env -S uv run -s
# /// script
# dependencies = [
#   "ruff>=0.9.6",
#   "pytest>=8.3.4",
#   "mypy>=1.15.0",
# ]
# ///
# this_file: cleanup.py

"""
Cleanup tool for managing repository tasks and maintaining code quality.

This script provides a comprehensive set of commands for repository maintenance:

When to use each command:

- `cleanup.py status`: Use this FIRST when starting work to check the current state
  of the repository. It shows file structure, git status, and runs all code quality
  checks. Run this before making any changes to ensure you're starting from a clean state.

- `cleanup.py venv`: Run this when setting up the project for the first time or if
  your virtual environment is corrupted/missing. Creates a new virtual environment
  using uv.

- `cleanup.py install`: Use after `venv` or when dependencies have changed. Installs
  the package and all development dependencies in editable mode.

- `cleanup.py update`: Run this when you've made changes and want to commit them.
  It will:
  1. Show current status (like `status` command)
  2. Stage and commit any changes with a generic message
  Use this for routine maintenance commits.

- `cleanup.py push`: Run this after `update` when you want to push your committed
  changes to the remote repository.

Workflow Example:
1. Start work: `cleanup.py status`
2. Make changes to code
3. Commit changes: `cleanup.py update`
4. Push to remote: `cleanup.py push`

The script maintains a CLEANUP.log file that records all operations with timestamps.
It also includes content from README.md at the start and TODO.md at the end of logs
for context.

Required Files:
- LOG.md: Project changelog
- README.md: Project documentation
- TODO.md: Pending tasks and future plans
"""

import subprocess
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import NoReturn

# Configuration
IGNORE_PATTERNS = [
    ".git",
    ".venv",
    "__pycache__",
    "*.pyc",
    "dist",
    "build",
    "*.egg-info",
]
REQUIRED_FILES = ["LOG.md", ".cursor/rules/0project.mdc", "TODO.md"]
LOG_FILE = Path("CLEANUP.log")

# Ensure we're working from the script's directory
os.chdir(Path(__file__).parent)


def new() -> None:
    """Remove existing log file."""
    if LOG_FILE.exists():
        LOG_FILE.unlink()


def prefix() -> None:
    """Write README.md content to log file."""
    readme = Path(".cursor/rules/0project.mdc")
    if readme.exists():
        log_message("\n=== PROJECT STATEMENT ===")
        content = readme.read_text()
        log_message(content)


def suffix() -> None:
    """Write TODO.md content to log file."""
    todo = Path("TODO.md")
    if todo.exists():
        log_message("\n=== TODO.md ===")
        content = todo.read_text()
        log_message(content)


def log_message(message: str) -> None:
    """Log a message to file and console with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} - {message}\n"
    with LOG_FILE.open("a") as f:
        f.write(log_line)


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        if result.stdout:
            log_message(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        log_message(f"Command failed: {' '.join(cmd)}")
        log_message(f"Error: {e.stderr}")
        if check:
            raise
        return subprocess.CompletedProcess(cmd, 1, "", str(e))


def check_command_exists(cmd: str) -> bool:
    """Check if a command exists in the system."""
    try:
        subprocess.run(["which", cmd], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


class Cleanup:
    """Main cleanup tool class."""

    def __init__(self) -> None:
        self.workspace = Path.cwd()

    def _print_header(self, message: str) -> None:
        """Print a section header."""
        log_message(f"\n=== {message} ===")

    def _check_required_files(self) -> bool:
        """Check if all required files exist."""
        missing = False
        for file in REQUIRED_FILES:
            if not (self.workspace / file).exists():
                log_message(f"Error: {file} is missing")
                missing = True
        return not missing

    def _generate_tree(self) -> None:
        """Generate and display tree structure of the project."""
        if not check_command_exists("tree"):
            log_message("Warning: 'tree' command not found. Skipping tree generation.")
            return None

        try:
            # Create/overwrite the file with YAML frontmatter
            rules_dir = Path(".cursor/rules")
            rules_dir.mkdir(parents=True, exist_ok=True)
            # Get tree output
            tree_result = run_command(
                ["tree", "-a", "-I", ".git", "--gitignore", "-n", "-h", "-I", "*_cache"]
            )
            tree_text = tree_result.stdout
            # Write frontmatter and tree output to file
            with open(rules_dir / "filetree.mdc", "w") as f:
                f.write("---\ndescription: File tree of the project\nglobs: \n---\n")
                f.write(tree_text)

            # Log the contents
            log_message("\nProject structure:")
            log_message(tree_text)

        except Exception as e:
            log_message(f"Failed to generate tree: {e}")
        return None

    def _git_status(self) -> bool:
        """Check git status and return True if there are changes."""
        result = run_command(["git", "status", "--porcelain"], check=False)
        return bool(result.stdout.strip())

    def _venv(self) -> None:
        """Create and activate virtual environment using uv."""
        log_message("Setting up virtual environment")
        try:
            run_command(["uv", "venv"])
            # Activate the virtual environment
            venv_path = self.workspace / ".venv" / "bin" / "activate"
            if venv_path.exists():
                os.environ["VIRTUAL_ENV"] = str(self.workspace / ".venv")
                os.environ["PATH"] = (
                    f"{self.workspace / '.venv' / 'bin'}{os.pathsep}{os.environ['PATH']}"
                )
                log_message("Virtual environment created and activated")
            else:
                log_message("Virtual environment created but activation failed")
        except Exception as e:
            log_message(f"Failed to create virtual environment: {e}")

    def _install(self) -> None:
        """Install package in development mode with all extras."""
        log_message("Installing package with all extras")
        try:
            self._venv()
            run_command(["uv", "pip", "install", "-e", ".[test,dev]"])
            log_message("Package installed successfully")
        except Exception as e:
            log_message(f"Failed to install package: {e}")

    def _run_checks(self) -> None:
        """Run code quality checks using ruff and pytest."""
        log_message("Running code quality checks")

        try:
            # Run ruff checks
            log_message(">>> Running code fixes...")
            run_command(
                [
                    "python",
                    "-m",
                    "ruff",
                    "check",
                    "--fix",
                    "--unsafe-fixes",
                    "src",
                    "tests",
                ],
                check=False,
            )
            run_command(
                [
                    "python",
                    "-m",
                    "ruff",
                    "format",
                    "--respect-gitignore",
                    "src",
                    "tests",
                ],
                check=False,
            )

            # Run type checks
            log_message(">>>Running type checks...")
            run_command(["python", "-m", "mypy", "src", "tests"], check=False)

            # Run tests
            log_message(">>> Running tests...")
            run_command(["python", "-m", "pytest", "tests"], check=False)

            log_message("All checks completed")
        except Exception as e:
            log_message(f"Failed during checks: {e}")

    def status(self) -> None:
        """Show current repository status: tree structure, git status, and run checks."""
        prefix()  # Add README.md content at start
        self._print_header("Current Status")

        # Check required files
        self._check_required_files()

        # Show tree structure
        self._generate_tree()

        # Show git status
        result = run_command(["git", "status"], check=False)
        log_message(result.stdout)

        # Run additional checks
        self._print_header("Environment Status")
        self._venv()
        self._install()
        self._run_checks()

        suffix()  # Add TODO.md content at end

    def venv(self) -> None:
        """Create and activate virtual environment."""
        self._print_header("Virtual Environment Setup")
        self._venv()

    def install(self) -> None:
        """Install package with all extras."""
        self._print_header("Package Installation")
        self._install()

    def update(self) -> None:
        """Show status and commit any changes if needed."""
        # First show current status
        self.status()

        # Then handle git changes if any
        if self._git_status():
            log_message("Changes detected in repository")
            try:
                # Add all changes
                run_command(["git", "add", "."])
                # Commit changes
                commit_msg = "Update repository files"
                run_command(["git", "commit", "-m", commit_msg])
                log_message("Changes committed successfully")
            except Exception as e:
                log_message(f"Failed to commit changes: {e}")
        else:
            log_message("No changes to commit")

    def push(self) -> None:
        """Push changes to remote repository."""
        self._print_header("Pushing Changes")
        try:
            run_command(["git", "push"])
            log_message("Changes pushed successfully")
        except Exception as e:
            log_message(f"Failed to push changes: {e}")


def print_usage() -> None:
    """Print usage information."""
    log_message("Usage:")
    log_message("  cleanup.py status   # Show current status and run all checks")
    log_message("  cleanup.py venv     # Create virtual environment")
    log_message("  cleanup.py install  # Install package with all extras")
    log_message("  cleanup.py update   # Update and commit changes")
    log_message("  cleanup.py push     # Push changes to remote")


def main() -> NoReturn:
    """Main entry point."""
    new()  # Clear log file

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]
    cleanup = Cleanup()

    try:
        if command == "status":
            cleanup.status()
        elif command == "venv":
            cleanup.venv()
        elif command == "install":
            cleanup.install()
        elif command == "update":
            cleanup.update()
        elif command == "push":
            cleanup.push()
        else:
            print_usage()
            sys.exit(1)
    except Exception as e:
        log_message(f"Error: {e}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()

```
pyproject.toml
```.toml
# this_file: twat_mp/pyproject.toml

# this_file: twat_mp/pyproject.toml

# Build System Configuration
# -------------------------
# Specifies the build system and its requirements for packaging the project
# Specifies the build backend and its requirements for building the package
[build-system]
requires = [
    "hatchling>=1.27.0",     # Core build backend for Hatch
    "hatch-vcs>=0.4.0",      # Version Control System plugin for Hatch
]
build-backend = "hatchling.build"  # Use Hatchling as the build backend

# Project Metadata Configuration
# ------------------------------
# Comprehensive project description, requirements, and compatibility information
[project]
name = "twat-mp"
dynamic = ["version"]  # Version is determined dynamically from VCS
description = "Parallel processing utilities using Pathos mpprocessing library"
readme = "README.md"
requires-python = ">=3.10"  # Minimum Python version required
license = "MIT"
keywords = ["parallel", "mpprocessing", "pathos", "map", "pool"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]

# Runtime Dependencies
# -------------------
# External packages required for the project to function
dependencies = [
    "pathos>=0.3.0",         # Parallel processing library
    "twat>=1.8.1",           # Main twat package
]

[[project.authors]]
name = "Adam Twardoch"
email = "adam+github@twardoch.com"

[project.urls]
Documentation = "https://github.com/twardoch/twat-mp#readme"
Issues = "https://github.com/twardoch/twat-mp/issues"
Source = "https://github.com/twardoch/twat-mp"

[project.entry-points."twat.plugins"]
mp = "twat_mp"

[tool.hatch.build.targets.wheel]
packages = ["src/twat_mp"]

[tool.hatch.version]
source = "vcs"

[tool.hatch.version.raw-options]
version_scheme = "post-release"

[tool.hatch.build.hooks.vcs]
version-file = "src/twat_mp/__version__.py"

[tool.hatch.envs.default]
dependencies = ["mypy>=1.0.0", "ruff>=0.1.0"]

[project.optional-dependencies]
test = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-benchmark[histogram]>=4.0.0",
    "pytest-xdist>=3.5.0",                # For parallel test execution
    "pandas>=2.0.0",                      # Required by some test dependencies
    "numpy>=1.24.0",                      # Required by pandas
    "matplotlib>=3.7.0",                  # For benchmark visualization

]

dev = ["pre-commit>=3.6.0"]

all = ["twat>=1.0.0", "pathos>=0.3.0"]

[tool.hatch.envs.test]
dependencies = [".[test]"]

[tool.hatch.envs.test.scripts]
# Regular tests can run in parallel
test = "python -m pytest -n auto {args:tests}"
test-cov = "python -m pytest -n auto --cov-report=term-missing --cov-config=pyproject.toml --cov=src/twat_mp --cov=tests {args:tests}"
# Benchmarks must run sequentially
bench = "python -m pytest -v -p no:briefcase tests/test_benchmark.py --benchmark-only"
bench-save = "python -m pytest -v -p no:briefcase tests/test_benchmark.py --benchmark-only --benchmark-json=benchmark/results.json"
bench-hist = "python -m pytest -v -p no:briefcase tests/test_benchmark.py --benchmark-only --benchmark-histogram=benchmark/hist"
bench-compare = "python -m pytest-benchmark compare benchmark/results.json --sort fullname --group-by func"

[tool.hatch.envs.lint]
detached = true
dependencies = ["black>=23.1.0", "mypy>=1.0.0", "ruff>=0.1.0"]

[tool.hatch.envs.lint.scripts]
typing = "mypy --install-types --non-interactive {args:src/twat_mp tests}"
style = ["ruff check {args:.}", "ruff format {args:.}"]
fmt = ["ruff format {args:.}", "ruff check --fix {args:.}"]
all = ["style", "typing"]

[tool.ruff]
target-version = "py310"
line-length = 88
lint.extend-select = [
    "I",   # isort
    "N",   # pep8-naming
    "B",   # flake8-bugbear
    "RUF", # Ruff-specific rules
]
lint.ignore = [
    "ARG001", # Unused function argument
    "E501",   # Line too long
    "I001",
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "lf"

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]

[tool.coverage.run]
source_pkgs = ["twat_mp", "tests"]
branch = true
parallel = true
omit = ["src/twat_mp/__about__.py"]

[tool.coverage.paths]
twat_mp = ["src/twat_mp", "*/twat-mp/src/twat_mp"]
tests = ["tests", "*/twat-mp/tests"]

[tool.coverage.report]
exclude_lines = ["no cov", "if __name__ == .__main__.:", "if TYPE_CHECKING:"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true

[tool.pytest.ini_options]
markers = ["benchmark: marks tests as benchmarks (select with '-m benchmark')"]
addopts = "-v -p no:briefcase"
testpaths = ["tests"]
python_files = ["test_*.py"]
filterwarnings = ["ignore::DeprecationWarning", "ignore::UserWarning"]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"

[tool.pytest-benchmark]
min_rounds = 100
min_time = 0.1
histogram = true
storage = "file"
save-data = true
compare = [
    "min",    # Minimum time
    "max",    # Maximum time
    "mean",   # Mean time
    "stddev", # Standard deviation
    "median", # Median time
    "iqr",    # Inter-quartile range
    "ops",    # Operations per second
    "rounds", # Number of rounds

]

```
src/twat_mp/__init__.py
```.py
from twat_mp.__version__ import version as __version__
from twat_mp.mp import MultiPool, ProcessPool, ThreadPool, amap, imap, mmap, pmap

__all__ = [
    "MultiPool",
    "ProcessPool",
    "ThreadPool",
    "__version__",
    "amap",
    "imap",
    "mmap",
    "pmap",
]

```
src/twat_mp/mp.py
```.py
"""
Parallel processing utilities using the Pathos multiprocessing library.

This module provides convenient context managers for creating and managing
parallel processing pools (process or thread based) and decorators for applying
parallel map operations to functions. It uses Pathos pools under the hood,
automatically determining the optimal number of processes/threads based on the
system's CPU count if not specified.

Example usage:
    >>> from mp import pmap, imap, amap, ProcessPool, ThreadPool
    >>>
    >>> # Using the parallel map decorator (synchronous mapping)
    >>> @pmap
    ... def square(x: int) -> int:
    ...     return x * x
    >>>
    >>> results = list(square(range(10)))
    >>> print(results)
    [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
"""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Literal, TypeVar

from pathos.helpers import mp  # Provides CPU count helper
from pathos.pools import ProcessPool as PathosProcessPool
from pathos.pools import ThreadPool as PathosThreadPool

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

# Type variables for generality in mapping functions
T = TypeVar("T")
U = TypeVar("U")

# Define a union type for either a process pool or a thread pool from Pathos
PathosPool = PathosProcessPool | PathosThreadPool
"""Type alias for either a ProcessPool or ThreadPool from Pathos."""


class MultiPool:
    """
    Context manager for managing Pathos parallel processing pools.

    This class abstracts the creation and cleanup of a parallel processing pool.
    It automatically chooses the number of nodes (processes or threads) based on
    the CPU count if not provided. It can be subclassed for specific pool types.

    Attributes:
        pool_class: The Pathos pool class to instantiate.
        nodes: The number of processes/threads to use.
        pool: The actual pool instance (created on entering the context).

    Example:
        >>> with MultiPool(pool_class=PathosProcessPool) as pool:
        ...     results = pool.map(lambda x: x * 2, range(5))
        >>> print(list(results))
    """

    def __init__(
        self, pool_class: type[PathosPool] = PathosProcessPool, nodes: int | None = None
    ) -> None:
        """
        Initialize the MultiPool context manager.

        Args:
            pool_class: The pool class to use (ProcessPool or ThreadPool).
            Defaults to ProcessPool.
            nodes: The number of processes/threads to create.
            If None, uses the CPU count.
        """
        self.pool_class = pool_class
        # If nodes is not specified, determine optimal number based on CPU count.
        self.nodes: int = nodes if nodes is not None else mp.cpu_count()  # type: ignore
        self.pool: PathosPool | None = None  # Pool will be created in __enter__

    def __enter__(self) -> PathosPool:
        """
        Enter the runtime context and create the pool.

        Returns:
            The instantiated pool object.

        Raises:
            RuntimeError: If pool creation fails.
        """
        self.pool = self.pool_class(nodes=self.nodes)
        if self.pool is None:
            # This should rarely happen; raise an error if pool instantiation fails.
            msg = f"Failed to create a pool using {self.pool_class}"
            raise RuntimeError(msg)
        return self.pool

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> Literal[False]:
        """
        Exit the runtime context, ensuring the pool is properly closed and resources are freed.

        Args:
            exc_type: The exception type if an exception was raised.
            exc_value: The exception value if an exception was raised.
            traceback: The traceback if an exception was raised.

        Returns:
            False to indicate that any exception should be propagated.
        """
        if self.pool:
            # Close the pool and join to wait for all tasks to complete
            self.pool.close()
            self.pool.join()
            # Clear the pool to free up resources
            self.pool.clear()
        return False  # Propagate any exception that occurred


class ProcessPool(MultiPool):
    """
    Context manager specifically for creating a process-based pool.

    This subclass of MultiPool defaults to using the ProcessPool from Pathos.

    Example:
        >>> with ProcessPool() as pool:
        ...     results = pool.map(lambda x: x * 2, range(10))
    """

    def __init__(self, nodes: int | None = None) -> None:
        """
        Initialize a ProcessPool with an optional node count.

        Args:
            nodes: Number of processes to use. If None, defaults to the CPU count.
        """
        super().__init__(pool_class=PathosProcessPool, nodes=nodes)


class ThreadPool(MultiPool):
    """
    Context manager specifically for creating a thread-based pool.

    This subclass of MultiPool defaults to using the ThreadPool from Pathos.

    Example:
        >>> with ThreadPool() as pool:
        ...     results = pool.map(lambda x: x * 2, range(10))
    """

    def __init__(self, nodes: int | None = None) -> None:
        """
        Initialize a ThreadPool with an optional node count.

        Args:
            nodes: Number of threads to use. If None, defaults to the CPU count.
        """
        super().__init__(pool_class=PathosThreadPool, nodes=nodes)


def mmap(
    how: str, *, get_result: bool = False
) -> Callable[[Callable[[T], U]], Callable[[Iterator[T]], Iterator[U]]]:
    """
    Create a decorator to perform parallel mapping using a specified Pathos pool method.

    The decorator wraps a function so that when it is called with an iterable,
    the function is applied in parallel using the specified mapping method.
    For asynchronous mapping (e.g., 'amap'), the result's `.get()` method can be
    automatically called to retrieve the computed values.

    Args:
        how: Name of the pool mapping method ('map', 'imap', or 'amap').
        get_result: If True, automatically call .get() on the result (useful for amap).
                    Defaults to False.

    Returns:
        A decorator function that transforms the target function for parallel execution.

    Example:
        >>> @mmap('map')
        ... def cube(x: int) -> int:
        ...     return x ** 3
        >>> results = list(cube(range(5)))
        >>> print(results)
        [0, 1, 8, 27, 64]
    """

    def decorator(func: Callable[[T], U]) -> Callable[[Iterator[T]], Iterator[U]]:
        @wraps(func)
        def wrapper(iterable: Iterator[T], *args: Any, **kwargs: Any) -> Any:
            # Create a MultiPool context to manage the pool lifecycle
            with MultiPool() as pool:
                # Dynamically fetch the mapping method (map, imap, or amap)
                mapping_method = getattr(pool, how)
                result = mapping_method(func, iterable)
                # For asynchronous mapping, call .get() to obtain the actual results
                if get_result:
                    result = result.get()
                return result

        return wrapper

    return decorator


# Convenience decorators for common mapping strategies:
imap = mmap(how="imap")  # Lazy evaluation: returns an iterator
amap = mmap(how="amap", get_result=True)  # Async evaluation with automatic .get()
pmap = mmap(how="map")  # Standard parallel map (eager evaluation)

```
tests/test_benchmark.py
```.py
"""Benchmark tests for twat_mp."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from twat_mp import ProcessPool, ThreadPool, amap, imap, mmap, pmap

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator


def _compute_intensive(x: int) -> int:
    """Compute-intensive operation for benchmarking."""
    result = x
    for _ in range(1000):  # Simulate CPU-intensive work
        result = (result * x + x) % 10000
    return result


def _io_intensive(x: int) -> int:
    """I/O-intensive operation for benchmarking."""
    import time

    time.sleep(0.001)  # Simulate I/O wait
    return x * 2


def generate_data(size: int) -> list[int]:
    """Generate test data of specified size."""
    return list(range(size))


@pytest.fixture
def small_data() -> list[int]:
    """Fixture for small dataset."""
    return generate_data(100)


@pytest.fixture
def medium_data() -> list[int]:
    """Fixture for medium dataset."""
    return generate_data(1000)


@pytest.fixture
def large_data() -> list[int]:
    """Fixture for large dataset."""
    return generate_data(10000)


def run_parallel_operation(
    func: Callable[[int], int],
    data: list[int] | Iterator[int],
    parallel_impl: Callable[
        [Callable[[Any], Any]], Callable[[list[Any] | Iterator[Any]], Iterator[Any]]
    ],
) -> list[int]:
    """Run a parallel operation with given implementation."""
    parallel_func = parallel_impl(func)
    return list(parallel_func(data))


@pytest.mark.benchmark
class TestComputeIntensiveBenchmarks:
    """Benchmark suite for compute-intensive operations."""

    def test_sequential_vs_process_pool(self, benchmark, medium_data):
        """Compare sequential vs process pool performance for compute-intensive work."""

        def sequential() -> list[int]:
            return list(map(_compute_intensive, medium_data))

        def parallel() -> list[int]:
            with ProcessPool() as pool:
                return list(pool.map(_compute_intensive, medium_data))

        result = sequential()  # Run once to get result
        assert parallel() == result  # Verify results match

        # Benchmark both implementations in a single call
        def run_both() -> tuple[list[int], list[int]]:
            return sequential(), parallel()

        benchmark(run_both)

    @pytest.mark.parametrize("data_size", [100, 1000, 10000])
    def test_parallel_implementations(self, benchmark, data_size):
        """Compare different parallel implementations with varying data sizes."""
        data = generate_data(data_size)

        def process_map(
            f: Callable[[Any], Any],
        ) -> Callable[[Any], Iterator[Any]]:
            return mmap(how="map")(f)

        def thread_map(
            f: Callable[[Any], Any],
        ) -> Callable[[Any], Iterator[Any]]:
            def wrapper(iterable: Any) -> Iterator[Any]:
                with ThreadPool() as pool:
                    return pool.map(f, iterable)

            return wrapper

        implementations = {
            "process_pool": process_map,
            "thread_pool": thread_map,
            "amap": lambda f: amap(f),
            "imap": lambda f: imap(f),
            "pmap": lambda f: pmap(f),
        }

        # Run once to get reference result
        reference_impl = implementations["process_pool"]
        reference_result = run_parallel_operation(
            _compute_intensive, data, reference_impl
        )

        # Verify all implementations produce the same result
        results = {}
        for name, impl in implementations.items():
            result = run_parallel_operation(_compute_intensive, data, impl)
            assert result == reference_result  # Verify results match
            results[name] = result

        # Benchmark all implementations in a single call
        def run_all() -> dict[str, list[int]]:
            return {
                name: run_parallel_operation(_compute_intensive, data, impl)
                for name, impl in implementations.items()
            }

        benchmark(run_all)


@pytest.mark.benchmark
class TestIOIntensiveBenchmarks:
    """Benchmark suite for I/O-intensive operations."""

    def test_thread_vs_process_pool(self, benchmark, medium_data):
        """Compare thread pool vs process pool for I/O-intensive work."""

        def process_pool() -> list[int]:
            with ProcessPool() as pool:
                return list(pool.map(_io_intensive, medium_data))

        def thread_pool() -> list[int]:
            with ThreadPool() as pool:
                return list(pool.map(_io_intensive, medium_data))

        result = process_pool()  # Run once to get result
        assert thread_pool() == result  # Verify results match

        # Benchmark both implementations in a single call
        def run_both() -> tuple[list[int], list[int]]:
            return process_pool(), thread_pool()

        benchmark(run_both)


@pytest.mark.benchmark
class TestScalabilityBenchmarks:
    """Benchmark suite for testing scalability with different numbers of workers."""

    @pytest.mark.parametrize("nodes", [2, 4, 8, 16])
    def test_worker_scaling(self, benchmark, medium_data, nodes):
        """Test how performance scales with different numbers of worker processes."""

        def run_with_workers() -> list[int]:
            with ProcessPool(nodes=nodes) as pool:
                return list(pool.map(_compute_intensive, medium_data))

        benchmark(run_with_workers)


@pytest.mark.benchmark
class TestCompositionBenchmarks:
    """Benchmark suite for testing composed parallel operations."""

    def test_chained_operations(self, benchmark, medium_data):
        """Test performance of chained parallel operations."""

        def sequential_chain() -> list[int]:
            return [_io_intensive(_compute_intensive(x)) for x in medium_data]

        def parallel_chain() -> list[int]:
            compute = amap(_compute_intensive)
            io_op = amap(_io_intensive)
            return list(io_op(compute(medium_data)))

        result = sequential_chain()  # Run once to get result
        assert parallel_chain() == result  # Verify results match

        # Benchmark both implementations in a single call
        def run_both() -> tuple[list[int], list[int]]:
            return sequential_chain(), parallel_chain()

        benchmark(run_both)

```
tests/test_twat_mp.py
```.py
"""Test suite for twat_mp."""

import time
from collections.abc import Iterator
from typing import TypeVar

import pytest

from twat_mp import ProcessPool, ThreadPool, amap, imap, mmap, pmap
from twat_mp.__version__ import version as __version__

T = TypeVar("T")
U = TypeVar("U")

# Test constants
TEST_PROCESS_POOL_SIZE = 2
TEST_THREAD_POOL_SIZE = 3


def test_version():
    """Verify package exposes version."""
    assert __version__


def _square(x: int) -> int:
    """Square a number."""
    return x * x


def _subs(x: int) -> int:
    """Subtract one."""
    return x - 1


# Create decorated versions of the functions
isquare = amap(_square)
isubs = amap(_subs)


def test_process_pool_context():
    """Test ProcessPool context manager functionality."""
    with ProcessPool() as pool:
        result = list(pool.map(_square, iter(range(5))))
        assert result == [0, 1, 4, 9, 16]


def test_thread_pool_context():
    """Test ThreadPool context manager functionality."""
    with ThreadPool() as pool:
        result = list(pool.map(_square, iter(range(5))))
        assert result == [0, 1, 4, 9, 16]


def test_amap_decorator():
    """Test async parallel map decorator."""
    result = list(isquare(iter(range(5))))
    assert result == [0, 1, 4, 9, 16]


def test_pmap_decorator():
    """Test standard parallel map decorator."""
    psquare = pmap(_square)
    result = list(psquare(iter(range(5))))
    assert result == [0, 1, 4, 9, 16]


def test_imap_decorator():
    """Test iterator parallel map decorator."""
    isquare_iter = imap(_square)
    result = list(isquare_iter(iter(range(5))))
    assert result == [0, 1, 4, 9, 16]
    # Verify it returns an iterator
    result_iter = isquare_iter(iter(range(5)))
    assert isinstance(result_iter, Iterator)


def test_composed_operations():
    """Test composition of parallel operations."""
    result = list(isubs(isquare(iter(range(5)))))
    assert result == [-1, 0, 3, 8, 15]


def test_pool_nodes_specification():
    """Test pool creation with specific node count."""
    with ProcessPool(nodes=TEST_PROCESS_POOL_SIZE) as pool:
        assert pool.nodes == TEST_PROCESS_POOL_SIZE
    with ThreadPool(nodes=TEST_THREAD_POOL_SIZE) as pool:
        assert pool.nodes == TEST_THREAD_POOL_SIZE


@pytest.mark.benchmark
def test_parallel_vs_sequential_performance():
    """Benchmark parallel vs sequential processing."""
    test_range = range(1000)

    # Sequential processing
    start_time = time.perf_counter()
    seq_result = list(map(_square, test_range))
    time.perf_counter() - start_time

    # Parallel processing
    start_time = time.perf_counter()
    par_result = list(isquare(iter(test_range)))
    time.perf_counter() - start_time

    # Assert results are equal
    assert seq_result == par_result

    # On sufficiently large inputs, parallel should be faster
    # Note: This might not always be true due to overhead, system load, etc.
    # so we don't make it a hard assertion


def test_mmap_decorator_variants():
    """Test mmap decorator with different 'how' parameters."""
    # Test standard map variant
    standard_map = mmap(how="map")(_square)
    result_map = list(standard_map(iter(range(5))))
    assert result_map == [0, 1, 4, 9, 16]

    # Test imap variant
    iter_map = mmap(how="imap")(_square)
    result_imap = list(iter_map(iter(range(5))))
    assert result_imap == [0, 1, 4, 9, 16]
    # Verify it returns an iterator
    result_iter = iter_map(iter(range(5)))
    assert isinstance(result_iter, Iterator)

    # Test amap variant with get_result=True
    async_map = mmap(how="amap", get_result=True)(_square)
    result_amap = list(async_map(iter(range(5))))
    assert result_amap == [0, 1, 4, 9, 16]

    # Verify all variants produce the same results
    assert result_map == result_imap == result_amap

```

