#!/usr/bin/env python3
"""Heuristic pre-scan for the java-code-review skill.

Finds likely violations of the house standards (immutability, SRP metrics,
functional style, AssertJ, tests that assert nothing) and, given a JaCoCo XML
report, per-class coverage and uncovered lines.

Everything here is regex/brace-matching based: treat hits as leads to confirm
by reading the code, not as findings.

Usage:
    java_review_scan.py PATH [PATH ...] [--jacoco jacoco.xml]
                        [--line-min 95] [--branch-min 90] [--json]
PATH may be a .java file or a directory (searched recursively).
If --jacoco is omitted, common report locations under each directory are tried.
"""
from __future__ import annotations

import argparse
import bisect
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict, field
from pathlib import Path

SEVERITY_ORDER = {"Blocker": 0, "Major": 1, "Minor": 2, "Nit": 3}


@dataclass
class Hit:
    file: str
    line: int
    severity: str
    tag: str
    message: str


@dataclass
class Metrics:
    file: str
    kind: str  # main | test
    loc: int
    methods: int
    max_ctor_params: int
    fields: int
    long_methods: list = field(default_factory=list)


# --------------------------------------------------------------------------
# Source preprocessing
# --------------------------------------------------------------------------

def _blank(seg: str) -> str:
    return "".join("\n" if ch == "\n" else " " for ch in seg)


def strip_code(src: str) -> str:
    """Blank out comments and string/char literals, preserving line numbers."""
    out, i, n = [], 0, len(src)
    while i < n:
        if src.startswith("//", i):
            j = src.find("\n", i)
            j = n if j == -1 else j
            out.append(_blank(src[i:j]))
            i = j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            j = n if j == -1 else j + 2
            out.append(_blank(src[i:j]))
            i = j
        elif src.startswith('"""', i):
            j = src.find('"""', i + 3)
            j = n if j == -1 else j + 3
            out.append('"' + _blank(src[i + 1:j - 1]) + '"')
            i = j
        elif src[i] in "\"'":
            q, j = src[i], i + 1
            while j < n and src[j] not in (q, "\n"):
                j += 2 if src[j] == "\\" else 1
            if j < n and src[j] == q:
                out.append(q + _blank(src[i + 1:j]) + q)
                i = j + 1
            else:  # unterminated - keep line structure
                out.append(_blank(src[i:j]))
                i = j
        else:
            out.append(src[i])
            i += 1
    return "".join(out)


def comment_lines(src: str) -> set:
    """1-based numbers of the lines that contain (part of) a comment."""
    lines, i, n, line = set(), 0, len(src), 1
    while i < n:
        if src.startswith("//", i):
            lines.add(line)
            j = src.find("\n", i)
            i = n if j == -1 else j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            j = n if j == -1 else j + 2
            for k in range(line, line + src.count("\n", i, j) + 1):
                lines.add(k)
            line += src.count("\n", i, j)
            i = j
        elif src.startswith('"""', i):
            j = src.find('"""', i + 3)
            j = n if j == -1 else j + 3
            line += src.count("\n", i, j)
            i = j
        elif src[i] in "\"'":
            q, j = src[i], i + 1
            while j < n and src[j] not in (q, "\n"):
                j += 2 if src[j] == "\\" else 1
            i = j + 1 if j < n and src[j] == q else j
        else:
            if src[i] == "\n":
                line += 1
            i += 1
    return lines


class Justification:
    """A construct is justified when a comment sits on its line or the line directly above."""

    def __init__(self, src: str):
        self.lines = comment_lines(src)

    def __call__(self, line: int) -> bool:
        return line in self.lines or (line - 1) in self.lines


class LineIndex:
    def __init__(self, text: str):
        self.starts = [0] + [m.end() for m in re.finditer(r"\n", text)]

    def line(self, pos: int) -> int:
        return bisect.bisect_right(self.starts, pos)


def match_brace(text: str, open_pos: int, open_ch="{", close_ch="}") -> int:
    depth = 0
    for k in range(open_pos, len(text)):
        if text[k] == open_ch:
            depth += 1
        elif text[k] == close_ch:
            depth -= 1
            if depth == 0:
                return k
    return len(text) - 1


def parse_imports(text: str) -> dict:
    """simple name -> package, plus '*' entries for wildcard packages."""
    imports = {"*": []}
    for m in re.finditer(r"^\s*import\s+(static\s+)?([\w.]+)(\.\*)?\s*;", text, re.M):
        if m.group(1):
            continue
        name = m.group(2)
        if m.group(3):
            imports["*"].append(name)
        else:
            pkg, _, simple = name.rpartition(".")
            imports[simple] = pkg
    return imports


