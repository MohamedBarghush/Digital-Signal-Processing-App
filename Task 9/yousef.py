import numpy as np

def calculate_window_type(stop_band_attenuation):
    if stop_band_attenuation <= 21:
        return "rectangular"
    elif stop_band_attenuation <= 44:
        return "hanning"
    elif stop_band_attenuation <= 53:
        return "hamming"
    elif stop_band_attenuation <= 74:
        return "blackman"
    else:
        raise ValueError("Stop band attenuation is too high. Choose a lower value.")

def window_function(window_type, n, N):
    if window_type == "rectangular":
        return 1
    elif window_type == "hanning":
        return 0.5 + (0.5 * np.cos((2 * np.pi * n) / N))
    elif window_type == "hamming":
        return 0.54 + (0.46 * np.cos((2 * np.pi * n) / N))
    elif window_type == "blackman":
        return 0.42 + (0.5 * np.cos(2 * np.pi * n / (N - 1))) + 0.08 * np.cos(4 * np.pi * n / (N - 1))

def calculate_samples(window_type, delta_f):
    if window_type == "rectangular":
        return int(np.ceil(0.9 / delta_f))
    elif window_type == "hanning":
        return int(np.ceil(3.1 / delta_f))
    elif window_type == "hamming":
        return int(np.ceil(3.3 / delta_f))
    elif window_type == "blackman":
        return int(np.ceil(5.5 / delta_f))

def design_filter(filter_type, FS, stop_band_attenuation, FC, FC2=None, transition_band=None):
    window_type = calculate_window_type(stop_band_attenuation)
    print("The window type is:", window_type)

    # Step 1: Define the filter type
    if filter_type not in ["low_pass", "high_pass", "band_pass", "band_reject"]:
        raise ValueError("Invalid filter type. Choose from 'low_pass', 'high_pass', 'band_pass', or 'band_reject'.")

    # Step 2: From stop band attenuation, define the window type
    if window_type not in ["rectangular", "hanning", "hamming", "blackman"]:
        raise ValueError("Invalid window type. Choose from 'rectangular', 'hanning', 'hamming', or 'blackman'.")

    # Step 3: Calculate N from transition width known from the window type
    if transition_band is None:
        raise ValueError("Transition band must be specified.")
    delta_f = transition_band / FS
    N = calculate_samples(window_type, delta_f) 
    if N %2 == 0:
        N += 1
    print("N=", N)

    # Step 4: Calculate the new cut-off frequency
    if filter_type == "low_pass":
        new_fc = FC + 0.5 * transition_band
        print("fc=", new_fc)

        # Normalize cut off frequency
        new_fc = new_fc / FS
        print("The normalized fc=", new_fc)

    elif filter_type == "high_pass":
        new_fc = FC - 0.5 * transition_band
        print("fc=", new_fc)

        # Normalize cut off frequency
        new_fc = new_fc / FS
        print("The normalized fc=", new_fc)

    

    elif filter_type == "band_pass":
        new_fc = FC - 0.5 * transition_band
        print("fc1=", new_fc)

        # Normalize cut off frequency
        new_fc = new_fc / FS
        print("The normalized fc1=", new_fc)
        if FC2 is None:
            raise ValueError("For band pass or, FC2 must be specified.")
        new_fc2 = FC2 + 0.5 * transition_band
        print ("fc2=", new_fc2)

        # Normalize cutt off frequency
        new_fc2 = new_fc2 / FS
        print("The normalized fc2=", new_fc2)


    elif filter_type == "band_reject":
        new_fc = FC + 0.5 * transition_band
        print("fc1=", new_fc)

        # Normalize cut off frequency
        new_fc = new_fc / FS
        print("The normalized fc1=", new_fc)
        if FC2 is None:
            raise ValueError("For band reject, FC2 must be specified.")
        new_fc2 = FC2 - 0.5 * transition_band
        print ("fc2=", new_fc2)

        # Normalize cutt off frequency
        new_fc2 = new_fc2 / FS
        print("The normalized fc2=", new_fc2)

    # Create the filter
    h = []

    for i in range(-N // 2 + 1, N // 2 + 1):
        n = i

        if filter_type == "low_pass":
            if i == 0:
                h.append(2 * new_fc)
            else:
                sinc_term = (((2 * new_fc * np.sin(n * 2 * np.pi * new_fc)) / (n * 2 * np.pi * new_fc)))  # Corrected sinc function
                h_value = sinc_term * window_function(window_type, n, N)
                h.append(h_value)

        elif filter_type == "high_pass":
            if i == 0:
                h_value= (1 - 2 * new_fc) * window_function(window_type, n, N)
                h.append(h_value)
            else:
                sinc_term = (((2 * new_fc * np.sin(n * 2 * np.pi * new_fc)) / (n * 2 * np.pi * new_fc)))  # Corrected sinc function
                h_value = -(sinc_term * window_function(window_type, n, N))
                h.append(h_value)

        elif filter_type == "band_pass":
            if i == 0:
                h_value= (2 * (new_fc2 - new_fc)) * window_function(window_type, n, N)
                h.append(h_value)
            else:
                sinc_term1 = (((2 * new_fc * np.sin(n * 2 * np.pi * new_fc)) / (n * 2 * np.pi * new_fc)))  # Corrected sinc function
                sinc_term2 = (((2 * new_fc2 * np.sin(n * 2 * np.pi * new_fc2)) / (n * 2 * np.pi * new_fc2)))  # Corrected sinc function
                total_sincs = sinc_term2 - sinc_term1
                h_value = total_sincs * window_function(window_type, n, N)
                h.append(h_value)

        elif filter_type == "band_reject":
            if i == 0:
                h_value= (1 - (2 * (new_fc2 - new_fc))) * window_function(window_type, n, N)
                h.append(h_value)
            else:
                sinc_term1 = (((2 * new_fc * np.sin(n * 2 * np.pi * new_fc)) / (n * 2 * np.pi * new_fc)))  # Corrected sinc function
                sinc_term2 = (((2 * new_fc2 * np.sin(n * 2 * np.pi * new_fc2)) / (n * 2 * np.pi * new_fc2)))  # Corrected sinc function
                total_sincs = sinc_term1 - sinc_term2
                h_value = total_sincs * window_function(window_type, n, N)
                h.append(h_value)

    # Print the indices and corresponding values
    for i in range(-N // 2 + 1, N // 2 + 1):
        n = i
        print(f"{n} {h[i + N // 2]}")

# Example usage:
design_filter("band_reject", FS=1000, stop_band_attenuation=60, FC=150,FC2=250, transition_band=50)
