#!/usr/bin/env python3
"""Detect names in Python code that shadow bindings from outer scopes."""

from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator


SCOPE_MODULE = "module"
SCOPE_FUNCTION = "function"
SCOPE_CLASS = "class"
SCOPE_LAMBDA = "lambda"
SCOPE_COMPREHENSION = "comprehension"


@dataclass(frozen=True)
class Binding:
    name: str
    lineno: int
    kind: str


@dataclass
class Scope:
    scope_type: str
    display_name: str
    lineno: int
    parent: "Scope | None" = None
    bindings: dict[str, Binding] = field(default_factory=dict)
    children: list["Scope"] = field(default_factory=list)
    globals_declared: set[str] = field(default_factory=set)
    nonlocals_declared: set[str] = field(default_factory=set)

    def add_binding(self, name: str, lineno: int, kind: str) -> None:
        if name not in self.bindings:
            self.bindings[name] = Binding(name=name, lineno=lineno, kind=kind)


@dataclass(frozen=True)
class ShadowIssue:
    path: Path
    line: int
    name: str
    outer_line: int
    outer_scope: str
    inner_scope: str
    kind: str
    mode: str

    def format(self) -> str:
        relation = "shadows" if self.mode == "lexical" else "shadows earlier name"
        return (
            f"{self.path}:{self.line}: {self.name!r} {relation} {self.kind} from "
            f"{self.outer_scope} at line {self.outer_line} inside {self.inner_scope}"
        )


def iter_python_files(paths: Iterable[str]) -> Iterator[Path]:
    seen: set[Path] = set()
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_file():
            if path.suffix == ".py" and path not in seen:
                seen.add(path)
                yield path
            continue
        if path.is_dir():
            for candidate in sorted(path.rglob("*.py")):
                if candidate not in seen:
                    seen.add(candidate)
                    yield candidate


def assignment_targets(node: ast.AST) -> Iterator[ast.Name]:
    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
        yield node
        return
    if isinstance(node, (ast.Tuple, ast.List)):
        for elt in node.elts:
            yield from assignment_targets(elt)
        return
    if isinstance(node, ast.Starred):
        yield from assignment_targets(node.value)


class ScopeCollector(ast.NodeVisitor):
    def __init__(self, file_path: Path | None = None) -> None:
        self.root = Scope(SCOPE_MODULE, "module", 1)
        self.stack = [self.root]
        self._file_path = file_path
        self._is_init_file = file_path is not None and file_path.name == "__init__.py"

    @property
    def scope(self) -> Scope:
        return self.stack[-1]

    def push_scope(self, scope_type: str, display_name: str, lineno: int) -> Scope:
        scope = Scope(scope_type, display_name, lineno, parent=self.scope)
        self.scope.children.append(scope)
        self.stack.append(scope)
        return scope

    def pop_scope(self) -> None:
        self.stack.pop()

    def bind_arguments(self, args: ast.arguments) -> None:
        for arg in args.posonlyargs + args.args + args.kwonlyargs:
            self.scope.add_binding(arg.arg, arg.lineno, "argument")
        if args.vararg:
            self.scope.add_binding(args.vararg.arg, args.vararg.lineno, "argument")
        if args.kwarg:
            self.scope.add_binding(args.kwarg.arg, args.kwarg.lineno, "argument")

    def visit_Global(self, node: ast.Global) -> None:
        self.scope.globals_declared.update(node.names)

    def visit_Nonlocal(self, node: ast.Nonlocal) -> None:
        self.scope.nonlocals_declared.update(node.names)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.scope.add_binding(node.name, node.lineno, "function")
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.scope.add_binding(node.name, node.lineno, "function")
        self._visit_function(node)

    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        self.push_scope(SCOPE_FUNCTION, f"function {node.name}", node.lineno)
        self.bind_arguments(node.args)
        self.generic_visit(node)
        self.pop_scope()

    def visit_Lambda(self, node: ast.Lambda) -> None:
        self.push_scope(SCOPE_LAMBDA, f"lambda@{node.lineno}", node.lineno)
        self.bind_arguments(node.args)
        self.generic_visit(node)
        self.pop_scope()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.scope.add_binding(node.name, node.lineno, "class")
        self.push_scope(SCOPE_CLASS, f"class {node.name}", node.lineno)
        self.generic_visit(node)
        self.pop_scope()

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            local_name = alias.asname or alias.name.split(".", 1)[0]
            self.scope.add_binding(local_name, node.lineno, "import")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            if alias.name == "*":
                continue
            local_name = alias.asname or alias.name
            self.scope.add_binding(local_name, node.lineno, "import")
        implicit_submodule = self._implicit_submodule_name(node)
        if implicit_submodule is not None:
            self.scope.add_binding(implicit_submodule, node.lineno, "implicit submodule")

    def _implicit_submodule_name(self, node: ast.ImportFrom) -> str | None:
        if not self._is_init_file or self.scope.scope_type != SCOPE_MODULE or not node.module:
            return None
        if node.level == 1:
            return node.module.split(".", 1)[0]
        if node.level != 0 or self._file_path is None:
            return None
        candidate = node.module.rsplit(".", 1)[-1]
        init_dir = self._file_path.parent
        module_file = init_dir / f"{candidate}.py"
        module_dir = init_dir / candidate
        if module_file.exists() or module_dir.is_dir():
            return candidate
        return None

    def visit_NamedExpr(self, node: ast.NamedExpr) -> None:
        for target in assignment_targets(node.target):
            self.scope.add_binding(target.id, target.lineno, "assignment")
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            for name in assignment_targets(target):
                self.scope.add_binding(name.id, name.lineno, "assignment")
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        for name in assignment_targets(node.target):
            self.scope.add_binding(name.id, name.lineno, "assignment")
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        for name in assignment_targets(node.target):
            self.scope.add_binding(name.id, name.lineno, "assignment")
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        for name in assignment_targets(node.target):
            self.scope.add_binding(name.id, name.lineno, "loop variable")
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        for name in assignment_targets(node.target):
            self.scope.add_binding(name.id, name.lineno, "loop variable")
        self.generic_visit(node)

    def visit_With(self, node: ast.With) -> None:
        for item in node.items:
            if item.optional_vars is not None:
                for name in assignment_targets(item.optional_vars):
                    self.scope.add_binding(name.id, name.lineno, "with target")
        self.generic_visit(node)

    def visit_AsyncWith(self, node: ast.AsyncWith) -> None:
        for item in node.items:
            if item.optional_vars is not None:
                for name in assignment_targets(item.optional_vars):
                    self.scope.add_binding(name.id, name.lineno, "with target")
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if node.name:
            self.scope.add_binding(node.name, node.lineno, "except target")
        self.generic_visit(node)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self._visit_comprehension(node, "listcomp")

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self._visit_comprehension(node, "setcomp")

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self._visit_comprehension(node, "genexpr")

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self._visit_comprehension(node, "dictcomp")

    def _visit_comprehension(
        self,
        node: ast.ListComp | ast.SetComp | ast.GeneratorExp | ast.DictComp,
        label: str,
    ) -> None:
        self.push_scope(SCOPE_COMPREHENSION, f"{label}@{node.lineno}", node.lineno)
        for generator in node.generators:
            for name in assignment_targets(generator.target):
                self.scope.add_binding(name.id, name.lineno, "comprehension variable")
        self.generic_visit(node)
        self.pop_scope()