def uses_vavr(imports: dict, text: str) -> bool:
    return any(p.startswith("io.vavr") for k, p in imports.items() if k != "*") or \
        any(p.startswith("io.vavr") for p in imports["*"]) or "io.vavr." in text


MUTABLE_JAVA_TYPES = {
    "ArrayList", "LinkedList", "HashMap", "LinkedHashMap", "TreeMap", "HashSet",
    "LinkedHashSet", "TreeSet", "ArrayDeque", "Vector", "Stack", "Hashtable",
    "Date", "Calendar", "StringBuilder", "StringBuffer", "EnumMap", "EnumSet",
    "ConcurrentHashMap", "CopyOnWriteArrayList", "PriorityQueue",
}
JAVA_INTERFACE_TYPES = {"List", "Map", "Set", "Collection", "Queue", "Deque",
                        "Iterator", "SortedMap", "SortedSet", "NavigableMap"}


def is_mutable_type(type_str: str, imports: dict) -> bool:
    if "[]" in type_str:
        return True
    if re.search(r"\bjava\.util\.", type_str):
        return True
    head = re.match(r"\s*([\w.]+)", type_str)
    if not head:
        return False
    simple = head.group(1).rsplit(".", 1)[-1]
    if simple in MUTABLE_JAVA_TYPES and imports.get(simple, "java.util").startswith("java."):
        return True
    if simple in JAVA_INTERFACE_TYPES:
        pkg = imports.get(simple)
        if pkg is not None:
            return pkg == "java.util"
        wild = imports["*"]
        return "java.util" in wild and not any(w.startswith("io.vavr") for w in wild)
    return False


# --------------------------------------------------------------------------
# Main-code checks
# --------------------------------------------------------------------------

LINE_RULES_MAIN = [
    (r"\bnew\s+(ArrayList|LinkedList|HashMap|LinkedHashMap|TreeMap|HashSet|LinkedHashSet|TreeSet|"
     r"ArrayDeque|Vector|Stack|Hashtable|PriorityQueue|ConcurrentHashMap|CopyOnWriteArrayList)\b",
     "Major", "Immutability", "Mutable java.util collection '{0}' - use a vavr persistent collection"),
    (r"\bnew\s+(Date|GregorianCalendar)\s*\(", "Major", "Immutability",
     "Mutable date type '{0}' - use java.time"),
    (r"\b(?:public|protected)?\s*void\s+(set[A-Z]\w*)\s*\(", "Major", "Immutability",
     "Setter '{0}' - return a new value (wither) instead"),
    (r"@(Data|Setter)\b", "Major", "Immutability", "Lombok @{0} generates mutators - use @Value/@With"),
    (r"\breturn\s+null\s*;", "Major", "Functional", "Returns null - return Option/Either instead"),
    (r"catch\s*\([^)]*\)\s*\{\s*\}", "Major", "Functional", "Empty catch block - use Try/Either or handle it"),
    (r"throw\s+new\s+UnsupportedOperationException\b", "Major", "LSP",
     "UnsupportedOperationException - likely LSP/ISP violation if this overrides a supertype method"),
    (r"\bCollectors\.(toList|toSet|toMap)\s*\(", "Minor", "Immutability",
     "Collectors.{0}() yields a mutable collection - use Stream.toList() or vavr collectors"),
    (r"\bArrays\.asList\s*\(", "Minor", "Immutability", "Arrays.asList is mutable (set) - use List.of / vavr List.of"),
    (r"\.\s*(isPresent|isDefined)\s*\(\s*\)", "Minor", "Functional",
     "{0}() check - prefer map/flatMap/fold/getOrElse"),
    (r"\b(LocalDateTime|LocalDate|Instant|ZonedDateTime|OffsetDateTime)\.now\s*\(\s*\)", "Minor", "DIP",
     "{0}.now() - inject a Clock"),
    (r"\bSystem\.currentTimeMillis\s*\(|\bUUID\.randomUUID\s*\(|\bnew\s+Random\s*\(", "Minor", "DIP",
     "Hidden time/randomness dependency - inject a Clock/Supplier"),
    (r"\bnew\s+(\w+(?:Service|Repository|Client|Dao|Gateway|Adapter))\s*\(", "Major", "DIP",
     "Instantiates collaborator '{0}' - inject it via the constructor"),
    (r"(?:==|!=)\s*null\b|\bnull\s*(?:==|!=)", "Minor", "Functional",
     "Null check - model absence with Option at the boundary"),
]

