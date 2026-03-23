---
hide:
  - navigation
---

# API Reference

## Core API

### Initialization

| Function | Description |
|----------|-------------|
| `agnocast::init(argc, argv)` | Initialize Agnocast (for `agnocast::Node`, Stage 2) |
| `agnocast::initialize_agnocast()` | Initialize shared memory pools |

### Free Functions (Stage 1)

These free functions are used with `rclcpp::Node` at Stage 1. Pass the node pointer as the first argument.

| Function | Description |
|----------|-------------|
| `agnocast::create_publisher<MessageT>(node, topic, qos, options)` | Create an Agnocast publisher |
| `agnocast::create_subscription<MessageT>(node, topic, qos, callback, options)` | Create an event-driven subscription |
| `agnocast::create_subscription<MessageT>(node, topic, qos)` | Create a polling subscription |
| `agnocast::create_client<ServiceT>(node, service_name)` | Create a service client |
| `agnocast::create_service<ServiceT>(node, service_name, callback)` | Create a service server |
| `agnocast::create_timer(node, clock, period, callback)` | Create a timer |

---

## Node

### `agnocast::Node`

Stage 2 node class that bypasses the rcl layer. API-compatible with `rclcpp::Node` for supported features.

**Constructors:**

| Signature | Description |
|-----------|-------------|
| `Node(name)` | Create node with name |
| `Node(name, namespace)` | Create node with name and namespace |
| `Node(name, options)` | Create node with options |

**Topic Methods:**

| Method | Description |
|--------|-------------|
| `create_publisher<T>(topic, qos, options)` | Create Agnocast publisher |
| `create_subscription<T>(topic, qos, callback, options)` | Create event-driven subscription |
| `create_subscription<T>(topic, qos)` | Create polling subscription |

**Service Methods:**

| Method | Description |
|--------|-------------|
| `create_client<T>(name)` | Create service client |
| `create_service<T>(name, callback)` | Create service server |

**Timer Methods:**

| Method | Description |
|--------|-------------|
| `create_wall_timer(period, callback)` | Create wall-clock timer |

**Parameter Methods:**

| Method | Description |
|--------|-------------|
| `declare_parameter(name, default_value)` | Declare a parameter |
| `get_parameter(name, value)` | Get parameter value |
| `set_parameter(parameter)` | Set parameter value |
| `add_on_set_parameters_callback(callback)` | Register parameter change callback |

**Node Info:**

| Method | Description |
|--------|-------------|
| `get_name()` | Node name |
| `get_namespace()` | Node namespace |
| `get_fully_qualified_name()` | Fully qualified node name |
| `get_logger()` | Logger instance |
| `get_clock()` | Clock instance |
| `now()` | Current time |

---

## Publisher

### `agnocast::Publisher<MessageT>`

| Method | Description |
|--------|-------------|
| `borrow_loaned_message()` | Allocate message in shared memory → `ipc_shared_ptr<MessageT>` |
| `publish(ipc_shared_ptr<MessageT>&&)` | Publish message (zero-copy) |
| `get_subscription_count()` | Number of subscribers |
| `get_topic_name()` | Topic name |
| `get_gid()` | Publisher GID (unique across Agnocast and ROS 2) |

---

## Subscription

### `agnocast::Subscription<MessageT>`

Event-driven subscription. Callback is invoked when a new message arrives.

**Callback signature:** `void(const agnocast::ipc_shared_ptr<MessageT> &)`

### `agnocast::PollingSubscriber<MessageT>`

Polling-based subscription. Messages are retrieved explicitly.

| Method | Description |
|--------|-------------|
| `take_data()` | Retrieve latest message (returns `nullptr` if none available) |
| `take(allow_same_message)` | Retrieve message with option to re-read |

---

## Smart Pointer

### `agnocast::ipc_shared_ptr<T>`

Shared pointer for IPC messages in shared memory. Thread-safe with atomic reference counting.

| Method | Description |
|--------|-------------|
| `get()` | Raw pointer (`nullptr` if invalidated) |
| `operator->()` | Dereference (terminates if invalidated) |
| `operator*()` | Dereference (terminates if invalidated) |
| `reset()` | Release ownership |
| `get_topic_name()` | Topic name of the message |

!!! note
    After a message is published with `publish(std::move(msg))`, the original `ipc_shared_ptr` is invalidated. Accessing it will terminate the program.

---

## Service

### `agnocast::Service<ServiceT>`

| Type Alias | Description |
|------------|-------------|
| `RequestT` | Request message type |
| `ResponseT` | Response message type |

**Server callback signature:** `void(const ipc_shared_ptr<RequestT>&, ipc_shared_ptr<ResponseT>&)`

### `agnocast::Client<ServiceT>`

| Method | Description |
|--------|-------------|
| `borrow_loaned_request()` | Allocate request in shared memory |
| `async_send_request(request, callback)` | Send request with callback |
| `async_send_request(request)` | Send request, returns future |
| `wait_for_service(timeout)` | Wait for service availability |
| `service_is_ready()` | Check if service is available |

---

## Executors

| Executor | ROS 2 Callbacks | Agnocast Callbacks | Use Case |
|----------|----------------|-------------------|----------|
| `SingleThreadedAgnocastExecutor` | Yes | Yes | Stage 1, single-threaded |
| `MultiThreadedAgnocastExecutor` | Yes | Yes | Stage 1, multi-threaded |
| `CallbackIsolatedAgnocastExecutor` | Yes | Yes | Stage 1, callback-isolated |
| `AgnocastOnlySingleThreadedExecutor` | No | Yes | Stage 2, single-threaded |
| `AgnocastOnlyMultiThreadedExecutor` | No | Yes | Stage 2, multi-threaded |
| `AgnocastOnlyCallbackIsolatedExecutor` | No | Yes | Stage 2, callback-isolated |

---

## Subscription Options

### `agnocast::SubscriptionOptions`

| Field | Description |
|-------|-------------|
| `callback_group` | Callback group for the subscription |
| `qos_overriding_options` | QoS parameter override options |

---

## Auto-generation of API List

!!! info "Future Enhancement"
    We are investigating automatic API list generation from the agnocastlib source code, similar to how rclcpp uses `RCLCPP_PUBLIC` to mark public APIs. An `AGNOCAST_PUBLIC` visibility macro could serve the same purpose, enabling tools like Doxygen or Sphinx to automatically extract and document the public API surface.

    Currently, the agnocastlib codebase uses header-only templates and does not have explicit export macros. The API surface is defined by the public headers in `agnocastlib/include/agnocast/`.
