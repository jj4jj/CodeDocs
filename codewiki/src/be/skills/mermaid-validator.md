Use this skill to keep Mermaid diagrams compatible with the viewer runtime (`mermaid@11.9.0`).

Validation rules:
1. Never finish with Mermaid parser errors.
2. For `classDiagram`, avoid Go-style tuple return signatures like `([]ObjectInfo, error)`.
3. Keep method signatures simple, for example: `+ListObjects(ctx, opts) ObjectList`.
4. If validation reports an error, edit the diagram immediately and re-validate.

Project validation code:
```python
import asyncio
from codewiki.src.be.utils import validate_mermaid_diagrams

result = asyncio.run(validate_mermaid_diagrams("path/to/doc.md", "doc.md"))
print(result)
```

Completion criteria:
- Every generated markdown file with Mermaid blocks must pass validation with no syntax errors.
