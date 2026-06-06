# Claude Skills Repository - Development Guide

## Repository Overview

This is Anthropic's official repository of **Claude Skills** - reusable, self-contained instruction sets that extend Claude's capabilities for specialized tasks. Skills enable Claude to perform consistent, repeatable workflows across different domains: document creation and editing, web testing, design, development tooling, creative applications, and enterprise workflows.

**Key Resources:**
- Official Skills Documentation: [support.claude.com](https://support.claude.com/en/articles/12512176-what-are-skills)
- Agent Skills Standard: [agentskills.io](http://agentskills.io)
- Skills API Guide: [docs.claude.com](https://docs.claude.com/en/api/skills-guide)

## Project Structure

```
skills/
├── skills/                          # Individual skill directories
│   ├── algorithmic-art/            # Creative algorithmic generation
│   ├── brand-guidelines/           # Brand compliance and visual design
│   ├── canvas-design/              # Canvas-based visual design
│   ├── claude-api/                 # Claude API & SDK documentation
│   ├── doc-coauthoring/            # Collaborative document editing
│   ├── docx/                       # Word document processing (source-available)
│   ├── frontend-design/            # Frontend UI/UX patterns
│   ├── internal-comms/             # Internal communication workflows
│   ├── mcp-builder/                # MCP server generation
│   ├── pdf/                        # PDF processing (source-available)
│   ├── pptx/                       # PowerPoint processing (source-available)
│   ├── skill-creator/              # Skill creation and optimization
│   ├── slack-gif-creator/          # Slack GIF animation generation
│   ├── theme-factory/              # Theme and styling generation
│   ├── web-artifacts-builder/      # Web artifact creation
│   ├── webapp-testing/             # Web application testing
│   └── xlsx/                       # Excel spreadsheet processing (source-available)
├── spec/                           # Agent Skills specification
├── template/                       # Skill template for new skills
├── .claude-plugin/                 # Plugin marketplace configuration
├── README.md                       # User-facing project documentation
├── THIRD_PARTY_NOTICES.md         # License information
└── CLAUDE.md                       # This file - developer guide
```

## Skill Anatomy and Structure

Every skill is a directory containing:

### Required Files
- **SKILL.md** - The core skill file with YAML frontmatter and instructions

### Optional Bundled Resources
- **scripts/** - Python, JavaScript, or shell scripts used by the skill
- **reference.md** - Detailed reference documentation (e.g., PDF skill)
- **forms.md** - Specific form handling instructions (e.g., PDF forms)
- **LICENSE.txt** - License information (required for proprietary skills)
- **README.md** - Additional documentation
- **images/**, **templates/**, **examples/** - Support assets

### SKILL.md Format

Every SKILL.md begins with YAML frontmatter:

```yaml
---
name: skill-identifier           # Required: lowercase, hyphens for spaces
description: Clear, actionable   # Required: when to use + what it does
license: Apache 2.0 | Proprietary # Optional: defaults to Apache 2.0
compatibility: [tool/dependency] # Optional: required tools or dependencies
---

# Skill Title

[Markdown instructions follow...]
```

**Key conventions for skill descriptions:**
- Include both "what it does" AND "when to use it"
- Be explicit about trigger conditions (e.g., "whenever the user mentions X, use this skill")
- Skills tend to undertrigger, so descriptions should be slightly "pushy"
- Example: "Use this skill whenever the user mentions PDFs, wants to extract data, combine documents, fill forms, or create PDF reports"

## Skill Categories

### 1. **Document Skills** (Source-Available)
These are production-grade skills powering Claude's document capabilities. Available in the `document-skills` plugin bundle.

- **docx**: Word document creation, editing, styling, redlining, change tracking
- **pptx**: PowerPoint slides, animations, layouts, visual design
- **pdf**: PDF reading, extraction, merging, form filling, encryption, OCR
- **xlsx**: Excel spreadsheet operations, formulas, data management, validation

**License:** Source-available (reference implementations, not open source)

### 2. **Development & Technical Skills**
Tools for developers and engineers.

- **claude-api**: Claude API and SDK documentation, model selection, best practices
- **mcp-builder**: Generate MCP (Model Context Protocol) servers
- **skill-creator**: Create new skills, run evals, optimize skill descriptions
- **webapp-testing**: Web application testing with browser automation

### 3. **Design & Creative Skills**
Visual design and creative content generation.

- **algorithmic-art**: Procedural art generation
- **canvas-design**: Canvas-based visual design tools
- **frontend-design**: Frontend UI patterns and component design
- **theme-factory**: Dynamic theme and style generation
- **web-artifacts-builder**: Web artifact creation and deployment

### 4. **Enterprise & Communication Skills**
Business workflows and internal communications.

- **brand-guidelines**: Brand compliance, visual standards enforcement
- **internal-comms**: Internal communication templates and workflows
- **doc-coauthoring**: Collaborative document editing
- **slack-gif-creator**: Animated GIF creation for Slack

## Key Development Conventions

### 1. **Writing Skill Instructions**

**Do:**
- Use clear, step-by-step instructions
- Include concrete examples and code snippets
- Document edge cases and limitations
- Provide reference materials for complex skills
- Format code blocks with language specifiers (```python, ```javascript, etc.)

**Don't:**
- Add comments explaining "what" the code does (variable names should be self-documenting)
- Over-comment or create unnecessary abstractions
- Include boilerplate error handling for impossible scenarios
- Create premature abstractions (three similar lines is better than over-engineering)

### 2. **Skill Names and Identifiers**
- Use lowercase with hyphens for multi-word names
- Keep names concise but descriptive
- Match directory name to skill name identifier

### 3. **Script Organization**

Scripts should be:
- Well-organized by function/purpose
- Documented with clear usage instructions in SKILL.md
- Python or JavaScript preferred (platform compatibility)
- Licensed appropriately (proprietary skills need LICENSE.txt)

### 4. **Testing Skills**

Skills can be tested using Claude directly:
1. Write test prompts covering common use cases
2. Run prompts with the skill enabled
3. Evaluate results qualitatively
4. Run quantitative benchmarks using skill-creator's eval tools
5. Iterate based on feedback

The **skill-creator** skill includes tools for:
- Writing test case assertions
- Running evaluations against test prompts
- Benchmarking performance with variance analysis
- Optimizing skill descriptions for triggering accuracy

## Plugin Marketplace Structure

Skills are bundled into plugins via `.claude-plugin/marketplace.json`:

**Three Plugin Bundles:**
1. **document-skills** - Professional document processing (docx, pptx, pdf, xlsx)
2. **example-skills** - Demonstration skills across multiple domains
3. **claude-api** - API/SDK documentation and migration guides

Installation methods:
```bash
# Via Claude Code CLI
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
/plugin install claude-api@anthropic-agent-skills

# Or add the marketplace
/plugin marketplace add anthropics/skills
```

## Common Workflows

### Creating a New Skill

1. **Copy the template**: Use `template/SKILL.md` as a starting point
2. **Create the skill directory**: `skills/my-new-skill/`
3. **Write SKILL.md**:
   - Complete YAML frontmatter (name, description)
   - Clear instructions with examples
   - Include trigger conditions in description
4. **Add supporting files** as needed (scripts, reference docs)
5. **Test thoroughly** with Claude
6. **Update marketplace.json** if adding to a plugin bundle
7. **Commit and push** to feature branch

### Modifying Existing Skills

1. Update `SKILL.md` with improved instructions
2. Add/update supporting scripts in `scripts/` directory
3. Run evaluations to ensure quality
4. Test edge cases and regressions
5. Commit with clear message describing changes

### Running Skill Evaluations

Use the **skill-creator** skill:
```python
# Quantitative eval format (JSON assertions)
{
  "prompt": "user query",
  "expected_output_properties": {
    "has_code": true,
    "code_language": "python"
  }
}
```

The skill-creator provides:
- Test case execution
- Variance analysis
- Performance benchmarking
- Description optimization

## File Modification Guidelines

### README.md
- Publicly visible, user-facing documentation
- Explains what skills are and how to use them
- Documents installation methods
- Includes disclaimers about reference implementations

### SKILL.md Files
- Instructions must be clear and complete
- Include examples for complex operations
- Document all required dependencies
- Describe edge cases and limitations
- Be explicit about skill triggers

### Scripts
- Keep organized and focused
- Document with clear usage examples in SKILL.md
- Test with typical inputs
- License appropriately for proprietary skills

### LICENSE.txt
- Required for proprietary/source-available skills
- Include full license terms
- Reference in SKILL.md frontmatter

## Licensing

**Default:** Apache 2.0 for example/demonstration skills

**Exceptions:**
- Document skills (docx, pdf, pptx, xlsx): **Source-available, not open source**
  - Licensed under Anthropic proprietary license
  - Provided as reference implementations
  - LICENSE.txt included in each skill directory

Always check SKILL.md frontmatter and LICENSE.txt files for current licensing.

## Quality Standards

### Before Committing Skills

1. ✅ YAML frontmatter is valid and complete
2. ✅ Instructions are clear with concrete examples
3. ✅ Skill triggers are explicitly described
4. ✅ Scripts are tested and functional
5. ✅ Edge cases are documented
6. ✅ License information is accurate
7. ✅ No syntax errors in SKILL.md
8. ✅ Supporting files are organized

### Testing Checklist

- [ ] Skill description accurately triggers on relevant prompts
- [ ] Instructions are clear and actionable
- [ ] Code examples work correctly
- [ ] Edge cases are handled gracefully
- [ ] No broken references or imports
- [ ] Scripts output expected results

## Repository Guidelines

### Git Conventions
- Work on feature branches (not main)
- Use clear, descriptive commit messages
- Reference skill improvements in commit messages
- Keep commits focused (one skill per commit when possible)

### Code Style
- Python: Follow PEP 8
- JavaScript: Use consistent formatting
- Shell scripts: Quote variables, handle edge cases
- Markdown: Use standard GFM with code fence language specifiers

### No Secrets
- Never commit API keys, credentials, or tokens
- .gitignore excludes: .DS_Store, __pycache__/, .idea/, .vscode/
- Use environment variables for sensitive configuration

## AI Assistant Guidelines

When working with this repository, AI assistants should:

1. **Understand the skill model**: Skills are instruction sets, not code frameworks
2. **Respect existing patterns**: Follow conventions established in similar skills
3. **Prioritize clarity**: Instructions are read by humans across skill levels
4. **Document thoroughly**: Include examples, edge cases, and reference materials
5. **Test before shipping**: Use Claude directly to verify skill behavior
6. **Be precise about triggers**: Explicitly state when skills should be used
7. **License appropriately**: Check and respect licensing requirements
8. **Avoid over-engineering**: Skills are about teaching Claude to perform tasks, not building infrastructure

## Useful Aliases and Commands

```bash
# Show all skills
find skills -name "SKILL.md" | sort

# Check for syntax errors (if using a linter)
# Validate YAML frontmatter and markdown structure

# Search within skills
grep -r "keyword" skills/ --include="SKILL.md"

# Count skills by category
ls -la skills/ | grep "^d" | wc -l
```

## References

- **Official Skills Docs**: https://support.claude.com/en/articles/12512176-what-are-skills
- **Creating Custom Skills**: https://support.claude.com/en/articles/12512198-creating-custom-skills
- **Agent Skills Spec**: https://agentskills.io/specification
- **Skills API Quickstart**: https://docs.claude.com/en/api/skills-guide
- **Anthropic Blog**: https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

## Current Branches

- **main** - Production-ready skills, stable
- **Feature branches** - Development work for new/improved skills

Always develop on feature branches and push to the designated development branch. Create pull requests for review before merging to main.
