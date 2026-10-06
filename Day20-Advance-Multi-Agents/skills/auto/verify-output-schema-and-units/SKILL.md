---
name: verify-output-schema-and-units
description: Use when generating structured output files (JSON, CSV) from data processing or log parsing tasks to ensure exact format, schema version, and data types.
---
- Verify all currency and monetary values are represented in integer cents rather than fractional major units.
- Include all required top-level metadata and schema version keys specified in task instructions.
- Apply required string transformations (such as lowercasing and replacing hyphens with underscores in service names) across all output fields.
- Write and verify clean dataset outputs with exact headers and canonical value formatting.