def relevant_ancestors(scope: Scope) -> Iterator[Scope]:
    parent = scope.parent
    while parent is not None:
        if not (scope.scope_type in {SCOPE_FUNCTION, SCOPE_LAMBDA} and parent.scope_type == SCOPE_CLASS):
            yield parent
        parent = parent.parent


def iter_scopes(scope: Scope) -> Iterator[Scope]:
    yield scope
    for child in scope.children:
        yield from iter_scopes(child)


def find_same_module_match(root: Scope, scope: Scope, binding: Binding) -> tuple[Scope, Binding] | None:
    best: tuple[Scope, Binding] | None = None
    for candidate_scope in iter_scopes(root):
        if candidate_scope is scope:
            continue
        candidate = candidate_scope.bindings.get(binding.name)
        if candidate is None or candidate.lineno >= binding.lineno:
            continue
        if best is None or candidate.lineno > best[1].lineno:
            best = (candidate_scope, candidate)
    return best


def find_shadow_issues(path: Path, root: Scope, mode: str) -> list[ShadowIssue]:
    issues: list[ShadowIssue] = []

    def walk(scope: Scope) -> None:
        ignored = scope.globals_declared | scope.nonlocals_declared
        for name, binding in scope.bindings.items():
            if name in ignored:
                continue
            for ancestor in relevant_ancestors(scope):
                outer = ancestor.bindings.get(name)
                if outer is None:
                    continue
                issues.append(
                    ShadowIssue(
                        path=path,
                        line=binding.lineno,
                        name=name,
                        outer_line=outer.lineno,
                        outer_scope=ancestor.display_name,
                        inner_scope=scope.display_name,
                        kind=outer.kind,
                        mode="lexical",
                    )
                )
                break
            else:
                if mode == "module" and scope.scope_type != SCOPE_MODULE:
                    same_module_match = find_same_module_match(root, scope, binding)
                    if same_module_match is not None:
                        outer_scope, outer = same_module_match
                        issues.append(
                            ShadowIssue(
                                path=path,
                                line=binding.lineno,
                                name=name,
                                outer_line=outer.lineno,
                                outer_scope=outer_scope.display_name,
                                inner_scope=scope.display_name,
                                kind=outer.kind,
                                mode="module",
                            )
                        )
        for child in scope.children:
            walk(child)

    walk(root)
    return sorted(issues, key=lambda issue: (str(issue.path), issue.line, issue.name))


def analyze_file(path: Path, mode: str) -> list[ShadowIssue]:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"{path}: unable to read file: {exc}", file=sys.stderr)
        return []
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        print(f"{path}:{exc.lineno}: syntax error: {exc.msg}", file=sys.stderr)
        return []
    collector = ScopeCollector(file_path=path)
    collector.visit(tree)
    return find_shadow_issues(path, collector.root, mode)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report Python names that shadow bindings from outer scopes."
    )
    parser.add_argument(
        "--mode",
        choices=("module", "lexical"),
        default="lexical",
        help="`lexical` matches enclosing-scope shadowing; `module` is broader and catches earlier same-module names.",
    )
    parser.add_argument("paths", nargs="+", help="Python files or directories to scan")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    files = list(iter_python_files(args.paths))
    if not files:
        print("No Python files found.", file=sys.stderr)
        return 2

    issue_count = 0
    for path in files:
        for issue in analyze_file(path, args.mode):
            issue_count += 1
            print(issue.format())
    return 1 if issue_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
