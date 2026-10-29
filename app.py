import ast
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import streamlit as st
from radon.complexity import cc_visit
from radon.metrics import mi_visit


st.set_page_config(
    page_title="CodeMind AI",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 CodeMind AI")
st.subheader("Intelligent Code Review and Quality Analysis")

st.write(
    "Analyze Python code, identify code-quality issues, "
    "and measure code complexity and maintainability."
)

with st.sidebar:
    st.header("Project Information")
    st.write("Language: Python")
    st.write("Interface: Streamlit")
    st.write("Static Analysis: Ruff")
    st.write("Complexity Analysis: Radon")

    st.info(
        "This application analyzes Python code "
        "without executing the submitted code."
    )


sample_code = '''def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def main():
    print(divide(10, 2))


if __name__ == "__main__":
    main()
'''


code = st.text_area(
    "Paste your Python code here:",
    value=sample_code,
    height=300,
)


def analyze_with_ruff(source_code):
    """Analyze Python code using Ruff."""

    ruff_path = shutil.which("ruff")

    if ruff_path is None:
        raise RuntimeError(
            "Ruff is not installed. Run: "
            "python -m pip install ruff"
        )

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "submitted_code.py"

        file_path.write_text(
            source_code,
            encoding="utf-8",
        )

        result = subprocess.run(
            [
                ruff_path,
                "check",
                "--output-format",
                "json",
                str(file_path),
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        if result.returncode not in (0, 1):
            raise RuntimeError(
                result.stderr.strip()
                or "Ruff analysis failed."
            )

        return json.loads(result.stdout or "[]")


if st.button("Analyze Code", type="primary"):

    if not code.strip():
        st.warning("Please enter some Python code.")

    else:
        try:
            ast.parse(code)

        except SyntaxError as error:
            st.error(
                f"Syntax error on line {error.lineno}: "
                f"{error.msg}"
            )

        else:
            st.success("Python syntax is valid!")

            st.header("1. Static Analysis")

            try:
                issues = analyze_with_ruff(code)

                if not issues:
                    st.success("No Ruff issues detected.")

                else:
                    st.warning(
                        f"Ruff detected {len(issues)} issue(s)."
                    )

                    for issue in issues:
                        location = issue.get("location", {})
                        row = location.get("row", "?")
                        column = location.get("column", "?")

                        with st.expander(
                            f"{issue.get('code', 'Issue')} "
                            f"- Line {row}"
                        ):
                            st.write(
                                issue.get(
                                    "message",
                                    "No description available.",
                                )
                            )
                            st.caption(f"Column: {column}")

            except (
                OSError,
                RuntimeError,
                json.JSONDecodeError,
                subprocess.TimeoutExpired,
            ) as error:
                st.error(
                    f"Static analysis failed: {error}"
                )

            st.header("2. Code Quality Metrics")

            try:
                blocks = cc_visit(code)
                maintainability = mi_visit(
                    code,
                    multi=False,
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Lines of Code",
                    len(code.splitlines()),
                )

                col2.metric(
                    "Functions and Classes",
                    len(blocks),
                )

                col3.metric(
                    "Maintainability Index",
                    f"{maintainability:.1f}",
                )

                st.subheader("Cyclomatic Complexity")

                if blocks:
                    for block in blocks:
                        st.write(
                            f"**{block.name}** — "
                            f"Complexity: {block.complexity}"
                        )

                        if block.complexity > 10:
                            st.warning(
                                f"{block.name} may benefit "
                                "from simpler logic."
                            )

                else:
                    st.write(
                        "No functions or classes were found "
                        "for complexity reporting."
                    )

            except (SyntaxError, ValueError) as error:
                st.warning(
                    f"Could not calculate code metrics: {error}"
                )

            st.header("3. Recommendations")

            recommendations = [
                "Review reported static-analysis issues.",
                "Test normal inputs and edge cases.",
                "Handle invalid inputs and exceptions.",
                "Simplify functions with high complexity.",
                "Add unit tests to verify expected behavior.",
            ]

            for number, recommendation in enumerate(
                recommendations,
                start=1,
            ):
                st.write(f"{number}. {recommendation}")

            st.caption(
                "Static analysis cannot detect every defect. "
                "A clean report does not guarantee bug-free code."
            )


st.divider()
st.caption(
    "CodeMind AI | Educational Code Analysis Prototype"
)