# SOLID checklist

## S - Single responsibility (top priority)

A class should have one reason to change: one actor or concern whose changing
requirements would force edits to it. SRP applies to methods too.

### How to detect a violation
Read the class and write its responsibility in one sentence. Then check:

- **The sentence needs "and"** ("validates orders *and* saves them *and* emails
  the customer").
- **Name smells**: `*Manager`, `*Helper`, `*Util(s)`, `*Processor`, `*Handler`
  (generic), `*And*`, `Common*`, `Base*` holding unrelated behaviour.
- **Low cohesion**: fields split into groups that are used by disjoint groups of
  methods. Each group is a candidate class.
- **Many collaborators**: more than ~4 constructor dependencies usually means
  more than one job.
- **Imports span layers**: persistence (`javax.persistence`, JDBC), transport
  (HTTP, JSON), formatting, and business rules in one file.
- **Size**: > ~200 lines or > ~15 public methods is a prompt to look hard (not
  a violation by itself).
- **Mixed abstraction levels in a method**: a method that orchestrates
  high-level steps and also does string parsing or SQL is doing two jobs.
- **Methods > ~20 lines**, or with sections separated by blank lines/comments
  ("// now build the response") - each section is a method or a class.
- **Boolean/flag parameters** that switch behaviour: two responsibilities
  sharing one method.
- **Tests that need elaborate setup of unrelated collaborators** to exercise one
  behaviour - the class under test is doing too much.

### How to write the fix
Give a design sketch: new types, one-sentence responsibility each, which
members move where, and how the original class now composes them.

```
OrderService (validates, prices, persists, notifies)  ->
  OrderValidator   - decides whether an order is acceptable: Validation<Seq<Error>, Order>
  PriceCalculator  - computes totals from lines and discounts (pure function)
  OrderRepository  - persists orders (interface; infra implements it)
  OrderNotifier    - tells the customer about accepted orders (interface)
  PlaceOrder       - use case: validate -> price -> save -> notify
```

Prefer pure-function classes (or static functions on records) for the business
rules so they need no mocks to test.

## O - Open/closed

Adding a new variant of behaviour should mean adding code, not editing
existing branches in many places.

Flag:
- `if/else if` chains or `switch` on a type code/enum that are **repeated** in
  several places.
- `instanceof` chains over an **open** hierarchy.
- Methods that grow a new branch every time a feature is added.

Fix with polymorphism (strategy interface, one implementation per variant) or,
where the set of variants is genuinely closed, a `sealed` interface with
records, with the behaviour as a method on the interface. An exhaustive
pattern-matching `switch` over the sealed types (no `default`, so the compiler
finds every place to update) is acceptable only with a comment justifying the
`switch` (see functional-style.md). The sealed approach is *not* an OCP
violation - it's a deliberate closed world.

## L - Liskov substitution

A subtype must be usable anywhere its supertype is, without surprises.

Flag:
- Overrides that throw `UnsupportedOperationException` or do nothing.
- Overrides that strengthen preconditions (reject inputs the parent accepts) or
  weaken postconditions (return null where the parent never does).
- Callers doing `instanceof`/casts to special-case a subtype.
- Inheritance used for code reuse rather than an is-a relation - prefer
  composition. With immutability, most domain types should be `final` or
  records anyway.

## I - Interface segregation

Flag:
- Interfaces where implementers leave methods empty or throwing.
- Clients that depend on an interface but use one or two of its many methods.
- "Repository" interfaces with twenty query methods used by different features.

Fix: split into role interfaces named for what the client needs
(`OrderLookup`, `OrderWriter`). Functional interfaces (`Function`, `Supplier`,
custom `@FunctionalInterface`) are the smallest interface and fit the
functional style well.

## D - Dependency inversion

High-level policy depends on abstractions it owns; details implement them.

Flag:
- `new SomeService()`, `new SomeRepository()`, `new HttpClient...` inside
  business logic.
- Static calls to infrastructure from domain code (`Database.save(...)`,
  singletons).
- Hidden dependencies on time and randomness: `Instant.now()`,
  `LocalDateTime.now()`, `System.currentTimeMillis()`, `UUID.randomUUID()`,
  `new Random()`. Inject a `Clock` or a `Supplier<UUID>` - this also makes
  tests deterministic.
- Field injection (`@Autowired`/`@Inject` on fields). Use constructor
  injection with `final` fields - it's also an immutability requirement.
- Domain packages importing infrastructure packages (the arrow should point
  the other way).
