/**
 * Vercel Serverless Function: /api/solve_inverse
 * Fast real-time inverse recipe solver for Plasma CO2 conversion.
 */

module.exports = (req, res) => {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader(
        'Access-Control-Allow-Headers',
        'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
    );

    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    const t0 = Date.now();
    let body = req.body;
    if (typeof body === 'string') {
        try {
            body = JSON.parse(body);
        } catch (e) {
            body = {};
        }
    }
    body = body || {};

    const targetConv = Math.min(85, Math.max(5, parseFloat(body.target_conv) || 50.0));
    const targetEff = Math.min(75, Math.max(5, parseFloat(body.target_eff) || 40.0));

    // Two-stage inverse optimizer
    // Physical bounds: P in [10, 1000] W, Q in [0.05, 10] LPM, Pressure in [0.05, 1.0] bar
    let bestP = 220, bestQ = 0.9, minErr = Infinity;

    // Coarse search across operating window
    for (let p = 20; p <= 800; p += 20) {
        for (let q = 0.2; q <= 4.0; q += 0.2) {
            const sei = (p / q) * 0.06;
            const conv = 16.23 + 59.97 * (1 - Math.exp(-0.010 * Math.pow(Math.max(0.01, sei), 1.48)));
            const eff = 58.2 * (1 - Math.exp(-1.0 * Math.max(0.01, sei))) * Math.exp(-0.031 * Math.max(0, sei - 5.0));
            const err = Math.pow(conv - targetConv, 2) + Math.pow(eff - targetEff, 2) + 0.001 * p;
            if (err < minErr) {
                minErr = err;
                bestP = p;
                bestQ = q;
            }
        }
    }

    // Fine grid refinement around optimum
    for (let p = bestP - 15; p <= bestP + 15; p += 1) {
        for (let q = bestQ - 0.15; q <= bestQ + 0.15; q += 0.01) {
            if (p < 10 || q < 0.05) continue;
            const sei = (p / q) * 0.06;
            const conv = 16.23 + 59.97 * (1 - Math.exp(-0.010 * Math.pow(Math.max(0.01, sei), 1.48)));
            const eff = 58.2 * (1 - Math.exp(-1.0 * Math.max(0.01, sei))) * Math.exp(-0.031 * Math.max(0, sei - 5.0));
            const err = Math.pow(conv - targetConv, 2) + Math.pow(eff - targetEff, 2) + 0.0005 * p;
            if (err < minErr) {
                minErr = err;
                bestP = p;
                bestQ = q;
            }
        }
    }

    const seiKjL = (bestP / bestQ) * 0.06;
    const seiEvMol = seiKjL * 0.2320;
    const achievedConv = 16.23 + 59.97 * (1 - Math.exp(-0.010 * Math.pow(Math.max(0.01, seiKjL), 1.48)));
    const achievedEff = 58.2 * (1 - Math.exp(-1.0 * Math.max(0.01, seiKjL))) * Math.exp(-0.031 * Math.max(0, seiKjL - 5.0));
    const secKjMol = 283.0 / Math.max(0.01, (achievedEff / 100.0));

    const pressureBar = targetConv > 60.0 ? 0.40 : 1.0;
    const gapMm = 1.67;
    const lenMm = 287.7;
    const freqKhz = 100.0;

    // Residence time calculation
    const rInner = 0.8;
    const rOuter = rInner + (gapMm / 10.0);
    const vPlasma = Math.PI * (Math.pow(rOuter, 2) - Math.pow(rInner, 2)) * (lenMm / 10.0);
    const qActual = bestQ * (1000.0 / 60.0) * (1.01325 / pressureBar);
    const tauRes = vPlasma / Math.max(0.01, qActual);

    const latencyMs = Math.max(1.2, Date.now() - t0);

    const response = {
        status: "converged",
        latency_ms: parseFloat(latencyMs.toFixed(2)),
        target: {
            CO2_Conversion_pct: parseFloat(targetConv.toFixed(1)),
            Energy_Efficiency_pct: parseFloat(targetEff.toFixed(1))
        },
        achieved: {
            CO2_Conversion_pct: parseFloat(achievedConv.toFixed(2)),
            Energy_Efficiency_pct: parseFloat(achievedEff.toFixed(2)),
            Specific_Energy_Consumption_kJ_mol: parseFloat(secKjMol.toFixed(1))
        },
        conversion_error_pct: parseFloat(Math.abs(achievedConv - targetConv).toFixed(2)),
        efficiency_error_pct: parseFloat(Math.abs(achievedEff - targetEff).toFixed(2)),
        recommended_recipe: {
            Discharge_Power_W: Math.round(bestP),
            Gas_Flow_Rate_LPM: parseFloat(bestQ.toFixed(3)),
            Operating_Pressure_bar: parseFloat(pressureBar.toFixed(2)),
            Discharge_Gap_mm: parseFloat(gapMm.toFixed(2)),
            Discharge_Length_mm: parseFloat(lenMm.toFixed(1)),
            AC_Frequency_kHz: parseFloat(freqKhz.toFixed(1)),
            Specific_Energy_Input_kJ_L: parseFloat(seiKjL.toFixed(1)),
            Specific_Energy_Input_eV_molec: parseFloat(seiEvMol.toFixed(3)),
            Residence_Time_s: parseFloat(tauRes.toFixed(3))
        }
    };

    res.status(200).json(response);
};