DISCARD_METHODS = ["add", "addAll", "put", "putAll", "remove", "removeAll", "clear", "set",
                   "removeIf", "sort", "replaceAll", "retainAll", "push", "offer", "poll"]
VAVR_DISCARD_METHODS = ["append", "appendAll", "prepend", "prependAll", "insert", "update",
                        "merge", "filter", "map", "reject"]

TYPE_HEADER = re.compile(r"\b(class|interface|enum|record)\s+(\w+)")
METHOD_HEADER = re.compile(r"(\w+)\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)\s*(?:throws[\w\s,.]+)?$", re.S)
CONTROL_WORDS = {"if", "for", "while", "switch", "catch", "synchronized", "try", "do", "else", "return", "new"}


def strip_leading_annotations(stmt: str):
    anns, s = [], stmt.lstrip()
    while s.startswith("@"):
        m = re.match(r"@([\w.]+)\s*", s)
        name, s2 = m.group(1), s[m.end():]
        if s2.startswith("("):
            end = match_brace(s2, 0, "(", ")")
            s2 = s2[end + 1:]
        anns.append(name)
        s = s2.lstrip()
    return anns, s


LOCAL_DECLARATION = re.compile(
    r"^(final\s+)?([\w.$]+(?:\s*<[^;=(){}]*>)?(?:\s*\[\s*\])*)\s+([A-Za-z_$][\w$]*)\s*(?:=|$|\[|,)", re.S)
NOT_A_TYPE = {"return", "throw", "new", "else", "case", "default", "assert", "yield", "break", "continue", "do",
              "try", "finally", "synchronized", "if", "for", "while", "switch", "catch", "this", "super",
              "package", "import", "goto"}


def check_parameters(path, params, line, method, kind, hits, justified):
    if justified(line):
        return
    for p in params:
        _, decl = strip_leading_annotations(p)
        tokens = decl.split()
        if len(tokens) >= 2 and tokens[0] != "final":
            hits.append(Hit(path, line, "Major" if kind == "main" else "Minor", "Immutability",
                            f"Parameter '{tokens[-1]}' of '{method}' is not final - declare it final, "
                            f"or say beside it why it must be reassigned"))


def check_local(path, stmt, start, idx, kind, hits, justified):
    _, s = strip_leading_annotations(stmt)
    s = s.strip()
    m = LOCAL_DECLARATION.match(s)
    if not m or m.group(1) or m.group(2).split("<")[0].strip() in NOT_A_TYPE:
        return
    line = idx.line(start + stmt.index(s[:1])) if s else idx.line(start)
    if not justified(line):
        hits.append(Hit(path, line, "Major" if kind == "main" else "Minor", "Immutability",
                        f"Local '{m.group(3)}' is not final - declare it final, "
                        f"or say beside it why it must be reassigned"))


