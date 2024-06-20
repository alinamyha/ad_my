from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.models import Slider, CheckboxGroup, Button, TextInput, Div, Toggle
from bokeh.themes import Theme
import numpy as np
import random

def harmonic(t, amplitude, frequency, phase):
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)

def create_noise(t, noise_mean, noise_std):
    return np.random.normal(noise_mean, noise_std, len(t))

def harmonic_with_noise(t, amplitude, frequency, phase=0, noise_mean=0, noise_std=0.1, noise=None):
    harmonic_signal = harmonic(t, amplitude, frequency, phase)
    if noise is not None:
        return harmonic_signal + noise
    else:
        global noise_g
        noise_g = create_noise(t, noise_mean, noise_std)
        return harmonic_signal + noise_g

def moving_avg(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='same')

# Initial parameters
initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_std = 0.1

t = np.linspace(0, 10, 1000)

plot = figure(title="Harmonic Signal with Noise and Moving Average Filter",
              x_axis_label='Time', y_axis_label='Amplitude',
              width=1200, height=600, background_fill_color='#2e2e2e', border_fill_color='#2e2e2e')

harmonic_line = plot.line(t, harmonic(t, initial_amplitude, initial_frequency, initial_phase),
                          line_width=2, color='blue', legend_label='Harmonic line')

with_noise_line = plot.line(t, harmonic_with_noise(t, initial_amplitude, initial_frequency, initial_phase,
                                                   initial_noise_mean, initial_noise_std),
                            line_width=2, color='red', legend_label='Signal with noise')

filtered_signal = moving_avg(with_noise_line.data_source.data['y'], 5)
filtered_line = plot.line(t, filtered_signal, line_width=2, color='green', legend_label='Filtered Signal')

plot.legend.label_text_color = "white"
plot.legend.background_fill_color = "#2e2e2e"
plot.legend.border_line_color = None
plot.xaxis.axis_label_text_color = "white"
plot.yaxis.axis_label_text_color = "white"
plot.xaxis.major_label_text_color = "white"
plot.yaxis.major_label_text_color = "white"
plot.title.text_color = "white"

# Widgets
s_amplitude = Slider(title="Amplitude", value=initial_amplitude, start=0.1, end=10.0, step=0.1, bar_color='blue')
s_frequency = Slider(title="Frequency", value=initial_frequency, start=0.1, end=10.0, step=0.1, bar_color='blue')
s_phase = Slider(title="Phase", value=initial_phase, start=0.0, end=2 * np.pi, step=0.1, bar_color='blue')
s_noise_mean = Slider(title="Noise Mean", value=initial_noise_mean, start=-1.0, end=1.0, step=0.1, bar_color='red')
s_noise_std = Slider(title="Noise Std Dev", value=initial_noise_std, start=0.0, end=1.0, step=0.1, bar_color='red')
s_window_size = Slider(title="Moving Average Window Size", value=5, start=1, end=50, step=1, bar_color='green')

cb_show_noise = CheckboxGroup(labels=['Show Noise'], active=[0], css_classes=['custom-checkbox'])
button_regenerate_noise = Button(label='Regenerate Noise', button_type='success', css_classes=['custom-button'])
button_random_params = Button(label='Random Params', button_type='warning', css_classes=['custom-button'])
button_reset = Button(label='Reset', button_type='danger', css_classes=['custom-button'])
input_title = TextInput(value='Harmonic Signal with Noise and Moving Average Filter', title='Plot Title:', css_classes=['custom-input'])
title_div = Div(text=f"<h2 style='color:white;'>{input_title.value}</h2>")

toggle_theme = Toggle(label="Toggle Light/Dark Theme", button_type="default", css_classes=['custom-toggle'])

def update(attr, old, new):
    amplitude = s_amplitude.value
    frequency = s_frequency.value
    phase = s_phase.value
    noise_mean = s_noise_mean.value
    noise_std = s_noise_std.value
    window_size = s_window_size.value

    harmonic_line.data_source.data['y'] = harmonic(t, amplitude, frequency, phase)
    with_noise_line.data_source.data['y'] = harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_std)
    filtered_signal = moving_avg(with_noise_line.data_source.data['y'], window_size)
    filtered_line.data_source.data['y'] = filtered_signal

    plot.title.text = input_title.value
    title_div.text = f"<h2 style='color:white;'>{input_title.value}</h2>"

def regenerate_noise():
    noise_mean = s_noise_mean.value
    noise_std = s_noise_std.value
    noise_g = create_noise(t, noise_mean, noise_std)
    update(None, None, None)

