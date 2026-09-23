# Ecode AI Problem Generation Specification

## 1. Purpose

Ecode uses AI to generate programming problems for its
100-day progressive coding curriculum.

The AI is responsible only for generating problems.

The backend remains responsible for validating the generated
problem and controlling scoring, progression, submissions,
leaderboards, and other platform rules.

## 2. AI Input Contract

### 2.1 Day Number

The backend provides the curriculum day number to the AI.

Example:

day_number: 27

The day number identifies where the generated problem belongs
within Ecode's 100-day curriculum.

The AI must not modify or reinterpret the assigned day.

### 2.2 User-Facing Topic

The backend provides the main curriculum topic associated with the
assigned day.

Example:

topic: Repetition

The topic represents the concept that Ecode wants the student to
practice.

The topic is also visible to the student so that the student knows
what concept they should prepare for.

The AI must generate a problem that is relevant to the provided topic.
The AI must not replace the assigned topic with an unrelated topic.

### 2.3 Hidden Sub-topic

The backend provides the specific sub-topic associated with the
assigned day.

Example:

sub_topic: Nested loops

The hidden sub-topic gives the AI a more precise generation target
than the user-facing topic.

The sub-topic is an internal curriculum control and is not directly
shown to the student.

The AI must generate a problem that primarily tests the provided
sub-topic.

The backend remains responsible for determining the assigned
sub-topic.

### 2.4 Difficulty

The backend provides a difficulty level for the assigned day.

Example:

difficulty: 4

The difficulty level controls the expected complexity of the
generated problem within Ecode's curriculum.

The AI must generate a problem appropriate for the provided
difficulty level.

Difficulty must be consistent with the assigned day, topic,
and hidden sub-topic.

The AI must not independently increase or decrease the assigned
difficulty.

### 2.5 Expected Solving Time

The backend provides the expected solving time for the generated
problem.

Example:

expected_time_minutes: 10

The expected solving time represents the approximate amount of time
a student should need to understand and solve the problem.

The AI must generate a problem whose complexity is appropriate for
the provided time limit.

The expected solving time is a generation constraint and does not
allow the AI to modify Ecode's actual judging or submission rules.

The backend remains responsible for enforcing the actual time limit.

### 2.6 Allowed Concepts

The backend provides a list of programming concepts that the AI is
allowed to use when generating the problem.

Example:

allowed_concepts:
- variables
- arithmetic
- for loops
- range
- nested loops

The allowed concepts are determined by Ecode's curriculum.

The AI must generate a problem that can be solved using the provided
allowed concepts.

The AI must not require concepts that are outside the provided
allowed-concepts list unless those concepts are explicitly permitted
by the curriculum configuration.

The backend uses this information as part of its validation process.

### 2.7 Forbidden Concepts

The backend provides a list of programming concepts that the AI must
not require when generating the problem.

Example:

forbidden_concepts:
- methods
- recursion
- classes
- collections
- external libraries

The AI must not create a problem that requires any forbidden concept
to solve it.

Forbidden concepts are determined by Ecode's curriculum and are used
to prevent the generated problem from exceeding the student's current
learning stage.

The backend should also validate the generated problem against these
restrictions before accepting it.

### 2.8 Problem Type

The backend specifies the type of problem that the AI must generate.

For Ecode's programming challenges, the problem type is:

problem_type: programming_problem

The AI must generate a problem that requires the student to write
and submit a program as the solution.

The generated problem must contain a clear programming objective,
input requirements, output requirements, and constraints.

The AI must not generate theory questions, multiple-choice questions,
explanation-only questions, or questions that can be answered without
writing a program.

### 2.9 Test Case Requirements

The AI must generate exactly five test cases for every programming
problem.

The test cases must be divided into:

- 1 public test case
- 4 hidden test cases

Each test case must contain:

- input
- expected output

The public test case may be shown to the student before submission.

The hidden test cases must remain private and must never be exposed
to the student.

The AI must generate test cases that are relevant to the problem and
sufficient to verify different valid input conditions.

Each test case is worth 10 points, for a total of 50 points.

The backend must validate the generated test-case structure before
storing the problem.

### 2.10 Programming Language

Ecode currently supports Java and Python.

The problem itself must remain language-independent so that the same
problem can be solved in either supported language.

The programming language is therefore not treated as a property of
the problem.

The selected programming language is associated with the student's
submission.

Example:

Problem:
"Calculate the sum of all even numbers from 1 to N."

Possible submissions:

- Python
- Java

The backend determines whether the submitted language is supported
and executes the submitted code using the appropriate execution
environment.

The AI must not create separate problem logic for different
languages unless the generation process explicitly requires
language-specific syntax or constraints.

### 2.11 Generation Quality Requirements

Every generated problem must satisfy the following requirements:

- The problem must match the assigned day, topic, sub-topic, and
  difficulty.
- The problem must be solvable using the allowed concepts.
- The problem must not require forbidden concepts.
- The problem must have a clear and unambiguous objective.
- The problem must contain a complete problem description.
- The input format must clearly describe the expected input.
- The output format must clearly describe the expected output.
- The constraints must be sufficient to define valid input boundaries.
- The generated test cases must be consistent with the problem statement.
- The expected outputs must be correct for their corresponding inputs.
- The problem must be suitable for automated code judging.
- The problem should be reasonably solvable within the specified
  expected solving time.