def scan_structure(path, text, idx, imports, kind, hits, justified=lambda line: False):
    """Walk braces: fields, methods, constructor params, long methods."""
    stack = []  # entries: dict(kind='type'|'block', name, enum_first)
    stmt_start = 0
    methods = fields = max_ctor = 0
    long_methods = []
    type_names = []
    method_spans = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch == "{":
            header = text[stmt_start:i]
            _, hdr = strip_leading_annotations(header)
            tm = TYPE_HEADER.search(hdr)
            if tm and "=" not in hdr.split(tm.group(0))[0] and not re.search(r"\bnew\b", hdr):
                stack.append({"kind": "type", "name": tm.group(2), "enum": tm.group(1) == "enum",
                              "iface": tm.group(1) == "interface" or "@interface" in hdr,
                              "first": True})
                type_names.append(tm.group(2))
                if tm.group(1) == "record" and kind == "main":
                    check_record_components(path, hdr, i - len(header) + (len(header) - len(hdr)),
                                            idx, imports, hits)
            else:
                parent_is_type = bool(stack) and stack[-1]["kind"] == "type"
                mm = METHOD_HEADER.search(hdr.strip())
                if parent_is_type and mm and mm.group(1) not in CONTROL_WORDS and "=" not in hdr:
                    methods += 1
                    params = [p for p in re.split(r",(?![^<]*>)", mm.group(2)) if p.strip()]
                    check_parameters(path, params, idx.line(i), mm.group(1), kind, hits, justified)
                    if mm.group(1) == stack[-1]["name"]:
                        max_ctor = max(max_ctor, len(params))
                    end = match_brace(text, i)
                    span = idx.line(end) - idx.line(i) - 1
                    method_spans.append((mm.group(1), idx.line(i), span))
                stack.append({"kind": "block"})
            stmt_start = i + 1
        elif ch == "}":
            if stack:
                stack.pop()
            stmt_start = i + 1
        elif ch == ";":
            if stack and stack[-1]["kind"] == "type":
                top = stack[-1]
                stmt = text[stmt_start:i]
                if top["enum"] and top["first"]:
                    top["first"] = False
                elif top["iface"]:
                    pass  # interface fields are implicitly public static final
                else:
                    check_field(path, stmt, stmt_start, idx, imports, kind, hits, justified)
                    if re.search(r"\w", stmt) and "(" not in stmt.split("=")[0]:
                        fields += 1
            elif stack and stack[-1]["kind"] == "block":
                check_local(path, text[stmt_start:i], stmt_start, idx, kind, hits, justified)
            stmt_start = i + 1
        i += 1
    for name, line, span in method_spans:
        if span > 25:
            long_methods.append(f"{name}@{line} ({span} lines)")
            if kind == "main":
                hits.append(Hit(path, line, "Minor", "SRP",
                                f"Method '{name}' is {span} lines - check it does one thing at one abstraction level"))
    return methods, fields, max_ctor, long_methods, type_names


def check_field(path, stmt, start, idx, imports, kind, hits, justified=lambda line: False):
    anns, s = strip_leading_annotations(stmt)
    if not s.strip():
        return
    decl = s.split("=", 1)[0]
    if "(" in decl:  # method declaration (abstract/interface) or odd syntax
        return
    tokens = decl.split()
    if len(tokens) < 2:
        return
    line = idx.line(start + (len(stmt) - len(stmt.lstrip())))
    mods = set(t for t in tokens if t in {"public", "private", "protected", "static", "final",
                                          "transient", "volatile"})
    name = tokens[-1]
    type_str = " ".join(t for t in tokens[:-1] if t not in mods)
    if kind == "test":
        if "static" in mods and "final" not in mods:
            hits.append(Hit(path, line, "Minor", "Tests", f"Mutable static field '{name}' in test"))
        return
    if any(a in ("Autowired", "Inject") for a in anns):
        hits.append(Hit(path, line, "Major", "DIP",
                        f"Field injection on '{name}' - use constructor injection with a final field"))
    if "final" not in mods and justified(line):
        return  # reassignment explained by an adjacent comment; the reviewer judges whether it holds
    if "static" in mods and "final" not in mods:
        hits.append(Hit(path, line, "Blocker", "Immutability", f"Mutable static field '{name}'"))
    elif "final" not in mods:
        hits.append(Hit(path, line, "Major", "Immutability",
                        f"Non-final field '{name}' - declare it final, or say beside it why it must be reassigned"))
    elif is_mutable_type(type_str, imports):
        sev = "Blocker" if "static" in mods else "Major"
        hits.append(Hit(path, line, sev, "Immutability",
                        f"Final field '{name}' references mutable type '{type_str.strip()}'"))


def check_record_components(path, hdr, hdr_pos, idx, imports, hits):
    m = re.search(r"\brecord\s+\w+\s*(<[^>]*>)?\s*\(", hdr)
    if not m:
        return
    close = match_brace(hdr, m.end() - 1, "(", ")")
    params = [p for p in re.split(r",(?![^<]*>)", hdr[m.end():close]) if p.strip()]
    for p in params:
        _, decl = strip_leading_annotations(p)
        tokens = decl.split()
        if len(tokens) >= 2 and is_mutable_type(" ".join(tokens[:-1]), imports):
            hits.append(Hit(path, idx.line(hdr_pos + m.start()), "Major", "Immutability",
                            f"Record component '{tokens[-1]}' has mutable type '{' '.join(tokens[:-1])}' "
                            f"- use a vavr collection or copy defensively"))


CONTROL_STATEMENT = re.compile(r"\b(if|for|while|switch)\s*\(|\b(do)\s*\{")
def closes_do_block(text: str, pos: int) -> bool:
    before = text[:pos].rstrip()
    if not before.endswith("}"):
        return False
    depth = 0
    for k in range(len(before) - 1, -1, -1):
        depth += {"}": 1, "{": -1}.get(before[k], 0)
        if depth == 0:
            return re.search(r"\bdo\s*$", before[:k]) is not None
    return False


