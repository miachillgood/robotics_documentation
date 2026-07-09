# Migration divergence patches

This directory tracks repository-specific divergences from the upstream docs template.

## When to use these patches

Whenever you do an upstream migration or sync (template refresh, stack migration, or baseline sync), apply all patches in this directory after syncing upstream changes.

## How to apply

From the repository root:

```bash
git apply patches/*.patch
```