The backend must validate these requirements before accepting the
generated problem.

### 2.12 Duplicate and Originality Requirements

The AI should generate problems that are meaningfully different from
previously stored problems.

A generated problem must not be an exact duplicate of an existing
problem.

The problem should also avoid being a trivial rewording of an
existing problem when the underlying task, solution approach, and
required reasoning are substantially the same.

The backend must perform duplicate detection before accepting and
storing a generated problem.

If a generated problem is detected as a duplicate, it must be
rejected and regenerated or replaced using the configured
alternative or fallback mechanism.

Duplicate detection is a backend responsibility. The AI must not be
trusted to determine whether a problem is unique.

### 2.13 Structured Output Requirement

The AI must return the generated problem in a predefined structured
format.

The response must contain the following fields:

- title
- description
- input_format
- output_format
- constraints
- public_test_case
- hidden_test_cases

The public_test_case must contain:

- input
- expected_output

The hidden_test_cases field must contain exactly four test cases.

Each hidden test case must contain:

- input
- expected_output

The AI must not return additional explanatory text outside the
defined problem structure.

The backend must validate the structure before accepting the
generated response.

## 3. AI Output Contract

The AI must return every generated programming problem in a
predefined structured format.

The backend must not depend on free-form AI responses.

Every generated problem must contain the required problem metadata
and exactly five test cases: one public test case and four hidden
test cases.

### 3.1 Problem Metadata

Each generated problem must contain the following fields:

- title
- description
- input_format
- output_format
- constraints

These fields describe the programming problem that will be presented
to the student.

The title must briefly identify the problem.

The description must clearly explain what the student is required
to solve.

The input_format must describe the input provided to the program.

The output_format must describe the expected output.

The constraints must define the valid input boundaries and relevant
limitations for the problem.

All fields are required and must contain meaningful content.

### 3.2 Public Test Case

Each generated problem must contain exactly one public test case.

The public test case must contain:

- input
- expected_output

The public test case is used to demonstrate the expected behavior of
the problem to the student.

The public test case must be valid according to the problem's stated
input format, constraints, and expected output.

The expected output must correspond exactly to the provided input.

The public test case may be displayed to the student, so it must not
contain information that reveals the hidden test cases.

### 3.3 Hidden Test Cases

Each generated problem must contain exactly four hidden test cases.

Each hidden test case must contain:

- input
- expected_output

Hidden test cases are used by the backend to evaluate student
submissions and must never be exposed to the student.

The hidden test cases must:

- follow the problem's input format and constraints
- have correct expected outputs
- test valid inputs beyond the public example
- help verify that a submitted program correctly solves the problem
- avoid relying on concepts or conditions that are not defined by the
  problem statement

The AI must generate all four hidden test cases together with the
problem.

The backend must validate the hidden test cases before accepting the
problem.

Each hidden test case is worth 10 points.

### 3.4 Complete JSON Structure

The AI must return a JSON object following this exact structure:

{
  "title": "...",
  "description": "...",
  "input_format": "...",
  "output_format": "...",
  "constraints": "...",
  "public_test_case": {
    "input": "...",
    "expected_output": "..."
  },
  "hidden_test_cases": [
    {
      "input": "...",
      "expected_output": "..."
    },
    {
      "input": "...",
      "expected_output": "..."
    },
    {
      "input": "...",
      "expected_output": "..."
    },
    {
      "input": "...",
      "expected_output": "..."
    }
  ]
}

The backend must treat this structure as the required output contract.

The backend must reject a response if required fields are missing,
if the structure is invalid, or if the number of hidden test cases is
not exactly four.

The AI must return only the structured JSON response and must not
include additional conversational text outside the JSON object.

## 4. Backend Validation Rules

The backend must validate every AI-generated problem before it is
accepted and stored.

AI-generated content must be treated as untrusted input.

The backend is the final authority for determining whether a generated
problem satisfies Ecode's curriculum and technical requirements.

### 4.1 Required Fields

The backend must verify that the AI response contains all required
fields:

- title
- description
- input_format
- output_format
- constraints
- public_test_case
- hidden_test_cases

The backend must reject the response if any required field is missing
or contains invalid data.

### 4.2 Data Type and Structure Validation

The backend must verify that every field in the AI response has the
expected data type and structure.

The backend must verify that:

- The AI response is a valid JSON object.
- title is a string.
- description is a string.
- input_format is a string.
- output_format is a string.
- constraints is a string.
- public_test_case is an object.
- hidden_test_cases is an array.
- Each test case is an object.
- Each test case contains input and expected_output.
- input and expected_output contain valid values for the generated
  problem.

The backend must reject the response if any field has an unexpected
type or structure.

The backend must not attempt to automatically repair malformed AI
responses before validation.

### 4.3 Curriculum Alignment Validation

The backend must verify that the generated problem is aligned with
the curriculum information provided to the AI.

The backend must verify that the generated problem:

- matches the assigned topic
- primarily tests the assigned sub-topic
- is appropriate for the assigned difficulty
- can be solved using the allowed concepts
- does not require forbidden concepts

The backend must reject the generated problem if it is not
sufficiently aligned with the assigned curriculum requirements.

The AI's own description of the problem must not be treated as proof
of curriculum alignment. The backend must perform its own validation.

### 4.4 Test Case Validation

The backend must validate all generated test cases before accepting
the problem.

The backend must verify that:

- Exactly one public test case exists.
- Exactly four hidden test cases exist.
- Every test case contains input and expected_output.
- Every test case follows the problem's input format.
- Every test case satisfies the stated constraints.
- Every expected output corresponds correctly to its input.
- Test cases are not exact duplicates of one another.
- Hidden test cases provide additional coverage beyond the public
  test case.

The backend must reject the generated problem if any test case is
invalid, inconsistent with the problem, or cannot be reliably used
for automated judging.

### 4.5 Difficulty and Time Validation

The backend must verify that the generated problem is appropriate for
the assigned difficulty level and expected solving time.

The generated problem must not be substantially easier or harder than
the assigned curriculum level.

The problem should also be reasonably solvable within the expected
solving time provided to the AI.

The backend must reject a generated problem when its complexity is
clearly inconsistent with the assigned difficulty or expected solving
time.

The AI's stated difficulty or estimated solving time must not be
treated as proof of correctness. The backend must perform its own
validation where practical.

### 4.6 Duplicate Problem Validation

The backend must check whether the generated problem duplicates or
substantially repeats a previously accepted problem.

The validation should consider both exact duplication and meaningful
similarity between problems.

An exact duplicate must always be rejected.

A problem that is substantially similar to an existing problem should
also be rejected when it provides essentially the same task, reasoning,
and solution approach with only minor changes in wording or values.

The duplicate check must be performed against previously accepted
problems stored by Ecode.

If a generated problem fails the duplicate check, it must not be
stored as the canonical problem.

The backend must decide whether a problem is accepted; the AI must not
make this decision.

### 4.7 Executability and Judge Compatibility Validation

The backend must verify that the generated problem and its test cases
are suitable for Ecode's automated judging system.

The backend must verify that:

- The problem has a deterministic expected output for each valid input.
- The input format can be parsed by the supported programming
  languages.
- The expected output can be compared reliably with a student
  submission.
- The test cases can be executed by the judging system.
- The problem does not depend on external services, files, network
  access, user interaction, or other resources that are unavailable
  to the judging environment.
- The generated problem does not require functionality that Ecode's
  execution environment does not support.

A generated problem that cannot be reliably judged must be rejected
and must not become a canonical Ecode problem.

### 4.8 Final Acceptance Rule

A generated problem may be accepted and stored as a canonical Ecode
problem only when it passes all required backend validation checks.

The backend must reject a generated problem when any mandatory
validation check fails.

A rejected problem must never become the canonical problem for the
assigned day.

The backend must record the reason for rejection so that the system
can determine the appropriate next action, such as regeneration,
using a pre-generated alternative problem, or using a curated
fallback problem.

Only the backend can make the final acceptance decision.

## 5. AI Failure and Recovery

AI generation is an enhancement to Ecode and must not be a
single point of failure.

The platform must be able to provide a valid programming problem even
when the live AI generation process fails.

A failure may occur because of:

- AI provider unavailability
- API timeout
- API rate limit
- invalid AI response
- failed backend validation
- duplicate problem detection
- invalid test cases
- judge compatibility failure
- temporary network failure
- other unexpected generation errors

The backend must handle these failures through a predefined recovery
process.

The recovery process must preserve the assigned day, topic,
sub-topic, difficulty, and other curriculum requirements.

The AI must never be allowed to bypass backend validation because
generation has failed.

### 5.1 Regeneration Strategy

When a live AI-generated problem fails backend validation, the backend
may request a new problem from the AI.

Each regeneration request must use the same curriculum requirements
as the original generation request.

The backend must not relax or remove curriculum restrictions simply
because previous generations failed.

A regenerated problem must pass the same complete validation process
as the original problem.

The number of live regeneration attempts must be limited by a
configured maximum.

If all allowed regeneration attempts fail, the backend must stop
requesting new live generations and move to the next recovery stage.

A failed generation must never be stored as the canonical problem.

The regeneration process must not change:

- day number
- user-facing topic
- hidden sub-topic
- assigned difficulty
- expected solving time
- allowed concepts
- forbidden concepts
- test-case requirements

### 5.2 Pre-generated Alternative Problems

Ecode must maintain a pre-generated alternative problem for each day
of the 100-day curriculum.

The alternative problems are generated and validated before they are
needed at runtime.

Each alternative problem must satisfy the same curriculum and
technical requirements as the corresponding primary problem.

For each curriculum day, the alternative problem must match:

- day number
- user-facing topic
- hidden sub-topic
- difficulty
- expected solving time
- allowed concepts
- forbidden concepts
- problem type
- test-case requirements

Each alternative problem must contain exactly:

- 1 public test case
- 4 hidden test cases

Every alternative problem must pass the complete backend validation
process before being stored.

The alternative problem must be meaningfully different from the
primary problem and other alternatives for the same day.

The backend may use the pre-generated alternative when live AI
generation has failed or when the generated problem cannot be
accepted after the configured regeneration attempts.

Pre-generated alternatives must not bypass validation at runtime
when they are selected for use.

The alternative problem becomes the canonical problem for that
generation cycle only after the backend confirms that it is valid
and available for use.

### 5.3 Curated Fallback Problems

Ecode must maintain a small set of manually curated fallback
problems that can be used when the live AI generation process and
pre-generated alternative problems are unavailable or unusable.

The curated fallback problems are intended as a last-resort recovery
mechanism.

The fallback set must cover the major stages of the 100-day curriculum.