CATCH_PARAMETER = re.compile(r"\bcatch\s*\(\s*(?!final\b)([\w.|\s]+?)\s+(\w+)\s*\)")


def scan_main(path, raw, text, idx, imports, hits, justified=lambda line: False):
    vavr = uses_vavr(imports, text)
    for m in CONTROL_STATEMENT.finditer(text):
        line = idx.line(m.start())
        if m.group(1) == "while" and closes_do_block(text, m.start()):
            continue  # the tail of a do ... while, already reported at its 'do'
        if not justified(line):
            keyword = m.group(1) or m.group(2)
            hits.append(Hit(path, line, "Major", "Functional",
                            f"'{keyword}' statement with no justifying comment - express it with "
                            f"map/filter/fold, Option, polymorphism or a lookup, or say beside it why it is required"))
    for pattern, sev, tag, msg in LINE_RULES_MAIN:
        for m in re.finditer(pattern, text):
            arg = m.group(1) if m.groups() and m.group(1) else m.group(0).strip()
            hits.append(Hit(path, idx.line(m.start()), sev, tag, msg.format(arg)))
    methods = DISCARD_METHODS + (VAVR_DISCARD_METHODS if vavr else [])
    discard = re.compile(r"^\s*(?!return\b)[\w.$\[\]]+?\.(" + "|".join(methods) + r")\s*\(", re.M)
    for m in discard.finditer(text):
        line_end = text.find("\n", m.start())
        line_txt = text[m.start():line_end if line_end != -1 else len(text)]
        if "=" in line_txt.split(".", 1)[0] or "->" in line_txt:
            continue
        hits.append(Hit(path, idx.line(m.start()), "Major", "Immutability",
                        f"Result of .{m.group(1)}(...) discarded - either mutation, or a no-op on a "
                        f"persistent collection (bug)"))
    if re.search(r"^\s*import\s+java\.util\.Optional\s*;", text, re.M) and vavr:
        hits.append(Hit(path, 1, "Nit", "Functional", "Mixes java.util.Optional with vavr - prefer Option"))
    instanceof_count = len(re.findall(r"\binstanceof\b", text))
    if instanceof_count >= 2 and not re.search(r"\bsealed\b", text):
        hits.append(Hit(path, 1, "Minor", "OCP",
                        f"{instanceof_count} instanceof checks - type switching over an open hierarchy?"))


# --------------------------------------------------------------------------
# Test-code checks
# --------------------------------------------------------------------------

TEST_ANN = re.compile(r"@(Test|ParameterizedTest|RepeatedTest|TestFactory|TestTemplate|Property|Example)\b")
ASSERT_CALL = re.compile(r"\b(assert\w*|verify\w*|then\w*|expect\w*|should\w*)\s*\(")
NON_ASSERTING_CHAIN = {"as", "describedAs", "withFailMessage", "overridingErrorMessage",
                       "usingComparator", "usingRecursiveComparison", "withRepresentation",
                       "usingDefaultComparator", "extracting", "asInstanceOf"}
WEAK_CHAIN = {"isNotNull", "doesNotThrowAnyException"}
WEAK_JUNIT = {"assertNotNull", "assertDoesNotThrow"}
MOCK_STUBBING = {"thenReturn", "thenThrow", "thenAnswer", "thenCallRealMethod", "expectLastCall"}
JUNIT_STYLE = re.compile(r"\b(assertEquals|assertNotEquals|assertTrue|assertFalse|assertNull|"
                         r"assertNotNull|assertThrows|assertSame|assertArrayEquals|assertIterableEquals)\s*\(")


def chain_methods(body: str, after: int) -> list:
    names, k = [], after
    while True:
        m = re.match(r"\s*\.\s*(\w+)\s*(<[^>]*>)?\s*\(", body[k:])
        if not m:
            return names
        names.append(m.group(1))
        open_pos = k + m.end() - 1
        k = match_brace(body, open_pos, "(", ")") + 1


