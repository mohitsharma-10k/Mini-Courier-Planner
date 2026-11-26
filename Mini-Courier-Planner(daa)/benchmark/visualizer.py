"""
Visualization Module for Capstone Assignment
Generates:
1. Pure ASCII terminal charts (renders inside console/terminal without any libraries)
2. Standalone Scalable Vector Graphics (SVG) interactive charts
3. Self-contained HTML report with responsive visual bar charts
"""
from typing import List, Dict, Any
import os


def print_ascii_bar_chart(results: List[Dict[str, Any]], metric_key: str = "Total_Pipeline_ms", label: str = "Total Pipeline Runtime (ms)"):
    """
    Prints a clean ASCII horizontal bar chart in the terminal.
    """
    print(f"\n{'='*75}")
    print(f"  PERFORMANCE BENCHMARK CHART: {label}")
    print(f"{'='*75}")

    max_val = max(row[metric_key] for row in results) if results else 1.0
    bar_max_width = 40

    for row in results:
        val = row[metric_key]
        n = row["N_Parcels"]
        bar_len = int((val / max_val) * bar_max_width) if max_val > 0 else 0
        bar = "█" * bar_len + "░" * (bar_max_width - bar_len)
        print(f"  N={n:<5d} | {bar} | {val:8.3f} ms")

    print(f"{'='*75}\n")


def export_runtime_chart_svg(results: List[Dict[str, Any]], output_filepath: str = "runtime_chart.svg"):
    """
    Creates a publication-quality SVG chart showing runtime scaling across all 4 algorithmic components.
    Zero external dependencies required.
    """
    width = 900
    height = 520
    margin_left = 90
    margin_right = 50
    margin_top = 70
    margin_bottom = 80

    chart_w = width - margin_left - margin_right
    chart_h = height - margin_top - margin_bottom

    # Find maximum values for Y scale
    max_time = max(row["Total_Pipeline_ms"] for row in results) * 1.15
    if max_time <= 0:
        max_time = 1.0

    num_groups = len(results)
    group_width = chart_w / max(1, num_groups)
    bar_width = min(22.0, (group_width - 15) / 4)

    # Colors
    c_merge = "#3b82f6"     # Blue (MergeSort)
    c_knapsack = "#10b981"  # Green (Knapsack DP)
    c_dijkstra = "#f59e0b"  # Amber (Dijkstra)
    c_tsp = "#ef4444"       # Red (TSP NN+2Opt)

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background:#ffffff; font-family: Segoe UI, Arial, sans-serif;">',
        '<!-- Header -->',
        f'<rect width="{width}" height="{height}" fill="#f8fafc" rx="12"/>',
        f'<rect x="20" y="20" width="{width-40}" height="{height-40}" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" rx="8"/>',
        f'<text x="{width/2}" y="48" text-anchor="middle" font-size="18" font-weight="bold" fill="#0f172a">Mini-Courier Planner: Algorithmic Runtime Scaling Benchmark</text>',
        f'<text x="{width/2}" y="66" text-anchor="middle" font-size="12" fill="#64748b">ETCCDA302: DAA - K.R. Mangalam University | Student: Mohit Sharma (2501010091)</text>',
    ]

    # Gridlines & Y-Axis Labels
    num_y_ticks = 5
    for i in range(num_y_ticks + 1):
        y_val = (max_time / num_y_ticks) * i
        y_pos = margin_top + chart_h - (i / num_y_ticks) * chart_h
        svg_parts.append(f'<line x1="{margin_left}" y1="{y_pos}" x2="{width - margin_right}" y2="{y_pos}" stroke="#f1f5f9" stroke-width="1.5"/>')
        svg_parts.append(f'<text x="{margin_left - 10}" y="{y_pos + 4}" text-anchor="end" font-size="11" fill="#64748b">{y_val:.2f} ms</text>')

    # Axes
    svg_parts.append(f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + chart_h}" stroke="#94a3b8" stroke-width="2"/>')
    svg_parts.append(f'<line x1="{margin_left}" y1="{margin_top + chart_h}" x2="{width - margin_right}" y2="{margin_top + chart_h}" stroke="#94a3b8" stroke-width="2"/>')

    # Bars for each dataset size N
    for idx, row in enumerate(results):
        g_center = margin_left + (idx + 0.5) * group_width
        n_label = f"N={row['N_Parcels']}"
        svg_parts.append(f'<text x="{g_center}" y="{margin_top + chart_h + 24}" text-anchor="middle" font-size="12" font-weight="600" fill="#334155">{n_label}</text>')
        svg_parts.append(f'<text x="{g_center}" y="{margin_top + chart_h + 40}" text-anchor="middle" font-size="10" fill="#94a3b8">Total: {row["Total_Pipeline_ms"]:.2f}ms</text>')

        # 4 bars: MergeSort, Knapsack, Dijkstra, TSP
        components = [
            (row["MergeSort_ms"], c_merge),
            (row["KnapsackDP_ms"], c_knapsack),
            (row["Dijkstra_ms"], c_dijkstra),
            (row["TSP_NN_2Opt_ms"], c_tsp)
        ]

        total_bar_group_w = bar_width * 4
        start_x = g_center - (total_bar_group_w / 2.0)

        for b_idx, (val, color) in enumerate(components):
            bar_h = (val / max_time) * chart_h
            bx = start_x + b_idx * bar_width
            by = margin_top + chart_h - bar_h
            svg_parts.append(f'<rect x="{bx}" y="{by}" width="{bar_width - 2}" height="{max(1.0, bar_h)}" fill="{color}" rx="2"/>')

    # Legend
    legend_items = [
        ("Merge Sort O(N log N)", c_merge),
        ("0/1 Knapsack DP O(N·W)", c_knapsack),
        ("Dijkstra Shortest Path O((V+E)log V)", c_dijkstra),
        ("TSP NN + 2-Opt O(K²)", c_tsp)
    ]
    leg_x = margin_left + 20
    leg_y = height - 25
    for item_idx, (text, col) in enumerate(legend_items):
        cx = leg_x + item_idx * 185
        svg_parts.append(f'<rect x="{cx}" y="{leg_y - 10}" width="12" height="12" fill="{col}" rx="3"/>')
        svg_parts.append(f'<text x="{cx + 18}" y="{leg_y}" font-size="11" fill="#334155">{text}</text>')

    svg_parts.append('</svg>')

    os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))


