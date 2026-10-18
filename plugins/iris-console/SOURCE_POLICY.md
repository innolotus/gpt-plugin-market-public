# Iris Console Source Policy

## 1. Principle

Iris Console separates **analysis capability** from **source acquisition method**.

For the current GPT-native demo phase, source selection is driven by the maintainer-managed static registry under:

- `Console/Sources/trusted-sources.yaml`
- `Console/Sources/source-authority.yaml`

Normal users do not add, remove or rank sources.

A Skill requests evidence by FactType/capability and follows the static registry's authority and fallback rules.

## 2. Zero-config source behaviour

The expected Console flow is:

```text
Skill
 ↓
FactType / evidence requirement
 ↓
static trusted-source registry
 ↓
preferred approved source/tool
 ↓
permitted fallback
 ↓
evidence + provenance
```

If no approved source can establish the fact, return UNKNOWN rather than asking the user to configure a new source.

Users may provide documents or facts as supplementary evidence, but that does not change the maintained source registry.

## 3. Fact-type-specific authority

Do not use a global rule such as:

```text
government source > all other sources
```

Authority depends on the fact.

Examples:

- planning zone / overlays / statutory planning policy → PlanSA;
- South Australian stamp duty / FHOG / duty relief → RevenueSA;
- title / registered dealings → Land Services SA / formal title evidence;
- cash-rate target → RBA;
- official demographics / Census → ABS;
- current listing / agent guide / auction schedule → approved market/listing source;
- property estimates / market performance / comparables → approved licensed market source.

The canonical mapping is maintained in `Console/Sources/source-authority.yaml`.

## 4. Policy registry relationship

The trusted-source registry and purchase-assistance registry have different jobs.

```text
Purchase Assistance Registry
→ which programs/rules to consider

Trusted Source Registry / Source Authority
→ where those rules must be verified
```

A policy-registry snapshot must not be treated as more authoritative than the official source it references.

Time-sensitive policy rules marked for execution-time verification must be refreshed from the authoritative source before being used as current FACT.

## 5. Domain

Domain is an approved licensed market source via its official Developer API.

Reference:

https://developer.domain.com.au/docs/latest/apis/pkg_property/

Use official API capabilities where available and permitted.

Respect:

- authentication;
- scopes;
- quotas;
- rate limits;
- licence terms;
- disclaimers;
- retention requirements;
- enabled data package/access level.

Do not treat API access as permission to build an unrestricted permanent replica of Domain data.

## 6. realestate.com.au / REA

Do not automate scraping, crawling, indexing or systematic extraction of REA website content unless explicit authorisation permits the intended use.

Reference:

https://about.realestate.com.au/terms-use/

Permitted evidence may come from:

- an official REA capability made available to the user;
- an authorised REA / PropTrack integration;
- licensed client access where the licence permits the workflow;
- user-supplied material where the user has appropriate rights.

Do not design a Skill that depends on unauthorised REA scraping.

## 7. Government, planning and statutory sources

Use the static source registry to select authoritative government/statutory sources for facts such as:

- planning;
- overlays;
- development applications;
- cadastral/title information;
- taxation;
- first-home assistance;
- monetary policy;
- official demographic statistics.

For time-sensitive rules or policies, verify at execution time and retain:

- source;
- jurisdiction;
- publication/effective date where applicable;
- retrieval time;
- policy/code version where available.

## 8. Evidence conflicts

Do not silently resolve material source disagreement.

Use the EvidenceState semantics defined in Contracts when available:

- CONFIRMED
- CONFLICTED
- STALE
- UNVERIFIED
- UNKNOWN

Examples:

- two current listing sources disagree on status → CONFLICTED;
- an older price estimate conflicts with a recent sale → preserve timestamps and do not treat both as equally current;
- an agent claim conflicts with a statutory planning source → statutory planning source governs the planning fact, while the agent claim remains evidence that the claim was made.

## 9. User-provided evidence

User-provided PDFs, screenshots, appraisals, pre-approvals, builder quotes, title documents and reports may be analysed.

The Skill must distinguish:

- what the material explicitly states;
- whether the document itself is authoritative for that fact;
- what is calculated from it;
- what is inferred from it.

Examples:

- a formal current title search may be authoritative title evidence;
- an agent rental appraisal is evidence of the appraisal, not guaranteed future rent;
- a builder quote is strong evidence of quoted project cost for its stated scope, not a universal cost benchmark.

## 10. Retention

For the demo phase, avoid creating a third-party property database.

Prefer retaining only what is needed for the active analysis/report or permitted regression fixture, such as:

- normalized observations;
- provenance;
- timestamps;
- hashes;
- derived calculations;
- source-registry version;
- assumption-set version.

Respect source-specific retention/licensing rules in `trusted-sources.yaml`.

## 11. Failure behaviour

If a required source cannot legally or technically be accessed:

- do not bypass access controls;
- do not fabricate the missing evidence;
- try only configured permitted fallbacks;
- return UNKNOWN if the fact remains unresolved;
- state what evidence would be required to resolve it.

## 12. Maintenance

Source selection is a maintainer responsibility.

Changes to approved sources must be made through the repository:

1. verify the source and current access terms;
2. update the source definition;
3. update affected FactType mappings;
4. increment the registry version;
5. review affected regression fixtures/reports.

Do not expose this as a normal end-user configuration surface.