def find_test_methods(text):
    for m in TEST_ANN.finditer(text):
        k = m.end()
        if k < len(text) and text[k:].lstrip().startswith("("):
            k = match_brace(text, text.index("(", k), "(", ")") + 1
        # skip further annotations
        _, rest = strip_leading_annotations(text[k:])
        k = len(text) - len(rest)
        mm = re.search(r"(\w+)\s*\(", text[k:])
        if not mm:
            continue
        name = mm.group(1)
        paren = k + mm.end() - 1
        close = match_brace(text, paren, "(", ")")
        brace = text.find("{", close)
        semi = text.find(";", close)
        if brace == -1 or (semi != -1 and semi < brace):
            continue
        end = match_brace(text, brace)
        yield m, name, brace, text[brace + 1:end], text[m.start():brace]


def scan_test(path, text, idx, hits):
    junit = JUNIT_STYLE.findall(text)
    hamcrest = re.search(r"import\s+(static\s+)?org\.hamcrest", text)
    if junit or hamcrest:
        what = f"{len(junit)} JUnit assertion(s)" if junit else ""
        what += (" + " if junit and hamcrest else "") + ("Hamcrest" if hamcrest else "")
        hits.append(Hit(path, 1, "Minor", "Tests", f"{what} - use AssertJ"))
    for m in re.finditer(r"@(Disabled|Ignore)\b", text):
        hits.append(Hit(path, idx.line(m.start()), "Minor", "Tests", f"@{m.group(1)} test"))

    for ann, name, brace, body, header in find_test_methods(text):
        line = idx.line(brace)
        expected_attr = re.search(r"expected\s*=", header)
        calls = list(ASSERT_CALL.finditer(body))
        real, weak_only, empty_chains, verify_only = 0, True, 0, True
        for c in calls:
            fname = c.group(1)
            if fname in MOCK_STUBBING:
                continue
            before = body[:c.start()].rstrip()
            if fname.startswith("then") and before.endswith("."):
                continue  # a method named then(...) on some object, e.g. function composition
            if before.endswith("->"):
                continue  # inside a lambda such as isThrownBy(() -> ...); not the test's assertion
            close = match_brace(body, c.end() - 1, "(", ")")
            if before.endswith("=") or re.search(r"\breturn$", before):
                real += 1  # assertion object stored or returned; chain happens elsewhere
                weak_only = verify_only = False
                continue
            if fname.startswith("assertThat") or fname in ("then", "thenThrownBy", "thenCode"):
                checking = [x for x in chain_methods(body, close + 1) if x not in NON_ASSERTING_CHAIN]
                if not checking:
                    empty_chains += 1
                    hits.append(Hit(path, idx.line(brace + 1 + c.start()), "Blocker", "Tests",
                                    f"'{name}': {fname}(...) with no assertion chained - checks nothing"))
                    continue
                real += 1
                verify_only = False
                if not set(checking) <= WEAK_CHAIN:
                    weak_only = False
                continue
            real += 1
            if not fname.startswith("verify"):
                verify_only = False
            if fname not in WEAK_JUNIT:
                weak_only = False
        has_fail = re.search(r"\bfail\s*\(", body)
        if real == 0 and empty_chains == 0 and not expected_attr and not has_fail:
            hits.append(Hit(path, line, "Blocker", "Tests",
                            f"Test '{name}' has no recognisable assertion (verify: custom helper?)"))
        elif real > 0 and weak_only:
            hits.append(Hit(path, line, "Major", "Tests",
                            f"Test '{name}' only asserts non-null / no-exception - assert on the value"))
        if real > 0 and verify_only:
            hits.append(Hit(path, line, "Minor", "Tests",
                            f"'{name}' only verifies mock interactions - confirm it tests behaviour, "
                            f"not implementation"))
        if expected_attr:
            hits.append(Hit(path, line, "Minor", "Tests",
                            f"'{name}' uses @Test(expected=...) - use assertThatThrownBy"))
        if has_fail and re.search(r"\bcatch\s*\(", body):
            hits.append(Hit(path, line, "Major", "Tests",
                            f"'{name}' uses try/fail/catch - use assertThatThrownBy(...).isInstanceOf(...)"))
        if re.search(r"\b(if|for|while)\s*\(", body):
            hits.append(Hit(path, line, "Minor", "Tests",
                            f"'{name}' contains logic (if/loop) - use @ParameterizedTest"))
        if re.search(r"\bThread\.sleep\s*\(", body):
            hits.append(Hit(path, line, "Minor", "Tests", f"'{name}' uses Thread.sleep"))
        if re.search(r"\bSystem\.(out|err)\.", body):
            hits.append(Hit(path, line, "Nit", "Tests", f"'{name}' prints to System.out/err"))


# --------------------------------------------------------------------------
# Coverage
# --------------------------------------------------------------------------

