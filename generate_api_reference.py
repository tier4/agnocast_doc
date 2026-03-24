#!/usr/bin/env python3
"""Generate docs/api/index.md from Doxygen XML output.

Usage:
    # 1. Generate Doxygen XML (requires doxygen installed)
    doxygen Doxyfile
    # 2. Generate the markdown
    python3 generate_api_reference.py
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

XML_DIR = Path(__file__).parent / ".doxygen_xml" / "xml"
OUTPUT_DIR = Path(__file__).parent / "docs" / "api"

# ── helpers ──────────────────────────────────────────────────────────────────


def text_content(elem):
    """Recursively extract text from an XML element, stripping tags."""
    if elem is None:
        return ""
    parts = []
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        parts.append(text_content(child))
        if child.tail:
            parts.append(child.tail)
    return "".join(parts).strip()


def brief(memberdef):
    b = memberdef.find("briefdescription")
    return text_content(b) if b is not None else ""


def get_detailed_prose(mdef):
    """Extract prose paragraphs from detaileddescription, excluding @param/@tparam/@return sections."""
    detail = mdef.find("detaileddescription")
    if detail is None:
        return ""
    parts = []
    for para in detail.findall("para"):
        # Check if paragraph contains special elements
        has_special = any(child.tag in ("parameterlist", "simplesect") for child in para)
        if not has_special:
            t = text_content(para).strip()
            if t:
                parts.append(t)
        else:
            # Extract text before the first special child element
            prose_parts = []
            if para.text:
                prose_parts.append(para.text.strip())
            for child in para:
                if child.tag in ("parameterlist", "simplesect"):
                    break
                prose_parts.append(text_content(child))
                if child.tail:
                    prose_parts.append(child.tail.strip())
            t = " ".join(p for p in prose_parts if p).strip()
            if t:
                parts.append(t)
    return " ".join(parts)


def get_param_defaults(mdef):
    """Extract default values for parameters from the XML param elements."""
    defaults = {}
    for param in mdef.findall("param"):
        pname_elem = param.find("declname")
        defval_elem = param.find("defval")
        if pname_elem is not None and defval_elem is not None:
            pname = pname_elem.text or ""
            defval = text_content(defval_elem).strip()
            if pname and defval:
                # Restore namespace prefixes for aliased types
                defval = defval.replace("agnocast::PublisherOptions", "agnocast::PublisherOptions")  # no-op guard
                defval = defval.replace("agnocast::SubscriptionOptions", "agnocast::SubscriptionOptions")  # no-op guard
                if "agnocast::" not in defval:
                    defval = defval.replace("PublisherOptions", "agnocast::PublisherOptions")
                    defval = defval.replace("SubscriptionOptions", "agnocast::SubscriptionOptions")
                defval = defval.replace("ParameterDescriptor", "rcl_interfaces::msg::ParameterDescriptor")
                defaults[pname] = defval
    return defaults


def get_params(mdef):
    """Extract @param descriptions from detaileddescription, with defaults."""
    params = []
    defaults = get_param_defaults(mdef)
    detail = mdef.find("detaileddescription")
    if detail is None:
        return params
    for paramlist in detail.iter("parameterlist"):
        if paramlist.get("kind") != "param":
            continue
        for item in paramlist.findall("parameteritem"):
            namelist = item.find("parameternamelist")
            desc_elem = item.find("parameterdescription")
            if namelist is not None and desc_elem is not None:
                pname = text_content(namelist.find("parametername"))
                pdesc = text_content(desc_elem)
                if pname and pdesc:
                    defval = defaults.get(pname, "")
                    params.append((pname, pdesc, defval))
    return params


def get_tparams(mdef):
    """Extract @tparam descriptions from detaileddescription."""
    tparams = []
    detail = mdef.find("detaileddescription")
    if detail is None:
        return tparams
    for paramlist in detail.iter("parameterlist"):
        if paramlist.get("kind") != "templateparam":
            continue
        for item in paramlist.findall("parameteritem"):
            namelist = item.find("parameternamelist")
            desc_elem = item.find("parameterdescription")
            if namelist is not None and desc_elem is not None:
                pname = text_content(namelist.find("parametername"))
                pdesc = text_content(desc_elem)
                if pname and pdesc:
                    tparams.append((pname, pdesc))
    return tparams


def get_return(mdef):
    """Extract @return description from detaileddescription."""
    detail = mdef.find("detaileddescription")
    if detail is None:
        return ""
    for simplesect in detail.iter("simplesect"):
        if simplesect.get("kind") == "return":
            return text_content(simplesect)
    return ""


def clean_sig(definition, argsstring):
    """Build a readable signature from Doxygen's definition + argsstring."""
    defn = definition or ""
    args = argsstring or ""

    # For member functions, strip "agnocast::" and template args from the class prefix,
    # keeping "ClassName::" e.g.:
    #   "agnocast::BasicPublisher<MessageT, BridgeRequestPolicy>::borrow_loaned_message"
    #   → "BasicPublisher::borrow_loaned_message"
    # For member functions, strip "agnocast::" namespace and template args from the
    # class prefix, keeping "ClassName::" e.g.:
    #   "agnocast::BasicPublisher<MessageT, BridgeRequestPolicy>::publish"
    #   → "BasicPublisher::publish"
    defn = re.sub(r"agnocast::(\w+)(<[^>]+>)?\s*::", r"\1::", defn)
    # Map internal class names to user-facing alias names
    defn = defn.replace("BasicPublisher::", "Publisher::")
    defn = defn.replace("BasicSubscription::", "Subscription::")
    defn = defn.replace("BasicTakeSubscription::", "TakeSubscription::")
    defn = defn.replace("BasicPollingSubscriber::", "PollingSubscriber::")
    # For free functions, strip bare "agnocast::" before function name
    defn = re.sub(r"\bagnocast::(?=\w+$)", "", defn)

    sig = defn + args

    # Add agnocast:: prefix to known agnocast types that Doxygen emits without namespace
    agnocast_types = [
        "PublisherOptions", "SubscriptionOptions", "Publisher", "Subscription",
        "PollingSubscriber", "TakeSubscription", "ipc_shared_ptr",
        "Client", "Service", "TimerBase", "GenericTimer", "WallTimer", "Node",
    ]
    for t in agnocast_types:
        # Only prefix if not already prefixed with agnocast:: or std:: etc.
        sig = re.sub(rf"(?<!:|\w)(?<!agnocast::)\b{t}\b(?=<|::|[ &*),])", f"agnocast::{t}", sig)

    # In "ClassName::method" positions, strip "agnocast::" from the class name
    # since the section heading already provides context.
    # Match "agnocast::ClassName::methodName(" pattern and remove "agnocast::"
    sig = re.sub(r"agnocast::(\w+::(?:\w+|~\w+)\s*\()", r"\1", sig)

    # Restore namespace prefixes for aliased types that Doxygen strips
    sig = re.sub(r"\bParameterValue\b", "rclcpp::ParameterValue", sig)
    sig = re.sub(r"\bParameterDescriptor\b", "rcl_interfaces::msg::ParameterDescriptor", sig)
    sig = re.sub(r"\bOnSetParametersCallbackType\b",
                 "rclcpp::node_interfaces::OnSetParametersCallbackType", sig)

    # Normalize Doxygen spacing in template args: "< X, Y >" → "<X, Y>"
    sig = re.sub(r"< ", "<", sig)
    sig = re.sub(r" >", ">", sig)

    sig = sig.replace("const ", "")
    # Drop default values from signature (they'll be shown in the parameter table)
    # But don't strip "=" that's part of "operator="
    sig = re.sub(r"(?<!operator)\s*=\s*[^,)]+", "", sig)
    # Remove return types like "typename agnocast::..."
    sig = re.sub(r"^typename\s+", "", sig)
    # Fix mismatched parens from Doxygen default-argument stripping
    open_count = sig.count("(")
    close_count = sig.count(")")
    if close_count > open_count:
        for _ in range(close_count - open_count):
            sig = sig.replace("),", ",", 1) if ")," in sig else re.sub(r"\)+", ")" * open_count, sig)
    # Remove "virtual " prefix
    sig = sig.replace("virtual ", "")
    # Clean up "override" suffix
    sig = sig.replace(" override", "")
    # Collapse multiple spaces
    sig = re.sub(r"  +", " ", sig)
    return sig.strip()


