
# GenericTimer

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->


### `agnocast::GenericTimer<FunctorT>`

**Extends:** `agnocast::TimerBase`

Timer that fires periodically using a user-provided clock.


---

#### `is_steady()`

```cpp
bool GenericTimer::is_steady()
```

Return whether this timer uses a steady clock.

| | |
|-----------|-------------|
| **Returns** | True if the clock is steady. |


---

#### `get_clock()`

```cpp
rclcpp::Clock::SharedPtr GenericTimer::get_clock()
```

Get the clock associated with this timer.

| | |
|-----------|-------------|
| **Returns** | Shared pointer to the clock. |

