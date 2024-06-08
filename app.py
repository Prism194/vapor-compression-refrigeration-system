from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    # Constants
    T0 = 298.15  # Reference temperature in Kelvin

    # Get user input
    Tev = float(request.form['Tev'])
    Tcond = float(request.form['Tcond'])
    h1 = float(request.form['h1'])
    h2 = float(request.form['h2'])
    h3 = float(request.form['h3'])
    h4 = float(request.form['h4'])
    s1 = float(request.form['s1'])
    s2 = float(request.form['s2'])
    s3 = float(request.form['s3'])
    s4 = float(request.form['s4'])
    mass_flow_rate = float(request.form['mass_flow_rate'])
    mech_efficiency = float(request.form['mech_eff'])
    elec_efficiency = float(request.form['elec_eff'])

    # Exergy destruction in evaporator
    Q_ev = mass_flow_rate * (h1 - h4)  # Heat addition in evaporator
    I_ev = mass_flow_rate * ((h4 - h1) - T0 * (s4 - s1)) + Q_ev * (1 - T0 / Tev)

    # Exergy destruction in compressor
    Wc = mass_flow_rate * (h2 - h1)  # Compressor work
    Wel = Wc / (mech_efficiency * elec_efficiency)  # Electrical power assuming efficiencies
    I_comp = mass_flow_rate * ((h1 - h2) - T0 * (s1 - s2)) + Wel

    # Exergy destruction in condenser
    Q_cond = mass_flow_rate * (h2 - h3)  # Heat rejection in condenser
    I_cond = mass_flow_rate * ((h2 - h3) - T0 * (s2 - s3)) - Q_cond * (1 - T0 / Tcond)

    # Exergy destruction in expansion valve
    I_exp = mass_flow_rate * (s4 - s3)  # Assuming h4 = h3 due to throttling

    # Total exergy destruction
    I_total = I_ev + I_comp + I_cond + I_exp

    # Coefficient of Performance (COP)
    COP = Q_ev / Wel

    # Exergy efficiency
    exergy_efficiency = ((h1 - h4) - T0 * (s1 - s4)) / Wel

    #Energy efficiency
    energy_efficiency = (h1 - h4) / Wel

    return render_template('results.html', 
                           I_ev=f"{I_ev:.2f}", 
                           I_comp=f"{I_comp:.2f}", 
                           I_cond=f"{I_cond:.2f}", 
                           I_exp=f"{I_exp:.2f}", 
                           I_total=f"{I_total:.2f}", 
                           exergy_efficiency=f"{exergy_efficiency:.2f}",
                           energy_efficiency=f"{energy_efficiency:.2f}", 
                           COP=f"{COP:.2f}")

if __name__ == '__main__':
    app.run(debug=True)
