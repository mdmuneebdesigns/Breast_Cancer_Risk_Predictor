from flask import Flask, render_template_string, request, jsonify
import requests
import json

app = Flask(__name__)

HTML_TEMPLATE = """<!DOCTYPE html>
<html class="light" lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Breast Cancer Risk Predictor - OncoGuard AI</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🩺</text></svg>">
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
    <script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "background": "#f8f9fa",
                        "outline": "#727783",
                        "primary-container": "#005dac",
                        "on-background": "#191c1d",
                        "surface": "#f8f9fa",
                        "on-primary-container": "#bfd7ff",
                        "on-background": "#191c1d",
                        "on-error": "#ffffff",
                        "surface-container-low": "#f3f4f5",
                        "outline-variant": "#c1c6d3",
                        "on-surface-variant": "#414751",
                        "on-tertiary-fixed": "#321200",
                        "on-primary-fixed": "#001c3a",
                        "primary": "#004583",
                        "on-primary": "#ffffff",
                        "surface-container-high": "#e7e8e9",
                        "brand-blue": "#005dac",
                        "brand-white": "#ffffff",
                        "brand-gray-light": "#dee2e6",
                        "brand-dark": "#191c1d",
                        "brand-red": "#dc3545",
                        "brand-green": "#28a745"
                    },
                    "fontFamily": {
                        "body-md": ["Inter"],
                        "body-lg": ["Inter"]
                    }
                }
            }
        }
    </script>
    <style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .material-symbols-outlined.fill {
            font-variation-settings: 'FILL' 1;
        }
        
        .tab-content { display: none; }
        .tab-content.active { display: grid; }
        
        .input-group {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .custom-input {
            width: 100%;
            border: 1px solid #343a40;
            border-radius: 0.125rem;
            padding: 8px 12px;
            font-family: 'Inter', sans-serif;
            font-size: 16px;
            color: #191c1d;
            background-color: #ffffff;
            transition: all 0.2s ease;
        }
        .custom-input:focus {
            outline: none;
            border-color: #005dac;
            box-shadow: 0 0 0 2px rgba(0, 93, 172, 0.2);
        }
        
        #loading-overlay {
            backdrop-filter: blur(4px);
        }
        .spinner {
            border: 4px solid rgba(0, 93, 172, 0.1);
            border-left-color: #005dac;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .hide-scrollbar {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        .hide-scrollbar::-webkit-scrollbar {
            display: none;
        }

        /* NEW STYLES for interactive colors */
        .gradient-text {
            background: linear-gradient(90deg, #005dac, #00a8cc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .hover-lift {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .hover-lift:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 20px rgba(0, 93, 172, 0.15);
        }
        .button-pulse:hover {
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 93, 172, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(0, 93, 172, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 93, 172, 0); }
        }
    </style>
</head>
<body class="bg-background text-on-background antialiased min-h-screen font-body-md flex flex-col md:flex-row">
<!-- Sidebar Navigation -->
<nav class="hidden md:flex bg-surface-container-low border-r border-outline-variant fixed left-0 top-0 h-screen w-64 flex-col z-40">
    <div class="p-6 border-b border-outline-variant">
        <h1 class="font-bold text-xl text-on-surface flex items-center gap-2">
            <span class="material-symbols-outlined text-primary">health_and_safety</span>
            Medical Portal
        </h1>
        <p class="text-sm text-on-surface-variant mt-1">Diagnostic Unit A</p>
    </div>
    <div class="flex-1 py-4 px-4">
        <ul class="flex flex-col gap-1">
            <li>
                <a class="flex items-center gap-3 px-4 py-3 rounded text-primary font-bold border-r-4 border-primary bg-surface-container-high" href="#">
                    <span class="material-symbols-outlined fill">add_chart</span>
                    <span>New Prediction</span>
                </a>
            </li>
        </ul>
    </div>
    <div class="p-6 border-t border-outline-variant space-y-4">
        <button onclick="predictRisk()" class="w-full bg-gradient-to-r from-primary to-blue-500 text-on-primary py-3 rounded flex justify-center items-center gap-2 hover:from-blue-600 hover:to-blue-700 transition-all shadow-md button-pulse font-bold">
            <span class="material-symbols-outlined">science</span>
            Predict Risk
        </button>
    </div>
</nav>

<!-- Main Content -->
<main class="flex-1 md:ml-64 flex flex-col min-h-screen">
    <header class="md:hidden bg-surface border-b border-outline-variant fixed top-0 w-full z-50 flex justify-between items-center px-4 h-16">
        <h1 class="font-bold text-xl text-primary">OncoGuard AI</h1>
    </header>

    <div class="flex-1 mt-16 md:mt-0 p-4 md:p-12 grid grid-cols-1 lg:grid-cols-12 gap-6 max-w-7xl mx-auto w-full">
        <!-- Main Form -->
        <div class="lg:col-span-8 space-y-8">
            <header class="border-b-2 border-brand-dark pb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div class="space-y-2">
                    <h2 class="font-bold text-3xl text-on-background flex items-center gap-3">
                        <div class="bg-gradient-to-tr from-primary to-blue-400 p-2 rounded-lg text-white shadow-lg flex items-center justify-center">
                            <span class="material-symbols-outlined" style="font-size: 32px;">local_hospital</span>
                        </div>
                        <span class="gradient-text">Breast Cancer Risk Predictor</span>
                    </h2>
                    <p class="text-xl text-on-surface-variant">AI-Powered Diagnostic Tool</p>
                    <p class="text-base text-outline">Get instant predictions using advanced ML models based on cytological features.</p>
                </div>
                <div class="bg-gradient-to-br from-green-50 to-green-100 border border-green-200 px-5 py-3 rounded-xl shadow-sm flex flex-col items-center justify-center transform hover:scale-105 transition-transform cursor-default">
                    <span class="text-xs text-green-700 font-bold uppercase tracking-wider mb-1">Model Accuracy</span>
                    <span class="text-2xl font-black text-green-600 flex items-center gap-1 drop-shadow-sm">
                        <span class="material-symbols-outlined text-green-500" style="font-size: 24px;">verified</span>
                        99.12%
                    </span>
                </div>
            </header>

            <section class="bg-brand-white border border-brand-gray-light rounded shadow-sm p-6 relative hover-lift transition-all">
                <!-- Tabs -->
                <div class="flex border-b border-outline-variant mb-6 overflow-x-auto hide-scrollbar">
                    <button class="tab-btn px-6 py-3 text-primary border-b-2 border-primary whitespace-nowrap font-semibold" id="tab-btn-mean" onclick="switchTab('mean')">Mean Values</button>
                    <button class="tab-btn px-6 py-3 text-on-surface-variant border-b-2 border-transparent whitespace-nowrap font-semibold" id="tab-btn-se" onclick="switchTab('se')">SE Values</button>
                    <button class="tab-btn px-6 py-3 text-on-surface-variant border-b-2 border-transparent whitespace-nowrap font-semibold" id="tab-btn-worst" onclick="switchTab('worst')">Worst Values</button>
                </div>

                <form class="space-y-8" id="prediction-form">
                    <!-- Mean Values Tab -->
                    <div class="tab-content active grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4" id="tab-mean">
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="radius_mean">Radius Mean</label>
                            <input class="custom-input" id="radius_mean" name="radius_mean" placeholder="0.00" step="any" type="number" required/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="texture_mean">Texture Mean</label>
                            <input class="custom-input" id="texture_mean" name="texture_mean" placeholder="0.00" step="any" type="number" required/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="perimeter_mean">Perimeter Mean</label>
                            <input class="custom-input" id="perimeter_mean" name="perimeter_mean" placeholder="0.00" step="any" type="number" required/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="area_mean">Area Mean</label>
                            <input class="custom-input" id="area_mean" name="area_mean" placeholder="0.00" step="any" type="number" required/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="smoothness_mean">Smoothness Mean</label>
                            <input class="custom-input" id="smoothness_mean" name="smoothness_mean" placeholder="0.00" step="any" type="number" required/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="compactness_mean">Compactness Mean</label>
                            <input class="custom-input" id="compactness_mean" name="compactness_mean" placeholder="0.00" step="any" type="number" required/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="concavity_mean">Concavity Mean</label>
                            <input class="custom-input" id="concavity_mean" name="concavity_mean" placeholder="0.00" step="any" type="number" required/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="concave_points_mean">Concave Points Mean</label>
                            <input class="custom-input" id="concave_points_mean" name="concave_points_mean" placeholder="0.00" step="any" type="number" required/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="symmetry_mean">Symmetry Mean</label>
                            <input class="custom-input" id="symmetry_mean" name="symmetry_mean" placeholder="0.00" step="any" type="number" required/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="fractal_dimension_mean">Fractal Dimension Mean</label>
                            <input class="custom-input" id="fractal_dimension_mean" name="fractal_dimension_mean" placeholder="0.00" step="any" type="number" required/>
                        </div>
                    </div>

                    <!-- SE Values Tab -->
                    <div class="tab-content grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4" id="tab-se">
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="radius_se">Radius SE</label>
                            <input class="custom-input" id="radius_se" name="radius_se" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="texture_se">Texture SE</label>
                            <input class="custom-input" id="texture_se" name="texture_se" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="perimeter_se">Perimeter SE</label>
                            <input class="custom-input" id="perimeter_se" name="perimeter_se" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="area_se">Area SE</label>
                            <input class="custom-input" id="area_se" name="area_se" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="smoothness_se">Smoothness SE</label>
                            <input class="custom-input" id="smoothness_se" name="smoothness_se" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="compactness_se">Compactness SE</label>
                            <input class="custom-input" id="compactness_se" name="compactness_se" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="concavity_se">Concavity SE</label>
                            <input class="custom-input" id="concavity_se" name="concavity_se" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="concave_points_se">Concave Points SE</label>
                            <input class="custom-input" id="concave_points_se" name="concave_points_se" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="symmetry_se">Symmetry SE</label>
                            <input class="custom-input" id="symmetry_se" name="symmetry_se" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="fractal_dimension_se">Fractal Dimension SE</label>
                            <input class="custom-input" id="fractal_dimension_se" name="fractal_dimension_se" placeholder="0.00" step="any" type="number"/>
                        </div>
                    </div>

                    <!-- Worst Values Tab -->
                    <div class="tab-content grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4" id="tab-worst">
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="radius_worst">Radius Worst</label>
                            <input class="custom-input" id="radius_worst" name="radius_worst" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="texture_worst">Texture Worst</label>
                            <input class="custom-input" id="texture_worst" name="texture_worst" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="perimeter_worst">Perimeter Worst</label>
                            <input class="custom-input" id="perimeter_worst" name="perimeter_worst" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="area_worst">Area Worst</label>
                            <input class="custom-input" id="area_worst" name="area_worst" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="smoothness_worst">Smoothness Worst</label>
                            <input class="custom-input" id="smoothness_worst" name="smoothness_worst" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="compactness_worst">Compactness Worst</label>
                            <input class="custom-input" id="compactness_worst" name="compactness_worst" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="concavity_worst">Concavity Worst</label>
                            <input class="custom-input" id="concavity_worst" name="concavity_worst" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="concave_points_worst">Concave Points Worst</label>
                            <input class="custom-input" id="concave_points_worst" name="concave_points_worst" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="symmetry_worst">Symmetry Worst</label>
                            <input class="custom-input" id="symmetry_worst" name="symmetry_worst" placeholder="0.00" step="any" type="number"/>
                        </div>
                        <div class="input-group">
                            <label class="font-semibold text-sm" for="fractal_dimension_worst">Fractal Dimension Worst</label>
                            <input class="custom-input" id="fractal_dimension_worst" name="fractal_dimension_worst" placeholder="0.00" step="any" type="number"/>
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div class="flex flex-wrap gap-4 pt-6 border-t border-brand-dark mt-8">
                        <button class="bg-brand-blue text-brand-white px-6 py-2 rounded flex items-center gap-2 hover:bg-primary transition-colors font-semibold" onclick="loadBenignSample()" type="button">
                            <span class="material-symbols-outlined">download</span>
                            Load Benign Sample
                        </button>
                        <button class="bg-brand-red text-brand-white px-6 py-2 rounded flex items-center gap-2 hover:opacity-90 transition-colors font-semibold" onclick="loadMalignantSample()" type="button">
                            <span class="material-symbols-outlined">download</span>
                            Load Malignant Sample
                        </button>
                        <button class="border border-brand-blue text-brand-blue px-6 py-2 rounded hover:bg-surface-container-highest transition-colors font-semibold" onclick="clearForm()" type="button">
                            <span class="material-symbols-outlined">refresh</span>
                            Clear Form
                        </button>
                    </div>
                </form>

                <!-- Loading Overlay -->
                <div class="hidden absolute inset-0 bg-white/80 flex-col justify-center items-center z-10 rounded" id="loading-overlay">
                    <div class="spinner mb-4"></div>
                    <p class="font-semibold text-brand-blue text-lg">Analyzing cytological data...</p>
                    <p class="text-sm text-outline mt-2">Connecting to Inference API</p>
                </div>
            </section>

            <!-- Results Section -->
            <section class="hidden" id="results-section">
                <h3 class="font-bold text-2xl text-on-background mb-4">Diagnostic Result</h3>
                <div class="bg-brand-white border border-brand-gray-light p-6 shadow-sm relative overflow-hidden" id="result-card">
                    <div class="absolute left-0 top-0 bottom-0 w-1 bg-brand-blue" id="result-accent"></div>
                    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 ml-2">
                        <div>
                            <p class="font-semibold text-sm text-outline mb-1">AI Prediction</p>
                            <h4 class="font-bold text-2xl text-brand-blue flex items-center gap-2" id="result-diagnosis">
                                <span class="material-symbols-outlined">info</span>
                                Awaiting Data
                            </h4>
                        </div>
                        <div class="text-right">
                            <p class="font-semibold text-sm text-outline mb-1">Confidence Score</p>
                            <p class="font-bold text-2xl text-on-background" id="result-confidence">--%</p>
                        </div>
                    </div>
                    <div class="mt-6 pt-4 border-t border-outline-variant grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <span class="text-outline">Model Version:</span>
                            <span class="font-semibold text-on-background ml-2">v2.4.1 (Ensemble)</span>
                        </div>
                        <div class="text-right">
                            <span class="text-outline">Timestamp:</span>
                            <span class="font-semibold text-on-background ml-2" id="result-timestamp">--:--:--</span>
                        </div>
                    </div>
                </div>
            </section>
        </div>

        <!-- Sidebar / History -->
        <div class="lg:col-span-4 space-y-6">
            <div class="bg-brand-white border border-brand-gray-light rounded shadow-sm h-full max-h-96 flex flex-col">
                <div class="p-4 border-b-2 border-brand-dark flex justify-between items-center bg-surface-container-low">
                    <h3 class="font-bold text-lg text-on-background flex items-center gap-2">
                        <span class="material-symbols-outlined">history</span>
                        Recent Predictions
                    </h3>
                </div>
                <div class="flex-1 overflow-y-auto p-4 space-y-4" id="history-container">
                    <p class="text-sm text-on-surface-variant">No predictions yet</p>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="lg:col-span-12 mt-8 pt-6 pb-2 text-center border-t border-outline-variant">
            <p class="text-base font-medium text-on-surface-variant">
                Created by <span class="text-primary font-bold">Muneeb</span> &copy; 2026
            </p>
            <p class="text-xs text-outline mt-1">Empowering Healthcare with AI</p>
        </footer>
    </div>
</main>

<script>
    const benignSample = {
        radius_mean: 12.45, texture_mean: 15.6, perimeter_mean: 82.1, area_mean: 480,
        smoothness_mean: 0.086, compactness_mean: 0.097, concavity_mean: 0.048,
        concave_points_mean: 0.053, symmetry_mean: 0.158, fractal_dimension_mean: 0.058,
        radius_se: 0.542, texture_se: 0.673, perimeter_se: 3.8, area_se: 51.3,
        smoothness_se: 0.0056, compactness_se: 0.009, concavity_se: 0.006,
        concave_points_se: 0.004, symmetry_se: 0.0089, fractal_dimension_se: 0.0022,
        radius_worst: 14.2, texture_worst: 21.3, perimeter_worst: 92.1, area_worst: 630,
        smoothness_worst: 0.125, compactness_worst: 0.195, concavity_worst: 0.090,
        concave_points_worst: 0.087, symmetry_worst: 0.281, fractal_dimension_worst: 0.091
    };

    const malignantSample = {
        radius_mean: 17.99, texture_mean: 10.38, perimeter_mean: 122.8, area_mean: 1001,
        smoothness_mean: 0.11840, compactness_mean: 0.27760, concavity_mean: 0.3001,
        concave_points_mean: 0.14710, symmetry_mean: 0.2419, fractal_dimension_mean: 0.07871,
        radius_se: 1.095, texture_se: 0.9053, perimeter_se: 8.589, area_se: 153.4,
        smoothness_se: 0.006399, compactness_se: 0.04904, concavity_se: 0.05373,
        concave_points_se: 0.01587, symmetry_se: 0.03003, fractal_dimension_se: 0.002842,
        radius_worst: 25.38, texture_worst: 17.33, perimeter_worst: 184.6, area_worst: 2019,
        smoothness_worst: 0.1622, compactness_worst: 0.6656, concavity_worst: 0.7119,
        concave_points_worst: 0.2654, symmetry_worst: 0.4601, fractal_dimension_worst: 0.11890
    };

    function switchTab(tabId) {
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('text-primary', 'border-primary');
            btn.classList.add('text-on-surface-variant', 'border-transparent');
        });
        
        document.getElementById(`tab-${tabId}`).classList.add('active');
        const activeBtn = document.getElementById(`tab-btn-${tabId}`);
        activeBtn.classList.remove('text-on-surface-variant', 'border-transparent');
        activeBtn.classList.add('text-primary', 'border-primary');
    }

    function fillForm(data) {
        Object.keys(data).forEach(key => {
            const input = document.getElementById(key);
            if (input) input.value = data[key];
        });
    }

    function loadBenignSample() {
        fillForm(benignSample);
        showNotification('✅ Benign sample data loaded!', 'success');
    }

    function loadMalignantSample() {
        fillForm(malignantSample);
        showNotification('⚠️ Malignant sample data loaded!', 'warning');
    }

    function clearForm() {
        document.getElementById('prediction-form').reset();
        document.getElementById('results-section').classList.add('hidden');
        showNotification('✓ Form cleared!', 'info');
    }

    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 px-4 py-3 rounded text-white text-sm font-semibold ${type === 'success' ? 'bg-brand-green' : type === 'warning' ? 'bg-brand-red' : 'bg-brand-blue'} z-50 shadow-lg`;
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }

    async function predictRisk() {
        const overlay = document.getElementById('loading-overlay');
        const resultsSection = document.getElementById('results-section');
        
        try {
            overlay.classList.remove('hidden');
            overlay.classList.add('flex');

            const formData = new FormData(document.getElementById('prediction-form'));
            const data = Object.fromEntries(formData);
            
            Object.keys(data).forEach(key => {
                data[key] = parseFloat(data[key]) || 0;
            });

            const response = await fetch('/predict', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });

            if (!response.ok) throw new Error('API Error');
            
            const result = await response.json();
            displayResult(result);
            updateHistory(result);
            resultsSection.classList.remove('hidden');
            setTimeout(() => resultsSection.scrollIntoView({ behavior: 'smooth' }), 100);

        } catch (error) {
            showNotification('❌ Prediction failed: ' + error.message, 'warning');
        } finally {
            overlay.classList.add('hidden');
            overlay.classList.remove('flex');
        }
    }

    function updateHistory(result) {
        const historyContainer = document.getElementById('history-container');
        const emptyMsg = historyContainer.querySelector('p.text-on-surface-variant');
        if (emptyMsg && emptyMsg.textContent.includes('No predictions yet')) {
            emptyMsg.remove();
        }

        const prediction = result.prediction || 0;
        const confidence = parseFloat(result.confidence).toFixed(1);
        const time = new Date().toLocaleTimeString();
        
        let statusHtml = '';
        if (prediction === 1) {
            statusHtml = `<span class="text-brand-red font-bold">Malignant</span>`;
        } else {
            statusHtml = `<span class="text-brand-green font-bold">Benign</span>`;
        }

        const historyItem = document.createElement('div');
        historyItem.className = 'p-3 bg-surface border border-outline-variant rounded shadow-sm text-sm flex justify-between items-center';
        historyItem.innerHTML = `
            <div>
                <p class="font-semibold text-on-background">${statusHtml}</p>
                <p class="text-xs text-outline">${time}</p>
            </div>
            <div class="text-right">
                <p class="font-bold text-on-background">${confidence}%</p>
                <p class="text-xs text-outline">Confidence</p>
            </div>
        `;
        
        historyContainer.prepend(historyItem);
    }

    function displayResult(result) {
        const resultDiagnosis = document.getElementById('result-diagnosis');
        const resultConfidence = document.getElementById('result-confidence');
        const resultAccent = document.getElementById('result-accent');
        const timestamp = document.getElementById('result-timestamp');

        const prediction = result.prediction || 0;
        const confidence = parseFloat(result.confidence).toFixed(1);
        
        timestamp.textContent = new Date().toLocaleTimeString();
        resultConfidence.textContent = `${confidence}%`;

        if (prediction === 1) {
            resultDiagnosis.innerHTML = `<span class="material-symbols-outlined">warning</span> High Risk: Malignant`;
            resultDiagnosis.className = 'font-bold text-2xl text-brand-red flex items-center gap-2';
            resultAccent.className = 'absolute left-0 top-0 bottom-0 w-2 bg-brand-red';
        } else {
            resultDiagnosis.innerHTML = `<span class="material-symbols-outlined">check_circle</span> Low Risk: Benign`;
            resultDiagnosis.className = 'font-bold text-2xl text-brand-green flex items-center gap-2';
            resultAccent.className = 'absolute left-0 top-0 bottom-0 w-1 bg-brand-green';
        }
    }
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    """Proxy API calls to the backend"""
    try:
        data = request.json
        response = requests.post('http://localhost:8000/predict', json=data)
        return response.json()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
