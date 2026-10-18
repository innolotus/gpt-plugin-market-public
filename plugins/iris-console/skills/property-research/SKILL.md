---
name: property-research
description: Resolve an Australian address or listing to the correct property scope and build a provenance-aware evidence bundle.
metadata:
  product: Iris Console
  version: 0.3.0
  portable: true
---

# Property Research

## Purpose

Resolve a user-supplied address/listing/property reference into the correct property entity scope and evidence bundle.

A street address does **not** always identify one PropertyRef.

The first responsibility is therefore:

> Is this a single property, a property complex, or still unresolved?

## Inputs

At least one of:

- address;
- listing URL;
- source listing ID;
- PropertyRef;
- PropertyComplex reference;
- user-provided property evidence;
- provisional AcquisitionTarget.

## Property entity resolution

Return one of:

- SINGLE_PROPERTY
- PROPERTY_COMPLEX
- UNRESOLVED

### SINGLE_PROPERTY

Use when the evidence supports one specific independently analysed property/unit/lot.

Return:

- PropertyRef;
- PropertyProfile;
- ListingObservation[];
- evidence.

### PROPERTY_COMPLEX

Use when the supplied address identifies a multi-property complex/building/group.

Return:

- PropertyComplex;
- known/partial PropertyRef[];
- complex-level evidence;
- unit-level observations where available;
- inferred/default AcquisitionTarget if useful.

A complex is not an identity failure merely because a specific unit is not known.

### UNRESOLVED

Use only when the entity itself cannot be safely identified.

Examples:

- address matches materially different unrelated properties;
- location/address is incomplete;
- evidence is too weak to distinguish a property from another entity.

Ask only for the minimum identifier needed to continue.

## AcquisitionTarget inference

Where the address resolves to a PropertyComplex:

### User names a specific unit

```text
targetType = SPECIFIC_PROPERTY
selectionState = RESOLVED
```

### User says one unit may be for sale but unit is unknown

```text
targetType = UNKNOWN_UNIT_IN_COMPLEX
selectionState = PARTIALLY_RESOLVED
```

### User wants any suitable unit in the complex

```text
targetType = ANY_UNIT_IN_COMPLEX
selectionState = OPEN_SET
```

### User explicitly wants the entire complex

```text
targetType = COMPLEX_AS_WHOLE
```

Do not infer COMPLEX_AS_WHOLE from the base address alone.

## Procedure

1. Normalize the input address/reference.
2. Resolve PropertyEntityType.
3. If SINGLE_PROPERTY, resolve canonical PropertyRef.
4. If PROPERTY_COMPLEX, resolve PropertyComplex and known unit/property references where available.
5. Separate ComplexFact, UnitFact and SharedFact.
6. Acquire permitted listing/property evidence.
7. Separate listing claims from independently supported property facts.
8. Collect available sale/rental history at the correct entity level.
9. Capture physical characteristics relevant to the selected scope.
10. Record missing condition/title/planning evidence as UNKNOWN.
11. Return the entity-resolution result + evidence bundle.

## Complex fact discipline

Examples of ComplexFact:

- building/common address;
- known property/unit count;
- common access;
- shared site attributes.

Examples of UnitFact:

- bedrooms;
- internal area;
- parking;
- specific sale/rent history;
- unit-specific title.

Do not promote one unit's attributes to every unit in the complex.

## Title discipline

Do not infer:

- strata;
- community title;
- Torrens;
- company title;
- other legal ownership structure

from appearance, mailboxes, map imagery or marketing language.

Until formally supported:

```text
titleStructure = UNKNOWN
```

## Strategy-relevant attributes

For a resolved specific property, capture where available:

- year built / approximate age;
- apparent condition;
- renovation history;
- habitability indicators;
- land area;
- frontage;
- site shape;
- access;
- property type;
- bedrooms / bathrooms / parking;
- current / recent rent;
- current listing state;
- historical sale evidence.

For a complex-level target, collect distributions/archetypes rather than fabricating one representative unit.

## Output

Return as applicable:

- PropertyEntityType;
- PropertyRef;
- PropertyComplex;
- ComplexProfile;
- AcquisitionTarget;
- PropertyProfile;
- ListingObservation[];
- EvidenceItem[];
- unknowns;
- warnings;
- confidence.

## Guardrails

Never:

- silently select an arbitrary unit from a complex;
- treat the base/common address as one dwelling without evidence;
- promote one unit's facts to the whole complex;
- invent title structure;
- invent sold prices or rents;
- convert asking price into market value;
- infer seller motivation as fact;
- mark a property uninhabitable without evidence;
- treat an old building as economically worthless solely because it is old;
- scrape restricted sources in breach of Source Policy.