Ecode should maintain at least five fallback groups corresponding to
the following curriculum ranges:

- Days 1–20
- Days 21–40
- Days 41–60
- Days 61–80
- Days 81–100

Each fallback group should contain multiple validated problems rather
than a single problem.

Fallback problems must be designed and validated before they are
needed at runtime.

Each fallback problem must satisfy the technical requirements of
Ecode and must contain:

- 1 public test case
- 4 hidden test cases

When a fallback problem is selected, the backend must verify that it
is compatible with the assigned curriculum day and its requirements.

A fallback problem must never be selected solely because it is
available. It must satisfy the required curriculum constraints.

Fallback problems must be treated as the final recovery mechanism and
must not normally be used when a valid primary or alternative problem
is available.

### 5.4 Recovery Order

Ecode must follow a predefined recovery order when generating the
canonical problem for a curriculum day.

The backend must use the following order:

1. Generate a problem using the live AI provider.
2. Validate the generated problem.
3. If validation fails, request regeneration up to the configured
   maximum number of attempts.
4. If all live generation attempts fail, select the corresponding
   pre-generated alternative problem.
5. Validate the selected alternative before using it.
6. If the alternative is unavailable or fails validation, select a
   compatible curated fallback problem.
7. Validate the selected fallback before using it.
8. If no valid problem is available after all recovery stages, the
   backend must report a generation failure rather than storing an
   invalid problem.

The recovery process must never skip backend validation.

The first valid problem selected by this process becomes the
canonical problem for the assigned generation cycle.

The backend must record which generation source was used, such as:

- live_ai
- regenerated_ai
- pre_generated_alternative
- curated_fallback

This information is internal system metadata and does not affect the
problem's curriculum rules or student scoring.

### 5.5 Generation Source Tracking

The backend should track the source from which the canonical problem
was obtained.

The generation source should identify which stage of the recovery
process produced the problem.

Supported generation sources are:

- live_ai
- regenerated_ai
- pre_generated_alternative
- curated_fallback

The generation source must be stored as internal problem metadata.

Generation source tracking should allow the backend to determine:

- whether the live AI provider was successful
- whether regeneration was required
- whether a pre-generated alternative was used
- whether a curated fallback was required

Generation source metadata must not affect:

- student scoring
- student progression
- leaderboard calculations
- problem difficulty
- curriculum assignment

The generation source is an operational and debugging attribute only.

The backend should also record relevant generation failures so that
repeated AI or validation failures can be monitored and investigated.

Generation failure information must not expose internal AI prompts,
provider credentials, hidden test cases, or other sensitive system
information to students.

### 5.6 Canonical Problem Selection

Ecode uses a global daily problem model.

For each curriculum day, Ecode must select one canonical problem
that is shared by all students participating in that day's ranked
challenge.

The canonical problem must be selected by the backend.

Students must not receive different randomly generated problems for
the same ranked curriculum day.

The backend must ensure that the selected canonical problem:

- belongs to the correct curriculum day
- matches the assigned topic
- primarily tests the assigned sub-topic
- matches the assigned difficulty
- satisfies the allowed and forbidden concept rules
- contains exactly 1 public and 4 hidden test cases
- has passed all required backend validation

Once a valid problem has been selected as the canonical problem for a
day, the backend must not replace it with another problem during the
same active challenge period unless an explicit administrative
recovery procedure is triggered.

The canonical problem must remain consistent for all students during
that challenge period.

The student's selected programming language does not create a
different problem. The same canonical problem must be solvable using
each programming language supported by Ecode.

The backend must use the canonical problem as the authoritative source
for:

- problem presentation
- hidden test cases
- submission evaluation
- execution limits
- scoring
- daily challenge assignment

Students must never be able to select, modify, or replace the
canonical problem through the client application.

### 5.7 Problem Immutability

Once a problem has been accepted as the canonical problem for an
active curriculum day, its core problem and judging data must be
treated as immutable.

The backend must not modify the following fields while the problem is
being used by students:

- problem statement
- input format
- output format
- constraints
- difficulty
- public test case
- hidden test cases
- execution time limit
- problem identity

This ensures that all students participating in the same ranked
challenge are evaluated against the same problem definition and
judging conditions.

If a serious error is discovered after a problem becomes canonical,
the backend must not silently modify the existing problem in a way
that changes the meaning of existing submissions.

Instead, Ecode should use an explicit administrative correction or
replacement procedure.

Any replacement problem must receive a distinct problem identity and
must pass the complete backend validation process before being used.

Changes to canonical problems should be recorded for auditing and
debugging purposes.

Historical submission records must continue to reference the problem
identity against which the submission was evaluated.

### 5.8 Generation Versioning

Ecode should maintain internal version information for problems
generated through the AI and recovery process.

Generation versioning must distinguish between different generation
attempts without changing the identity of the canonical problem.

A generation attempt may include:

- an initial live AI generation
- a regenerated AI problem
- a pre-generated alternative
- a curated fallback

Each generation attempt should have its own internal generation
record or version identifier.

The generation record should allow the backend to determine:

- when the generation was performed
- which generation source was used
- which curriculum day was requested
- whether validation succeeded or failed
- why a generation attempt was rejected
- which generation attempt produced the accepted problem

Generation attempts that fail validation must not become student-facing
problems.

The canonical problem identity must remain separate from the generation
attempt or generation version.