def ranges(nums):
    out, start, prev = [], None, None
    for x in nums:
        if start is None:
            start = prev = x
        elif x == prev + 1:
            prev = x
        else:
            out.append(f"{start}" if start == prev else f"{start}-{prev}")
            start = prev = x
    if start is not None:
        out.append(f"{start}" if start == prev else f"{start}-{prev}")
    return out


def counters(el):
    return {c.get("type"): (int(c.get("missed")), int(c.get("covered"))) for c in el.findall("counter")}


def pct(pair):
    missed, covered = pair
    total = missed + covered
    return None if total == 0 else 100.0 * covered / total


def read_jacoco(path: Path, line_min: float, branch_min: float):
    root = ET.parse(path).getroot()
    overall = counters(root)
    classes, below = [], []
    for pkg in root.findall("package"):
        uncovered = {}
        for sf in pkg.findall("sourcefile"):
            miss = [int(l.get("nr")) for l in sf.findall("line")
                    if int(l.get("ci")) == 0 and int(l.get("mi")) > 0]
            part = [int(l.get("nr")) for l in sf.findall("line")
                    if int(l.get("mb", 0)) > 0 and (int(l.get("cb", 0)) > 0 or int(l.get("ci")) > 0)]
            uncovered[sf.get("name")] = (miss, part)
        for cl in pkg.findall("class"):
            c = counters(cl)
            lp, bp = pct(c.get("LINE", (0, 0))), pct(c.get("BRANCH", (0, 0)))
            src = cl.get("sourcefilename")
            miss, part = uncovered.get(src, ([], []))
            entry = {"class": cl.get("name").replace("/", "."), "source": src,
                     "line_pct": lp, "branch_pct": bp,
                     "uncovered_lines": ranges(miss), "partial_branch_lines": ranges(part)}
            classes.append(entry)
            if (lp is not None and lp < line_min) or (bp is not None and bp < branch_min):
                below.append(entry)
    return {"report": str(path),
            "line_pct": pct(overall.get("LINE", (0, 0))),
            "branch_pct": pct(overall.get("BRANCH", (0, 0))),
            "classes": len(classes), "below_threshold": below}


JACOCO_CANDIDATES = ["target/site/jacoco/jacoco.xml",
                     "build/reports/jacoco/test/jacocoTestReport.xml",
                     "target/site/jacoco-aggregate/jacoco.xml"]


def find_jacoco(paths):
    for p in paths:
        base = Path(p)
        if base.is_dir():
            for cand in JACOCO_CANDIDATES:
                if (base / cand).exists():
                    return base / cand
            for found in base.rglob("jacoco*.xml"):
                return found
    return None


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def is_test_file(p: Path) -> bool:
    s = p.as_posix()
    return "/src/test/" in s or bool(re.search(r"(Test|Tests|IT|Spec)\.java$", p.name))


def collect(paths):
    files = []
    for p in paths:
        pp = Path(p)
        if pp.is_file() and pp.suffix == ".java":
            files.append(pp)
        elif pp.is_dir():
            files.extend(f for f in sorted(pp.rglob("*.java"))
                         if not any(part in {"target", "build", "generated", ".git"} for part in f.parts))
    return files


def scan_file(p: Path):
    raw = p.read_text(encoding="utf-8", errors="replace")
    text = strip_code(raw)
    idx = LineIndex(text)
    imports = parse_imports(text)
    kind = "test" if is_test_file(p) else "main"
    justified = Justification(raw)
    hits = []
    methods, fields, max_ctor, long_methods, types = scan_structure(str(p), text, idx, imports, kind, hits, justified)
    for m in CATCH_PARAMETER.finditer(text):
        line = idx.line(m.start())
        if not justified(line):
            hits.append(Hit(str(p), line, "Major" if kind == "main" else "Minor", "Immutability",
                            f"Catch parameter '{m.group(2)}' is not final"))
    loc = sum(1 for l in text.splitlines() if l.strip() and not l.strip().startswith(("import", "package")))
    if kind == "main":
        scan_main(str(p), raw, text, idx, imports, hits, justified)
        name_smell = [t for t in types if re.search(r"(Manager|Helper|Utils?|Processor)$|And[A-Z]", t)]
        for t in name_smell:
            hits.append(Hit(str(p), 1, "Minor", "SRP", f"Type name '{t}' suggests a grab-bag of responsibilities"))
        if loc > 200:
            hits.append(Hit(str(p), 1, "Major", "SRP", f"{loc} lines of code - check for multiple responsibilities"))
        if max_ctor > 4:
            hits.append(Hit(str(p), 1, "Major", "SRP",
                            f"Constructor takes {max_ctor} parameters - many collaborators, likely several jobs"))
        if methods > 15:
            hits.append(Hit(str(p), 1, "Minor", "SRP", f"{methods} methods - check cohesion"))
    else:
        scan_test(str(p), text, idx, hits)
    return hits, Metrics(str(p), kind, loc, methods, max_ctor, fields, long_methods)


