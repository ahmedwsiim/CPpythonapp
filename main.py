from flask import Flask, render_template_string
import psutil

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Health Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --glass-bg: rgba(30, 41, 59, 0.7);
            --glass-border: rgba(255, 255, 255, 0.1);
            --primary: #38bdf8;
            --secondary: #818cf8;
            --success: #34d399;
            --warning: #fbbf24;
            --danger: #ef4444;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background: radial-gradient(circle at top right, #1e1b4b, #0f172a, #020617);
            color: #f8fafc;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 2rem;
            box-sizing: border-box;
            overflow-x: hidden;
        }

        h1 {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
            text-align: center;
            animation: fadeInDown 1s ease-out;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            width: 100%;
            max-width: 1200px;
        }

        .metric-card {
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            animation: fadeInUp 0.8s ease-out backwards;
        }

        .metric-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
            border-color: rgba(255, 255, 255, 0.2);
        }

        .metric-card:nth-child(1) { animation-delay: 0.1s; }
        .metric-card:nth-child(2) { animation-delay: 0.2s; }
        .metric-card:nth-child(3) { animation-delay: 0.3s; }

        .icon-wrapper {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(129, 140, 248, 0.2));
            border: 1px solid rgba(56, 189, 248, 0.3);
        }

        .icon-wrapper svg {
            width: 40px;
            height: 40px;
            stroke: var(--primary);
        }

        .metric-name {
            font-size: 1.25rem;
            font-weight: 500;
            color: #cbd5e1;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .metric-value {
            font-size: 3.5rem;
            font-weight: 700;
            margin: 0;
            display: flex;
            align-items: baseline;
        }

        .metric-value span {
            font-size: 1.5rem;
            margin-left: 0.25rem;
            color: #94a3b8;
        }

        .progress-bar-bg {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            margin-top: 1.5rem;
            overflow: hidden;
            position: relative;
        }

        .progress-bar-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            position: relative;
        }
        
        .progress-bar-fill::after {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.3) 50%, rgba(255,255,255,0) 100%);
            animation: shimmer 2s infinite linear;
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(40px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes shimmer {
            from { transform: translateX(-100%); }
            to { transform: translateX(100%); }
        }

        .refresh-btn {
            margin-top: 4rem;
            padding: 1rem 2.5rem;
            font-family: inherit;
            font-size: 1.1rem;
            font-weight: 500;
            color: #fff;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none;
            border-radius: 30px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4);
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        
        .refresh-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(56, 189, 248, 0.6);
        }
        
        .refresh-btn:active {
            transform: translateY(1px);
        }

        .fill-cpu { background: linear-gradient(90deg, #38bdf8, #818cf8); }
        .fill-ram { background: linear-gradient(90deg, #34d399, #10b981); }
        .fill-disk { background: linear-gradient(90deg, #f472b6, #e11d48); }
        
        .icon-cpu svg { stroke: #818cf8; }
        .icon-ram svg { stroke: #34d399; }
        .icon-disk svg { stroke: #f472b6; }
    </style>
</head>
<body>
    <h1>System Monitor</h1>
    
    <div class="dashboard-grid">
        <!-- CPU Card -->
        <div class="metric-card">
            <div class="icon-wrapper icon-cpu" style="background: linear-gradient(135deg, rgba(129, 140, 248, 0.2), rgba(56, 189, 248, 0.2)); border-color: rgba(129, 140, 248, 0.3);">
                <svg fill="none" viewBox="0 0 24 24" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 3v1.5M4.5 8.25H3m18 0h-1.5M4.5 12H3m18 0h-1.5m-15 3.75H3m18 0h-1.5M8.25 19.5V21M12 3v1.5m0 15V21m3.75-18v1.5m0 15V21m-9-1.5h10.5a2.25 2.25 0 002.25-2.25V6.75a2.25 2.25 0 00-2.25-2.25H6.75A2.25 2.25 0 004.5 6.75v10.5a2.25 2.25 0 002.25 2.25zm.75-12h9v9h-9v-9z" />
                </svg>
            </div>
            <div class="metric-name">CPU Usage</div>
            <div class="metric-value">{{ cpu_percent }}<span>%</span></div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill fill-cpu" style="width: {{ cpu_percent }}%;"></div>
            </div>
        </div>

        <!-- RAM Card -->
        <div class="metric-card">
            <div class="icon-wrapper icon-ram" style="background: linear-gradient(135deg, rgba(52, 211, 153, 0.2), rgba(16, 185, 129, 0.2)); border-color: rgba(52, 211, 153, 0.3);">
                <svg fill="none" viewBox="0 0 24 24" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 14.25h7.5M8.25 9.75h7.5m-10.5 6h13.5a2.25 2.25 0 002.25-2.25V6.75a2.25 2.25 0 00-2.25-2.25H4.5A2.25 2.25 0 002.25 6.75v10.5a2.25 2.25 0 002.25 2.25zm-2.25-9h18m-18 4.5h18" />
                </svg>
            </div>
            <div class="metric-name">Memory</div>
            <div class="metric-value">{{ memory_percent }}<span>%</span></div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill fill-ram" style="width: {{ memory_percent }}%;"></div>
            </div>
        </div>

        <!-- Disk Card -->
        <div class="metric-card">
            <div class="icon-wrapper icon-disk" style="background: linear-gradient(135deg, rgba(244, 114, 182, 0.2), rgba(225, 29, 72, 0.2)); border-color: rgba(244, 114, 182, 0.3);">
                <svg fill="none" viewBox="0 0 24 24" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125" />
                </svg>
            </div>
            <div class="metric-name">Disk Space</div>
            <div class="metric-value">{{ disk_percent }}<span>%</span></div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill fill-disk" style="width: {{ disk_percent }}%;"></div>
            </div>
        </div>
    </div>
    
    <a href="/" class="refresh-btn">Refresh Metrics</a>
</body>
</html>
"""

@app.route('/')
def dashboard():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return render_template_string(
        HTML_TEMPLATE,
        cpu_percent=cpu_percent,
        memory_percent=memory.percent,
        disk_percent=disk.percent
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
