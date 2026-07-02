---
sequential_nav: none
---

# How-to guides

% Include start summary

**How-to guides** to achieve specific goals with Canonical's robotics stack.

% Include stop summary

## Development

```{include} development/index.rst
   :start-after: .. Include start summary
   :end-before: .. Include stop summary
```

```{toctree}
:maxdepth: 2

development/index
```

## Packaging

```{include} packaging/index.rst
   :start-after: .. Include start summary
   :end-before: .. Include stop summary
```

```{toctree}
:maxdepth: 2

packaging/index
```

## Operation

```{include} operation/index.rst
   :start-after: .. Include start summary
   :end-before: .. Include stop summary
```

```{toctree}
:maxdepth: 2

operation/index
```

## Maintenance

```{include} maintenance/index.rst
   :start-after: .. Include start summary
   :end-before: .. Include stop summary
```

```{toctree}
:maxdepth: 2

maintenance/index
```

## Security

```{include} security/hardening-your-robot.md
   :start-after: % Include start summary
   :end-before: % Include stop summary
```

* [Hardening your robot](./security/hardening-your-robot.md)

```{toctree}
:hidden:
:maxdepth: 2

Security <security/hardening-your-robot.md>
```