# A member is (sig_or_name, brief_text, params_list, return_text)
Member = tuple  # (str, str, list[tuple[str,str]], str)


def parse_memberdef(mdef):
    """Parse a single memberdef. Returns (sig, description, tparams, params, return) or None."""
    mkind = mdef.get("kind")
    mname = text_content(mdef.find("name"))
    mbr = brief(mdef)

    if not mbr:
        return None

    # Combine brief + detailed prose for a complete description
    detail = get_detailed_prose(mdef)
    full_desc = f"{mbr} {detail}".strip() if detail else mbr

    defn = text_content(mdef.find("definition"))
    args = text_content(mdef.find("argsstring"))
    tparams = get_tparams(mdef)
    params = get_params(mdef)
    ret = get_return(mdef)

    if mkind == "function":
        sig = clean_sig(defn, args)
        return (sig, full_desc, tparams, params, ret)
    elif mkind == "variable":
        return (mname, full_desc, [], [], "")
    elif mkind == "typedef":
        return (mname, full_desc, [], [], "")
    return None


def parse_struct_fields(xml_path):
    """Parse a struct XML file. Return (name, brief, [(type, name, default, brief)])."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    cdef = root.find("compounddef")
    if cdef is None:
        return None

    name = text_content(cdef.find("compoundname"))
    cls_brief = brief(cdef)

    fields = []
    for sdef in cdef.findall("sectiondef"):
        kind = sdef.get("kind", "")
        if "private" in kind:
            continue
        for mdef in sdef.findall("memberdef"):
            if mdef.get("kind") != "variable":
                continue
            mbr = brief(mdef)
            if not mbr:
                continue
            fname = text_content(mdef.find("name"))
            ftype = text_content(mdef.find("type"))
            init_elem = mdef.find("initializer")
            default = text_content(init_elem) if init_elem is not None else ""
            # Clean up default value: "{nullptr}" → "nullptr", "{false}" → "false"
            default = re.sub(r"^\{(.+)\}$", r"\1", default.strip())
            # Clean up "= value" prefix
            default = re.sub(r"^=\s*", "", default)
            fields.append((ftype, fname, default, mbr))

    return name, cls_brief, fields


def get_base_classes(cdef):
    """Extract base class names from compounddef."""
    bases = []
    for b in cdef.findall("basecompoundref"):
        bname = text_content(b)
        if bname:
            bases.append(bname)
    return bases


# Map internal class names to user-facing names for base class display
BASE_CLASS_DISPLAY = {
    "agnocast::AgnocastExecutor": "agnocast::AgnocastExecutor",
    "agnocast::AgnocastOnlyExecutor": "agnocast::AgnocastOnlyExecutor",
    "agnocast::TimerBase": "agnocast::TimerBase",
    "agnocast::GenericTimer< FunctorT >": "agnocast::GenericTimer<FunctorT>",
    "rclcpp::Executor": "rclcpp::Executor",
    "SubscriptionBase": None,  # internal, don't show
}


def parse_class(xml_path):
    """Parse a class XML file. Return (name, brief, bases, [Member])."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    cdef = root.find("compounddef")
    if cdef is None:
        return None

    name = text_content(cdef.find("compoundname"))
    cls_brief_text = brief(cdef)
    cls_detail = get_detailed_prose(cdef)
    cls_brief = f"{cls_brief_text} {cls_detail}".strip() if cls_detail else cls_brief_text

    bases = get_base_classes(cdef)

    members = []

    # Parse documented inner classes/structs (e.g., Client::RequestT, Client::FutureAndRequestId)
    for ic in cdef.findall("innerclass"):
        refid = ic.get("refid", "")
        prot = ic.get("prot", "")
        if prot == "private":
            continue
        ic_xml = xml_path.parent / f"{refid}.xml"
        if not ic_xml.exists():
            continue
        ic_tree = ET.parse(ic_xml)
        ic_cdef = ic_tree.getroot().find("compounddef")
        if ic_cdef is None:
            continue
        ic_brief = brief(ic_cdef)
        if not ic_brief:
            continue
        ic_detail = get_detailed_prose(ic_cdef)
        ic_full = f"{ic_brief} {ic_detail}".strip() if ic_detail else ic_brief
        ic_name = text_content(ic_cdef.find("compoundname"))
        # Use short name: "agnocast::Client::RequestT" → "RequestT"
        short = ic_name.rsplit("::", 1)[-1] if "::" in ic_name else ic_name
        members.append((f"struct {short}", ic_full, [], [], ""))

    for sdef in cdef.findall("sectiondef"):
        kind = sdef.get("kind", "")
        if "private" in kind or "friend" in kind or "protected" in kind:
            continue
        for mdef in sdef.findall("memberdef"):
            m = parse_memberdef(mdef)
            if m:
                members.append(m)

    return name, cls_brief, bases, members


