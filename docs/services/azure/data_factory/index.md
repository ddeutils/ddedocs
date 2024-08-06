# Azure Data Factory

## Getting Started

## Syntax

### Coalesce

If an incoming value that you want to extract;

```json title="P_EXTRACT"
{
    "parent": {
      "child": {
        "key": "value"
      }
    }
}
```

```text
@coalesce(parameters.P_EXTRACT.parent.child?.key, 'default')
```