def dedupe(hits):
    seen, out = set(), []
    for h in hits:
        key = (h.file, h.line, h.tag, h.message)
        if key not in seen:
            seen.add(key)
            out.append(h)
    return out


def render_markdown(hits, metrics, coverage, line_min, branch_min):
    lines = ["# java-code-review pre-scan (heuristic - confirm each hit)", ""]
    counts = {s: sum(1 for h in hits if h.severity == s) for s in SEVERITY_ORDER}
    n_main = sum(1 for m in metrics if m.kind == "main")
    lines.append(f"Files: {n_main} main, {len(metrics) - n_main} test. Hits: " +
                 ", ".join(f"{v} {k}" for k, v in counts.items()))
    lines.append("")
    if n_main and len(metrics) == n_main:
        lines += ["**No test files found in scope.**", ""]
    by_file = {}
    for h in hits:
        by_file.setdefault(h.file, []).append(h)
    for f in sorted(by_file):
        lines.append(f"## {f}")
        for h in sorted(by_file[f], key=lambda h: (SEVERITY_ORDER[h.severity], h.line)):
            lines.append(f"- L{h.line} **{h.severity}** [{h.tag}] {h.message}")
        lines.append("")
    lines.append("## Size metrics (main code)")
    lines.append("| File | LOC | Methods | Max ctor params | Fields |")
    lines.append("|---|---|---|---|---|")
    for m in metrics:
        if m.kind == "main":
            lines.append(f"| {Path(m.file).name} | {m.loc} | {m.methods} | {m.max_ctor_params} | {m.fields} |")
    lines.append("")
    lines.append("## Coverage")
    if coverage is None:
        lines.append("No JaCoCo report found - coverage must be generated or estimated by hand.")
    else:
        fmt = lambda v: "n/a" if v is None else f"{v:.1f}%"
        lines.append(f"Report: {coverage['report']} - overall {fmt(coverage['line_pct'])} line, "
                     f"{fmt(coverage['branch_pct'])} branch across {coverage['classes']} classes. "
                     f"Thresholds: {line_min}% line / {branch_min}% branch.")
        if coverage["below_threshold"]:
            lines += ["", "| Class | Line | Branch | Uncovered lines | Partial branches |", "|---|---|---|---|---|"]
            for c in coverage["below_threshold"]:
                lines.append(f"| {c['class']} | {fmt(c['line_pct'])} | {fmt(c['branch_pct'])} | "
                             f"{', '.join(c['uncovered_lines']) or '-'} | {', '.join(c['partial_branch_lines']) or '-'} |")
        else:
            lines.append("All classes meet the thresholds.")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--jacoco")
    ap.add_argument("--line-min", type=float, default=95.0)
    ap.add_argument("--branch-min", type=float, default=90.0)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    files = collect(args.paths)
    if not files:
        print("No .java files found.", file=sys.stderr)
        return 1
    all_hits, metrics = [], []
    for f in files:
        try:
            h, m = scan_file(f)
        except Exception as e:  # keep going on odd files
            print(f"warning: could not scan {f}: {e}", file=sys.stderr)
            continue
        all_hits += h
        metrics.append(m)
    all_hits = dedupe(all_hits)

    jacoco = Path(args.jacoco) if args.jacoco else find_jacoco(args.paths)
    coverage = None
    if jacoco:
        try:
            coverage = read_jacoco(jacoco, args.line_min, args.branch_min)
        except Exception as e:
            print(f"warning: could not read JaCoCo report {jacoco}: {e}", file=sys.stderr)

    if args.json:
        print(json.dumps({"hits": [asdict(h) for h in all_hits],
                          "metrics": [asdict(m) for m in metrics],
                          "coverage": coverage}, indent=2))
    else:
        print(render_markdown(all_hits, metrics, coverage, args.line_min, args.branch_min))
    return 0


if __name__ == "__main__":
    sys.exit(main())