def parse_namespace_typedefs(xml_path):
    """Parse namespace XML to get documented type aliases."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    cdef = root.find("compounddef")
    if cdef is None:
        return []

    typedefs = []
    for sdef in cdef.findall("sectiondef"):
        kind = sdef.get("kind", "")
        if kind != "typedef":
            continue
        for mdef in sdef.findall("memberdef"):
            mbr = brief(mdef)
            if not mbr:
                continue
            name = text_content(mdef.find("name"))
            defn = text_content(mdef.find("definition"))
            detail = get_detailed_prose(mdef)
            full_desc = f"{mbr} {detail}".strip() if detail else mbr
            # Extract the "= ..." part from definition
            # e.g. "using agnocast::Publisher = typedef agnocast::BasicPublisher<...>"
            target = ""
            if "typedef" in defn:
                target = defn.split("typedef", 1)[1].strip()
            elif "=" in defn:
                target = defn.split("=", 1)[1].strip()
            # Strip internal policy template args from the target
            # e.g. "BasicPublisher<MessageT, agnocast::AgnocastToRosRequestPolicy>"
            #    → "BasicPublisher<MessageT>"
            target = re.sub(r",\s*agnocast::\w+RequestPolicy", "", target)
            typedefs.append((name, target, full_desc))
    return typedefs


def parse_namespace_functions(xml_path):
    """Parse namespace XML to get free functions."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    cdef = root.find("compounddef")
    if cdef is None:
        return []

    funcs = []
    for sdef in cdef.findall("sectiondef"):
        kind = sdef.get("kind", "")
        if kind != "func":
            continue
        for mdef in sdef.findall("memberdef"):
            m = parse_memberdef(mdef)
            if m is None:
                continue
            sig, mbr, tparams, params, ret = m
            # The function name's agnocast:: prefix is already stripped by clean_sig
            funcs.append((sig, mbr, tparams, params, ret))
    return funcs


