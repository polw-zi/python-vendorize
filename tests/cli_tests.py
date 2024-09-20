import os
import shutil
import contextlib

from spur import LocalShell

_local = LocalShell()

def example_path(example_name):
    return os.path.join(os.path.dirname(__file__), "../examples", example_name)

def normalize_line_separator(s):
    return s.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

def test_vendorizing_single_module_with_no_dependencies_grabs_one_module_file():
    with _vendorize_example("isolated-module") as project_path:
        result = _local.run(["python", os.path.join(project_path, "main.py")])
        assert b"('one', 1)" == normalize_line_separator(result.output.strip())

def test_can_vendorize_local_modules_from_relative_paths():
    with _vendorize_example("local-module") as project_path:
        result = _local.run(["python", os.path.join(project_path, "main.py")])
        assert b"hello\n" == normalize_line_separator(result.output)

def test_absolute_paths_in_same_distribution_are_rewritten_to_be_relative():
    with _vendorize_example("absolute-import-rewrite") as project_path:
        result = _local.run(["python", os.path.join(project_path, "main.py")])
        assert b"hello\n" == normalize_line_separator(result.output)

def test_can_rewrite_indented_absolute_simple_imports():
    with _vendorize_example("indented-absolute-simple-import-rewrite") as project_path:
        result = _local.run(["python", os.path.join(project_path, "main.py")])
        assert b"hello\n" == normalize_line_separator(result.output)

def test_can_vendorize_multiple_dependencies():
    with _vendorize_example("multiple-dependencies") as project_path:
        result = _local.run(["python", os.path.join(project_path, "main.py")])
        assert b"hello\nworld\n" == normalize_line_separator(result.output)

def test_can_vendorize_multiple_dependencies_that_require_import_rewriting():
    with _vendorize_example("multiple-dependencies-with-rewrite") as project_path:
        result = _local.run(["python", os.path.join(project_path, "main.py")])
        assert b"hello\nworld\n" == normalize_line_separator(result.output)

def test_can_vendorize_with_pyproject_toml():
    with _vendorize_example("isolated-module-pyproject") as project_path:
        result = _local.run(["python", os.path.join(project_path, "main.py")])
        assert b"('one', 1)" == normalize_line_separator(result.output.strip())

@contextlib.contextmanager
def _vendorize_example(example_name):
    path = example_path(example_name)
    _clean_project(path)
    _local.run(["python-vendorize"], cwd=path, encoding="utf-8")
    yield path


def _clean_project(path):
    vendor_path = os.path.join(path, "_vendor")
    if os.path.exists(vendor_path):
        shutil.rmtree(vendor_path)


def test_upgrade():
    example_name = "isolated-module"
    path = os.path.join(example_path(example_name), "_vendor/")
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, "six.py"), "w+") as f:
        f.write("print('Not six')")

    _local.run(
        ["python-vendorize", "--upgrade"],
        cwd=example_path(example_name),
        encoding="utf-8"
    )
    with open(os.path.join(path, "six.py"), "r+") as f:
        assert 'Not six' not in f.read()

    _clean_project(path)