Once a problem becomes canonical, its problem identity must remain
stable for submissions and historical records.

Generation versioning is an internal operational mechanism and must
not affect student scoring, progression, or leaderboard calculations.

### 5.9 AI Generation Logging

The backend should maintain operational logs for AI problem generation
and validation events.

Generation logs should provide enough information to diagnose
generation failures and monitor the reliability of the AI generation
pipeline.

The backend should record relevant metadata such as:

- generation timestamp
- curriculum day
- generation source
- generation attempt number
- validation result
- rejection reason, when applicable
- final selection result
- AI provider or model identifier, when available

Generation logs must not expose sensitive information to students.

The backend must not store AI provider credentials, API keys, or other
authentication secrets in generation logs.

Logs should also avoid unnecessarily storing complete AI requests or
responses when they contain sensitive system information.

Generation logging must not affect the student's problem, score,
progression, or leaderboard position.

The logging system should support monitoring of repeated failures,
validation problems, duplicate generation, and fallback usage.

### 5.10 AI Provider Independence

Ecode should not depend on a specific AI provider for its core
platform functionality.

The AI generation layer should be separated from the rest of the
backend through a provider-independent service interface.

The problem generation system should allow the AI provider to be
changed without requiring changes to the core problem, submission,
scoring, progression, or leaderboard systems.

The AI provider layer should be responsible for:

- sending generation requests
- receiving AI responses
- handling provider-specific errors
- applying provider-specific configuration

The rest of the Ecode backend should interact with the AI generation
layer through a consistent internal interface.

Changing the AI provider must not change Ecode's:

- curriculum rules
- problem structure
- validation rules
- test-case requirements
- submission rules
- scoring rules
- progression rules
- leaderboard rules
- fallback architecture

If the configured AI provider is unavailable, Ecode must use the
existing recovery process rather than treating the provider as a
required dependency for the platform to operate.

The AI provider must never be treated as the final authority for
whether a problem is accepted.

### 5.11 Recovery Guarantee

The AI generation system must be designed so that temporary AI
failures do not prevent Ecode from providing its daily ranked
challenge.

The backend must attempt to obtain a valid problem through the
configured recovery order:

1. Live AI generation
2. AI regeneration
3. Pre-generated alternative
4. Curated fallback

Every problem selected through any stage must satisfy the required
backend validation rules before becoming canonical.

The system must never publish an unvalidated AI-generated problem to
students merely because no valid problem was generated by the
preferred source.

If every recovery stage fails to provide a valid problem, the backend
must report a generation failure and must not create an invalid
canonical problem.

The recovery system must preserve the integrity of Ecode's curriculum,
problem identity, test cases, judging rules, and student scoring.

Therefore, AI availability is not a requirement for the correctness
of the Ecode platform.

The backend remains the final authority throughout the entire problem
generation and recovery process.

## 6. Problem Generation Workflow

Ecode must follow a controlled workflow when generating the canonical
problem for a curriculum day.

The workflow must ensure that curriculum requirements are determined
by the backend, problem content is generated by the AI, and the final
problem is accepted only after backend validation.

The general workflow is:

1. Load the curriculum configuration for the assigned day.
2. Build the AI generation request using the curriculum requirements.
3. Send the generation request to the configured AI provider.
4. Receive the AI response.
5. Validate the response structure.
6. Validate the generated problem against the curriculum.
7. Validate the generated test cases.
8. Validate difficulty, time, and judge compatibility.
9. Check for duplicate or substantially similar problems.
10. If all required checks pass, accept the problem.
11. If validation fails, follow the configured regeneration and
    recovery process.
12. Store the first valid problem selected by the recovery process as
    the canonical problem.

The workflow must preserve the separation of responsibilities:

- The curriculum determines what should be generated.
- The AI generates the problem content.
- The backend validates the generated content.
- The backend selects the canonical problem.
- The backend stores and serves the canonical problem.
- The judging system evaluates student submissions.

No AI-generated problem may bypass the workflow and become available
to students without passing the required backend validation.

### 6.1 Load Curriculum Configuration

Before generating a problem, the backend must load the curriculum
configuration associated with the assigned day.

The curriculum configuration is the authoritative source for the
requirements that the generated problem must satisfy.

The configuration should provide, where applicable:

- day number
- user-facing topic
- hidden sub-topic
- difficulty
- expected solving time
- allowed concepts
- forbidden concepts
- problem type
- supported test-case requirements

The backend must use the stored curriculum configuration when building
the AI generation request.

The AI must not be allowed to determine or modify these curriculum
requirements.

If the curriculum configuration for the assigned day is missing or
invalid, the backend must not request a problem from the AI.

The generation process must instead report a curriculum configuration
failure and follow the appropriate recovery procedure.

The curriculum configuration must remain consistent throughout the
generation process for that problem.

### 6.2 Build Generation Request

After loading the curriculum configuration, the backend must build a
structured generation request for the AI provider.

The generation request must contain the curriculum requirements needed
to generate the problem.

The request should include:

- day number
- user-facing topic
- hidden sub-topic
- difficulty
- expected solving time
- allowed concepts
- forbidden concepts
- problem type
- test-case requirements

The backend must construct these values from the stored curriculum
configuration rather than accepting them from the AI provider.

The generation request must clearly instruct the AI to return the
required structured problem format.

The request must also instruct the AI to:

- generate a language-independent programming problem
- generate exactly one public test case
- generate exactly four hidden test cases
- provide an expected output for every test case
- follow the provided constraints
- avoid forbidden concepts
- remain appropriate for the assigned difficulty and solving time
- return only the required structured response

The backend must not include student-controlled values in the
curriculum requirements of the generation request.

Provider-specific request formatting should remain inside the AI
provider integration layer and must not affect Ecode's core problem
generation contract.

### 6.3 Send Generation Request

The backend must send the generation request to the configured AI
provider through the AI provider integration layer.

The provider integration layer is responsible for handling
provider-specific communication details.

It should handle:

- API authentication
- request formatting
- connection handling
- provider-specific configuration
- request timeouts
- provider errors
- response retrieval

The core Ecode problem-generation workflow must not depend on
provider-specific implementation details.

The backend must apply a configured timeout to the AI generation
request.

If the AI provider does not respond within the configured timeout, the
generation attempt must be treated as failed.

If the provider returns an API error, unavailable response, rate-limit
response, or other provider failure, the generation attempt must be
treated as failed.

A failed provider request must not create or modify a canonical
problem.

The backend must record the relevant generation failure metadata and
continue according to the configured recovery process.

The AI provider must not have direct access to the Ecode database or
the ability to modify stored problems.

Only the Ecode backend may accept, validate, store, or reject the
generated problem.

### 6.4 Receive and Parse AI Response

After the AI provider returns a response, the backend must receive and
parse the response before performing any further processing.

The backend must treat the AI response as untrusted external input.

The response must first be checked to determine whether it can be
parsed as valid JSON.

If the response is not valid JSON, the generation attempt must be
treated as failed.

If the response contains additional conversational text outside the
required JSON structure, the generation attempt must be treated as
invalid unless the provider integration layer can guarantee that the
returned content is already a valid structured response.

The backend must not attempt to infer missing fields or silently
correct malformed values.

After successful parsing, the resulting JSON object must be passed to
the backend validation pipeline.

The backend must not store or expose the response to students before
validation is complete.

A parsing failure must be logged as a generation failure and must
continue through the configured regeneration and recovery process.

### 6.5 Run Validation Pipeline

After successfully parsing the AI response, the backend must pass the
generated problem through the complete validation pipeline.

The validation pipeline must verify the generated problem against the
requirements defined by Ecode.

The backend must validate, where applicable:

- required fields
- data types and structure
- curriculum alignment
- topic and sub-topic alignment
- allowed concepts
- forbidden concepts
- difficulty
- expected solving time
- test-case structure
- test-case validity
- expected outputs
- judge compatibility
- duplicate or substantial similarity

Each validation stage must produce a clear success or failure result.

If any mandatory validation stage fails, the generated problem must be
rejected.

The backend must not accept a problem based on partial validation.

A problem that passes structural validation but fails curriculum
validation must still be rejected.

A problem that passes curriculum validation but fails test-case
validation must still be rejected.

Only a problem that passes all mandatory validation stages may proceed
to canonical problem selection.

Validation failures must be recorded with sufficient information for
the generation system to determine the appropriate recovery action.

### 6.6 Accept Valid Problem

When a generated problem passes all mandatory backend validation
stages, the backend may accept it as a valid problem candidate.

The backend must assign the appropriate generation source and internal
generation metadata to the accepted candidate.

The accepted candidate must then proceed to canonical problem
selection and storage.

Before storage, the backend must ensure that:

- the problem belongs to the intended curriculum day
- the problem has a valid problem structure
- all five test cases are valid
- the problem has passed duplicate detection
- the problem is compatible with the judging system
- all required problem metadata is available

The backend must store only the validated problem data required by
Ecode.

The accepted problem must not be modified by the AI after acceptance.

If the problem is selected as the canonical problem, its problem
identity must remain stable for the duration of its use.

A successfully validated problem must not automatically become
student-facing until the canonical problem selection process has
completed.

### 6.7 Handle Validation Failure

If a generated problem fails any mandatory backend validation stage,
the backend must reject the problem candidate.

The backend must identify the validation stage that failed and record
the relevant failure information.

A rejected candidate must not be stored as a canonical problem.

The backend must then determine the appropriate recovery action based
on the configured generation attempt and recovery state.

The recovery process must follow the order defined in Section 5.

If additional live AI generation attempts are available, the backend
may request another generation.

If the maximum live generation attempts have been reached, the
backend must move to the pre-generated alternative.

If the pre-generated alternative is unavailable or fails validation,
the backend must move to a compatible curated fallback problem.

Every replacement candidate must pass the same mandatory validation
pipeline before it can be accepted.

The backend must not weaken validation requirements to make a candidate
acceptable.

A validation failure must never be exposed to students as a
student-facing problem.

### 6.8 Canonical Problem Storage

After a valid problem candidate has been selected as the canonical
problem, the backend must store it in the Ecode database.

The stored problem must contain the information required for:

- problem presentation
- automated judging
- submission evaluation
- scoring
- curriculum tracking
- historical records

The backend must store the problem together with its associated test
cases.

The public test case must be identifiable separately from the hidden
test cases.

Hidden test cases must remain accessible only to the backend judging
system and must never be returned through student-facing API
responses.

The stored problem must retain its assigned:

- day number
- topic
- hidden sub-topic
- difficulty
- time limit
- generation source
- generation metadata, where applicable

