# Immutability checklist

Immutable values are thread-safe, can be shared freely, make equality and
hashing reliable, and make code easier to reason about because nothing changes
behind your back. The standard is: domain objects never change after
construction; change is a new value.

## Types
- Prefer `record` for data carriers. Otherwise `final class` with all fields
  `private final`. Non-final classes invite mutable subclasses.
- No setters. To "change" a field, provide a wither returning a new instance:

  ```java
  public record Order(OrderId id, Seq<Line> lines, Status status) {
      public Order withStatus(final Status newStatus) {
          return new Order(id, lines, newStatus);
      }
      public Order addLine(final Line line) {
          return new Order(id, lines.append(line), status);
      }
  }
  ```
- Validate invariants in the constructor (compact record constructor), so an
  invalid instance can't exist. For expected invalid input, use a static
  factory returning `Validation`/`Either` instead of throwing.
- Lombok: `@Value` and `@With` are fine; `@Data`, `@Setter`, and non-final
  `@Getter` classes are findings.

## Fields and state
- No non-final instance fields (JPA/framework boundary types excepted - see
  SKILL.md).
- **No mutable static state** (Blocker). `static final` is only safe if the
  referenced object is itself immutable - `static final List<X> = new
  ArrayList<>()` is mutable static state.
- `final` does not make the *referent* immutable: a `final java.util.List`,
  array, `Date`, `Calendar`, `StringBuilder` or mutable POJO field is still
  mutable state.

## Collections
- Domain code uses vavr persistent collections: `io.vavr.collection.List`
  (linked; cheap prepend/head), `Vector` (indexed access), `HashMap`,
  `LinkedHashMap`, `HashSet`, `TreeMap`, `Seq` as the parameter/return type.
- `new ArrayList`, `new HashMap`, `new HashSet` etc. in domain code are findings.
- `java.util` collections only at boundaries (framework APIs, third-party
  libraries), converted on the way in (`List.ofAll(javaList)`,
  `HashMap.ofAll(javaMap)`) and out (`seq.asJava()` gives an unmodifiable view;
  `toJavaList()` gives a *mutable* copy - don't return that from an API meant
  to be read-only).
- If vavr isn't available at some boundary, `List.copyOf`/`Map.copyOf`/
  `Stream.toList()` give unmodifiable `java.util` copies. `Collections.
  unmodifiableList(x)` is only a view - the caller holding `x` can still
  mutate it, so defensively copy first.
- `Arrays.asList` is fixed-size but still allows `set` - not immutable.
- **Discarded results**: with persistent collections, `list.append(x);` on its
  own line does nothing. That is a bug, not a style issue - always Major or
  Blocker.
- **Exposed internals**: returning a mutable internal collection or array lets
  callers change the object's state (Blocker). Arrays are always mutable:
  prefer `Seq`/`Vector`; if an array must be returned, clone it.

## Dates and misc
- `java.util.Date`/`Calendar` are mutable - use `java.time` types.
## Final references
Every reference is declared `final`: fields, method and constructor
parameters, local variables, and catch parameters. Effectively-final is not
enough - the keyword documents intent and stops later edits quietly
introducing reassignment.

- Exceptions that need no comment: record components (implicitly final),
  interface constants (implicitly final), parameters of abstract or interface
  methods (`final` there is not part of the signature and has no effect), and
  untyped lambda parameters (Java does not allow `final` on them).
- A reference that absolutely must be reassigned keeps its non-final
  declaration *with an explanatory comment beside it* (same line or the line
  above) saying why. "// reassigned: accumulates the running checksum in a
  measured hot loop" is a justification; "// the total" is not.
- A local reassigned in a loop is usually a fold waiting to happen (see
  functional-style.md); a reassigned parameter is almost never justified -
  introduce a new local instead.

```java
// Before
public Money total(List<Line> lines, Discount discount) {
    Money sum = Money.ZERO;
    for (Line l : lines) sum = sum.plus(l.price());
    return discount.apply(sum);
}

// After
public Money total(final Seq<Line> lines, final Discount discount) {
    final Money sum = lines.map(Line::price).fold(Money.ZERO, Money::plus);
    return discount.apply(sum);
}
```