def export_interactive_html_dashboard(results: List[Dict[str, Any]], output_filepath: str = "benchmark_report.html"):
    """
    Exports a standalone HTML report with interactive data tables and visual styling.
    """
    rows_html = []
    for r in results:
        rows_html.append(f"""
        <tr>
            <td style="font-weight:600;">{r['N_Parcels']}</td>
            <td>{r['Graph_Nodes']}</td>
            <td>{r['Selected_Parcels']}</td>
            <td>{r['MergeSort_ms']:.3f} ms</td>
            <td>{r['QuickSort_ms']:.3f} ms</td>
            <td style="color:#059669; font-weight:600;">{r['KnapsackDP_ms']:.3f} ms</td>
            <td>{r['Dijkstra_ms']:.3f} ms</td>
            <td>{r['TSP_NN_2Opt_ms']:.3f} ms</td>
            <td style="font-weight:bold; color:#1e40af;">{r['Total_Pipeline_ms']:.3f} ms</td>
            <td>{r['Capacity_Util_Pct']:.1f}%</td>
            <td>{r['Tour_Distance_km']:.2f} km</td>
        </tr>
        """)

    table_body = "\n".join(rows_html)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini-Courier Planner: Capstone Benchmark Dashboard</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 24px; }}
        .container {{ max-width: 1100px; margin: 0 auto; background: #1e293b; border-radius: 12px; padding: 32px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
        h1 {{ color: #38bdf8; margin-top: 0; font-size: 26px; }}
        h2 {{ color: #94a3b8; font-size: 16px; margin-bottom: 24px; font-weight: normal; }}
        .badge {{ background: #0369a1; color: #e0f2fe; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 13px; }}
        th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #334155; }}
        th {{ background: #0f172a; color: #38bdf8; font-weight: 600; text-transform: uppercase; font-size: 11px; }}
        tr:hover {{ background: #293548; }}
        .chart-box {{ margin-top: 30px; text-align: center; background: #ffffff; padding: 16px; border-radius: 8px; }}
        .card-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 20px; }}
        .card {{ background: #0f172a; padding: 16px; border-radius: 8px; border-left: 4px solid #38bdf8; }}
        .card-title {{ font-size: 12px; color: #94a3b8; }}
        .card-val {{ font-size: 20px; font-weight: bold; color: #f8fafc; margin-top: 4px; }}
    </style>
</head>
<body>
    <div class="container">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <h1>Mini-Courier Planner &bull; Algorithmic Performance Report</h1>
            <span class="badge">ETCCDA302 Capstone</span>
        </div>
        <h2>K.R. Mangalam University | Design & Analysis of Algorithms | Student: Mohit Sharma (Roll No: 2501010091)</h2>

        <div class="card-grid">
            <div class="card" style="border-left-color: #3b82f6;">
                <div class="card-title">Sorting Module</div>
                <div class="card-val">Merge Sort O(N log N)</div>
            </div>
            <div class="card" style="border-left-color: #10b981;">
                <div class="card-title">Packing Optimizer</div>
                <div class="card-val">0/1 Knapsack DP O(N&middot;W)</div>
            </div>
            <div class="card" style="border-left-color: #f59e0b;">
                <div class="card-title">Shortest Path</div>
                <div class="card-val">Dijkstra Min-Heap</div>
            </div>
            <div class="card" style="border-left-color: #ef4444;">
                <div class="card-title">Route Planner</div>
                <div class="card-val">TSP NN + 2-Opt</div>
            </div>
        </div>

        <h3 style="margin-top: 30px; color: #f1f5f9;">Comparative Execution Times across Input Sizes</h3>
        <table>
            <thead>
                <tr>
                    <th>N Parcels</th>
                    <th>Nodes</th>
                    <th>Selected</th>
                    <th>MergeSort</th>
                    <th>QuickSort</th>
                    <th>0/1 Knapsack</th>
                    <th>Dijkstra</th>
                    <th>TSP (NN+2Opt)</th>
                    <th>Total Time</th>
                    <th>Util %</th>
                    <th>Tour Dist</th>
                </tr>
            </thead>
            <tbody>
                {table_body}
            </tbody>
        </table>

        <div class="chart-box">
            <h4 style="color:#0f172a; margin:0 0 12px 0;">Algorithmic Scaling Vector Graphic (SVG)</h4>
            <object data="runtime_chart.svg" type="image/svg+xml" style="max-width:100%; height:auto;"></object>
        </div>
    </div>
</body>
</html>
"""
    os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