The problem must receive a stable problem identity.

Once stored as the canonical problem, the problem and its judging data
must follow the immutability rules defined in Section 5.

The backend must ensure that the complete problem and its test cases
are stored consistently.

A partially stored problem must not become available to students.

If storage fails, the backend must treat the canonicalization process
as unsuccessful and must not expose the incomplete problem.

The stored canonical problem becomes the authoritative problem used by
Ecode for the corresponding ranked challenge.

### 6.8 Canonical Problem Storage

After a valid problem candidate has been selected as the canonical
problem, the backend must store it in the Ecode database.

The stored problem must contain the information required for:

- problem presentation
- automated judging
- submission evaluation
- scoring
- curriculum tracking
- historical records

The backend must store the problem together with its associated test
cases.

The public test case must be identifiable separately from the hidden
test cases.

Hidden test cases must remain accessible only to the backend judging
system and must never be returned through student-facing API
responses.

The stored problem must retain its assigned:

- day number
- topic
- hidden sub-topic
- difficulty
- time limit
- generation source
- generation metadata, where applicable

The problem must receive a stable problem identity.

Once stored as the canonical problem, the problem and its judging data
must follow the immutability rules defined in Section 5.

The backend must ensure that the complete problem and its test cases
are stored consistently.

A partially stored problem must not become available to students.

If storage fails, the backend must treat the canonicalization process
as unsuccessful and must not expose the incomplete problem.

The stored canonical problem becomes the authoritative problem used by
Ecode for the corresponding ranked challenge.

### 6.10 Complete Generation Workflow

The complete Ecode problem generation workflow must operate as a
controlled backend process.

The workflow is:

1. Load the curriculum configuration for the assigned day.
2. Build the structured AI generation request.
3. Send the request to the configured AI provider.
4. Receive the AI response.
5. Parse the response as JSON.
6. Reject the response if parsing fails.
7. Run the complete backend validation pipeline.
8. Reject the candidate if any mandatory validation check fails.
9. If regeneration attempts remain, request another AI-generated
   candidate.
10. If live generation is exhausted, use the corresponding
    pre-generated alternative.
11. Validate the alternative using the same validation pipeline.
12. If the alternative is unavailable or invalid, use a compatible
    curated fallback.
13. Validate the fallback using the same validation pipeline.
14. Select the first valid candidate as the canonical problem.
15. Store the canonical problem and its test cases in a single
    database transaction.
16. Make the problem available to student-facing systems only after
    successful storage.
17. Record the generation source and relevant operational metadata.

At every stage, the backend remains responsible for enforcing Ecode's
rules.

The AI provider is responsible only for generating candidate problem
content.

The final canonical problem must always be a backend-validated and
successfully stored problem.

## 7. Duplicate Detection

Ecode must prevent generated problems from being exact duplicates or
substantially repeated versions of previously accepted problems.

Duplicate detection is a backend responsibility.

The backend should perform duplicate detection using multiple
properties of a problem rather than relying only on its title.

Relevant information may include:

- problem title
- problem description
- required solution approach
- input structure
- output structure
- constraints
- test-case patterns

An exact duplicate must always be rejected.

A substantially similar problem should also be rejected when the
underlying task and required reasoning are essentially the same despite
minor changes in wording, variable names, or input values.

The duplicate detection mechanism may use normalized text comparison,
hashing, similarity analysis, or other suitable techniques.

Duplicate detection must not be treated as perfect proof of
originality.

The backend remains responsible for the final acceptance decision.

### 7.1 Duplicate Detection Scope

Duplicate detection should be performed against previously accepted
canonical problems and other stored problem candidates where
appropriate.

The system should prevent duplicate problems from being used as:

- primary generated problems
- regenerated problems
- pre-generated alternatives
- curated fallback problems

Problems that are intentionally reused as part of an administrative
recovery process must be explicitly identified rather than accidentally
classified as new problems.

### 7.2 Duplicate Rejection

If a generated problem is identified as a duplicate or substantially
similar to an existing problem, it must be rejected.

The rejection should be recorded with the appropriate validation or
duplicate-detection reason.

The rejected problem must not become canonical.

The generation workflow must then continue according to the configured
recovery process.

---

## 8. Problem Storage and Canonicalization

A problem becomes an Ecode problem only after it has passed all required
validation stages and has been selected as the canonical problem for
its assigned curriculum day.

The backend must create a stable problem identity for the canonical
problem.

The canonical problem must retain its relationship with:

- curriculum day
- topic
- hidden sub-topic
- difficulty
- time limit
- test cases
- generation source

The canonical problem must be stored together with its required test
cases.

The database must preserve the relationship between a problem and its
test cases.

The backend must ensure that exactly five test cases are associated
with the canonical problem:

- 1 public test case
- 4 hidden test cases

The canonical problem must not be exposed to students until storage
has completed successfully.

### 8.1 Canonical Problem Identity

Each canonical problem must have a unique and stable problem identity.

The problem identity must be used by the submission system when
students submit solutions.

The problem identity must not depend on:

- student identity
- programming language
- submission attempt
- AI provider
- generation attempt

A problem identity must remain stable while the problem is being used
by the ranked challenge.

### 8.2 Canonical Problem and Test Cases

The canonical problem and its test cases must be treated as one logical
judging package.

The backend must ensure that the test cases referenced by a canonical
problem are the exact test cases used during submission evaluation.

