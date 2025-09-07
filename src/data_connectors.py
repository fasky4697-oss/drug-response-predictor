import os
import pandas as pd
import io

def load_example_data():
    # tiny toy dataset: 50 genes x 30 samples
    expr_csv = pkg_data("example_data/sample_expression.csv")
    target_csv = pkg_data("example_data/sample_drug_response.csv")
    expr = pd.read_csv(expr_csv, index_col=0)
    target = pd.read_csv(target_csv)
    return expr, target

def read_uploaded_csvs(uploaded_files):
    """Expect two CSVs: expression (genes x samples) and target (sample, response).
    Return (expr_df, target_df) or (None, None) on failure."""
    if not uploaded_files or len(uploaded_files) < 1:
        return None, None
    # Simple heuristic: pick largest file as expression
    files = sorted(uploaded_files, key=lambda f: -getattr(f, "size", 0))
    try:
        expr = pd.read_csv(files[0])
        # if first column is gene names, set index
        if expr.columns[0].lower() in ("gene", "gene_id", "genes", "id"):
            expr = expr.set_index(expr.columns[0])
        target = None
        if len(files) > 1:
            target = pd.read_csv(files[1])
        return expr, target
    except Exception as e:
        print("read_uploaded_csvs error", e)
        return None, None

# helper to return packaged example file path (relative to project root)
def pkg_data(relpath: str) -> str:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_dir, relpath)
