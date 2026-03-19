---
id: 1-6-git-history
title: "1.6 The History of Truth"
sidebar_label: "1.6 Git & Version Control"
description: "DAGs, Merkle Trees, and the theory of Distributed Logic."
---

# 1.6 The History of Truth
**Stage I: The Substrate**

> "Code without history is just a snapshot of a thought. Git turns code into a narrative."

## 1. The Directed Acyclic Graph (DAG)

Git is not a file backup system. It is a **Content-Addressable Filesystem**.
Every commit is a node in a graph.
Every node points to its parent(s).
No cycles allowed (Acyclic).

### The Hash (SHA-1)
Every object is named by the hash of its contents.
If you change one byte in a file, the file's hash changes.
The directory tree hash changes.
The commit hash changes.
The downstream history changes.
**Merkle Tree**: This ensures cryptographic integrity. You cannot alter the past without changing the future.

---

## 2. Pointers (HEAD, Branches, Tags)

A **Branch** is just a sticky note with a Commit Hash on it.
When you "move a branch", you are just peeling the sticker off one node and putting it on another.
**HEAD** is a pointer to the current branch.

### Detached HEAD
Ideally, HEAD points to a Branch Name (Ref).
If HEAD points directly to a Commit Hash, it is "Detached". You are floating in the graph with no sticky note to mark your progress. Any new commits will be lost to the Garbage Collector if you switch away.

---

## 3. Distributed Consensus

Merge Conflicts are not errors. They are **diverging realities**.
Two authors claimed two different truths for line 42.
The "Merge" operation is the act of reconciling these truths into a new consensus node.

### Fact: Rebase vs. Merge
*   **Merge**: Preserves history. "This happened, then that happened, then we combined them." Truthful but messy.
*   **Rebase**: Rewrites history. "I pretend I wrote my changes *after* yours." Linearity over honesty.

---

## Deep FAQ

> **Q: What is the Staging Area (Index)?**
> A: It is the draft. Git has three trees:
> 1.  **Working Directory**: Your actual files on disk.
> 2.  **Index (Staging)**: The proposed next commit snapshot.
> 3.  **HEAD**: The last committed snapshot.
> `git add` moves data from 1 to 2. `git commit` moves data from 2 to 3.

> **Q: Can I delete a commit forever?**
> A: Yes and no. `git reset --hard` moves the branch pointer. The commit node still exists in the database until `git gc` (Garbage Collection) runs and sees it has no references pointing to it.