def random_params():
    s_amplitude.value = random.uniform(0.1, 10.0)
    s_frequency.value = random.uniform(0.1, 10.0)
    s_phase.value = random.uniform(0.0, 2 * np.pi)
    s_noise_mean.value = random.uniform(-1.0, 1.0)
    s_noise_std.value = random.uniform(0.0, 1.0)
    regenerate_noise()

def reset_params():
    s_amplitude.value = initial_amplitude
    s_frequency.value = initial_frequency
    s_phase.value = initial_phase
    s_noise_mean.value = initial_noise_mean
    s_noise_std.value = initial_noise_std
    s_window_size.value = 5
    input_title.value = 'Harmonic Signal with Noise and Moving Average Filter'
    regenerate_noise()

def toggle_light_dark_theme(active):
    if active:
        curdoc().theme = Theme(json={'attrs': {'Figure': {'background_fill_color': '#ffffff',
                                                          'border_fill_color': '#ffffff',
                                                          'outline_line_color': '#000000'},
                                               'Axis': {'major_label_text_color': '#000000',
                                                        'axis_label_text_color': '#000000',
                                                        'major_tick_line_color': '#000000',
                                                        'minor_tick_line_color': '#000000',
                                                        'axis_line_color': '#000000'},
                                               'Title': {'text_color': '#000000'},
                                               'Legend': {'background_fill_color': '#ffffff',
                                                          'border_line_color': '#000000',
                                                          'label_text_color': '#000000'}}})
    else:
        curdoc().theme = Theme(json={'attrs': {'Figure': {'background_fill_color': '#2e2e2e',
                                                          'border_fill_color': '#2e2e2e',
                                                          'outline_line_color': '#ffffff'},
                                               'Axis': {'major_label_text_color': '#ffffff',
                                                        'axis_label_text_color': '#ffffff',
                                                        'major_tick_line_color': '#ffffff',
                                                        'minor_tick_line_color': '#ffffff',
                                                        'axis_line_color': '#ffffff'},
                                               'Title': {'text_color': '#ffffff'},
                                               'Legend': {'background_fill_color': '#2e2e2e',
                                                          'border_line_color': None,
                                                          'label_text_color': '#ffffff'}}})

s_amplitude.on_change('value', update)
s_frequency.on_change('value', update)
s_phase.on_change('value', update)
s_noise_mean.on_change('value', update)
s_noise_std.on_change('value', update)
s_window_size.on_change('value', update)
input_title.on_change('value', update)

button_regenerate_noise.on_click(regenerate_noise)
button_random_params.on_click(random_params)
button_reset.on_click(reset_params)
toggle_theme.on_click(toggle_light_dark_theme)

layout = column(title_div, plot,
                column(s_amplitude, s_frequency, s_phase, s_noise_mean, s_noise_std, s_window_size, css_classes=['custom-widgetbox']),
                row(cb_show_noise, button_regenerate_noise, button_random_params, button_reset, toggle_theme, css_classes=['custom-row']),
                input_title,
                sizing_mode='stretch_width')

curdoc().add_root(layout)
curdoc().title = "Signal Processing Interactive Tool"

curdoc().template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{{ title if title else "Bokeh Application" }}</title>
    <style>
        body {
            background-color: #2e2e2e;
            color: white;
        }
        .bk-root .bk-slider-horizontal .bk-bar {
            background: blue;
        }
        .bk-root .bk-checkbox-group .bk-input-group {
            color: white;
        }
        .bk-root .custom-checkbox .bk-checkbox-label {
            color: white;
        }
        .bk-root .custom-button .bk-btn {
            color: white;
            background: blue;
            border-color: white;
        }
        .bk-root .custom-button .bk-btn.bk-btn-success {
            background: green;
        }
        .bk-root .custom-button .bk-btn.bk-btn-warning {
            background: orange;
        }
        .bk-root .custom-button .bk-btn.bk-btn-danger {
            background: red;
        }
        .bk-root .custom-input .bk-input {
            color: white;
            background: #1c1c1c;
        }
        .bk-root .custom-toggle .bk-btn-default {
            color: white;
            background: #444444;
        }
        .bk-root .custom-widgetbox .bk-widget {
            background: #3e3e3e;
            border: 1px solid #ffffff;
        }
        .bk-root .custom-row .bk-widget {
            margin: 5px;
        }
    </style>
</head>
<body>
    {{ plot_div|indent(8) }}
    {{ plot_script|indent(8) }}
</body>
</html>
"""
