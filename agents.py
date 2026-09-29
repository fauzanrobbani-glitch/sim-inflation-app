import numpy as np

class PaymentAdoptionAgent:
    """Agent 1: Menganalisis & menghitung dampak intervensi pada indikator Sistem Pembayaran."""
    def process_policy(self, qris_delta: float, cash_delta: float, baseline_qris: float, baseline_cash: float):
        new_qris = min(100.0, max(0.0, baseline_qris + qris_delta))
        new_cash = min(100.0, max(0.0, baseline_cash + cash_delta))
        
        # Velocity ratio: Semakin tinggi adopsi digital, kecepatan perputaran uang meningkat
        velocity_index = (new_qris * 1.2 + new_cash * 0.8) / 100.0
        return new_qris, new_cash, velocity_index

class CoreInflationAgent:
    """Agent 2: Memodelkan transmisi perputaran uang terhadap Inflasi Inti."""
    def calculate_inflation(self, baseline_inflation: float, velocity_index: float, seasonal_shock: float):
        # Transmisi sederhana: Kenaikan perputaran uang & shock musim (Nataru/Lebaran) mendorong inflasi inti
        demand_pull_effect = (velocity_index - 1.0) * 0.45
        shock_effect = seasonal_shock * 0.35
        
        simulated_inflation = baseline_inflation + demand_pull_effect + shock_effect
        simulated_inflation = max(0.5, round(simulated_inflation, 2))
        return simulated_inflation, demand_pull_effect, shock_effect

class StressTesterAgent:
    """Agent 3: Menilai tingkat risiko & batas ketahanan sistem ekonomi daerah."""
    def evaluate_risk(self, inflation: float, qris_level: float):
        if inflation > 3.5:
            status = "CRITICAL"
            color = "#FF4136"
            message = "Inflasi Inti terlalu tinggi! Daya beli masyarakat terancam tergerus."
        elif inflation > 2.8:
            status = "WARNING"
            color = "#FFDC00"
            message = "Inflasi Inti merambat naik. Perlu pengawasan pada sektor ritel & jasa."
        else:
            status = "STABLE"
            color = "#2ECC40"
            message = "Stabilitas Inflasi Inti terjaga dengan baik dalam rentang sasaran."
            
        system_resilience = "TINGGI" if qris_level > 65 else "SEDANG" if qris_level > 40 else "RENDAH"
        return status, color, message, system_resilience

class SimCityAdvisorAgent:
    """Agent 4: Narator / Penasihat Kota ala Game SimCity."""
    def generate_brief(self, city_name: str, status: str, inflation: float, qris: float, policy_name: str):
        briefs = {
            "STABLE": f"🏛️ **Walikota {city_name}!** Kebijakan *'{policy_name}'* berjalan sangat efektif! Adopsi digital mencapai **{qris:.1f}%** dan Inflasi Inti berada di level aman (**{inflation}% YoY**). Warga kota sangat puas!",
            "WARNING": f"⚠️ **Laporan Penasihat Kota:** Efisiensi pembayaran digital memicu lonjakan konsumsi lokal. Inflasi Inti merangkak naik ke **{inflation}% YoY**. Disarankan menambah literasi keuangan dan koordinasi pasar.",
            "CRITICAL": f"🚨 **Peringatan Krisis!** Perputaran uang dan ekspansi transaksi tidak terkendali! Inflasi Inti melonjak ke **{inflation}% YoY**. Intervensi pasokan dan stabilisasi harga mutlak diperlukan!"
        }
        return briefs.get(status, "Sistem berjalan normal.")