# ── rendering ────────────────────────────────────────────────────────────────


# Fallback descriptions for common template parameters that are obvious
# from context but may not have explicit @tparam in the source.
TPARAM_FALLBACKS = {
    "NodeT": "Node type (`rclcpp::Node` or `agnocast::Node`).",
    "Func": "Callable type for the callback.",
    "CallbackT": "Callable type for the callback.",
    "FunctorT": "Callable type for the callback.",
    "MessageT": "ROS message type.",
    "ServiceT": "ROS service type.",
    "RequestT": "Request message type (derived from `ServiceT::Request`).",
    "ResponseT": "Response message type (derived from `ServiceT::Response`).",
    "ParameterT": "Parameter value type.",
}


def infer_tparams(sig, existing_tparams):
    """Add fallback @tparam entries for template args in sig that are not already documented."""
    documented = {t[0] for t in existing_tparams}
    result = list(existing_tparams)
    # Find template-looking identifiers (words ending in T, or 'Func')
    candidates = re.findall(r'\b([A-Z]\w*T)\b', sig) + re.findall(r'\b(Func)\b', sig)
    seen = set()
    for name in candidates:
        if name in documented or name in seen or name in ("SharedPtr",):
            continue
        seen.add(name)
        if name in TPARAM_FALLBACKS:
            result.append((name, TPARAM_FALLBACKS[name]))
    return result


def format_prose(text):
    """Wrap namespace-qualified type names in backticks for consistency."""
    # Match rclcpp::X, agnocast::X, std::X patterns not already in backticks
    text = re.sub(r'(?<!`)\b((?:rclcpp|agnocast|std|rcl_interfaces)\b(?:::\w+)+)', r'`\1`', text)
    # Fix double-backtick from already-backticked content
    text = text.replace("``", "`")
    return text


def extract_short_name(sig):
    """Extract a short method/function name for ToC headings."""
    # Destructor: "~ClassName()"
    m = re.search(r"(~\w+)\s*\(", sig)
    if m:
        return f"{m.group(1)}() (destructor)"

    # Operators: "operator=", "operator*", "operator->", "operator bool"
    m = re.search(r"(operator\s*(?:bool|[^\s(]+))\s*\(", sig)
    if m:
        return f"{m.group(1).strip()}()"

    # Constructor: "ClassName::ClassName("
    m = re.search(r"(\w+)::\1\s*\(", sig)
    if m:
        return f"{m.group(1)}() (constructor)"

    # Regular method/function: "ClassName::methodName(" or "functionName("
    m = re.search(r"(?:\w+::)?(\w+)\s*\(", sig)
    if m:
        return f"{m.group(1)}()"

    # No parens — likely a struct field
    return sig.split()[-1] if sig else sig


def render_member(f, sig, mbr, tparams, params, ret, seen_names=None):
    """Render a single API member as markdown."""
    short_name = extract_short_name(sig)

    # Disambiguate overloads by appending a counter
    if seen_names is not None:
        if short_name in seen_names:
            seen_names[short_name] += 1
            # "get_clock()" → "get_clock() [overload 2]"
            short_name = f"{short_name} [overload {seen_names[short_name]}]"
        else:
            seen_names[short_name] = 1

    f.write(f"\n---\n\n")
    f.write(f"#### `{short_name}`\n\n")
    f.write(f"```cpp\n{sig}\n```\n\n")
    f.write(f"{format_prose(mbr)}\n\n")
    tparams = infer_tparams(sig, tparams)
    has_content = tparams or params or ret
    if has_content:
        has_defaults = any(defval for _, _, defval in params) if params else False

        if tparams:
            f.write("| Template Parameter | Description |\n")
            f.write("|-----------|-------------|\n")
            for pname, pdesc in tparams:
                f.write(f"| `{pname}` | {format_prose(pdesc)} |\n")

        if params:
            if tparams:
                if has_defaults:
                    f.write("| **Parameter** | **Default** | **Description** |\n")
                else:
                    f.write("| **Parameter** | **Description** |\n")
            else:
                if has_defaults:
                    f.write("| Parameter | Default | Description |\n")
                    f.write("|-----------|---------|-------------|\n")
                else:
                    f.write("| Parameter | Description |\n")
                    f.write("|-----------|-------------|\n")
            for pname, pdesc, defval in params:
                if has_defaults:
                    defval_fmt = f"`{defval}`" if defval else "—"
                    f.write(f"| `{pname}` | {defval_fmt} | {format_prose(pdesc)} |\n")
                else:
                    f.write(f"| `{pname}` | {format_prose(pdesc)} |\n")

        if ret:
            if tparams or params:
                if has_defaults:
                    f.write("| | | |\n")
                else:
                    f.write("| | |\n")
            else:
                f.write("| | |\n")
                f.write("|-----------|-------------|\n")
            f.write(f"| **Returns** | {format_prose(ret)} |\n")
        f.write("\n")


