---
name: todo-list
description: Help users organize, prioritize, and manage their task lists. Use when user wants to create a TODO list, organize tasks, prioritize work, track progress, or manage deadlines. Trigger when user mentions tasks, to-do lists, project planning, or managing their workload.
---

# TODO List Management

This skill provides a structured workflow for helping users organize and manage their tasks effectively. Act as an active guide to help users build clear, actionable task lists and track progress.

## When to Offer This Workflow

**Trigger conditions:**
- User mentions managing tasks: "create a to-do list", "organize my tasks", "track my work"
- User mentions specific todo contexts: "project planning", "sprint planning", "deadline tracking"
- User seems overwhelmed by multiple things to do
- User wants to prioritize or break down a large project

**Initial offer:**
Offer the user a structured workflow for managing their tasks. Explain that you can help them:

1. **Organize & Clarify**: Capture all tasks and clarify what needs to be done
2. **Prioritize & Plan**: Help prioritize tasks and break down complex items into actionable steps
3. **Track & Update**: Monitor progress and adjust the list as priorities shift

Ask if they want to use this workflow or prefer a simpler approach.

## Stage 1: Capture & Clarify

**Goal:** Get a complete picture of everything the user needs to do.

### Initial Questions

Start by asking the user:

1. What's the scope of this task list? (e.g., personal, work project, specific initiative)
2. What's the timeframe? (e.g., this week, this month, ongoing)
3. Are there existing lists or documents with tasks we should incorporate?
4. What's the main goal or outcome you're working toward?

Inform them they can answer quickly or provide as much detail as needed.

**If user provides existing documents or lists:**
- Ask them to share the file or paste the content
- Read and organize the existing tasks
- Identify any duplicate or related items

### Task Capture

Once you understand the scope, help the user capture all tasks. Ask:

- What are the main things you need to get done?
- Are there subtasks or dependencies between items?
- Which items are blocking others?
- Are there any recurring or one-time tasks?

**Organization tips:**
- Group related tasks into categories
- Identify task dependencies (what needs to happen first)
- Note any constraints: deadlines, resources, or prerequisites

**Exit condition:**
All tasks have been captured when the user confirms nothing is missing and they feel the list is complete.

## Stage 2: Prioritize & Plan

**Goal:** Create a realistic plan with clear priorities.

### Prioritization

Help the user prioritize by asking:

1. **Urgency vs. Importance**: Which tasks are urgent? Which are important but not urgent?
2. **Impact**: Which tasks have the biggest impact on the main goal?
3. **Dependencies**: What must be done first?
4. **Capacity**: How much time is realistically available?

Use a prioritization framework:
- **High Priority (P0)**: Critical path items, immediate deadlines, blocking other work
- **Medium Priority (P1)**: Important but not immediately urgent
- **Low Priority (P2)**: Nice to have, can be deferred

**Breaking Down Complex Tasks**

For larger items, break them into smaller, actionable steps:
- Each step should be completable in a reasonable timeframe (ideally 1-4 hours)
- Include any prep work or research needed
- Identify success criteria for each step

### Planning Timeline

Help create a realistic timeline:
- Assign target dates or weeks for each task
- Account for task duration and dependencies
- Build in buffer time for unexpected issues
- Highlight critical path items

## Stage 3: Track & Maintain

**Goal:** Keep the list current and monitor progress.

### Suggested Format

Structure the TODO list for clarity:
- **Today/This Week**: High-priority items due soon
- **Next Week/Soon**: Medium priority items with upcoming dates
- **Later**: Low priority or items with no specific deadline
- **On Hold**: Blocked tasks or deferred items

Or organize by:
- **Project/Category**: Group by area of work
- **Status**: Not Started → In Progress → Complete

### Regular Updates

Suggest a regular review cadence:
- **Daily**: Review today's tasks and prioritize
- **Weekly**: Assess progress, adjust priorities, plan next week
- **Monthly**: Review larger goals and adjust the overall plan

**During reviews, help the user:**
- Mark completed tasks
- Reassess priorities based on new information
- Identify blockers and dependencies
- Add new tasks as they emerge
- Adjust timeline if needed

### Progress Tracking

Keep the user motivated by:
- Celebrating completed tasks
- Highlighting progress on large projects
- Identifying which tasks consistently slip
- Adjusting estimates if patterns emerge

## Example TODO List Format

```
# Q2 2024 Work Plan

## This Week (High Priority)
- [ ] Complete quarterly review report (due Fri)
  - [ ] Gather metrics from team
  - [ ] Write analysis and recommendations
  - [ ] Get manager feedback
- [ ] Prepare for client presentation (due Wed)
  - [ ] Update slides with latest data
  - [ ] Practice presentation
- [ ] Code review for feature-x branch (depends on: feature completion)

## Next Week
- [ ] Plan Q3 roadmap session
- [ ] Onboard new team member
  - [ ] Prepare welcome doc
  - [ ] Schedule pairing sessions
  - [ ] Set up development environment

## Later (Lower Priority)
- [ ] Refactor authentication module (no deadline yet)
- [ ] Update documentation (nice to have)

## On Hold
- [ ] API redesign (waiting for product requirements)
```

## Guidelines

- **Keep tasks specific and actionable**: "Update docs" is vague; "Add API examples to auth documentation" is clear
- **Avoid too-granular lists**: Breaking everything into tiny tasks makes the list overwhelming
- **Group related work**: Keep context switching to a minimum
- **Update regularly**: A stale list loses value quickly
- **Be realistic about capacity**: Better to do fewer things well than overcommit
- **Celebrate progress**: Regularly review what you've accomplished

## When to Adjust the Workflow

- If the user prefers a simpler approach: Just create a basic list without the full framework
- If tasks are ongoing or recurring: Use a different structure than time-based
- If managing a team: Add sections for delegated tasks and team dependencies
