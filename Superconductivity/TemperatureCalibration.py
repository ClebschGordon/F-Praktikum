import numpy as np



A_coeffs_high = [3.146631,1.257655,0.413923,0.091159,0.016349,0.001826,-0.004325,-0.004973,0,0]
B_high = 10.3
C_high = 1.9

A_coeffs_low = [1.392408,0.527153,0.166756,0.050988,0.026514,0.001975,-0.017976,0.005409,0.013259,0]
B_low = 5.6
C_low = 2.9


def pressure_to_temperature(pressure_mbar, above_threshold):
    """
    Calculate the temperature (in Kelvin) corresponding to a given pressure (in mBar) using the
    polynomial expansion formula with different sets of coefficients based on the temperature region.

    Parameters:
    - pressure_mbar: Pressure in mBar
    - above_threshold: Boolean indicating whether we are in the high-temperature region (True)
                       or low-temperature region (False)

    Returns:
    - Temperature in Kelvin
    """
    # Convert pressure from mBar to Pa (1 mBar = 100 Pa)
    pressure_pa = pressure_mbar * 100

    # Calculate the term (ln(p) - B) / C for both high and low temperature regions
    log_term_high = (np.log(pressure_pa) - B_high) / C_high
    log_term_low = (np.log(pressure_pa) - B_low) / C_low

    # Check if we are above or below the threshold temperature (using the boolean parameter)
    if above_threshold:
        # Use the high-temperature coefficients for T > threshold_temp
        temperature_k = A_coeffs_high[0]  # Start with A_0
        for i in range(1, len(A_coeffs_high)):
            temperature_k += A_coeffs_high[i] * log_term_high ** i
    else:
        # Use the low-temperature coefficients for T < threshold_temp
        temperature_k = A_coeffs_low[0]  # Start with A_0
        for i in range(1, len(A_coeffs_low)):
            temperature_k += A_coeffs_low[i] * log_term_low ** i

    return temperature_k