def render_class_section(f, display_name, xml_file, desc_override=None, section_name=None):
    xml_path = XML_DIR / xml_file
    if not xml_path.exists():
        f.write(f"\n### `{display_name}`\n\n*Documentation not generated.*\n\n")
        return

    parsed = parse_class(xml_path)
    if parsed is None:
        return

    name, cls_brief, bases, members = parsed
    desc = desc_override or cls_brief

    f.write(f"\n### `{display_name}`\n\n")

    # Show base class(es)
    visible_bases = []
    for b in bases:
        display = BASE_CLASS_DISPLAY.get(b, b)  # default: show as-is
        if display is not None:
            visible_bases.append(display)
    if visible_bases:
        bases_str = ", ".join(f"`{b}`" for b in visible_bases)
        f.write(f"**Extends:** {bases_str}\n\n")

    if desc:
        f.write(f"{format_prose(desc)}\n\n")

    # Usage example
    example = EXAMPLES.get(section_name or "")
    if example:
        f.write("**Example:**\n")
        f.write(example)
        f.write("\n")

    seen_names = {}
    for sig, mbr, tparams, params, ret in members:
        render_member(f, sig, mbr, tparams, params, ret, seen_names)


def render_free_functions(f, funcs):
    seen_names = {}
    for sig, mbr, tparams, params, ret in funcs:
        render_member(f, sig, mbr, tparams, params, ret, seen_names)


def render_struct_section(f, display_name, xml_file):
    xml_path = XML_DIR / xml_file
    if not xml_path.exists():
        f.write(f"\n### `{display_name}`\n\n*Documentation not generated.*\n\n")
        return

    parsed = parse_struct_fields(xml_path)
    if parsed is None:
        return

    name, cls_brief, fields = parsed

    f.write(f"\n### `{display_name}`\n\n")
    if cls_brief:
        f.write(f"{format_prose(cls_brief)}\n\n")

    if fields:
        f.write("| Type | Field | Default | Description |\n")
        f.write("|------|-------|---------|-------------|\n")
        for ftype, fname, default, fdesc in fields:
            ftype_fmt = f"`{ftype}`"
            fname_fmt = f"`{fname}`"
            default_fmt = f"`{default}`" if default else "—"
            f.write(f"| {ftype_fmt} | {fname_fmt} | {default_fmt} | {format_prose(fdesc)} |\n")
        f.write("\n")


# ── usage examples ────────────────────────────────────────────────────────────

EXAMPLES = {
    "Publisher": '''
```cpp
// Create a publisher (Stage 1, with rclcpp::Node)
auto pub = agnocast::create_publisher<MyMsg>(this, "/topic", 10);

// Borrow, populate, publish
auto msg = pub->borrow_loaned_message();
msg->data = 42;
pub->publish(std::move(msg));  // msg is invalidated after this
```
''',

    "Subscription": '''
```cpp
// Event-driven subscription (Stage 1, with rclcpp::Node)
auto sub = agnocast::create_subscription<MyMsg>(
  this, "/topic", 10,
  [this](const agnocast::ipc_shared_ptr<const MyMsg> & msg) {
    RCLCPP_INFO(get_logger(), "Received: %d", msg->data);
  });
```
''',

    "PollingSubscriber": '''
```cpp
// Polling subscription — call take_data() in a timer callback
auto sub = this->create_subscription<MyMsg>("/topic", rclcpp::QoS(1));

auto timer = this->create_wall_timer(100ms, [this, sub]() {
  auto msg = sub->take_data();
  if (msg) {
    RCLCPP_INFO(get_logger(), "Polled: %d", msg->data);
  }
});
```
''',

    "Service": '''
```cpp
using SrvT = example_interfaces::srv::AddTwoInts;
using RequestT = agnocast::Service<SrvT>::RequestT;
using ResponseT = agnocast::Service<SrvT>::ResponseT;

auto service = agnocast::create_service<SrvT>(
  this, "add_two_ints",
  [this](const agnocast::ipc_shared_ptr<RequestT> & req,
         agnocast::ipc_shared_ptr<ResponseT> & res) {
    res->sum = req->a + req->b;
  });
```
''',

    "Client": '''
```cpp
using SrvT = example_interfaces::srv::AddTwoInts;

auto client = agnocast::create_client<SrvT>(this, "add_two_ints");
client->wait_for_service();

// Send a request with a callback
auto req = client->borrow_loaned_request();
req->a = 1;
req->b = 2;
client->async_send_request(std::move(req),
  [this](agnocast::Client<SrvT>::SharedFuture future) {
    RCLCPP_INFO(get_logger(), "Result: %ld", future.get()->sum);
  });

// Or send a request and get a future
auto req2 = client->borrow_loaned_request();
req2->a = 3;
req2->b = 4;
auto future = client->async_send_request(std::move(req2));
RCLCPP_INFO(get_logger(), "Result: %ld", future.get()->sum);
```
''',

    "ipc_shared_ptr": '''
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
''',
}


# ── data ─────────────────────────────────────────────────────────────────────

