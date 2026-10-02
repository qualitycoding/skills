# Tests and coverage

## Coverage
- Targets (unless the user says otherwise): **>= 95% line and >= 90% branch
  per class**, overall as close to 100% as possible. Changed code in a PR
  should be fully covered.
- Branch coverage matters more than line coverage: every `if`, every `switch`
  arm, both sides of every `Option`/`Either`/`Try` (`fold` arms, `getOrElse`
  fallbacks, `recover` paths), every validation failure.
- Legitimate exclusions (generated code, `main` bootstrap, framework wiring)
  belong in JaCoCo configuration, not in silently red reports.
- Suggest enforcing thresholds in the build so coverage can't regress:

```xml
<!-- Maven: jacoco-maven-plugin, in <executions> -->
<execution>
  <id>check</id>
  <goals><goal>check</goal></goals>
  <configuration>
    <rules>
      <rule>
        <element>CLASS</element>
        <limits>
          <limit><counter>LINE</counter><value>COVEREDRATIO</value><minimum>0.95</minimum></limit>
          <limit><counter>BRANCH</counter><value>COVEREDRATIO</value><minimum>0.90</minimum></limit>
        </limits>
      </rule>
    </rules>
  </configuration>
</execution>
```

```groovy
// Gradle
jacocoTestCoverageVerification {
    violationRules {
        rule {
            element = 'CLASS'
            limit { counter = 'LINE';   minimum = 0.95 }
            limit { counter = 'BRANCH'; minimum = 0.90 }
        }
    }
}
check.dependsOn jacocoTestCoverageVerification
```

- Coverage proves code *ran*, not that it was *checked*. Recommend mutation
  testing (PIT: `pitest-maven`, or the `info.solidsoft.pitest` Gradle plugin)
  as the real measure that assertions bite. Surviving mutants are specific,
  actionable test gaps.

## Every test asserts something meaningful
Blockers:
- A test method with no assertion (it passes as long as nothing throws).
- `assertThat(x);` with nothing chained - AssertJ checks nothing until a
  method like `isEqualTo` is called. Same for chains that only call
  `as(...)`/`describedAs(...)`.
- `try { ...; fail(); } catch (X e) {}` that swallows the exception without
  checking it - and in any case prefer `assertThatThrownBy`.

Major:
- The only assertion is `isNotNull()`, `assertNotNull`, or
  `doesNotThrowAnyException()` - it would pass for almost any wrong answer.
  Assert on the *value*.
- Asserting on a boolean instead of the thing: `assertThat(list.contains(x))
  .isTrue()` -> `assertThat(list).contains(x)` (and the failure message
  becomes useful).
- Mockito-only tests that just `verify` the calls the implementation happens
  to make - they test the implementation, not behaviour. Interaction checks are
  fine for genuine outbound side effects (notifications, events); state checks
  otherwise.
- Tests that re-implement the production logic to compute the expected value.

Minor:
- `@Disabled`/`@Ignore` without a linked reason.
- `if`/loops inside a test - use `@ParameterizedTest` (`@CsvSource`,
  `@MethodSource`) instead.
- `Thread.sleep` (use an injected `Clock`, or Awaitility for real async).
- `System.out` in tests.
- Mocking value objects or types you don't own; prefer real immutable values
  and simple fakes.

## AssertJ, fluently
Replace JUnit (`assertEquals`, `assertTrue`, `assertThrows`) and Hamcrest with
AssertJ everywhere. Useful idioms:

```java
assertThat(order.total()).isEqualByComparingTo("42.50");
assertThat(names).containsExactly("ann", "bob");
assertThat(people).extracting(Person::name).containsExactlyInAnyOrder("ann", "bob");
assertThat(people).singleElement().returns("ann", Person::name);
assertThat(result).usingRecursiveComparison().isEqualTo(expected);

assertThatThrownBy(() -> Money.of(-1, GBP))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessageContaining("negative");

SoftAssertions.assertSoftly(softly -> {
    softly.assertThat(dto.id()).isEqualTo(id);
    softly.assertThat(dto.status()).isEqualTo(PAID);
});
```

vavr values have value equality, so plain AssertJ works:
`assertThat(result).isEqualTo(Either.right(order))`,
`assertThat(lookup).isEqualTo(Option.none())`. For richer messages the
`assertj-vavr` module adds dedicated assertions (e.g. `isRight()`,
`containsOnRight(...)`, `isDefined()`, `contains(...)` for Option) - check what
the project's version provides before recommending specific methods.

## Structure
- One behaviour per test, named for the behaviour:
  `rejectsOrderWhenBasketIsEmpty`, not `testOrder2`.
- Given / when / then layout; the "when" is usually one line.
- Test the public behaviour of a class, not its private methods. If a private
  method seems to need its own tests, it's probably a separate responsibility
  (SRP finding on the main code).
- Tests are code: same naming and duplication standards, immutable fixtures
  (static factory methods or builders returning records) rather than shared
  mutable `@BeforeEach` state.
