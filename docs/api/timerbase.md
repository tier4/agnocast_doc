
# TimerBase

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->


### `agnocast::TimerBase`

Base class for Agnocast timers providing periodic callback execution. Defines the common interface for all timer types, including callback execution, clock access, and period storage.


---

#### `is_steady()`

```cpp
bool TimerBase::is_steady() const
```

Return whether this timer uses a steady clock.

| | |
|-----------|-------------|
| **Returns** | True if the clock is steady. |


---

#### `get_clock()`

```cpp
rclcpp::Clock::SharedPtr TimerBase::get_clock()
```

Get the clock associated with this timer.

| | |
|-----------|-------------|
| **Returns** | Shared pointer to the clock. |