CLASSES = [
    ("Node", "classagnocast_1_1Node.xml",
     "agnocast::Node",
     None),
    ("Publisher", "classagnocast_1_1BasicPublisher.xml",
     "agnocast::Publisher<MessageT>",
     None),
    ("Subscription", "classagnocast_1_1BasicSubscription.xml",
     "agnocast::Subscription<MessageT>",
     None),
    ("TakeSubscription", "classagnocast_1_1BasicTakeSubscription.xml",
     "agnocast::TakeSubscription<MessageT>",
     None),
    ("PollingSubscriber", "classagnocast_1_1BasicPollingSubscriber.xml",
     "agnocast::PollingSubscriber<MessageT>",
     None),
    ("ipc_shared_ptr", "classagnocast_1_1ipc__shared__ptr.xml",
     "agnocast::ipc_shared_ptr<T>",
     None),
    ("Client", "classagnocast_1_1Client.xml",
     "agnocast::Client<ServiceT>",
     None),
    ("Service", "classagnocast_1_1Service.xml",
     "agnocast::Service<ServiceT>",
     None),
    ("TimerBase", "classagnocast_1_1TimerBase.xml",
     "agnocast::TimerBase",
     None),
    ("GenericTimer", "classagnocast_1_1GenericTimer.xml",
     "agnocast::GenericTimer<FunctorT>",
     None),
    ("WallTimer", "classagnocast_1_1WallTimer.xml",
     "agnocast::WallTimer<FunctorT>",
     None),
]

EXECUTOR_CLASSES = [
    ("AgnocastExecutor", "classagnocast_1_1AgnocastExecutor.xml",
     "agnocast::AgnocastExecutor", None),
    ("SingleThreadedAgnocastExecutor", "classagnocast_1_1SingleThreadedAgnocastExecutor.xml",
     "agnocast::SingleThreadedAgnocastExecutor", None),
    ("MultiThreadedAgnocastExecutor", "classagnocast_1_1MultiThreadedAgnocastExecutor.xml",
     "agnocast::MultiThreadedAgnocastExecutor", None),
    ("CallbackIsolatedAgnocastExecutor", "classagnocast_1_1CallbackIsolatedAgnocastExecutor.xml",
     "agnocast::CallbackIsolatedAgnocastExecutor", None),
    ("AgnocastOnlyExecutor", "classagnocast_1_1AgnocastOnlyExecutor.xml",
     "agnocast::AgnocastOnlyExecutor", None),
    ("AgnocastOnlySingleThreadedExecutor", "classagnocast_1_1AgnocastOnlySingleThreadedExecutor.xml",
     "agnocast::AgnocastOnlySingleThreadedExecutor", None),
    ("AgnocastOnlyMultiThreadedExecutor", "classagnocast_1_1AgnocastOnlyMultiThreadedExecutor.xml",
     "agnocast::AgnocastOnlyMultiThreadedExecutor", None),
    ("AgnocastOnlyCallbackIsolatedExecutor", "classagnocast_1_1AgnocastOnlyCallbackIsolatedExecutor.xml",
     "agnocast::AgnocastOnlyCallbackIsolatedExecutor", None),
]

OPTION_STRUCTS = [
    ("PublisherOptions", "structagnocast_1_1PublisherOptions.xml",
     "agnocast::PublisherOptions"),
    ("SubscriptionOptions", "structagnocast_1_1SubscriptionOptions.xml",
     "agnocast::SubscriptionOptions"),
]


# ── main ─────────────────────────────────────────────────────────────────────

def page_header(title):
    return f"\n# {title}\n\n<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->\n\n"


