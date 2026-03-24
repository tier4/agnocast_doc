
# ipc_shared_ptr

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->


### `agnocast::ipc_shared_ptr<T>`

Smart pointer for zero-copy IPC message sharing between publishers and subscribers. ipc_shared_ptr manages the lifetime of messages allocated in shared memory. Publishers obtain an instance via Publisher::borrow_loaned_message(), fill in message fields, and transfer ownership with Publisher::publish(). Subscribers receive ipc_shared_ptr<const MessageT> in their callbacks; the kernel-side reference is released when all copies are destroyed.

**Example:**

```cpp
// Publisher side
auto msg = publisher->borrow_loaned_message();  // ipc_shared_ptr<MyMsg>
msg->data = 42;
publisher->publish(std::move(msg));
// msg is now invalidated — do NOT access it

// Subscriber side (callback receives ipc_shared_ptr<const MyMsg>)
void callback(const agnocast::ipc_shared_ptr<const MyMsg> & msg) {
  int value = msg->data;     // zero-copy read from shared memory
}  // kernel reference released when msg goes out of scope
```


---

#### `ipc_shared_ptr() (constructor)`

```cpp
ipc_shared_ptr::ipc_shared_ptr()
```

Construct an empty (null) ipc_shared_ptr.


---

#### `ipc_shared_ptr() (constructor) [overload 2]`

```cpp
ipc_shared_ptr::ipc_shared_ptr(agnocast::ipc_shared_ptr &r)
```

Copy constructor. Creates a new reference to the same message. The reference count is incremented atomically, so it is safe to copy from an instance that another thread also copies from. However, two threads must not copy-from and write-to the same instance concurrently.


---

#### `operator=()`

```cpp
agnocast::ipc_shared_ptr& agnocast::ipc_shared_ptr::operator=(agnocast::ipc_shared_ptr &r)
```

Copy assignment. Releases the current reference and shares ownership with r . Same thread-safety guarantees as the copy constructor.

| | |
|-----------|-------------|
| **Returns** | Reference to *this. |


---

#### `ipc_shared_ptr() (constructor) [overload 3]`

```cpp
ipc_shared_ptr::ipc_shared_ptr(agnocast::ipc_shared_ptr &&r) noexcept
```

Move constructor. Transfers ownership from r without changing the reference count. Not thread-safe: the caller must ensure no other thread accesses r concurrently.


---

#### `operator=() [overload 2]`

```cpp
agnocast::ipc_shared_ptr& agnocast::ipc_shared_ptr::operator=(agnocast::ipc_shared_ptr &&r) noexcept
```

Move assignment. Releases the current reference and takes ownership from r . Not thread-safe: the caller must ensure no other thread accesses r concurrently.

| | |
|-----------|-------------|
| **Returns** | Reference to *this. |


---

#### `ipc_shared_ptr() (constructor) [overload 4]`

```cpp
ipc_shared_ptr::ipc_shared_ptr(agnocast::ipc_shared_ptr<U> &r)
```

Converting copy constructor (e.g., ipc_shared_ptr<T> to ipc_shared_ptr<const T>). Enabled only when U* is implicitly convertible to T*.


---

#### `ipc_shared_ptr() (constructor) [overload 5]`

```cpp
ipc_shared_ptr::ipc_shared_ptr(agnocast::ipc_shared_ptr<U> &&r)
```

Converting move constructor (e.g., ipc_shared_ptr<T> to ipc_shared_ptr<const T>). Enabled only when U* is implicitly convertible to T*.


---

#### `operator=() [overload 3]`

```cpp
agnocast::ipc_shared_ptr& agnocast::ipc_shared_ptr::operator=(agnocast::ipc_shared_ptr<U> &r)
```

Converting copy assignment (e.g., ipc_shared_ptr<T> to ipc_shared_ptr<const T>). Enabled only when U* is implicitly convertible to T* .

| | |
|-----------|-------------|
| **Returns** | Reference to *this. |


---

#### `operator=() [overload 4]`

```cpp
agnocast::ipc_shared_ptr& agnocast::ipc_shared_ptr::operator=(agnocast::ipc_shared_ptr<U> &&r)
```

Converting move assignment (e.g., ipc_shared_ptr<T> to ipc_shared_ptr<const T>). Enabled only when U* is implicitly convertible to T* .

| | |
|-----------|-------------|
| **Returns** | Reference to *this. |


---

#### `operator*()`

```cpp
T& agnocast::ipc_shared_ptr::operator*() noexcept
```

Dereference the managed message. Calls `std::terminate`() if the pointer has been invalidated by publish().

| | |
|-----------|-------------|
| **Returns** | Reference to the managed message. |


---

#### `operator->()`

```cpp
T* agnocast::ipc_shared_ptr::operator->() noexcept
```

Access a member of the managed message. Calls `std::terminate`() if the pointer has been invalidated by publish().

| | |
|-----------|-------------|
| **Returns** | Pointer to the managed message. |


---

#### `operator bool()`

```cpp
agnocast::ipc_shared_ptr::operator bool() noexcept
```

Return true if the pointer is non-null and has not been invalidated.

| | |
|-----------|-------------|
| **Returns** | True if non-null and not invalidated. |


---

#### `get()`

```cpp
T* ipc_shared_ptr::get() noexcept
```

Return the raw pointer, or nullptr if empty or invalidated.

| | |
|-----------|-------------|
| **Returns** | Raw pointer, or nullptr if empty or invalidated. |


---

#### `reset()`

```cpp
void ipc_shared_ptr::reset()
```

Release ownership of the managed message. If this is the last reference: on the subscriber side, notifies the kernel module that the message can be reclaimed; on the publisher side (if unpublished), frees the allocated memory.

