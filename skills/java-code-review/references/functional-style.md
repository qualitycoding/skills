# Functional and fluent style (vavr)

Check the project's vavr version before recommending version-specific APIs.

## Absence: Option, never null
- No `return null`, no `null` parameters, no fields that may be null.
- Wrap nullable values from outside at the boundary: `Option.of(javaValue)`.
- Don't do `if (opt.isDefined()) { ... opt.get() ... }` - use `map`,
  `flatMap`, `fold`, `getOrElse`, `peek` (side effect at the edge only).
- `Option.get()` without a proven-present value is a latent crash (Major).
- Mixing `java.util.Optional` and vavr `Option` in the same codebase is a Nit;
  pick vavr in domain code, convert at the boundary (`Option.ofOptional`,
  `toJavaOptional()`).

```java
// Before
Customer c = repo.find(id);
if (c == null) return "unknown";
return c.name();

// After
return repo.find(id)          // Option<Customer>
        .map(Customer::name)
        .getOrElse("unknown");
```

## Failure: values, not exceptions, for expected cases
- `Either<Error, T>` for business failures the caller must handle (the error
  type should be a sealed interface or enum, not a String).
- `Try<T>` to wrap code that throws (I/O, parsing, legacy APIs), usually
  converted to `Either` quickly: `Try.of(() -> parse(s)).toEither().mapLeft(...)`.
- `Validation<E, T>` to accumulate *all* validation errors, e.g.
  `Validation.combine(validName(n), validAge(a)).ap(Person::new)`
  (gives `Validation<Seq<E>, Person>`).
- Exceptions remain for programming errors (broken invariants).
- Flag: `try/catch` used for control flow, empty `catch` blocks (Major),
  catching `Exception`/`Throwable` broadly, returning error codes/booleans.

## Control-flow statements
`if`, `for`, `while`, `do` and `switch` are not used unless absolutely
required. Each use that remains carries an explanatory comment, on the same
line or the line above, saying *why* no expression-based alternative will do.
The reviewer judges whether that reason holds.

Alternatives, by statement:

| Statement | Instead |
|---|---|
| `if` choosing a value | `Option` (`map`/`filter`/`getOrElse`/`fold`), a conditional expression (`c ? a : b`) for a simple two-way choice, or polymorphism |
| `if` guarding arguments | `Objects.requireNonNull`, a `Checks`/`Validate` helper, or `Validation` for user input |
| `if` handling failure | `Either`/`Try` with `map`, `flatMap`, `fold`, `recover` |
| `for` / `while` / `do` | `map`, `filter`, `flatMap`, `foldLeft`, `zipWithIndex`, `takeWhile`, `Stream.iterate`, `Iterator.unfold` |
| `switch` on a type code or enum | a method on the enum/sealed type, or a `Map` from key to function |
| `switch` on a sealed hierarchy | a method on the sealed interface; an exhaustive pattern-matching switch only with a justifying comment |

The conditional operator `? :` is an expression, not a statement, so it is
acceptable for a short two-way choice; nested conditionals are a sign the
logic wants a lookup or polymorphism.

Legitimate reasons are rare and specific, for example: a measured hot path where
a stream's allocation matters; implementing an `Iterator`, which is inherently
stateful; or a framework callback that requires a statement form.

```java
// Not acceptable: no reason given
for (final Order order : orders) {
    if (order.isPaid()) notifier.send(order);
}

// Acceptable: the reason is real and stated
// while: Iterator.hasNext/next is the only API this third-party cursor offers
while (cursor.hasNext()) {
    sink.accept(cursor.next());
}
```

## Iteration: expressions, not loops
- `for`/`while` -> `map`, `filter`, `flatMap`, `foldLeft`, `groupBy`,
  `partition`, `zip`, `sliding`, `find`, `exists`, `forAll` (see Control-flow
  statements above).
- A local variable accumulated in a loop is a fold:

```java
// Before
BigDecimal total = BigDecimal.ZERO;
for (Line l : lines) { total = total.add(l.price()); }

// After
final BigDecimal total = lines.map(Line::price).fold(BigDecimal.ZERO, BigDecimal::add);
```
- No side effects inside `map`/`filter`; `peek`/`forEach` only at the edge.
- `java.util.stream`: collecting with `Collectors.toList()` yields a mutable
  list - use `Stream.toList()` (unmodifiable) or better, stay in vavr
  (`List.ofAll(stream)` or `.collect(List.collector())`).
- Performance notes worth raising when relevant: vavr `List` has O(n) `get(i)`
  and `append` - use `Vector` for indexed access or heavy appends.

## Purity and composition
- Business rules as pure functions of their inputs (no I/O, no clock, no
  randomness) - easy to test without mocks.
- Side effects (DB, HTTP, logging, time) at the edges of a use case.
- `Tuple2`/`Tuple3` are fine locally; for anything crossing a method boundary
  with meaning, a named record is clearer.
- Pattern matching: prefer a method on the sealed type. Where an exhaustive
  pattern-matching `switch` over records/sealed types is genuinely clearer, it is
  preferable to vavr's `API.Match`, but it is a control-flow statement and needs
  its justifying comment.

## Fluent style
- Expression-oriented code: build results with chained calls rather than
  declaring a variable and mutating it.
- One operation per line in multi-step chains; align the dots.
- If a lambda grows beyond ~3 lines, extract a named method and use a method
  reference - the chain should read like a sentence.
- Immutable fluent APIs: withers (`order.withStatus(PAID)`), builders whose
  `build()` returns an immutable value, and static factories with intention
  revealing names (`Money.of(10, GBP)`, `Order.empty(id)`).
- Don't chain across null-returning methods (train wrecks); if a chain reaches
  deep into other objects' internals (`a.getB().getC().getD()`), that's a
  Law-of-Demeter / encapsulation finding.