def write_page(filename, content_fn):
    """Write a page to OUTPUT_DIR/filename."""
    path = OUTPUT_DIR / filename
    f = open(path, "w")
    content_fn(f)
    f.close()
    print(f"  Generated {path}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Collect brief descriptions for the landing page
    landing_entries = []

    # ── Free Functions page ────────────────────────────────────────────────
    def write_free_functions(f):
        f.write(page_header("Free Functions (Stage 1)"))
        f.write("These free functions are used with `rclcpp::Node` at Stage 1. "
                "Pass the node pointer as the first argument.\n\n")
        ns_xml = XML_DIR / "namespaceagnocast.xml"
        if ns_xml.exists():
            funcs = parse_namespace_functions(ns_xml)
            if funcs:
                render_free_functions(f, funcs)

    write_page("free-functions.md", write_free_functions)
    landing_entries.append(("Free Functions (Stage 1)", "free-functions.md",
                            "Free functions for use with `rclcpp::Node` (`create_publisher`, `create_subscription`, etc.)."))

    # ── Type Aliases page ──────────────────────────────────────────────────
    def write_type_aliases(f):
        f.write(page_header("Type Aliases"))
        f.write("These are the user-facing type aliases. Use these types instead of the internal "
                "`Basic*` templates when declaring variables.\n\n")
        ns_xml = XML_DIR / "namespaceagnocast.xml"
        if ns_xml.exists():
            typedefs = parse_namespace_typedefs(ns_xml)
            if typedefs:
                f.write("| Alias | Defined As | Description |\n")
                f.write("|-------|-----------|-------------|\n")
                for name, target, desc in typedefs:
                    f.write(f"| `agnocast::{name}<MessageT>` | `{target}` | {format_prose(desc)} |\n")
                f.write("\n")

    write_page("type-aliases.md", write_type_aliases)
    landing_entries.append(("Type Aliases", "type-aliases.md",
                            "User-facing type aliases (`Publisher`, `Subscription`, `PollingSubscriber`, etc.)."))

    # ── Class pages ────────────────────────────────────────────────────────
    for section_name, xml_file, display_name, desc_override in CLASSES:
        slug = section_name.lower().replace(" ", "-")

        def make_writer(sn, xf, dn, do_):
            def write_cls(f):
                f.write(page_header(sn))
                render_class_section(f, dn, xf, do_, section_name=sn)
            return write_cls

        write_page(f"{slug}.md", make_writer(section_name, xml_file, display_name, desc_override))

        # Get brief for landing page
        xml_path = XML_DIR / xml_file
        cls_desc = ""
        if xml_path.exists():
            parsed = parse_class(xml_path)
            if parsed:
                _, cls_desc, _, _ = parsed
        cls_desc = desc_override or cls_desc
        # Take just the first sentence for the landing page
        first_sentence = cls_desc.split(". ")[0].rstrip(".") + "." if cls_desc else ""
        landing_entries.append((f"`{display_name}`", f"{slug}.md", first_sentence))

    # ── Executors page ─────────────────────────────────────────────────────
    def write_executors(f):
        f.write(page_header("Executors"))
        for section_name, xml_file, display_name, desc_override in EXECUTOR_CLASSES:
            render_class_section(f, display_name, xml_file, desc_override, section_name=section_name)

    write_page("executors.md", write_executors)
    landing_entries.append(("Executors", "executors.md",
                            "Single-threaded, multi-threaded, and callback-isolated executors for Stage 1 and Stage 2."))

    # ── Options page ───────────────────────────────────────────────────────
    def write_options(f):
        f.write(page_header("Options"))
        for section_name, xml_file, display_name in OPTION_STRUCTS:
            render_struct_section(f, display_name, xml_file)

    write_page("options.md", write_options)
    landing_entries.append(("Options", "options.md",
                            "`PublisherOptions` and `SubscriptionOptions` configuration structs."))

    # ── Environment Variables page ──────────────────────────────────────────
    def write_env_vars(f):
        f.write(page_header("Environment Variables"))
        f.write("These environment variables configure Agnocast runtime behavior.\n\n")

        f.write("---\n\n")
        f.write("#### `LD_PRELOAD`\n\n")
        f.write("**Required.** Must include `libagnocast_heaphook.so` to route heap allocations "
                "to shared memory. Agnocast validates this at startup and exits with an error if missing.\n\n")
        f.write("Set it per-node in a launch file:\n\n")
        f.write("```xml\n<node pkg=\"my_package\" exec=\"my_node\" name=\"my_node\" output=\"screen\">\n")
        f.write("    <env name=\"LD_PRELOAD\" value=\"libagnocast_heaphook.so:$(env LD_PRELOAD '')\" />\n")
        f.write("</node>\n```\n\n")

        f.write("---\n\n")
        f.write("#### `AGNOCAST_BRIDGE_MODE`\n\n")
        f.write("Controls the Agnocast–ROS 2 bridge mode for interoperability with standard ROS 2 nodes.\n\n")
        f.write("| Value | Description |\n")
        f.write("|-------|-------------|\n")
        f.write("| `0` or `off` | Bridge disabled. Agnocast topics are not visible to ROS 2 nodes. |\n")
        f.write("| `1` or `standard` | **Standard mode (default).** Each Agnocast process runs its own bridge manager. |\n")
        f.write("| `2` or `performance` | **Performance mode.** A single global bridge manager handles all bridging with pre-compiled plugins for lower overhead. |\n")
        f.write("\nCase-insensitive. Falls back to Standard mode with a warning if an unknown value is given.\n\n")
        f.write("```bash\nexport AGNOCAST_BRIDGE_MODE=standard\n```\n\n")

        f.write("---\n\n")
        f.write("#### `AGNOCAST_BRIDGE_PLUGINS_PATH`\n\n")
        f.write("**Performance mode only.** Colon-separated list of additional search paths for "
                "bridge plugin shared libraries (`.so` files). If not set, plugins are searched in "
                "the default package install location.\n\n")
        f.write("```bash\nexport AGNOCAST_BRIDGE_PLUGINS_PATH=/opt/my_plugins:/home/user/plugins\n```\n\n")

    write_page("environment-variables.md", write_env_vars)
    landing_entries.append(("Environment Variables", "environment-variables.md",
                            "`LD_PRELOAD`, `AGNOCAST_BRIDGE_MODE`, and other runtime configuration variables."))

    # ── Message Filters page ─────────────────────────────────────────────────
    MESSAGE_FILTER_CLASSES = [
        ("Subscriber", "classagnocast_1_1message__filters_1_1Subscriber.xml",
         "agnocast::message_filters::Subscriber<M>", None),
        ("Synchronizer", "classagnocast_1_1message__filters_1_1Synchronizer.xml",
         "agnocast::message_filters::Synchronizer<Policy>", None),
        ("PassThrough", "classagnocast_1_1message__filters_1_1PassThrough.xml",
         "agnocast::message_filters::PassThrough<M>", None),
        ("ExactTime", "structagnocast_1_1message__filters_1_1sync__policies_1_1ExactTime.xml",
         "agnocast::message_filters::sync_policies::ExactTime<M0, M1, ...>", None),
        ("ApproximateTime", "structagnocast_1_1message__filters_1_1sync__policies_1_1ApproximateTime.xml",
         "agnocast::message_filters::sync_policies::ApproximateTime<M0, M1, ...>", None),
    ]

    def write_message_filters(f):
        f.write(page_header("Message Filters"))
        f.write("Agnocast provides message synchronization filters compatible with the ROS 2 "
                "`message_filters` API. These allow you to synchronize messages from multiple "
                "Agnocast topics based on their timestamps.\n\n")

        for section_name, xml_file, display_name, desc_override in MESSAGE_FILTER_CLASSES:
            render_class_section(f, display_name, xml_file, desc_override, section_name=section_name)

        # Full example
        f.write("---\n\n")
        f.write("## Full Example\n\n")
        f.write("```cpp\n")
        f.write('#include "agnocast/agnocast.hpp"\n\n')
        f.write("using MsgA = sensor_msgs::msg::Image;\n")
        f.write("using MsgB = sensor_msgs::msg::CameraInfo;\n")
        f.write("using Policy = agnocast::message_filters::sync_policies::ExactTime<MsgA, MsgB>;\n\n")
        f.write("class MySyncNode : public rclcpp::Node {\n")
        f.write("  agnocast::message_filters::Subscriber<MsgA> sub_a_;\n")
        f.write("  agnocast::message_filters::Subscriber<MsgB> sub_b_;\n")
        f.write("  agnocast::message_filters::Synchronizer<Policy> sync_;\n\n")
        f.write("  void callback(const agnocast::ipc_shared_ptr<const MsgA> & a,\n")
        f.write("                const agnocast::ipc_shared_ptr<const MsgB> & b) {\n")
        f.write("    // Process synchronized messages\n")
        f.write("  }\n\n")
        f.write("public:\n")
        f.write("  MySyncNode() : Node(\"sync_node\"),\n")
        f.write('    sub_a_(this, "/image"),\n')
        f.write('    sub_b_(this, "/camera_info"),\n')
        f.write("    sync_(Policy(10), sub_a_, sub_b_) {\n")
        f.write("    sync_.registerCallback(&MySyncNode::callback, this);\n")
        f.write("  }\n")
        f.write("};\n")
        f.write("```\n\n")

    write_page("message-filters.md", write_message_filters)
    landing_entries.append(("Message Filters", "message-filters.md",
                            "Synchronizer, Subscriber filter, PassThrough, and time sync policies."))

    # ── Landing page ───────────────────────────────────────────────────────
    def write_landing(f):
        f.write("\n# API Reference\n\n")
        f.write("<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->\n\n")
        f.write("!!! info \"Stability Guarantee\"\n")
        f.write("    All API signatures documented here are marked with `AGNOCAST_PUBLIC` in the source code.\n")
        f.write("    These signatures are **stable** and will not break backward compatibility unless the\n")
        f.write("    **major version** is incremented. See the [versioning rules](../environment-setup/index.md)\n")
        f.write("    for details.\n\n")
        f.write("    **Exception:** The [Service](service.md) and [Client](client.md) APIs are **experimental**.\n")
        f.write("    Their signatures may introduce breaking changes without a major version increment.\n\n")
        f.write("| Section | Description |\n")
        f.write("|---------|-------------|\n")
        for title, link, desc in landing_entries:
            f.write(f"| [{title}]({link}) | {format_prose(desc)} |\n")
        f.write("\n")

    write_page("index.md", write_landing)

    # ── .pages navigation file ─────────────────────────────────────────────
    pages_path = OUTPUT_DIR / ".pages"
    with open(pages_path, "w") as f:
        f.write("nav:\n")
        f.write("    - Overview: index.md\n")
        f.write("    - Free Functions: free-functions.md\n")
        f.write("    - Type Aliases: type-aliases.md\n")
        for section_name, _, _, _ in CLASSES:
            slug = section_name.lower().replace(" ", "-")
            f.write(f"    - {section_name}: {slug}.md\n")
        f.write("    - Executors: executors.md\n")
        f.write("    - Options: options.md\n")
        f.write("    - Message Filters: message-filters.md\n")
        f.write("    - Environment Variables: environment-variables.md\n")
    print(f"  Generated {pages_path}")

    print("Done.")


if __name__ == "__main__":
    main()