Students must never be able to replace or modify the test cases through
the client application.

---

## 9. Global Daily Problem Assignment

Ecode uses one global daily problem for the ranked challenge.

For each curriculum day, the backend selects one canonical problem.

All students participating in that ranked challenge receive the same
canonical problem.

The backend must not generate a separate ranked problem for each
student.

The student's selected programming language does not change the
problem.

The same problem must be solvable using each supported programming
language.

### 9.1 Daily Problem Availability

The backend must determine when the canonical problem becomes available
for the assigned curriculum day.

The problem must remain consistent for all students during the active
challenge period.

Students joining or accessing the challenge during the active period
must receive the same canonical problem.

### 9.2 Problem Assignment Authority

The client application must never determine which problem is assigned
to a student.

The backend must determine the canonical problem based on the
curriculum and daily challenge state.

Student-controlled values must not be trusted for:

- problem selection
- difficulty
- topic
- sub-topic
- test cases
- time limit
- scoring rules

The client may request the daily problem, but the backend remains the
authority over the returned problem.

---

## 10. Security and Trust Boundaries

AI-generated content, client requests, and student submissions must all
be treated as untrusted input.

The backend must enforce Ecode's rules independently of the client and
AI provider.

The following components must not have authority to modify canonical
problem rules:

- student clients
- AI providers
- frontend JavaScript
- student submissions

Only trusted backend services and authorized administrative operations
may modify system-controlled data.

The AI provider must not have direct database access.

Student-facing APIs must not expose hidden test cases.

Sensitive operational information must not be returned to students.

### 10.1 Student Trust Boundary

The backend must not trust values supplied by the student for:

- user identity
- score
- execution time
- difficulty
- topic
- test cases
- problem correctness
- progression state

Authenticated identity must be obtained from the backend authentication
mechanism.

All judging-related values must be determined by the backend.

### 10.2 AI Trust Boundary

The AI must be treated as an external content generator.

The backend must assume that an AI response can be:

- incorrect
- incomplete
- malformed
- duplicated
- outside curriculum requirements
- unsuitable for automated judging

The AI must therefore never be treated as an authority for problem
acceptance or student evaluation.

---

## 11. AI Service Architecture

The AI generation functionality should be isolated from the rest of
the Ecode backend through a dedicated service layer.

The service layer should separate:

- curriculum preparation
- prompt construction
- provider communication
- response parsing
- validation
- duplicate detection
- recovery
- canonical problem storage

The core application should not directly depend on provider-specific
API calls.

A possible internal structure is:

app/
└── services/
    └── ai/
        ├── problem_generator.py
        └── prompts.py

The exact structure may evolve during implementation.

### 11.1 Problem Generator Service

The problem generator service should coordinate the generation process.

Its responsibilities should include:

- receiving curriculum requirements
- preparing the generation request
- requesting a candidate problem
- handling provider responses
- passing candidates to validation
- triggering regeneration
- selecting alternatives or fallbacks
- returning the final valid candidate

The service must not determine student scores or progression.

### 11.2 Provider Integration

Provider-specific API communication should remain isolated from the
core generation workflow.

The provider integration should handle:

- authentication
- API requests
- response retrieval
- provider-specific errors
- timeouts
- provider-specific configuration

The rest of Ecode should interact with the provider through a
consistent internal interface.

---

## 12. Operational Considerations

The AI generation system must be designed for reliability and
maintainability.

The backend should monitor:

- generation success rate
- validation failure rate
- duplicate rejection rate
- regeneration frequency
- alternative usage
- fallback usage
- provider failures
- generation latency

Operational monitoring should help identify recurring problems in the
generation pipeline.

The system should also prevent excessive AI requests caused by
repeated failures.

Configured limits should exist for:

- generation attempts
- request timeout
- recovery attempts
- other provider-specific resource limits

Operational failures must not change Ecode's curriculum or student
scoring rules.

---

## 13. Data Privacy and Sensitive Information

The AI generation system must minimize the amount of sensitive
information sent to external AI providers.

Student personal information must not be included in problem
generation requests unless explicitly required by a future feature.

Problem generation should use curriculum information rather than
student identity or personal information.

AI generation logs must not contain:

- API keys
- provider credentials
- authentication secrets
- unnecessary student information
- hidden test cases

The backend must control which information is sent to external AI
providers.

---

## 14. AI Responsibility Boundary

The responsibility of the AI in Ecode is limited to generating
programming problem candidates according to backend-provided
requirements.

The AI may generate:

- problem titles
- problem descriptions
- input formats
- output formats
- constraints
- public test cases
- hidden test cases

The AI must not control:

- curriculum assignment
- student identity
- problem selection
- canonical problem status
- submission validity
- execution results
- scores
- progression
- streaks
- leaderboards
- competition results

The backend remains the final authority for all platform rules.

AI-generated content must always pass backend validation before it can
be used by students.

---

## 15. Final Architecture Principle

Ecode follows the principle:

AI generates.
Backend validates.
Backend decides.
Backend stores.
Backend judges.

The AI is therefore an assistive generation component rather than the
authority of the Ecode platform.

The system must remain functional when the AI provider is unavailable
through the configured regeneration, pre-generated alternative, and
curated fallback mechanisms.

The correctness of Ecode must never depend solely on the correctness
or availability of an AI provider.

This separation of responsibilities is a core architectural principle
of Ecode.


