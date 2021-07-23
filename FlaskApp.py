# -*- coding: utf-8 -*-
import numpy as np
from flask import Flask, request, flash, redirect, render_template
import os
import pandas as pd

UPLOAD_FOLDER = 'datasets'
MEASUREMENTS_FILENAME = "measurements.csv"
CRITICAL_FEA_FILENAME = "critical_features.csv"
ALLOWED_EXTENSIONS = {'csv'}

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload-datasets', methods=['POST'])
def upload_datasets():
    file_measurements = request.files['measurements_file']
    file_critical_fea = request.files['critical_features_file']
    if file_measurements.filename == '':
        flash('No selected measurements file')
        return redirect(request.url)

    if file_critical_fea.filename == '':
        flash('No selected critical features file')
        return redirect(request.url)

    # save measurements dataset
    # filename_measurements = secure_filename(file_measurements.filename)
    file_measurements.save(os.path.join(app.config['UPLOAD_FOLDER'], MEASUREMENTS_FILENAME))

    # save critical features dataset
    # filename_critical_fea = secure_filename(file_critical_fea.filename)
    file_critical_fea.save(os.path.join(app.config['UPLOAD_FOLDER'], CRITICAL_FEA_FILENAME))

    return redirect('/feature-selection')


@app.route('/feature-selection')
def feature_selection():
    df_measurements = pd.read_csv(os.path.join(UPLOAD_FOLDER, MEASUREMENTS_FILENAME), header=2)
    # Remove empty columns
    # df_measures.dropna(how='all', axis=1, inplace=True)
    # Get all combination of features
    features = df_measurements.columns[3:].tolist()
    # Compare features each other with the same axis
    fea_xaxis = list(filter(lambda f: f.endswith('[X]'), features))
    fea_yaxis = list(filter(lambda f: f.endswith('[Y]'), features))
    fea_zaxis = list(filter(lambda f: f.endswith('[Z]'), features))
    # Compare only error features
    fea_errors = list(filter(lambda f: f.endswith('[err]'), features))

    return render_template('feature_selection.html', fea_xaxis=fea_xaxis,
                           fea_yaxis=fea_yaxis, fea_zaxis=fea_zaxis, fea_errors=fea_errors)

@app.route('/dashboard', methods=['POST'])
def dashboard():
    fea_xaxis = request.form.getlist('fea_xaxis')
    fea_yaxis = request.form.getlist('fea_yaxis')
    fea_zaxis = request.form.getlist('fea_zaxis')
    fea_errors = request.form.getlist('fea_errors')

    return render_template('dashboard.html', fea_xaxis=fea_xaxis,
                           fea_yaxis=fea_yaxis, fea_zaxis=fea_zaxis, fea_errors=fea_errors)


if __name__=='__main__':
    app.run()